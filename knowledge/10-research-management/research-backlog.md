---
type: Concept
title: Research Backlog
description: Prioritized research tasks, dependencies, and acceptance criteria.
tags:
  - research
  - backlog
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:25:24Z
status: draft
---

## P0: Establish trustworthy foundations

- [x] Maintain source catalogs, claim-level citations, open questions, chronological research log, and repeatable verification protocols.
- [x] Establish a portable LLM coordination workflow with bounded task packets, role prompts, independent review, validation gates, human-controlled integration, and a VS Code/PowerShell quick start.
- [x] Add a standard-library Markdown link checker, validation tests, and a one-command local runner; CI run 31 passed 17 calculation tests, 5 validation-tool tests, and 579 local links across 94 Markdown files after correcting four existing broken links.

- [x] Document blueprint object types, BPO/BPC distinctions, acquisition paths, and their industry roles.
- [x] Document ME and TE research steps, effects, job-level formulas, and material-rounding limitations.
- [ ] Independently test ME material rounding against representative in-game manufacturing jobs.
- [ ] Independently test BPC copying behavior, including copy-job quantity versus runs per copy.
- [x] Document Manufacturing, Science, and Reaction job pools, slot formulas, support skills, and remote-management skills.
- [ ] Independently verify maximum job counts and remote-start ranges in game for each job type.
- [ ] Verify Alpha and Omega job capacity using actual character skill states.
- [x] Document facility families, role bonuses, industrial services, service-module fuel/downtime risk, and rig categories.
- [x] Document the CCP industry installation-fee equation, EIV basis for Manufacturing, tax components, and activity-specific exceptions.
- [ ] Independently verify facility role/rig modifiers against current in-game job quotes for representative item groups.
- [ ] Verify current owner taxes, activity SCI, and fee rounding for NPC stations and Upwell facilities.
- [x] Record CCP's 2025-07-18 reduction of the ME/TE research SCC surcharge from 4% to 2%, explicitly described as temporary; no later CCP reversal found as of 2026-11-14.
- [ ] Confirm the current 2% ME/TE research surcharge against a live Industry quote; keep it configurable until then.
- [ ] Validate current EIV/process-value bases and fee calculations for Science, Copying, Invention, and Reactions.
- [x] Implemented a read-only ESI collector for industry system indices, adjusted prices, and selected market orders/history; local validation remains open.

## P1: Complete production systems

- [x] Document high-level industry activity taxonomy, job pools, product families, and end-to-end supply-chain stages.
- [x] Document advanced manufacturing families: Tech II/III, capital ships, Upwell structures, boosters, and specialist BPC products.
- [x] Document asteroid ore and base mineral sourcing, mining/compression factors, and current-data limitations.
- [x] Document moon extraction, R4–R64 ore classes, moon-material processing skills, and reaction-chain role.
- [x] Document Mykoserocin/Cytoserocin and Fullerite gas sources, harvesting, and industrial uses.
- [x] Document Sleeper Ancient Salvage, blue-loot distinction, and Tech III component supply.
- [x] Document procurement channels, material valuation, reprocessing categories, and provisional yield models.
  - [ ] Verify current reprocessing yield formulas, skills, taxes, and rig/structure modifiers against the live Reprocessing UI.
  - [ ] Build current SDE-driven ore, moon-ore, reaction-gas, and salvage material matrices.

- [x] Document Tech I manufacturing workflow, BPO/BPC use, run/output distinction, job-level material rounding, provisional time/material models, and delivery.
  - [ ] Independently test combined ME/TE, character, structure, and rig modifiers against Industry quotes.
  - [ ] Verify maximum job duration/run limits and BPO/BPC concurrent-use behavior.
- [x] Document Tech II invention inputs, skill-adjusted probability formula, category base chances, decryptor modifiers, output BPC characteristics, and expected-cost model.
  - [ ] Verify invention chance precision/cap and multi-run datacore/decryptor consumption against the Industry UI.
  - [ ] Verify output BPC runs/ME/TE for each decryptor and representative item families.
- [x] Document standalone blueprint-copying mechanics, BPC inherited values, two-field copy-job setup, licensed-run limits, time model, and distribution use.
  - [ ] Verify copy input materials against Job Runs versus Runs per Copy for a blueprint requiring exceptional inputs.
  - [ ] Verify copy time and skill/facility modifiers against live Industry quotes.
  - [ ] Verify concurrent copy-job restrictions from one BPO.
- [ ] Validate the complete Tech II invention-to-manufacturing chain.
- [x] Document the Tech II component supply chain, composite reaction stages, Advanced Component manufacturing, final Tech II input categories, R.A.M. material behavior, and vertical-integration decisions.
  - [ ] Build and independently verify a type-level Advanced Component recipe/skill matrix from current SDE and Industry UI data.
  - [ ] Validate representative Advanced Component and final Tech II production quotes.
- [x] Document reaction reactor families, Refinery/security constraints, reaction skill/job pool dependencies, and the common Tech II composite reaction chain.
  - [ ] Verify intermediate/composite recipe input-output quantities against current SDE and in-game Reaction Formulas.
  - [ ] Verify reactor-family availability and reaction-rig effects for representative facilities.
  - [ ] Capture current fuel-block requirements and run/output rounding for all reaction families.
- [x] Document the four-stage Tech III production chain, relic families, output runs, sourcing, skill dependencies, and final manufacturing stages.
  - [ ] Reconcile CCP's published relic base success chances with SDE per-output probabilities and live Industry-window results.
  - [ ] Verify reverse-engineering skill modifiers and optional decryptor behavior.
  - [ ] Build and validate the complete Hybrid Tech Component recipe/skill matrix.
  - [ ] Verify R.A.M.- Starship Tech requirements and current hull/subsystem manufacturing inputs.
