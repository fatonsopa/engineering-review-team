"""Retained behavioral scenarios and disposable native-host preparation.

These tests check fixture transport, not AI review quality. Assess actual reviewer
outputs against review_cases.json; expected answers are never staged for the AI.
"""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from install_skill import install, register_agents


def cases():
    return json.loads((ROOT / "tests/review_cases.json").read_text())


def validate_control_coverage(case):
    """Development inventory check only; this cannot establish AI behavior."""
    standard = (ROOT / "references/standards" / (case["id"] + ".md")).read_text()
    required = set(re.findall(r"^### ([A-Z]+-\d{2})\b", standard, re.M))
    covered = {control for scenario in case["additional_scenarios"]
               for control in scenario["controls"]}
    if required - covered:
        raise ValueError("Uncovered controls: " + ", ".join(sorted(required - covered)))
    expected = set(case["required_expectations"])
    present = {scenario["id"] + "/" + expectation["id"]
               for scenario in case["additional_scenarios"]
               for expectation in scenario["expectations"]}
    if expected != present:
        raise ValueError("Expectation inventory changed: " + ", ".join(sorted(expected ^ present)))


def stage(pending, destination, host, prompt):
    destination = Path(destination).expanduser().resolve()
    for name in pending:
        if PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts:
            raise ValueError("Fixture paths must stay within the disposable workspace.")
    destination.mkdir(parents=True, exist_ok=False)
    for name, content in pending.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    native_skills = ".agents/skills" if host == "codex" else ".claude/skills"
    skill = destination / native_skills / "engineering-review"
    install(ROOT, host, skill)
    (destination / "skill").symlink_to(skill, target_is_directory=True)
    agents = ".codex/agents" if host == "codex" else ".claude/agents"
    register_agents(skill, host, destination / agents)
    (destination / "prompt.txt").write_text(prompt)
    return destination


