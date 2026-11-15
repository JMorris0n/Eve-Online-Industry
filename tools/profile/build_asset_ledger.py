#!/usr/bin/env python3
"""Build a private, location-aware ledger from personal ESI asset snapshots.

This is a conservative inventory screen, not proof that an item is available
to a particular Industry job or facility. The command is offline.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from import_esi_profile import (
    DEFAULT_IMPORT_MANIFEST,
    DEFAULT_REGISTRY,
    DEFAULT_SNAPSHOT_ROOT,
    ProfileImportError,
    assign_slots,
    load_latest_snapshot,
    positive_id,
    previous_slot_assignments,
    read_authorized_characters,
    write_json_atomic,
)

DEFAULT_OUTPUT = Path("data/private/esi/asset-ledger.json")
ASSET_SAFETY_LOCATION_ID = 2004


class AssetLedgerError(RuntimeError):
    """Raised when ESI asset data cannot safely produce a ledger."""


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def validate_assets(rows: Any) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        raise AssetLedgerError("The ESI assets response must be a JSON array.")
    normalized: list[dict[str, Any]] = []
    seen: set[int] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise AssetLedgerError(f"Asset record {index} is not an object.")
        item_id = positive_id(row.get("item_id"), f"Asset record {index} item_id")
        type_id = positive_id(row.get("type_id"), f"Asset record {index} type_id")
        location_id = positive_id(row.get("location_id"), f"Asset record {index} location_id")
        quantity = row.get("quantity")
        singleton = row.get("is_singleton")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
            raise AssetLedgerError(f"Asset record {index} has an invalid quantity.")
        if not isinstance(singleton, bool):
            raise AssetLedgerError(f"Asset record {index} has an invalid is_singleton flag.")
        location_flag = row.get("location_flag")
        location_type = row.get("location_type")
        if not isinstance(location_flag, str) or not location_flag:
            raise AssetLedgerError(f"Asset record {index} has an invalid location_flag.")
        if not isinstance(location_type, str) or not location_type:
            raise AssetLedgerError(f"Asset record {index} has an invalid location_type.")
        copy_flag = row.get("is_blueprint_copy")
        if copy_flag is not None and not isinstance(copy_flag, bool):
            raise AssetLedgerError(f"Asset record {index} has an invalid is_blueprint_copy flag.")
        if item_id in seen:
            raise AssetLedgerError(f"Duplicate asset item_id {item_id} in one character snapshot.")
        seen.add(item_id)
        normalized.append({
            "item_id": item_id,
            "type_id": type_id,
            "location_id": location_id,
            "location_type": location_type,
            "location_flag": location_flag,
            "quantity": quantity,
            "is_singleton": singleton,
            "is_blueprint_copy": copy_flag is True,
        })
    return normalized


def blueprint_item_ids(rows: Any) -> set[int]:
    if not isinstance(rows, list):
        raise AssetLedgerError("The ESI blueprints response must be a JSON array.")
    result: set[int] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise AssetLedgerError(f"Blueprint record {index} is not an object.")
        result.add(positive_id(row.get("item_id"), f"Blueprint record {index} item_id"))
    return result


def resolve_locations(assets: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    """Resolve item-parent chains without guessing unresolved ESI location types."""
    by_id = {row["item_id"]: row for row in assets}
    memo: dict[int, dict[str, Any]] = {}
    visiting: set[int] = set()

    def resolve(item_id: int) -> dict[str, Any]:
        if item_id in memo:
            return memo[item_id]
        if item_id in visiting:
            return {
                "location_state": "parent_cycle",
                "root_location_id": None,
                "root_location_type": None,
                "root_location_flag": None,
                "parent_item_path": [],
                "ancestor_flags": [],
            }
        row = by_id[item_id]
        visiting.add(item_id)
        location_type = row["location_type"]
        location_id = row["location_id"]

        if location_type == "item":
            parent = by_id.get(location_id)
            if parent is None:
                result = {
                    "location_state": "unresolved_parent",
                    "root_location_id": None,
                    "root_location_type": None,
                    "root_location_flag": None,
                    "parent_item_path": [location_id],
                    "ancestor_flags": [],
                }
            else:
                parent_result = resolve(location_id)
                result = {
                    **parent_result,
                    "parent_item_path": [location_id] + parent_result["parent_item_path"],
                    "ancestor_flags": [parent["location_flag"]] + parent_result["ancestor_flags"],
                }
        elif location_type in {"station", "solar_system"}:
            result = {
                "location_state": "resolved",
                "root_location_id": location_id,
                "root_location_type": location_type,
                "root_location_flag": row["location_flag"],
                "parent_item_path": [],
                "ancestor_flags": [],
            }
        elif location_type == "other" and location_id == ASSET_SAFETY_LOCATION_ID:
            result = {
                "location_state": "asset_safety",
                "root_location_id": location_id,
                "root_location_type": "asset_safety",
                "root_location_flag": row["location_flag"],
                "parent_item_path": [],
                "ancestor_flags": [],
            }
        elif location_type == "other":
            result = {
                "location_state": "unresolved_other_location",
                "root_location_id": location_id,
                "root_location_type": "other",
                "root_location_flag": row["location_flag"],
                "parent_item_path": [],
                "ancestor_flags": [],
            }
        else:
            result = {
                "location_state": "unsupported_location_type",
                "root_location_id": location_id,
                "root_location_type": location_type,
                "root_location_flag": row["location_flag"],
                "parent_item_path": [],
                "ancestor_flags": [],
            }

        visiting.remove(item_id)
        memo[item_id] = result
        return result

    for row in assets:
        resolve(row["item_id"])
    return memo


def stock_candidate_state(
    asset: dict[str, Any],
    location: dict[str, Any],
    *,
    is_blueprint: bool,
    snapshot_stale: bool,
) -> str:
    if snapshot_stale:
        return "stale_snapshot"
    if is_blueprint or asset["is_blueprint_copy"]:
        return "blueprint"
    if asset["is_singleton"]:
        return "singleton_asset"
    if location["location_state"] != "resolved":
        return "unresolved_location"
    if location["root_location_type"] != "station":
        return "not_station_root"
    # Restrict the initial stock candidate set to standard Hangar paths.
    # Cargo, deliveries, corporation divisions, and specialized holds stay out.
    flags = [asset["location_flag"], *location["ancestor_flags"]]
    if any(flag != "Hangar" for flag in flags):
        return "non_standard_hangar_location"
    return "candidate_station_hangar"


def normalize_character_assets(
    assets_payload: Any,
    blueprints_payload: Any,
    *,
    slot: int,
    character_id: int,
    snapshot_retrieved_at: str,
    asset_sha256: str | None,
    blueprint_sha256: str | None,
    snapshot_stale: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    assets = validate_assets(assets_payload)
    blueprint_ids = blueprint_item_ids(blueprints_payload)
    locations = resolve_locations(assets)
    records: list[dict[str, Any]] = []
    state_counts: Counter[str] = Counter()
    candidate_count = 0

    for asset in assets:
        location = locations[asset["item_id"]]
        is_blueprint = asset["item_id"] in blueprint_ids
        candidate_state = stock_candidate_state(
            asset, location, is_blueprint=is_blueprint, snapshot_stale=snapshot_stale
        )
        state_counts[location["location_state"]] += 1
        candidate_count += candidate_state == "candidate_station_hangar"
        records.append({
            "character_slot": slot,
            "character_id": character_id,
            **asset,
            "is_blueprint_record": is_blueprint,
            **location,
            "stock_candidate_state": candidate_state,
            "snapshot_retrieved_at": snapshot_retrieved_at,
        })

    summary = {
        "character_slot": slot,
        "character_id": character_id,
        "snapshot_retrieved_at": snapshot_retrieved_at,
        "snapshot_stale": snapshot_stale,
        "asset_record_count": len(records),
        "blueprint_asset_record_count": sum(
            1 for row in records if row["is_blueprint_record"] or row["is_blueprint_copy"]
        ),
        "candidate_station_hangar_record_count": candidate_count,
        "location_state_counts": dict(sorted(state_counts.items())),
        "asset_snapshot_sha256": asset_sha256,
        "blueprint_snapshot_sha256": blueprint_sha256,
    }
    return records, summary


def aggregate_candidate_stock(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[int, int, int], dict[str, int]] = defaultdict(
        lambda: {"quantity": 0, "record_count": 0}
    )
    for row in records:
        if row["stock_candidate_state"] != "candidate_station_hangar":
            continue
        key = (row["character_slot"], row["root_location_id"], row["type_id"])
        groups[key]["quantity"] += row["quantity"]
        groups[key]["record_count"] += 1

    result = []
    for (slot, location_id, type_id), values in sorted(groups.items()):
        result.append({
            "character_slot": slot,
            "root_location_type": "station",
            "root_location_id": location_id,
            "type_id": type_id,
            "quantity": values["quantity"],
            "record_count": values["record_count"],
            "state": "candidate_not_confirmed_usable",
        })
    return result


def build_asset_ledger(
    registry_path: Path,
    snapshot_root: Path,
    import_manifest_path: Path,
    max_snapshot_age_hours: float = 24.0,
) -> dict[str, Any]:
    if max_snapshot_age_hours <= 0:
        raise AssetLedgerError("--max-snapshot-age-hours must be greater than zero.")
    registry = read_authorized_characters(registry_path)
    slot_assignments = previous_slot_assignments(import_manifest_path)
    slotted = assign_slots(registry, slot_assignments)

    all_records: list[dict[str, Any]] = []
    character_summaries = []
    for character in slotted:
        try:
            snapshot = load_latest_snapshot(character, snapshot_root, max_snapshot_age_hours)
        except ProfileImportError as exc:
            raise AssetLedgerError(str(exc)) from exc
        manifest = snapshot["manifest"]
        metadata = manifest["files"]
        records, summary = normalize_character_assets(
            snapshot["payloads"]["assets"],
            snapshot["payloads"]["blueprints"],
            slot=character["slot"],
            character_id=character["character_id"],
            snapshot_retrieved_at=manifest["retrieved_at"],
            asset_sha256=metadata["assets"].get("sha256"),
            blueprint_sha256=metadata["blueprints"].get("sha256"),
            snapshot_stale=snapshot["stale"],
        )
        summary["snapshot_age_hours"] = round(snapshot["age_hours"], 2)
        character_summaries.append(summary)
        all_records.extend(records)

    return {
        "schema_version": 1,
        "generated_at": utc_iso(),
        "source": "Git-ignored local ESI personal asset and blueprint snapshots",
        "policy": {
            "candidate_stock_rule": (
                "Only non-singleton, non-blueprint stacks whose full location chain "
                "resolves to a station and uses Hangar flags at every level are "
                "summarized as candidate stock."
            ),
            "candidate_stock_caveat": (
                "Candidate stock is not proof of access to an Industry service, "
                "availability to a particular job, or current usable quantity. "
                "Check the target character, facility, inventory division, and job UI."
            ),
            "unresolved_locations": (
                "Non-item 'other' locations, missing parents, parent cycles, and "
                "unsupported location types are retained but excluded from candidate stock."
            ),
            "blueprint_deduplication": (
                "Items returned by the personal blueprint endpoint, and assets flagged "
                "as blueprint copies, are excluded from candidate material stock."
            ),
            "ownership_scope": (
                "Personal assets for the three authorized characters only. Corporation "
                "assets and shared hangars are not imported by this tool."
            ),
        },
        "characters": character_summaries,
        "asset_records": all_records,
        "candidate_station_hangar_stock": aggregate_candidate_stock(all_records),
        "privacy": {
            "contains_character_ids": True,
            "contains_item_ids": True,
            "contains_type_ids": True,
            "contains_location_ids": True,
            "contains_isk_amounts": False,
            "must_remain_local": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--snapshot-root", type=Path, default=DEFAULT_SNAPSHOT_ROOT)
    parser.add_argument("--import-manifest", type=Path, default=DEFAULT_IMPORT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-snapshot-age-hours", type=float, default=24.0)
    args = parser.parse_args()

    try:
        report = build_asset_ledger(
            args.registry, args.snapshot_root, args.import_manifest,
            args.max_snapshot_age_hours,
        )
        write_json_atomic(args.output, report)
    except (AssetLedgerError, ProfileImportError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        "PASS: wrote private asset ledger for "
        f"{len(report['characters'])} character(s), "
        f"{sum(item['asset_record_count'] for item in report['characters'])} asset record(s), "
        f"{len(report['candidate_station_hangar_stock'])} candidate stock line(s) "
        f"to {args.output}"
    )
    print("Keep the ledger under data/private/; do not upload it or commit it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
