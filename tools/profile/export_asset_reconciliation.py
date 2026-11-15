#!/usr/bin/env python3
"""Export conservative personal asset candidates to a private reconciliation CSV.

The CSV includes item/location identifiers and quantities. Keep it local and
never commit or upload it.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Callable
from urllib.error import URLError
from urllib.request import Request, urlopen

DEFAULT_LEDGER = Path("data/private/esi/asset-ledger.json")
DEFAULT_SDE_DIR = Path("data/raw/sde/3698585/extracted")
DEFAULT_OUTPUT = Path("local/asset-stock-reconciliation.csv")
ESI_STATION_URL = "https://esi.evetech.net/latest/universe/stations/{station_id}/?datasource=tranquility"
CSV_FIELDS = (
    "character_slot",
    "station_name",
    "station_name_state",
    "station_id",
    "item_name",
    "type_id",
    "candidate_quantity",
    "source_asset_record_count",
    "inventory_location_verified",
    "inventory_quantity_verified",
    "industry_input_eligible",
    "notes",
)


class AssetReconciliationError(RuntimeError):
    """Raised when a private asset ledger or SDE type table is invalid."""


def iter_jsonl(path: Path):
    """Yield SDE JSONL objects, accepting the generic _key/_value envelope."""
    with path.open("r", encoding="utf-8-sig") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise AssetReconciliationError(
                    f"{path}:{line_number}: invalid JSON: {exc}"
                ) from exc
            if not isinstance(record, dict):
                raise AssetReconciliationError(
                    f"{path}:{line_number}: expected a JSON object."
                )
            if isinstance(record.get("_value"), dict):
                value = dict(record["_value"])
                value.setdefault("_key", record.get("_key"))
                record = value
            yield record


def load_type_names(types_path: Path) -> dict[int, str]:
    """Load English item names from the current CCP SDE types.jsonl table."""
    if not types_path.is_file():
        raise FileNotFoundError(f"Missing SDE type table: {types_path}")
    names: dict[int, str] = {}
    for record in iter_jsonl(types_path):
        type_id = record.get("_key")
        if isinstance(type_id, bool) or not isinstance(type_id, int) or type_id <= 0:
            continue
        raw_name = record.get("name")
        name = raw_name.get("en") if isinstance(raw_name, dict) else None
        if isinstance(name, str) and name.strip():
            names[type_id] = name.strip()
    if not names:
        raise AssetReconciliationError(
            f"No English type names were loaded from {types_path}."
        )
    return names


def load_ledger(path: Path) -> dict[str, Any]:
    try:
        ledger = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AssetReconciliationError(f"Invalid asset-ledger JSON: {exc}") from exc
    if not isinstance(ledger, dict) or ledger.get("schema_version") != 1:
        raise AssetReconciliationError("Unsupported or malformed asset ledger.")
    if not isinstance(ledger.get("candidate_station_hangar_stock"), list):
        raise AssetReconciliationError("Ledger candidate stock must be an array.")
    return ledger


def _positive_int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise AssetReconciliationError(f"Candidate {field} must be a positive integer.")
    return value


def validate_candidate_lines(ledger: dict[str, Any]) -> list[dict[str, int]]:
    """Validate that every exported row is still a conservative station-hangar candidate."""
    candidates = ledger["candidate_station_hangar_stock"]
    validated: list[dict[str, int]] = []
    for index, row in enumerate(candidates, start=1):
        if not isinstance(row, dict):
            raise AssetReconciliationError(f"Candidate row {index} is malformed.")
        slot = row.get("character_slot")
        if isinstance(slot, bool) or not isinstance(slot, int) or slot not in (1, 2, 3):
            raise AssetReconciliationError(f"Candidate row {index} has an invalid character slot.")
        if row.get("state") != "candidate_not_confirmed_usable":
            raise AssetReconciliationError(
                f"Candidate row {index} is not labeled candidate_not_confirmed_usable."
            )
        if row.get("root_location_type") != "station":
            raise AssetReconciliationError(
                f"Candidate row {index} does not resolve to an NPC station."
            )
        validated.append({
            "character_slot": slot,
            "station_id": _positive_int(row.get("root_location_id"), "station ID"),
            "type_id": _positive_int(row.get("type_id"), "type ID"),
            "quantity": _positive_int(row.get("quantity"), "quantity"),
            "record_count": _positive_int(row.get("record_count"), "record count"),
        })
    return sorted(
        validated,
        key=lambda row: (row["character_slot"], row["station_id"], row["type_id"]),
    )


def resolve_station_names(
    station_ids: set[int],
    *,
    timeout: float = 10.0,
    opener: Callable[..., Any] | None = None,
) -> tuple[dict[int, str], set[int]]:
    """Resolve known NPC station IDs through public ESI, without character authentication."""
    open_url = opener or urlopen
    names: dict[int, str] = {}
    failures: set[int] = set()
    for station_id in sorted(station_ids):
        request = Request(
            ESI_STATION_URL.format(station_id=station_id),
            headers={
                "Accept": "application/json",
                "User-Agent": "Eve-Online-Industry local asset reconciliation",
            },
        )
        try:
            with open_url(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            name = payload.get("name") if isinstance(payload, dict) else None
            if not isinstance(name, str) or not name.strip():
                failures.add(station_id)
                continue
            names[station_id] = name.strip()
        except (OSError, URLError, TimeoutError, UnicodeDecodeError, json.JSONDecodeError):
            failures.add(station_id)
    return names, failures


def build_reconciliation_rows(
    candidates: list[dict[str, int]],
    type_names: dict[int, str],
    station_names: dict[int, str],
) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for candidate in candidates:
        station_id = candidate["station_id"]
        type_id = candidate["type_id"]
        station_name = station_names.get(station_id)
        rows.append({
            "character_slot": candidate["character_slot"],
            "station_name": station_name or f"Station ID {station_id}",
            "station_name_state": "resolved" if station_name else "unresolved_or_skipped",
            "station_id": station_id,
            "item_name": type_names.get(type_id, f"Type ID {type_id}"),
            "type_id": type_id,
            "candidate_quantity": candidate["quantity"],
            "source_asset_record_count": candidate["record_count"],
            "inventory_location_verified": "",
            "inventory_quantity_verified": "",
            "industry_input_eligible": "",
            "notes": "",
        })
    return rows


def write_reconciliation_csv(path: Path, rows: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--sde-dir", type=Path, default=DEFAULT_SDE_DIR,
                        help="Extracted SDE directory containing types.jsonl.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--no-station-name-lookup", action="store_true",
                        help="Skip public ESI station-name lookups and keep numeric station IDs.")
    parser.add_argument("--esi-timeout", type=float, default=10.0)
    args = parser.parse_args()

    try:
        ledger = load_ledger(args.ledger)
        candidates = validate_candidate_lines(ledger)
        type_names = load_type_names(args.sde_dir / "types.jsonl")
        station_ids = {row["station_id"] for row in candidates}
        station_names: dict[int, str] = {}
        failures: set[int] = set()
        if not args.no_station_name_lookup and station_ids:
            station_names, failures = resolve_station_names(
                station_ids, timeout=args.esi_timeout
            )
        rows = build_reconciliation_rows(candidates, type_names, station_names)
        write_reconciliation_csv(args.output, rows)
    except (AssetReconciliationError, OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    resolved_types = sum(
        1 for row in rows if not str(row["item_name"]).startswith("Type ID ")
    )
    resolved_stations = len(station_names)
    print(
        f"PASS: wrote private reconciliation CSV for {len(rows)} candidate stock line(s), "
        f"{len(station_ids)} station(s), {resolved_types}/{len(rows)} item names, "
        f"{resolved_stations}/{len(station_ids)} station names to {args.output}"
    )
    if failures:
        print(
            f"WARNING: {len(failures)} station name lookup(s) failed; "
            "the CSV retains their numeric station IDs.",
            file=sys.stderr,
        )
    print("The CSV contains private locations, type IDs, and quantities. Keep it local.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
