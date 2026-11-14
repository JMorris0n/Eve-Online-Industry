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
from collections import defaultdict, deque
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

SUMMARY_SCHEMA_VERSION = 3


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



def _read_jsonl_records(path: Path):
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_number} is invalid JSON: {exc}") from exc
                if not isinstance(record, dict):
                    raise ValueError(f"{path}:{line_number} must contain a JSON object")
                yield record
    except OSError as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc


def load_sde_market_map(sde_dir: Path) -> dict[str, Any]:
    """Load solar-system regions and directed stargate connections from the JSONL SDE."""
    systems_path = sde_dir / "mapSolarSystems.jsonl"
    gates_path = sde_dir / "mapStargates.jsonl"
    if not systems_path.is_file():
        raise ValueError(f"SDE map file is missing: {systems_path}")
    if not gates_path.is_file():
        raise ValueError(f"SDE map file is missing: {gates_path}")

    system_regions: dict[int, int] = {}
    for record in _read_jsonl_records(systems_path):
        system_id = record.get("_key")
        region_id = record.get("regionID")
        if (
            isinstance(system_id, bool) or not isinstance(system_id, int) or system_id <= 0
            or isinstance(region_id, bool) or not isinstance(region_id, int) or region_id <= 0
        ):
            raise ValueError(f"{systems_path} contains a record without valid _key/regionID")
        system_regions[system_id] = region_id

    reverse_adjacency: dict[int, set[int]] = defaultdict(set)
    for record in _read_jsonl_records(gates_path):
        source_system = record.get("solarSystemID")
        destination = record.get("destination")
        destination_system = destination.get("solarSystemID") if isinstance(destination, dict) else None
        if (
            isinstance(source_system, bool) or not isinstance(source_system, int)
            or isinstance(destination_system, bool) or not isinstance(destination_system, int)
        ):
            raise ValueError(f"{gates_path} contains a record without valid solar-system endpoints")
        if source_system in system_regions and destination_system in system_regions:
            reverse_adjacency[destination_system].add(source_system)

    if not system_regions or not reverse_adjacency:
        raise ValueError("SDE map files did not produce a usable solar-system jump graph")
    return {"system_regions": system_regions, "reverse_adjacency": dict(reverse_adjacency)}


def shortest_jump_distances(
    start_system_id: int,
    reverse_adjacency: dict[int, set[int]],
    system_regions: dict[int, int],
    region_id: int,
    *,
    max_jumps: int = 40,
) -> dict[int, int]:
    """Return source-to-target distances via the reversed SDE gate graph."""
    if system_regions.get(start_system_id) != region_id:
        return {}
    distances = {start_system_id: 0}
    queue = deque([start_system_id])
    while queue:
        current = queue.popleft()
        current_distance = distances[current]
        if current_distance >= max_jumps:
            continue
        for neighbor in reverse_adjacency.get(current, set()):
            if neighbor not in system_regions or neighbor in distances:
                continue
            distances[neighbor] = current_distance + 1
            queue.append(neighbor)
    return distances


def classify_buy_order_range(
    order: dict[str, Any],
    *,
    target_location_id: int,
    target_system_id: int | None,
    target_region_id: int,
    system_regions: dict[int, int] | None,
    jump_distances: dict[int, int] | None,
) -> tuple[str, str, int | None]:
    """Classify a bid's reach at a target market location."""
    source_location_id = order.get("location_id")
    source_system_id = order.get("system_id")
    if source_location_id == target_location_id:
        return "eligible", "same_location", 0
    order_range = order.get("range")
    if not isinstance(order_range, str) or not order_range:
        return "unknown", "missing_or_invalid_range", None
    if order_range == "station":
        return "excluded", "station_range_elsewhere", None
    if order_range == "region":
        if system_regions is not None and isinstance(source_system_id, int) and target_system_id is not None:
            source_region = system_regions.get(source_system_id)
            target_region = system_regions.get(target_system_id)
            if source_region is None or target_region is None:
                return "unknown", "system_missing_from_sde_map", None
            if source_region != target_region or target_region != target_region_id:
                return "excluded", "different_region", None
        return "eligible", "region_range", None
    if order_range == "solarsystem":
        if (
            not isinstance(source_system_id, int)
            or isinstance(source_system_id, bool)
            or target_system_id is None
        ):
            return "unknown", "missing_system_id", None
        if source_system_id == target_system_id:
            return "eligible", "same_solar_system", 0
        return "excluded", "different_solar_system", None
    try:
        maximum_jumps = int(order_range)
    except (TypeError, ValueError):
        return "unknown", "unsupported_range_value", None
    if str(maximum_jumps) != order_range or maximum_jumps not in {1, 2, 3, 4, 5, 10, 20, 30, 40}:
        return "unknown", "unsupported_range_value", None
    if (
        not isinstance(source_system_id, int)
        or isinstance(source_system_id, bool)
        or target_system_id is None
    ):
        return "unknown", "missing_system_id", None
    if source_system_id == target_system_id:
        return "eligible", "same_solar_system", 0
    if jump_distances is None or system_regions is None:
        return "unknown", "numeric_range_requires_sde_map", None
    source_region = system_regions.get(source_system_id)
    target_region = system_regions.get(target_system_id)
    if source_region is None or target_region is None:
        return "unknown", "system_missing_from_sde_map", None
    if source_region != target_region or target_region != target_region_id:
        return "excluded", "different_region", None
    distance = jump_distances.get(source_system_id)
    if distance is None:
        return "excluded", "no_route_within_40_jumps_in_region", None
    if distance <= maximum_jumps:
        return "eligible", "within_jump_range", distance
    return "excluded", "outside_jump_range", distance


