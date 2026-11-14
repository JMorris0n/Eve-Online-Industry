#!/usr/bin/env python3
"""Check recipe feasibility against a private local operating profile.

This is a hard-constraint screen only. It does not calculate material costs,
ME/TE-adjusted quantities, job quotes, market access, or profitability.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _blueprint_status(profile: dict[str, Any], blueprint_type_id: int) -> tuple[str, str]:
    records = profile.get("blueprints", [])
    matches = [record for record in records if record.get("type_id") == blueprint_type_id]
    verified = [record for record in matches if record.get("state") == "verified"]
    partial = [record for record in matches if record.get("state") in {"partial", "unknown"}]

    usable = []
    for record in verified:
        if record.get("kind") == "BPO":
            usable.append(record)
        elif record.get("kind") == "BPC":
            runs = record.get("licensed_runs")
            if isinstance(runs, int) and runs > 0:
                usable.append(record)
            elif runs is None:
                partial.append(record)
    if usable:
        return "eligible", f"Verified usable blueprint copy/record found for type {blueprint_type_id}."
    if partial:
        return "unknown", "A matching blueprint record exists but its usability is not fully verified."
    if profile.get("blueprints_state") == "verified":
        return "ineligible", f"Blueprint inventory is verified complete and has no usable copy for type {blueprint_type_id}."
    return "unknown", "Blueprint inventory is not verified complete; absence cannot be treated as non-ownership."


def _character_status(character: dict[str, Any], recipe: dict[str, Any]) -> tuple[str, list[str]]:
    activity = recipe["activity"]
    pool = "manufacturing" if activity == "manufacturing" else "reaction"
    reasons: list[str] = []
    unknown = False

    capacity = character.get("job_capacity", {}).get(pool)
    if capacity is None:
        unknown = True
        reasons.append(f"{pool} job capacity is unknown")
    elif capacity <= 0:
        return "ineligible", [f"no available {pool} job capacity"]

    for skill in recipe.get("required_skills", []):
        skill_id = str(skill["type_id"])
        required = skill["level"]
        trained = character.get("skills", {}).get(skill_id)
        if trained is None:
            if character.get("skills_state") == "verified":
                trained = 0
            else:
                unknown = True
                reasons.append(f"skill {skill_id} level is unknown (requires {required})")
                continue
        if trained < required:
            return "ineligible", [f"skill {skill_id} level {trained} is below required level {required}"]

    if unknown:
        return "unknown", reasons
    return "eligible", ["character meets listed skill and job-capacity requirements"]


def evaluate_recipe(profile: dict[str, Any], recipe: dict[str, Any]) -> dict[str, Any]:
    blueprint_status, blueprint_reason = _blueprint_status(
        profile, recipe["blueprint_type_id"]
    )
    # Facilities use a list of supported services rather than a single ID.
    facility_records = profile.get("facilities", [])
    matching_facilities = [
        item for item in facility_records
        if recipe["activity"] in item.get("services", [])
    ]
    verified_facilities = [item for item in matching_facilities if item.get("state") == "verified"]
    partial_facilities = [item for item in matching_facilities if item.get("state") in {"partial", "unknown"}]
    if verified_facilities:
        facility_status = "eligible"
        facility_reason = f"{len(verified_facilities)} verified accessible facility record(s) support {recipe['activity']}."
    elif partial_facilities:
        facility_status = "unknown"
        facility_reason = "A potentially suitable facility is recorded but not verified."
    elif profile.get("facilities_state") == "verified":
        facility_status = "ineligible"
        facility_reason = f"Facility inventory is verified complete and no accessible {recipe['activity']} facility is recorded."
    else:
        facility_status = "unknown"
        facility_reason = "Facility inventory is not verified complete; access is unknown."

    character_results = []
    for character in profile.get("characters", []):
        status, reasons = _character_status(character, recipe)
        character_results.append({
            "slot": character.get("slot"),
            "label": character.get("label"),
            "status": status,
            "reasons": reasons,
        })
    if any(item["status"] == "eligible" for item in character_results):
        character_status = "eligible"
        character_reason = "At least one character meets the recipe skill and job-capacity requirements."
    elif any(item["status"] == "unknown" for item in character_results):
        character_status = "unknown"
        character_reason = "No character is confirmed eligible; at least one character has incomplete skill or job-capacity data."
    else:
        character_status = "ineligible"
        character_reason = "No character meets the recipe skill and job-capacity requirements."

    component_statuses = [blueprint_status, facility_status, character_status]
    overall = (
        "ineligible" if "ineligible" in component_statuses
        else "unknown" if "unknown" in component_statuses
        else "eligible"
    )
    return {
        "product_type_ids": [item["type_id"] for item in recipe.get("products", [])],
        "product_names": [item.get("name") for item in recipe.get("products", [])],
        "blueprint_type_id": recipe["blueprint_type_id"],
        "blueprint_name": recipe.get("blueprint_name"),
        "activity": recipe["activity"],
        "status": overall,
        "checks": {
            "blueprint": {"status": blueprint_status, "reason": blueprint_reason},
            "facility": {"status": facility_status, "reason": facility_reason},
            "characters": {
                "status": character_status,
                "reason": character_reason,
                "by_character": character_results,
            },
        },
        "limitations": [
            "This is a hard-constraint screen, not a production quote or profitability recommendation.",
            "It does not calculate material efficiency, time efficiency, facility bonuses, job installation costs, or market access.",
            "A character with a free job slot is not proof that the slot is actually unused at job installation time.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--recipes", type=Path, required=True,
                        help="Normalized JSONL from tools/sde/parse_industry_recipes.py")
    parser.add_argument("--product-type-id", type=int,
                        help="Optional product type ID filter")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
        results = []
        with args.recipes.open("r", encoding="utf-8-sig") as stream:
            for line_number, line in enumerate(stream, start=1):
                if not line.strip():
                    continue
                recipe = json.loads(line)
                if args.product_type_id is not None and not any(
                    product.get("type_id") == args.product_type_id
                    for product in recipe.get("products", [])
                ):
                    continue
                results.append(evaluate_recipe(profile, recipe))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps({"schema_version": 1, "results": results}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    counts = {status: sum(item["status"] == status for item in results)
              for status in ("eligible", "ineligible", "unknown")}
    print(f"PASS: evaluated {len(results)} recipe(s): {counts}; report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
