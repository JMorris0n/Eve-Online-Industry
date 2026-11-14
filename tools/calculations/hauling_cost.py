#!/usr/bin/env python3
"""Compare expected self-haul and courier costs from a JSON scenario.

Uses Decimal arithmetic and only the Python standard library. This is a
scenario calculator, not a route-risk predictor.
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_HALF_UP
from pathlib import Path
from typing import Any

ZERO = Decimal("0")
ONE = Decimal("1")
HOURS_PER_YEAR = Decimal("8760")


def dec(mapping: dict[str, Any], key: str) -> Decimal:
    if key not in mapping:
        raise ValueError(f"Missing required input: {key}")
    try:
        value = Decimal(str(mapping[key]))
    except (InvalidOperation, ValueError):
        raise ValueError(f"Input {key} must be a decimal number") from None
    if not value.is_finite():
        raise ValueError(f"Input {key} must be finite")
    return value


def nonnegative(value: Decimal, name: str) -> Decimal:
    if value < ZERO:
        raise ValueError(f"{name} must be >= 0")
    return value


def positive(value: Decimal, name: str) -> Decimal:
    if value <= ZERO:
        raise ValueError(f"{name} must be > 0")
    return value


def probability(value: Decimal, name: str) -> Decimal:
    if value < ZERO or value > ONE:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


def ceil_div(numerator: Decimal, denominator: Decimal) -> int:
    return int((numerator / denominator).to_integral_value(rounding=ROUND_CEILING))


def money(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def number(value: Decimal) -> str:
    return str(value.normalize())


def calculate(config: dict[str, Any]) -> dict[str, Any]:
    cargo = config["cargo"]
    self_cfg = config["self_haul"]
    courier_cfg = config["courier"]

    cargo_value = positive(dec(cargo, "value_isk"), "cargo.value_isk")
    cargo_volume = positive(dec(cargo, "volume_m3"), "cargo.volume_m3")
    annual_rate = nonnegative(dec(cargo, "annual_capital_rate"), "annual_capital_rate")

    # Self-haul scenario
    self_capacity = positive(dec(self_cfg, "capacity_m3"), "self_haul.capacity_m3")
    self_trips = ceil_div(cargo_volume, self_capacity)
    pilot_hours_per_trip = nonnegative(
        dec(self_cfg, "pilot_hours_per_trip"), "pilot_hours_per_trip"
    )
    pilot_value_per_hour = nonnegative(
        dec(self_cfg, "time_value_isk_per_hour"), "time_value_isk_per_hour"
    )
    direct_cost_per_trip = nonnegative(
        dec(self_cfg, "direct_cost_isk_per_trip"), "direct_cost_isk_per_trip"
    )
    self_loss_probability = probability(
        dec(self_cfg, "loss_probability_per_trip"), "loss_probability_per_trip"
    )
    cargo_loss_severity = probability(
        dec(self_cfg, "cargo_loss_severity"), "cargo_loss_severity"
    )
    ship_replacement = nonnegative(
        dec(self_cfg, "ship_replacement_cost_isk"), "ship_replacement_cost_isk"
    )
    insurance_payout = nonnegative(
        dec(self_cfg, "insurance_payout_isk"), "insurance_payout_isk"
    )
    if insurance_payout > ship_replacement:
        raise ValueError("insurance_payout_isk cannot exceed ship_replacement_cost_isk")
    transit_hours = nonnegative(
        dec(self_cfg, "transit_hours_per_trip"), "transit_hours_per_trip"
    )

    self_direct = Decimal(self_trips) * direct_cost_per_trip
    self_pilot_hours = Decimal(self_trips) * pilot_hours_per_trip
    self_time_cost = self_pilot_hours * pilot_value_per_hour
    self_cargo_loss = cargo_value * self_loss_probability * cargo_loss_severity
    self_ship_loss = (
        Decimal(self_trips)
        * self_loss_probability
        * max(ship_replacement - insurance_payout, ZERO)
    )
    self_capital_cost = (
        cargo_value * annual_rate * transit_hours / HOURS_PER_YEAR
    )
    self_total = (
        self_direct
        + self_time_cost
        + self_cargo_loss
        + self_ship_loss
        + self_capital_cost
    )
    self_any_loss = ONE - (ONE - self_loss_probability) ** self_trips

    # Courier scenario, from the cargo owner's perspective
    courier_capacity = positive(
        dec(courier_cfg, "capacity_m3"), "courier.capacity_m3"
    )
    contracts = ceil_div(cargo_volume, courier_capacity)
    reward_per_contract = nonnegative(
        dec(courier_cfg, "reward_isk_per_contract"), "reward_isk_per_contract"
    )
    fee_per_contract = nonnegative(
        dec(courier_cfg, "creation_fee_isk_per_contract"),
        "creation_fee_isk_per_contract",
    )
    collateral_per_contract = nonnegative(
        dec(courier_cfg, "collateral_isk_per_contract"), "collateral_isk_per_contract"
    )
    courier_failure_probability = probability(
        dec(courier_cfg, "failure_probability_per_contract"),
        "failure_probability_per_contract",
    )
    delivery_hours = nonnegative(
        dec(courier_cfg, "delivery_exposure_hours"), "delivery_exposure_hours"
    )

    cargo_value_per_contract = cargo_value / Decimal(contracts)
    uncovered_per_contract = max(
        cargo_value_per_contract - collateral_per_contract, ZERO
    )
    courier_reward = Decimal(contracts) * reward_per_contract
    courier_fees = Decimal(contracts) * fee_per_contract
    courier_uncovered_loss = (
        Decimal(contracts) * courier_failure_probability * uncovered_per_contract
    )
    courier_capital_cost = (
        cargo_value * annual_rate * delivery_hours / HOURS_PER_YEAR
    )
    courier_total = (
        courier_reward
        + courier_fees
        + courier_uncovered_loss
        + courier_capital_cost
    )
    courier_any_failure = ONE - (ONE - courier_failure_probability) ** contracts

    difference = self_total - courier_total
    lower_cost = "self_haul" if difference <= ZERO else "courier"

    return {
        "inputs": config,
        "self_haul": {
            "trips": self_trips,
            "probability_at_least_one_trip_loss": number(self_any_loss),
            "direct_cost_isk": money(self_direct),
            "pilot_hours": number(self_pilot_hours),
            "pilot_time_cost_isk": money(self_time_cost),
            "expected_cargo_loss_isk": money(self_cargo_loss),
            "expected_ship_loss_isk": money(self_ship_loss),
            "cargo_capital_cost_isk": money(self_capital_cost),
            "expected_total_cost_isk": money(self_total),
            "cost_per_m3_isk": money(self_total / cargo_volume),
            "cost_as_percent_of_cargo_value": number(self_total / cargo_value),
        },
        "courier": {
            "contracts": contracts,
            "probability_at_least_one_contract_failure": number(courier_any_failure),
            "total_reward_isk": money(courier_reward),
            "total_contract_fees_isk": money(courier_fees),
            "expected_uncovered_cargo_loss_isk": money(courier_uncovered_loss),
            "cargo_capital_cost_isk": money(courier_capital_cost),
            "expected_total_cost_isk": money(courier_total),
            "cost_per_m3_isk": money(courier_total / cargo_volume),
            "cost_as_percent_of_cargo_value": number(courier_total / cargo_value),
        },
        "comparison": {
            "self_haul_minus_courier_isk": money(difference),
            "lower_expected_cost": lower_cost,
            "interpretation": (
                "Positive difference means courier has the lower expected cost."
                if difference > ZERO
                else "Negative difference means self-haul has the lower expected cost."
                if difference < ZERO
                else "Both methods have equal expected cost under these assumptions."
            ),
        },
        "model_warning": (
            "Scenario model only. Loss/failure probabilities and delivery exposure "
            "must be supplied for the actual route, ship, cargo, and contractor."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    result = calculate(config)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
