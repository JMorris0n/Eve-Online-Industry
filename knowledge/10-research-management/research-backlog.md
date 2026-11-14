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
- [ ] Confirm whether the temporary 2% ME/TE research SCC surcharge is still active in November 2026.
- [ ] Validate current EIV/process-value bases and fee calculations for Science, Copying, Invention, and Reactions.
- [ ] Set up repeatable live-data capture for ESI industry systems and adjusted prices.

## P1: Complete production systems

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
- [x] Document broker fees, sales tax, relist fees, NPC versus Upwell market differences, and transaction execution behavior.
  - [ ] Validate fee calculations against wallet journal and live order quotes for NPC and Upwell markets.
  - [ ] Build a representative worked manufacturing product example using current prices and a chosen market location.
- [ ] Facility and regional location economics.
- [ ] Logistics, capital, and inventory risk.

## P3: Optimization

- [ ] Manufacturing and science throughput.
- [ ] Production scheduling.
- [ ] Character specialization and marginal skill value.
- [ ] Multi-character and multi-facility scaling.

## P4: Market intelligence, tools, and playbooks

- [ ] Market data quality and liquidity analysis.
- [ ] Regional arbitrage model.
- [ ] Third-party tool evaluation.
- [ ] ESI and data acquisition notes.
- [ ] Operational playbooks derived from verified concepts.

## Acceptance criteria for a research task

A task is complete only when its key claims have sources, calculations are reproducible, known conflicts are recorded, dependencies are linked, and the proposed edits have passed critical review.

A checked research item means the topic has been documented to the stated scope. It does not automatically mean the concept has received independent in-game verification. The concept's OKF lifecycle status and any verified events must reflect the actual review performed.
