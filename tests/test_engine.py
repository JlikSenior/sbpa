import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "engine" / "sbpa.py"


class EngineTests(unittest.TestCase):
    def run_sbpa(self, root, *args):
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=root,
            text=True,
            capture_output=True,
        )

    def test_untracked_file_invalidates_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "source.txt").write_text("v1", encoding="utf-8")
            self.assertEqual(self.run_sbpa(root, "init").returncode, 0)
            self.assertEqual(self.run_sbpa(root, "inventory").returncode, 0)
            self.assertEqual(self.run_sbpa(root, "validate").returncode, 0)
            (root / "later.txt").write_text("new evidence", encoding="utf-8")
            result = self.run_sbpa(root, "validate")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("inventory is stale", result.stdout)

    def test_exact_requires_target_and_verification_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "source.txt").write_text("behavior", encoding="utf-8")
            self.run_sbpa(root, "init")
            self.run_sbpa(root, "inventory")
            evidence = list(csv.DictReader((root / ".sbpa/evidence.csv").open(encoding="utf-8")))
            eid = evidence[0]["evidence_id"]
            behavior = {
                "id": "B-000001",
                "title": "A behavior",
                "evidence_class": "CONFIRMED",
                "source_evidence": [eid],
                "contract": {},
            }
            (root / ".sbpa/behaviors.jsonl").write_text(json.dumps(behavior) + "\n", encoding="utf-8")
            with (root / ".sbpa/traceability.csv").open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["behavior_id","source_evidence","requirement","target_evidence","target_status","verification_evidence","notes"])
                writer.writeheader()
                writer.writerow({"behavior_id":"B-000001","source_evidence":eid,"requirement":"R1","target_evidence":"","target_status":"EXACT","verification_evidence":"","notes":""})
            result = self.run_sbpa(root, "validate")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("EXACT requires target_evidence and verification_evidence", result.stdout)


if __name__ == "__main__":
    unittest.main()
