---
type: Concept
title: Open Questions
description: Current unresolved questions requiring research, testing, or a source decision.
tags:
  - research
  - open-questions
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:25:24Z
status: draft
---

## Active questions

### Q-001: What is the current ME/TE research SCC surcharge?

- **Question:** What is the latest supported SCC surcharge value for ME and TE research, and is the temporary 2% rate still active in the live Industry UI?
- **Affected concepts:** [Installation Cost Computation](../09-computations/installation-costs.md), [Blueprints and Research](../01-foundations/blueprints-and-research.md).
- **Why it matters:** The surcharge directly changes the ISK cost of blueprint research and can materially alter whether a BPO research level is economically worthwhile.
- **Evidence needed:** CCP's 2025-07-18 announcement and current in-game ME/TE research quotes.
- **Resolution:** CCP reduced the ME/TE research SCC surcharge from 4% to 2% on 2025-07-18 and explicitly described the reduction as temporary. No later official reversal was found in the source search through 2026-11-14. The 2% value is therefore the latest published CCP value, but it remains configurable until a live Industry quote confirms it.
- **Status:** Source research resolved; live in-game verification remains open.

### Q-002: What are the exact current fee valuation bases for Science, Copying, Invention, and Reaction jobs?

- **Question:** Does the value base used in each current activity installation fee match the secondary formulas currently published by EVE University and the EVE Reactions Calculator?
- **Affected concepts:** [Installation Cost Computation](../09-computations/installation-costs.md), [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md), [Production Systems](../02-production-systems/index.md).
- **Why it matters:** Applying Manufacturing EIV logic to other activity categories could produce systematically incorrect estimates.
- **Evidence needed:** Controlled in-game job quotes with job type, blueprint/formula, run count, system, facility, owner tax, character clone state, and relevant SCI captured. Compare fee deltas against independently calculated model inputs.
- **Status:** Open. Secondary calculators provide candidate models, but no controlled comparison is recorded in this corpus.

### Q-003: How do applicable structure role bonuses and rigs combine and round?

- **Question:** For representative manufacturing, research, invention, and reaction jobs, are applicable structure and rig modifiers applied multiplicatively, additively, or through another order, and at what stage are output quantities rounded?
- **Affected concepts:** [Facilities and Rigs](../01-foundations/facilities-and-rigs.md), [Blueprints and Research](../01-foundations/blueprints-and-research.md), [Installation Cost Computation](../09-computations/installation-costs.md).
- **Why it matters:** Incorrect modifier stacking can produce incorrect material requirements, times, and installation fees in all later calculators.
- **Evidence needed:** Matched job quotes from facilities with different hull roles/rigs, identical blueprints/formulas, identical run counts, and saved UI details or screenshots.
- **Status:** Open. Current documentation identifies the eligible bonuses but does not yet establish a complete independently tested combined-modifier model.

### Q-004: What is the exact current material/time calculation and rounding sequence for Manufacturing?

- **Question:** For a Tech I manufacturing job, what exact formula and intermediate precision does the game use when applying blueprint ME/TE, character skills, Engineering Complex role bonuses, security-scaled Upwell rigs, and any other applicable modifiers?
- **Affected concepts:** [Tech I Manufacturing](../02-production-systems/tech-1-manufacturing.md), [Blueprints and Research](../01-foundations/blueprints-and-research.md), [Facilities and Rigs](../01-foundations/facilities-and-rigs.md).
- **Why it matters:** Material rounding and time stacking affect job inputs, throughput, and cost. Applying modifiers in the wrong order can cause a systematic error in every future production calculator.
- **Evidence needed:** Controlled, matched Industry UI quotes using the same blueprint and run count across NPC, Engineering Complex, and rigged/unrigged Upwell facilities. Record character skills, blueprint ME/TE, item group, system security, material quantities, duration, and job fee.
- **Status:** Open. CCP documents the ME job-level rule and individual effects; current community calculators provide candidate combined formulas, but this corpus has no independent controlled reproduction.

### Q-005: What are the maximum Manufacturing job duration and run constraints?