def _buy_order_minimum_volume(order: dict[str, Any]) -> int | None:
    """Treat omitted ESI min_volume as the one-unit platform default."""
    if "min_volume" not in order:
        return 1
    value = order.get("min_volume")
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        return None
    return value


def sweep_buy_orders(orders: list[dict[str, Any]], quantity: int) -> dict[str, Any]:
    """Sweep bids while applying each minimum to the original requested sell order."""
    def priority(order: dict[str, Any]):
        issued = order.get("issued")
        order_id = order.get("order_id")
        return (
            -dec(order.get("price"), "order.price"),
            issued if isinstance(issued, str) else "",
            order_id if isinstance(order_id, int) and not isinstance(order_id, bool) else 0,
        )

    remaining = quantity
    filled = 0
    gross = Decimal("0")
    worst_price: Decimal | None = None
    filled_order_count = 0
    skipped_below_minimum = 0
    skipped_invalid_minimum = 0
    for order in sorted(orders, key=priority):
        volume = order.get("volume_remain")
        if isinstance(volume, bool) or not isinstance(volume, int) or volume <= 0:
            continue
        minimum_volume = _buy_order_minimum_volume(order)
        if minimum_volume is None:
            skipped_invalid_minimum += 1
            continue
        # The minimum qualifies the original sell order, not the residual quantity
        # remaining after higher-priced buy orders have matched.
        if quantity < minimum_volume:
            skipped_below_minimum += 1
            continue
        take = min(remaining, volume)
        if take <= 0:
            break
        price = dec(order.get("price"), "order.price")
        filled += take
        remaining -= take
        gross += price * take
        worst_price = price
        filled_order_count += 1
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
        "minimum_volume_enforced": True,
        "filled_order_count": filled_order_count,
        "orders_skipped_because_requested_quantity_below_min_volume": skipped_below_minimum,
        "orders_skipped_with_invalid_min_volume": skipped_invalid_minimum,
        "same_price_order_priority": "issued_then_order_id_proxy",
    }


