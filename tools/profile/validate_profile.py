#!/usr/bin/env python3
"""Validate a private local EVE industry operating profile (standard library only)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

VALID_STATES = {"unknown", "partial", "verified"}
TOP_LEVEL = {
    "profile_version", "profile_name", "last_reviewed", "characters",
    "capital", "operations", "facilities", "blueprints", "notes",
}


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

    missing = TOP_LEVEL - data.keys()
    if missing:
        errors.append("missing top-level fields: " + ", ".join(sorted(missing)))
    extra = data.keys() - TOP_LEVEL
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
        if character.get("state") not in VALID_STATES:
            errors.append(f"{prefix}.state must be unknown, partial, or verified")
        if not isinstance(character.get("label"), str) or not character.get("label", "").strip():
            errors.append(f"{prefix}.label must be a non-empty string")
        skills = character.get("skills")
        if not isinstance(skills, dict):
            errors.append(f"{prefix}.skills must be an object")
        else:
            for skill, level in skills.items():
                if not isinstance(skill, str) or not skill.strip():
                    errors.append(f"{prefix}.skills contains an empty skill name")
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
        if capital.get("state") not in VALID_STATES:
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
        if operations.get("state") not in VALID_STATES:
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
        if operations.get("risk_tolerance") not in {"unknown", "low", "moderate", "high"}:
            errors.append("operations.risk_tolerance is invalid")

    for collection in ("facilities", "blueprints", "notes"):
        if not isinstance(data.get(collection), list):
            errors.append(f"{collection} must be an array")

    for index, facility in enumerate(data.get("facilities", []) if isinstance(data.get("facilities"), list) else []):
        if not isinstance(facility, dict):
            errors.append(f"facilities[{index}] must be an object")
            continue
        if not isinstance(facility.get("label"), str) or not facility.get("label", "").strip():
            errors.append(f"facilities[{index}].label must be a non-empty string")
        if facility.get("state") not in VALID_STATES:
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
        if blueprint.get("kind") not in {"BPO", "BPC"}:
            errors.append(f"blueprints[{index}].kind must be BPO or BPC")
        if blueprint.get("state") not in VALID_STATES:
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
