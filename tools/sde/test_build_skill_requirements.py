"""Tests for local recipe-derived skill requirements reference."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from build_skill_requirements import build_skill_reference


def recipe(
    blueprint_id: int = 100,
    *,
    activity: str = "manufacturing",
    blueprint_published: bool = True,
    product_published: bool = True,
    materials_state: str = "present",
    recipe_status: str = "complete",
    skills_state: str = "present",
    skills: list[dict] | None = None,
    base_time: int = 120,
) -> dict:
    return {
        "schema_version": 2,
        "activity": activity,
        "recipe_data_status": recipe_status,
        "source_field_state": {
            "materials": materials_state,
            "products": "present",
            "required_skills": skills_state,
        },
        "blueprint_type_id": blueprint_id,
        "blueprint_name": f"Blueprint {blueprint_id}",
        "blueprint_published": blueprint_published,
        "base_time_seconds_per_run": base_time,
        "materials": [{
            "type_id": 300,
            "name": "Material",
            "quantity_per_run": 4,
            "published": True,
        }] if materials_state == "present" else [],
        "products": [{
            "type_id": 200,
            "name": "Product",
            "quantity_per_run": 2,
            "published": product_published,
        }],
        "required_skills": skills if skills is not None else [{
            "type_id": 400,
            "name": "Industry",
            "level": 2,
            "published": True,
        }],
    }


class SkillReferenceTests(unittest.TestCase):
    def write_records(self, path: Path, records: list[dict]) -> None:
        path.write_text(
            "".join(json.dumps(item) + "\n" for item in records),
            encoding="utf-8",
        )

    def test_builds_profile_capture_skills_from_eligible_recipes(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "recipes.jsonl"
            self.write_records(source, [recipe()])
            report = build_skill_reference(source)

        self.assertEqual(report["summary"]["source_recipe_count"], 1)
        self.assertEqual(report["summary"]["eligible_recipe_count"], 1)
        self.assertEqual(report["summary"]["profile_capture_skill_count"], 1)
        skill = report["profile_capture_skills"][0]
        self.assertEqual(skill["type_id"], 400)
        self.assertEqual(skill["name"], "Industry")
        self.assertEqual(skill["max_candidate_required_level"], 2)
        self.assertEqual(report["eligible_recipes"][0]["blueprint_type_id"], 100)

    def test_aggregates_recipe_coverage_and_required_levels(self):
        first = recipe(100)
        second = recipe(101, activity="reaction")
        second["required_skills"] = [
            {"type_id": 400, "name": "Industry", "level": 3, "published": True},
            {"type_id": 401, "name": "Advanced Industry", "level": 1, "published": True},
        ]
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "recipes.jsonl"
            self.write_records(source, [first, second])
            report = build_skill_reference(source)

        by_id = {row["type_id"]: row for row in report["all_observed_skill_types"]}
        self.assertEqual(by_id[400]["candidate_recipe_count"], 2)
        self.assertEqual(by_id[400]["candidate_required_level_counts"], {"2": 1, "3": 1})
        self.assertEqual(by_id[400]["candidate_activity_recipe_counts"], {
            "manufacturing": 1, "reaction": 1,
        })
        self.assertEqual(by_id[401]["candidate_recipe_count"], 1)
        self.assertEqual(report["summary"]["eligible_recipe_counts_by_activity"], {
            "manufacturing": 1, "reaction": 1,
        })

    def test_unpublished_required_skill_is_preserved_but_not_a_profile_capture_skill(self):
        item = recipe(100)
        item["required_skills"][0]["published"] = False
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "recipes.jsonl"
            self.write_records(source, [item])
            report = build_skill_reference(source)

        self.assertEqual(report["summary"]["eligible_recipe_count"], 0)
        self.assertEqual(report["summary"]["unpublished_skill_type_id_count"], 1)
        self.assertEqual(report["unpublished_skill_exceptions"][0]["type_id"], 400)
        self.assertEqual(report["profile_capture_skills"], [])
        self.assertIn(
            "unpublished_required_skill",
            report["excluded_recipe_samples"][0]["reason_codes"],
        )

    def test_missing_skill_array_is_not_interpreted_as_no_requirements(self):
        item = recipe(100, skills_state="omitted", skills=[])
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "recipes.jsonl"
            self.write_records(source, [item])
            report = build_skill_reference(source)

        self.assertEqual(report["summary"]["eligible_recipe_count"], 0)
        self.assertEqual(report["summary"]["recipes_with_missing_skill_arrays"], 1)
        self.assertIn(
            "skill_requirements_unavailable_or_incomplete",
            report["excluded_recipe_samples"][0]["reason_codes"],
        )

    def test_excludes_incomplete_unpublished_zero_time_and_unresolved_inputs(self):
        incomplete = recipe(100, materials_state="omitted", recipe_status="incomplete")
        unpublished = recipe(101, blueprint_published=False)
        zero_time = recipe(102, base_time=0)
        unresolved_material = recipe(103)
        unresolved_material["materials"][0]["name"] = None
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "recipes.jsonl"
            self.write_records(source, [incomplete, unpublished, zero_time, unresolved_material])
            report = build_skill_reference(source)

        self.assertEqual(report["summary"]["eligible_recipe_count"], 0)
        reasons = {
            reason
            for sample in report["excluded_recipe_samples"]
            for reason in sample["reason_codes"]
        }
        self.assertTrue({
            "incomplete_recipe_data",
            "unpublished_blueprint",
            "zero_or_invalid_base_time",
            "unresolved_material_metadata",
        }.issubset(reasons))

    def test_requires_a_published_resolved_product(self):
        item = recipe(100, product_published=False)
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "recipes.jsonl"
            self.write_records(source, [item])
            report = build_skill_reference(source)

        self.assertEqual(report["summary"]["eligible_recipe_count"], 0)
        self.assertIn(
            "no_published_resolvable_output",
            report["excluded_recipe_samples"][0]["reason_codes"],
        )

    def test_activity_filter_limits_the_reference(self):
        manufacturing = recipe(100)
        reaction = recipe(101, activity="reaction")
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "recipes.jsonl"
            self.write_records(source, [manufacturing, reaction])
            report = build_skill_reference(source, activity="manufacturing")

        self.assertEqual(report["activity_filter"], "manufacturing")
        self.assertEqual(report["summary"]["source_recipe_count"], 1)
        self.assertEqual(report["summary"]["eligible_recipe_count"], 1)
        self.assertEqual(report["summary"]["source_recipe_counts_by_activity"], {"manufacturing": 1})

    def test_rejects_invalid_json_with_line_number(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "bad.jsonl"
            source.write_text("{}\n{bad json}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, r"bad.jsonl:2: invalid JSON"):
                build_skill_reference(source)

    def test_rejects_invalid_arguments_and_missing_file(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "recipes.jsonl"
            self.write_records(source, [recipe()])
            with self.assertRaisesRegex(ValueError, "sample_limit"):
                build_skill_reference(source, sample_limit=0)
            with self.assertRaisesRegex(ValueError, "activity must be"):
                build_skill_reference(source, activity="copying")
            with self.assertRaises(FileNotFoundError):
                build_skill_reference(Path(temp) / "missing.jsonl")


if __name__ == "__main__":
    unittest.main()
