"""Tests for the local, conservative ESI personal asset ledger."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "profile"))

from build_asset_ledger import (  # noqa: E402
    AssetLedgerError,
    aggregate_candidate_stock,
    normalize_character_assets,
    resolve_locations,
    validate_assets,
)


def asset(item_id, type_id, location_id, location_type, flag="Hangar",
          quantity=1, singleton=False, blueprint_copy=False):
    row = {
        "item_id": item_id, "type_id": type_id, "location_id": location_id,
        "location_type": location_type, "location_flag": flag,
        "quantity": quantity, "is_singleton": singleton,
    }
    if blueprint_copy:
        row["is_blueprint_copy"] = True
    return row


class AssetValidationTests(unittest.TestCase):
    def test_validates_asset_rows(self):
        rows = validate_assets([asset(1001, 34, 60000001, "station", quantity=250)])
        self.assertEqual(rows[0]["quantity"], 250)
        self.assertFalse(rows[0]["is_blueprint_copy"])

    def test_rejects_duplicate_item_ids(self):
        with self.assertRaisesRegex(AssetLedgerError, "Duplicate asset item_id"):
            validate_assets([
                asset(1001, 34, 60000001, "station"),
                asset(1001, 35, 60000001, "station"),
            ])

    def test_rejects_invalid_singleton_and_quantity(self):
        bad = asset(1001, 34, 60000001, "station")
        bad["is_singleton"] = "false"
        with self.assertRaisesRegex(AssetLedgerError, "is_singleton"):
            validate_assets([bad])
        bad = asset(1002, 34, 60000001, "station", quantity=0)
        with self.assertRaisesRegex(AssetLedgerError, "quantity"):
            validate_assets([bad])


class AssetLocationTests(unittest.TestCase):
    def test_resolves_nested_container_to_station(self):
        rows = validate_assets([
            asset(1001, 3293, 60000001, "station", singleton=True),
            asset(1002, 34, 1001, "item", quantity=250),
        ])
        child = resolve_locations(rows)[1002]
        self.assertEqual(child["location_state"], "resolved")
        self.assertEqual(child["root_location_id"], 60000001)
        self.assertEqual(child["root_location_type"], "station")
        self.assertEqual(child["parent_item_path"], [1001])
        self.assertEqual(child["ancestor_flags"], ["Hangar"])

    def test_ship_cargo_is_not_standard_hangar_stock(self):
        rows = validate_assets([
            asset(1001, 587, 60000001, "station", singleton=True),
            asset(1002, 34, 1001, "item", flag="Cargo", quantity=500),
        ])
        records, _ = normalize_character_assets(
            rows, [], slot=1, character_id=77,
            snapshot_retrieved_at="2026-11-15T00:00:00Z",
            asset_sha256=None, blueprint_sha256=None, snapshot_stale=False,
        )
        self.assertEqual(records[1]["stock_candidate_state"], "non_standard_hangar_location")

    def test_missing_parent_is_unresolved(self):
        rows = validate_assets([asset(1002, 34, 9999, "item")])
        self.assertEqual(resolve_locations(rows)[1002]["location_state"], "unresolved_parent")

    def test_asset_safety_is_not_candidate_stock(self):
        rows = validate_assets([asset(1002, 34, 2004, "other")])
        result = resolve_locations(rows)[1002]
        self.assertEqual(result["location_state"], "asset_safety")
        records, _ = normalize_character_assets(
            rows, [], slot=1, character_id=77,
            snapshot_retrieved_at="2026-11-15T00:00:00Z",
            asset_sha256=None, blueprint_sha256=None, snapshot_stale=False,
        )
        self.assertEqual(records[0]["stock_candidate_state"], "unresolved_location")

    def test_other_locations_remain_unknown(self):
        rows = validate_assets([asset(1002, 34, 99000001, "other")])
        result = resolve_locations(rows)[1002]
        self.assertEqual(result["location_state"], "unresolved_other_location")
        self.assertEqual(result["root_location_id"], 99000001)

    def test_parent_cycle_is_detected(self):
        rows = validate_assets([
            asset(1001, 3293, 1002, "item"),
            asset(1002, 3293, 1001, "item"),
        ])
        locations = resolve_locations(rows)
        self.assertEqual(locations[1001]["location_state"], "parent_cycle")
        self.assertEqual(locations[1002]["location_state"], "parent_cycle")


class AssetStockTests(unittest.TestCase):
    def test_only_station_hangar_stacks_become_candidates(self):
        rows = [
            asset(1001, 34, 60000001, "station", quantity=250),
            asset(1002, 35, 60000001, "station", quantity=500),
            asset(1003, 587, 60000001, "station", singleton=True),
        ]
        records, summary = normalize_character_assets(
            rows, [{"item_id": 1002}], slot=2, character_id=88,
            snapshot_retrieved_at="2026-11-15T00:00:00Z",
            asset_sha256="a" * 64, blueprint_sha256="b" * 64,
            snapshot_stale=False,
        )
        self.assertEqual(records[0]["stock_candidate_state"], "candidate_station_hangar")
        self.assertEqual(records[1]["stock_candidate_state"], "blueprint")
        self.assertEqual(records[2]["stock_candidate_state"], "singleton_asset")
        self.assertEqual(summary["candidate_station_hangar_record_count"], 1)
        self.assertEqual(aggregate_candidate_stock(records), [{
            "character_slot": 2, "root_location_type": "station",
            "root_location_id": 60000001, "type_id": 34,
            "quantity": 250, "record_count": 1,
            "state": "candidate_not_confirmed_usable",
        }])

    def test_stale_snapshot_never_becomes_candidate_stock(self):
        rows = [asset(1001, 34, 60000001, "station", quantity=250)]
        records, summary = normalize_character_assets(
            rows, [], slot=1, character_id=77,
            snapshot_retrieved_at="2026-11-14T00:00:00Z",
            asset_sha256=None, blueprint_sha256=None, snapshot_stale=True,
        )
        self.assertEqual(records[0]["stock_candidate_state"], "stale_snapshot")
        self.assertEqual(summary["candidate_station_hangar_record_count"], 0)

    def test_blueprint_copy_flag_excludes_item(self):
        rows = [asset(1001, 34, 60000001, "station", blueprint_copy=True)]
        records, _ = normalize_character_assets(
            rows, [], slot=1, character_id=77,
            snapshot_retrieved_at="2026-11-15T00:00:00Z",
            asset_sha256=None, blueprint_sha256=None, snapshot_stale=False,
        )
        self.assertEqual(records[0]["stock_candidate_state"], "blueprint")

    def test_aggregates_same_type_at_same_location(self):
        rows = [
            asset(1001, 34, 60000001, "station", quantity=100),
            asset(1002, 34, 60000001, "station", quantity=150),
        ]
        records, _ = normalize_character_assets(
            rows, [], slot=1, character_id=77,
            snapshot_retrieved_at="2026-11-15T00:00:00Z",
            asset_sha256=None, blueprint_sha256=None, snapshot_stale=False,
        )
        stock = aggregate_candidate_stock(records)
        self.assertEqual(stock[0]["quantity"], 250)
        self.assertEqual(stock[0]["record_count"], 2)


if __name__ == "__main__":
    unittest.main()
