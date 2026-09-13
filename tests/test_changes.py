import csv
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from sbpa_engine.changes import detect_changes
from sbpa_engine.inventory import build_inventory


class ChangeDetectionTests(unittest.TestCase):
    def test_added_changed_deleted_are_distinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            keep = root / "keep.txt"
            change = root / "change.txt"
            remove = root / "remove.txt"
            keep.write_text("same", encoding="utf-8")
            change.write_text("before", encoding="utf-8")
            remove.write_text("gone", encoding="utf-8")
            build_inventory(root)

            change.write_text("after", encoding="utf-8")
            remove.unlink()
            (root / "added.txt").write_text("new", encoding="utf-8")

            result = detect_changes(root)
            self.assertEqual(result["added"], ["added.txt"])
            self.assertEqual(result["changed"], ["change.txt"])
            self.assertEqual(result["deleted"], ["remove.txt"])
            self.assertIn("keep.txt", result["unchanged"])


if __name__ == "__main__":
    unittest.main()
