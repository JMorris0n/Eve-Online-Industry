# Read-only ESI collector

This collector retrieves selected public market and industry data from CCP's EVE Swagger Interface (ESI). It uses only the Python standard library and does not use EVE SSO or request character/corporation scopes.

## Requirements

- Python 3.10 or newer.
- Internet access to `esi.evetech.net`.
- A reviewed ESI compatibility date.
- Region IDs and item type IDs for market order/history collection.

## Configure

Copy the example configuration:

```powershell
Copy-Item tools/esi/config.example.json tools/esi/config.json
```

Edit `tools/esi/config.json`:
- `regions`: EVE region IDs to collect.
- `type_ids`: item type IDs to collect in each region.
- `include_industry_systems`: collect public activity-specific system cost indices.
- `include_market_prices`: collect CCP adjusted/average prices.

An empty region or type list skips regional order/history collection. The two global public resources can still be collected.

## Run

```powershell
py -3 tools/esi/collect_public_market_data.py --config tools/esi/config.json --compatibility-date YYYY-MM-DD
```

The compatibility date must be a date that has actually been reviewed and tested against the current ESI schema. Do not copy the placeholder literally. CCP advances ESI compatibility dates at 11:00 UTC; before using the current calendar date, confirm that the date is available in the API Explorer. Record the tested date with the resulting collection manifest.

Optional overrides:

```powershell
py -3 tools/esi/collect_public_market_data.py --config tools/esi/config.json --compatibility-date YYYY-MM-DD --output-dir data/raw/esi --cache-dir data/cache/esi
```

## Output

Each run writes to a timestamped folder under `data/raw/esi/` containing:
- `industry-systems.json`
- `market-prices.json`
- One JSON file per regional market-order page and type ID.
- One JSON file per regional market-history/type ID.
- `manifest.json` with URLs, timestamps, ETags, cache status, SHA-256 hashes, and the compatibility date.

The persistent HTTP cache is stored under `data/cache/esi/`. These folders are excluded from Git.

## Important behavior

- Uses public read-only endpoints only. No EVE SSO token is required.
- Uses CCP's unversioned ESI base URL and sends a pinned `X-Compatibility-Date` plus a project User-Agent.
- Records both the requested compatibility date and ESI's matched response date. ESI may return the requested date or an earlier route-specific date; an earlier response date is not by itself a rejection.
- Respects Expires and ETag metadata; it does not request a cached resource again before its Expires time.
- Uses conditional requests after cache expiry.
- Handles X-Pages pagination for regional market orders.
- Honors Retry-After for HTTP 429.
- Stops on HTTP 420 error-limit responses rather than retrying aggressively.
- Does not attempt to collect all market orders for a region unless specific type IDs are configured.
- Does not infer market prices from adjusted prices.

## Summarize collected order books and history

After a collection completes, summarize the timestamped output folder. Supply the extracted SDE directory to resolve numeric buy-order jump ranges:

~~~powershell
py -3 tools/esi/summarize_market_data.py --input-dir data/raw/esi/RUN_TIMESTAMP --sde-dir data/raw/sde/BUILD/extracted --quantities 100,1000,10000 --output data/derived/market-summary.json
~~~

The --sde-dir argument is optional. Without it, station, same-system, and region ranges can be resolved, but remote numeric jump ranges are marked unknown and excluded from target-location bid sweeps.

The version 4 report separates three perspectives:

- order_book is a region-wide composite for discovery. Its best bid and best ask can come from different stations or structures. A crossed composite is not evidence of executable arbitrage.
- posted_location_books groups all orders by the location where each order was posted. This is a provenance/debugging view, not the market book available at that location.
- location_books evaluates a target location. Sell orders are included only when posted at that exact station or structure. Buy orders are included when their range setting covers the target system. Numeric jump ranges use mapSolarSystems.jsonl and mapStargates.jsonl from the supplied SDE, with both the buy-order system and target system in the selected market region. A shortest route may pass through other regions.

For target-location books, sell_into_bids applies each buy order's min_volume to that individual fill. A fill smaller than min_volume is permitted only when it consumes the buy order's entire remaining volume and that remaining volume is itself below min_volume. If min_volume is omitted from the ESI response, it defaults to one unit. This interpretation follows the secondary [EVE Market Strategies reference](https://orbitalenterprises.github.io/eve-market-strategies/index), which describes minimum volume per fill and the below-minimum final-remainder exception. Treat the summary as a screening estimate, not a guaranteed execution quote; live in-game behavior remains the operational authority.

Each target book reports range-resolution counts: eligible remote bids, excluded out-of-range bids, unresolved ranges, and eligible bids with invalid minimum-volume data. Equal-price bids use issue time and order ID as a deterministic ordering proxy; exact same-price in-game priority is not asserted as verified.

This remains a screening estimate, not a guaranteed execution quote. User access to a station/structure, fees, order expiry, snapshot drift, and exact in-game matching behavior still need consideration. Material procurement uses sell orders at the target location only. Liquidation uses eligible buy orders whose range reaches that target and enforces each order's minimum acceptable sell-order size.

The report retains SHA-256 hashes for raw source files and includes source timestamps/cache metadata when present. It does not apply market fees, manufacturing costs, installation costs, hauling, or a demand forecast.

## Limitations

This is an initial collector, not a production-grade data warehouse. It does not:
- Authenticate to EVE SSO.
- Retrieve character skills, assets, or industry jobs.
- Collect structure markets requiring authorization.
- Normalize or calculate profitability.
- Guarantee a consistent snapshot across multiple pages if the ESI cache expires during pagination.

For large multi-page collections, run near the beginning of the endpoint cache window and deduplicate records by order ID. Compare the response timestamps and cache metadata before combining files.

Official documentation:
- https://developers.eveonline.com/docs/services/esi/overview/
- https://developers.eveonline.com/docs/services/esi/best-practices/
- https://esi.evetech.net/ui/?version=latest
