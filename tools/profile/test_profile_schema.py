"""Contract tests keeping the public example, JSON Schema, and validator aligned."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from validate_profile import REQUIRED_TOP_LEVEL, validate_profile_data


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "config" / "operating-profile.schema.json"
EXAMPLE_PATH = ROOT / "config" / "operating-profile.example.json"


class ProfileSchemaContractTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.example = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))

    def test_schema_required_fields_match_validator_contract(self):
        self.assertEqual(set(self.schema["required"]), REQUIRED_TOP_LEVEL)

    def test_public_example_contains_all_schema_required_fields(self):
        self.assertTrue(set(self.schema["required"]).issubset(self.example))

    def test_skill_keys_are_sde_type_ids(self):
        skills = self.schema["$defs"]["character"]["properties"]["skills"]
        self.assertEqual(skills["propertyNames"]["pattern"], "^[1-9][0-9]*$")
        self.assertEqual(skills["additionalProperties"]["maximum"], 5)

    def test_example_passes_runtime_validator(self):
        self.assertEqual(validate_profile_data(self.example), [])


if __name__ == "__main__":
    unittest.main()
