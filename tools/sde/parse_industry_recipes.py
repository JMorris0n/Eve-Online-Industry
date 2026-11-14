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


def load_type_names(path: Path) -> dict[int, str]:
    names: dict[int, str] = {}
    for record in iter_jsonl(path):
        type_id = record.get("_key")
        name = record.get("name")
        if isinstance(type_id, int) and isinstance(name, dict):
            english = name.get("en")
            if isinstance(english, str) and english:
                names[type_id] = english
    return names


def _normalize_items(items: Any, names: dict[int, str], field: str) -> list[dict[str, Any]]:
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
        normalized.append({
            "type_id": type_id,
            "name": names.get(type_id),
            "quantity_per_run": quantity,
        })
    return sorted(normalized, key=lambda entry: entry["type_id"])


def normalize_blueprint(
    blueprint: dict[str, Any],
    names: dict[int, str],
    activity_name: str,
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

    products = _normalize_items(activity.get("products"), names, "products")
    materials = _normalize_items(activity.get("materials"), names, "materials")
    if not products:
        raise ValueError(f"{activity_name} activity for blueprint {blueprint_id} has no products")
    if not materials:
        raise ValueError(f"{activity_name} activity for blueprint {blueprint_id} has no materials")

    time_seconds = activity.get("time")
    if isinstance(time_seconds, bool) or not isinstance(time_seconds, int) or time_seconds < 0:
        raise ValueError(f"{activity_name} activity for blueprint {blueprint_id} has invalid time")

    skills = activity.get("skills", [])
    if not isinstance(skills, list):
        raise ValueError(f"{activity_name} activity skills must be an array")
    normalized_skills = []
    for skill in skills:
        if not isinstance(skill, dict):
            raise ValueError("skill entries must be objects")
        type_id, level = skill.get("typeID"), skill.get("level")
        if (isinstance(type_id, bool) or not isinstance(type_id, int) or type_id <= 0
                or isinstance(level, bool) or not isinstance(level, int) or not 0 <= level <= 5):
            raise ValueError(f"invalid required skill entry: {skill!r}")
        normalized_skills.append({"type_id": type_id, "name": names.get(type_id), "level": level})

    return {
        "schema_version": 1,
        "source": "CCP SDE",
        "activity": activity_name,
        "blueprint_type_id": blueprint_id,
        "blueprint_name": names.get(blueprint_id),
        "max_production_limit": blueprint.get("maxProductionLimit"),
        "base_time_seconds_per_run": time_seconds,
        "materials": materials,
        "products": products,
        "required_skills": sorted(normalized_skills, key=lambda entry: entry["type_id"]),
    }


def extract_recipes(
    sde_dir: Path,
    activity_names: tuple[str, ...] = SUPPORTED_ACTIVITIES,
) -> Iterator[dict[str, Any]]:
    blueprint_path = sde_dir / "blueprints.jsonl"
    types_path = sde_dir / "types.jsonl"
    if not blueprint_path.is_file():
        raise FileNotFoundError(f"Missing SDE file: {blueprint_path}")
    if not types_path.is_file():
        raise FileNotFoundError(f"Missing SDE file: {types_path}")
    names = load_type_names(types_path)
    for blueprint in iter_jsonl(blueprint_path):
        for activity_name in activity_names:
            recipe = normalize_blueprint(blueprint, names, activity_name)
            if recipe is not None:
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
    try:
        with args.output.open("w", encoding="utf-8", newline="\n") as output:
            for recipe in extract_recipes(args.sde_dir, selected):
                output.write(json.dumps(recipe, ensure_ascii=False) + "\n")
                count += 1
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        args.output.unlink(missing_ok=True)
        return 1
    print(f"PASS: wrote {count:,} normalized recipes to {args.output}")
    print("Note: material quantities are SDE base quantities per run; industry job modifiers and facility costs are not applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
