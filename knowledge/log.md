## 2026-11-15 - Redacted importer diagnostics

- Extended the readiness report to read the local import manifest and translate private importer warnings into generic, slot-scoped `skills_diagnostic_codes` and `job_capacity_diagnostic_codes`. The report does not expose raw warning text, character IDs/names, skill IDs/levels, blueprint identifiers, or asset/job item IDs.
- Added reason-code coverage for stale snapshots, completed-but-unreflected skill-queue entries, malformed/unreadable queue entries, malformed or unrecognized industry-job activity/status records, unverified free-slot counts, and capacity blocked by partial skill data.
- Updated the documented report-regeneration command to include the private manifest. No ESI sync or reauthorization is required to regenerate the report from the existing local profile and manifest.
- GitHub Actions run [43677050949](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43677050949) passed the full repository validation suite after the diagnostic tests were corrected.

## 2026-11-15 - First live three-character profile import

- Reviewed the user's redacted `profile-readiness.json` from Dropbox. The report is schema-valid with **0 validation errors** and confirms **3 fresh snapshots out of 3**, with no stale snapshots.
- Character slot 1 is verified with 358 known skills; Manufacturing, Science, and Reaction job capacity are each reported available. Character slot 2 is partial with 55 known skills; all three job-capacity values remain unknown. Character slot 3 is verified with 59 known skills; all three job-capacity values are each reported available.
- Personal blueprint inventory is verified for the three authorized characters, with **375 records**. The broader blueprint inventory remains partial because corporation-owned blueprints are outside the current import scope.
- Facility inventory remains unknown (zero verified facilities); market access is not entered; working capital, liquidity reserve, maximum capital at risk, active-hours budget, setup tolerance, liquidation target, and risk tolerance remain unknown; logistics is not entered.
- The report confirms it contains no character labels, skill IDs/levels, blueprint IDs, market-location IDs/names, or ISK amounts. No private profile or raw ESI data was uploaded or committed.
- Next M2 evidence gates: investigate why character slot 2 is partial, verify skill/job data and free slots against the in-game Industry window (including the 90-day completed-job history caveat), inspect asset/location samples, and normalize useful personal assets without assuming every located item is available for industry. Facility, market, capital, operations, and logistics configuration remain separate manual/targeted checks.

# Knowledge Base Log

## 2026-11-14

- Integrated schema-v4 market-summary quotes into the quote-first product evaluator. Material lines can use exact-quantity local-ask VWAPs as replacement-cost estimates; partial procurement quotes are rejected. Sale scenarios can use exact-quantity range-eligible bids, with partial fills treated as sold units and the remainder retained as inventory. The evaluator records source hashes/timestamps and emits snapshot-age/cache-expiry warnings; market and installation fees remain explicit inputs.
- The first CI run exposed a local variable shadowing the Industry quote and a partial-fill test-fixture arithmetic mismatch. Both were corrected. GitHub Actions run [43645289758](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43645289758) passed 41 calculation tests, 5 validation-tool tests, 30 operating-profile tests, 14 SDE parser/audit tests, 27 ESI tests, and 595 Markdown links.

- Completed M1 for the bounded SDE/ESI sample. Reviewed schema-v4 market-summary-v4.json from collection 20261114T185315Z: 516 regional orders, 72 target-location books, 409 history days per mineral, zero unresolved buy-order ranges, no invalid minimum-volume metadata, and consistent 100/1,000/10,000-unit bid sweeps. All 72 target books fully covered the requested sell-into-bids quantities; local ask-side procurement was less uniform (41/72, 40/72, and 37/72 books fully covered 100, 1,000, and 10,000 units respectively).
- Recorded that the source order snapshots were retrieved around 18:53:19Z-18:53:24Z and ESI cache windows expired around 18:53:55Z-18:54:05Z, well before the summary's 21:18:56Z upload. The file validates the pipeline but is not a live execution quote. The three sampled order endpoints each returned one page, so live multi-page traversal remains untested.
- Compared v3 and v4 bid sweeps: all 216 sample quantity/location results were numerically unchanged. Schema v4 remains canonical because its per-fill minimum-volume semantics and caveat are corrected. Q-016 tracks a compact local SDE record-level quality report before the candidate scanner treats the full recipe universe as complete.

