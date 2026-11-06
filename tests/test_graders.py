#!/usr/bin/env python3
"""
Unit Test Suite for `contract-precedence-eval` Graders and Reference Solutions.
Compatible with both Python standard-library `unittest` (zero dependencies) and `pytest`:
  python3 -m unittest discover -s tests -v
  pytest tests/test_graders.py -v
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from graders.grader import grade_task

TASKS_DIR = ROOT / "tasks"
REF_DIR = ROOT / "reference"


def get_all_task_ids():
    return [f"task_0{i}" for i in range(1, 7)]


class TestContractPrecedenceGraders(unittest.TestCase):
    def test_all_reference_solutions_pass_100_percent(self):
        """Every reference solution must pass its grader with score == 1.0 and passed == True."""
        for tid in get_all_task_ids():
            ref = json.loads((REF_DIR / f"{tid}_reference.json").read_text(encoding="utf-8"))
            res = grade_task(tid, json.dumps(ref), ref)
            self.assertTrue(res["passed"], f"Reference solution failed for {tid}: {res}")
            self.assertEqual(res["score"], 1.0, f"Reference score != 1.0 for {tid}: {res}")
            self.assertEqual(res["checks_passed"], res["total_checks"])

    def test_all_naive_failures_are_rejected_with_partial_credit(self):
        """Deliberately flawed naive model outputs must fail (passed == False) while earning partial credit."""
        for tid in get_all_task_ids():
            task_data = json.loads((TASKS_DIR / f"{tid}.json").read_text(encoding="utf-8"))
            ref = json.loads((REF_DIR / f"{tid}_reference.json").read_text(encoding="utf-8"))
            naive = task_data["naive_failure"]
            res = grade_task(tid, json.dumps(naive), ref)
            self.assertFalse(res["passed"], f"Grader produced FALSE PASS on naive output for {tid}")
            self.assertGreater(res["score"], 0.0, f"Partial credit should be > 0.0 for {tid}")
            self.assertLess(res["score"], 1.0, f"Partial credit should be < 1.0 for {tid}")

    def test_numeric_tolerance_accepts_minor_rounding(self):
        """Grader must accept values within $0.01 numeric tolerance (no false fails over rounding)."""
        ref = json.loads((REF_DIR / "task_01_reference.json").read_text(encoding="utf-8"))
        slightly_rounded = json.loads(json.dumps(ref))
        slightly_rounded["total_recoverable_usd"] = ref["total_recoverable_usd"] + 0.008
        res = grade_task("task_01", json.dumps(slightly_rounded), ref)
        self.assertTrue(res["passed"], "Grader rejected answer within 0.01 numeric tolerance")

    def test_malformed_or_empty_json_fails_cleanly(self):
        """Grader must reject non-JSON or empty outputs without throwing unhandled exceptions."""
        ref = json.loads((REF_DIR / "task_01_reference.json").read_text(encoding="utf-8"))
        res = grade_task("task_01", "I think the liability cap is $270,000.", ref)
        self.assertFalse(res["passed"])
        self.assertEqual(res["score"], 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
