"""Tests for current-format SDE recipe normalization."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from parse_industry_recipes import extract_recipes, iter_jsonl, normalize_blueprint


NAMES = {
    100: {"name": "Example Blueprint", "published": True, "group_id": 9, "market_group_id": 10,
          "tech_level": 1, "portion_size": 1, "volume": 1.0, "packaged_volume": 1.0},
    200: {"name": "Example Product", "published": True, "group_id": 11, "market_group_id": 12,
          "tech_level": 2, "portion_size": 1, "volume": 2.0, "packaged_volume": 1.0},
    300: {"name": "Example Material", "published": True, "group_id": 13, "market_group_id": 14,
          "tech_level": 1, "portion_size": 1, "volume": 0.1, "packaged_volume": 0.1},
    400: {"name": "Industry", "published": True, "group_id": 15, "market_group_id": None,
          "tech_level": 1, "portion_size": 1, "volume": 0.01, "packaged_volume": 0.01},
}


class RecipeParserTests(unittest.TestCase):
    def setUp(self):
        self.blueprint = {
            "_key": 100,
            "blueprintTypeID": 100,
            "maxProductionLimit": 10000,
            "activities": {
                "manufacturing": {
                    "time": 120,
                    "materials": [{"typeID": 300, "quantity": 4}],
                    "products": [{"typeID": 200, "quantity": 2}],
                    "skills": [{"typeID": 400, "level": 1}],
                },
                "copying": {"time": 60, "materials": [], "skills": []},
            },
        }

    def test_normalizes_manufacturing_recipe_and_names(self):
        result = normalize_blueprint(self.blueprint, NAMES, "manufacturing")
        self.assertEqual(result["blueprint_type_id"], 100)
        self.assertEqual(result["blueprint_name"], "Example Blueprint")
        self.assertEqual(result["materials"][0]["name"], "Example Material")
        self.assertEqual(result["materials"][0]["quantity_per_run"], 4)
        self.assertEqual(result["products"][0]["market_group_id"], 12)
        self.assertEqual(result["products"][0]["tech_level"], 2)
        self.assertTrue(result["products"][0]["published"])
        self.assertEqual(result["products"][0]["quantity_per_run"], 2)
        self.assertEqual(result["base_time_seconds_per_run"], 120)
        self.assertEqual(result["required_skills"][0]["level"], 1)
        self.assertEqual(result["required_skills"][0]["name"], "Industry")
        self.assertIs(result["required_skills"][0]["published"], True)
        self.assertEqual(result["schema_version"], 2)
        self.assertEqual(result["recipe_data_status"], "complete")
        self.assertEqual(
            result["source_field_state"],
            {"materials": "present", "products": "present", "required_skills": "present"},
        )


    def test_missing_skill_metadata_remains_unknown_not_unpublished(self):
        result = normalize_blueprint(self.blueprint, {}, "manufacturing")
        skill = result["required_skills"][0]
        self.assertIsNone(skill["name"])
        self.assertIsNone(skill["published"])
        self.assertEqual(skill["level"], 1)

    def test_absent_activity_is_not_an_error(self):
        self.assertIsNone(normalize_blueprint(self.blueprint, NAMES, "reaction"))

    def test_reaction_activity_is_separated_from_manufacturing(self):
        self.blueprint["activities"]["reaction"] = {
            "time": 360, "materials": [{"typeID": 300, "quantity": 5}],
            "products": [{"typeID": 200, "quantity": 1}],
            "skills": [{"typeID": 400, "level": 1}],
        }
        result = normalize_blueprint(self.blueprint, NAMES, "reaction")
        self.assertEqual(result["activity"], "reaction")
        self.assertEqual(result["base_time_seconds_per_run"], 360)

    def test_rejects_nonpositive_material_quantity(self):
        self.blueprint["activities"]["manufacturing"]["materials"][0]["quantity"] = 0
        with self.assertRaisesRegex(ValueError, "invalid quantity"):
            normalize_blueprint(self.blueprint, NAMES, "manufacturing")

    def test_missing_manufacturing_materials_are_preserved_as_incomplete(self):
        del self.blueprint["activities"]["manufacturing"]["materials"]
        result = normalize_blueprint(self.blueprint, NAMES, "manufacturing")
        self.assertEqual(result["materials"], [])
        self.assertEqual(result["source_field_state"]["materials"], "omitted")
        self.assertEqual(result["recipe_data_status"], "incomplete")

    def test_explicitly_empty_manufacturing_materials_are_distinct_from_omission(self):
        self.blueprint["activities"]["manufacturing"]["materials"] = []
        result = normalize_blueprint(self.blueprint, NAMES, "manufacturing")
        self.assertEqual(result["materials"], [])
        self.assertEqual(result["source_field_state"]["materials"], "empty")
        self.assertEqual(result["recipe_data_status"], "complete")

    def test_missing_products_are_skipped_not_emitted_as_recipes(self):
        del self.blueprint["activities"]["manufacturing"]["products"]
        stats = {}
        result = normalize_blueprint(self.blueprint, NAMES, "manufacturing", stats)
        self.assertIsNone(result)
        self.assertEqual(stats["skipped_without_products"], 1)

    def test_missing_required_reaction_materials_are_rejected(self):
        self.blueprint["activities"]["reaction"] = {
            "time": 360,
            "products": [{"typeID": 200, "quantity": 1}],
            "skills": [{"typeID": 400, "level": 1}],
        }
        with self.assertRaisesRegex(ValueError, "activity.materials is required"):
            normalize_blueprint(self.blueprint, NAMES, "reaction")

    def test_iter_jsonl_supports_direct_and_key_value_records(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "records.jsonl"
            path.write_text(
                json.dumps({"_key": 1, "name": {"en": "Direct"}}) + "\n" +
                json.dumps({"_key": 2, "_value": {"name": {"en": "Wrapped"}}}) + "\n",
                encoding="utf-8",
            )
            records = list(iter_jsonl(path))
        self.assertEqual(records[0]["_key"], 1)
        self.assertEqual(records[1]["_key"], 2)
        self.assertEqual(records[1]["name"]["en"], "Wrapped")

    def test_extracts_both_supported_activity_families(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "types.jsonl").write_text(
                "\n".join(json.dumps({"_key": key, "name": {"en": name["name"]}, "published": name["published"], "groupID": name["group_id"], "marketGroupID": name["market_group_id"], "techLevel": name["tech_level"], "portionSize": name["portion_size"], "volume": name["volume"], "packagedVolume": name["packaged_volume"]})
                           for key, name in NAMES.items()) + "\n",
                encoding="utf-8",
            )
            blueprint = dict(self.blueprint)
            blueprint["activities"] = dict(self.blueprint["activities"])
            blueprint["activities"]["reaction"] = {
                "time": 360, "materials": [{"typeID": 300, "quantity": 5}],
                "products": [{"typeID": 200, "quantity": 1}],
                "skills": [{"typeID": 400, "level": 1}],
            }
            (root / "blueprints.jsonl").write_text(json.dumps(blueprint) + "\n", encoding="utf-8")
            recipes = list(extract_recipes(root))
        self.assertEqual({item["activity"] for item in recipes}, {"manufacturing", "reaction"})


if __name__ == "__main__":
    unittest.main()