def summarize_target_location_book(
    orders: list[dict[str, Any]],
    quantities: list[int],
    *,
    target_location_id: int,
    target_system_id: int | None,
    region_id: int,
    sde_market_map: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build the market book available at one target station or structure."""
    system_regions = sde_market_map["system_regions"] if sde_market_map else None
    reverse_adjacency = sde_market_map["reverse_adjacency"] if sde_market_map else None
    jump_distances = None
    if reverse_adjacency is not None and system_regions is not None and target_system_id is not None:
        jump_distances = shortest_jump_distances(
            target_system_id, reverse_adjacency, system_regions, region_id, max_jumps=40
        )

    eligible_bids: list[dict[str, Any]] = []
    local_asks: list[dict[str, Any]] = []
    excluded_out_of_range = 0
    unknown_range = 0
    unknown_reasons: dict[str, int] = defaultdict(int)
    total_buy_orders = 0
    for order in orders:
        volume = order.get("volume_remain")
        if isinstance(volume, bool) or not isinstance(volume, int) or volume <= 0:
            continue
        if order.get("is_buy_order") is True:
            total_buy_orders += 1
            status, reason, _ = classify_buy_order_range(
                order,
                target_location_id=target_location_id,
                target_system_id=target_system_id,
                target_region_id=region_id,
                system_regions=system_regions,
                jump_distances=jump_distances,
            )
            if status == "eligible":
                eligible_bids.append(order)
            elif status == "unknown":
                unknown_range += 1
                unknown_reasons[reason] += 1
            else:
                excluded_out_of_range += 1
        elif order.get("is_buy_order") is False and order.get("location_id") == target_location_id:
            local_asks.append(order)

    bid_levels: dict[Decimal, int] = defaultdict(int)
    ask_levels: dict[Decimal, int] = defaultdict(int)
    for order in eligible_bids:
        bid_levels[dec(order.get("price"), "order.price")] += order["volume_remain"]
    for order in local_asks:
        ask_levels[dec(order.get("price"), "order.price")] += order["volume_remain"]
    best_bid = max(bid_levels) if bid_levels else None
    best_ask = min(ask_levels) if ask_levels else None
    spread = best_ask - best_bid if best_bid is not None and best_ask is not None else None
    spread_pct = (
        float(spread / best_ask * 100)
        if spread is not None and best_ask is not None and best_ask > 0
        else None
    )
    invalid_minimum_count = sum(
        1 for order in eligible_bids if _buy_order_minimum_volume(order) is None
    )
    remote_eligible = sum(
        1 for order in eligible_bids if order.get("location_id") != target_location_id
    )
    range_note = (
        "Numeric jump ranges use the SDE stargate graph; the buy-order and target systems must be in the selected market region, but the route may pass through other regions."
        if sde_market_map
        else "Remote numeric jump ranges are unknown without --sde-dir and excluded from target-location bid sweeps."
    )
    caveat = (
        "This target-location book includes only local sell orders and buy orders whose configured "
        "range covers the target system. Sell-into-bids sweeps apply min_volume to the original "
        "requested sell quantity. " + range_note + " Market access, fees, order expiry, snapshot "
        "changes, and exact same-price matching priority are not resolved; this is not a guaranteed quote."
    )
    return {
        "market_scope": "target_location",
        "is_crossed": best_bid is not None and best_ask is not None and best_bid > best_ask,
        "order_count": len(eligible_bids) + len(local_asks),
        "buy_order_count": len(eligible_bids),
        "sell_order_count": len(local_asks),
        "buy_volume": sum(bid_levels.values()),
        "sell_volume": sum(ask_levels.values()),
        "best_bid": float(best_bid) if best_bid is not None else None,
        "best_ask": float(best_ask) if best_ask is not None else None,
        "spread_isk": float(spread) if spread is not None else None,
        "spread_pct_of_best_ask": spread_pct,
        "sell_into_bids": [sweep_buy_orders(eligible_bids, q) for q in quantities],
        "buy_from_asks": [sweep(sorted(ask_levels.items()), q) for q in quantities],
        "range_resolution": {
            "sde_jump_graph_available": sde_market_map is not None,
            "buy_orders_in_regional_snapshot": total_buy_orders,
            "eligible_buy_orders": len(eligible_bids),
            "eligible_remote_buy_orders": remote_eligible,
            "excluded_out_of_range_buy_orders": excluded_out_of_range,
            "unknown_range_buy_orders": unknown_range,
            "unknown_range_reasons": dict(sorted(unknown_reasons.items())),
            "eligible_buy_orders_with_invalid_min_volume": invalid_minimum_count,
        },
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


def summarize_directory(
    input_dir: Path,
    quantities: list[int],
    *,
    sde_dir: Path | None = None,
) -> list[dict[str, Any]]:
    _, source_metadata = load_manifest_metadata(input_dir)
    sde_market_map = load_sde_market_map(sde_dir) if sde_dir is not None else None
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
        posted_location_books = []
        location_books = []
        for location_id, local_orders in sorted(location_orders.items()):
            system_ids = sorted({
                order["system_id"] for order in local_orders
                if isinstance(order.get("system_id"), int)
                and not isinstance(order.get("system_id"), bool)
            })
            posted_location_books.append({
                "location_id": location_id,
                "system_ids": system_ids,
                "order_book": summarize_book(
                    local_orders, quantities, market_scope="single_location"
                ),
            })
            target_system_id = system_ids[0] if len(system_ids) == 1 else None
            location_books.append({
                "location_id": location_id,
                "system_ids": system_ids,
                "system_id": target_system_id,
                "order_book": summarize_target_location_book(
                    book_orders,
                    quantities,
                    target_location_id=location_id,
                    target_system_id=target_system_id,
                    region_id=region_id,
                    sde_market_map=sde_market_map,
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
            "posted_location_books": posted_location_books,
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
    parser.add_argument("--sde-dir", type=Path,
                        help="Optional extracted JSONL SDE directory; needed for numeric buy-order jump ranges")
    args = parser.parse_args()
    try:
        quantities = sorted(set(int(value) for value in args.quantities.split(",")))
        if not quantities or any(value <= 0 for value in quantities):
            raise ValueError("--quantities must contain positive integers")
        if not args.input_dir.is_dir():
            raise ValueError(f"input directory does not exist: {args.input_dir}")
        summaries = summarize_directory(args.input_dir, quantities, sde_dir=args.sde_dir)
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
                "schema_version": SUMMARY_SCHEMA_VERSION,
                "source": "public ESI regional market snapshots",
                "input_directory": str(args.input_dir),
                "requested_quantities": quantities,
                "collection": collection_metadata,
                "execution_model": {
                    "target_location_books": True,
                    "buy_order_ranges_expanded": True,
                    "sde_jump_graph_loaded": args.sde_dir is not None,
                    "minimum_volume_enforced_for_sell_into_bids": True,
                    "min_volume_missing_default": 1,
                    "same_price_order_priority": "issued_then_order_id_proxy",
                },
                "summaries": summaries,
                "caveats": [
                    "Order book data is a point-in-time regional snapshot.",
                    "Regional order locations may be inaccessible to the operator.",
                    "Market history is backward-looking and is not a sales forecast.",
                    "No market fee, hauling, installation, or character/facility adjustment is applied.",
                    "Target-location books include only local sell orders and buy orders whose posted range covers the target system.",
                    "Remote numeric buy-order jump ranges require the SDE stargate graph; unresolved ranges are excluded from target-location bid sweeps.",
                    "Buy-order minimum volume is tested against the original requested sell quantity; omitted ESI min_volume defaults to one.",
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