- [x] Document Planetary Industry colony mechanics, extraction programs, processor roles, skills, routing, storage, taxes, Customs Offices, Skyhooks, and Alpha restrictions.
- [x] Document P0-P4 commodity tiers, representative schematic recipes, and standard batch structures from the community reference.
  - [ ] Rebuild the full PI schematic and commodity matrix from the current CCP SDE and verify against the in-game UI.
  - [ ] Confirm Equinox-era planet eligibility, Skyhook transfer fees, and any changes to colony restrictions.

## P2: Industrial economics

- [x] Establish consistent replacement-cost, opportunity-cost, historical-cost, and EIV accounting conventions.
- [x] Document manufacturing profitability framework, batch-level contribution, break-even pricing, slot-hour efficiency, and capital-return metrics.
- [x] Implement a deterministic manufacturing profitability calculator with material valuation, partial-sale inventory accounting, full-batch projections, break-even/target-margin pricing, and input-price thresholds.
  - [x] Confirm the calculation suite passes in [GitHub Actions run 18](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43578869255) (17 calculation tests; also passed 5 validation tests and 579 local Markdown links across 94 files); the same run also passed five validation-tool tests and 571 local Markdown links. Reconcile a worked example against actual Industry quotes, market fills, and wallet records.
- [x] Document broker fees, sales tax, relist fees, NPC versus Upwell market differences, and transaction execution behavior.
  - [ ] Validate fee calculations against wallet journal and live order quotes for NPC and Upwell markets.
  - [x] Add a deterministic fee estimator and standard-library unit tests; included in the 17-calculation-test successful [GitHub Actions run 18](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43578869255).
  - [ ] Build a representative worked manufacturing product example using current prices and a chosen market location.
- [x] Document facility and regional location economics, including activity-specific SCI, ESI/market data, facility comparison, remote installation, and total landed cost.
  - [x] Implement the public ESI collector needed to retrieve system indices and market orders.
  - [ ] Run the collector and build a representative location comparison using live market orders, SCI, facility fees, and logistics.
- [x] Document self-haul and courier-contract cost components, collateral exposure, route risk, Upwell Asset Safety, and structure continuity risks.
- [x] Build a configurable self-haul versus courier cost model, including expected cargo/ship loss, collateral coverage, pilot time, and capital exposure.
  - [x] Run the calculator unit tests successfully in the 17-calculation-test [GitHub Actions run 18](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43578869255); validate assumptions against a real route/contract scenario.
- [x] Document working capital, inventory valuation, capital turnover, asset concentration, and capital allocation.
- [x] Document expected-value invention economics, including batch success variance, cost per successful BPC, and cost per Tech II manufacturing run.
- [x] Document incremental ME/TE research ROI, break-even production volume, and Science slot-hour opportunity cost.
- [x] Define a deterministic capital-turnover computation using dated cash flows, capital-days, and cash conversion time.
  - [ ] Validate the model with a real production batch and wallet/asset records.

## P3: Optimization

- [x] Document Manufacturing throughput, job-slot utilization, output rates, blueprint/BPC constraints, batch sizing, and bottleneck analysis.
- [x] Document Science job-slot allocation, research/copying output rates, expected invention BPC throughput, and Science-to-Manufacturing bottlenecks.
- [x] Document multi-pool production scheduling, precedence dependencies, slot/resource constraints, critical path, batch sizing, and replanning triggers.
- [x] Document industrial role profiles, job-slot/time/invention/remote/market/PI skill categories, and marginal skill-value planning.
- [x] Document industrial scaling across characters, facilities, regions, and vertical integration, including bottlenecks and incremental expansion tests.

## P4: Market intelligence, tools, and playbooks

- [x] Document market order mechanics, immediate matching, regional scope, ESI market/history endpoints, and cache rules.
- [x] Document demand, liquidity, and market-depth analysis, including zero-trade-day handling, transaction counts, VWAP execution, spreads, and liquidation horizons.
- [x] Document price-history analysis, executable order-book valuation, adjusted-price/EIV distinctions, volatility, and price provenance.
- [x] Document regional arbitrage using source/destination VWAP, fees, hauling, collateral, risk, and capital holding time.
- [x] Survey current third-party manufacturing, reaction, PI, market, local asset, and AI/MCP tools; record data and privacy caveats.
  - [ ] Independently test representative tool outputs against live Industry quotes and current SDE/ESI inputs.
- [x] Document ESI and SDE data acquisition, compatibility dates, OAuth scopes, caching, rate limits, pagination, and industrial endpoints.
  - [x] Add local CCP SDE download and archive-inspection scripts using the standard library.
- [ ] Run the SDE downloader locally, record the current build manifest, and inspect the current JSONL schema.
- [x] Implement a read-only public ESI collector with provenance, compatibility-date pinning, cache handling, pagination, and rate-limit compliance.
  - [ ] Run the collector locally with a small region/type-ID set and validate response schemas, cache behavior, and output hashes.
- [x] Draft operational playbooks for product evaluation, T1/T2 production, PI, reactions, and market delivery from the documented concepts.
- [ ] Verify playbooks against live in-game workflows and promote them only when their underlying mechanics are independently reviewed.

- [x] Create reproducible verification protocols for ME rounding, BPC copying, job slots, facility modifiers, fees, invention, reactions, Alpha PI, SDE, and ESI.

## Acceptance criteria for a research task

A task is complete only when its key claims have sources, calculations are reproducible, known conflicts are recorded, dependencies are linked, and the proposed edits have passed critical review.

A checked research item means the topic has been documented to the stated scope. It does not automatically mean the concept has received independent in-game verification. The concept's OKF lifecycle status and any verified events must reflect the actual review performed.
