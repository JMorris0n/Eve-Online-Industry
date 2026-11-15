"""Privacy and readiness tests for the profile summary command."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from readiness_report import build_readiness_report


ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "config" / "operating-profile.example.json"


class ProfileReadinessTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_reports_readiness_without_private_values(self):
        self.profile["profile_name"] = "PRIVATE PROFILE NAME"
        self.profile["characters"][0]["label"] = "PRIVATE CHARACTER LABEL"
        self.profile["characters"][0]["skills"] = {"16622": 5}
        self.profile["characters"][0]["skills_state"] = "partial"
        self.profile["characters"][0]["job_capacity"]["manufacturing"] = 2
        self.profile["capital"]["working_capital_isk"] = 123456789
        self.profile["capital"]["liquidity_reserve_isk"] = 23456789
        self.profile["blueprints"] = [{
            "type_id": 987654,
            "state": "verified",
            "kind": "BPO",
            "quantity": 1,
        }]
        self.profile["blueprints_state"] = "partial"
        self.profile["market_access"] = {
            "state": "verified",
            "locations": [{
                "label": "PRIVATE MARKET NAME",
                "state": "verified",
                "market_type": "npc_station",
                "location_id": 60003760,
                "roles": ["procurement", "sales"],
            }],
        }
        result = build_readiness_report(self.profile)
        serialized = json.dumps(result)
        self.assertEqual(result["character_slots"][0]["known_skill_count"], 1)
        self.assertEqual(
            result["character_slots"][0]["job_capacity_status"]["manufacturing"],
            "available",
        )
        self.assertEqual(result["market_access"]["procurement_location_count"], 1)
        self.assertNotIn("PRIVATE", serialized)
        for private_value in ("123456789", "23456789", "16622", "987654", "60003760"):
            self.assertNotIn(private_value, serialized)

    def test_blank_example_is_structurally_valid_but_not_ready(self):
        result = build_readiness_report(self.profile)
        self.assertTrue(result["profile_schema_valid"])
        self.assertGreater(len(result["unfilled_areas"]), 0)
        self.assertEqual(result["blueprint_inventory"]["record_count"], 0)
        self.assertEqual(result["market_access"]["location_count"], 0)

    def test_malformed_profile_sections_do_not_break_redacted_report(self):
        self.profile["characters"][0]["state"] = []
        self.profile["market_access"] = {
            "state": [],
            "locations": [{"roles": None}, {"roles": "procurement"}],
        }
        self.profile["logistics"] = {
            "state": [],
            "preferred_method": ["PRIVATE VALUE"],
            "max_route_jumps": None,
            "max_active_minutes_per_batch": None,
            "max_cargo_m3": None,
        }
        result = build_readiness_report(self.profile)
        serialized = json.dumps(result)
        self.assertFalse(result["profile_schema_valid"])
        self.assertEqual(result["market_access"]["procurement_location_count"], 0)
        self.assertEqual(result["logistics"]["preferred_method"], "unknown")
        self.assertNotIn("PRIVATE VALUE", serialized)

    def test_import_diagnostics_are_generic_and_do_not_expose_private_values(self):
        self.profile["characters"][1]["skills_state"] = "partial"
        self.profile["characters"][1]["job_capacity"] = {
            "manufacturing": None,
            "science": None,
            "reaction": None,
        }
        manifest = {
            "character_mapping": [{
                "slot": 2,
                "character_id": 99887766,
                "character_name": "PRIVATE CHARACTER NAME",
                "snapshot_stale": False,
                "warnings": [
                    "Skill-queue row 0 has an unreadable completion time.",
                    "Industry-job row 1 has an unrecognized activity ID.",
                    "Reaction free-slot count could not be verified.",
                ],
            }],
        }
        result = build_readiness_report(self.profile, manifest)
        row = result["character_slots"][1]
        serialized = json.dumps(result)
        self.assertIn(
            "unreadable_skill_queue_finish_time",
            row["skills_diagnostic_codes"],
        )
        self.assertIn(
            "unrecognized_industry_activity_id",
            row["job_capacity_diagnostic_codes"],
        )
        self.assertIn(
            "free_slot_count_unverified",
            row["job_capacity_diagnostic_codes"],
        )
        for private_value in ("99887766", "PRIVATE CHARACTER NAME", "Skill-queue row", "Reaction"):
            self.assertNotIn(private_value, serialized)


    def test_verified_profile_sections_are_recognized(self):
        self.profile["blueprints_state"] = "verified"
        self.profile["facilities_state"] = "verified"
        self.profile["capital"].update({
            "state": "verified",
            "working_capital_isk": 1000000,
            "liquidity_reserve_isk": 100000,
            "max_capital_at_risk_isk": 500000,
        })
        self.profile["operations"].update({
            "state": "verified",
            "active_hours_per_week": 5,
            "max_setup_minutes_per_batch": 30,
            "target_liquidation_days": 7,
            "risk_tolerance": "low",
        })
        self.profile["market_access"] = {
            "state": "verified",
            "locations": [{
                "label": "Market",
                "state": "verified",
                "market_type": "npc_station",
                "roles": ["procurement", "sales"],
            }],
        }
        self.profile["logistics"] = {
            "state": "verified",
            "preferred_method": "self_haul",
            "max_route_jumps": 10,
            "max_active_minutes_per_batch": 30,
            "max_cargo_m3": 50000,
        }
        result = build_readiness_report(self.profile)
        self.assertTrue(result["capital"]["fields_known"]["working_capital_isk"])
        self.assertTrue(result["operations"]["fields_known"]["active_hours_per_week"])
        self.assertTrue(result["logistics"]["practical_limits_known"])
        self.assertNotIn("blueprints: verify the inventory or mark it partial", result["unfilled_areas"])


if __name__ == "__main__":
    unittest.main()
