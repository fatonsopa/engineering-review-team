"""Six bounded regression groups for the stateless runtime acceptance checker."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_review.py"
spec = importlib.util.spec_from_file_location("check_review", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class ReviewGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "target").mkdir()
        self.source = self.root / "target/module.py"
        self.source.write_text("raise RuntimeError('reviewed code must never execute')\n")
        self.requirements = self.root / "requirements.txt"
        self.requirements.write_text("R1: required behavior. R2: required tenant isolation.\n")
        self.assignment_path = self.root / "assignment.json"
        self.assignment = {"criteria": ["R1", "R2"], "sources": ["target/module.py"],
                           "requirements": ["requirements.txt"]}
        self.save_assignment()
        _, snapshot, issues = gate.capture(self.assignment_path)
        self.assertEqual(issues, [])
        self.report = {"snapshot": snapshot, "outcome": "completed",
                       "dispositions": {"R1": "met", "R2": "met"}}

    def save_assignment(self):
        self.assignment_path.write_text(json.dumps(self.assignment))

    def check(self, report=None):
        return gate.check(self.assignment_path, json.dumps(report or self.report).encode())

    def cli(self, *args, data=None):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)],
                                input=data, capture_output=True, timeout=10)
        return result.returncode, json.loads(result.stdout)

    def test_valid_current_completion_and_input_validation(self):
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertTrue(self.check()["accepted"])
        code, capture = self.cli("capture", self.assignment_path)
        self.assertEqual(code, 0)
        self.assertEqual(capture, self.report["snapshot"])
        code, result = self.cli("check", self.assignment_path, "-",
                                data=json.dumps(self.report).encode())
        self.assertEqual(code, 0)
        self.assertTrue(result["review_complete"])
        report_path = self.root / "report.json"
        report_path.write_text(json.dumps(self.report))
        code, result = self.cli("check", self.assignment_path, report_path)
        self.assertEqual(code, 0)
        self.assertEqual(result["report_sha256"], gate.digest(report_path.read_bytes()))
        for path, content in before.items():
            self.assertEqual(path.read_bytes(), content)
        self.assertEqual(set(self.root.rglob("*")) - {report_path},
                         set(before) | {self.root / "target"})
        for replacement in ({"R1": "met", "R3": "met"}, {"R1": "unknown"}, {"R1": True}):
            report = deepcopy(self.report)
            report["dispositions"] = replacement
            with self.subTest(dispositions=replacement), self.assertRaises(ValueError):
                self.check(report)
        malformed = b'{"outcome":"failed","outcome":"completed"}'
        code, result = self.cli("check", self.assignment_path, "-", data=malformed)
        self.assertEqual(code, 2)
        self.assertFalse(result["record_valid"])

    def test_omitted_criterion_is_rejected_despite_all_roles(self):
        report = deepcopy(self.report)
        report["roles"] = ["code", "security"]
        del report["dispositions"]["R2"]
        result = self.check(report)
        self.assertTrue(result["record_valid"])
        self.assertFalse(result["accepted"])
        self.assertIn("Missing required criteria: R2", result["issues"])
        code, result = self.cli("check", self.assignment_path, "-", data=json.dumps(report).encode())
        self.assertEqual(code, 1)

    def test_partial_unknown_and_contradicted_are_not_clean_acceptance(self):
        for status in ("partial", "not_assessed", "contradicted"):
            report = deepcopy(self.report)
            report["dispositions"]["R2"] = status
            with self.subTest(status=status):
                result = self.check(report)
                self.assertTrue(result["record_valid"])
                self.assertFalse(result["accepted"])
                self.assertEqual(result["review_complete"], status == "contradicted")

    def test_changed_or_unavailable_source_rejects_acceptance(self):
        self.source.write_text("changed source\n")
        result = self.check()
        self.assertTrue(result["record_valid"])
        self.assertFalse(result["accepted"])
        self.source.unlink()
        result = self.check()
        self.assertTrue(result["record_valid"])
        self.assertFalse(result["accepted"])
        _, snapshot, issues = gate.capture(self.assignment_path)
        self.assertIsNone(snapshot["files"]["target/module.py"])
        self.assertTrue(issues)
        code, result = self.cli("capture", self.assignment_path)
        self.assertEqual(code, 1)

    def test_changed_requirements_or_assignment_rejects_acceptance(self):
        self.requirements.write_text("R2 now requires a different contract.\n")
        self.assertFalse(self.check()["accepted"])
        self.assignment["criteria"] = ["R3"]
        self.save_assignment()
        result = self.check()
        self.assertTrue(result["record_valid"])
        self.assertFalse(result["accepted"])
        self.assertIn("Assignment changed since the pre-review capture.", result["issues"])

    def test_failure_timeout_and_cancel_records_survive_drift_and_revocation(self):
        self.source.write_text("source drift\n")
        for outcome in ("failed", "timed_out", "cancelled"):
            report = deepcopy(self.report)
            report["outcome"] = outcome
            del report["dispositions"]["R2"]
            with self.subTest(outcome=outcome):
                result = self.check(report)
                self.assertTrue(result["record_valid"])
                self.assertEqual(result["outcome"], outcome)
                self.assertFalse(result["accepted"])
        self.assignment["active"] = False
        self.assignment["criteria"] = ["R3"]
        self.save_assignment()
        report["outcome"] = "cancelled"
        original_read = Path.read_bytes

        def permitted_read(path):
            if path in (self.source, self.requirements):
                raise AssertionError("Revoked input was read")
            return original_read(path)

        with patch.object(Path, "read_bytes", permitted_read):
            result = self.check(report)
        self.assertTrue(result["record_valid"])
        self.assertFalse(result["accepted"])
        self.assertTrue(any("revoked" in issue for issue in result["issues"]))


if __name__ == "__main__":
    unittest.main()
