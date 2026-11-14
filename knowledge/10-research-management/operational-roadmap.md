---
type: Process
title: Operational Manufacturing Decision-Support Roadmap
description: Proposed milestones for turning the industrial knowledge base into a practical null-sec manufacturing opportunity and decision-support system.
tags:
  - roadmap
  - product-selection
  - manufacturing
  - operations
generated:
  by: openai/gpt-6
  at: 2026-11-14T10:10:00Z
status: active
---

## Status and purpose

**Roadmap state:** Accepted as the working plan on 2026-11-14.

This roadmap translates the user's clarified objective into a sequence of measurable milestones. It should guide new development and reprioritize the existing research backlog. It does not declare any proposed milestone complete unless its acceptance criteria have actually been met.

The purpose is not to maximize theoretical industrial complexity. It is to identify and execute manufacturing opportunities that deliver attractive, realistic ISK returns for a manageable amount of player attention and capital.

## North-star objective

Answer this operational question:

> Given my characters, skills, blueprints, available facilities, market access, and working capital, what should I manufacture right now to maximize realistic profit?

A second use case is to evaluate a chosen item, including a Tech II product:

> What inputs should I acquire, what jobs should I install, where should I produce, how much capital is required, and can I realistically sell the output at an attractive return?

The system should produce recommendations with the evidence, inputs, assumptions, and constraints visible. It should be allowed to say that no current opportunity meets the user's criteria.

## Operating principles

1. **Optimize for player attention, not theoretical maximum margin.** The initial ranking measure is unadjusted net contribution per active operator-hour. Count time spent evaluating, sourcing, staging, installing, adjusting orders, moving goods, and reconciling results. Do not count unattended job duration as active labor. Show risk drivers and low/base/high scenarios separately; do not invent a risk premium before pilot data supports calibration.
2. **Prefer predictable turnover.** Consider liquidity, realistic order-book depth, capital-days, expected liquidation time, and downside scenarios. A high-margin item with a long or uncertain sale horizon may rank below a simpler, faster-turning item.
3. **Start shallow, not vertically integrated.** Assume inputs and intermediate components can be bought. Manufacture upstream inputs only when the incremental return justifies the additional jobs, skills, capital, and attention.
4. **Treat alliance doctrine demand as a useful candidate signal, not guaranteed sales.** Evaluate doctrine relevance alongside actual regional history, order-book depth, local competition, staging-market access, and logistics.
5. **Make market-order management part of the operating model.** Recommendations should account for sales fees, relist costs, competing orders, fill horizon, and the amount of periodic attention required.
6. **Support a three-character industrial profile.** Character skills, available job slots, role specialization, blueprints, and facility access should constrain what the system calls feasible.
7. **Public data first; private account integration later.** Validate public SDE and ESI inputs before considering optional local EVE SSO integration.
8. **Use exploration and gas opportunities as optional supply inputs.** Gas harvesting in an accessible wormhole and materials from relic/data-site activity may be evaluated when convenient. Do not make mining or self-sourcing a prerequisite for the baseline industrial operation.
9. **Separate recommendation confidence from calculation precision.** Deterministic arithmetic does not make uncertain prices, recipe assumptions, facility quotes, or market demand certain.
10. **Keep private operating data local.** Character skills, assets, blueprints, balances, order exports, and credentials must not be committed to the repository.

## Evaluation model

### Primary measure

**Unadjusted net contribution per active operator-hour (initial ranking measure)**

\\[
\\frac{\\text{Net contribution after variable costs}}
{\\text{Active operator-hours}}
\\]

Do not subtract an invented risk premium. Display risk drivers, confidence, and low/base/high scenarios alongside the unadjusted measure. A risk-adjusted ranking may be considered only after pilot observations support a defensible calibration.

### Secondary measures

| Measure | Why it matters |
|---|---|
| Net contribution per batch | Absolute ISK value generated |
| Active operator-hours | Setup and periodic management burden |
| ISK per Manufacturing / Science / Reaction slot-hour | Opportunity cost of character job capacity |
| Peak working capital | Maximum cash committed before proceeds return |
| Capital-days / contribution per capital-day | Return relative to how long capital is tied up |
| Expected liquidation days | How long it may take to turn output back into cash |
| Market depth and planned share of volume | Whether the intended quantity is realistically saleable |
| Material procurement depth | Whether required inputs can be obtained at modeled prices |
| Number of jobs and dependencies | Operational complexity and risk of interruption |
| Low/base/high scenario results | Sensitivity to prices, fees, volume, and time |

