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


def market_summary_fixture():
    def type_record(type_id, purpose, requested, filled, unit_price):
        asks = [{
            "requested_quantity": requested,
            "filled_quantity": requested if purpose == "procurement" else 0,
            "unfilled_quantity": 0 if purpose == "procurement" else requested,
            "vwap": unit_price if purpose == "procurement" else None,
            "gross_value_isk": requested * unit_price if purpose == "procurement" else None,
            "worst_fill_price": unit_price if purpose == "procurement" else None,
            "fully_fillable_in_snapshot": purpose == "procurement",
        }]
        bids = [{
            "requested_quantity": requested,
            "filled_quantity": filled,
            "unfilled_quantity": requested - filled,
            "vwap": unit_price if filled else None,
            "gross_value_isk": filled * unit_price if filled else None,
            "worst_fill_price": unit_price if filled else None,
            "fully_fillable_in_snapshot": filled == requested,
            "minimum_volume_enforced": True,
            "filled_order_count": 1 if filled else 0,
            "orders_skipped_because_fill_below_min_volume": 0,
            "orders_skipped_with_invalid_min_volume": 0,
        }]
        return {
            "region_id": 100,
            "type_id": type_id,
            "source_files": [{
                "filename": f"market-orders-region-100-type-{type_id}-page-1.json",
                "sha256": f"hash-{type_id}",
                "retrieved_at": "2026-11-14T19:59:30Z",
                "expires": "Sat, 14 Nov 2026 20:00:30 GMT",
            }],
            "location_books": [{
                "location_id": 6001,
                "system_id": 3001,
                "system_ids": [3001],
                "order_book": {
                    "market_scope": "target_location",
                    "range_resolution": {"unknown_range_buy_orders": 0},
                    "buy_from_asks": asks,
                    "sell_into_bids": bids,
                    "caveat": "synthetic fixture",
                },
            }],
        }
    return {
        "schema_version": 4,
        "collection": {"retrieved_at": "2026-11-14T19:59:30Z"},
        "execution_model": {
            "minimum_volume_enforced_for_sell_into_bids": True,
            "min_volume_semantics": "per_individual_buy_order_fill_with_final_remainder_exception",
        },
        "summaries": [
            type_record(900003, "procurement", 20, 0, 10),
            type_record(900004, "procurement", 30, 0, 20),
            type_record(900002, "liquidation", 10, 6, 20),
        ],
    }


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

    def test_market_summary_prices_materials_and_partial_liquidation(self):
        config = copy.deepcopy(self.config)
        config["market_summary"] = {
            "file": None,
            "region_id": 100,
            "location_id": 6001,
            "evaluation_time_utc": "2026-11-14T20:00:00Z",
            "max_snapshot_age_minutes": 2,
        }
        for line in config["industry_quote"]["materials"]:
            line.pop("unit_value_isk")
            line.pop("valuation_basis")
            line["valuation_source"] = "market_summary_v4"
        config["sale_scenarios"][0]["evidence_basis"] = "v4_order_book_estimate"
        config["sale_scenarios"][0]["sale"]["fills"] = []
        config["sale_scenarios"][0]["market_summary_quote"] = {}

        with tempfile.TemporaryDirectory() as directory:
            summary_file = Path(directory) / "market-summary-v4.json"
            summary_file.write_text(json.dumps(market_summary_fixture()), encoding="utf-8")
            config["market_summary"]["file"] = str(summary_file)
            result = evaluate(config)

        calculation = result["sale_scenarios"][0]["calculation"]
        self.assertEqual(calculation["batch_costs"]["materials_isk"], "800.00")
        self.assertEqual(calculation["realized_sales"]["sold_units"], "6")
        self.assertEqual(calculation["realized_sales"]["unsold_units"], "4")
        self.assertEqual(len(result["market_summary"]["quotes"]), 3)
        self.assertFalse(any("older than" in warning for warning in result["warnings"]))

    def test_market_summary_quote_warns_when_snapshot_is_stale_or_cache_expired(self):
        config = copy.deepcopy(self.config)
        config["market_summary"] = {
            "file": None,
            "region_id": 100,
            "location_id": 6001,
            "evaluation_time_utc": "2026-11-14T21:00:00Z",
            "max_snapshot_age_minutes": 5,
        }
        for line in config["industry_quote"]["materials"]:
            line.pop("unit_value_isk")
            line.pop("valuation_basis")
            line["valuation_source"] = "market_summary_v4"
        config["sale_scenarios"][0]["evidence_basis"] = "v4_order_book_estimate"
        config["sale_scenarios"][0]["sale"]["fills"] = []
        config["sale_scenarios"][0]["market_summary_quote"] = {}
        with tempfile.TemporaryDirectory() as directory:
            summary_file = Path(directory) / "market-summary-v4.json"
            summary_file.write_text(json.dumps(market_summary_fixture()), encoding="utf-8")
            config["market_summary"]["file"] = str(summary_file)
            result = evaluate(config)
        self.assertTrue(any("older than the configured" in warning for warning in result["warnings"]))
        self.assertTrue(any("cache window had expired" in warning for warning in result["warnings"]))

    def test_market_summary_procurement_requires_complete_quantity(self):
        config = copy.deepcopy(self.config)
        summary = market_summary_fixture()
        ask = summary["summaries"][0]["location_books"][0]["order_book"]["buy_from_asks"][0]
        ask["filled_quantity"] = 10
        ask["unfilled_quantity"] = 10
        ask["fully_fillable_in_snapshot"] = False
        config["market_summary"] = {
            "file": None,
            "region_id": 100,
            "location_id": 6001,
            "evaluation_time_utc": "2026-11-14T20:00:00Z",
        }
        for line in config["industry_quote"]["materials"]:
            line.pop("unit_value_isk")
            line.pop("valuation_basis")
            line["valuation_source"] = "market_summary_v4"
        with tempfile.TemporaryDirectory() as directory:
            summary_file = Path(directory) / "market-summary-v4.json"
            summary_file.write_text(json.dumps(summary), encoding="utf-8")
            config["market_summary"]["file"] = str(summary_file)
            with self.assertRaisesRegex(ValueError, "procurement quote is not fully fillable"):
                evaluate(config)

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
