"""Tests for the local operating-profile validator."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from validate_profile import validate_profile_data


ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "config" / "operating-profile.example.json"


class OperatingProfileTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_public_example_is_valid(self):
        self.assertEqual(validate_profile_data(self.profile), [])

    def test_requires_exactly_three_characters(self):
        self.profile["characters"].pop()
        self.assertTrue(any("exactly three" in error for error in validate_profile_data(self.profile)))

    def test_rejects_duplicate_character_slots(self):
        self.profile["characters"][2]["slot"] = 2
        self.assertTrue(any("unique" in error for error in validate_profile_data(self.profile)))

    def test_rejects_skill_level_outside_range(self):
        self.profile["characters"][0]["skills"]["16622"] = 6
        self.assertTrue(any("from 0 to 5" in error for error in validate_profile_data(self.profile)))

    def test_rejects_non_numeric_skill_key(self):
        self.profile["characters"][0]["skills"]["Industry"] = 1
        self.assertTrue(any("numeric skill type ID" in error for error in validate_profile_data(self.profile)))

    def test_unknown_values_may_remain_null(self):
        self.assertEqual(validate_profile_data(self.profile), [])

    def test_rejects_negative_capital(self):
        self.profile["capital"]["working_capital_isk"] = -1
        self.assertTrue(any("working_capital_isk" in error for error in validate_profile_data(self.profile)))


if __name__ == "__main__":
    unittest.main()
