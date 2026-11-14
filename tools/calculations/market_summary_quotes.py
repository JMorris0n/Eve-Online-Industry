#!/usr/bin/env python3
"""Extract exact-quantity quotes from a schema-v4 ESI market summary.

Offline only: no network access, quantity extrapolation, market fees, or proof
of market access.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 4
EXPECTED_MIN_VOLUME_SEMANTICS = "per_individual_buy_order_fill_with_final_remainder_exception"


def load_market_summary(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Cannot read market summary {source}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Market summary is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Market summary root must be a JSON object")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"market summary schema_version must be {SCHEMA_VERSION}")
    model = data.get("execution_model")
    if not isinstance(model, dict):
        raise ValueError("market summary execution_model is missing or invalid")
    if model.get("minimum_volume_enforced_for_sell_into_bids") is not True:
        raise ValueError("market summary does not declare sell-side minimum-volume enforcement")
    if model.get("min_volume_semantics") != EXPECTED_MIN_VOLUME_SEMANTICS:
        raise ValueError("market summary has unrecognized minimum-volume semantics")
    if not isinstance(data.get("summaries"), list):
        raise ValueError("market summary summaries must be an array")
    return data


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


def _one(items: list[Any], predicate, label: str) -> dict[str, Any]:
    found = [item for item in items if isinstance(item, dict) and predicate(item)]
    if not found:
        raise ValueError(f"No {label} found in the market summary")
    if len(found) != 1:
        raise ValueError(f"Multiple {label} records found in the market summary")
    return found[0]


def _order_sources(type_summary: dict[str, Any], region_id: int, type_id: int) -> dict[str, Any]:
    files = type_summary.get("source_files")
    if not isinstance(files, list):
        raise ValueError("source_files is missing from the market summary")
    prefix = f"market-orders-region-{region_id}-type-{type_id}-page-"
    sources = [
        item for item in files
        if isinstance(item, dict) and str(item.get("filename", "")).startswith(prefix)
    ]
    if not sources:
        raise ValueError("No regional market-order source metadata is available for this type")
    sources.sort(key=lambda item: str(item.get("retrieved_at", "")))
    return {
        "retrieved_at": sources[0].get("retrieved_at"),
        "last_page_retrieved_at": sources[-1].get("retrieved_at"),
        "expires": sources[0].get("expires"),
        "source_files": [
            {
                "filename": item.get("filename"),
                "sha256": item.get("sha256"),
                "retrieved_at": item.get("retrieved_at"),
                "expires": item.get("expires"),
                "etag": item.get("etag"),
            }
            for item in sources
        ],
    }


def get_market_quote(
    market_summary: dict[str, Any],
    *,
    region_id: int,
    type_id: int,
    location_id: int,
    quantity: int,
    purpose: str,
) -> dict[str, Any]:
    """Return one precomputed exact-quantity procurement or liquidation quote.

    Procurement uses local asks; liquidation uses buy orders whose ranges reach
    the target. The requested quantity must be present exactly in the summary.
    """
    if purpose not in {"procurement", "liquidation"}:
        raise ValueError("purpose must be 'procurement' or 'liquidation'")
    for value, label in (
        (region_id, "region_id"),
        (type_id, "type_id"),
        (location_id, "location_id"),
        (quantity, "quantity"),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{label} must be a positive integer")

    summaries = market_summary.get("summaries")
    if not isinstance(summaries, list):
        raise ValueError("market summary summaries must be an array")
    type_summary = _one(
        summaries,
        lambda x: x.get("region_id") == region_id and x.get("type_id") == type_id,
        f"region {region_id}, type {type_id} summary",
    )
    locations = type_summary.get("location_books")
    if not isinstance(locations, list):
        raise ValueError("target location_books are missing from type summary")
    location = _one(locations, lambda x: x.get("location_id") == location_id, f"target location {location_id}")
    book = location.get("order_book")
    if not isinstance(book, dict) or book.get("market_scope") != "target_location":
        raise ValueError("selected location does not contain a target-location order book")

    field = "buy_from_asks" if purpose == "procurement" else "sell_into_bids"
    sweeps = book.get(field)
    if not isinstance(sweeps, list):
        raise ValueError(f"target-location {field} sweeps are missing")
    sweep = _one(sweeps, lambda x: x.get("requested_quantity") == quantity, f"{quantity}-unit {purpose} sweep")

    filled, unfilled = sweep.get("filled_quantity"), sweep.get("unfilled_quantity")
    if (
        isinstance(filled, bool) or not isinstance(filled, int) or filled < 0
        or isinstance(unfilled, bool) or not isinstance(unfilled, int) or unfilled < 0
        or filled + unfilled != quantity
    ):
        raise ValueError("sweep fill quantities do not reconcile to the requested quantity")
    full = sweep.get("fully_fillable_in_snapshot")
    if not isinstance(full, bool) or full != (unfilled == 0):
        raise ValueError("sweep fully_fillable_in_snapshot flag is inconsistent")

    gross, vwap = sweep.get("gross_value_isk"), sweep.get("vwap")
    if filled == 0:
        if gross is not None or vwap is not None:
            raise ValueError("zero-fill sweep must have null gross value and VWAP")
    else:
        gross = _number(gross, "gross_value_isk")
        vwap = _number(vwap, "vwap")
        if abs(gross - filled * vwap) > max(0.02, abs(gross) * 1e-9):
            raise ValueError("sweep gross value does not reconcile to filled quantity × VWAP")
    if purpose == "liquidation" and sweep.get("minimum_volume_enforced") is not True:
        raise ValueError("sell-into-bids sweep does not confirm minimum-volume enforcement")

    range_info = book.get("range_resolution", {})
    if not isinstance(range_info, dict):
        range_info = {}
    warnings = []
    if not full:
        warnings.append("The snapshot does not cover the full requested quantity.")
    if purpose == "liquidation" and sweep.get("orders_skipped_with_invalid_min_volume", 0):
        warnings.append("Some eligible bids with invalid minimum-volume data were excluded.")
    if purpose == "liquidation" and range_info.get("unknown_range_buy_orders", 0):
        warnings.append("Some remote bid ranges were unresolved and excluded.")
    source = _order_sources(type_summary, region_id, type_id)
    return {
        "status": "full" if full else ("partial" if filled else "no_fill"),
        "purpose": purpose,
        "region_id": region_id,
        "type_id": type_id,
        "location_id": location_id,
        "quantity": quantity,
        "filled_quantity": filled,
        "unfilled_quantity": unfilled,
        "fully_fillable_in_snapshot": full,
        "vwap_isk": vwap,
        "gross_value_isk": gross,
        "worst_fill_price_isk": sweep.get("worst_fill_price"),
        "minimum_volume_enforced": sweep.get("minimum_volume_enforced") if purpose == "liquidation" else None,
        "filled_order_count": sweep.get("filled_order_count") if purpose == "liquidation" else None,
        "orders_skipped_below_minimum": sweep.get("orders_skipped_because_fill_below_min_volume", 0) if purpose == "liquidation" else None,
        "orders_skipped_invalid_minimum": sweep.get("orders_skipped_with_invalid_min_volume", 0) if purpose == "liquidation" else None,
        "range_resolution": range_info if purpose == "liquidation" else None,
        "collection_retrieved_at": market_summary.get("collection", {}).get("retrieved_at"),
        "source_timestamp": source.get("retrieved_at"),
        "order_book_source": source,
        "caveat": book.get("caveat"),
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--region-id", type=int, required=True)
    parser.add_argument("--type-id", type=int, required=True)
    parser.add_argument("--location-id", type=int, required=True)
    parser.add_argument("--quantity", type=int, required=True)
    parser.add_argument("--purpose", choices=("procurement", "liquidation"), required=True)
    args = parser.parse_args()
    try:
        data = load_market_summary(args.summary)
        result = get_market_quote(
            data, region_id=args.region_id, type_id=args.type_id,
            location_id=args.location_id, quantity=args.quantity, purpose=args.purpose,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
