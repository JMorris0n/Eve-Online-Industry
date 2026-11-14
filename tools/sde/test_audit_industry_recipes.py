"""Tests for the normalized SDE recipe audit."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from audit_industry_recipes import audit_recipes


def recipe(
    blueprint_id: int = 100,
    activity: str = "manufacturing",
    *,
    completeness: str = "complete",
    materials_state: str = "present",
    base_time: int = 120,
) -> dict:
    return {
        "schema_version": 2,
        "activity": activity,
        "recipe_data_status": completeness,
        "source_field_state": {
            "materials": materials_state,
            "products": "present",
            "required_skills": "empty",
        },
        "blueprint_type_id": blueprint_id,
        "blueprint_name": None if blueprint_id == 100 else "Example Blueprint",
        "blueprint_published": False if blueprint_id == 100 else True,
        "base_time_seconds_per_run": base_time,
        "materials": [{
            "type_id": 300,
            "name": None,
            "quantity_per_run": 4,
            "published": False,
        }],
        "products": [{
            "type_id": 200,
            "name": "Example Product",
            "quantity_per_run": 2,
            "published": False,
        }],
        "required_skills": [{
            "type_id": 400,
            "name": None,
            "level": 1,
        }],
    }


class RecipeAuditTests(unittest.TestCase):
    def write_records(self, path: Path, records: list[dict]) -> None:
        path.write_text(
            "".join(json.dumps(item) + "\n" for item in records),
            encoding="utf-8",
        )

    def test_counts_duplicates_completeness_metadata_and_exceptions(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "recipes.jsonl"
            incomplete = recipe(
                101,
                completeness="incomplete",
                materials_state="omitted",
            )
            incomplete["materials"] = []
            incomplete["source_field_state"]["required_skills"] = "omitted"
            self.write_records(
                source,
                [recipe(), recipe(), incomplete, recipe(102, "reaction", base_time=0)],
            )
            report = audit_recipes(source, max_samples=5)

        self.assertEqual(report["record_count"], 4)
        self.assertEqual(report["activity_counts"]["manufacturing"], 3)
        self.assertEqual(report["activity_counts"]["reaction"], 1)
        self.assertEqual(report["recipe_completeness_counts"]["complete"], 3)
        self.assertEqual(report["recipe_completeness_counts"]["incomplete"], 1)
        self.assertEqual(report["recipe_key_quality"]["duplicate_key_repeats"], 1)
        self.assertEqual(report["recipe_key_quality"]["duplicate_key_count"], 1)
        self.assertEqual(report["type_metadata"]["unique_unresolved_type_id_count"], 3)
        self.assertEqual(report["type_metadata"]["unpublished_product_type_id_count"], 1)
        self.assertEqual(report["exceptional_records"]["zero_base_time_recipe_count"], 1)
        self.assertEqual(report["exceptional_records"]["unpublished_blueprint_record_count"], 2)
        self.assertEqual(report["structural_quality"]["record_validation_issue_count"], 0)

    def test_report_counts_exceptions_beyond_sample_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "many-recipes.jsonl"
            self.write_records(source, [recipe(), recipe(101), recipe(102, base_time=0), recipe(103, base_time=0)])
            report = audit_recipes(source, max_samples=1)
        self.assertEqual(report["exceptional_records"]["zero_base_time_recipe_count"], 2)
        self.assertEqual(len(report["exceptional_records"]["zero_base_time_recipe_samples"]), 1)
        self.assertEqual(report["exceptional_records"]["unpublished_blueprint_record_count"], 2)
        self.assertEqual(len(report["exceptional_records"]["unpublished_blueprint_record_samples"]), 1)

    def test_rejects_invalid_json_line_with_line_number(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "bad.jsonl"
            source.write_text("{}\n{bad json}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, r"bad.jsonl:2: invalid JSON"):
                audit_recipes(source)

    def test_requires_positive_sample_size(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "recipes.jsonl"
            self.write_records(source, [recipe()])
            with self.assertRaisesRegex(ValueError, "max_samples must be >= 1"):
                audit_recipes(source, max_samples=0)


if __name__ == "__main__":
    unittest.main()
