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

## Entry format

- **Question:** precise, answerable wording.
- **Affected concepts:** relative links.
- **Why it matters:** operational or economic consequence.
- **Evidence needed:** source, test, or calculation.
- **Status:** open, researching, blocked, resolved.
- **Resolution:** final answer and evidence, once resolved.