- **Question:** Does the live game enforce a 30-day maximum for Manufacturing jobs, and what exceptions or item-specific constraints apply?
- **Affected concepts:** [Tech I Manufacturing](../02-production-systems/tech-1-manufacturing.md), [Production Scheduling](../05-optimization/production-scheduling.md).
- **Why it matters:** A duration cap limits runs per job. This can force a production plan to split demand across multiple jobs and repeat per-job material rounding.
- **Evidence needed:** In-game attempts with the same blueprint at run counts immediately below and above the candidate duration boundary, including items with unusually long base manufacturing times. Record the installed quote or exact UI rejection.
- **Status:** Open. A 2025 community formula reference uses 2,592,000 seconds (30 days) when calculating maximum runs, but that alone does not establish all current game exceptions.

### Q-006: Can the same BPO support more than one active Manufacturing job?

- **Question:** Is the one-active-Manufacturing-job-per-BPO restriction unchanged, and how does the rule behave for personal and corporation blueprints, locations, and copied BPCs?
- **Affected concepts:** [Tech I Manufacturing](../02-production-systems/tech-1-manufacturing.md), [Blueprints and Research](../01-foundations/blueprints-and-research.md), [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md).
- **Why it matters:** Blueprint concurrency can limit production throughput independently of character job slots. A plan that assumes one BPO can feed several parallel Manufacturing jobs may be impossible without copies.
- **Evidence needed:** Controlled in-game test attempting overlapping Manufacturing jobs from one BPO, then testing multiple BPCs copied from the same BPO. Record whether each blueprint is personal or corporation-owned and its location.
- **Status:** Open. The current one-job-per-BPO statement is supported by EVE University, but it has not been independently tested in this corpus.

### Q-007: How does the Industry UI round or cap invention success probability?

- **Question:** Does the live Industry UI round the skill-adjusted invention probability at any intermediate stage, and how does it display or handle a calculated chance at or above 100%?
- **Affected concepts:** [Tech II Invention](../02-production-systems/tech-2-invention.md).
- **Why it matters:** The expected attempt count and expected invention cost depend on the probability actually used by the game, not just a displayed approximation.
- **Evidence needed:** Compare calculated probabilities with UI previews for multiple base-chance item classes and skill/decryptor combinations, including a combination whose raw formula is close to or above 100%.
- **Status:** Open. The current formula and base chances are documented by CCP's historic Phoebe notes and EVE University's current invention reference; exact current display precision/capping is not specified in those sources.

### Q-008: How do datacore and decryptor quantities scale in multi-run invention jobs?

- **Question:** For an invention job with multiple runs, how many datacores and decryptors are consumed per installed run, and are there item-specific exceptions?
- **Affected concepts:** [Tech II Invention](../02-production-systems/tech-2-invention.md), [Installation Cost Computation](../09-computations/installation-costs.md).
- **Why it matters:** Per-attempt input quantities directly determine expected cost per successful Tech II BPC. A mistaken assumption about decryptor or datacore consumption would materially distort decryptor selection and profitability.
- **Evidence needed:** Install matched one-run and multi-run jobs for a representative module and ship BPC, recording the Industry UI input quantities before installation and actual inputs consumed after delivery.
- **Status:** Open. CCP confirms that the inputs are consumed regardless of success and that one input BPC run is consumed per invention run, but the cited support text does not explicitly state all multi-run optional-item quantity rules.

### Q-009: How do copy time modifiers and BPO concurrency work in the live Industry system?

- **Question:** Does the base Copy activity time equal 80% of the BPO's base Manufacturing run time for every blueprint, and how do Science, Advanced Industry, Engineering Complex role bonuses, Copy-specific rigs, and simultaneous copy jobs interact?
- **Affected concepts:** [Blueprint Copying](../02-production-systems/blueprint-copying.md), [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md), [Facilities and Rigs](../01-foundations/facilities-and-rigs.md).
- **Why it matters:** Copy-job duration determines how quickly BPC inventory can be replenished and consumes Science job slots. BPO concurrency affects how much copy throughput one original can supply.
- **Evidence needed:** Matched Industry UI Copy quotes for a representative short-run and long-run blueprint, with and without applicable copy skills and facility bonuses. Attempt overlapping copy jobs from one BPO and compare personal and corporation blueprint behavior.
- **Status:** Open. EVE University documents an 80%-of-base-Manufacturing-time model, Science and Advanced Industry reductions, and single active Manufacturing job per BPO; this corpus has not independently reproduced copy time or copy-job concurrency.

