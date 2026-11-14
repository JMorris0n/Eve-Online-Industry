#!/usr/bin/env python3
"""Summarize local profile completeness without exposing private values."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from validate_profile import validate_profile_data

CAPACITY_POOLS = ("manufacturing", "science", "reaction")
CAPITAL_FIELDS = (
    "working_capital_isk",
    "liquidity_reserve_isk",
    "max_capital_at_risk_isk",
)
OPERATION_FIELDS = (
    "active_hours_per_week",
    "max_setup_minutes_per_batch",
    "target_liquidation_days",
)


def _state(value: Any) -> str:
    return value if isinstance(value, str) and value in {"unknown", "partial", "verified"} else "not_entered"


def _capacity_state(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return "invalid"
    return "available" if value > 0 else "none"


def build_readiness_report(profile: dict[str, Any]) -> dict[str, Any]:
    """Return a low-disclosure readiness summary; never return account values."""
    errors = validate_profile_data(profile)
    characters = profile.get("characters", [])
    if not isinstance(characters, list):
        characters = []

    character_rows = []
    unfilled: list[str] = []
    for index, character in enumerate(characters):
        if not isinstance(character, dict):
            character = {}
        slot = character.get("slot")
        if not isinstance(slot, int) or isinstance(slot, bool) or slot not in (1, 2, 3):
            slot = index + 1
        skills = character.get("skills", {})
        if not isinstance(skills, dict):
            skills = {}
        skills_state = _state(character.get("skills_state"))
        capacities = character.get("job_capacity", {})
        if not isinstance(capacities, dict):
            capacities = {}
        capacity_summary = {
            pool: _capacity_state(capacities.get(pool))
            for pool in CAPACITY_POOLS
        }
        character_rows.append({
            "slot": slot,
            "record_state": _state(character.get("state")),
            "skills_state": skills_state,
            "known_skill_count": len(skills),
            "job_capacity_status": capacity_summary,
        })
        if skills_state != "verified":
            unfilled.append(f"character_slot_{slot}: verify the relevant skill inventory")
        for pool, status in capacity_summary.items():
            if status == "unknown":
                unfilled.append(f"character_slot_{slot}: enter currently free {pool} job slots")

    capital = profile.get("capital", {})
    if not isinstance(capital, dict):
        capital = {}
    capital_known = {field: capital.get(field) is not None for field in CAPITAL_FIELDS}
    for field, known in capital_known.items():
        if not known:
            unfilled.append(f"capital: enter {field}")

    operations = profile.get("operations", {})
    if not isinstance(operations, dict):
        operations = {}
    operations_known = {field: operations.get(field) is not None for field in OPERATION_FIELDS}
    for field, known in operations_known.items():
        if not known:
            unfilled.append(f"operations: enter {field}")
    if operations.get("risk_tolerance", "unknown") == "unknown":
        unfilled.append("operations: set risk_tolerance")

    blueprints = profile.get("blueprints", [])
    if not isinstance(blueprints, list):
        blueprints = []
    blueprint_state = _state(profile.get("blueprints_state"))
    if blueprint_state != "verified":
        unfilled.append("blueprints: verify the inventory or mark it partial")

    facilities = profile.get("facilities", [])
    if not isinstance(facilities, list):
        facilities = []
    facility_state = _state(profile.get("facilities_state"))
    verified_facilities = sum(
        1 for item in facilities
        if isinstance(item, dict) and item.get("state") == "verified"
    )
    if facility_state != "verified":
        unfilled.append("facilities: verify accessible facility coverage or mark it partial")

    market = profile.get("market_access")
    if isinstance(market, dict):
        market_state = _state(market.get("state"))
        locations = market.get("locations", [])
        if not isinstance(locations, list):
            locations = []
        procurement_count = sum(
            1 for item in locations
            if isinstance(item, dict)
            and isinstance(item.get("roles"), list)
            and "procurement" in item["roles"]
        )
        sales_count = sum(
            1 for item in locations
            if isinstance(item, dict)
            and isinstance(item.get("roles"), list)
            and "sales" in item["roles"]
        )
    else:
        market_state = "not_entered"
        locations = []
        procurement_count = 0
        sales_count = 0
    if market_state != "verified" or procurement_count == 0 or sales_count == 0:
        unfilled.append("market_access: verify at least one procurement and one sales location")

    logistics = profile.get("logistics")
    if isinstance(logistics, dict):
        logistics_state = _state(logistics.get("state"))
        raw_method = logistics.get("preferred_method", "unknown")
        allowed_methods = {"unknown", "self_haul", "courier", "either", "none"}
        logistics_method = raw_method if isinstance(raw_method, str) and raw_method in allowed_methods else "unknown"
        logistics_limits_known = all(
            logistics.get(field) is not None
            for field in ("max_route_jumps", "max_active_minutes_per_batch", "max_cargo_m3")
        )
    else:
        logistics_state = "not_entered"
        logistics_method = "unknown"
        logistics_limits_known = False
    if logistics_state != "verified" or logistics_method == "unknown" or not logistics_limits_known:
        unfilled.append("logistics: verify preferred method and practical route/time/cargo limits")

    return {
        "report_version": 1,
        "profile_schema_valid": not errors,
        "validation_error_count": len(errors),
        "character_slots": character_rows,
        "blueprint_inventory": {
            "state": blueprint_state,
            "record_count": len(blueprints),
        },
        "facility_inventory": {
            "state": facility_state,
            "record_count": len(facilities),
            "verified_facility_count": verified_facilities,
        },
        "market_access": {
            "state": market_state,
            "location_count": len(locations),
            "procurement_location_count": procurement_count,
            "sales_location_count": sales_count,
        },
        "capital": {
            "state": _state(capital.get("state")),
            "fields_known": capital_known,
        },
        "operations": {
            "state": _state(operations.get("state")),
            "fields_known": operations_known,
            "risk_tolerance_known": operations.get("risk_tolerance") in {"low", "moderate", "high"},
        },
        "logistics": {
            "state": logistics_state,
            "preferred_method": logistics_method,
            "practical_limits_known": logistics_limits_known,
        },
        "unfilled_areas": unfilled,
        "privacy": {
            "contains_character_labels": False,
            "contains_skill_ids_or_levels": False,
            "contains_blueprint_ids": False,
            "contains_market_location_ids_or_names": False,
            "contains_isk_amounts": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        type=Path,
        default=Path("local/operating-profile.json"),
        help="Private profile path (default: local/operating-profile.json)",
    )
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()
    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
        if not isinstance(profile, dict):
            raise ValueError("Profile root must be a JSON object")
        report = build_readiness_report(profile)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"PASS: wrote redacted profile readiness report to {args.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
