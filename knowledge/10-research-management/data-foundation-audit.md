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


## Final schema-v4 market summary review (2026-11-14)

The user uploaded `market-summary-v4.json` from saved collection `data/raw/esi/20261114T185315Z`, with SDE build **3698585** supplied to the summarizer. The report was retrieved from Dropbox at **2026-11-14T21:18:56Z** and parsed as schema version **4**.

### Collection and summary integrity

- [x] The report identifies The Forge (region **10000002**), type IDs **34 (Tritanium)**, **35 (Pyerite)**, and **36 (Mexallon)**, and requested sweep quantities **100, 1,000, and 10,000**.
- [x] The source collection contains **516** regional market orders: 158 Tritanium, 186 Pyerite, and 172 Mexallon.
- [x] No duplicate order IDs were removed and no order records lacked a location ID.
- [x] The report contains **72** target-location books: 28 Tritanium, 27 Pyerite, and 17 Mexallon. Location IDs are unique within each type.
- [x] Each mineral has **409** days of history from **2025-10-01** through **2026-11-13**.
- [x] The report identifies the SDE jump graph as loaded and schema-v4 minimum-volume semantics as `per_individual_buy_order_fill_with_final_remainder_exception`.
- [x] All 72 target books fully cover their 100-, 1,000-, and 10,000-unit sell-into-bids sweeps. Fill quantities, fillability flags, and gross-value/VWAP arithmetic reconcile.
- [x] No target book reports unresolved buy-order ranges or eligible bids with invalid minimum-volume data.

Target-location books are intentionally not additive across locations. A remote buy order can be eligible at multiple target systems, so sums of target-book order counts are not unique regional order counts.

### Ask-side procurement depth

Across the 72 target-location books (three mineral types combined), local ask-side sweeps were fully fillable as follows:

| Requested quantity | Fully fillable books | Partial books | No-fill books |
|---:|---:|---:|---:|
| 100 units | 41 / 72 | 1 | 30 |
| 1,000 units | 40 / 72 | 2 | 30 |
| 10,000 units | 37 / 72 | 5 | 30 |

This measures local ask depth only. It does not establish that the user can access each location or that the tested minerals are suitable industrial inputs for the eventual candidate.

### Location 60003760 / system 30000142

| Mineral | Eligible bids | Eligible remote bids | Out-of-range bids | Best bid | Best ask | 10,000-unit sell-into-bids VWAP |
|---|---:|---:|---:|---:|---:|---:|
| Tritanium | 88 | 29 | 12 | 4.15 | 4.35 | 4.15 |
| Pyerite | 52 | 27 | 12 | 16.30 | 16.86 | 16.29 |
| Mexallon | 97 | 37 | 4 | 53.06 | 55.87 | 53.06 |

Pyerite's 16.29 ISK bid-side VWAP is below its 16.30 best bid because the highest-priced order is skipped by the minimum-volume rule for these requested quantities. Best bid is not necessarily the executable price for every sell size.

### Schema-v3/schema-v4 comparison

Schema v4 applies `min_volume` to each individual match. A final below-minimum fill is allowed only when it consumes the buy order's entire remaining volume and that remainder is itself below `min_volume`. A below-minimum partial fill that leaves volume on the order is rejected.

Comparing the uploaded v3 and v4 summaries found **no numeric change** in the **216** sampled bid-side sweeps (72 location books × three quantities). The v4 report remains canonical because its matching rule and caveat are corrected. Identical outputs on this sample do not demonstrate that v3's earlier rule was generally correct.

