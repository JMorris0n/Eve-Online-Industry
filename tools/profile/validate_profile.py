#!/usr/bin/env python3
"""Validate a private local EVE industry operating profile (standard library only)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

VALID_STATES = {"unknown", "partial", "verified"}
ALLOWED_TOP_LEVEL = {
    "profile_version", "profile_name", "last_reviewed", "characters",
    "capital", "operations", "facilities", "blueprints", "blueprints_state",
    "facilities_state", "notes", "market_access", "logistics",
}
REQUIRED_TOP_LEVEL = {
    "profile_version", "profile_name", "characters", "capital", "operations",
    "facilities", "blueprints", "blueprints_state", "facilities_state",
}


def _is_choice(value: Any, choices: set[str]) -> bool:
    """Safely validate enum-like fields, including malformed non-string JSON values."""
    return isinstance(value, str) and value in choices


def _nonnegative_number(value: Any) -> bool:
    return value is None or (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and value >= 0
    )


def validate_profile_data(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["profile must be a JSON object"]

    missing = REQUIRED_TOP_LEVEL - data.keys()
    if missing:
        errors.append("missing top-level fields: " + ", ".join(sorted(missing)))
    extra = data.keys() - ALLOWED_TOP_LEVEL
    if extra:
        errors.append("unknown top-level fields: " + ", ".join(sorted(extra)))
    if isinstance(data.get("profile_version"), bool) or data.get("profile_version") != 1:
        errors.append("profile_version must be 1")
    if not isinstance(data.get("profile_name"), str) or not data.get("profile_name", "").strip():
        errors.append("profile_name must be a non-empty string")

    characters = data.get("characters")
    if not isinstance(characters, list) or len(characters) != 3:
        errors.append("characters must contain exactly three character records")
        characters = []
    slots: list[int] = []
    for index, character in enumerate(characters):
        prefix = f"characters[{index}]"
        if not isinstance(character, dict):
            errors.append(f"{prefix} must be an object")
            continue
        slot = character.get("slot")
        if isinstance(slot, bool) or not isinstance(slot, int) or slot not in (1, 2, 3):
            errors.append(f"{prefix}.slot must be 1, 2, or 3")
        else:
            slots.append(slot)
        if not _is_choice(character.get("state"), VALID_STATES):
            errors.append(f"{prefix}.state must be unknown, partial, or verified")
        if not isinstance(character.get("label"), str) or not character.get("label", "").strip():
            errors.append(f"{prefix}.label must be a non-empty string")
        if not _is_choice(character.get("skills_state"), VALID_STATES):
            errors.append(f"{prefix}.skills_state must be unknown, partial, or verified")
        skills = character.get("skills")
        if not isinstance(skills, dict):
            errors.append(f"{prefix}.skills must be an object")
        else:
            for skill, level in skills.items():
                if not isinstance(skill, str) or not skill.isdigit() or int(skill) <= 0:
                    errors.append(f"{prefix}.skills key {skill!r} must be a positive numeric skill type ID")
                if isinstance(level, bool) or not isinstance(level, int) or not 0 <= level <= 5:
                    errors.append(f"{prefix}.skills[{skill!r}] must be an integer from 0 to 5")
        capacity = character.get("job_capacity")
        if not isinstance(capacity, dict):
            errors.append(f"{prefix}.job_capacity must be an object")
        else:
            for pool in ("manufacturing", "science", "reaction"):
                if pool not in capacity:
                    errors.append(f"{prefix}.job_capacity.{pool} is required")
                elif capacity[pool] is not None and (
                    isinstance(capacity[pool], bool)
                    or not isinstance(capacity[pool], int)
                    or capacity[pool] < 0
                ):
                    errors.append(f"{prefix}.job_capacity.{pool} must be a non-negative integer or null")
    if sorted(slots) != [1, 2, 3]:
        errors.append("character slots must be unique and include 1, 2, and 3")

    capital = data.get("capital")
    if not isinstance(capital, dict):
        errors.append("capital must be an object")
    else:
        if not _is_choice(capital.get("state"), VALID_STATES):
            errors.append("capital.state is invalid")
        for field in ("working_capital_isk", "liquidity_reserve_isk", "max_capital_at_risk_isk"):
            value = capital.get(field)
            if field not in capital or not _nonnegative_number(value) or (
                value is not None and not isinstance(value, int)
            ):
                errors.append(f"capital.{field} must be a non-negative integer or null")

    operations = data.get("operations")
    if not isinstance(operations, dict):
        errors.append("operations must be an object")
    else:
        if not _is_choice(operations.get("state"), VALID_STATES):
            errors.append("operations.state is invalid")
        for field in ("active_hours_per_week", "max_setup_minutes_per_batch", "target_liquidation_days"):
            if field not in operations:
                errors.append(f"operations.{field} is required")
        if not _nonnegative_number(operations.get("active_hours_per_week")):
            errors.append("operations.active_hours_per_week must be non-negative or null")
        for field in ("max_setup_minutes_per_batch", "target_liquidation_days"):
            value = operations.get(field)
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int) or value < 0
            ):
                errors.append(f"operations.{field} must be a non-negative integer or null")
        if not _is_choice(operations.get("risk_tolerance"), {"unknown", "low", "moderate", "high"}):
            errors.append("operations.risk_tolerance is invalid")

    if "market_access" in data:
        market_access = data["market_access"]
        if not isinstance(market_access, dict):
            errors.append("market_access must be an object")
        else:
            if not _is_choice(market_access.get("state"), VALID_STATES):
                errors.append("market_access.state is invalid")
            locations = market_access.get("locations")
            if not isinstance(locations, list):
                errors.append("market_access.locations must be an array")
                locations = []
            if "notes" in market_access and not isinstance(market_access["notes"], list):
                errors.append("market_access.notes must be an array")
            for index, location in enumerate(locations):
                prefix = f"market_access.locations[{index}]"
                if not isinstance(location, dict):
                    errors.append(f"{prefix} must be an object")
                    continue
                if not isinstance(location.get("label"), str) or not location.get("label", "").strip():
                    errors.append(f"{prefix}.label must be a non-empty string")
                if not _is_choice(location.get("state"), VALID_STATES):
                    errors.append(f"{prefix}.state is invalid")
                if not _is_choice(location.get("market_type"), {"unknown", "npc_station", "upwell_structure"}):
                    errors.append(f"{prefix}.market_type is invalid")
                for field in ("region_id", "system_id", "location_id"):
                    value = location.get(field)
                    if value is not None and (
                        isinstance(value, bool) or not isinstance(value, int) or value < 1
                    ):
                        errors.append(f"{prefix}.{field} must be a positive integer or null")
                roles = location.get("roles")
                if not isinstance(roles, list) or any(
                    not _is_choice(role, {"procurement", "sales"}) for role in roles
                ):
                    errors.append(f"{prefix}.roles must contain only procurement and/or sales")
                if "notes" in location and not isinstance(location["notes"], list):
                    errors.append(f"{prefix}.notes must be an array")

    if "logistics" in data:
        logistics = data["logistics"]
        if not isinstance(logistics, dict):
            errors.append("logistics must be an object")
        else:
            if not _is_choice(logistics.get("state"), VALID_STATES):
                errors.append("logistics.state is invalid")
            if not _is_choice(logistics.get("preferred_method"), {"unknown", "self_haul", "courier", "either", "none"}):
                errors.append("logistics.preferred_method is invalid")
            for field in ("max_route_jumps", "max_active_minutes_per_batch"):
                value = logistics.get(field)
                if value is not None and (
                    isinstance(value, bool) or not isinstance(value, int) or value < 0
                ):
                    errors.append(f"logistics.{field} must be a non-negative integer or null")
            if not _nonnegative_number(logistics.get("max_cargo_m3")):
                errors.append("logistics.max_cargo_m3 must be non-negative or null")
            if "notes" in logistics and not isinstance(logistics["notes"], list):
                errors.append("logistics.notes must be an array")

    for state_field in ("facilities_state", "blueprints_state"):
        if not _is_choice(data.get(state_field), VALID_STATES):
            errors.append(f"{state_field} must be unknown, partial, or verified")

    for collection in ("facilities", "blueprints"):
        if not isinstance(data.get(collection), list):
            errors.append(f"{collection} must be an array")
    if "notes" in data and not isinstance(data["notes"], list):
        errors.append("notes must be an array")

    for index, facility in enumerate(data.get("facilities", []) if isinstance(data.get("facilities"), list) else []):
        if not isinstance(facility, dict):
            errors.append(f"facilities[{index}] must be an object")
            continue
        if not isinstance(facility.get("label"), str) or not facility.get("label", "").strip():
            errors.append(f"facilities[{index}].label must be a non-empty string")
        if not _is_choice(facility.get("state"), VALID_STATES):
            errors.append(f"facilities[{index}].state is invalid")
        tax = facility.get("tax_rate")
        if tax is not None and (
            isinstance(tax, bool) or not isinstance(tax, (int, float)) or not 0 <= tax <= 1
        ):
            errors.append(f"facilities[{index}].tax_rate must be between 0 and 1 or null")

    for index, blueprint in enumerate(data.get("blueprints", []) if isinstance(data.get("blueprints"), list) else []):
        if not isinstance(blueprint, dict):
            errors.append(f"blueprints[{index}] must be an object")
            continue
        for field in ("type_id", "quantity"):
            value = blueprint.get(field)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                errors.append(f"blueprints[{index}].{field} must be a positive integer")
        if not _is_choice(blueprint.get("kind"), {"BPO", "BPC"}):
            errors.append(f"blueprints[{index}].kind must be BPO or BPC")
        if not _is_choice(blueprint.get("state"), VALID_STATES):
            errors.append(f"blueprints[{index}].state is invalid")
        for field in ("material_efficiency", "time_efficiency", "licensed_runs"):
            value = blueprint.get(field)
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int) or value < 0
            ):
                errors.append(f"blueprints[{index}].{field} must be a non-negative integer or null")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True, help="Path to the local profile JSON")
    args = parser.parse_args()
    try:
        data = json.loads(args.profile.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read profile: {exc}", file=sys.stderr)
        return 2

    errors = validate_profile_data(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {args.profile} is structurally valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
