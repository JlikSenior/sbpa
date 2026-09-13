import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SchemaTests(unittest.TestCase):
    def test_all_json_schemas_are_valid_json_objects(self):
        schemas = sorted((ROOT / "schemas").glob("*.schema.json"))
        self.assertTrue(schemas)
        for path in schemas:
            with self.subTest(path=path.name):
                value = json.loads(path.read_text(encoding="utf-8"))
                self.assertIsInstance(value, dict)
                self.assertEqual(value.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(value.get("type"), "object")


if __name__ == "__main__":
    unittest.main()