### Q-010: Are copying input materials and fees fully explained by the separate copy-count and licensed-run fields?

- **Question:** For BPOs with exceptional Copy inputs, are material quantities solely a function of Job Runs, and does the live Copy installation fee scale with both Job Runs and Runs per Copy as suggested by secondary references?
- **Affected concepts:** [Blueprint Copying](../02-production-systems/blueprint-copying.md), [Installation Cost Computation](../09-computations/installation-costs.md).
- **Why it matters:** A copy plan can produce the same total licensed-run capacity with different physical copy counts. Material and fee scaling can therefore change the optimal BPC configuration.
- **Evidence needed:** Install matched copy quotes with equal (C 	imes R) but different values of (C) and (R), recording material inputs, SCI, facility tax, SCC, and fee. Include at least one blueprint with non-zero copy inputs.
- **Status:** Open. CCP explicitly states exceptional copy input materials scale with Job Runs and not Runs per Copy; the activity-specific fee calculation still requires comparison with current in-game quotes.

### Q-011: What is the current complete type-level Tech II component and construction recipe matrix?

- **Question:** For every current Advanced Component and representative Tech II product group, what are the exact input type IDs, quantities per run, output quantity, required skills/levels, blueprint ME/TE behavior, and applicable facility/rig rules in the current SDE and Industry UI?
- **Affected concepts:** [Tech II Components](../02-production-systems/tech-2-components.md), [Reactions](../02-production-systems/reactions.md), [Moon Materials](../03-materials-and-sourcing/moon-materials.md), [Tech II Invention](../02-production-systems/tech-2-invention.md).
- **Why it matters:** A generic supply-chain diagram is not sufficient for a deterministic production planner. Recipe-level data controls material sourcing, job planning, costs, skill requirements, and the expansion of a complete Tech II production tree.
- **Evidence needed:** Current versioned SDE recipe/BOM data plus matched in-game Industry quotes for representative components and final Tech II items. Record type IDs, SDE build identifier, retrieval timestamp, skill state, blueprint state, facility, and displayed inputs.
- **Status:** Open. The concept documents the supply-chain structure, but a comprehensive type-level recipe and skill catalog has not been built.

### Q-012: Are the published composite reaction input/output tables still current?

- **Question:** Do the intermediate and composite recipe inputs, fuel-block quantities, and output batch quantities in the Reactions concept match the current SDE and live in-game Reaction Formulas?
- **Affected concepts:** [Reactions](../02-production-systems/reactions.md), [Tech II Components](../02-production-systems/tech-2-components.md), [Moon Materials](../03-materials-and-sourcing/moon-materials.md).
- **Why it matters:** These recipes are upstream dependencies for Advanced Components and a large portion of Tech II item production. A single recipe or yield mismatch propagates through the entire build-cost tree.
- **Evidence needed:** Current SDE reaction formula records with build identifier and controlled in-game quotes for representative two-input, multi-input, special-intermediate, and special-composite formulas. Record exact type IDs, quantities, fuel blocks, output quantities, and rounding.
- **Status:** Open. The current tables are transcribed from EVE University (last modified 2025-06-22); no type-by-type SDE or in-game comparison has yet been recorded.

### Q-013: What is the complete current Biochemical and Molecular-Forged reaction catalog?

