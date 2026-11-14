#!/usr/bin/env python3
"""Summarize public regional ESI market order books and daily history snapshots.

Order-book depth is an observation, not a promise of executable liquidity:
regional orders may be at inaccessible stations or structures, and snapshots
can change before a player acts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from statistics import median
from typing import Any


ORDER_PATTERN = re.compile(
    r"market-orders-region-(?P<region>\d+)-type-(?P<type>\d+)-page-(?P<page>\d+)\.json$"
)
HISTORY_PATTERN = re.compile(
    r"market-history-region-(?P<region>\d+)-type-(?P<type>\d+)\.json$"
)


def dec(value: Any, label: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"{label} must be numeric, got {value!r}") from exc
    if not result.is_finite():
        raise ValueError(f"{label} must be finite")
    return result


def sweep(levels: list[tuple[Decimal, int]], quantity: int) -> dict[str, Any]:
    remaining = quantity
    filled = 0
    gross = Decimal("0")
    worst_price: Decimal | None = None
    for price, available in levels:
        take = min(remaining, available)
        if take <= 0:
            continue
        filled += take
        remaining -= take
        gross += price * take
        worst_price = price
        if remaining == 0:
            break
    return {
        "requested_quantity": quantity,
        "filled_quantity": filled,
        "unfilled_quantity": remaining,
        "vwap": float(gross / filled) if filled else None,
        "gross_value_isk": float(gross) if filled else None,
        "worst_fill_price": float(worst_price) if worst_price is not None else None,
        "fully_fillable_in_snapshot": remaining == 0,
    }


def summarize_book(
    orders: list[dict[str, Any]],
    quantities: list[int],
    *,
    market_scope: str = "regional_composite",
) -> dict[str, Any]:
    asks: dict[Decimal, int] = defaultdict(int)
    bids: dict[Decimal, int] = defaultdict(int)
    ask_count = bid_count = 0
    for order in orders:
        if not isinstance(order, dict):
            raise ValueError("market order entry must be an object")
        price = dec(order.get("price"), "order.price")
        volume = order.get("volume_remain")
        if price <= 0:
            raise ValueError(f"order.price must be positive, got {price}")
        if isinstance(volume, bool) or not isinstance(volume, int) or volume < 0:
            raise ValueError(f"order volume_remain must be a non-negative integer, got {volume!r}")
        if volume == 0:
            continue
        if order.get("is_buy_order") is True:
            bids[price] += volume
            bid_count += 1
        elif order.get("is_buy_order") is False:
            asks[price] += volume
            ask_count += 1
        else:
            raise ValueError("order.is_buy_order must be boolean")

    ask_levels = sorted(asks.items(), key=lambda pair: pair[0])
    bid_levels = sorted(bids.items(), key=lambda pair: pair[0], reverse=True)
    best_ask = ask_levels[0][0] if ask_levels else None
    best_bid = bid_levels[0][0] if bid_levels else None
    spread = best_ask - best_bid if best_ask is not None and best_bid is not None else None
    spread_pct = (
        float(spread / best_ask * 100)
        if spread is not None and best_ask and best_ask > 0
        else None
    )
    is_crossed = (
        best_bid is not None and best_ask is not None and best_bid > best_ask
    )
    if market_scope == "regional_composite":
        caveat = (
            "This is a region-wide composite. Orders can be at different stations "
            "or structures, so the displayed best bid and ask may not be mutually "
            "executable. A crossed regional composite is not proof of arbitrage."
        )
    elif market_scope == "single_location":
        caveat = (
            "This groups orders by their posted location only. Buy-order range, "
            "minimum fill volume, operator access, fees, and snapshot changes are "
            "not resolved; it is not a guaranteed executable quote."
        )
    else:
        raise ValueError(f"unsupported market scope: {market_scope}")
    return {
        "market_scope": market_scope,
        "is_crossed": is_crossed,
        "order_count": ask_count + bid_count,
        "buy_order_count": bid_count,
        "sell_order_count": ask_count,
        "buy_volume": sum(bids.values()),
        "sell_volume": sum(asks.values()),
        "best_bid": float(best_bid) if best_bid is not None else None,
        "best_ask": float(best_ask) if best_ask is not None else None,
        "spread_isk": float(spread) if spread is not None else None,
        "spread_pct_of_best_ask": spread_pct,
        "sell_into_bids": [sweep(bid_levels, quantity) for quantity in quantities],
        "buy_from_asks": [sweep(ask_levels, quantity) for quantity in quantities],
        "caveat": caveat,
    }


def summarize_history(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"days_observed": 0, "first_date": None, "last_date": None}
    volumes: list[int] = []
    total_volume = 0
    total_trades = 0
    weighted_price = Decimal("0")
    dates: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("market history entry must be an object")
        date = row.get("date")
        volume = row.get("volume")
        order_count = row.get("order_count")
        if not isinstance(date, str):
            raise ValueError("history.date must be a string")
        if isinstance(volume, bool) or not isinstance(volume, int) or volume < 0:
            raise ValueError("history.volume must be a non-negative integer")
        if isinstance(order_count, bool) or not isinstance(order_count, int) or order_count < 0:
            raise ValueError("history.order_count must be a non-negative integer")
        average = dec(row.get("average"), "history.average")
        dates.append(date)
        volumes.append(volume)
        total_volume += volume
        total_trades += order_count
        weighted_price += average * volume
    return {
        "days_observed": len(rows),
        "first_date": min(dates),
        "last_date": max(dates),
        "total_volume": total_volume,
        "average_daily_volume": total_volume / len(rows),
        "median_daily_volume": median(volumes),
        "total_reported_order_count": total_trades,
        "volume_weighted_average_daily_price": (
            float(weighted_price / total_volume) if total_volume else None
        ),
        "caveat": "History is completed daily regional activity; it is not a forecast or proof of current demand.",
    }


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc


def load_manifest_metadata(input_dir: Path) -> tuple[dict[str, Any] | None, dict[str, dict[str, Any]]]:
    path = input_dir / "manifest.json"
    if not path.is_file():
        return None, {}
    manifest = load_json(path)
    if not isinstance(manifest, dict):
        raise ValueError(f"{path} must contain a JSON object")
    sources: dict[str, dict[str, Any]] = {}
    for output in manifest.get("outputs", []):
        if not isinstance(output, dict) or not isinstance(output.get("file"), str):
            continue
        filename = Path(output["file"]).name
        sources[filename] = {
            field: output.get(field)
            for field in ("url", "status", "retrieved_at", "from_cache", "expires", "etag", "sha256")
        }
    return manifest, sources


def summarize_directory(input_dir: Path, quantities: list[int]) -> list[dict[str, Any]]:
    _, source_metadata = load_manifest_metadata(input_dir)
    orders: dict[tuple[int, int], dict[int, dict[str, Any]]] = defaultdict(dict)
    raw_order_counts: dict[tuple[int, int], int] = defaultdict(int)
    duplicate_counts: dict[tuple[int, int], int] = defaultdict(int)
    histories: dict[tuple[int, int], list[dict[str, Any]]] = {}
    source_hashes: dict[str, str] = {}

    def source_sort_key(path: Path) -> tuple[Any, ...]:
        order_match = ORDER_PATTERN.fullmatch(path.name)
        if order_match:
            return (0, int(order_match.group("region")), int(order_match.group("type")),
                    int(order_match.group("page")), path.name)
        history_match = HISTORY_PATTERN.fullmatch(path.name)
        if history_match:
            return (1, int(history_match.group("region")), int(history_match.group("type")), 0, path.name)
        return (2, path.name)

    for path in sorted(input_dir.glob("*.json"), key=source_sort_key):
        match = ORDER_PATTERN.fullmatch(path.name)
        if match:
            key = (int(match.group("region")), int(match.group("type")))
            data = load_json(path)
            if not isinstance(data, list):
                raise ValueError(f"{path} must contain a JSON array")
            for order in data:
                if not isinstance(order, dict):
                    raise ValueError(f"{path} contains a non-object order")
                order_id = order.get("order_id")
                if isinstance(order_id, bool) or not isinstance(order_id, int) or order_id <= 0:
                    raise ValueError(f"{path} contains an order without a valid positive order_id")
                if order.get("type_id") != key[1]:
                    raise ValueError(
                        f"{path} contains order {order_id} for unexpected type_id {order.get('type_id')!r}"
                    )
                raw_order_counts[key] += 1
                if order_id in orders[key]:
                    duplicate_counts[key] += 1
                location_id = order.get("location_id")
                if location_id is not None and (
                    isinstance(location_id, bool)
                    or not isinstance(location_id, int)
                    or location_id <= 0
                ):
                    raise ValueError(
                        f"{path} contains order {order_id} with invalid location_id {location_id!r}"
                    )
                # Page files are processed in page-number order. If pagination
                # drift repeats an order, retain the last observed copy once.
                orders[key][order_id] = order
            source_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
            continue
        match = HISTORY_PATTERN.fullmatch(path.name)
        if match:
            key = (int(match.group("region")), int(match.group("type")))
            data = load_json(path)
            if not isinstance(data, list):
                raise ValueError(f"{path} must contain a JSON array")
            histories[key] = data
            source_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()

    keys = sorted(set(orders) | set(histories))
    results = []
    for region_id, type_id in keys:
        key = (region_id, type_id)
        book_orders = list(orders.get(key, {}).values())
        location_orders: dict[int, list[dict[str, Any]]] = defaultdict(list)
        orders_without_location_id = 0
        for order in book_orders:
            location_id = order.get("location_id")
            if location_id is None:
                orders_without_location_id += 1
            else:
                location_orders[location_id].append(order)
        location_books = []
        for location_id, local_orders in sorted(location_orders.items()):
            system_ids = sorted({
                order["system_id"] for order in local_orders
                if isinstance(order.get("system_id"), int)
                and not isinstance(order.get("system_id"), bool)
            })
            location_books.append({
                "location_id": location_id,
                "system_ids": system_ids,
                "order_book": summarize_book(
                    local_orders, quantities, market_scope="single_location"
                ),
            })
        results.append({
            "region_id": region_id,
            "type_id": type_id,
            "raw_order_record_count": raw_order_counts.get(key, 0),
            "duplicate_order_ids_removed": duplicate_counts.get(key, 0),
            "orders_without_location_id": orders_without_location_id,
            "location_count": len(location_books),
            "location_books": location_books,
            "order_book": summarize_book(
                book_orders, quantities, market_scope="regional_composite"
            ) if book_orders else None,
            "history": summarize_history(histories[(region_id, type_id)])
            if (region_id, type_id) in histories else None,
            "source_files": [
                {
                    "filename": name,
                    "sha256": source_hashes[name],
                    **source_metadata.get(name, {}),
                }
                for name in sorted(source_hashes)
                if f"region-{region_id}-type-{type_id}-" in name
                or name == f"market-history-region-{region_id}-type-{type_id}.json"
            ],
        })
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True,
                        help="One timestamped ESI collection directory")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--quantities", default="1,10,100",
                        help="Comma-separated target quantities for order-book sweeps")
    args = parser.parse_args()
    try:
        quantities = sorted(set(int(value) for value in args.quantities.split(",")))
        if not quantities or any(value <= 0 for value in quantities):
            raise ValueError("--quantities must contain positive integers")
        if not args.input_dir.is_dir():
            raise ValueError(f"input directory does not exist: {args.input_dir}")
        summaries = summarize_directory(args.input_dir, quantities)
        manifest, _ = load_manifest_metadata(args.input_dir)
        collection_metadata = None if manifest is None else {
            "retrieved_at": manifest.get("retrieved_at"),
            "compatibility_date": manifest.get("compatibility_date"),
            "regions": manifest.get("regions", []),
            "type_ids": manifest.get("type_ids", []),
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps({
                "schema_version": 1,
                "source": "public ESI regional market snapshots",
                "input_directory": str(args.input_dir),
                "requested_quantities": quantities,
                "collection": collection_metadata,
                "summaries": summaries,
                "caveats": [
                    "Order book data is a point-in-time regional snapshot.",
                    "Regional order locations may be inaccessible to the operator.",
                    "Market history is backward-looking and is not a sales forecast.",
                    "No market fee, hauling, installation, or character/facility adjustment is applied.",
                ],
            }, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: summarized {len(summaries)} region/type combinations to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
