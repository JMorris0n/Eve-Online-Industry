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
- Actual ingestion against CCP build 3698585 is verified locally at the command/output-count level: the archive was downloaded, integrity-checked, extracted, and the parser completed. The user supplied aggregate console output, but not the generated JSONL file; record-level output quality has therefore not been independently inspected in this audit.

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
- The summarizer labels regional depth as potentially inaccessible and does not treat snapshot fillability as guaranteed execution. The bounded Forge collection and earlier location-aware summaries have been reviewed; schema-v4 bid-side execution still requires a local rerun against the saved raw files.

## Important compatibility-date note

The collector was tested with requested compatibility date **2026-11-13** against `GET /industry/systems/` and `GET /markets/prices/`. Both returned HTTP 200 and reported matched compatibility date **2020-01-01**. Record both the requested and matched dates. An earlier matched date is not by itself a failed request; compatibility behavior remains route-specific.

Source: [CCP ESI versioning documentation](https://developers.eveonline.com/docs/services/esi/overview/)

## Remaining validation

- [x] Run a bounded public ESI collection for The Forge (region 10000002) and type IDs 34, 35, and 36.
- [x] Reconcile the saved collection's order counts, daily history coverage, location grouping, cache/timestamp provenance, and v2/v3 summary structure. Schema-v4 bid-side execution still requires its own local rerun and review.
- [ ] Run the local normalized-recipe audit command and review its record-level quality report.
- [ ] Define a refresh cadence from observed ESI cache behavior before scheduling repeated pulls; this can wait until the first real evaluation is established.
- [x] Keep public regional market coverage separate from authorized Upwell structure-market access and personal character/account data.

The SDE acquisition, extraction, and parser execution are locally validated at the command/output-count level. M1 remains in progress pending the local schema-v4 market summary rerun/review and the normalized-recipe audit report.

No current market price or profitability conclusion is asserted by this audit.

## Local execution results supplied on 2026-11-14

### SDE build 3698585

- [x] Downloaded CCP JSONL archive using the repository downloader.
- [x] Latest manifest reported build **3698585**, release date **2026-11-13T11:06:47Z**.
- [x] Archive resolved to `eve-online-static-data-3698585-jsonl.zip`, size **99,758,284 bytes**.
- [x] Archive SHA-256: `afda59ef777c8e89ef7c6864dd5e103e4b75455ab158f370b780c8f6e0826649`.
- [x] ZIP integrity test passed.
- [x] Archive inspection found 102 entries, including `blueprints.jsonl` (3,459,370 bytes), `types.jsonl` (155,972,886 bytes), and `planetSchematics.jsonl` (31,548 bytes).
- [x] Archive extracted to the local build directory.
- [x] Parser executed against the extracted archive. The user-provided console output reported 5,022 normalized recipes from 5,045 activity records examined, with 23 activities skipped because no product array was available. The generated JSONL was not supplied for direct record-level inspection in this audit, so no uniqueness, type-join, publication-flag, or individual-record conclusions are claimed here.

### Public ESI smoke test

- [x] Public `GET /industry/systems/` returned HTTP 200; body length **1,957,353 bytes**; SHA-256 `36a90f17429bf9ba5768767d7a370b63ef3e969e7722e8da75b6c95785c9a876`.
- [x] Public `GET /markets/prices/` returned HTTP 200; body length **1,124,326 bytes**; SHA-256 `4042806df7f5b7f71a15a9e90d183937f38821ae23b759c328d16c39cf61b49d`.
- [x] The client sent compatibility date **2026-11-13**. Both responses reported matched compatibility date **2020-01-01**. CCP's versioning guidance explicitly says the matched response date can be the requested date or earlier depending on route internals. This is not a failed request; retain both values for provenance.
- [x] ESI supplied ETags, cache-expiry timestamps, and HTTP 200 responses. Both responses showed `X-Esi-Cache-Status: HIT`.
- [x] The earlier global-resource smoke test used empty `regions` and `type_ids`, so that run alone collected no regional orders or history.
- [x] A later bounded regional collection for The Forge and three mineral type IDs is documented below.

### Private profile

- [x] A local copy of the three-character example profile was created and passed the structural validator.
- [ ] The profile is still the blank example. Character skills, job capacity, blueprint inventory, facility access, operating capital, and attention budget have not yet been populated or verified.

### Audit interpretation

The SDE download, integrity, extraction, and parser execution are complete. The later bounded regional ESI collection and schema-v3 summary have been reviewed. M1 remains open pending a local schema-v4 rerun and review. M2's profile template/validator workflow is available, but the actual operating profile remains unpopulated and unverified.


## SDE parser finding from first actual archive run

The first parser execution against build 3698585 stopped with `activity.materials must be an array`. The current community-maintained schema documents Manufacturing `materials`, `products`, and `skills` arrays as optional fields, while Reaction arrays are required. The parser's fixture assumptions were therefore too strict for manufacturing records.

The parser has been updated to:
- Preserve omitted, null, explicitly empty, and populated arrays as distinct source states.
- Mark a recipe incomplete when its manufacturing material array is omitted/null. Such a recipe must not be priced as a zero-input recipe.
- Skip and count activities without a usable product array rather than failing the entire SDE ingestion.
- Keep reaction materials/products/skills required.
- Make the profile feasibility report return `unknown` when normalized recipe arrays are incomplete or the recipe predates completeness metadata.

This parser correction was applied and then executed successfully against the already extracted build 3698585. The actual output counts and data-quality findings are recorded in the section below. No new download or extraction was required.


## Normalized recipe parser execution counts (2026-11-14)

The user ran the corrected parser against the already extracted SDE build **3698585** and supplied the console output.

### Reported execution results

- [x] **5,022** normalized recipes written from **5,045** activity records examined.
- [x] **23** activities skipped because no product array was available.
- [x] **17** recipes have omitted/null material arrays.
- [x] **137** recipes have omitted/null skill arrays.
- [x] The parser warns that recipes with omitted/null material arrays are incomplete and must not be costed as zero-input recipes.
- [x] The parser reports base material quantities per run and explicitly notes that job modifiers and facility costs are not applied.

### Evidence boundary

Only the console output was supplied for this run. The generated `industry-recipes.jsonl` was not provided in the conversation and was not directly inspected during this audit. Accordingly, this audit does **not** claim to have verified activity-type breakdowns, unique blueprint/activity keys, duplicate absence, individual type-metadata joins, publication flags, or exceptional record contents. Those checks can be completed later from a small local quality-report output or a sanitized excerpt. Raw SDE data and the full normalized recipe data should remain local.

No profitability conclusions have been drawn from the parser output.

## Bounded regional ESI collection results (2026-11-14)

The user completed a first public regional market collection for The Forge (region **10000002**) and type IDs **34 (Tritanium)**, **35 (Pyerite)**, and **36 (Mexallon)**. The saved collection folder was `20261114T185315Z`; the summary was produced with requested sweep sizes **100, 1,000, and 10,000 units**.

### Collection and response validation

- [x] The collection manifest records requested compatibility date **2026-11-13**, retrieval time **2026-11-14T18:53:25Z**, region, type IDs, endpoint URLs, response timestamps, ETags, cache expiry, hashes, and request headers.
- [x] `GET /industry/systems/` returned HTTP **200**.
- [x] `GET /markets/prices/` returned HTTP **304**, and the client reused its previously cached response and SHA-256.
- [x] All three regional order-book requests returned HTTP **200**, each with `X-Pages: 1`.
- [x] All three regional history requests returned HTTP **200**.
- [x] All sampled responses reported matched compatibility date **2020-01-01** even though the requested pin was **2026-11-13**. Preserve requested and matched dates separately; this was not a request failure.
- [x] The saved summary contains **516** order records across the three types, with no duplicate order IDs removed.
- [x] The summary contains **409** daily history rows per type, spanning **2025-10-01** through **2026-11-13**.

### Initial market observations

| Type ID | Order records | Buy orders | Sell orders | Best regional bid | Best regional ask | 409-day average daily volume | Median daily volume | Volume-weighted average daily price |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 34 Tritanium | 158 | 100 | 58 | 4.15 ISK | 4.35 ISK | 5,903,288,265 | 5,548,382,356 | 4.0124 ISK |
| 35 Pyerite | 186 | 64 | 122 | 16.30 ISK | 15.91 ISK | 2,710,920,993 | 2,645,231,654 | 20.7091 ISK |
| 36 Mexallon | 172 | 101 | 71 | 53.06 ISK | 51.05 ISK | 693,147,995 | 655,029,922 | 57.0858 ISK |

The 100-, 1,000-, and 10,000-unit aggregate sweeps were fully covered in each region-wide snapshot. These are not executable liquidity guarantees because the reported regional book combines orders from multiple locations and the current sweep does not enforce order minimum fill quantities or access restrictions.

### Important reconciliation finding: crossed regional composites

The region-wide best bid exceeded the best ask for:
- Pyerite: **16.30 bid vs 15.91 ask**, a displayed composite spread of **-0.39 ISK**.
- Mexallon: **53.06 bid vs 51.05 ask**, a displayed composite spread of **-2.01 ISK**.

This is not proof of arbitrage. ESI regional market orders include a `location_id`; a region-wide maximum bid and minimum ask can originate at different stations or structures. These orders may not be mutually executable. The earlier summary did not group by location, so its regional spread and depth values are discovery-only.

The summarizer has therefore been extended to emit:
- A clearly labeled `regional_composite` book, with an explicit crossed-book flag and a warning not to interpret cross-location spreads as arbitrage.
- `location_books` grouped by posted `location_id`, including system IDs where the response supplies them.
- Counts for orders missing a location ID.
- Summary schema version 2.

The location-level view remains a screening aid, not a firm quote. It groups buy orders by the location where they were posted but does not yet expand buy-order ranges into other eligible systems, enforce `min_volume`, confirm structure access, or calculate transaction fees. These are explicit follow-on requirements for the production evaluator.

### Local script synchronization note

The uploaded console output shows the local collector requested `https://esi.evetech.net/latest/...` URLs. The current repository collector uses the unversioned base URL `https://esi.evetech.net` with the same explicit `X-Compatibility-Date` header. The successful local run is retained as valid execution evidence for the responses it received, but the user's local collector script is behind the current repository version and should be refreshed before the next collection. The already saved raw regional JSON files can be summarized again without repeating ESI requests.

### M1 status

SDE download, extraction, recipe normalization, and the bounded public regional ESI collection have all completed locally. M1 remains **in progress** until the location-aware summarizer is run against the saved raw regional orders, the local collector/summarizer copies are synchronized, and remaining order-range/minimum-volume and private-market access limits are documented. No manufacturing profitability conclusion is made from this small mineral sample.


## Location-aware market execution review (2026-11-14)

The uploaded `market-summary-v2.json` and later `market-summary-v3.json` were generated from saved regional collection `20261114T185315Z`. Their structure, collection provenance, and target-location grouping were reviewed. The v3 report is superseded for bid-side execution calculations by schema v4.

### Collection and location reconciliation

- [x] The source collection covers The Forge (region **10000002**) and type IDs **34 (Tritanium)**, **35 (Pyerite)**, and **36 (Mexallon)**.
- [x] The raw collection contains **516** unique order records: 158 Tritanium, 186 Pyerite, and 172 Mexallon.
- [x] No duplicate order IDs were removed and no order records lacked a location ID.
- [x] The v2 summary grouped orders into 28 Tritanium, 27 Pyerite, and 17 Mexallon location books, **72 total**.
- [x] Each type contains **409** daily history rows spanning **2025-10-01** through **2026-11-13**.
- [x] The v3 summary added target-location books and expanded eligible buy orders using their range settings plus the SDE stargate graph.
- [x] Each of the 72 target books had a single system mapping in the uploaded summary.

The most active location observed in the initial v2 data was location **60003760**, system **30000142**. It accounted for 57.6% of Tritanium order records, 66.7% of Pyerite, and 68.0% of Mexallon. This is a bounded market observation, not evidence that the user has access to the location or that these minerals are suitable production candidates.

Regional composite best bid/ask values for Pyerite and Mexallon appeared crossed in the first report, while location-specific books were not crossed. Cross-location regional composites are discovery data only and must not be interpreted as executable spreads.

### Market execution model and version history

The target-location view uses local sell orders and buy orders whose configured range covers the target system. The SDE stargate graph resolves numeric jump ranges. The queried buy-order system and target system must be in the selected market region, although the shortest path may transit other regions. Remote numeric ranges remain unknown and are excluded when no SDE graph is supplied.

- **Schema v2:** grouped orders by posted location. It did not yet expand remote buy-order ranges or apply buy-order minimum volume correctly.
- **Schema v3:** added target-location books and range expansion. Its first minimum-volume implementation was later identified as too restrictive because it tested each order against the original requested sell quantity.
- **Schema v4:** supersedes v3 for sell-into-bids estimates. It applies each buy order's `min_volume` to the individual fill. A fill below `min_volume` is permitted only when it consumes the buy order's entire remaining volume and that remaining volume is itself below `min_volume`. A below-minimum partial fill that leaves order volume remaining is rejected.

The secondary [EVE Market Strategies reference](https://orbitalenterprises.github.io/eve-market-strategies/index) describes minimum volume as applying to each fill and notes that the final match may be smaller when the order's remaining volume is already below the minimum. This is secondary documentation, not an official CCP statement. Exact live behavior should still be checked against an in-game quote before committing capital.

Other remaining limitations include structure access, fees, order expiry, snapshot drift, and exact same-price matching priority. Equal-price bids use issue time and order ID as a deterministic ordering proxy; exact in-game priority is not claimed as verified.

Sources:
- [CCP Buy and Sell Orders](https://support.eveonline.com/hc/en-us/articles/203218932-Buy-and-Sell-Orders): range eligibility and order matching.
- [ESI market order fields](https://docs.rs/eve-esi-client/latest/eve_esi_client/types/struct.CharactersCharacterIdOrdersGetItem.html): range, `min_volume`, `location_id`, and `system_id`.
- [SDE mapStargates schema](https://sde.riftforeve.online/schema/mapStargates/): gate records map source systems to destination systems.
- [SDE mapSolarSystems schema](https://sde.riftforeve.online/schema/mapSolarSystems/): system records provide region identifiers.
- [EVE Market Strategies](https://orbitalenterprises.github.io/eve-market-strategies/index): secondary explanation of per-fill minimum volume and final remainder behavior.

### Remaining local validation

- [x] Schema-v3 location/range changes and schema-v4 per-fill minimum-volume logic are covered by tests.
- [x] GitHub Actions run [43639123156](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43639123156) passed 27 ESI summary tests.
- [ ] Run the current schema-v4 summarizer against the saved raw collection with SDE build 3698585.
- [ ] Review schema-v4 target-location bid sweeps, skipped orders, and VWAP values before using them in product liquidation estimates.

The previously uploaded `market-summary-v3.json` remains useful for source coverage and location reconciliation, but its bid-side fill quantities, VWAPs, and fillability conclusions are superseded. Do not use those v3 execution estimates for production economics.