The [EVE Market Strategies reference](https://orbitalenterprises.github.io/eve-market-strategies/index) describes minimum volume per fill and the final-remainder exception. This is secondary documentation, not an official CCP specification. In-game execution remains authoritative.

### Freshness and validation limits

- The three order-book source files were retrieved between **18:53:19Z and 18:53:24Z**. Their recorded ESI cache expiry times were between **18:53:55Z and 18:54:05Z**.
- The v4 summary was uploaded at **21:18:56Z**. The underlying order snapshot was already well beyond its ESI cache window. It validates the collection/summarization pipeline but is not a current trading quote.
- The history resources were retrieved between **18:53:20Z and 18:53:25Z** and had later cache expiry. History is backward-looking and is not a sales forecast.
- Each of the three live market-order endpoints returned one page (`X-Pages: 1`). Live multi-page traversal was not exercised in this collection; pagination remains covered by automated tests.
- The saved source URLs use ESI's `/latest` path. This dataset remains valid evidence of the responses collected. Synchronize the local collector to the current repository version before the next live collection.
- The summary does not include market fees, installation costs, character/facility adjustments, hauling, or authorized Upwell structure access. A public regional snapshot does not prove access to every order location.

### M1 disposition

**M1 is complete for the bounded SDE/ESI sample demonstrated here.** The SDE archive was downloaded, integrity-checked, extracted, and parsed locally; parser aggregate counts and incomplete-field counts are recorded. The bounded public ESI collection and schema-v4 target-location summary were reviewed for collection provenance, order/history coverage, range resolution, per-fill minimum volume, and internal arithmetic.

This is not a claim that every SDE recipe record has been audited, every market type or region has been collected, live multi-page traversal has been observed, or the uploaded order book remains current. Those are distinct tasks for candidate generation and a live product evaluation.



## Local SDE recipe quality audit review (2026-11-14)

The user ran `tools/sde/audit_industry_recipes.py` against the normalized recipes from SDE build **3698585** and uploaded the compact report `industry-recipes-audit.json` to Dropbox. The report was reviewed on **2026-11-14**. Its source JSONL SHA-256 is `00ef1d53a92f217832f490dc5563e1e364cdd1224f7469103ff7da4e92ae7c7c`.

### Record and key integrity

- [x] **5,022** recipe records: 4,902 manufacturing and 120 reaction activities.
- [x] **5,022** unique blueprint/activity keys; zero duplicate keys and zero invalid keys.
- [x] Zero record-validation issues, invalid recipe items, or duplicate item IDs within recipe lists.
- [x] **5,005** recipes are marked complete and **17** are incomplete because their source material arrays were omitted. These 17 must not be costed as zero-input recipes.
- [x] **137** records omit required-skill arrays. The parser preserves that source state; skill-array omission does not make the material bill incomplete, but the missing skill data remains unknown for feasibility screening.

### Type metadata and exceptional records

- The report contains **811** unpublished blueprint records and **580** unpublished product type IDs. These are not ordinary candidate outputs and must be filtered from the normal candidate universe.
- There are **21** distinct unresolved type IDs: 20 product references with missing names and one material reference with a missing name. Publication state is also unknown for those records. Do not infer that they are marketable, purchasable, or valid candidate outputs.
- The report records **54** unpublished material references. Inputs marked unpublished or unresolved require explicit treatment; do not assume they can be purchased from the ordinary market.
- One recipe has a zero-second base time: blueprint type ID **34256**, the Vargur Krusual Edition Blueprint. EVE Ref lists a zero-second manufacturing time, one Vargur as the input, and one Vargur Krusual Edition as the output. This is retained as an exceptional SDE record, not treated as a normal throughput candidate. [EVE Ref: Vargur Krusual Edition Blueprint](https://everef.net/types/34256)
- In the refreshed report, all **9,360** required-skill references have resolved names and known publication status: **9,225 published** and **135 unpublished references**, with **zero unknown-publication references**. These are reference counts, not distinct skill-type counts. The SDE `published` flag is retained for downstream review; do not infer trainability or current character eligibility from this flag alone.

### Candidate-generation controls

The candidate scanner must require, at minimum:
1. A complete material list and a resolved name/type reference for every input.
2. A published blueprint and a published, resolved output.
3. A positive base manufacturing time for ordinary throughput ranking.
4. An actual Industry quote for current material quantities, output, duration, and installation fee.
5. Independent confirmation of market access, procurement availability, and realistic output liquidity.

Unpublished, unresolved, incomplete, and zero-time records should be excluded or placed in an explicit manual-review queue. The audit validates the normalized file's structure and joined metadata; it does not independently re-parse the source SDE rows or establish marketability, feasibility, or profitability.

### Q016 disposition

**Q-016 is resolved for the current normalized SDE build.** The local audit has been executed and reviewed. Its identified exceptions are now explicit downstream filters and known limitations; they are not reasons to treat the entire normalized recipe dataset as unusable. The required-skill publication-field omission is recorded as a representation limitation for a later parser enhancement, not as a failed recipe audit.




## Required-skill publication metadata follow-up (2026-11-14)

Review of the uploaded recipe audit showed all **9,360** required-skill references with unknown publication status. Code inspection identified a normalization omission: `load_type_metadata()` already reads each type's `published` flag, but the required-skill serializer previously emitted only type ID, name, and required level.

The parser now includes the joined `published` value in each normalized required-skill entry and preserves `null` when the skill type metadata is unresolved or lacks the flag. This does not change the underlying skill requirement or infer publication status. Regression tests cover both a known published skill and missing skill metadata.

**Local follow-up required:** the existing `industry-recipes.jsonl` and `industry-recipes-audit.json` were generated before this correction. Re-run the parser against the already-extracted SDE build 3698585, then rerun the audit. Upload only the refreshed compact audit report. Do not upload the normalized JSONL or raw SDE data. Until that refresh is reviewed, do not quote a new skill-publication count or claim the existing report reflects the updated parser.

## Local operating-profile readiness review (2026-11-14)

The user ran `tools/profile/readiness_report.py` against the private local profile and uploaded the privacy-safe `profile-readiness.json` report. The report is valid (`profile_schema_valid: true`) with **zero validation errors**, but it confirms that the local profile is still effectively the blank example template.

### Reported state

- All three character slots are `unknown`; each has zero recorded skills and unknown Manufacturing, Science, and Reaction free-job capacity.
- Blueprint inventory is unknown, with zero records.
- Facility inventory is unknown, with zero records and zero verified facilities.
- Market access has not been entered; there are no procurement or sales locations in the profile.
- Working capital, liquidity reserve, and maximum capital at risk are unknown.
- Weekly active hours, maximum setup time per batch, liquidation target, and risk tolerance are unknown.
- Logistics method and practical limits are unknown/not entered.
- The report confirms that it contains no character labels, skill IDs/levels, blueprint IDs, market location IDs/names, or ISK amounts.

**Interpretation:** This is evidence that the profile used to generate the report has not yet been populated. It is not evidence that the characters have no relevant skills, that no blueprints are owned, or that no facilities/markets are accessible. Unknown fields must remain unknown and must not be interpreted as zero or unavailable.

### Authentication status and project boundary

No EVE SSO authorization has been requested or used in the workflow completed to date. The SDE download and public ESI market-data collection use public resources. The local profile is a manually populated, local-only input; it is not automatically populated from the EVE launcher session.

Private character/account information is intentionally deferred to **M8 (optional local EVE SSO integration)**. Until that milestone is explicitly selected and implemented, there should be no EVE login prompt, OAuth token, refresh token, client secret, or authenticated ESI request. The manual profile workflow remains usable without SSO.

### M2 disposition

M2 remains **in progress**. The schema, validator, feasibility screen, and safe readiness report work, but the operating profile has not yet been populated or verified. A useful first product evaluation needs only the relevant subset of the profile, but the necessary character eligibility, blueprint, facility, procurement/sales access, working-capital, and attention assumptions must be entered or explicitly left unknown.


## Refreshed SDE recipe audit after skill metadata correction (2026-11-14)

The user regenerated `industry-recipes.jsonl` using the corrected parser and uploaded a refreshed `industry-recipes-audit.json`. The report was retrieved from Dropbox root path `/industry-recipes-audit.json`, modified **2026-11-14T22:32:59Z**. Its source JSONL SHA-256 is `53d97771b76d077c5b241a282d207e1cbc00c049aa602d5a43a526ae7d1191ba`, confirming that it is a different generated artifact from the prior report.

The refreshed report preserves the same **5,022** recipes (4,902 manufacturing, 120 reaction), 5,005 complete and 17 incomplete material records, 5,022 unique blueprint/activity keys, and zero duplicate keys, invalid keys, record-validation issues, invalid recipe items, or duplicate item IDs.

The parser metadata correction is validated against the live SDE-derived dataset:
- Required-skill references: **9,360 total**.
- Missing required-skill names: **0**.
- Unknown required-skill publication references: **0**.
- Published required-skill references: **9,225**.
- Unpublished required-skill references: **135**.

The 135 is a reference count, not a distinct type-ID count. The compact audit currently does not include unpublished skill IDs or unique unpublished skill counts. Preserve the flag and route such skill requirements through explicit downstream review; do not infer trainability or character eligibility solely from SDE publication status.

The remaining product/material/blueprint metadata exceptions are unchanged from the earlier audit: 21 unresolved type IDs (20 product, one material), 580 unpublished product type IDs, 54 unpublished material references, 811 unpublished blueprint records, and one zero-time recipe (blueprint type 34256). The 17 incomplete material recipes remain ineligible for costing as zero-input recipes.

**Q-017 is resolved for SDE build 3698585.** Parser regression tests and a regenerated report demonstrate that required-skill publication metadata is now preserved and all skill references have known publication status in this normalized output. The unpublished-reference cases remain flagged for downstream handling; this resolution does not claim that those skills are trainable or untrainable.

## Audit version 2 review and skill-reference preparation (2026-11-14)

The newest local audit was uploaded to Dropbox root path /industry-recipes-audit.json, modified **2026-11-14T22:41:30Z**. This report is audit version 2. The older copies moved into Eve-Online-Industry-Stale-Files were not used.

The version 2 results confirm:
- **9,360** required-skill references, all with resolved names and known publication status.
- **9,225** published skill references and **135** unpublished references.
- **24 distinct unpublished skill type IDs** account for the 135 unpublished references.
- **Zero** distinct skill IDs have unknown publication status.
- **5,022** unique blueprint/activity keys and zero duplicate keys or record-validation issues.

The unpublished type IDs remain exceptions for review. A publication flag is not evidence that a skill can or cannot be trained, nor does it reveal whether an existing character has a historical skill level.

### Next local reference

A local tool, tools/sde/build_skill_requirements.py, now derives a skill-coverage reference from the normalized recipe JSONL. It retains all observed skill types, ranks requirements by the number of statically eligible recipes, and preserves exclusion reasons for incomplete recipes, unpublished blueprints/skills, unresolved metadata, and unknown skill arrays. The reference intentionally stays in Git-ignored data/derived/. Its local execution and report review are still pending.

This tool is a profile-preparation step only. It does not establish actual character skills, blueprint ownership, facility access, marketability, or profitability.
