#!/usr/bin/env python3
"""Build a local, recipe-derived skill reference for the operating profile.

The output is a static-data reference, not proof of character eligibility,
blueprint ownership, facility access, marketability, or profitability.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ACTIVITIES = ("manufacturing", "reaction")
VALID_RECIPE_STATES = {"complete", "incomplete"}
VALID_ARRAY_STATES = {"present", "empty"}


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _level(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 5


def _name(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _publication(value: Any) -> str:
    if value is True:
        return "published"
    if value is False:
        return "unpublished"
    return "unknown"


def _new_skill_stat(type_id: int) -> dict[str, Any]:
    return {
        "type_id": type_id,
        "names": set(),
        "publication_states": set(),
        "source_recipe_keys": set(),
        "source_reference_count": 0,
        "candidate_recipe_keys": set(),
        "source_activity_counts": Counter(),
        "candidate_activity_counts": Counter(),
        "source_level_counts": Counter(),
        "candidate_level_counts": Counter(),
        "sample_candidate_recipes": [],
    }


def _recipe_label(recipe: dict[str, Any]) -> dict[str, Any]:
    return {
        "blueprint_type_id": recipe.get("blueprint_type_id"),
        "blueprint_name": recipe.get("blueprint_name"),
        "activity": recipe.get("activity"),
    }


def _add_sample(target: list[dict[str, Any]], sample: dict[str, Any], limit: int) -> None:
    if len(target) < limit and sample not in target:
        target.append(sample)


def _parse_jsonl(source_bytes: bytes, path: Path):
    try:
        source_text = source_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: file is not valid UTF-8: {exc}") from exc

    for line_number, line in enumerate(source_text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"{path.name}:{line_number}: expected a JSON object")
        yield record


def build_skill_reference(
    input_path: Path,
    activity: str = "all",
    sample_limit: int = 10,
) -> dict[str, Any]:
    """Build a deterministic skill reference from normalized recipe JSONL."""
    if activity not in {"all", *ACTIVITIES}:
        raise ValueError("activity must be all, manufacturing, or reaction")
    if sample_limit < 1:
        raise ValueError("sample_limit must be >= 1")
    if not input_path.is_file():
        raise FileNotFoundError(f"Recipe file does not exist: {input_path}")

    source_bytes = input_path.read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    skill_stats: dict[int, dict[str, Any]] = {}
    recipe_counts: Counter[str] = Counter()
    eligible_counts: Counter[str] = Counter()
    exclusion_counts: Counter[str] = Counter()
    exclusion_samples: list[dict[str, Any]] = []
    skill_reference_count = 0
    recipes_with_missing_skill_arrays = 0
    recipes_with_unpublished_skill_requirements = 0
    recipes_with_unknown_skill_metadata = 0
    selected_recipe_count = 0
    eligible_recipes: list[dict[str, Any]] = []

    for recipe in _parse_jsonl(source_bytes, input_path):
        recipe_activity = recipe.get("activity")
        if recipe_activity not in ACTIVITIES:
            continue
        if activity != "all" and recipe_activity != activity:
            continue

        selected_recipe_count += 1
        recipe_counts[recipe_activity] += 1
        states = recipe.get("source_field_state")
        if not isinstance(states, dict):
            states = {}

        raw_skills = recipe.get("required_skills")
        skills_state = states.get("required_skills")
        skill_rows: list[dict[str, Any]] = []
        skill_metadata_complete = (
            skills_state in VALID_ARRAY_STATES and isinstance(raw_skills, list)
        )
        if (
            (skills_state == "empty" and isinstance(raw_skills, list) and raw_skills)
            or (skills_state == "present" and isinstance(raw_skills, list) and not raw_skills)
        ):
            skill_metadata_complete = False
        unpublished_skill = False
        unknown_skill_metadata = False
        seen_skill_ids: set[int] = set()

        if not skill_metadata_complete:
            recipes_with_missing_skill_arrays += 1

        if isinstance(raw_skills, list):
            for item in raw_skills:
                if not isinstance(item, dict):
                    skill_metadata_complete = False
                    unknown_skill_metadata = True
                    continue
                type_id = item.get("type_id")
                if not _positive_int(type_id):
                    skill_metadata_complete = False
                    unknown_skill_metadata = True
                    continue

                stat = skill_stats.setdefault(type_id, _new_skill_stat(type_id))
                skill_reference_count += 1
                stat["source_reference_count"] += 1
                if _name(item.get("name")):
                    stat["names"].add(item["name"].strip())
                status = _publication(item.get("published"))
                stat["publication_states"].add(status)

                valid_level = _level(item.get("level"))
                if valid_level:
                    stat["source_level_counts"][str(item["level"])] += 1
                else:
                    skill_metadata_complete = False
                    unknown_skill_metadata = True

                stat["source_recipe_keys"].add(
                    (recipe.get("blueprint_type_id"), recipe_activity)
                )
                stat["source_activity_counts"][recipe_activity] += 0

                if not _name(item.get("name")) or not isinstance(item.get("published"), bool):
                    skill_metadata_complete = False
                    unknown_skill_metadata = True

                if status == "unpublished":
                    unpublished_skill = True

                if type_id in seen_skill_ids:
                    skill_metadata_complete = False
                    unknown_skill_metadata = True
                seen_skill_ids.add(type_id)

                if valid_level:
                    skill_rows.append({
                        "type_id": type_id,
                        "name": item.get("name"),
                        "required_level": item["level"],
                        "published": item.get("published"),
                    })

        # A source record may not provide a key; keep it out of candidate
        # aggregation rather than conflating different unidentified recipes.
        recipe_key = (recipe.get("blueprint_type_id"), recipe_activity)
        if skill_metadata_complete:
            for type_id in seen_skill_ids:
                stat = skill_stats[type_id]
                stat["source_activity_counts"][recipe_activity] += 1

        if unpublished_skill:
            recipes_with_unpublished_skill_requirements += 1
        if unknown_skill_metadata:
            recipes_with_unknown_skill_metadata += 1

        reasons: list[str] = []

        # Recipe material/product arrays must be explicitly present or empty.
        if (
            recipe.get("recipe_data_status") != "complete"
            or states.get("materials") not in VALID_ARRAY_STATES
            or states.get("products") != "present"
            or not isinstance(recipe.get("materials"), list)
            or not isinstance(recipe.get("products"), list)
        ):
            reasons.append("incomplete_recipe_data")

        if recipe.get("blueprint_published") is False:
            reasons.append("unpublished_blueprint")
        elif recipe.get("blueprint_published") is not True:
            reasons.append("unknown_blueprint_publication")
        if not _positive_int(recipe.get("blueprint_type_id")) or not _name(recipe.get("blueprint_name")):
            reasons.append("unresolved_blueprint_metadata")

        base_time = recipe.get("base_time_seconds_per_run")
        if not isinstance(base_time, int) or isinstance(base_time, bool) or base_time <= 0:
            reasons.append("zero_or_invalid_base_time")

        materials = recipe.get("materials")
        if isinstance(materials, list):
            for material in materials:
                if (
                    not isinstance(material, dict)
                    or not _positive_int(material.get("type_id"))
                    or not _positive_int(material.get("quantity_per_run"))
                    or not _name(material.get("name"))
                ):
                    reasons.append("unresolved_material_metadata")
                    break

        products = recipe.get("products")
        published_products: list[dict[str, Any]] = []
        if isinstance(products, list):
            for product in products:
                if not isinstance(product, dict):
                    continue
                if (
                    product.get("published") is True
                    and _positive_int(product.get("type_id"))
                    and _positive_int(product.get("quantity_per_run"))
                    and _name(product.get("name"))
                ):
                    published_products.append({
                        "type_id": product["type_id"],
                        "name": product["name"].strip(),
                        "quantity_per_run": product.get("quantity_per_run"),
                    })
        if not published_products:
            reasons.append("no_published_resolvable_output")

        if not skill_metadata_complete:
            reasons.append("skill_requirements_unavailable_or_incomplete")
        if unpublished_skill:
            reasons.append("unpublished_required_skill")
        if unknown_skill_metadata:
            reasons.append("unknown_required_skill_metadata")

        # An explicit empty skills array is valid; it means the SDE lists no
        # additional skill requirement for this activity. Omitted/null is not
        # interpreted as an empty list.
        if not isinstance(raw_skills, list) or skills_state not in VALID_ARRAY_STATES:
            reasons.append("skill_requirements_unavailable_or_incomplete")

        if reasons:
            for reason in set(reasons):
                exclusion_counts[reason] += 1
            _add_sample(
                exclusion_samples,
                {
                    **_recipe_label(recipe),
                    "reason_codes": sorted(set(reasons)),
                },
                sample_limit,
            )
            continue

        # At this point the recipe is suitable for skill-reference mapping:
        # it is complete, published, positively timed, and has resolved inputs,
        # at least one published output, and known published skill requirements.
        eligible_counts[recipe_activity] += 1
        recipe_skills = sorted(skill_rows, key=lambda row: row["type_id"])
        for skill in recipe_skills:
            stat = skill_stats[skill["type_id"]]
            stat["candidate_recipe_keys"].add(recipe_key)
            stat["candidate_activity_counts"][recipe_activity] += 1
            stat["candidate_level_counts"][str(skill["required_level"])] += 1
            _add_sample(
                stat["sample_candidate_recipes"],
                {
                    **_recipe_label(recipe),
                    "product_names": sorted({p["name"] for p in published_products}),
                },
                sample_limit,
            )

        eligible_recipes.append({
            **_recipe_label(recipe),
            "base_time_seconds_per_run": base_time,
            "published_outputs": published_products,
            "required_skills": recipe_skills,
            "unpublished_or_unresolved_secondary_output_count": (
                len(products) - len(published_products) if isinstance(products, list) else 0
            ),
        })

    skill_records = []
    for type_id, stat in skill_stats.items():
        statuses = stat["publication_states"]
        publication_status = next(iter(statuses)) if len(statuses) == 1 else (
            "unknown" if not statuses else "inconsistent"
        )
        names = sorted(stat["names"])
        skill_records.append({
            "type_id": type_id,
            "name": names[0] if len(names) == 1 else (names[0] if names else None),
            "name_conflict": len(names) > 1,
            "publication_status": publication_status,
            "source_recipe_count": len(stat["source_recipe_keys"]),
            "source_reference_count": stat["source_reference_count"],
            "candidate_recipe_count": len(stat["candidate_recipe_keys"]),
            "source_activity_recipe_counts": dict(sorted(stat["source_activity_counts"].items())),
            "candidate_activity_recipe_counts": dict(sorted(stat["candidate_activity_counts"].items())),
            "source_required_level_counts": dict(sorted(stat["source_level_counts"].items())),
            "candidate_required_level_counts": dict(sorted(stat["candidate_level_counts"].items())),
            "max_candidate_required_level": max(
                (int(level) for level in stat["candidate_level_counts"]), default=None
            ),
            "sample_candidate_recipes": stat["sample_candidate_recipes"],
        })

    skill_records.sort(
        key=lambda row: (
            -row["candidate_recipe_count"],
            -row["source_recipe_count"],
            row["publication_status"] != "published",
            (row["name"] or "").casefold(),
            row["type_id"],
        )
    )

    profile_capture_skills = [
        {
            "type_id": row["type_id"],
            "name": row["name"],
            "candidate_recipe_count": row["candidate_recipe_count"],
            "candidate_activity_recipe_counts": row["candidate_activity_recipe_counts"],
            "candidate_required_level_counts": row["candidate_required_level_counts"],
            "max_candidate_required_level": row["max_candidate_required_level"],
        }
        for row in skill_records
        if row["publication_status"] == "published" and row["candidate_recipe_count"] > 0
    ]

    unpublished_skill_exceptions = [
        {
            "type_id": row["type_id"],
            "name": row["name"],
            "source_recipe_count": row["source_recipe_count"],
            "candidate_recipe_count": row["candidate_recipe_count"],
        }
        for row in skill_records
        if row["publication_status"] == "unpublished"
    ]

    total_eligible = sum(eligible_counts.values())
    total_excluded = sum(exclusion_counts.values())
    return {
        "report_version": 1,
        "source_file": input_path.name,
        "source_sha256": source_hash,
        "activity_filter": activity,
        "selection_rule": (
            "Skill-reference candidates must have an explicitly complete material/product recipe; "
            "a published, named blueprint; positive base time; valid named material inputs; at least "
            "one named published product output; and an explicitly present/empty required-skill array "
            "whose skill names, levels, and publication flags are known and published. This is a "
            "static-data filter only, not a marketability or operating-feasibility determination."
        ),
        "summary": {
            "source_recipe_count": selected_recipe_count,
            "source_recipe_counts_by_activity": dict(sorted(recipe_counts.items())),
            "eligible_recipe_count": total_eligible,
            "eligible_recipe_counts_by_activity": dict(sorted(eligible_counts.items())),
            "unique_skill_type_id_count": len(skill_records),
            "profile_capture_skill_count": len(profile_capture_skills),
            "unpublished_skill_type_id_count": len(unpublished_skill_exceptions),
            "unpublished_skill_reference_count": sum(
                stat["source_reference_count"] for stat in skill_stats.values()
                if stat["publication_states"] == {"unpublished"}
            ),
            "recipes_with_missing_skill_arrays": recipes_with_missing_skill_arrays,
            "recipes_with_unpublished_skill_requirements": recipes_with_unpublished_skill_requirements,
            "recipes_with_unknown_skill_metadata": recipes_with_unknown_skill_metadata,
            "excluded_recipe_count_with_one_or_more_reasons": selected_recipe_count - total_eligible,
            "exclusion_reason_counts_overlap": True,
            "exclusion_reason_counts": dict(sorted(exclusion_counts.items())),
        },
        "profile_capture_skills": profile_capture_skills,
        "all_observed_skill_types": skill_records,
        "unpublished_skill_exceptions": unpublished_skill_exceptions,
        "eligible_recipes": sorted(
            eligible_recipes,
            key=lambda row: (row["activity"], (row["blueprint_name"] or "").casefold(), row["blueprint_type_id"]),
        ),
        "excluded_recipe_samples": exclusion_samples,
        "privacy": {
            "contains_character_names_or_ids": False,
            "contains_character_skills_or_levels": False,
            "contains_blueprint_inventory": False,
            "contains_wallet_or_market_location_data": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Normalized local recipe JSONL")
    parser.add_argument("--output", type=Path, required=True, help="Local JSON reference output")
    parser.add_argument("--activity", choices=("all", *ACTIVITIES), default="all")
    parser.add_argument("--sample-limit", type=int, default=10)
    args = parser.parse_args()

    try:
        report = build_skill_reference(args.input, args.activity, args.sample_limit)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    summary = report["summary"]
    print(f"PASS: wrote local skill reference to {args.output}")
    print(f"Source recipes: {summary['source_recipe_count']:,}")
    print(f"Eligible skill-reference recipes: {summary['eligible_recipe_count']:,}")
    print(f"Unique observed skill types: {summary['unique_skill_type_id_count']:,}")
    print(f"Skills to capture in the local profile: {summary['profile_capture_skill_count']:,}")
    print(
        "Excluded recipes with one or more reasons: "
        f"{summary['excluded_recipe_count_with_one_or_more_reasons']:,}"
    )
    print("The output is not a marketability, character-feasibility, or profitability report.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