- Added a redacted local profile-readiness report and hardened profile enum validation so malformed data produces validation errors instead of runtime exceptions. The readiness report exposes statuses and counts only, omitting character labels, skill IDs/levels, blueprint and facility identifiers, market names/IDs, and ISK values. Validation passed in GitHub Actions run [43643637137](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43643637137).
- Added the quote-first manufacturing product evaluator. It reconciles the normalized SDE recipe with actual Industry-window quote quantities, job durations, output, and installation fee, then compares explicit sale strategies. The first version does not calculate unverified ME/facility material rounding and does not apply a risk premium. Its synthetic regression suite passed run [43642951268](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43642951268).
- Added the local normalized-recipe quality audit for completeness, duplicate blueprint/activity keys, metadata joins/publication flags, repeated item IDs, and exceptional records. It writes a compact report under ignored `data/derived/`; the raw recipe file stays local. Validation passed in run [43644007867](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43644007867).
- Added an exact-quantity adapter for schema-v4 market summaries. It extracts precomputed procurement or liquidation sweeps only for quantities present in the summary, retains source timestamps/hashes and fillability, and does not extrapolate, apply fees, or infer structure access. Validation passed in run [43644121568](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43644121568).
- M1's bounded SDE/ESI review is complete. Remaining local evidence gates are the record-level SDE audit (Q-016), completion of the private operating profile (M2), and one real product evaluation (M4). No private account profile or raw SDE/ESI data was committed.

- Corrected the M1 evidence boundary: the SDE parser console output confirms aggregate counts only (5,022 outputs from 5,045 activities examined; 23 skipped; 17 omitted/null material arrays; 137 omitted/null skill arrays). The generated JSONL was not provided for record-level inspection, so the audit no longer claims verified per-record joins, publication flags, uniqueness, or exceptional recipe values.
- Corrected the ESI summarizer's schema-v4 explanatory caveat and added a regression assertion to prevent obsolete v3 wording from returning. Schema v4 applies `min_volume` to each individual fill and permits a below-minimum final fill only when it consumes the buy order's entire below-minimum remaining volume.
- Updated the initial ranking KPI to unadjusted net contribution per active operator-hour, with risk shown separately until pilot data supports a defensible calibration.

- Completed the first bounded public regional ESI collection for The Forge (region 10000002) and Tritanium/Pyerite/Mexallon (type IDs 34/35/36). All three order-book and history requests returned HTTP 200 with one order page each; the market-prices request returned 304 and reused a valid cached body; industry systems returned 200. The summary covered 516 order records with no duplicate IDs and 409 historical rows per mineral from 2025-10-01 to 2026-11-13. The region-wide Pyerite and Mexallon books appeared crossed, demonstrating that regional best bid/ask composites cannot be treated as executable spreads because orders can be at different locations. Recorded the live collection and the limitation in the M1 audit.
- Extended the ESI market summarizer with a clearly identified region-wide composite, a crossed-book warning/flag, per-location order-book groups using ESI `location_id`, system IDs where provided, and missing-location counts. Bumped summary schema to version 2 and added tests for location grouping, crossed composite detection, missing location IDs, and schema version. The location view remains screening-only because buy-order range, `min_volume`, structure access, and fees are not fully modeled. Local summarizer execution against the just-collected raw files is still required.
- The user's local ESI collector output used the old `/latest` URL base, while the current repository collector uses the unversioned ESI base with a pinned compatibility date. Preserve the successful collection as evidence but synchronize the local collector/summarizer before the next collection. Raw market data and local profiles remain uncommitted.


