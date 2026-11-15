#!/usr/bin/env python3
"""Write a redacted, identifier-free summary of a private personal asset ledger."""
from __future__ import annotations
import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

DEFAULT_LEDGER = Path("data/private/esi/asset-ledger.json")
DEFAULT_OUTPUT = Path("local/asset-ledger-readiness.json")
LOCATION_STATES = {"resolved", "asset_safety", "unresolved_parent",
                   "unresolved_other_location", "parent_cycle", "unsupported_location_type"}
STOCK_STATES = {"candidate_station_hangar", "blueprint", "singleton_asset",
                "unresolved_location", "not_station_root",
                "non_standard_hangar_location", "stale_snapshot"}


class AssetSummaryError(RuntimeError):
    """Raised when an asset ledger cannot safely be summarized."""


def _count(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise AssetSummaryError(f"{field} must be a non-negative integer.")
    return value


def build_redacted_asset_summary(ledger: dict[str, Any]) -> dict[str, Any]:
    """Return aggregate counts only; never copy names, identifiers, or quantities."""
    if not isinstance(ledger, dict) or ledger.get("schema_version") != 1:
        raise AssetSummaryError("Unsupported or malformed asset ledger.")
    assets = ledger.get("asset_records")
    candidates = ledger.get("candidate_station_hangar_stock")
    characters = ledger.get("characters")
    if not isinstance(assets, list) or not isinstance(candidates, list) or not isinstance(characters, list):
        raise AssetSummaryError("Ledger asset, candidate, and character collections must be arrays.")

    assets_by_slot: Counter[int] = Counter()
    blueprints_by_slot: Counter[int] = Counter()
    candidates_by_slot: Counter[int] = Counter()
    locations: dict[int, Counter[str]] = {}
    stock_states: dict[int, Counter[str]] = {}
    for row in assets:
        if not isinstance(row, dict):
            raise AssetSummaryError("Malformed asset row.")
        slot = row.get("character_slot")
        if isinstance(slot, bool) or not isinstance(slot, int) or slot not in (1, 2, 3):
            raise AssetSummaryError("Asset row has invalid character slot.")
        location = row.get("location_state")
        stock = row.get("stock_candidate_state")
        if location not in LOCATION_STATES:
            raise AssetSummaryError("Asset row has unrecognized location state.")
        if stock not in STOCK_STATES:
            raise AssetSummaryError("Asset row has unrecognized stock state.")
        assets_by_slot[slot] += 1
        locations.setdefault(slot, Counter())[location] += 1
        stock_states.setdefault(slot, Counter())[stock] += 1
        if row.get("is_blueprint_record") is True or row.get("is_blueprint_copy") is True:
            blueprints_by_slot[slot] += 1
        if stock == "candidate_station_hangar":
            candidates_by_slot[slot] += 1

    output_slots = []
    seen: set[int] = set()
    for row in characters:
        if not isinstance(row, dict):
            raise AssetSummaryError("Malformed character summary.")
        slot = row.get("character_slot")
        if isinstance(slot, bool) or not isinstance(slot, int) or slot not in (1, 2, 3) or slot in seen:
            raise AssetSummaryError("Invalid or duplicate character slot in summary.")
        seen.add(slot)
        stale = row.get("snapshot_stale")
        age = row.get("snapshot_age_hours")
        if not isinstance(stale, bool) or isinstance(age, bool) or not isinstance(age, (int, float)) or age < 0:
            raise AssetSummaryError("Character snapshot freshness metadata is invalid.")
        count = _count(row.get("asset_record_count"), "asset_record_count")
        bp_count = _count(row.get("blueprint_asset_record_count"), "blueprint_asset_record_count")
        candidate_count = _count(row.get("candidate_station_hangar_record_count"), "candidate_station_hangar_record_count")
        if count != assets_by_slot[slot] or bp_count != blueprints_by_slot[slot] or candidate_count != candidates_by_slot[slot]:
            raise AssetSummaryError("Character asset counts do not match underlying records.")
        output_slots.append({
            "slot": slot,
            "snapshot_stale": stale,
            "snapshot_age_hours": round(float(age), 2),
            "asset_record_count": count,
            "blueprint_asset_record_count": bp_count,
            "candidate_asset_record_count": candidate_count,
            "candidate_stock_line_count": sum(
                1 for item in candidates
                if isinstance(item, dict) and item.get("character_slot") == slot
            ),
            "location_state_counts": {
                key: locations.get(slot, Counter()).get(key, 0)
                for key in sorted(LOCATION_STATES)
            },
            "stock_candidate_state_counts": {
                key: value for key, value in sorted(stock_states.get(slot, Counter()).items())
            },
        })
    if seen != {1, 2, 3}:
        raise AssetSummaryError("Ledger must contain all three character slots.")
    valid_lines = sum(
        1 for row in candidates
        if isinstance(row, dict)
        and row.get("state") == "candidate_not_confirmed_usable"
        and isinstance(row.get("character_slot"), int)
        and not isinstance(row.get("character_slot"), bool)
        and row.get("character_slot") in (1, 2, 3)
    )
    if valid_lines != len(candidates):
        raise AssetSummaryError("Candidate stock lines are malformed or not conservatively labeled.")

    return {
        "report_version": 1,
        "source_ledger_schema_version": 1,
        "generated_at": ledger.get("generated_at") if isinstance(ledger.get("generated_at"), str) else None,
        "character_slots": sorted(output_slots, key=lambda row: row["slot"]),
        "totals": {
            "character_count": 3,
            "asset_record_count": len(assets),
            "blueprint_asset_record_count": sum(blueprints_by_slot.values()),
            "candidate_asset_record_count": sum(candidates_by_slot.values()),
            "candidate_stock_line_count": len(candidates),
        },
        "policy": {
            "candidate_stock_is_confirmed_usable": False,
            "ownership_scope": "Personal character assets only; corporation and shared assets are excluded.",
            "identifiers_and_item_details_omitted": True,
            "quantities_and_isk_values_omitted": True,
        },
        "privacy": {
            "contains_character_names_or_ids": False,
            "contains_item_ids": False,
            "contains_type_ids": False,
            "contains_location_ids_or_names": False,
            "contains_asset_quantities": False,
            "contains_isk_amounts": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
        report = build_redacted_asset_summary(ledger)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (OSError, json.JSONDecodeError, AssetSummaryError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        "PASS: wrote redacted asset summary for "
        f"{report['totals']['character_count']} character(s), "
        f"{report['totals']['asset_record_count']} asset record(s), "
        f"{report['totals']['candidate_stock_line_count']} candidate stock line(s) "
        f"to {args.output}"
    )
    print("The summary omits character, item, type, location, and quantity values.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
