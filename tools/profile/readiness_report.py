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
DEFAULT_IMPORT_MANIFEST = Path("data/private/esi/profile-import-manifest.json")
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


def _diagnostic_codes(warnings: Any, category: str) -> list[str]:
    """Map private importer warnings to generic, non-identifying reason codes."""
    if not isinstance(warnings, list):
        return []
    codes: set[str] = set()
    for warning in warnings:
        if not isinstance(warning, str):
            continue
        message = warning.casefold()
        if category == "skills":
            if "snapshot exceeds" in message:
                codes.add("snapshot_stale")
            elif "skill api level is behind" in message:
                codes.add("completed_skill_queue_level_not_reflected")
            elif "skill-queue row" in message and "malformed" in message:
                codes.add("malformed_skill_queue_entry")
            elif "skill-queue row" in message and "completion time" in message:
                codes.add("unreadable_skill_queue_finish_time")
        elif category == "jobs":
            if "snapshot exceeds" in message:
                codes.add("snapshot_stale")
            elif "industry-job row" in message and "malformed" in message:
                codes.add("malformed_industry_job_record")
            elif "no valid status" in message:
                codes.add("missing_industry_job_status")
            elif "unrecognized status" in message:
                codes.add("unrecognized_industry_job_status")
            elif "no valid activity id" in message:
                codes.add("missing_industry_activity_id")
            elif "unrecognized activity id" in message:
                codes.add("unrecognized_industry_activity_id")
            elif "free-slot count could not be verified" in message:
                codes.add("free_slot_count_unverified")
        if not codes and message:
            codes.add("other_import_warning")
    return sorted(codes)


def build_readiness_report(
    profile: dict[str, Any],
    import_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a low-disclosure readiness summary; never return account values."""
    errors = validate_profile_data(profile)
    characters = profile.get("characters", [])
    if not isinstance(characters, list):
        characters = []

    manifest_rows = (
        import_manifest.get("character_mapping", [])
        if isinstance(import_manifest, dict) else []
    )
    if not isinstance(manifest_rows, list):
        manifest_rows = []
    manifest_by_slot = {
        row.get("slot"): row
        for row in manifest_rows
        if isinstance(row, dict)
        and isinstance(row.get("slot"), int)
        and not isinstance(row.get("slot"), bool)
    }

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
        import_row = manifest_by_slot.get(slot, {})
        warnings = import_row.get("warnings", []) if isinstance(import_row, dict) else []
        skills_reasons = _diagnostic_codes(warnings, "skills")
        jobs_reasons = _diagnostic_codes(warnings, "jobs")
        if isinstance(import_row, dict) and import_row.get("snapshot_stale") is True:
            if "snapshot_stale" not in skills_reasons:
                skills_reasons = sorted([*skills_reasons, "snapshot_stale"])
            if "snapshot_stale" not in jobs_reasons:
                jobs_reasons = sorted([*jobs_reasons, "snapshot_stale"])
        if import_manifest is not None and skills_state != "verified" and not skills_reasons:
            skills_reasons = ["unclassified_partial_state"]
        if (
            import_manifest is not None
            and any(status == "unknown" for status in capacity_summary.values())
            and not jobs_reasons
        ):
            jobs_reasons = (
                ["job_capacity_blocked_by_partial_skills"]
                if skills_reasons else ["job_capacity_unverified"]
            )
        character_rows.append({
            "slot": slot,
            "record_state": _state(character.get("state")),
            "skills_state": skills_state,
            "known_skill_count": len(skills),
            "job_capacity_status": capacity_summary,
            "skills_diagnostic_codes": skills_reasons,
            "job_capacity_diagnostic_codes": jobs_reasons,
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
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_IMPORT_MANIFEST,
        help="Private import manifest used to add redacted diagnostic reason codes.",
    )
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()
    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
        if not isinstance(profile, dict):
            raise ValueError("Profile root must be a JSON object")
        import_manifest = None
        if args.manifest.is_file():
            import_manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
            if not isinstance(import_manifest, dict):
                raise ValueError("Import manifest root must be a JSON object")
        report = build_readiness_report(profile, import_manifest)
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