- Completed local execution of the corrected recipe parser against CCP SDE build **3698585**. The user-provided console output confirms **5,045** activity records examined, **5,022** normalized recipes written, **23** activities skipped because no product array was available, **17** omitted/null material arrays, and **137** omitted/null skill arrays. The generated JSONL was not supplied for direct record-level review, so this evidence does not establish activity-type breakdowns, duplicate-key status, individual metadata joins, publication counts, or exceptional recipe IDs. An earlier version of this log overstated those details; the M1 audit now records the evidence boundary accurately. The SDE parser correction passed GitHub Actions run [43623419034](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43623419034). The bounded ESI collection has since been completed; schema-v4 local execution remains pending.


- Added optional active-operator-hour accounting to the batch profitability calculator and documented the primary attention-efficiency KPI across the computation, economic concept, product-selection workflow, and evaluation playbook. The metric uses attributable hands-on time only; unattended job duration and passive waiting are excluded, missing/zero time yields an unknown metric, and risk premiums remain unadjusted until pilot data supports calibration. GitHub Actions run [43586733668](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43586733668) passed the calculation regression tests and all repository validation groups.
- Corrected the market fee estimator to apply a 100 ISK minimum to non-immediate order creation and relisting when the order value is positive. Added small-order regression tests and documented that the minimum is supported by EVE University rather than explicitly stated in CCP's linked fee page, so live order quotes remain authoritative for low-value orders. Also clarified the separate 0.5 percentage-point SCC component in Upwell broker fees using CCP's Viridian example. GitHub Actions run [43587112979](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43587112979) passed all six validation groups: 22 calculation tests, 5 repository-validation tests, 19 operating-profile tests, 7 SDE parser tests, 13 ESI tests, and 591 local Markdown links.

- Continued M1/M2 work while local desktop execution is unavailable. Added a current-format SDE recipe parser for manufacturing and reactions, joining type names from `types.jsonl`, plus fixture tests. Added an ESI order-book/history summarizer that combines paginated regional books, calculates visible ask/bid VWAP depth at target batch quantities, summarizes daily history, and records source hashes. Added network-free collector tests for URL construction, HTTP-date handling, Retry-After, and pagination.
- Added a profile feasibility screen that distinguishes eligible, ineligible, and unknown results using verified skills, job capacity, blueprint ownership, and facility services. Revised the private profile schema to key skills by SDE type IDs and to track whether skill, blueprint, and facility inventories are complete. This prevents missing data from being misclassified as non-ownership or untrained skills.
- Current CI run [43585568060](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43585568060) passed all six check groups: 17 calculation tests, 5 repository validation tests, 14 profile/feasibility tests, 7 SDE parser tests, 6 ESI market summary tests, and 591 local Markdown links. A further ESI collector regression-test file has since been added and is awaiting its own CI confirmation.
- Expanded the SDE recipe output with published status, group/market-group IDs, tech level, portion size, and volume metadata. Expanded ESI normalization to deduplicate order IDs across numerically ordered pages and retain each raw file's collection timestamp, cache status, expiry, ETag, and SHA-256 provenance. Added schema/validator contract tests and updated CI path filters so changes under `tools/profile/`, `tools/sde/`, `tools/esi/`, and `config/` trigger validation.
- GitHub Actions run [43585870286](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43585870286) passed all six validation groups: 17 calculation tests, 5 repository validation tests, 19 profile/schema/feasibility tests, 7 SDE parser tests, 13 ESI tests, and 591 local Markdown links. The subsequent documentation-only run [43585889672](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43585889672) also passed.
- These are fixture-tested implementations only. Actual ingestion against the latest CCP archive and live ESI responses remains pending; no market opportunity or profitability recommendation has been generated.

