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
- Added `tools/sde/parse_industry_recipes.py`, which reads current-format `blueprints.jsonl` and `types.jsonl`, joins English type names plus published/group/market-group/tech-level/volume metadata, and emits normalized manufacturing/reaction recipe JSONL.
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
- Added `tools/esi/summarize_market_data.py` to combine paginated order books, deduplicate repeated order IDs across numerically ordered pages, distinguish asks from bids, calculate visible-book VWAP/depth for requested quantities, summarize backward-looking daily history, and retain source hashes plus manifest timestamps/cache metadata.
- Added network-free unit tests for collector URL construction, HTTP-date parsing, Retry-After parsing, and X-Pages pagination.
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
3. Reconcile the current-format parser against the actual downloaded archive, especially record counts, blueprint IDs, material/product joins, skill requirements, and reaction activities.
4. Add any schema corrections discovered during that reconciliation, then keep parser fixtures aligned with real source records.
5. Do not feed normalized recipes into profitability calculations until material modifiers, facility bonuses, job quotes, and output quantities are implemented and separately tested.

No current market price or profitability conclusion is asserted by this audit.


## Local execution results supplied on 2026-11-14

### SDE build 3698585

- [x] Downloaded CCP JSONL archive using the repository downloader.
- [x] Latest manifest reported build **3698585**, release date **2026-11-13T11:06:47Z**.
- [x] Archive resolved to `eve-online-static-data-3698585-jsonl.zip`, size **99,758,284 bytes**.
- [x] Archive SHA-256: `afda59ef777c8e89ef7c6864dd5e103e4b75455ab158f370b780c8f6e0826649`.
- [x] ZIP integrity test passed.
- [x] Archive inspection found 102 entries, including `blueprints.jsonl` (3,459,370 bytes), `types.jsonl` (155,972,886 bytes), and `planetSchematics.jsonl` (31,548 bytes).
- [ ] Archive has not yet been extracted; the recipe parser has not yet been run against the actual archive.
- [ ] The inspector's first sample was `accountingEntryTypes.jsonl`, not a blueprint or type record. Actual blueprint/type schema and joins therefore remain to be reconciled.

### Public ESI smoke test

- [x] Public `GET /industry/systems/` returned HTTP 200; body length **1,957,353 bytes**; SHA-256 `36a90f17429bf9ba5768767d7a370b63ef3e969e7722e8da75b6c95785c9a876`.
- [x] Public `GET /markets/prices/` returned HTTP 200; body length **1,124,326 bytes**; SHA-256 `4042806df7f5b7f71a15a9e90d183937f38821ae23b759c328d16c39cf61b49d`.
- [x] The client sent compatibility date **2026-11-13**. Both responses reported matched compatibility date **2020-01-01**. CCP's versioning guidance explicitly says the matched response date can be the requested date or earlier depending on route internals. This is not a failed request; retain both values for provenance.
- [x] ESI supplied ETags, cache-expiry timestamps, and HTTP 200 responses. Both responses showed `X-Esi-Cache-Status: HIT`.
- [ ] The example config contains empty `regions` and `type_ids`; consequently this run collected **no regional order books or market history**. It tested only the two global resources.
- [ ] A bounded regional market order/history collection is still required to validate pagination, order depth, transaction history, and the market summarizer against live responses.

### Private profile

- [x] A local copy of the three-character example profile was created and passed the structural validator.
- [ ] The profile is still the blank example. Character skills, job capacity, blueprint inventory, facility access, operating capital, and attention budget have not yet been populated or verified.

### Audit interpretation

The SDE download/integrity stage and the two global public ESI endpoint smoke tests are successful. M1 is not complete until the extracted current-build recipe parser and a small regional market-data collection have been validated. M2's local file/validator workflow is successful, but the actual operating profile remains unknown.
