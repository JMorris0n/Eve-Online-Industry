"""Tests for exact-quantity quotes extracted from schema-v4 market summaries."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from market_summary_quotes import get_market_quote, load_market_summary


def fixture():
    return {
        "schema_version": 4,
        "collection": {"retrieved_at": "2026-11-14T18:53:25Z"},
        "execution_model": {
            "minimum_volume_enforced_for_sell_into_bids": True,
            "min_volume_semantics": "per_individual_buy_order_fill_with_final_remainder_exception",
        },
        "summaries": [{
            "region_id": 100,
            "type_id": 34,
            "source_files": [{
                "filename": "market-orders-region-100-type-34-page-1.json",
                "sha256": "abc123",
                "retrieved_at": "2026-11-14T18:53:19Z",
                "expires": "Sat, 14 Nov 2026 18:53:55 GMT",
                "etag": "etag",
            }],
            "location_books": [{
                "location_id": 6001,
                "system_id": 3001,
                "system_ids": [3001],
                "order_book": {
                    "market_scope": "target_location",
                    "caveat": "screening only",
                    "range_resolution": {"unknown_range_buy_orders": 0},
                    "buy_from_asks": [{
                        "requested_quantity": 100,
                        "filled_quantity": 100,
                        "unfilled_quantity": 0,
                        "vwap": 5.0,
                        "gross_value_isk": 500.0,
                        "worst_fill_price": 5.0,
                        "fully_fillable_in_snapshot": True,
                    }],
                    "sell_into_bids": [{
                        "requested_quantity": 100,
                        "filled_quantity": 80,
                        "unfilled_quantity": 20,
                        "vwap": 4.5,
                        "gross_value_isk": 360.0,
                        "worst_fill_price": 4.4,
                        "fully_fillable_in_snapshot": False,
                        "minimum_volume_enforced": True,
                        "filled_order_count": 2,
                        "orders_skipped_because_fill_below_min_volume": 1,
                        "orders_skipped_with_invalid_min_volume": 0,
                    }],
                },
            }],
        }],
    }


class MarketSummaryQuoteTests(unittest.TestCase):
    def test_load_accepts_schema_v4(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "summary.json"
            path.write_text(json.dumps(fixture()), encoding="utf-8")
            self.assertEqual(load_market_summary(path)["schema_version"], 4)

    def test_load_rejects_schema_v3(self):
        data = fixture()
        data["schema_version"] = 3
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "summary.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "schema_version must be 4"):
                load_market_summary(path)

    def test_procurement_quote_uses_exact_ask_sweep(self):
        quote = get_market_quote(
            fixture(), region_id=100, type_id=34, location_id=6001,
            quantity=100, purpose="procurement",
        )
        self.assertEqual(quote["status"], "full")
        self.assertEqual(quote["vwap_isk"], 5.0)
        self.assertEqual(quote["gross_value_isk"], 500.0)
        self.assertEqual(quote["source_timestamp"], "2026-11-14T18:53:19Z")
        self.assertEqual(quote["order_book_source"]["source_files"][0]["sha256"], "abc123")

    def test_liquidation_quote_preserves_partial_fill_and_minimum_volume(self):
        quote = get_market_quote(
            fixture(), region_id=100, type_id=34, location_id=6001,
            quantity=100, purpose="liquidation",
        )
        self.assertEqual(quote["status"], "partial")
        self.assertEqual(quote["filled_quantity"], 80)
        self.assertEqual(quote["unfilled_quantity"], 20)
        self.assertEqual(quote["gross_value_isk"], 360.0)
        self.assertTrue(quote["minimum_volume_enforced"])
        self.assertEqual(quote["orders_skipped_below_minimum"], 1)
        self.assertTrue(quote["warnings"])

    def test_rejects_quantity_not_summarized_exactly(self):
        with self.assertRaisesRegex(ValueError, "No 250-unit"):
            get_market_quote(
                fixture(), region_id=100, type_id=34, location_id=6001,
                quantity=250, purpose="procurement",
            )

    def test_rejects_missing_minimum_volume_enforcement(self):
        data = fixture()
        data["summaries"][0]["location_books"][0]["order_book"]["sell_into_bids"][0].pop("minimum_volume_enforced")
        with self.assertRaisesRegex(ValueError, "does not confirm minimum-volume"):
            get_market_quote(
                data, region_id=100, type_id=34, location_id=6001,
                quantity=100, purpose="liquidation",
            )

    def test_rejects_inconsistent_fill_quantity(self):
        data = fixture()
        data["summaries"][0]["location_books"][0]["order_book"]["buy_from_asks"][0]["filled_quantity"] = 99
        with self.assertRaisesRegex(ValueError, "do not reconcile"):
            get_market_quote(
                data, region_id=100, type_id=34, location_id=6001,
                quantity=100, purpose="procurement",
            )

    def test_rejects_unknown_purpose_and_nonpositive_quantity(self):
        with self.assertRaisesRegex(ValueError, "purpose must be"):
            get_market_quote(
                fixture(), region_id=100, type_id=34, location_id=6001,
                quantity=100, purpose="arbitrage",
            )
        with self.assertRaisesRegex(ValueError, "quantity must be"):
            get_market_quote(
                fixture(), region_id=100, type_id=34, location_id=6001,
                quantity=0, purpose="procurement",
            )


if __name__ == "__main__":
    unittest.main()
