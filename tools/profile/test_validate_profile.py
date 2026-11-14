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

    def test_optional_metadata_fields_may_be_omitted(self):
        self.profile.pop("last_reviewed")
        self.profile.pop("notes")
        self.assertEqual(validate_profile_data(self.profile), [])

    def test_unknown_values_may_remain_null(self):
        self.assertEqual(validate_profile_data(self.profile), [])

    def test_accepts_market_access_and_logistics(self):
        self.profile["market_access"] = {
            "state": "partial",
            "locations": [{
                "label": "Preferred market",
                "state": "verified",
                "market_type": "npc_station",
                "region_id": 10000002,
                "system_id": 30000142,
                "location_id": 60003760,
                "roles": ["procurement", "sales"],
                "notes": [],
            }],
            "notes": [],
        }
        self.profile["logistics"] = {
            "state": "partial",
            "preferred_method": "either",
            "max_route_jumps": 15,
            "max_active_minutes_per_batch": 45,
            "max_cargo_m3": 50000,
            "notes": [],
        }
        self.assertEqual(validate_profile_data(self.profile), [])

    def test_rejects_invalid_market_location_id(self):
        self.profile["market_access"] = {
            "state": "partial",
            "locations": [{
                "label": "Market",
                "state": "unknown",
                "market_type": "unknown",
                "location_id": -1,
                "roles": [],
            }],
        }
        self.assertTrue(any("location_id" in error for error in validate_profile_data(self.profile)))

    def test_rejects_invalid_logistics_method(self):
        self.profile["logistics"] = {
            "state": "unknown",
            "preferred_method": "teleport",
            "max_route_jumps": None,
            "max_active_minutes_per_batch": None,
            "max_cargo_m3": None,
        }
        self.assertTrue(any("preferred_method" in error for error in validate_profile_data(self.profile)))

    def test_rejects_negative_capital(self):
        self.profile["capital"]["working_capital_isk"] = -1
        self.assertTrue(any("working_capital_isk" in error for error in validate_profile_data(self.profile)))


if __name__ == "__main__":
    unittest.main()
