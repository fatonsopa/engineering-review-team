"""Read-only source capture and structural report validation, not AI judgment."""

import argparse
import hashlib
import json
import os
import stat
import uuid
from pathlib import Path, PurePosixPath

MAX_BYTES = 2 * 1024 * 1024


class Invalid(ValueError):
    pass


def need(value, reason):
    if not value:
        raise Invalid(reason)


def load(path):
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream)


def save(path, value, root):
    path = Path(path).absolute()
    need(not path.resolve().is_relative_to(root), "Evidence must be outside the reviewed target")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")


def source(root, name):
    p = PurePosixPath(name)
    need(isinstance(name, str) and name and not p.is_absolute()
         and ".." not in p.parts and "\\" not in name, "Source path leaves selected root")
    path = root.joinpath(*p.parts)
    need(not any(x.is_symlink() for x in [path, *path.parents] if x != root.parent),
         "Source symlinks are unsupported")
    need(path.resolve().is_relative_to(root), "Source is outside selected root")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        need(stat.S_ISREG(before.st_mode) and not before.st_mode & 0o022,
             "Source must be a protected regular file")
        raw = stream.read(MAX_BYTES + 1)
        after = os.fstat(stream.fileno())
        identity = lambda info: (info.st_dev, info.st_ino, info.st_uid, info.st_mode,
                                 info.st_size, info.st_mtime_ns, info.st_ctime_ns)
        need(identity(before) == identity(after) and len(raw) <= MAX_BYTES, "Source changed or exceeds read limit")
    text = raw.decode("utf-8")
    return {"sha256": hashlib.sha256(raw).hexdigest(), "lines": len(text.splitlines()), "text": text}


def capture(root, paths, implementer, reviewer, requested_model=None, requested_effort=None):
    root = Path(root).absolute()
    need(root.is_dir() and root.resolve() == root, "A real explicit source root is required")
    need(implementer and reviewer and implementer != reviewer,
         "Lead must name a reviewer distinct from the implementer")
    need(0 < len(paths) <= 64 and len(set(paths)) == len(paths), "Select 1..64 distinct files")
    return {"version": 1, "capture_id": str(uuid.uuid4()), "root": str(root),
            "implementer": implementer, "reviewer": reviewer,
            "requested_model": requested_model, "requested_effort": requested_effort,
            "files": {name: source(root, name) for name in paths},
            "limits": "Participant/model fields are recorded claims, not authentication or quality proof."}


def current(snapshot):
    need(snapshot.get("version") == 1 and snapshot.get("files"), "A source capture is required")
    root = Path(snapshot["root"])
    for name, old in snapshot["files"].items():
        now = source(root, name)
        need(now == old, "Selected source drifted: " + name)
    return root


def inspect(snapshot, inspected, notes):
    current(snapshot)
    need(set(inspected) == set(snapshot["files"]) and notes.strip(),
         "Declare inspected scope and limitations before reporting")
    return {"capture_id": snapshot["capture_id"], "reviewer": snapshot["reviewer"],
            "inspected": sorted(inspected), "notes": notes,
            "limits": "This records an inspection claim; it does not prove AI reasoning."}


def validate(snapshot, inspection, report):
    current(snapshot)
    need(inspection.get("capture_id") == snapshot["capture_id"]
         and inspection.get("reviewer") == snapshot["reviewer"]
         and set(inspection.get("inspected", [])) == set(snapshot["files"]),
         "A matching prior inspection is required")
    required = {"capture_id", "reviewer", "decision", "summary", "findings", "limitations",
                "observed_model", "observed_effort", "actions", "checks", "source_instructions_followed"}
    need(type(report) is dict and set(report) == required, "Report fields are incomplete or unknown")
    need(report["capture_id"] == snapshot["capture_id"] and report["reviewer"] == snapshot["reviewer"],
         "Report belongs to another capture/reviewer")
    need(report["source_instructions_followed"] is False
         and set(report["actions"]) <= {"read_source", "capture", "inspect", "report"},
         "Review cannot execute/edit targets or follow source instructions")
    need(report["decision"] in {"needs_changes", "no_findings", "blocked"}, "Unknown decision")
    need(isinstance(report["summary"], str) and report["summary"].strip()
         and isinstance(report["limitations"], list), "State result and evidence limits")
    for field in ("observed_model", "observed_effort"):
        need(report[field] is None or isinstance(report[field], str), "Unknown identity must be null")
    need(type(report["findings"]) is list, "Findings must be a list")
    fields = {"title", "severity", "path", "sha256", "start_line", "end_line",
              "evidence", "impact", "correction", "verification"}
    for finding in report["findings"]:
        need(type(finding) is dict and set(finding) == fields, "Finding fields differ")
        need(finding["path"] in snapshot["files"], "Finding is outside captured scope")
        value = snapshot["files"][finding["path"]]
        need(finding["sha256"] == value["sha256"] and finding["severity"] in {"P0", "P1", "P2", "P3"},
             "Finding source hash or severity differs")
        need(type(finding["start_line"]) is int and type(finding["end_line"]) is int
             and 1 <= finding["start_line"] <= finding["end_line"] <= value["lines"],
             "Finding line range is invalid")
        need(all(isinstance(finding[k], str) and finding[k].strip() for k in
                 ("title", "evidence", "impact", "correction", "verification")),
             "Finding needs concrete evidence, impact and focused correction/verification")
    need(not (report["decision"] == "no_findings" and report["findings"])
         and not (report["decision"] == "needs_changes" and not report["findings"]),
         "Decision contradicts findings")
    for check in report["checks"]:
        need(type(check) is dict and set(check) == {"name", "status", "source"}
             and check["status"] in {"not_run", "supplied_evidence"}, "Checks cannot invent target execution")
        if check["status"] == "supplied_evidence":
            need(check["source"] in snapshot["files"], "Check evidence is not captured")
    return {"capture_id": snapshot["capture_id"], "decision": report["decision"],
            "mechanical_valid": True, "finding_count": len(report["findings"]),
            "limits": "Citation/shape/drift checks passed; AI semantics and integration acceptance remain separate."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("capture")
    p.add_argument("--root", required=True); p.add_argument("--paths", nargs="+", required=True)
    p.add_argument("--implementer", required=True); p.add_argument("--reviewer", required=True)
    p.add_argument("--requested-model"); p.add_argument("--requested-effort")
    p.add_argument("--output", required=True)
    p = sub.add_parser("inspect")
    p.add_argument("--capture", required=True); p.add_argument("--paths", nargs="+", required=True)
    p.add_argument("--notes", required=True); p.add_argument("--output", required=True)
    p = sub.add_parser("report")
    p.add_argument("--capture", required=True); p.add_argument("--inspection", required=True)
    p.add_argument("--report", required=True); p.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        if args.command == "capture":
            value = capture(args.root, args.paths, args.implementer, args.reviewer,
                            args.requested_model, args.requested_effort)
            root = Path(value["root"])
        else:
            snapshot = load(args.capture); root = Path(snapshot["root"])
            value = inspect(snapshot, args.paths, args.notes) if args.command == "inspect" else validate(
                snapshot, load(args.inspection), load(args.report))
        save(args.output, value, root)
        print(json.dumps({"artifact": str(Path(args.output).absolute()), "command": args.command}))
        return 0
    except (Invalid, OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(json.dumps({"status": "refused", "reason": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