Elapsed job time, active player time, character slot-hours, and cash-conversion time are different quantities. Do not collapse them into one generic "ISK per hour" number.

## Scope priorities

### Primary scope

- Tech I and Tech II manufacturing opportunities that fit the user's character skills, capital, market access, and preferred attention level.
- Buying materials and components when that is simpler or more profitable than producing them internally.
- Product candidates associated with alliance fleet doctrines and the markets where those doctrines are supported.
- Public regional market data, historical demand, order-book depth, procurement cost, market fees, installation costs, and logistics.
- Feasible batch sizing, production plans, shopping lists, expected return, and periodic order-maintenance recommendations.
- A local tool that eventually answers the north-star question with ranked, explainable recommendations.

### Opportunistic or secondary scope

- Tech III, reactions, invention, copying, and advanced components where a candidate product warrants the analysis.
- Gas harvesting when an accessible wormhole opportunity exists.
- Relic/data-site rewards as opportunistic material or blueprint sourcing.
- Market trading and order maintenance where the time and fee model supports it.

### Explicitly de-emphasized

- Self-mining as a core material supply strategy.
- Building every possible upstream chain.
- Maximizing vertical integration for a small percentage gain without accounting for added attention and complexity.
- Completing every encyclopedia topic before testing a practical product-evaluation workflow.
- Building a full graphical application before the underlying data and recommendation logic produce useful results.

## Milestones

The roadmap is accepted as the working plan. Milestones M1 and M2 are now in progress. Completion still requires the evidence listed in each milestone's acceptance criteria.

### M0. Confirm the operating objective

**Status:** Agreed at the strategic level.

**Purpose:** Establish the success criteria that govern future decisions.

**Acceptance criteria:**
- [x] Primary objective is practical manufacturing opportunity selection and realistic profit.
- [x] Prioritize ISK return relative to active setup and maintenance time.
- [x] Prefer predictable turnover and semi-passive operation.
- [x] De-emphasize self-mining and unnecessary vertical integration.
- [x] Treat doctrine-related null-sec demand as a primary opportunity source.
- [x] Public data first, with local optional SSO later.
- [ ] Confirm detailed operating thresholds during profile setup and the first pilot.

### M1. Validate the public data foundation

**Status:** Completed for the bounded SDE/ESI sample described in the M1 audit. SDE build 3698585 was acquired, parsed locally, and the schema-v4 The Forge market summary was generated and reviewed. The uploaded order snapshot is stale for live execution; this milestone validates the data pipeline, not a current market feed.

**Purpose:** Establish a reproducible source of current static recipes and public market observations.

**Work:**
- Run the current CCP SDE downloader and record build number, manifest, hash, and relevant schema samples.
- Run the public ESI collector for a small, selected set of regions and product type IDs.
- Validate market orders, market history, system cost indices, adjusted prices, cache behavior, pagination, timestamps, and response provenance.
- Evaluate buy orders at each target location using station, solar-system, numeric jump, or region range; enforce each order's minimum accepted sell-order quantity and resolve numeric distances with the SDE stargate graph.
- Identify the limits of public data for alliance staging markets and Upwell structure markets.
- Define refresh cadence based on ESI cache behavior rather than unnecessary polling.

**Acceptance criteria:**
- [x] A current SDE build is downloaded, integrity-checked, and recorded.
- [x] The current SDE archive was parsed locally and its generated recipe-quality report reviewed: 5,022 records and 5,022 unique blueprint/activity keys, with zero structural issues or duplicate keys. The report identifies 17 incomplete material recipes, unpublished and unresolved type references, 54 unpublished material references, and one zero-time recipe. Candidate generation filters or quarantines these exceptions. Required-skill publication metadata is now present and validated for all 9,360 references; audit version 2 identifies 24 distinct unpublished skill IDs across 135 references.
- [x] A small public ESI collection completes with a manifest and reproducible regional output.
- [x] The bounded collection manifest, order counts, daily history coverage, and location grouping have been reconciled against the uploaded summaries.
- [x] Schema-v4 target-location bid sweeps were generated and reviewed for range and per-fill minimum-volume behavior. The underlying order snapshot had passed its ESI cache expiry by upload time and is not a live quote.
- [x] Missing or private market data is explicitly identified rather than imputed, including the access limitations of regional structure orders and private Upwell structure markets.