- **Question:** Which formulas are currently supported by the Biochemical Reactor family, and what are their exact inputs, fuel blocks, outputs, acquisition routes, and dependencies?
- **Affected concepts:** [Reactions](../02-production-systems/reactions.md), [Facilities and Rigs](../01-foundations/facilities-and-rigs.md), [Advanced Manufacturing](../02-production-systems/advanced-manufacturing.md).
- **Why it matters:** CCP's Reactions support article mentions booster products and newer Neurolink/Isotropic industrial products, while community references separate these into Biochemical and Molecular-Forged formula groups. They should not be omitted or conflated in a comprehensive reaction dataset.
- **Evidence needed:** Current ESI/SDE reaction formula list, exact compatible reactor service, in-game formula Bill of Materials, and current facility/rig applicability for each formula family.
- **Status:** Open. The family-level support is documented, but no exhaustive type-level catalog is included in this concept.

## Entry format

- **Question:** precise, answerable wording.
- **Affected concepts:** relative links.
- **Why it matters:** operational or economic consequence.
- **Evidence needed:** source, test, or calculation.
- **Status:** open, researching, blocked, resolved.
- **Resolution:** final answer and evidence, once resolved.

 
### Q-014: What operating environment should the first live product-evaluation example use?

- **Question:** Which character(s), skill state, production location/facility, market region, and approximate working-capital range should be used for the first live product-ranking and worked manufacturing example?
- **Affected concepts:** [Product Selection](../06-market-intelligence/product-selection.md), [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md), [Market Location Economics](../04-industrial-economics/market-location-economics.md), [Character Specialization](../05-optimization/character-specialization.md).
- **Why it matters:** A meaningful live example needs actual job eligibility, BPO/BPC availability, facility quotes, regional order-book depth, logistics assumptions, and capital constraints. A generic Jita/Omega assumption could produce a misleading recommendation.
- **Evidence needed:** User-selected character(s) or skill export, intended production/market region, accessible facility/structure, and a working-capital range. Do not request or store EVE SSO tokens in the knowledge repository.
- **Status:** Open, awaiting user input. Continue with generic mechanics, data tooling, and verification work until the operating environment is selected.

 
### Q-015: Has the bounded public SDE/ESI pipeline been run against live data?

- **Question:** Has the local SDE parser and public ESI collector/summarizer completed a bounded live-data validation with provenance and output checks?
- **Affected concepts:** [ESI and Market Data](../07-tools-and-data/esi-and-market-data.md), [Data Quality and Reconciliation](../07-tools-and-data/data-quality.md), [Local SDE tools](../../tools/sde/README.md), [Read-only ESI collector](../../tools/esi/README.md).
- **Why it matters:** Fixture tests cannot expose every live SDE/ESI schema, cache, range, or execution-model assumption.
- **Evidence:** SDE build 3698585 was downloaded, integrity-checked, extracted, and parsed. Aggregate parser output was recorded. The Forge collection and schema-v4 summary were reviewed; 516 regional orders, 72 target-location books, 409 history days per mineral, SDE range resolution, per-fill minimum volume, and summary quantity arithmetic are recorded in the M1 audit.
- **Limitations:** The market-order snapshot had passed its ESI cache expiry by review time. The three sampled market-order endpoints each returned one page, so live multi-page traversal was not demonstrated.
- **Status:** Resolved for the bounded sample. Broader regions/types, live refresh, and multi-page observations are separate follow-up tasks.

### Q-016: What record-level quality checks should be applied to normalized SDE recipes?

- **Question:** Can the local `industry-recipes.jsonl` be summarized with record-level checks for product/material type joins, duplicate blueprint/activity keys, publication state, incomplete optional arrays, and exceptional base times?
- **Affected concepts:** [Data Quality and Reconciliation](../07-tools-and-data/data-quality.md), [Product Selection](../06-market-intelligence/product-selection.md), [SDE recipe parser](../../tools/sde/README.md).
- **Why it matters:** Candidate generation must not silently include unpublished outputs, unresolved type IDs, incomplete material recipes, or time values that break throughput calculations.
- **Evidence needed:** A compact local quality-report command that reads the normalized JSONL and emits aggregate counts plus a small list of exceptional IDs. Keep the complete recipe data local; only the report or selected non-sensitive excerpts need to be shared.
- **Status:** Open. This does not block M1's bounded acquisition/parser validation, but it must be addressed before the candidate scanner treats the full recipe universe as complete.
