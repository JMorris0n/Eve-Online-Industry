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

### Q-001: Is the ME/TE research SCC surcharge still 2%?

- **Question:** Does the temporary reduction of the SCC surcharge from 4% to 2% for blueprint ME and TE research remain active as of November 2026?
- **Affected concepts:** [Installation Cost Computation](../09-computations/installation-costs.md), [Blueprints and Research](../01-foundations/blueprints-and-research.md).
- **Why it matters:** The surcharge directly changes the ISK cost of blueprint research and can materially alter whether a BPO research level is economically worthwhile.
- **Evidence needed:** Current in-game Industry quotes for ME research and TE research; any later CCP patch note or announcement that extends, changes, or ends the temporary relief.
- **Status:** Open. CCP's 2025-07-18 announcement explicitly described the 2% rate as temporary. A current rate has not been independently checked in game.

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

## Entry format

- **Question:** precise, answerable wording.
- **Affected concepts:** relative links.
- **Why it matters:** operational or economic consequence.
- **Evidence needed:** source, test, or calculation.
- **Status:** open, researching, blocked, resolved.
- **Resolution:** final answer and evidence, once resolved.