### M2. Define the local operating profile

**Status:** In progress. The local profile schema, safe example, structural validator, feasibility screen, and automated tests are in place. The uploaded readiness report is schema-valid with zero errors but confirms that all three character records, blueprint/facility inventories, market access, capital, operations, and logistics remain unknown or unentered. No EVE SSO has been used; the current workflow is manual and public-data-only. The normalized SDE skill metadata correction has been validated against a regenerated local report: all 9,360 skill references have known publication status. Audit version 2 identifies 24 distinct unpublished skill type IDs across 135 references and zero unknown-publication skill IDs. The local skill-reference generator has now been run and reviewed: 4,145 of 5,022 recipe records qualify for static skill mapping (4,026 manufacturing and 119 reaction), identifying 58 published skills for targeted profile capture.

**Purpose:** Make product feasibility depend on the actual operation rather than generic character assumptions.

**Work:**
- Define a local, editable profile for the three industrial characters, their skills, job pools, specializations, and available slots.
- Generate a local skill-requirements reference from complete, published SDE recipes; rank skills by candidate recipe coverage while preserving unpublished and incomplete exceptions.
- Capture relevant blueprint/BPC availability and any limits on location or licensed runs.
- Capture accessible facilities, service availability, rig assumptions, taxes, and production systems.
- Capture market-access locations for procurement and sales, distinguishing NPC stations from Upwell structures.
- Record the preferred hauling method and practical route/time/cargo limits where known.
- Define an operating capital budget, liquidity reserve, and acceptable turnover horizon.
- Record how much active attention the user is willing to spend on setup and periodic maintenance.
- Keep actual character, asset, and financial details in ignored local files, never in tracked public repository files.

**Acceptance criteria:**
- [x] A documented local profile schema exists with a safe example configuration.
- [x] The schema represents all three characters and separates known values from unknown values.
- [x] A feasibility check distinguishes eligible, ineligible, and unknown character, blueprint, and facility requirements. It is a hard-constraint screen, not a job quote or profitability result.
- [x] The profile contract can represent market-access locations and logistics constraints without exposing them in the public repository.
- [x] A local skill-reference generator ranks published, known skill requirements across complete, resolved SDE recipes and preserves exclusion reasons.
- [x] Run and review the skill reference against the local normalized recipe file; it identifies 58 published skills across the full manufacturing/reaction catalog.
- [ ] Enter verified skill levels for the three characters after selecting the first product family and confirming owned blueprints; do not manually inventory unrelated skills yet.
- [ ] The three character records, blueprint inventory, facilities, market access, capital, and attention/logistics limits are populated and reviewed locally.
- [x] No private profile, balance, asset export, or credential is committed to Git.

### M3. Establish doctrine-linked demand and market context

**Status:** Deferred until the target alliance, doctrine set, and staging environment are known. A generic importer can be developed earlier.

**Purpose:** Identify products with plausible demand in the intended null-sec operating environment.

**Work:**
- Import doctrine fittings or other user-supplied doctrine item lists.
- Normalize item type IDs, variants, quantities, and fitted modules.
- Map doctrine-related products to manufacturing blueprints and material requirements.
- Identify staging market, relevant source markets, public/private market data availability, and logistics constraints.
- Compare doctrine relevance with historical volume, transaction frequency, live order-book depth, competition, and current stock/prices.
- Separate direct doctrine items from related consumables and intermediate materials.

**Acceptance criteria:**
- [ ] A doctrine import format is demonstrated using a sample fitting.
- [ ] Imported items map correctly to SDE type IDs.
- [ ] Each candidate's doctrine relationship is visible and traceable.
- [ ] Demand estimates are labeled as estimates unless backed by actual sales/stock data.
- [ ] Staging market data and inaccessible/private markets are clearly distinguished.

