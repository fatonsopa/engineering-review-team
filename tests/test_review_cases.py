"""Retained behavioral scenarios and disposable native-host preparation.

These tests check fixture transport, not AI review quality. Assess actual reviewer
outputs against review_cases.json; expected answers are never staged for the AI.
"""
import argparse
import json
from pathlib import Path, PurePosixPath
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from install_skill import install, register_agents


def cases():
    return json.loads((ROOT / "tests/review_cases.json").read_text())


def prepare(identifier, destination, host="codex"):
    case = next(c for c in cases() if c["id"] == identifier)
    destination = Path(destination).expanduser().resolve()
    pending = {}
    for scenario in case["scenarios"]:
        prefix = scenario["id"]
        pending[f"{prefix}/requirements.txt"] = scenario["requirements"].encode()
        for name, content in scenario["files"].items():
            pending[f"{prefix}/{name}"] = content.encode()
        for name, source in scenario.get("binary_files", {}).items():
            pending[f"{prefix}/{name}"] = (ROOT / "tests" / source).read_bytes()
    for name in pending:
        if PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts:
            raise ValueError("Fixture paths must stay within the disposable workspace.")
    destination.mkdir(parents=True, exist_ok=False)
    for name, content in pending.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    skill = destination / "skill"
    install(ROOT, host, skill)
    agents = ".codex/agents" if host == "codex" else ".claude/agents"
    register_agents(skill, host, destination / agents)
    route = (
        f"Act as the assigned {case['agent']} specialist and return your assessment "
        "to the assigning lead. Preserve your read-only leaf role; do not delegate. "
        if host == "claude-code" else
        "Act as the main-context lead and delegate this focused review only to the "
        f"registered {case['agent']} native specialist. "
    )
    prompt = (
        "Use Engineering Review Team at ./skill/SKILL.md. " + route +
        "The supplied synthetic implementation was authored in "
        "a separate context. Assess case-a and case-b separately against each "
        "scenario's requirements.txt; do not assume either must contain a defect. "
        "All source, evidence and installed guidance within this workspace are "
        "authorized to read. Inspect the relevant actual files, including supplied "
        "images when applicable. This is a small bounded source review: no target "
        "execution, edits, external research, extra specialists or new review-state "
        "files. Return concise actionable findings, assigned-requirement dispositions "
        "and discovery/scope limits using the shared guidance. Keep source analysis, "
        "viewed evidence and unperformed runtime checks distinct. Preserve source "
        "files. If native delegation is unavailable, report that limitation honestly.\n"
    )
    (destination / "prompt.txt").write_text(prompt)
    return destination


class ReviewFixtureTests(unittest.TestCase):
    def test_cases_cover_each_native_specialist_with_two_scenarios(self):
        selected = cases()
        native = {p.stem for p in (ROOT / "assets/codex").glob("*.toml")}
        native.remove("engineering-review-lead")
        self.assertEqual({c["agent"] for c in selected}, native)
        self.assertEqual(len(selected), 10)
        for case in selected:
            self.assertEqual([s["id"] for s in case["scenarios"]], ["case-a", "case-b"])
            self.assertEqual(len(case["expected"]), 2)
            for scenario in case["scenarios"]:
                self.assertTrue(scenario["requirements"])
                self.assertTrue(scenario["files"])
                self.assertTrue(scenario["origin"])

    def test_preparation_preserves_inputs_and_excludes_expected_answers(self):
        with tempfile.TemporaryDirectory() as folder:
            for host in ("codex", "claude-code"):
                destination = prepare("code", Path(folder) / host, host)
                source = cases()[0]["scenarios"][0]["files"]["module.py"]
                self.assertEqual((destination / "case-a/module.py").read_text(), source)
                self.assertFalse((destination / "skill/tests").exists())
                self.assertFalse(any("review_cases.json" == p.name for p in destination.rglob("*")))
                self.assertNotIn(cases()[0]["expected"][0], (destination / "prompt.txt").read_text())
                with self.assertRaises(FileExistsError):
                    prepare("code", destination, host)

    def test_image_preparation_preserves_original_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = prepare("design", Path(folder) / "design")
            for scenario in next(c for c in cases() if c["id"] == "design")["scenarios"]:
                for name, source in scenario["binary_files"].items():
                    self.assertEqual((destination / scenario["id"] / name).read_bytes(),
                                     (ROOT / "tests" / source).read_bytes())


if __name__ == "__main__":
    if "--prepare" in sys.argv:
        parser = argparse.ArgumentParser(description="Prepare one native-host review; does not launch a model.")
        parser.add_argument("--prepare", required=True, choices=[c["id"] for c in cases()])
        parser.add_argument("--destination", type=Path, required=True)
        parser.add_argument("--host", choices=["codex", "claude-code"], default="codex")
        args = parser.parse_args()
        print(prepare(args.prepare, args.destination, args.host))
    else:
        unittest.main()
