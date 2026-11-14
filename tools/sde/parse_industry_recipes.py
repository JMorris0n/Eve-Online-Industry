#!/usr/bin/env python3
"""Normalize current CCP SDE blueprint activities into recipe JSONL.

Targets the post-September-2025 SDE JSON Lines schema. This is a deterministic
extractor, not a job-quote or profitability calculator.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterator


SUPPORTED_ACTIVITIES = ("manufacturing", "reaction")


def iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    """Yield JSON objects with line-numbered parse errors."""
    with path.open("r", encoding="utf-8-sig") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            # Current SDE tables are normally direct objects keyed by _key.
            # Also accept the documented generic _key/_value envelope.
            if "_value" in record and isinstance(record["_value"], dict):
                value = dict(record["_value"])
                value.setdefault("_key", record.get("_key"))
                record = value
            yield record


def load_type_metadata(path: Path) -> dict[int, dict[str, Any]]:
    metadata: dict[int, dict[str, Any]] = {}
    for record in iter_jsonl(path):
        type_id = record.get("_key")
        name = record.get("name")
        if isinstance(type_id, bool) or not isinstance(type_id, int):
            continue
        english = name.get("en") if isinstance(name, dict) else None
        metadata[type_id] = {
            "name": english if isinstance(english, str) else None,
            "published": record.get("published"),
            "group_id": record.get("groupID"),
            "market_group_id": record.get("marketGroupID"),
            "tech_level": record.get("techLevel"),
            "portion_size": record.get("portionSize"),
            "volume": record.get("volume"),
            "packaged_volume": record.get("packagedVolume"),
        }
    return metadata


def _normalize_items(items: Any, type_metadata: dict[int, dict[str, Any]], field: str) -> list[dict[str, Any]]:
    if not isinstance(items, list):
        raise ValueError(f"activity.{field} must be an array")
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError(f"activity.{field} entries must be objects")
        type_id = item.get("typeID")
        quantity = item.get("quantity")
        if isinstance(type_id, bool) or not isinstance(type_id, int) or type_id <= 0:
            raise ValueError(f"activity.{field} contains invalid typeID: {type_id!r}")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError(f"activity.{field} contains invalid quantity: {quantity!r}")
        type_info = type_metadata.get(type_id, {})
        normalized.append({
            "type_id": type_id,
            "name": type_info.get("name"),
            "quantity_per_run": quantity,
            "published": type_info.get("published"),
            "group_id": type_info.get("group_id"),
            "market_group_id": type_info.get("market_group_id"),
            "tech_level": type_info.get("tech_level"),
            "portion_size": type_info.get("portion_size"),
            "volume": type_info.get("volume"),
            "packaged_volume": type_info.get("packaged_volume"),
        })
    return sorted(normalized, key=lambda entry: entry["type_id"])


def _normalize_optional_items(
    activity: dict[str, Any],
    field: str,
    type_metadata: dict[int, dict[str, Any]],
    *,
    required: bool = False,
) -> tuple[list[dict[str, Any]], str]:
    """Normalize an optional SDE array while preserving whether it was omitted."""
    if field not in activity:
        if required:
            raise ValueError(f"activity.{field} is required")
        return [], "omitted"
    raw_items = activity[field]
    if raw_items is None:
        if required:
            raise ValueError(f"activity.{field} cannot be null")
        return [], "null"
    normalized = _normalize_items(raw_items, type_metadata, field)
    return normalized, "present" if normalized else "empty"


def normalize_blueprint(
    blueprint: dict[str, Any],
    type_metadata: dict[int, dict[str, Any]],
    activity_name: str,
    stats: dict[str, int] | None = None,
) -> dict[str, Any] | None:
    activities = blueprint.get("activities")
    if not isinstance(activities, dict):
        raise ValueError("blueprint activities must be an object")
    activity = activities.get(activity_name)
    if activity is None:
        return None
    if not isinstance(activity, dict):
        raise ValueError(f"{activity_name} activity must be an object")

    blueprint_id = blueprint.get("blueprintTypeID", blueprint.get("_key"))
    if isinstance(blueprint_id, bool) or not isinstance(blueprint_id, int) or blueprint_id <= 0:
        raise ValueError(f"invalid blueprintTypeID: {blueprint_id!r}")

    # Manufacturing arrays are optional in the current SDE schema. Preserve
    # omission as an explicit incomplete-data state instead of interpreting it
    # as a zero-input recipe. Reaction arrays are required by the schema.
    arrays_required = activity_name == "reaction"
    materials, materials_state = _normalize_optional_items(
        activity, "materials", type_metadata, required=arrays_required
    )
    products, products_state = _normalize_optional_items(
        activity, "products", type_metadata, required=arrays_required
    )
    if not products:
        if stats is not None:
            stats["skipped_without_products"] = stats.get("skipped_without_products", 0) + 1
        return None
    if activity_name == "reaction" and not materials:
        raise ValueError(f"reaction activity for blueprint {blueprint_id} has no materials")

    time_seconds = activity.get("time")
    if isinstance(time_seconds, bool) or not isinstance(time_seconds, int) or time_seconds < 0:
        raise ValueError(f"{activity_name} activity for blueprint {blueprint_id} has invalid time")

    if "skills" not in activity:
        raw_skills, skills_state = [], "omitted"
    elif activity["skills"] is None:
        if activity_name == "reaction":
            raise ValueError("activity.skills cannot be null")
        raw_skills, skills_state = [], "null"
    else:
        raw_skills = activity["skills"]
        if not isinstance(raw_skills, list):
            raise ValueError(f"{activity_name} activity skills must be an array")
        skills_state = "present" if raw_skills else "empty"
    normalized_skills = []
    for skill in raw_skills:
        if not isinstance(skill, dict):
            raise ValueError("skill entries must be objects")
        type_id, level = skill.get("typeID"), skill.get("level")
        if (isinstance(type_id, bool) or not isinstance(type_id, int) or type_id <= 0
                or isinstance(level, bool) or not isinstance(level, int) or not 0 <= level <= 5):
            raise ValueError(f"invalid required skill entry: {skill!r}")
        normalized_skills.append({"type_id": type_id, "name": type_metadata.get(type_id, {}).get("name"), "level": level})

    blueprint_info = type_metadata.get(blueprint_id, {})
    return {
        "schema_version": 2,
        "source": "CCP SDE",
        "activity": activity_name,
        "source_field_state": {
            "materials": materials_state,
            "products": products_state,
            "required_skills": skills_state,
        },
        "recipe_data_status": (
            "complete"
            if materials_state in {"present", "empty"} and products_state == "present"
            else "incomplete"
        ),
        "blueprint_type_id": blueprint_id,
        "blueprint_name": blueprint_info.get("name"),
        "blueprint_published": blueprint_info.get("published"),
        "blueprint_group_id": blueprint_info.get("group_id"),
        "blueprint_market_group_id": blueprint_info.get("market_group_id"),
        "max_production_limit": blueprint.get("maxProductionLimit"),
        "base_time_seconds_per_run": time_seconds,
        "materials": materials,
        "products": products,
        "required_skills": sorted(normalized_skills, key=lambda entry: entry["type_id"]),
    }


def extract_recipes(
    sde_dir: Path,
    activity_names: tuple[str, ...] = SUPPORTED_ACTIVITIES,
    stats: dict[str, int] | None = None,
) -> Iterator[dict[str, Any]]:
    blueprint_path = sde_dir / "blueprints.jsonl"
    types_path = sde_dir / "types.jsonl"
    if not blueprint_path.is_file():
        raise FileNotFoundError(f"Missing SDE file: {blueprint_path}")
    if not types_path.is_file():
        raise FileNotFoundError(f"Missing SDE file: {types_path}")
    type_metadata = load_type_metadata(types_path)
    counters = stats if stats is not None else {}
    counters.setdefault("activity_records_seen", 0)
    counters.setdefault("recipes_with_omitted_materials", 0)
    counters.setdefault("recipes_with_omitted_skills", 0)
    counters.setdefault("skipped_without_products", 0)
    for blueprint in iter_jsonl(blueprint_path):
        for activity_name in activity_names:
            activities = blueprint.get("activities")
            if not isinstance(activities, dict) or activities.get(activity_name) is None:
                continue
            counters["activity_records_seen"] += 1
            recipe = normalize_blueprint(blueprint, type_metadata, activity_name, counters)
            if recipe is not None:
                if recipe["source_field_state"]["materials"] in {"omitted", "null"}:
                    counters["recipes_with_omitted_materials"] += 1
                if recipe["source_field_state"]["required_skills"] in {"omitted", "null"}:
                    counters["recipes_with_omitted_skills"] += 1
                yield recipe


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sde-dir", type=Path, required=True,
                        help="Directory containing extracted blueprints.jsonl and types.jsonl")
    parser.add_argument("--activity", choices=("manufacturing", "reaction", "all"),
                        default="all")
    parser.add_argument("--output", type=Path, required=True,
                        help="Destination JSONL file (normally under data/derived/)")
    args = parser.parse_args()
    selected = SUPPORTED_ACTIVITIES if args.activity == "all" else (args.activity,)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    stats: dict[str, int] = {}
    try:
        with args.output.open("w", encoding="utf-8", newline="\n") as output:
            for recipe in extract_recipes(args.sde_dir, selected, stats):
                output.write(json.dumps(recipe, ensure_ascii=False) + "\n")
                count += 1
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        args.output.unlink(missing_ok=True)
        return 1
    print(f"PASS: wrote {count:,} normalized recipes to {args.output}")
    print(f"Activity records examined: {stats.get('activity_records_seen', 0):,}")
    print(f"Skipped because no product array was available: {stats.get('skipped_without_products', 0):,}")
    print(f"Recipes with omitted/null material arrays: {stats.get('recipes_with_omitted_materials', 0):,}")
    print(f"Recipes with omitted/null skill arrays: {stats.get('recipes_with_omitted_skills', 0):,}")
    print("Recipes with omitted/null material arrays are marked incomplete and must not be costed as zero-input recipes.")
    print("Note: material quantities are SDE base quantities per run; industry job modifiers and facility costs are not applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
