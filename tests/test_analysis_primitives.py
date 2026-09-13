import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from sbpa_engine.benchmark import score_fixture
from sbpa_engine.fingerprint import behavior_fingerprint, duplicate_fingerprints
from sbpa_engine.graph import affected, build_graph


class AnalysisPrimitiveTests(unittest.TestCase):
    def test_fingerprint_ignores_human_language_fields(self):
        base = {
            "id": "B-000001",
            "title": "配置失败回退",
            "description": "中文描述",
            "source_evidence": ["E-000001"],
            "contract": {"trigger": "load", "outputs": ["fallback"]},
        }
        translated = dict(base, title="Fallback on config failure", description="English description")
        self.assertEqual(behavior_fingerprint(base), behavior_fingerprint(translated))

    def test_duplicate_fingerprint_detection(self):
        one = {"id":"B-000001","source_evidence":["E-000001"],"contract":{"outputs":[1]}}
        two = {"id":"B-000002","source_evidence":["E-000001"],"contract":{"outputs":[1]}}
        duplicates = duplicate_fingerprints([one, two])
        self.assertEqual(list(duplicates.values()), [["B-000001", "B-000002"]])

    def test_evidence_change_propagates_transitively(self):
        behaviors = [
            {"id":"B-000001","source_evidence":["E-000001"],"related_behaviors":[]},
            {"id":"B-000002","source_evidence":["E-000002"],"related_behaviors":["B-000001"]},
        ]
        graph = build_graph(behaviors)
        self.assertEqual(affected({"E-000001"}, graph), {"B-000001", "B-000002"})

    def test_fixture_scoring_penalizes_compression(self):
        expected = json.loads((ROOT / "fixtures/branch-fallback/expected.json").read_text())
        discovered = expected["expected_behaviors"][:]
        self.assertTrue(score_fixture(expected, discovered)["passed"])
        compressed = ["input validation", "fallback handling"]
        score = score_fixture(expected, compressed)
        self.assertFalse(score["passed"])
        self.assertLess(score["behavior_recall"], 1.0)


if __name__ == "__main__":
    unittest.main()
