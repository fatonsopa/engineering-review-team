#!/usr/bin/env python3
"""Read-only coverage and freshness check; never execute reviewed source."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


OUTCOMES = {"completed", "failed", "timed_out", "cancelled"}
DISPOSITIONS = {"met", "contradicted", "partial", "not_assessed"}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(data):
    value = json.loads(data, object_pairs_hook=unique_object)
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object.")
    return value


def strings(value, name, nonempty=False):
    if (not isinstance(value, list) or (nonempty and not value)
            or any(not isinstance(s, str) or not s.strip() for s in value)
            or len(set(value)) != len(value)):
        raise ValueError(f"{name} must contain distinct nonempty strings.")
    return value


def digest(data):
    return hashlib.sha256(data).hexdigest()


def capture(assignment_path):
    """Bind the independently supplied criteria and input files to their bytes."""
    path = Path(assignment_path)
    data = path.read_bytes()
    assignment = load_json(data)
    strings(assignment.get("criteria"), "criteria", nonempty=True)
    if not isinstance(assignment.get("active", True), bool):
        raise ValueError("active must be a boolean.")
    paths = []
    for group in ("sources", "requirements", "evidence"):
        paths.extend(strings(assignment.get(group, []), group,
                             nonempty=group != "evidence"))
    files, issues = {}, []
    if not assignment.get("active", True):
        files = dict.fromkeys(paths)
        issues.append("Assignment authorization is revoked; assigned inputs were not read.")
        return assignment, {"assignment_sha256": digest(data),
                            "criteria": assignment["criteria"], "files": files}, issues
    for name in dict.fromkeys(paths):
        target = Path(name)
        if not target.is_absolute():
            target = path.parent / target
        try:
            files[name] = digest(target.read_bytes())
        except OSError as error:
            files[name] = None
            issues.append(f"Cannot read assigned input {name}: {error}")
    return assignment, {"assignment_sha256": digest(data),
                        "criteria": assignment["criteria"], "files": files}, issues


def valid_digest(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def check(assignment_path, report_data):
    """Keep valid incomplete outcomes distinct from eligibility for acceptance."""
    assignment, current, issues = capture(assignment_path)
    report = load_json(report_data)
    snapshot = report.get("snapshot")
    dispositions = report.get("dispositions")
    outcome = report.get("outcome")
    if not isinstance(outcome, str) or outcome not in OUTCOMES:
        raise ValueError("Unknown or missing terminal outcome.")
    if not isinstance(dispositions, dict) or any(
            not isinstance(k, str) or not k.strip()
            or not isinstance(v, str) or v not in DISPOSITIONS
            for k, v in dispositions.items()):
        raise ValueError("dispositions must map criterion IDs to known statuses.")
    if (not isinstance(snapshot, dict)
            or not valid_digest(snapshot.get("assignment_sha256"))
            or not isinstance(snapshot.get("files"), dict)
            or any(not isinstance(k, str) or not k.strip()
                   or (v is not None and not valid_digest(v))
                   for k, v in snapshot["files"].items())):
        raise ValueError("Missing or malformed pre-review snapshot.")
    captured_criteria = strings(snapshot.get("criteria"), "snapshot criteria", nonempty=True)
    required = set(assignment["criteria"])
    unknown = set(dispositions) - set(captured_criteria)
    if unknown:
        raise ValueError("Unknown criterion IDs: " + ", ".join(sorted(unknown)))
    missing = required - dispositions.keys()
    if missing:
        issues.append("Missing required criteria: " + ", ".join(sorted(missing)))
    if snapshot["assignment_sha256"] != current["assignment_sha256"]:
        issues.append("Assignment changed since the pre-review capture.")
    if snapshot["criteria"] != current["criteria"]:
        issues.append("Required criteria changed since the pre-review capture.")
    if snapshot["files"] != current["files"]:
        issues.append("Assigned input identities changed or were omitted.")
    if any(value is None for value in snapshot["files"].values()):
        issues.append("Pre-review input identities are incomplete.")
    if outcome != "completed":
        issues.append("Review outcome is " + outcome + ".")
    incomplete = [k for k, v in dispositions.items() if v in {"partial", "not_assessed"}]
    if incomplete:
        issues.append("Incomplete criteria: " + ", ".join(sorted(incomplete)))
    review_complete = not issues
    contradicted = [k for k, v in dispositions.items() if v == "contradicted"]
    if contradicted:
        issues.append("Contradicted criteria: " + ", ".join(sorted(contradicted)))
    return {
        "record_valid": True,
        "review_complete": review_complete,
        "accepted": review_complete and not contradicted,
        "outcome": outcome,
        "assignment_sha256": current["assignment_sha256"],
        "report_sha256": digest(report_data),
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    capture_parser = modes.add_parser("capture", help="Capture inputs before review; JSON to stdout.")
    capture_parser.add_argument("assignment", type=Path)
    check_parser = modes.add_parser("check", help="Check the report; use '-' for JSON stdin.")
    check_parser.add_argument("assignment", type=Path)
    check_parser.add_argument("report")
    args = parser.parse_args()
    try:
        if args.mode == "capture":
            _, snapshot, issues = capture(args.assignment)
            if issues:
                snapshot["issues"] = issues
            print(json.dumps(snapshot, indent=2))
            return int(bool(issues))
        data = sys.stdin.buffer.read() if args.report == "-" else Path(args.report).read_bytes()
        result = check(args.assignment, data)
        print(json.dumps(result, indent=2))
        return 0 if result["accepted"] else 1
    except (OSError, ValueError) as error:
        print(json.dumps({"record_valid": False, "review_complete": False,
                          "accepted": False, "issues": [str(error)]}, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