- Added a standard-library operating-profile validator and six unit tests, integrated into the unified validation runner. The public example remains intentionally unknown/null until populated locally. GitHub Actions run [43584676836](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43584676836) passed 17 calculation tests, 5 validation tests, 6 profile tests, and 591 local Markdown links across 100 Markdown files.
- Accepted the operational manufacturing decision-support roadmap as the working plan and started M1 (public data foundation) and M2 (local operating profile) in parallel. Added an M1 audit documenting the current CCP SDE build 3698585 (2026-11-13), current JSONL/ESI source contracts, existing collector code-review findings, and execution evidence still required. Added a versioned JSON Schema and safe three-character example for the private local operating profile, with instructions to keep populated character, blueprint, facility, and capital data out of the public repository. No private operating values were committed.

- Clarified and recorded the project's primary use case: evaluate manufacturing products and identify realistic opportunities for a low-attention, predictable-turnover null-sec operation, prioritizing ISK per active operator-hour over unnecessary vertical integration. Added a proposed milestone roadmap and aligned the project charter/backlog. Added Git ignore rules for private local operation profiles and exports; exact character, asset, and financial details are not stored in this public repository.
- Added GitHub-native research/improvement and verification/defect issue templates plus a pull request checklist. Linked the intake process from the root README, LLM onboarding, and research-management index; updated CI path filters so template-only changes trigger validation.
- Published a VS Code/PowerShell LLM Workflow Quick Start covering baseline capture, task packet creation, branch workflow, model-role routing, validation, and handoff closeout. Updated all onboarding and calculator documentation to use the single local validation command.
- Added a standard-library Markdown link checker, five unit tests, and a one-command local validation runner. GitHub Actions now executes the same `py -3 tools/validation/run_all.py` command for relevant code and documentation changes. The first scan found and corrected four broken root-relative links in the blueprint concept. [GitHub Actions run 31](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43578869255) passed 17 calculation tests, 5 validation tests, and 579 local links across 94 Markdown files.

## 2026-11-14

- Reworked the LLM collaboration protocol into an operational workflow with bounded tasks, portable context packets, coordinator/researcher/reviewer/implementer roles, blind-first independent review, synthesis, validation gates, and human-controlled integration. Updated onboarding and added provider-neutral role prompts plus task, research, review, and change-proposal templates.
- Fixed the manufacturing profitability calculator's decimal quantity formatting, which caused the CI suite to fail when whole-number quantities were rendered in scientific notation. Added regression tests for whole numbers, large values, fractional values, and zero. GitHub Actions run 14 passed all 17 calculation tests.

## 2026-11-14

- Added a deterministic market fee estimator for Accounting sales tax, NPC broker fees, Upwell structure owner fees, and relist fees, with a JSON example and unit tests. Live order quotes and wallet records remain authoritative.
- Added a deterministic manufacturing-profitability calculator with JSON inputs, partial-sale inventory accounting, full-batch projections, break-even and target-margin pricing, slot-hour/elapsed-hour metrics, and maximum affordable input-price analysis. Added example scenarios, unit tests, and a GitHub Actions test workflow. The illustrative scenario is not live market data; the CI result still needs confirmation.
- Added a deterministic hauling-cost computation and standard-library Python calculator with a JSON scenario template and unit tests. It compares self-haul and courier costs from the cargo owner's perspective, including expected cargo/ship loss, collateral coverage, pilot time, and capital exposure. Real route probabilities remain user-supplied scenario inputs.