def prepare(identifier, destination, host="codex", scenario_ids=None):
    native_skills = ".agents/skills" if host == "codex" else ".claude/skills"
    entry = Path(destination).expanduser().resolve() / native_skills / "engineering-review/SKILL.md"
    if identifier == "lifecycle":
        case = json.loads((ROOT / "tests/lifecycle_case.json").read_text())
        return stage({p: text.encode() for p, text in case["files"].items()},
                     destination, host, case["instruction"].replace("./skill/SKILL.md", str(entry)))
    case = next(c for c in cases() if c["id"] == identifier)
    available = case["scenarios"] + case.get("additional_scenarios", [])
    selected = case["scenarios"]
    if scenario_ids is not None:
        by_id = {scenario["id"]: scenario for scenario in available}
        if not scenario_ids or len(set(scenario_ids)) != len(scenario_ids):
            raise ValueError("Select distinct scenario IDs.")
        if set(scenario_ids) - by_id.keys():
            raise ValueError("Unknown scenario ID for this reviewer.")
        selected = [by_id[scenario_id] for scenario_id in scenario_ids]
    pending = {}
    for scenario in selected:
        prefix = scenario["id"]
        pending[f"{prefix}/requirements.txt"] = scenario["requirements"].encode()
        for name, content in scenario["files"].items():
            pending[f"{prefix}/{name}"] = content.encode()
        for name, source in scenario.get("binary_files", {}).items():
            pending[f"{prefix}/{name}"] = (ROOT / "tests" / source).read_bytes()
    route = (
        f"Act as the assigned {case['agent']} specialist and return your assessment "
        "to the assigning lead. Preserve your read-only leaf role; do not delegate. "
        if host == "claude-code" else
        "Act as the main-context lead and delegate this focused review only to the "
        f"registered {case['agent']} native specialist. "
    )
    prompt = (
        "Use Engineering Review Team at " + str(entry) + ". " + route +
        "The supplied synthetic implementation was authored in "
        "a separate context. Assess only " + ", ".join(s["id"] for s in selected) +
        " separately against each "
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
    return stage(pending, destination, host, prompt)


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
                native = ".agents/skills" if host == "codex" else ".claude/skills"
                self.assertEqual((destination / "skill").resolve(), destination / native / "engineering-review")
                self.assertIn(str(destination / native / "engineering-review/SKILL.md"),
                              (destination / "prompt.txt").read_text())
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

    def test_selected_extended_cases_preserve_inputs_and_hide_oracles(self):
        for case in cases():
            extended = case.get("additional_scenarios", [])
            if not extended:
                continue
            scenario = extended[0]
            with self.subTest(reviewer=case["id"]), tempfile.TemporaryDirectory() as folder:
                destination = prepare(case["id"], Path(folder) / "selected",
                                      scenario_ids=[scenario["id"]])
                self.assertFalse((destination / "case-a").exists())
                for path, source in scenario["files"].items():
                    self.assertEqual((destination / scenario["id"] / path).read_text(), source)
                self.assertFalse((destination / "skill/tests").exists())
                self.assertFalse((destination / "expectations.json").exists())
                with self.assertRaisesRegex(ValueError, "Unknown scenario"):
                    prepare(case["id"], Path(folder) / "invalid", scenario_ids=["not-a-case"])
                self.assertFalse((Path(folder) / "invalid").exists())

    def test_extended_inventory_rejects_missing_control_coverage(self):
        from copy import deepcopy
        for case in cases():
            extended = case.get("additional_scenarios", [])
            if not extended:
                continue
            with self.subTest(reviewer=case["id"]):
                validate_control_coverage(case)
                omitted = extended[0]["controls"][0]
                incomplete = deepcopy(case)
                for scenario in incomplete["additional_scenarios"]:
                    scenario["controls"] = [control for control in scenario["controls"] if control != omitted]
                with self.assertRaisesRegex(ValueError, "Uncovered controls: " + omitted):
                    validate_control_coverage(incomplete)
                missing_criterion = deepcopy(case)
                missing_criterion["additional_scenarios"][0]["expectations"].pop()
                with self.assertRaisesRegex(ValueError, "Expectation inventory changed"):
                    validate_control_coverage(missing_criterion)
                for scenario in extended:
                    self.assertTrue(scenario["expectations"])
                    self.assertTrue(scenario["controls"])
                    self.assertEqual(len({e["id"] for e in scenario["expectations"]}),
                                     len(scenario["expectations"]))

    def test_lifecycle_stages_only_initial_source_and_no_expected_answers(self):
        case = json.loads((ROOT / "tests/lifecycle_case.json").read_text())
        with tempfile.TemporaryDirectory() as folder:
            destination = prepare("lifecycle", Path(folder) / "lifecycle")
            for name, text in case["files"].items():
                self.assertEqual((destination / name).read_text(), text)
            self.assertNotEqual((destination / "src/lookup.py").read_text(),
                                case["follow_up_files"]["src/lookup.py"])
            self.assertFalse((destination / "skill/tests").exists())

    def test_lifecycle_fixture_has_the_declared_boundary_and_partial_fix(self):
        # Fixture code is reviewed, pure test data; this is preflight of the
        # expected outcomes, not evidence that any AI reviewer found them.
        case = json.loads((ROOT / "tests/lifecycle_case.json").read_text())
        class Client:
            def __init__(self):
                self.calls = 0
                self.values = {str(i): object() for i in range(100)}
            def fetch_one(self, tenant, key):
                self.calls += 1
                return self.values[key]
            def fetch_many(self, tenant, keys):
                self.calls += 1
                return {key: self.values[key] for key in reversed(keys)}
        for source, fixed in [(case["files"]["src/lookup.py"], False),
                              (case["follow_up_files"]["src/lookup.py"], True)]:
            scope = {}
            exec(compile(source, "lookup-fixture", "exec"), scope)
            for size in (0, 1, 2, 100):
                client = Client()
                keys = [str(i) for i in range(size)]
                output = scope["values"](client, "tenant", keys)
                self.assertEqual(client.calls, int(size > 0) if fixed else size)
                self.assertEqual(output, [client.values[key] for key in keys])
                self.assertEqual(keys, [str(i) for i in range(size)])
        scope = {}
        exec(compile(case["files"]["src/cache.py"], "cache-fixture", "exec"), scope)
        store = {("A", "x"): "A data", ("B", "x"): "B data"}
        self.assertEqual(scope["read"]("A", "x", store), "A data")
        self.assertEqual(scope["read"]("B", "x", store), "A data")
        self.assertNotIn("src/cache.py", case["follow_up_files"])


if __name__ == "__main__":
    if "--prepare" in sys.argv:
        parser = argparse.ArgumentParser(description="Prepare one native-host review; does not launch a model.")
        parser.add_argument("--prepare", required=True, choices=[c["id"] for c in cases()] + ["lifecycle"])
        parser.add_argument("--destination", type=Path, required=True)
        parser.add_argument("--host", choices=["codex", "claude-code"], default="codex")
        parser.add_argument("--cases", nargs="+", help="Select retained scenario IDs; defaults to the original pair.")
        args = parser.parse_args()
        print(prepare(args.prepare, args.destination, args.host, args.cases))
    else:
        unittest.main()
