"""Tests for the safe-to-share aggregate asset-ledger report."""
from __future__ import annotations
import json
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "profile"))
from summarize_asset_ledger import AssetSummaryError, build_redacted_asset_summary  # noqa: E402


def sample_ledger():
    assets = [
        {"character_slot": 1, "character_id": 90000001, "item_id": 70001, "type_id": 34,
         "location_id": 60000001, "location_state": "resolved", "stock_candidate_state": "candidate_station_hangar",
         "is_blueprint_record": False, "is_blueprint_copy": False},
        {"character_slot": 1, "character_id": 90000001, "item_id": 70002, "type_id": 1001,
         "location_id": 60000001, "location_state": "resolved", "stock_candidate_state": "blueprint",
         "is_blueprint_record": True, "is_blueprint_copy": False},
        {"character_slot": 2, "character_id": 90000002, "item_id": 70003, "type_id": 35,
         "location_id": 99000001, "location_state": "unresolved_other_location", "stock_candidate_state": "unresolved_location",
         "is_blueprint_record": False, "is_blueprint_copy": False},
        {"character_slot": 3, "character_id": 90000003, "item_id": 70004, "type_id": 36,
         "location_id": 60000003, "location_state": "resolved", "stock_candidate_state": "stale_snapshot",
         "is_blueprint_record": False, "is_blueprint_copy": False},
    ]
    characters = [{
        "character_slot": slot,
        "character_id": 90000000 + slot,
        "snapshot_stale": False,
        "snapshot_age_hours": 1.25,
        "asset_record_count": sum(row["character_slot"] == slot for row in assets),
        "blueprint_asset_record_count": sum(
            row["character_slot"] == slot and (row["is_blueprint_record"] or row["is_blueprint_copy"])
            for row in assets
        ),
        "candidate_station_hangar_record_count": sum(
            row["character_slot"] == slot and row["stock_candidate_state"] == "candidate_station_hangar"
            for row in assets
        ),
    } for slot in (1, 2, 3)]
    return {
        "schema_version": 1, "generated_at": "2026-11-15T00:00:00Z",
        "characters": characters, "asset_records": assets,
        "candidate_station_hangar_stock": [{
            "character_slot": 1, "root_location_type": "station",
            "root_location_id": 60000001, "type_id": 34, "quantity": 250,
            "record_count": 1, "state": "candidate_not_confirmed_usable",
        }],
    }


class RedactedAssetSummaryTests(unittest.TestCase):
    def test_summarizes_without_identifiers_or_quantities(self):
        report = build_redacted_asset_summary(sample_ledger())
        self.assertEqual(report["totals"], {
            "character_count": 3, "asset_record_count": 4,
            "blueprint_asset_record_count": 1, "candidate_asset_record_count": 1,
            "candidate_stock_line_count": 1,
        })
        self.assertEqual(report["character_slots"][0]["stock_candidate_state_counts"], {
            "blueprint": 1, "candidate_station_hangar": 1,
        })
        serialized = json.dumps(report)
        for private_value in ("90000001", "70001", "60000001", "99000001", '"quantity"', "250"):
            self.assertNotIn(private_value, serialized)
        self.assertFalse(report["privacy"]["contains_item_ids"])
        self.assertFalse(report["policy"]["candidate_stock_is_confirmed_usable"])

    def test_detects_count_mismatch(self):
        ledger = sample_ledger()
        ledger["characters"][0]["asset_record_count"] = 99
        with self.assertRaisesRegex(AssetSummaryError, "counts do not match"):
            build_redacted_asset_summary(ledger)

    def test_rejects_unknown_state(self):
        ledger = sample_ledger()
        ledger["asset_records"][0]["location_state"] = "secret-location"
        with self.assertRaisesRegex(AssetSummaryError, "unrecognized location"):
            build_redacted_asset_summary(ledger)

    def test_requires_all_three_slots(self):
        ledger = sample_ledger()
        ledger["characters"] = ledger["characters"][:2]
        with self.assertRaisesRegex(AssetSummaryError, "all three"):
            build_redacted_asset_summary(ledger)


if __name__ == "__main__":
    unittest.main()
