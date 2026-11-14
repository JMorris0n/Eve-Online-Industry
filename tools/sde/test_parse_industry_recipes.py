"""Tests for current-format SDE recipe normalization."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from parse_industry_recipes import extract_recipes, iter_jsonl, normalize_blueprint


NAMES = {
    100: "Example Blueprint",
    200: "Example Product",
    300: "Example Material",
    400: "Industry",
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
        self.assertEqual(result["products"][0]["quantity_per_run"], 2)
        self.assertEqual(result["base_time_seconds_per_run"], 120)
        self.assertEqual(result["required_skills"][0]["level"], 1)

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

    def test_rejects_missing_products(self):
        self.blueprint["activities"]["manufacturing"]["products"] = []
        with self.assertRaisesRegex(ValueError, "has no products"):
            normalize_blueprint(self.blueprint, NAMES, "manufacturing")

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
                "\n".join(json.dumps({"_key": key, "name": {"en": name}})
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
