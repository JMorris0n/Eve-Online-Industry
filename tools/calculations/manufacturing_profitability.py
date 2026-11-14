#!/usr/bin/env python3
"""Calculate batch-level EVE manufacturing profitability from a JSON scenario.

This is a deterministic accounting model. It does not fetch market data,
predict fills, calculate live industry quotes, or infer blueprint recipes.
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any

ZERO = Decimal("0")
ONE = Decimal("1")
CENT = Decimal("0.01")


def decimal_value(value: Any, label: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{label} must be a decimal number") from None
    if not result.is_finite():
        raise ValueError(f"{label} must be finite")
    return result


def required(mapping: dict[str, Any], key: str) -> Any:
    if key not in mapping:
        raise ValueError(f"Missing required input: {key}")
    return mapping[key]


def nonnegative(value: Any, label: str) -> Decimal:
    result = decimal_value(value, label)
    if result < ZERO:
        raise ValueError(f"{label} must be >= 0")
    return result


def positive(value: Any, label: str) -> Decimal:
    result = decimal_value(value, label)
    if result <= ZERO:
        raise ValueError(f"{label} must be > 0")
    return result


def rate(value: Any, label: str) -> Decimal:
    result = decimal_value(value, label)
    if result < ZERO or result > ONE:
        raise ValueError(f"{label} must be between 0 and 1")
    return result


def fmt(value: Decimal) -> str:
    return str(value.quantize(CENT, rounding=ROUND_HALF_UP))


def fmt_decimal(value: Decimal) -> str:
    return str(value.normalize()) if value else "0"


def calculate(config: dict[str, Any]) -> dict[str, Any]:
    plan = required(config, "production")
    output_units = positive(required(plan, "delivered_output_units"), "delivered_output_units")
    capital = nonnegative(required(plan, "capital_deployed_isk"), "capital_deployed_isk")
    slot_hours = nonnegative(required(plan, "manufacturing_slot_hours"), "manufacturing_slot_hours")
    elapsed_hours = nonnegative(required(plan, "elapsed_critical_path_hours"), "elapsed_critical_path_hours")

    materials = required(config, "materials")
    if not isinstance(materials, list):
        raise ValueError("materials must be a list")
    material_total = ZERO
    material_detail = []
    material_quantities: dict[str, Decimal] = {}
    for index, line in enumerate(materials):
        label = str(line.get("name", f"material_{index + 1}"))
        quantity = nonnegative(required(line, "quantity"), f"{label}.quantity")
        unit_value = nonnegative(required(line, "unit_value_isk"), f"{label}.unit_value_isk")
        line_cost = quantity * unit_value
        material_total += line_cost
        material_quantities[label] = material_quantities.get(label, ZERO) + quantity
        material_detail.append({
            "name": label,
            "quantity": fmt_decimal(quantity),
            "unit_value_isk": fmt(unit_value),
            "economic_cost_isk": fmt(line_cost),
            "valuation_basis": str(line.get("valuation_basis", "unspecified")),
            "source_timestamp": line.get("source_timestamp"),
            "location": line.get("location"),
        })

    other = required(config, "other_batch_costs")
    installation = nonnegative(required(other, "installation_fees_isk"), "installation_fees_isk")
    upstream = nonnegative(required(other, "allocated_upstream_costs_isk"), "allocated_upstream_costs_isk")
    logistics = nonnegative(required(other, "logistics_and_handling_isk"), "logistics_and_handling_isk")
    other_batch = nonnegative(required(other, "other_variable_costs_isk"), "other_variable_costs_isk")
    batch_cost = material_total + installation + upstream + logistics + other_batch

    sale = required(config, "sale")
    tax_rate = rate(required(sale, "sales_tax_rate"), "sales_tax_rate")
    fills = required(sale, "fills")
    if not isinstance(fills, list):
        raise ValueError("sale.fills must be a list")
    sold_units = ZERO
    gross = ZERO
    fill_detail = []
    for index, fill in enumerate(fills):
        quantity = positive(required(fill, "quantity"), f"sale.fills[{index}].quantity")
        price = nonnegative(required(fill, "unit_price_isk"), f"sale.fills[{index}].unit_price_isk")
        sold_units += quantity
        gross += quantity * price
        fill_detail.append({
            "quantity": fmt_decimal(quantity),
            "unit_price_isk": fmt(price),
            "gross_value_isk": fmt(quantity * price),
        })
    if sold_units > output_units:
        raise ValueError("Total sold quantity cannot exceed delivered output units")

    broker_fees = nonnegative(required(sale, "broker_fees_isk"), "broker_fees_isk")
    relist_fees = nonnegative(required(sale, "relist_fees_isk"), "relist_fees_isk")
    other_sale = nonnegative(required(sale, "other_sale_costs_isk"), "other_sale_costs_isk")
    sales_tax = gross * tax_rate
    net_proceeds = gross - sales_tax - broker_fees - relist_fees - other_sale
    allocated_sold_cost = batch_cost * sold_units / output_units if sold_units else ZERO
    realized_contribution = net_proceeds - allocated_sold_cost
    unsold_units = output_units - sold_units
    unsold_inventory_cost = batch_cost - allocated_sold_cost

    projection = required(config, "full_batch_projection")
    projected_price = nonnegative(
        required(projection, "unit_sale_price_isk"), "projection.unit_sale_price_isk"
    )
    projected_tax_rate = rate(
        required(projection, "sales_tax_rate"), "projection.sales_tax_rate"
    )
    projected_broker = nonnegative(
        required(projection, "broker_fees_isk"), "projection.broker_fees_isk"
    )
    projected_relist = nonnegative(
        required(projection, "relist_fees_isk"), "projection.relist_fees_isk"
    )
    projected_other_sale = nonnegative(
        required(projection, "other_sale_costs_isk"), "projection.other_sale_costs_isk"
    )
    projected_gross = output_units * projected_price
    projected_tax = projected_gross * projected_tax_rate
    projected_net = (
        projected_gross - projected_tax - projected_broker
        - projected_relist - projected_other_sale
    )
    projected_contribution = projected_net - batch_cost

    projected_fixed_fees = projected_broker + projected_relist + projected_other_sale
    break_even_denominator = output_units * (ONE - projected_tax_rate)
    break_even_price = (
        (batch_cost + projected_fixed_fees) / break_even_denominator
        if break_even_denominator > ZERO else None
    )

    target_margin = rate(
        required(projection, "target_net_margin_rate"),
        "projection.target_net_margin_rate",
    )
    target_denominator = output_units * (ONE - projected_tax_rate - target_margin)
    target_price = (
        (batch_cost + projected_fixed_fees) / target_denominator
        if target_denominator > ZERO else None
    )

    target_material = projection.get("target_material_for_max_price")
    max_input_value = None
    if target_material is not None:
        if target_material not in material_quantities:
            raise ValueError(f"Target material {target_material!r} not found in materials")
        target_qty = material_quantities[target_material]
        if target_qty <= ZERO:
            raise ValueError("Target material quantity must be > 0")
        target_line_cost = sum(
            (nonnegative(line["quantity"], "quantity") * nonnegative(line["unit_value_isk"], "unit_value_isk")
             for line in materials if str(line.get("name", "")) == target_material),
            ZERO,
        )
        non_target_cost = batch_cost - target_line_cost
        affordable_total = projected_net - non_target_cost
        max_input_value = {
            "material": target_material,
            "required_quantity": fmt_decimal(target_qty),
            "maximum_unit_value_isk": fmt(affordable_total / target_qty),
        }

    return {
        "inputs": config,
        "material_costs": {
            "lines": material_detail,
            "total_isk": fmt(material_total),
        },
        "batch_costs": {
            "materials_isk": fmt(material_total),
            "installation_fees_isk": fmt(installation),
            "allocated_upstream_costs_isk": fmt(upstream),
            "logistics_and_handling_isk": fmt(logistics),
            "other_variable_costs_isk": fmt(other_batch),
            "economic_batch_cost_isk": fmt(batch_cost),
        },
        "realized_sales": {
            "sold_units": fmt_decimal(sold_units),
            "unsold_units": fmt_decimal(unsold_units),
            "fills": fill_detail,
            "gross_sale_value_isk": fmt(gross),
            "sales_tax_isk": fmt(sales_tax),
            "broker_fees_isk": fmt(broker_fees),
            "relist_fees_isk": fmt(relist_fees),
            "other_sale_costs_isk": fmt(other_sale),
            "net_sale_proceeds_isk": fmt(net_proceeds),
            "allocated_cost_of_sold_units_isk": fmt(allocated_sold_cost),
            "realized_contribution_isk": fmt(realized_contribution),
            "unsold_inventory_cost_basis_isk": fmt(unsold_inventory_cost),
        },
        "full_batch_projection": {
            "output_units": fmt_decimal(output_units),
            "unit_sale_price_isk": fmt(projected_price),
            "gross_sale_value_isk": fmt(projected_gross),
            "sales_tax_isk": fmt(projected_tax),
            "broker_fees_isk": fmt(projected_broker),
            "relist_fees_isk": fmt(projected_relist),
            "other_sale_costs_isk": fmt(projected_other_sale),
            "net_sale_proceeds_isk": fmt(projected_net),
            "projected_contribution_isk": fmt(projected_contribution),
            "unit_contribution_isk": fmt(projected_contribution / output_units),
            "net_margin_rate": fmt_decimal(projected_contribution / projected_gross) if projected_gross else None,
            "roi_on_capital_rate": fmt_decimal(projected_contribution / capital) if capital else None,
            "isk_per_manufacturing_slot_hour": fmt(projected_contribution / slot_hours) if slot_hours else None,
            "isk_per_elapsed_hour": fmt(projected_contribution / elapsed_hours) if elapsed_hours else None,
            "break_even_unit_price_isk": fmt(break_even_price) if break_even_price is not None else None,
            "target_net_margin_rate": fmt_decimal(target_margin),
            "target_margin_unit_price_isk": fmt(target_price) if target_price is not None else None,
            "maximum_affordable_input": max_input_value,
        },
        "warnings": [
            "The model does not fetch prices, recipes, or Industry quotes.",
            "Sale fills and projected price are assumptions or recorded executions, not guaranteed liquidity.",
            "Material cost is economic value, not necessarily historical wallet expenditure.",
            "The full-batch projection uses explicit aggregate broker/relist/other fees supplied by the user.",
            "Cost allocation to sold units is proportional to delivered output; use a different inventory method if required."
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    print(json.dumps(calculate(config), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
