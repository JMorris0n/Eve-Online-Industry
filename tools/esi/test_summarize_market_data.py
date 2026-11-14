"""Tests for public ESI order-book and history summarization."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from summarize_market_data import (
    SUMMARY_SCHEMA_VERSION,
    classify_buy_order_range,
    load_sde_market_map,
    shortest_jump_distances,
    summarize_book,
    summarize_directory,
    summarize_history,
    summarize_target_location_book,
    sweep,
    sweep_buy_orders,
)


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
        self.assertEqual(len(result[0]["posted_location_books"]), 2)
        self.assertEqual(result[0]["orders_without_location_id"], 0)
        location_ids = [item["location_id"] for item in result[0]["location_books"]]
        self.assertEqual(location_ids, [6001, 6002])
        self.assertEqual(
            [item["order_book"]["order_count"] for item in result[0]["location_books"]],
            [1, 1],
        )
        self.assertEqual(
            [item["system_ids"] for item in result[0]["location_books"]],
            [[3001], [3002]],
        )
        self.assertTrue(
            all(not item["order_book"]["is_crossed"] for item in result[0]["location_books"])
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
        self.assertEqual(result["spread_isk"], -2)
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

    def test_report_schema_version_is_current(self):
        self.assertEqual(SUMMARY_SCHEMA_VERSION, 4)

    def test_rejects_invalid_buy_order_flag(self):
        with self.assertRaisesRegex(ValueError, "must be boolean"):
            summarize_book([{"price": 1, "volume_remain": 1, "is_buy_order": "false"}], [1])


    def test_load_sde_market_map_and_calculates_source_to_target_jump_distances(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            systems = [
                {"_key": 3001, "regionID": 100},
                {"_key": 3002, "regionID": 100},
                {"_key": 3003, "regionID": 100},
                {"_key": 3004, "regionID": 100},
                {"_key": 4001, "regionID": 200},
            ]
            gates = [
                {"_key": 5001, "solarSystemID": 3002, "destination": {"solarSystemID": 3001}},
                {"_key": 5002, "solarSystemID": 3003, "destination": {"solarSystemID": 3002}},
                {"_key": 5003, "solarSystemID": 4001, "destination": {"solarSystemID": 3001}},
                {"_key": 5004, "solarSystemID": 3004, "destination": {"solarSystemID": 4001}},
            ]
            (root / "mapSolarSystems.jsonl").write_text(
                "\n".join(json.dumps(item) for item in systems) + "\n", encoding="utf-8"
            )
            (root / "mapStargates.jsonl").write_text(
                "\n".join(json.dumps(item) for item in gates) + "\n", encoding="utf-8"
            )
            market_map = load_sde_market_map(root)
        distances = shortest_jump_distances(
            3001, market_map["reverse_adjacency"], market_map["system_regions"], 100
        )
        self.assertEqual(distances[3001], 0)
        self.assertEqual(distances[3002], 1)
        self.assertEqual(distances[3003], 2)
        self.assertEqual(distances[4001], 1)
        self.assertEqual(distances[3004], 2)

    def test_classifies_station_system_region_and_numeric_ranges(self):
        system_regions = {3001: 100, 3002: 100, 3003: 100}
        reverse_adjacency = {3001: {3002}, 3002: {3003}, 3003: set()}
        distances = shortest_jump_distances(3001, reverse_adjacency, system_regions, 100)

        def classify(order):
            return classify_buy_order_range(
                order, target_location_id=6001, target_system_id=3001,
                target_region_id=100, system_regions=system_regions,
                jump_distances=distances,
            )

        self.assertEqual(classify({"location_id": 6001, "system_id": 3001, "range": "station"})[0], "eligible")
        self.assertEqual(classify({"location_id": 6002, "system_id": 3001, "range": "station"})[0], "excluded")
        self.assertEqual(classify({"location_id": 6002, "system_id": 3001, "range": "solarsystem"})[0], "eligible")
        self.assertEqual(classify({"location_id": 6002, "system_id": 3002, "range": "solarsystem"})[0], "excluded")
        self.assertEqual(classify({"location_id": 6002, "system_id": 3002, "range": "1"})[0], "eligible")
        self.assertEqual(classify({"location_id": 6003, "system_id": 3003, "range": "1"})[0], "excluded")
        self.assertEqual(classify({"location_id": 6003, "system_id": 3003, "range": "2"})[0], "eligible")
        self.assertEqual(classify({"location_id": 6003, "system_id": 3003, "range": "region"})[0], "eligible")

    def test_remote_numeric_range_is_unknown_without_sde_graph(self):
        status, reason, distance = classify_buy_order_range(
            {"location_id": 6002, "system_id": 3002, "range": "5"},
            target_location_id=6001, target_system_id=3001, target_region_id=100,
            system_regions=None, jump_distances=None,
        )
        self.assertEqual(status, "unknown")
        self.assertEqual(reason, "numeric_range_requires_sde_map")
        self.assertIsNone(distance)

    def test_buy_order_sweep_applies_minimum_to_each_individual_fill(self):
        orders = [
            {"price": 12, "volume_remain": 700, "min_volume": 600, "order_id": 1},
            {"price": 11, "volume_remain": 500, "min_volume": 400, "order_id": 2},
            {"price": 10, "volume_remain": 200, "min_volume": 1, "order_id": 3},
        ]
        result = sweep_buy_orders(orders, 1000)
        self.assertEqual(result["filled_quantity"], 900)
        self.assertEqual(result["unfilled_quantity"], 100)
        self.assertEqual(result["gross_value_isk"], 10400)
        self.assertEqual(result["orders_skipped_because_fill_below_min_volume"], 1)
        self.assertTrue(result["minimum_volume_enforced"])
        self.assertFalse(result["fully_fillable_in_snapshot"])

    def test_buy_order_sweep_allows_final_remainder_below_min_volume(self):
        orders = [
            {"price": 12, "volume_remain": 50, "min_volume": 100, "order_id": 1},
            {"price": 11, "volume_remain": 100, "min_volume": 100, "order_id": 2},
            {"price": 10, "volume_remain": 50, "min_volume": 1, "order_id": 3},
        ]
        result = sweep_buy_orders(orders, 100)
        self.assertEqual(result["filled_quantity"], 100)
        self.assertEqual(result["unfilled_quantity"], 0)
        self.assertEqual(result["gross_value_isk"], 1100)
        self.assertEqual(result["orders_skipped_because_fill_below_min_volume"], 1)
        self.assertTrue(result["fully_fillable_in_snapshot"])

    def test_buy_order_sweep_rejects_below_minimum_partial_of_small_remaining_order(self):
        result = sweep_buy_orders(
            [{"price": 12, "volume_remain": 50, "min_volume": 100, "order_id": 1}],
            20,
        )
        self.assertEqual(result["filled_quantity"], 0)
        self.assertEqual(result["unfilled_quantity"], 20)
        self.assertEqual(result["orders_skipped_because_fill_below_min_volume"], 1)

    def test_missing_min_volume_uses_one_unit_default(self):
        result = sweep_buy_orders([{"price": 10, "volume_remain": 50, "order_id": 1}], 10)
        self.assertEqual(result["filled_quantity"], 10)
        self.assertEqual(result["orders_skipped_with_invalid_min_volume"], 0)

    def test_target_location_book_uses_eligible_remote_bids_and_local_asks(self):
        market_map = {
            "reverse_adjacency": {3001: {3002}, 3002: {3003}, 3003: set()},
            "system_regions": {3001: 100, 3002: 100, 3003: 100},
        }
        orders = [
            {"order_id": 1, "price": 10, "volume_remain": 1000,
             "is_buy_order": False, "location_id": 6001, "system_id": 3001},
            {"order_id": 2, "price": 12, "volume_remain": 500, "min_volume": 100,
             "is_buy_order": True, "range": "1", "location_id": 6002, "system_id": 3002},
            {"order_id": 3, "price": 15, "volume_remain": 500, "min_volume": 1,
             "is_buy_order": True, "range": "1", "location_id": 6003, "system_id": 3003},
        ]
        result = summarize_target_location_book(
            orders, [100], target_location_id=6001, target_system_id=3001,
            region_id=100, sde_market_map=market_map,
        )
        self.assertEqual(result["market_scope"], "target_location")
        self.assertEqual(result["best_bid"], 12)
        self.assertEqual(result["best_ask"], 10)
        self.assertTrue(result["is_crossed"])
        self.assertEqual(result["range_resolution"]["eligible_remote_buy_orders"], 1)
        self.assertEqual(result["range_resolution"]["excluded_out_of_range_buy_orders"], 1)
        self.assertEqual(result["sell_into_bids"][0]["vwap"], 12)
        self.assertEqual(result["buy_from_asks"][0]["vwap"], 10)
        self.assertIn("min_volume is applied to its individual", result["caveat"])
        self.assertNotIn("requested sell quantity", result["caveat"])

    def test_directory_builds_target_books_with_sde_ranges(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            sde = root / "sde"
            sde.mkdir()
            (sde / "mapSolarSystems.jsonl").write_text(
                "\n".join(json.dumps(item) for item in [
                    {"_key": 3001, "regionID": 100},
                    {"_key": 3002, "regionID": 100},
                    {"_key": 3003, "regionID": 100},
                ]) + "\n", encoding="utf-8"
            )
            (sde / "mapStargates.jsonl").write_text(
                "\n".join(json.dumps(item) for item in [
                    {"_key": 5001, "solarSystemID": 3002, "destination": {"solarSystemID": 3001}},
                    {"_key": 5002, "solarSystemID": 3003, "destination": {"solarSystemID": 3002}},
                ]) + "\n", encoding="utf-8"
            )
            orders = [
                {"order_id": 1, "type_id": 200, "price": 10, "volume_remain": 1000,
                 "is_buy_order": False, "location_id": 6001, "system_id": 3001},
                {"order_id": 2, "type_id": 200, "price": 12, "volume_remain": 500, "min_volume": 100,
                 "is_buy_order": True, "range": "1", "location_id": 6002, "system_id": 3002},
                {"order_id": 3, "type_id": 200, "price": 15, "volume_remain": 500, "min_volume": 1,
                 "is_buy_order": True, "range": "1", "location_id": 6003, "system_id": 3003},
            ]
            (root / "market-orders-region-100-type-200-page-1.json").write_text(json.dumps(orders), encoding="utf-8")
            result = summarize_directory(root, [100], sde_dir=sde)
        target = next(item for item in result[0]["location_books"] if item["location_id"] == 6001)
        self.assertEqual(target["order_book"]["best_bid"], 12)
        self.assertEqual(target["order_book"]["best_ask"], 10)
        self.assertEqual(target["order_book"]["range_resolution"]["eligible_remote_buy_orders"], 1)


if __name__ == "__main__":
    unittest.main()
