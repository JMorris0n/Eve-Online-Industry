"""Tests for the quote-first single-product evaluator."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from product_evaluation import evaluate


ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "tools" / "calculations" / "product-evaluation.example.json"


class ProductEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_synthetic_example_evaluates_both_sale_strategies(self):
        result = evaluate(self.config)
        self.assertEqual(result["candidate"]["output_units"], 10)
        self.assertEqual(result["industry_quote"]["manufacturing_slot_hours"], "1")
        self.assertEqual(len(result["sale_scenarios"]), 2)
        immediate = result["sale_scenarios"][0]["calculation"]
        listed = result["sale_scenarios"][1]["calculation"]
        self.assertEqual(
            immediate["full_batch_projection"]["projected_contribution_isk"],
            "500.00",
        )
        self.assertEqual(
            immediate["full_batch_projection"]["isk_per_active_operator_hour"],
            "1000.00",
        )
        self.assertEqual(
            listed["realized_sales"]["unsold_inventory_cost_basis_isk"],
            "560.00",
        )
        self.assertFalse(result["decision"]["risk_adjustment_applied"])

    def test_rejects_quote_output_that_disagrees_with_sde_yield(self):
        config = copy.deepcopy(self.config)
        config["industry_quote"]["output_units"] = 9
        with self.assertRaisesRegex(ValueError, "does not match SDE product yield"):
            evaluate(config)

    def test_rejects_jobs_that_do_not_cover_candidate_runs(self):
        config = copy.deepcopy(self.config)
        config["industry_quote"]["jobs"][0]["runs"] = 9
        with self.assertRaisesRegex(ValueError, "job runs total"):
            evaluate(config)

    def test_rejects_job_above_sde_maximum_production_limit(self):
        config = copy.deepcopy(self.config)
        config["candidate"]["runs"] = 101
        config["industry_quote"]["jobs"] = [{"runs": 101, "duration_seconds": 3600}]
        config["industry_quote"]["output_units"] = 101
        with self.assertRaisesRegex(ValueError, "maximum production limit"):
            evaluate(config)

    def test_bpc_total_licensed_runs_are_checked(self):
        config = copy.deepcopy(self.config)
        config["blueprint"] = {
            "kind": "BPC", "quantity": 1, "material_efficiency": 10,
            "time_efficiency": 20, "licensed_runs": 5,
        }
        with self.assertRaisesRegex(ValueError, "exceed the total licensed runs"):
            evaluate(config)

    def test_incomplete_sde_material_recipe_is_rejected(self):
        config = copy.deepcopy(self.config)
        original = json.loads(
            (ROOT / "tools" / "calculations" / "fixtures" / "synthetic-manufacturing-recipe.jsonl")
            .read_text(encoding="utf-8")
        )
        original["recipe_data_status"] = "incomplete"
        original["source_field_state"]["materials"] = "omitted"
        with tempfile.TemporaryDirectory() as temp:
            recipe_file = Path(temp) / "recipe.jsonl"
            recipe_file.write_text(json.dumps(original) + "\n", encoding="utf-8")
            config["recipe_file"] = str(recipe_file)
            with self.assertRaisesRegex(ValueError, "recipe is incomplete"):
                evaluate(config)

    def test_missing_quote_material_is_reported_for_review(self):
        config = copy.deepcopy(self.config)
        config["industry_quote"]["materials"] = config["industry_quote"]["materials"][:1]
        result = evaluate(config)
        self.assertEqual(result["industry_quote"]["missing_from_quote_type_ids"], [900004])
        self.assertTrue(any("absent from the complete Industry quote" in item for item in result["warnings"]))

    def test_active_time_can_remain_unknown(self):
        config = copy.deepcopy(self.config)
        config["operating"].pop("active_operator_hours")
        config["operating"]["active_time_basis"] = "unknown"
        result = evaluate(config)
        projected = result["sale_scenarios"][0]["calculation"]["full_batch_projection"]
        self.assertIsNone(projected["isk_per_active_operator_hour"])
        self.assertIsNone(result["operating"]["active_operator_hours"])


if __name__ == "__main__":
    unittest.main()