- Initialized the EVE Online industrial knowledge repository scaffold.
- Established OKF v0.2 as the target format.
- Added governance, source-quality, LLM-collaboration, concept, and handoff templates.
- Created a comprehensive topic map and initial research backlog.
- Researched and replaced the Blueprints and Research placeholder with a source-backed draft covering BPOs, BPCs, ME/TE research, material rounding, and copying behavior.
- Added CCP source URLs, source update dates, and a current 2026 LP-store BPC example to the official source catalog.
- Researched and replaced the Skills and Job Capacity placeholder with a source-backed draft covering Manufacturing, Science, and Reaction pools, slot formulas, prerequisites, remote operation, and Alpha limits.
- Added CCP and EVE University source entries for skill and job-capacity research.
- Researched Facilities and Rigs, documenting Upwell families, engineering/refinery roles, industrial service modules, job interruption risks, rig specificity, and reaction rig distinctions.
- Replaced Installation Cost Computation with the CCP fee formula, EIV basis, tax components, structure SCI bonuses, ESI inputs, and activity-specific exceptions.
- Added Industrial Cost Accounting conventions to distinguish EIV from acquisition, replacement, and opportunity cost.
- Added unresolved questions for temporary ME/TE SCC relief, non-manufacturing EIV/value bases, and live verification of rig stacking and location-specific modifiers.
- Researched and replaced the Tech I Manufacturing placeholder with a source-backed draft covering job installation and delivery, BPO/BPC use, output-per-run, per-job material rounding, skill/structure/rig time and material models, and planning constraints.
- Added CCP Industry UI and additional community formula/calculator references. The combined material/time formulas are labeled provisional pending controlled in-game quotes.
- Added research questions for 30-day job-duration limits, BPO concurrency, and precise modifier/rounding behavior.
- Corrected an Upwell rig uniqueness description to match CCP's rule that two rigs affecting the same attribute cannot be equipped together.
- Normalized the Upwell structure-browser source identifier in Installation Cost Computation.
- Researched and replaced the Tech II Invention placeholder with a source-backed draft covering required inputs/skills, the current skill-adjusted success formula, base chance categories, decryptor modifiers, output BPC runs/ME/TE, and expected-cost calculations.
- Added official CCP invention, decryptor, datacore, and historical Phoebe patch-note sources, plus a current EVE University invention reference last modified 2026-10-09.
- Added open verification questions for probability rounding/capping and multi-run datacore/decryptor consumption.
- Researched and created a dedicated Blueprint Copying concept documenting the separate Job Runs and Runs per Copy fields, BPC inheritance, licensed-run limits, exceptional input scaling, base copy-time model, related skills, and operational purposes.
- Linked Blueprint Copying from the production systems index and Tech I Manufacturing guide. Clarified invention expected-cost allocation so multi-run datacore/decryptor quantities must come from actual job inputs.
- Added verification questions for copy-time modifiers, same-BPO concurrency, and the copy-specific input/fee scaling model.
- Researched and replaced the Tech II Components placeholder with a source-backed draft covering raw moon materials, intermediate/composite reactions, Advanced Component manufacturing, Tech II final input categories, skill dependencies, R.A.M. material behavior, and vertical-integration decisions.
- Added CCP's historical R.A.M./R.Db conversion reference and documented the limits of historical damage-per-run mechanic claims.
- Added an open question for a type-level, versioned Tech II component/recipe/skill dataset and independent quote validation.
- Researched and replaced the Reactions placeholder with a source-backed draft covering reactor families, Refinery/security constraints, reaction job lifecycle, moon-material intermediate/composite reaction tables, special reaction exceptions, Hybrid and Biochemical/Molecular-Forged families, and reaction economics.
- Linked the reaction and Tech II component concepts, added the EVE Omnitool reaction calculator to the community reference catalog, and recorded open questions for SDE/in-game recipe validation and a complete Molecular-Forged formula catalog.
- Documentation milestones do not constitute independent in-game verification; all three new concepts remain draft.
- Refreshed Facilities and Rigs against current SDE-derived structure and rig attributes, added manufacturing versus reaction security multipliers, and corrected rig uniqueness to same rig type including T1/T2 variants.
- Researched and replaced the Tech III Manufacturing placeholder with a source-backed four-stage production chain, relic/output mapping, sourcing, skill dependencies, and expected-attempt framework.
- Recorded a material conflict: CCP's Ancient Relics article lists 40%/35%/25% base success chances, while EVE University and sampled SDE relic outputs show different percentages. No formula was inferred; live Industry-window verification remains open.

