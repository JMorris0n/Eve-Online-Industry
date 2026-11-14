#!/usr/bin/env python3
"""Estimate EVE Online market taxes, broker fees, and relist fees.

Rates are decimal fractions. The model uses published NPC station formulas
and explicit owner-set Upwell broker rates. Verify live quotes before trading.
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


def dec(value: Any, name: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{name} must be a decimal number") from None
    if not result.is_finite():
        raise ValueError(f"{name} must be finite")
    return result


def money(value: Decimal) -> str:
    return str(value.quantize(CENT, rounding=ROUND_HALF_UP))


def rate_text(value: Decimal) -> str:
    return str(value.normalize())


def level(value: Any, name: str, maximum: int = 5) -> int:
    number = dec(value, name)
    if number != number.to_integral_value() or number < 0 or number > maximum:
        raise ValueError(f"{name} must be an integer from 0 to {maximum}")
    return int(number)


def bounded(value: Any, name: str, minimum: Decimal, maximum: Decimal) -> Decimal:
    result = dec(value, name)
    if result < minimum or result > maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return result


def calculate(config: dict[str, Any]) -> dict[str, Any]:
    character = config["character"]
    market = config["market"]
    order = config["order"]

    accounting = level(character["accounting_level"], "accounting_level")
    broker_relations = level(character["broker_relations_level"], "broker_relations_level")
    advanced_broker_relations = level(
        character["advanced_broker_relations_level"], "advanced_broker_relations_level"
    )
    faction_standing = bounded(
        character["unmodified_faction_standing"], "unmodified_faction_standing",
        Decimal("-10"), Decimal("10")
    )
    corporation_standing = bounded(
        character["unmodified_corporation_standing"], "unmodified_corporation_standing",
        Decimal("-10"), Decimal("10")
    )

    sales_tax_rate = Decimal("0.075") * (
        ONE - Decimal("0.11") * Decimal(accounting)
    )
    market_type = market["type"]
    if market_type == "npc_station":
        broker_rate = (
            Decimal("0.03")
            - Decimal("0.003") * Decimal(broker_relations)
            - Decimal("0.0003") * faction_standing
            - Decimal("0.0002") * corporation_standing
        )
        broker_rate = max(Decimal("0.01"), broker_rate)
        broker_detail = "NPC station formula using unmodified faction and corporation standings"
    elif market_type == "upwell_structure":
        scc_rate = Decimal("0.005")
        owner_rate = bounded(
            market["owner_broker_rate"], "owner_broker_rate", ZERO, ONE
        )
        broker_rate = scc_rate + owner_rate
        broker_detail = "0.5% SCC component plus the supplied owner-set rate; Broker Relations is not applied"
    else:
        raise ValueError("market.type must be npc_station or upwell_structure")

    order_value = dec(order["order_value_isk"], "order_value_isk")
    if order_value < ZERO:
        raise ValueError("order_value_isk must be >= 0")
    previous_order_value = dec(
        order["previous_order_value_isk"], "previous_order_value_isk"
    )
    if previous_order_value < ZERO:
        raise ValueError("previous_order_value_isk must be >= 0")
    sale_value = dec(order["sale_value_isk"], "sale_value_isk")
    if sale_value < ZERO:
        raise ValueError("sale_value_isk must be >= 0")

    create_non_immediate = order.get("create_non_immediate_order", True)
    reprice_existing = order.get("reprice_existing_order", False)
    if not isinstance(create_non_immediate, bool) or not isinstance(reprice_existing, bool):
        raise ValueError("create_non_immediate_order and reprice_existing_order must be booleans")
    create_broker_fee = order_value * broker_rate if create_non_immediate else ZERO
    relist_discount = Decimal("0.50") + Decimal("0.06") * Decimal(
        advanced_broker_relations
    )
    relist_fee = (
        max(ZERO, broker_rate * (order_value - previous_order_value))
        + (ONE - relist_discount) * broker_rate * order_value
        if reprice_existing else ZERO
    )
    sales_tax = sale_value * sales_tax_rate

    return {
        "market_type": market_type,
        "character": {
            "accounting_level": accounting,
            "broker_relations_level": broker_relations,
            "advanced_broker_relations_level": advanced_broker_relations,
            "unmodified_faction_standing": str(faction_standing),
            "unmodified_corporation_standing": str(corporation_standing),
        },
        "rates": {
            "sales_tax_rate": rate_text(sales_tax_rate),
            "broker_fee_rate": rate_text(broker_rate),
            "relist_discount_rate": rate_text(relist_discount),
        },
        "fees": {
            "order_creation_broker_fee_isk": money(create_broker_fee),
            "relist_fee_isk": money(relist_fee),
            "sales_tax_on_sale_value_isk": money(sales_tax),
        },
        "assumptions": {
            "broker_fee_formula": broker_detail,
            "relist_formula": "max(0, BR × (P2 - P1)) + (1 - RD) × BR × P2",
            "immediate_match_note": (
                "The order-creation broker fee applies to a non-immediate order. "
                "Do not apply it to an immediate fill; sales tax still applies to the seller."
            ),
        },
        "warning": "Estimate only. Confirm the live market order quote and wallet journal; structure owner fees and game rules can change."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    print(json.dumps(calculate(config), indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
