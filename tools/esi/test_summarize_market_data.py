"""Tests for public ESI order-book and history summarization."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from summarize_market_data import summarize_book, summarize_directory, summarize_history, sweep


class MarketSummaryTests(unittest.TestCase):
    def test_sweep_computes_partial_fill_vwap(self):
        result = sweep([(10, 2), (12, 5)], 4)
        self.assertEqual(result["filled_quantity"], 4)
        self.assertEqual(result["unfilled_quantity"], 0)
        self.assertEqual(result["gross_value_isk"], 44)
        self.assertEqual(result["vwap"], 11)
        self.assertTrue(result["fully_fillable_in_snapshot"])

    def test_sweep_reports_insufficient_depth(self):
        result = sweep([(10, 2)], 5)
        self.assertEqual(result["filled_quantity"], 2)
        self.assertEqual(result["unfilled_quantity"], 3)
        self.assertFalse(result["fully_fillable_in_snapshot"])

    def test_book_separates_bids_and_asks(self):
        orders = [
            {"price": 12, "volume_remain": 3, "is_buy_order": False, "location_id": 10},
            {"price": 10, "volume_remain": 4, "is_buy_order": False, "location_id": 10},
            {"price": 9, "volume_remain": 5, "is_buy_order": True, "location_id": 10},
            {"price": 8, "volume_remain": 7, "is_buy_order": True, "location_id": 10},
        ]
        result = summarize_book(orders, [2])
        self.assertEqual(result["best_ask"], 10)
        self.assertEqual(result["best_bid"], 9)
        self.assertEqual(result["spread_isk"], 1)
        self.assertEqual(result["buy_from_asks"][0]["vwap"], 10)
        self.assertEqual(result["sell_into_bids"][0]["vwap"], 9)

    def test_history_uses_volume_weighted_price(self):
        rows = [
            {"date": "2026-11-01", "volume": 10, "order_count": 2, "average": 100, "highest": 110, "lowest": 90},
            {"date": "2026-11-02", "volume": 30, "order_count": 3, "average": 200, "highest": 210, "lowest": 190},
        ]
        result = summarize_history(rows)
        self.assertEqual(result["total_volume"], 40)
        self.assertEqual(result["average_daily_volume"], 20)
        self.assertEqual(result["volume_weighted_average_daily_price"], 175)
        self.assertEqual(result["first_date"], "2026-11-01")
        self.assertEqual(result["last_date"], "2026-11-02")

    def test_directory_groups_order_pages_and_history(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "market-orders-region-100-type-200-page-1.json").write_text(
                json.dumps([{"order_id": 1, "type_id": 200, "price": 5, "volume_remain": 3, "is_buy_order": False, "location_id": 6001, "system_id": 3001}]),
                encoding="utf-8",
            )
            (root / "market-orders-region-100-type-200-page-2.json").write_text(
                json.dumps([{"order_id": 2, "type_id": 200, "price": 4, "volume_remain": 2, "is_buy_order": True, "location_id": 6002, "system_id": 3002}]),
                encoding="utf-8",
            )
            (root / "manifest.json").write_text(json.dumps({
                "retrieved_at": "2026-11-14T10:00:00Z",
                "compatibility_date": "2026-11-13",
                "regions": [100],
                "type_ids": [200],
                "outputs": [{
                    "file": str(root / "market-orders-region-100-type-200-page-1.json"),
                    "url": "https://esi.example/orders",
                    "status": 200,
                    "retrieved_at": "2026-11-14T10:00:01Z",
                    "from_cache": False,
                    "expires": "Fri, 14 Nov 2026 10:05:00 GMT",
                    "etag": "test-etag",
                    "sha256": "manifest-hash"
                }]
            }), encoding="utf-8")
            (root / "market-history-region-100-type-200.json").write_text(
                json.dumps([{"date": "2026-11-01", "volume": 2, "order_count": 1, "average": 4, "highest": 4, "lowest": 4}]),
                encoding="utf-8",
            )
            result = summarize_directory(root, [1])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["order_book"]["order_count"], 2)
        self.assertEqual(result[0]["raw_order_record_count"], 2)
        self.assertEqual(result[0]["duplicate_order_ids_removed"], 0)
        self.assertEqual(result[0]["history"]["total_volume"], 2)
        self.assertEqual(result[0]["location_count"], 2)
        self.assertEqual(result[0]["orders_without_location_id"], 0)
        location_ids = [item["location_id"] for item in result[0]["location_books"]]
        self.assertEqual(location_ids, [6001, 6002])
        self.assertEqual(
            [item["order_book"]["order_count"] for item in result[0]["location_books"]],
            [1, 1],
        )
        self.assertFalse(result[0]["order_book"]["is_crossed"])
        self.assertEqual(result[0]["order_book"]["market_scope"], "regional_composite")
        page_one_source = next(item for item in result[0]["source_files"] if item["filename"].endswith("page-1.json"))
        self.assertEqual(page_one_source["retrieved_at"], "2026-11-14T10:00:01Z")

    def test_directory_deduplicates_order_ids_across_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repeated = {"order_id": 7, "type_id": 200, "price": 5, "volume_remain": 3, "is_buy_order": False, "location_id": 6001}
            (root / "market-orders-region-100-type-200-page-1.json").write_text(json.dumps([repeated]), encoding="utf-8")
            (root / "market-orders-region-100-type-200-page-2.json").write_text(json.dumps([repeated]), encoding="utf-8")
            result = summarize_directory(root, [1])
        self.assertEqual(result[0]["raw_order_record_count"], 2)
        self.assertEqual(result[0]["duplicate_order_ids_removed"], 1)
        self.assertEqual(result[0]["order_book"]["order_count"], 1)

    def test_order_pages_are_sorted_numerically_before_duplicate_resolution(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page_two = {"order_id": 9, "type_id": 200, "price": 5, "volume_remain": 2, "is_buy_order": False, "location_id": 6001}
            page_ten = {"order_id": 9, "type_id": 200, "price": 5, "volume_remain": 7, "is_buy_order": False, "location_id": 6001}
            (root / "market-orders-region-100-type-200-page-2.json").write_text(json.dumps([page_two]), encoding="utf-8")
            (root / "market-orders-region-100-type-200-page-10.json").write_text(json.dumps([page_ten]), encoding="utf-8")
            result = summarize_directory(root, [1])
        self.assertEqual(result[0]["duplicate_order_ids_removed"], 1)
        self.assertEqual(result[0]["order_book"]["sell_volume"], 7)

    def test_rejects_order_type_mismatch(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            order = {"order_id": 7, "type_id": 999, "price": 5, "volume_remain": 3, "is_buy_order": False}
            (root / "market-orders-region-100-type-200-page-1.json").write_text(json.dumps([order]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unexpected type_id"):
                summarize_directory(root, [1])


    def test_flags_crossed_regional_composite_without_calling_it_arbitrage(self):
        orders = [
            {"price": 20, "volume_remain": 5, "is_buy_order": True, "location_id": 6001},
            {"price": 18, "volume_remain": 5, "is_buy_order": False, "location_id": 6002},
        ]
        result = summarize_book(orders, [1])
        self.assertTrue(result["is_crossed"])
        self.assertEqual(result["spread_isk"], 2)
        self.assertIn("not proof of arbitrage", result["caveat"])

    def test_directory_counts_orders_with_missing_location_id(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "market-orders-region-100-type-200-page-1.json").write_text(
                json.dumps([
                    {"order_id": 1, "type_id": 200, "price": 5, "volume_remain": 3, "is_buy_order": False}
                ]),
                encoding="utf-8",
            )
            result = summarize_directory(root, [1])
        self.assertEqual(result[0]["orders_without_location_id"], 1)
        self.assertEqual(result[0]["location_count"], 0)

    def test_rejects_invalid_buy_order_flag(self):
        with self.assertRaisesRegex(ValueError, "must be boolean"):
            summarize_book([{"price": 1, "volume_remain": 1, "is_buy_order": "false"}], [1])


if __name__ == "__main__":
    unittest.main()