- Researched and replaced the Planetary Industry placeholder with a source-backed colony, extraction, processor, skill, routing, export, tax, Skyhook, and Alpha-restriction concept.
- Replaced the Planetary Commodities placeholder with P0-P4 tiers, P0-to-P1 mapping, P1-to-P4 recipe reference tables, and standard schematic batch structures. These remain draft pending reconciliation against the post-2025 CCP SDE.
- Added CCP Planetary Interaction, Orbital Skyhook, Equinox, and current SDE documentation to the source catalog. Recorded the EVE University PI overview's explicit Equinox-update warning and the 2025 SDE schema break.

- Researched and replaced the Market Fees and Taxation placeholder using CCP's March 2026 fee article and official order-matching/relist documentation. Documented NPC station, Upwell structure, Accounting, Broker Relations, and relist mechanics.
- Researched and replaced the Manufacturing Profitability placeholder with batch-level economic cost, net proceeds, contribution, margin, ROI, slot-hour, break-even, and sensitivity frameworks.
- Replaced the Manufacturing Profitability Computation placeholder with deterministic input schemas and equations. Updated navigation and backlog; live fee/market validation and a worked current-price example remain open.

- Researched and replaced the Market Location Economics placeholder with a source-backed framework for activity-specific SCI, facility selection, ESI market data, remote installation, logistics, and total landed cost. A live location comparison remains open until current market and facility data are selected.

- Researched and replaced the Logistics and Risk placeholder with self-haul economics, courier-contract collateral/failure behavior, route exposure, Upwell Asset Safety exceptions, and risk-adjusted logistics cost formulas. Live route-specific risk and hauling-cost calibration remain open.

- Researched and replaced the Capital and Asset Management placeholder with working-capital, inventory, capital-turnover, asset-concentration, and capital-allocation guidance.
- Replaced the Capital Turnover Computation placeholder with dated cash-flow, peak working capital, capital-days, inventory-turnover, collateral, and cash-conversion formulas. Live production-cycle validation remains open.

- Researched and replaced the Manufacturing Throughput placeholder with slot-capacity formulas, job/output rate calculations, BPO/BPC parallelism constraints, batch-rounding considerations, and normalized bottleneck analysis. Independent in-game schedule and quote validation remains open.

- Researched and replaced the Science and Invention Throughput placeholder with shared Science slot-hour budgeting, ME/TE research and copying output rates, expected invention BPC/run formulas, and Science-to-Manufacturing bottleneck analysis. Live mixed-schedule validation remains open.

- Researched and replaced the Reaction Throughput placeholder with Reaction slot-hour budgeting, formula input/output rates, reactor and security constraints, time/material rig effects, and normalized reaction-chain bottleneck analysis. Live formula/rig quote validation remains open.

- Researched and replaced the Production Scheduling placeholder with a resource-constrained scheduling framework for Manufacturing, Science, and Reaction pools, including dependencies, blueprint/material/facility constraints, critical path, batch release, and replanning.

- Researched and replaced the Character Specialization placeholder with role profiles for Manufacturing, Science/Invention, Reactions, Market/Trade, and PI, plus a marginal skill-value framework and multi-character role allocation principles.

- Researched and replaced the Industrial Scaling placeholder with a framework for character/facility/region expansion, vertical integration, sustainable output constraints, economies/diseconomies, incremental capital return, and asset concentration controls.

- Researched and replaced the Market Mechanics placeholder with CCP order-matching rules, buy/sell order location/range behavior, regional market history, adjusted-price distinctions, ESI endpoints, and cache-handling requirements.

- Researched and replaced the Demand and Liquidity placeholder with historical volume/transaction analysis, order-book depth, VWAP execution, spread, liquidation horizon, volatility, and market absorption metrics. Clarified that ESI order_count represents completed transactions rather than currently open orders.

- Researched and replaced the Price Analysis placeholder with executable price definitions, historical trend measures, volume-weighted execution valuation, volatility, outlier handling, adjusted-price/EIV separation, and data-provenance rules.

