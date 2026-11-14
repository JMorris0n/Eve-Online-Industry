#!/usr/bin/env python3
"""Audit normalized SDE manufacturing/reaction recipes without dumping the recipe file."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

FIELDS = ("materials", "products", "required_skills")
TYPE_CATEGORIES = ("blueprint", "product", "material", "skill")


def _is_positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _is_choice(value: Any, choices: set[str]) -> bool:
    return isinstance(value, str) and value in choices


def _metadata_counts() -> dict[str, dict[str, int]]:
    return {
        category: {
            "references": 0,
            "missing_name": 0,
            "unpublished": 0,
            "unknown_publication": 0,
        }
        for category in TYPE_CATEGORIES
    }


def audit_recipes(input_path: Path, max_samples: int = 25) -> dict[str, Any]:
    if max_samples < 1:
        raise ValueError("max_samples must be >= 1")
    if not input_path.is_file():
        raise FileNotFoundError(f"Recipe file does not exist: {input_path}")

    activity_counts: Counter[str] = Counter()
    completeness_counts: Counter[str] = Counter()
    field_state_counts = {field: Counter() for field in FIELDS}
    metadata = _metadata_counts()
    unresolved_ids: set[int] = set()
    seen_keys: set[tuple[int, str]] = set()
    duplicate_keys: Counter[tuple[int, str]] = Counter()
    invalid_recipe_key_count = 0
    invalid_record_count = 0
    invalid_item_count = 0
    duplicate_item_type_id_count = 0
    zero_time_keys: list[dict[str, Any]] = []
    incomplete_material_keys: list[dict[str, Any]] = []
    unpublished_blueprint_keys: list[dict[str, Any]] = []
    unpublished_product_ids: set[int] = set()
    unknown_product_publication_ids: set[int] = set()
    record_count = 0
    zero_time_recipe_count = 0
    unpublished_blueprint_record_count = 0

    def observe_type(category: str, item: Any) -> None:
        if not isinstance(item, dict):
            return
        type_id = item.get("type_id")
        if not _is_positive_int(type_id):
            return
        counts = metadata[category]
        counts["references"] += 1
        if not isinstance(item.get("name"), str) or not item["name"].strip():
            counts["missing_name"] += 1
            unresolved_ids.add(type_id)
        if item.get("published") is False:
            counts["unpublished"] += 1
        elif item.get("published") is not True:
            counts["unknown_publication"] += 1

    with input_path.open("rb") as raw:
        source_bytes = raw.read()
    source_hash = hashlib.sha256(source_bytes).hexdigest()

    try:
        source_text = source_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{input_path}: file is not valid UTF-8: {exc}") from exc

    for line_number, line in enumerate(source_text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            recipe = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"{input_path.name}:{line_number}: invalid JSON: {exc}"
            ) from exc
        if not isinstance(recipe, dict):
            invalid_record_count += 1
            continue

        record_count += 1
        activity = recipe.get("activity")
        if isinstance(activity, str) and activity:
            activity_counts[activity] += 1
        else:
            activity_counts["<missing-or-invalid>"] += 1
            invalid_record_count += 1

        completeness = recipe.get("recipe_data_status")
        completeness_counts[str(completeness)] += 1
        if not _is_choice(completeness, {"complete", "incomplete"}):
            invalid_record_count += 1

        blueprint_id = recipe.get("blueprint_type_id")
        if not _is_positive_int(blueprint_id) or not isinstance(activity, str):
            invalid_recipe_key_count += 1
            key_label = None
        else:
            key = (blueprint_id, activity)
            key_label = {"blueprint_type_id": blueprint_id, "activity": activity}
            if key in seen_keys:
                duplicate_keys[key] += 1
            else:
                seen_keys.add(key)

        if _is_positive_int(blueprint_id):
            observe_type("blueprint", {
                "type_id": blueprint_id,
                "name": recipe.get("blueprint_name"),
                "published": recipe.get("blueprint_published"),
            })

        states = recipe.get("source_field_state")
        if not isinstance(states, dict):
            states = {}
            invalid_record_count += 1
        for field in FIELDS:
            state = states.get(field, "<missing>")
            field_state_counts[field][str(state)] += 1
        if _is_choice(states.get("materials"), {"omitted", "null"}):
            if key_label is not None and len(incomplete_material_keys) < max_samples:
                incomplete_material_keys.append(key_label)
        if _is_choice(states.get("materials"), {"omitted", "null"}) and completeness == "complete":
            invalid_record_count += 1
        if states.get("products") != "present" and completeness == "complete":
            invalid_record_count += 1

        base_time = recipe.get("base_time_seconds_per_run")
        if isinstance(base_time, bool) or not isinstance(base_time, int) or base_time < 0:
            invalid_record_count += 1
        elif base_time == 0:
            zero_time_recipe_count += 1
            if key_label is not None and len(zero_time_keys) < max_samples:
                zero_time_keys.append(key_label)

        if recipe.get("blueprint_published") is False:
            unpublished_blueprint_record_count += 1
            if key_label is not None and len(unpublished_blueprint_keys) < max_samples:
                unpublished_blueprint_keys.append(key_label)

        for field, category in (
            ("products", "product"),
            ("materials", "material"),
            ("required_skills", "skill"),
        ):
            items = recipe.get(field)
            if not isinstance(items, list):
                invalid_record_count += 1
                continue
            item_ids: set[int] = set()
            for item in items:
                if not isinstance(item, dict):
                    invalid_item_count += 1
                    continue
                type_id = item.get("type_id")
                if not _is_positive_int(type_id):
                    invalid_item_count += 1
                    continue
                if type_id in item_ids:
                    duplicate_item_type_id_count += 1
                item_ids.add(type_id)
                observe_type(category, item)
                if field == "products":
                    if item.get("published") is False:
                        unpublished_product_ids.add(type_id)
                    elif item.get("published") is not True:
                        unknown_product_publication_ids.add(type_id)

    return {
        "audit_version": 1,
        "source_file": input_path.name,
        "source_sha256": source_hash,
        "record_count": record_count,
        "activity_counts": dict(sorted(activity_counts.items())),
        "recipe_completeness_counts": dict(sorted(completeness_counts.items())),
        "source_field_state_counts": {
            field: dict(sorted(counts.items()))
            for field, counts in field_state_counts.items()
        },
        "recipe_key_quality": {
            "unique_blueprint_activity_keys": len(seen_keys),
            "duplicate_key_repeats": sum(duplicate_keys.values()),
            "duplicate_key_count": len(duplicate_keys),
            "invalid_key_count": invalid_recipe_key_count,
            "duplicate_key_samples": [
                {"blueprint_type_id": key[0], "activity": key[1], "extra_records": count}
                for key, count in sorted(duplicate_keys.items())[:max_samples]
            ],
        },
        "type_metadata": {
            "categories": metadata,
            "unique_unresolved_type_id_count": len(unresolved_ids),
            "unresolved_type_id_samples": sorted(unresolved_ids)[:max_samples],
            "unpublished_product_type_id_count": len(unpublished_product_ids),
            "unpublished_product_type_id_samples": sorted(unpublished_product_ids)[:max_samples],
            "unknown_product_publication_type_id_count": len(unknown_product_publication_ids),
            "unknown_product_publication_type_id_samples": sorted(unknown_product_publication_ids)[:max_samples],
        },
        "exceptional_records": {
            "zero_base_time_recipe_count": zero_time_recipe_count,
            "zero_base_time_recipe_samples": zero_time_keys,
            "unpublished_blueprint_record_count": unpublished_blueprint_record_count,
            "unpublished_blueprint_record_samples": unpublished_blueprint_keys,
            "incomplete_material_recipe_sample_count": len(incomplete_material_keys),
            "incomplete_material_recipe_samples": incomplete_material_keys,
        },
        "structural_quality": {
            "record_validation_issue_count": invalid_record_count,
            "invalid_recipe_item_count": invalid_item_count,
            "duplicate_item_type_id_count": duplicate_item_type_id_count,
        },
        "limitations": [
            "This audit checks normalized-file structure and joined metadata only.",
            "It does not verify source SDE rows beyond the parser output or resolve missing type metadata.",
            "Unpublished or unresolved records are reported for downstream filtering, not automatically repaired.",
            "No marketability, feasibility, or profitability conclusion is produced.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/derived/industry-recipes.jsonl"),
        help="Normalized recipe JSONL path",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/derived/industry-recipes-audit.json"),
        help="Audit JSON output path",
    )
    parser.add_argument("--max-samples", type=int, default=25)
    args = parser.parse_args()
    try:
        report = audit_recipes(args.input, args.max_samples)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"PASS: wrote SDE recipe audit to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
