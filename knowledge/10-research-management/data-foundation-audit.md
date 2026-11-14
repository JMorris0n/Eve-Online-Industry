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
- Actual ingestion against CCP build 3698585 is verified locally: the archive was downloaded, integrity-checked, extracted, and parsed into 5,022 normalized manufacturing/reaction records. The parser output-quality review is recorded below.

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

The collector was tested with requested compatibility date **2026-11-13** against `GET /industry/systems/` and `GET /markets/prices/`. Both returned HTTP 200 and reported matched compatibility date **2020-01-01**. Record both the requested and matched dates. An earlier matched date is not by itself a failed request; compatibility behavior remains route-specific.

Source: [CCP ESI versioning documentation](https://developers.eveonline.com/docs/services/esi/overview/)

## Remaining validation

- [ ] Run a bounded public ESI collection for one test region and a small set of type IDs.
- [ ] Reconcile regional order-book pagination, market-history records, cache headers, timestamps, and the market summarizer against saved live responses.
- [ ] Resolve or explicitly classify the 21 type metadata join gaps identified in the normalized SDE output. Do not infer item names or marketability from missing metadata.
- [ ] Define a refresh cadence from observed ESI cache behavior before scheduling repeated pulls.
- [ ] Keep public regional market coverage separate from authorized Upwell structure-market access and personal character/account data.

The SDE acquisition and recipe-normalization stages are locally validated. M1 remains in progress pending regional ESI validation and the remaining data-coverage questions.

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
- [x] Parser executed against the extracted archive and successfully normalized manufacturing and reaction records. The inspector's first generic sample was `accountingEntryTypes.jsonl`; the subsequent full parser run reconciled the recipe arrays and joins against the actual blueprint/type tables, with 21 missing type metadata references retained as explicit null metadata rather than guessed.

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

The SDE download, integrity, extraction, and current-build manufacturing/reaction parser stages are successful. The two global public ESI endpoint smoke tests are also successful. M1 remains open until a bounded regional market-data collection and its pagination/history outputs are validated. M2's local file/validator workflow is successful, but the actual operating profile remains unknown.


## SDE parser finding from first actual archive run

The first parser execution against build 3698585 stopped with `activity.materials must be an array`. The current community-maintained schema documents Manufacturing `materials`, `products`, and `skills` arrays as optional fields, while Reaction arrays are required. The parser's fixture assumptions were therefore too strict for manufacturing records.

The parser has been updated to:
- Preserve omitted, null, explicitly empty, and populated arrays as distinct source states.
- Mark a recipe incomplete when its manufacturing material array is omitted/null. Such a recipe must not be priced as a zero-input recipe.
- Skip and count activities without a usable product array rather than failing the entire SDE ingestion.
- Keep reaction materials/products/skills required.
- Make the profile feasibility report return `unknown` when normalized recipe arrays are incomplete or the recipe predates completeness metadata.

This parser correction was applied and then executed successfully against the already extracted build 3698585. The actual output counts and data-quality findings are recorded in the section below. No new download or extraction was required.


## Normalized recipe output quality review (2026-11-14)

The user ran the corrected parser against SDE build **3698585** and supplied the generated `industry-recipes.jsonl` for inspection.

### Parser execution

- [x] **5,022** normalized recipes written from **5,045** activity records examined.
- [x] **4,902** manufacturing recipes and **120** reaction recipes.
- [x] **23** activities skipped because no usable product array was available.
- [x] **17** recipes have omitted material arrays and are marked `incomplete`; none is incorrectly represented as a complete zero-input recipe.
- [x] **137** recipes have omitted required-skill arrays. The source-state metadata is retained so the feasibility evaluator can leave these results `unknown`.
- [x] **5,005** output records have `recipe_data_status=complete`; **17** are `incomplete`.
- [x] All **5,022** blueprint/activity keys are unique. No duplicate activity keys, missing blueprint names, or empty material arrays marked complete were found.

### Data-quality flags for downstream work

- **Unresolved type metadata:** one material type ID (**3924**) and 20 product type IDs (**37236, 37237, 37238, 37239, 37240, 37241, 37242, 37243, 37244, 37245, 37247, 37262, 37263, 37264, 37265, 37266, 37267, 37278, 37279, 37286**) have no matching usable name record in `types.jsonl`. Related metadata, including published/group fields, is null. Preserve these as unresolved references; do not invent names or treat them as ordinary market candidates. The missing type ID 3924 has also been reported in earlier SDE community discussion: [EVE Forums, “Missing typeid 3924 from static data export”](https://forums.eveonline.com/t/missing-typeid-3924-from-static-data-export/458479).
- **Publication flags:** 811 blueprint type records are unpublished; 580 product records are unpublished; 20 product records have unknown publication status because their type metadata join is missing. These flags should be explicit candidate-screen inputs, not silently ignored.
- **Zero base time:** one record, blueprint type **34256** (`Vargur Krusual Edition Blueprint`), has `base_time_seconds_per_run=0` and unpublished blueprint/product types. This is a source value, not a parser error. It must be treated as an exceptional recipe and reviewed before any time-based ranking or division.
- **Skill level zero:** the parser preserves level 0 values. These are valid source integers under the current parser contract and must not be raised to level 1 or discarded.

### Interpretation

The normalized output is structurally usable as a static recipe reference. It is **not** a fully market-resolved candidate universe. The 17 incomplete material recipes must not be costed; the 137 omitted-skill recipes must remain feasibility-unknown; unresolved product types must not enter ordinary market ranking without a separate resolution step; unpublished records and the zero-time recipe need explicit handling. No profitability conclusions have been drawn from this file.

Current schema reference: [CCP SDE schema for blueprints](https://sde.riftforeve.online/schema/blueprints/). The schema allows omitted Manufacturing arrays while requiring the Reaction arrays; it also defines activity time as a non-negative integer.
