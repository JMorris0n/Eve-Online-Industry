"""Tests for the private candidate-stock reconciliation export."""
from __future__ import annotations

import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "profile"))

from export_asset_reconciliation import (  # noqa: E402
    AssetReconciliationError,
    build_reconciliation_rows,
    load_type_names,
    resolve_station_names,
    validate_candidate_lines,
    write_reconciliation_csv,
)


def sample_ledger():
    return {
        "schema_version": 1,
        "candidate_station_hangar_stock": [
            {
                "character_slot": 1,
                "root_location_type": "station",
                "root_location_id": 60000001,
                "type_id": 34,
                "quantity": 250,
                "record_count": 2,
                "state": "candidate_not_confirmed_usable",
            },
            {
                "character_slot": 1,
                "root_location_type": "station",
                "root_location_id": 60000001,
                "type_id": 35,
                "quantity": 500,
                "record_count": 1,
                "state": "candidate_not_confirmed_usable",
            },
        ],
    }


class AssetReconciliationTests(unittest.TestCase):
    def test_loads_direct_and_enveloped_sde_type_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "types.jsonl"
            path.write_text(
                '{"_key":34,"name":{"en":"Tritanium"}}\n'
                '{"_key":35,"_value":{"name":{"en":"Pyerite"}}}\n',
                encoding="utf-8",
            )
            self.assertEqual(
                load_type_names(path),
                {34: "Tritanium", 35: "Pyerite"},
            )

    def test_validates_only_conservative_station_candidates(self):
        rows = validate_candidate_lines(sample_ledger())
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["quantity"], 250)
        self.assertEqual(rows[1]["type_id"], 35)

    def test_rejects_unconfirmed_state_changes(self):
        ledger = sample_ledger()
        ledger["candidate_station_hangar_stock"][0]["state"] = "usable"
        with self.assertRaisesRegex(AssetReconciliationError, "candidate_not_confirmed_usable"):
            validate_candidate_lines(ledger)

    def test_rejects_non_station_candidate(self):
        ledger = sample_ledger()
        ledger["candidate_station_hangar_stock"][0]["root_location_type"] = "other"
        with self.assertRaisesRegex(AssetReconciliationError, "NPC station"):
            validate_candidate_lines(ledger)

    def test_rejects_invalid_quantity(self):
        ledger = sample_ledger()
        ledger["candidate_station_hangar_stock"][0]["quantity"] = 0
        with self.assertRaisesRegex(AssetReconciliationError, "quantity"):
            validate_candidate_lines(ledger)

    def test_station_names_resolve_once_per_distinct_station(self):
        calls = []

        def fake_open(request, timeout):
            calls.append(request.full_url)
            return io.BytesIO(
                json.dumps({
                    "name": "Example NPC Station",
                    "system_id": 30000001,
                    "type_id": 56,
                }).encode("utf-8")
            )

        names, failures = resolve_station_names(
            {60000001, 60000001}, opener=fake_open
        )
        self.assertEqual(names, {60000001: "Example NPC Station"})
        self.assertEqual(failures, set())
        self.assertEqual(len(calls), 1)
        self.assertIn("/60000001/", calls[0])

    def test_station_lookup_failure_is_nonfatal(self):
        def fake_open(request, timeout):
            raise OSError("offline")

        names, failures = resolve_station_names({60000001}, opener=fake_open)
        self.assertEqual(names, {})
        self.assertEqual(failures, {60000001})

    def test_writes_private_reconciliation_fields_and_blank_checks(self):
        candidates = validate_candidate_lines(sample_ledger())
        rows = build_reconciliation_rows(
            candidates,
            {34: "Tritanium", 35: "Pyerite"},
            {60000001: "Example NPC Station"},
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "local" / "stock.csv"
            write_reconciliation_csv(path, rows)
            with path.open("r", encoding="utf-8-sig", newline="") as stream:
                written = list(csv.DictReader(stream))
        self.assertEqual(len(written), 2)
        self.assertEqual(written[0]["station_name"], "Example NPC Station")
        self.assertEqual(written[0]["item_name"], "Tritanium")
        self.assertEqual(written[0]["candidate_quantity"], "250")
        self.assertEqual(written[0]["inventory_location_verified"], "")
        self.assertEqual(written[0]["inventory_quantity_verified"], "")
        self.assertEqual(written[0]["industry_input_eligible"], "")


if __name__ == "__main__":
    unittest.main()
