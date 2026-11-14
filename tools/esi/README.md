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
- Sends a pinned `X-Compatibility-Date` and a project User-Agent.
- Respects Expires and ETag metadata; it does not request a cached resource again before its Expires time.
- Uses conditional requests after cache expiry.
- Handles X-Pages pagination for regional market orders.
- Honors Retry-After for HTTP 429.
- Stops on HTTP 420 error-limit responses rather than retrying aggressively.
- Does not attempt to collect all market orders for a region unless specific type IDs are configured.
- Does not infer market prices from adjusted prices.

## Summarize collected order books and history

After a collection completes, pass its timestamped output folder to the summarizer:

```powershell
py -3 tools/esi/summarize_market_data.py \
    --input-dir data/raw/esi/RUN_TIMESTAMP \
    --quantities 1,10,100 \
    --output data/derived/market-summary.json
```

The report groups all order-book pages by region and type, separates sell orders (asks) from buy orders (bids), calculates best bid/ask and spread, and sweeps the visible book to estimate the VWAP and unfilled quantity for each requested batch size. It also summarizes the supplied daily history using total and median/average daily volume and a volume-weighted average daily price.

The execution fields are deliberately named `buy_from_asks` and `sell_into_bids`. They describe the two sides of the book from the operator's perspective. A fillable quantity is only fillable in that observed snapshot. Regional orders may be located at structures or stations the operator cannot access.

The summary retains SHA-256 hashes for the raw source files. It does not apply market fees, manufacturing costs, installation costs, hauling, or any demand forecast.

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