### M4. Build a practical single-product evaluator

**Status:** In progress. The quote-first evaluator now validates normalized SDE recipes against actual Industry job quotes and can optionally source exact-quantity material procurement and liquidation estimates from a schema-v4 ESI summary. It records source timestamps/hashes and warns on stale or expired snapshots. It still relies on actual in-game job quantities and fees rather than an unverified ME/facility rounding implementation.

**Purpose:** Evaluate one real candidate without requiring the entire product scanner or a vertically integrated chain.

**Work:**
- Start from a selected product and a realistic batch size.
- Retrieve or load recipe and blueprint requirements from validated SDE data.
- Price materials at realistic procurement quantities, not just the cheapest displayed order. The evaluator can extract an exact-quantity local-ask VWAP from a schema-v4 summary or accept a clearly labeled manual replacement-cost input. It rejects partial procurement quotes and does not extrapolate to unsummarized quantities.
- Compare buying intermediate components against manufacturing them.
- Include blueprint/BPC cost, installation quote, market fees, hauling/handling, expected sales execution, inventory holding, and unsold output. The v4 adapter can source a range-eligible bid sweep for the exact output quantity; partial fills are modeled as sold units and the remainder stays in inventory.
- Use actual Industry quote inputs when system/structure variables are not available through public data.
- Reconcile the existing manufacturing profitability calculator with quoted installation fees, material sourcing costs, and separate sale scenarios. The first version accepts fee amounts as explicit quote/calculator inputs rather than inferring them.
- Keep self-haul/courier cost as an explicit cost input until a candidate-specific route can be modeled safely.
- Capture attributable active operator-hours as a measured value or clearly labeled estimate. Exclude unattended production and passive inventory wait; do not inflate hours for simultaneous alt-character actions by one operator.
- Report net contribution per active operator-hour when the input is known. Keep unadjusted contribution and explicit risks separate until pilot observations support a defensible risk adjustment.
- Show missing data and verification confidence prominently.

**Acceptance criteria:**
- [x] The first quote-first evaluator validates an SDE manufacturing recipe against an actual quoted output and complete quoted material bill; SDE base quantities remain visible for reconciliation.
- [x] The evaluator can source exact-quantity v4 procurement and liquidation estimates, preserve partial liquidation as unsold inventory, and record quote-source freshness/provenance. Manual cost inputs remain supported.
- [ ] A complete material bill and batch plan is demonstrated for one real product using the user's local SDE and Industry quote.
- [x] Input costs use quantity-aware procurement prices from exact-quantity v4 local-ask sweeps or clearly labeled manual inputs. Partial procurement sweeps are rejected.
- [x] Installation and market fees have separate explicit inputs in the batch-cost and sale-scenario calculations, avoiding implicit estimates or double counting. Real quote reconciliation remains part of the worked-product gate.
- [x] The evaluator supports immediate liquidation from v4 bid sweeps and a separate sell-order scenario with explicit prices and fee assumptions. A real-product comparison remains open.
- [ ] Buying versus producing intermediate components is evaluated.
- [ ] Output includes expected net contribution, active operator-hours (measured or estimated), net contribution per active operator-hour when known, slot-hours, capital, and liquidation horizon.
- [ ] Missing active-time data remains explicitly unknown rather than being replaced with elapsed job duration.
- [ ] A worked example is reconciled against actual Industry UI quotes and market observations.

### M5. Build the candidate scanner and opportunity ranker

**Status:** Not started. Depends on M1, M2, and the usable evaluator from M4.

**Purpose:** Answer "what should I manufacture now?" rather than requiring the user to nominate an item.

**Work:**
- Generate a candidate universe from blueprint/recipe data and doctrine-linked item lists.
- Apply hard feasibility filters using skills, jobs, blueprints, facilities, capital, input availability, and output market access.
- Eliminate candidates with insufficient data or clearly inadequate liquidity.
- Evaluate candidates using the same single-product economics as M4.
- In the initial scanner, rank by unadjusted net contribution per active operator-hour and display explicit risk indicators, low/base/high cases, capital, liquidity, slot, and complexity measures alongside it. Add a risk-adjusted score only after pilot data supports a defensible calibration; never hide an invented risk premium inside the ranking.
- Explain why candidates were accepted, rejected, or left unranked.