- Researched and replaced the Regional Arbitrage placeholder with a quantity-aware model for source procurement, destination liquidation, market fees, hauling, risk-adjusted loss, capital time, and false-arbitrage screening.

- Researched and replaced the Product Selection placeholder with a multi-criteria framework for feasibility, contribution, slot/capital efficiency, liquidity, make-versus-buy, portfolio risk, and Pareto screening. Live product ranking remains open until a market region, character skills, and operating constraints are selected.

- Researched and replaced the ESI and Market Data placeholder with current ESI versioning/compatibility dates, OpenAPI transition, SSO scopes, caching, rate limiting, pagination, industrial endpoint map, and SDE/ESI separation. Implementation remains open.

- Researched and replaced the Data Quality and Reconciliation placeholder with claim classes, evidence hierarchy, source/ESI/SDE provenance, freshness, normalization, validation dimensions, conflict resolution, and verification-state controls.

- Researched and replaced the Third-Party Industry Tools placeholder with a current tool survey covering EVE Retroindustry, EVE Cookbook/MCP, EVE Omnitool, EVECalc, EVE Online Industry Calculator, and PI planners. Recorded data freshness, feature scope, privacy, SSO, and verification caveats.

- Added draft operational playbooks for product evaluation, Tech I/II production, PI, reactions, and market delivery; indexed them and retained draft status pending live workflow validation.
- Added Q-014 to record the operating-environment inputs needed for a real product-ranking example. Continued work can proceed on generic mechanics and data tooling without blocking on those details.

- Corrected an Alpha-clone PI restriction after checking CCP's current February 2026 Alpha/Omega article and July 2024 quick facts: Alpha clones can import materials into colonies but cannot export colony goods. Updated the Planetary Industry concept, PI playbook, character specialization guidance, and official source catalog; the older PI support article's broader wording is now explicitly noted as less precise.

- Added local CCP SDE acquisition tooling: a standard-library downloader that records build/URL/hash metadata and verifies ZIP integrity, plus an archive inspector. Added usage documentation and ignored raw/generated data paths in Git.
- Updated the root README to reflect the current research repository state and local SDE workflow.

- Resolved the SCC surcharge research question at the documentation level: CCP's 2025-07-18 post reduced ME/TE research surcharge from 4% to 2% and described the reduction as temporary. No later official reversal was found as of 2026-11-14; live in-game quote verification remains open. Replaced the Installation Costs foundation placeholder with an overview linking to the detailed fee computation.

- Added a standard-library, read-only ESI collector for public market orders/history, adjusted prices, and industry system indices. It pins an explicit compatibility date, respects cache/ETag headers, handles X-Pages, honors 429 Retry-After, stops on 420 error-limit responses, and writes timestamped raw data with hashes/provenance. Local execution and schema validation remain open.

- Added deterministic Invention Economics and Research Investment ROI computations. The invention model uses batch-level expected outputs and binomial variance; the research model values incremental ME material savings and TE time savings against Science/Manufacturing slot-hour opportunity costs.

- Replaced the Industry Overview placeholder with a taxonomy of industrial activities, job pools, resource sources, product families, and economic constraints.
- Replaced the Advanced Manufacturing placeholder with a sourced map of Tech II/III, capital ship, Upwell structure, booster, and faction/storyline production chains and their facility/service dependencies.

- Added a structured verification-protocol suite covering ME rounding, BPC copying, job slots/remote range, facility/rig modifiers, installation fees, invention, reactions, Alpha PI permissions, ESI collector, and SDE acquisition.
- Updated the verification queue to distinguish source-documented claims from claims that still require independent in-game or local execution checks. Reclassified the ME/TE research SCC surcharge question as source-resolved with live quote confirmation still open.
- Added Q-015 for local SDE/ESI tool execution and sample-schema review; generic research can continue while that input is pending.

