#!/usr/bin/env python3
"""Evaluate one manufacturing product using SDE recipe data and explicit live quotes.

The SDE provides the recipe reference and unmodified per-run quantities. Actual
job material quantities, job durations, and installation fees must come from
the in-game Industry quote. Market prices, fills, and fee amounts are supplied
as observed data or clearly labeled scenarios. This tool does not invent
ME/facility rounding or predict market execution.
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from manufacturing_profitability import calculate as calculate_profitability

ZERO = Decimal("0")
ONE = Decimal("1")


def _required(data: dict[str, Any], key: str, label: str | None = None) -> Any:
    if key not in data:
        raise ValueError(f"Missing required input: {label or key}")
    return data[key]


def _decimal(value: Any, label: str) -> Decimal:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be a decimal number")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{label} must be a decimal number") from None
    if not result.is_finite():
        raise ValueError(f"{label} must be finite")
    return result


def _nonnegative(value: Any, label: str) -> Decimal:
    result = _decimal(value, label)
    if result < ZERO:
        raise ValueError(f"{label} must be >= 0")
    return result


def _positive(value: Any, label: str) -> Decimal:
    result = _decimal(value, label)
    if result <= ZERO:
        raise ValueError(f"{label} must be > 0")
    return result


def _positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{label} must be a positive integer")
    return value


def _load_recipe(
    recipe_file: Path,
    *,
    activity: str,
    blueprint_type_id: int,
    product_type_id: int,
) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    if not recipe_file.is_file():
        raise FileNotFoundError(f"Recipe file does not exist: {recipe_file}")

    matches: list[dict[str, Any]] = []
    with recipe_file.open("r", encoding="utf-8-sig") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"{recipe_file}:{line_number}: invalid JSON: {exc}"
                ) from exc
            if not isinstance(record, dict):
                raise ValueError(f"{recipe_file}:{line_number}: recipe must be an object")
            if (
                record.get("activity") == activity
                and record.get("blueprint_type_id") == blueprint_type_id
            ):
                matches.append(record)

    if not matches:
        raise ValueError(
            f"No {activity} recipe found for blueprint type ID {blueprint_type_id}"
        )
    if len(matches) != 1:
        raise ValueError(
            f"Found {len(matches)} matching recipes for blueprint type ID {blueprint_type_id}; "
            "the SDE recipe key is ambiguous"
        )

    recipe = matches[0]
    source_state = recipe.get("source_field_state")
    if recipe.get("recipe_data_status") != "complete":
        raise ValueError(
            "The selected SDE recipe is incomplete; do not cost omitted/null material arrays"
        )
    if not isinstance(source_state, dict):
        raise ValueError("The selected SDE recipe lacks source-field completeness metadata")
    if source_state.get("materials") not in {"present", "empty"}:
        raise ValueError("The selected SDE recipe has no complete material array")
    if source_state.get("products") != "present":
        raise ValueError("The selected SDE recipe has no complete product array")

    products = recipe.get("products")
    materials = recipe.get("materials")
    if not isinstance(products, list) or not isinstance(materials, list):
        raise ValueError("The selected SDE recipe has invalid products/materials arrays")

    product_matches = [
        item for item in products
        if isinstance(item, dict) and item.get("type_id") == product_type_id
    ]
    if len(product_matches) != 1:
        raise ValueError(
            f"Product type ID {product_type_id} must appear exactly once in the selected recipe"
        )
    product = product_matches[0]

    warnings: list[str] = []
    if recipe.get("blueprint_published") is False:
        raise ValueError("The selected blueprint is unpublished in the SDE")
    if product.get("published") is False:
        raise ValueError("The selected output product is unpublished in the SDE")
    if recipe.get("blueprint_published") is None:
        warnings.append("Blueprint publication status is unknown in the SDE metadata.")
    if product.get("published") is None:
        warnings.append("Output product publication status is unknown in the SDE metadata.")
    if source_state.get("required_skills") in {"omitted", "null"}:
        warnings.append(
            "The SDE recipe's required-skill array is omitted/null; character feasibility remains unknown."
        )
    return recipe, product, warnings


def evaluate(config: dict[str, Any]) -> dict[str, Any]:
    candidate = _required(config, "candidate")
    activity = _required(candidate, "activity")
    if activity != "manufacturing":
        raise ValueError("Product evaluator v1 currently supports manufacturing recipes only")

    blueprint_type_id = _positive_int(
        _required(candidate, "blueprint_type_id"), "candidate.blueprint_type_id"
    )
    product_type_id = _positive_int(
        _required(candidate, "product_type_id"), "candidate.product_type_id"
    )
    runs = _positive_int(_required(candidate, "runs"), "candidate.runs")
    recipe_file = Path(_required(config, "recipe_file"))
    recipe, product, warnings = _load_recipe(
        recipe_file,
        activity=activity,
        blueprint_type_id=blueprint_type_id,
        product_type_id=product_type_id,
    )

    blueprint = _required(config, "blueprint")
    blueprint_kind = _required(blueprint, "kind")
    if blueprint_kind not in {"BPO", "BPC"}:
        raise ValueError("blueprint.kind must be BPO or BPC")
    blueprint_quantity = _positive_int(
        _required(blueprint, "quantity"), "blueprint.quantity"
    )
    for field in ("material_efficiency", "time_efficiency", "licensed_runs"):
        value = blueprint.get(field)
        if value is not None:
            _nonnegative(value, f"blueprint.{field}")

    if blueprint_kind == "BPC":
        licensed_runs = blueprint.get("licensed_runs")
        if licensed_runs is None:
            warnings.append("BPC licensed runs are unknown; confirm the copy supports the planned runs.")
        elif runs > _positive_int(licensed_runs, "blueprint.licensed_runs") * blueprint_quantity:
            raise ValueError("Planned runs exceed the total licensed runs in the recorded BPC inventory.")
    if blueprint_quantity < 1:
        raise ValueError("At least one blueprint copy must be recorded.")

    quote = _required(config, "industry_quote")
    quote_source = _required(quote, "source")
    if not isinstance(quote_source, str) or not quote_source.strip():
        raise ValueError("industry_quote.source must be a non-empty string")
    if quote_source != "in_game_industry_window":
        warnings.append(
            "Industry quote source is not identified as the in-game Industry window; verify material quantities, duration, and installation fee."
        )

    jobs = _required(quote, "jobs")
    if not isinstance(jobs, list) or not jobs:
        raise ValueError("industry_quote.jobs must contain at least one quoted job")
    job_runs = 0
    slot_seconds = ZERO
    max_per_job = recipe.get("max_production_limit")
    for index, job in enumerate(jobs):
        if not isinstance(job, dict):
            raise ValueError(f"industry_quote.jobs[{index}] must be an object")
        job_run_count = _positive_int(
            _required(job, "runs", f"industry_quote.jobs[{index}].runs"),
            f"industry_quote.jobs[{index}].runs",
        )
        duration = _positive(
            _required(job, "duration_seconds", f"industry_quote.jobs[{index}].duration_seconds"),
            f"industry_quote.jobs[{index}].duration_seconds",
        )
        if isinstance(max_per_job, int) and max_per_job > 0 and job_run_count > max_per_job:
            raise ValueError(
                f"Job {index + 1} exceeds the SDE maximum production limit of {max_per_job} runs"
            )
        job_runs += job_run_count
        slot_seconds += duration
    if job_runs != runs:
        raise ValueError(
            f"Quoted job runs total {job_runs}, but candidate.runs is {runs}"
        )
    if len(jobs) > blueprint_quantity:
        warnings.append(
            "Quoted job count exceeds the number of blueprint copies recorded. Confirm jobs are not relying on simultaneous use of the same copy."
        )

    product_units_per_run = _positive_int(
        product.get("quantity_per_run"), "SDE product.quantity_per_run"
    )
    expected_output_units = product_units_per_run * runs
    quoted_output_units = _positive_int(
        _required(quote, "output_units"), "industry_quote.output_units"
    )
    if quoted_output_units != expected_output_units:
        raise ValueError(
            f"Industry quote output ({quoted_output_units}) does not match SDE product yield "
            f"({product_units_per_run} per run x {runs} runs = {expected_output_units})"
        )

    if quote.get("materials_complete") is not True:
        raise ValueError(
            "industry_quote.materials_complete must be true before a complete batch cost can be calculated"
        )
    quoted_materials = _required(quote, "materials")
    if not isinstance(quoted_materials, list):
        raise ValueError("industry_quote.materials must be a list")

    recipe_materials = {
        _positive_int(item.get("type_id"), "SDE material.type_id"): item
        for item in recipe["materials"]
        if isinstance(item, dict)
    }
    recipe_material_names = {
        type_id: item.get("name") for type_id, item in recipe_materials.items()
    }
    material_ids_seen: set[int] = set()
    calc_materials: list[dict[str, Any]] = []
    quoted_quantities: dict[int, Decimal] = {}
    for index, line in enumerate(quoted_materials):
        if not isinstance(line, dict):
            raise ValueError(f"industry_quote.materials[{index}] must be an object")
        type_id = _positive_int(
            _required(line, "type_id", f"industry_quote.materials[{index}].type_id"),
            f"industry_quote.materials[{index}].type_id",
        )
        if type_id in material_ids_seen:
            raise ValueError(f"Duplicate quoted material type ID: {type_id}")
        material_ids_seen.add(type_id)
        quantity = _positive(
            _required(line, "quantity", f"industry_quote.materials[{index}].quantity"),
            f"industry_quote.materials[{index}].quantity",
        )
        unit_value = _nonnegative(
            _required(line, "unit_value_isk", f"industry_quote.materials[{index}].unit_value_isk"),
            f"industry_quote.materials[{index}].unit_value_isk",
        )
        basis = _required(line, "valuation_basis", f"industry_quote.materials[{index}].valuation_basis")
        if not isinstance(basis, str) or not basis.strip():
            raise ValueError(f"industry_quote.materials[{index}].valuation_basis must be a non-empty string")
        name = line.get("name") or recipe_material_names.get(type_id) or f"type_id_{type_id}"
        quoted_quantities[type_id] = quantity
        calc_materials.append({
            "name": str(name),
            "quantity": str(quantity),
            "unit_value_isk": str(unit_value),
            "valuation_basis": basis,
            "source_timestamp": line.get("source_timestamp"),
            "location": line.get("location"),
        })

    expected_base_quantities: dict[int, Decimal] = {
        type_id: Decimal(item["quantity_per_run"]) * Decimal(runs)
        for type_id, item in recipe_materials.items()
    }
    missing_from_quote = sorted(set(expected_base_quantities) - set(quoted_quantities))
    additional_to_recipe = sorted(set(quoted_quantities) - set(expected_base_quantities))
    if missing_from_quote:
        warnings.append(
            "These SDE base-input types are absent from the complete Industry quote. They may have rounded to zero under job modifiers, but confirm the displayed bill: "
            + ", ".join(map(str, missing_from_quote))
        )
    if additional_to_recipe:
        warnings.append(
            "The Industry quote contains material IDs not listed in the SDE recipe; confirm whether these are job-specific additions: "
            + ", ".join(map(str, additional_to_recipe))
        )

    material_comparison = []
    for type_id in sorted(set(expected_base_quantities) | set(quoted_quantities)):
        base_quantity = expected_base_quantities.get(type_id, ZERO)
        quote_quantity = quoted_quantities.get(type_id, ZERO)
        material_comparison.append({
            "type_id": type_id,
            "name": recipe_material_names.get(type_id),
            "sde_base_quantity_for_runs": str(base_quantity),
            "industry_quote_quantity": str(quote_quantity),
            "difference_from_sde_base": str(quote_quantity - base_quantity),
        })

    installation_fee = _nonnegative(
        _required(quote, "installation_fee_isk"), "industry_quote.installation_fee_isk"
    )
    elapsed_hours = _positive(
        _required(quote, "elapsed_critical_path_hours"),
        "industry_quote.elapsed_critical_path_hours",
    )
    slot_hours = slot_seconds / Decimal(3600)

    operating = _required(config, "operating")
    capital_deployed = _nonnegative(
        _required(operating, "capital_deployed_isk"), "operating.capital_deployed_isk"
    )
    active_hours_value = operating.get("active_operator_hours")
    active_time_basis = operating.get("active_time_basis", "unknown")
    if active_time_basis not in {"unknown", "estimated", "measured"}:
        raise ValueError("operating.active_time_basis must be unknown, estimated, or measured")
    active_hours: Decimal | None = None
    if active_hours_value is not None:
        active_hours = _nonnegative(active_hours_value, "operating.active_operator_hours")
        if active_hours > ZERO and active_time_basis == "unknown":
            raise ValueError(
                "Set active_time_basis to estimated or measured when active_operator_hours is supplied"
            )
    elif active_time_basis != "unknown":
        raise ValueError("active_time_basis must be unknown when active_operator_hours is omitted")

    costs = config.get("other_batch_costs", {})
    if not isinstance(costs, dict):
        raise ValueError("other_batch_costs must be an object")
    other_costs = {
        "installation_fees_isk": str(installation_fee),
        "allocated_upstream_costs_isk": str(_nonnegative(costs.get("allocated_upstream_costs_isk", 0), "allocated_upstream_costs_isk")),
        "logistics_and_handling_isk": str(_nonnegative(costs.get("logistics_and_handling_isk", 0), "logistics_and_handling_isk")),
        "other_variable_costs_isk": str(_nonnegative(costs.get("other_variable_costs_isk", 0), "other_variable_costs_isk")),
    }

    production = {
        "delivered_output_units": str(quoted_output_units),
        "capital_deployed_isk": str(capital_deployed),
        "manufacturing_slot_hours": str(slot_hours),
        "elapsed_critical_path_hours": str(elapsed_hours),
    }
    if active_hours is not None:
        production["active_operator_hours"] = str(active_hours)

    scenarios = _required(config, "sale_scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("sale_scenarios must contain at least one strategy")
    scenario_names: set[str] = set()
    evaluated_scenarios = []
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            raise ValueError(f"sale_scenarios[{index}] must be an object")
        name = _required(scenario, "name", f"sale_scenarios[{index}].name")
        if not isinstance(name, str) or not name.strip() or name in scenario_names:
            raise ValueError("Sale scenario names must be non-empty and unique")
        scenario_names.add(name)
        evidence_basis = _required(
            scenario, "evidence_basis", f"sale_scenarios[{index}].evidence_basis"
        )
        if evidence_basis not in {
            "actual_fills", "v4_order_book_estimate", "manual_scenario", "synthetic_fixture"
        }:
            raise ValueError(f"sale_scenarios[{index}].evidence_basis is invalid")
        sale = _required(scenario, "sale", f"sale_scenarios[{index}].sale")
        projection = _required(
            scenario, "full_batch_projection", f"sale_scenarios[{index}].full_batch_projection"
        )
        calc_config = {
            "production": production,
            "materials": calc_materials,
            "other_batch_costs": other_costs,
            "sale": sale,
            "full_batch_projection": projection,
        }
        result = calculate_profitability(calc_config)
        evaluated_scenarios.append({
            "name": name,
            "evidence_basis": evidence_basis,
            "source_timestamp": scenario.get("source_timestamp"),
            "source_location": scenario.get("source_location"),
            "risk_notes": scenario.get("risk_notes", []),
            "calculation": result,
        })

    if not recipe_materials:
        warnings.append("The SDE recipe has an explicitly empty material list; verify that this activity is truly zero-input.")
    if not quote.get("quoted_at"):
        warnings.append("The Industry quote timestamp is missing; freshness cannot be assessed.")
    if quote_source != "in_game_industry_window":
        warnings.append("Do not treat the supplied job quote values as independently verified game output.")
    warnings.append(
        "SDE material quantities are unmodified base quantities per run. The quote's actual bill is used for costing; differences are shown for review, not recalculated by this tool."
    )
    warnings.append(
        "Market fees, prices, and fills are explicit scenario inputs. This tool does not fetch markets or guarantee execution."
    )
    warnings.append(
        "No risk premium is applied. Review the supplied risk notes and scenarios separately."
    )

    return {
        "schema_version": 1,
        "candidate": {
            "activity": activity,
            "product_type_id": product_type_id,
            "product_name": product.get("name") or f"type_id_{product_type_id}",
            "blueprint_type_id": blueprint_type_id,
            "blueprint_name": recipe.get("blueprint_name"),
            "runs": runs,
            "output_units": quoted_output_units,
        },
        "source": {
            "recipe_file": str(recipe_file),
            "sde_build": config.get("sde_build"),
            "recipe_schema_version": recipe.get("schema_version"),
        },
        "blueprint": blueprint,
        "sde_recipe_reference": {
            "blueprint_published": recipe.get("blueprint_published"),
            "product_published": product.get("published"),
            "base_time_seconds_per_run": recipe.get("base_time_seconds_per_run"),
            "max_production_limit": recipe.get("max_production_limit"),
            "materials": [
                {
                    "type_id": item["type_id"],
                    "name": item.get("name"),
                    "quantity_per_run": item["quantity_per_run"],
                }
                for item in recipe_materials.values()
            ],
            "products": recipe.get("products", []),
            "required_skills": recipe.get("required_skills", []),
            "source_field_state": recipe.get("source_field_state"),
        },
        "industry_quote": {
            "source": quote_source,
            "quoted_at": quote.get("quoted_at"),
            "character_slot": quote.get("character_slot"),
            "facility_label": quote.get("facility_label"),
            "system_id": quote.get("system_id"),
            "job_count": len(jobs),
            "manufacturing_slot_hours": str(slot_hours),
            "elapsed_critical_path_hours": str(elapsed_hours),
            "installation_fee_isk": str(installation_fee),
            "material_comparison": material_comparison,
            "missing_from_quote_type_ids": missing_from_quote,
            "additional_to_sde_type_ids": additional_to_recipe,
        },
        "operating": {
            "capital_deployed_isk": str(capital_deployed),
            "active_operator_hours": str(active_hours) if active_hours is not None else None,
            "active_time_basis": active_time_basis,
        },
        "sale_scenarios": evaluated_scenarios,
        "warnings": warnings,
        "decision": {
            "initial_efficiency_metric": "unadjusted_net_contribution_per_active_operator_hour",
            "risk_adjustment_applied": False,
            "status": "requires_human_review",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True, help="Product-evaluation input JSON")
    parser.add_argument("--output", type=Path, help="Optional report path; stdout when omitted")
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        report = evaluate(config)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"PASS: wrote product evaluation to {args.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