**Acceptance criteria:**
- [ ] The scanner produces an explainable candidate shortlist from a defined region/doctrine set.
- [ ] Infeasible candidates are filtered with a specific reason.
- [ ] Rankings use consistent price, fee, and time assumptions.
- [ ] Low/base/high cases and data timestamps accompany recommendations.
- [ ] The system can recommend no production when no candidate meets the configured thresholds.

### M6. Complete a limited production pilot

**Status:** Not started. Depends on a target operating environment and a candidate that passes M4/M5.

**Purpose:** Test whether the decision model produces a useful real-world result before expanding the tool.

**Work:**
- Select one or a small number of manageable candidates.
- Buy inputs and intermediates rather than building unnecessary upstream chains.
- Capture actual sourcing time, setup time, job count, installation quote, actual job duration, market fees, order adjustments, hauling, and sale proceeds.
- Compare actual outcomes with forecast contribution, attention time, and liquidation horizon.
- Revise the model where observed differences are material.

**Acceptance criteria:**
- [ ] At least one production batch is completed and delivered.
- [ ] Actual material use and job quotes are recorded.
- [ ] Actual operator time and market-management effort are estimated.
- [ ] Realized contribution and cash-conversion time are reconciled.
- [ ] The product and process are retained, revised, or rejected based on measured results.

### M7. Deliver the local decision-support tool

**Status:** Not started. Build incrementally after M4 and M5 prove useful.

**Purpose:** Make the workflow repeatable and convenient.

**Suggested progression:**
1. Local Python command that generates a ranked Markdown/CSV/JSON report.
2. Saved local profiles and timestamped market snapshots.
3. Product comparison, batch calculator, and shopping/job plan output.
4. Local dashboard only when it materially improves the experience.
5. Periodic refresh and market-order review recommendations.

**Acceptance criteria:**
- [ ] One local command produces a dated opportunity report.
- [ ] Every recommendation can be traced to input data and calculation assumptions.
- [ ] Profiles and snapshots can be refreshed without editing canonical mechanics documents.
- [ ] The report includes recommended actions and specific reasons not to act.
- [ ] The tool remains useful without an LLM; the LLM explains and helps investigate results rather than replacing deterministic calculations.

### M8. Add optional local EVE SSO integration

**Status:** Deferred by design.

**Purpose:** Reduce manual data entry when public data and the local tool are already useful.

**Potential data:**
- Character skills and job capacity.
- Personal assets, blueprints, and industry jobs.
- Personal market orders where supported.
- Authorized structure markets and other data justified by explicit need.

**Acceptance criteria:**
- [ ] Exact required endpoints and minimum OAuth scopes are documented.
- [ ] Tokens are stored locally using an appropriate secure mechanism.
- [ ] No secret or private account data enters Git or exported LLM packets by default.
- [ ] Public-data functionality remains available when SSO is disconnected.
- [ ] Each new private-data integration demonstrates a material improvement to recommendation quality or convenience.

## Deferred decisions and dependencies

These should be resolved only when the relevant milestone needs them:

- Target alliance, doctrine fittings, staging system, and local market arrangement.
- Whether doctrine demand should prioritize alliance buyback/market activity, local sell orders, fleet replacement, or broader regional demand.
- Character skill distribution and actual blueprint/BPC availability.
- Facility access and current structure tax/rig details.
- Acceptable liquidation horizon, risk tolerance, and active weekly attention budget.
- Whether the first product focus should be modules, ammunition, drones, ships, rigs, or a broader doctrine-derived list.
- Which private ESI scopes, if any, materially improve the eventual tool.

## Roadmap governance

- Keep this roadmap as the strategic sequence; use the research backlog for detailed tasks.
- Change milestone status only when its acceptance criteria have evidence.
- Mark milestones as **proposed**, **not started**, **in progress**, **blocked**, or **completed**. A blocked milestone must identify the dependency.
- Record material changes in the knowledge log.
- Do not expand into a new vertical chain or application feature until the previous milestone demonstrates value or the user explicitly changes priorities.
- Revisit priorities when an alliance, doctrine set, operating region, or actual production pilot changes the opportunity landscape.