- Replaced Minerals and Ore, Moon Materials, Gas and Fullerites, Sleeper Salvage, and Procurement and Reprocessing placeholders with source-backed concepts. Avoided stale ore-location/yield tables, recorded current moon extraction and gas-family mechanics, separated Sleeper blue loot from Ancient Salvage, and documented reprocessing formulas with explicit warnings where the community reference is flagged for update.




- Reviewed the uploaded v2 The Forge market summary: 516 unique orders across Tritanium, Pyerite, and Mexallon; 72 location books reconcile to the regional counts. The most active observed location (60003760 / system 30000142) held 57.6% to 68.0% of each type's order records. Regional Pyerite/Mexallon crossed composites were not crossed at this location. Upgraded the ESI summarizer to schema v3: target-location books expand buy-order ranges through the SDE stargate graph and enforce buy-order min_volume against the original sell-order size; the prior posted-location groups remain for provenance. Local execution against saved raw files is pending.

- Refined SDE jump-range handling: numeric buy-order distance is computed in the source-to-target direction using a reverse-graph BFS over the full stargate network. The buy order and target must be in the queried market region, but the shortest path may transit other regions. Added regression coverage for a cross-region transit route.

## 2026-11-14 - Reprioritize authenticated character-data acquisition

- Accepted the user's strategy correction: use local EVE SSO/ESI to import all three industrial characters' skills, skill queue, personal blueprints/assets, and active industry jobs rather than manually transcribing profile data.
- Promoted native PKCE SSO integration from deferred M8 to the immediate M2 implementation path. Minimum initial scopes and endpoint mapping are recorded in `knowledge/10-research-management/esi-authenticated-data-plan.md`.
- Confirmed the data boundary: ESI is character-oriented with no account-level endpoints, so each of the three characters requires separate authorization. Keep refresh tokens in the Windows credential store and private API snapshots under ignored `data/private/`/`local/` paths.
- Recorded a material facility-access limitation: no unified ESI route enumerates every Upwell structure a character can access. Use public facilities plus targeted character structure search/resolution and retain partial/unknown coverage.
- Deferred alliance-specific doctrine, buyback, shared corporation resources, staging market, and courier details until an alliance is selected. Keep three candidate strategy tracks: alliance-local manufacture, value-added export to higher-paying markets, and other high net-contribution-per-active-operator-hour opportunities.

## 2026-11-14 - Local SSO importer implementation

- Implemented a read-only native OAuth Authorization Code with PKCE client in `tools/esi/sso_local.py`. It discovers SSO metadata, validates signed JWT access tokens, checks audience/issuer/expiry and character subject, and validates the seven requested read/search scopes.
- Refresh tokens are stored using the OS keyring package with no plaintext fallback. The local client config is excluded from Git; raw character snapshots and registry data remain under ignored `data/private/esi/`.
- Added paginated pulls for personal blueprints, assets, and active industry jobs, plus skills, skill queue, and the public industry facility directory. Snapshots include per-page response headers, ESI compatibility date, granted scopes, retrieval timestamp, record counts, and SHA-256 hashes.
- Added `tools/esi/requirements-sso.txt`, a safe config example, and regression tests for PKCE, scope construction, and loopback redirect validation.
- Live SSO authorization and character imports remain unverified until the user registers a local EVE SSO app and authorizes each character.
## 2026-11-15 - Fix EVE SSO JWT issuer validation

- User's first live PKCE authorizations reached the token-validation stage but failed with `Invalid issuer`; no refresh token was saved and no local character was registered.
- Compared CCP's current JWT validation documentation and token issuer update notice. The documented issuers are `https://login.eveonline.com` and legacy `login.eveonline.com`, with no trailing slash. The initial validator incorrectly allowed the HTTPS issuer only with a trailing slash.
- Updated the accepted issuer allowlist and added regression tests for both accepted values and rejection of the slash-terminated value. Repository CI passed all six validation groups; the SSO test module now has 6 tests.
- User should pull the correction and retry authorization for one character before authorizing the remaining two. Do not ask the user to expose access tokens, refresh tokens, authorization codes, or callback URLs containing codes.