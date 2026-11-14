# M1 Data Foundation Audit

**Status:** In progress  
**Audit date:** 2026-11-14  
**Purpose:** Record the current source contract and the tests still required before the SDE/ESI pipeline is treated as validated.

## Current findings

### CCP Static Data Export

- CCP's current SDE landing page identifies build **3698585**, released **2026-11-13**.
- CCP provides both JSON Lines and YAML archives. JSON Lines is the preferred project format because the official documentation warns that large YAML datasets can be memory-intensive.
- Integer-keyed mappings are represented in JSONL using `_key` and `_value` records. A parser must not assume the old YAML/legacy CSV layout.
- CCP publishes a schema changelog and a machine-readable latest-build manifest. The downloader's manifest/hash/ZIP-integrity approach is directionally appropriate.
- CCP documents ETag and Last-Modified support for SDE resources.

Sources:
- [CCP SDE landing page](https://developers.eveonline.com/static-data)
- [CCP Static Data documentation](https://developers.eveonline.com/docs/services/static-data/)
- [CCP SDE schema changelog](https://developers.eveonline.com/static-data/tranquility/schema-changelog.yaml)

### EVE Swagger Interface

The collector targets these public data families:

| Collector output | ESI resource | Intended use | Validation still required |
|---|---|---|---|
| `industry-systems.json` | `GET /industry/systems/` | Activity-specific system cost indices | Confirm current response fields and freshness |
| `market-prices.json` | `GET /markets/prices/` | Adjusted and average prices | Confirm field meanings; never treat adjusted price as a live quote |
| Regional order pages | `GET /markets/{region_id}/orders/` | Current public regional order book | Confirm pagination, order-type coverage, and observation timestamps |
| Regional history | `GET /markets/{region_id}/history/` | Daily volume, order count, and price history | Confirm field semantics and one-year history limits |

CCP describes ESI as the official REST API. Some endpoints are public and others require SSO. The API Explorer is the authoritative endpoint and scope reference. The project must keep public regional markets distinct from authorized Upwell structure markets.

Sources:
- [CCP ESI overview](https://developers.eveonline.com/docs/services/esi/overview/)
- [CCP ESI API Explorer](https://developers.eveonline.com/api-explorer)

## Review of existing repository tooling

### SDE downloader, inspector, and recipe parser

Existing files:
- `tools/sde/fetch_sde.py`
- `tools/sde/inspect_sde.py`
- `tools/sde/README.md`

Initial code review:
- Uses the standard library and the CCP latest-build redirect.
- Records resolved archive URL, build number, retrieval time, SHA-256, HTTP metadata, and ZIP integrity.
- Includes path traversal protection during extraction.
- Inspector currently prints archive layout and a sample JSONL record.
- Added `tools/sde/parse_industry_recipes.py`, which reads current-format `blueprints.jsonl` and `types.jsonl`, joins English type names, and emits normalized manufacturing/reaction recipe JSONL.
- The parser has representative fixture tests and explicitly preserves base quantities/time without applying ME, facility bonuses, system indices, job fees, or market prices.
- Actual ingestion of the current CCP archive remains unverified until the user can run the downloader and inspector locally.

### Public ESI collector and market summarizer

Existing files:
- `tools/esi/collect_public_market_data.py`
- `tools/esi/config.example.json`
- `tools/esi/README.md`

Initial code review:
- Uses public endpoints only and does not request SSO scopes.
- Records endpoint URLs, retrieval timestamps, ETags, cache metadata, and content hashes.
- Implements X-Pages pagination, conditional requests, HTTP 429 Retry-After handling, and a stop on HTTP 420.
- Saves order-book and market-history observations separately.
- Does not collect private structure markets, character skills, assets, blueprints, or industry jobs. This is expected for the public-data-first phase.
- Added `tools/esi/summarize_market_data.py` to combine paginated order books, distinguish asks from bids, calculate visible-book VWAP/depth for requested quantities, summarize backward-looking daily history, and retain source hashes.
- The summarizer labels regional depth as potentially inaccessible and does not treat snapshot fillability as guaranteed execution. Fixture tests are in place; live ESI validation remains pending.

## Important compatibility-date note

CCP's ESI documentation says the API compatibility date represents the date the application implementation was reviewed. ESI changes its API date at **11:00 UTC**; using the current calendar date before that transition can be invalid. Therefore, the example command's `2026-11-14` value is a proposed pin, not evidence that this project has tested that compatibility contract. Select and record a date only after checking the API Explorer and successfully running the collector against it.

Source: [CCP ESI versioning documentation](https://developers.eveonline.com/docs/services/esi/overview/)

## Execution evidence still needed

The repository code review is not equivalent to local execution. The following remain open:

- [ ] Download the current SDE JSONL archive locally and confirm the build number, SHA-256, and ZIP test.
- [ ] Inspect the archive's actual file paths and sample records for types, blueprints, industry activities, and reaction data.
- [ ] Confirm the current SDE schema supports the recipe/material/product joins required for manufacturing and reactions.
- [x] Add a deterministic summarizer for paginated public order books and daily history, with source hashes and snapshot caveats.
- [ ] Run a deliberately small public ESI collection against a selected test region and a handful of item type IDs.
- [ ] Confirm response headers, page counts, market-history records, and cache behavior from the saved raw outputs.
- [ ] Record an explicit list of unavailable/private data, especially alliance Upwell structure market visibility.

## Next technical steps

1. Add focused SDE inspection for the actual blueprint/industry recipe files after the current archive is downloaded.
2. Run the existing public ESI collector with a deliberately small type/region sample and retain its manifest locally.
3. Add schema-aware parsing only after the current archive records have been inspected. Avoid coding against remembered pre-2025 SDE layouts.
4. Add tests around any parsing and normalization code before it feeds profitability calculations.

No current market price or profitability conclusion is asserted by this audit.
