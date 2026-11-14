"""Tests for recipe feasibility screening against a local profile."""

from __future__ import annotations

import unittest

from check_feasibility import evaluate_recipe


def profile():
    return {
        "characters": [
            {"slot": 1, "label": "Industry", "skills_state": "verified",
             "skills": {"3380": 4}, "job_capacity": {"manufacturing": 1, "reaction": 0}},
            {"slot": 2, "label": "Science", "skills_state": "verified",
             "skills": {"3380": 0}, "job_capacity": {"manufacturing": 0, "reaction": 0}},
            {"slot": 3, "label": "Unknown", "skills_state": "unknown",
             "skills": {}, "job_capacity": {"manufacturing": None, "reaction": None}},
        ],
        "blueprints_state": "verified",
        "blueprints": [{"type_id": 100, "state": "verified", "kind": "BPO", "quantity": 1}],
        "facilities_state": "verified",
        "facilities": [{"label": "Test facility", "state": "verified", "services": ["manufacturing"]}],
    }


def recipe(activity="manufacturing", skill_level=3):
    return {
        "activity": activity,
        "blueprint_type_id": 100,
        "blueprint_name": "Test Blueprint",
        "products": [{"type_id": 200, "name": "Test Product", "quantity_per_run": 1}],
        "required_skills": [{"type_id": 3380, "name": "Industry", "level": skill_level}],
        "source_field_state": {
            "materials": "present",
            "products": "present",
            "required_skills": "present",
        },
    }


class FeasibilityTests(unittest.TestCase):
    def test_eligible_when_all_hard_constraints_are_verified(self):
        result = evaluate_recipe(profile(), recipe())
        self.assertEqual(result["status"], "eligible")

    def test_unknown_when_skill_inventory_is_incomplete(self):
        data = profile()
        data["characters"][0]["skills_state"] = "partial"
        data["characters"][0]["skills"] = {}
        data["characters"][2]["job_capacity"]["manufacturing"] = None
        result = evaluate_recipe(data, recipe())
        self.assertEqual(result["status"], "unknown")

    def test_ineligible_when_all_verified_characters_lack_skill(self):
        data = profile()
        data["characters"][0]["skills"]["3380"] = 1
        data["characters"][2]["skills_state"] = "verified"
        data["characters"][2]["job_capacity"]["manufacturing"] = 0
        result = evaluate_recipe(data, recipe(skill_level=3))
        self.assertEqual(result["status"], "ineligible")

    def test_missing_blueprint_only_blocks_when_inventory_is_complete(self):
        data = profile()
        data["blueprints"] = []
        self.assertEqual(evaluate_recipe(data, recipe())["status"], "ineligible")
        data["blueprints_state"] = "partial"
        self.assertEqual(evaluate_recipe(data, recipe())["status"], "unknown")

    def test_bpc_without_known_runs_is_unknown(self):
        data = profile()
        data["blueprints"] = [{"type_id": 100, "state": "verified", "kind": "BPC",
                               "quantity": 1, "licensed_runs": None}]
        self.assertEqual(evaluate_recipe(data, recipe())["status"], "unknown")

    def test_facility_inventory_must_support_activity(self):
        data = profile()
        data["facilities"] = [{"label": "Wrong service", "state": "verified",
                               "services": ["reaction"]}]
        self.assertEqual(evaluate_recipe(data, recipe())["status"], "ineligible")

    def test_recipe_with_omitted_materials_is_unknown(self):
        data = recipe()
        data["materials"] = []
        data["source_field_state"]["materials"] = "omitted"
        data["recipe_data_status"] = "incomplete"
        result = evaluate_recipe(profile(), data)
        self.assertEqual(result["status"], "unknown")
        self.assertEqual(result["checks"]["recipe_data"]["status"], "unknown")

    def test_legacy_recipe_without_source_field_state_is_unknown(self):
        data = recipe()
        data.pop("source_field_state")
        result = evaluate_recipe(profile(), data)
        self.assertEqual(result["status"], "unknown")

    def test_explicitly_empty_material_list_is_not_treated_as_omitted(self):
        data = recipe()
        data["materials"] = []
        data["source_field_state"]["materials"] = "empty"
        result = evaluate_recipe(profile(), data)
        self.assertEqual(result["checks"]["recipe_data"]["status"], "eligible")

    def test_character_can_be_eligible_even_if_other_character_is_unknown(self):
        data = profile()
        result = evaluate_recipe(data, recipe())
        self.assertEqual(result["checks"]["characters"]["status"], "eligible")


if __name__ == "__main__":
    unittest.main()
