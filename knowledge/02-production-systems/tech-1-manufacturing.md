---
type: Concept
title: Tech I Manufacturing
description: Tech I manufacturing inputs, blueprint and job behavior, run quantities, material requirements, time modifiers, job installation, and delivery.
tags:
  - manufacturing
  - tech-i
  - production
sources:
  - id: ccp-manufacturing
    resource: https://support.eveonline.com/hc/en-us/articles/203210292-Manufacturing
    title: Manufacturing | EVE Online Support (updated 2024-08-29)
  - id: ccp-blueprints
    resource: https://support.eveonline.com/hc/en-us/articles/203269951-Blueprints
    title: Blueprints | EVE Online Support (updated 2024-08-29)
  - id: ccp-industry-ui
    resource: https://support.eveonline.com/hc/en-us/articles/203270121-Industry-User-Interface
    title: Industry User Interface | EVE Online Support (updated 2024-08-29)
  - id: ccp-me-research
    resource: https://support.eveonline.com/hc/en-us/articles/203210542-Material-Efficiency-Research
    title: Material Efficiency Research | EVE Online Support (updated 2024-07-15)
  - id: ccp-te-research
    resource: https://support.eveonline.com/hc/en-us/articles/203210512-Time-Efficiency-Research
    title: Time Efficiency Research | EVE Online Support (updated 2024-07-15)
  - id: ccp-viridian-fees
    resource: https://www.eveonline.com/news/view/viridian-expansion-notes
    title: Viridian Expansion Notes | EVE Online (2023-06-09)
  - id: eveuni-manufacturing
    resource: https://wiki.eveuniversity.org/Manufacturing
    title: Manufacturing | EVE University Wiki
  - id: eveuni-research
    resource: https://wiki.eveuniversity.org/Research
    title: Research | EVE University Wiki
  - id: eve-industry-formula-c4813
    resource: https://www.c4813.space/eve-online-industry-formula/
    title: EVE Online Industry Formula | C4813.space (2025-07-25)
  - id: eve-omnitool-manufacturing
    resource: https://eve-omnitool.com/industry/manufacturing/cost
    title: EVE Online Industry Cost Calculator | EVE Omnitool
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:25:24Z
status: draft
---

## Summary

Tech I manufacturing converts the input materials listed by a blueprint into the blueprint's defined output. A manufacturing job is an installed activity with a selected blueprint, run count, input location, output location, facility, duration, and installation fee. The character's available Manufacturing job slots limit how many jobs can run concurrently; CCP states there is no separate limit on the number of Manufacturing jobs a facility can accept. [^ccp-manufacturing] [^ccp-industry-ui]

A **run** is one execution of the blueprint's recipe, not necessarily one finished item. Many blueprints produce one item per run, but some produce multiple units per run. Ammunition is a common example. The blueprint's output quantity must therefore be used when translating required output units into manufacturing runs. [^eveuni-manufacturing]

This document establishes the operating workflow and a provisional calculation model for Tech I jobs. Exact combined effects of blueprint ME/TE, character skills, structure role bonuses, rigs, and rounding must still be verified against in-game job quotes.

## Inputs, outputs, and prerequisites

A manufacturing job requires:

- A blueprint or blueprint copy that supports Manufacturing.
- Sufficient materials in the selected input location at the facility where the job will run.
- A facility with the Manufacturing service available.
- An eligible job slot on the installing character.
- Required character skills shown by the blueprint and Industry interface.
- The installation fee shown by the job quote.

The Industry interface displays required and optional input materials, the installed blueprint, job outcome, selected facility, input and output locations, job duration, and job cost. Material availability is indicated in the input list. The run-count selector updates the required input quantities. [^ccp-manufacturing] [^ccp-industry-ui]

### Run count and output quantity

Let:

- (R) = number of manufacturing runs selected.
- (O) = blueprint output quantity per run.
- (Q) = total units produced by the job.

Then:

```text
Q = R × O
```

For a blueprint producing one unit per run, 50 runs produce 50 units. For a blueprint producing 100 units per run, 50 runs produce 5,000 units. Check the blueprint activity details rather than assuming one run equals one unit. [^eveuni-manufacturing]

### BPO and BPC behavior

Both BPOs and BPCs can be used for manufacturing. Detailed copy-job parameters, BPC inherited values, licensed-run limits, and copy-time mechanics are documented separately in [Blueprint Copying](blueprint-copying.md). An original has unlimited licensed runs; a copy has a finite run count. Manufacturing consumes licensed runs from a BPC. If a copy's final licensed run is consumed, the copy is exhausted. [^ccp-blueprints]

A BPO can be used for only one active Manufacturing job at a time, according to EVE University's research guide. The BPO can be copied first, and the resulting BPCs can be assigned to separate manufacturing jobs. This allows parallel jobs using multiple copies while the original is retained as the master blueprint. Treat this as a BPO-use rule documented in the community reference and confirm it in the Industry interface for critical production plans. [^eveuni-research]

### Location and remote installation

CCP states that the blueprint and required materials must be available at the destination facility. Supply Chain Management permits a character to start a Manufacturing job remotely at five additional jumps per skill level, up to 25 jumps at level V. The range is not restricted to the current region. Remote installation does not move the blueprint or materials. [^ccp-manufacturing]

Input and output locations are separately selectable in the Industry interface. When the expected materials appear missing, check that the correct hangar or container has been selected for the job. [^ccp-industry-ui] [^eveuni-manufacturing]

## Manufacturing job lifecycle

1. **Choose the blueprint.** Select an appropriate BPO or BPC and confirm that Manufacturing is available.
2. **Check blueprint requirements.** Review output per run, required materials, ME/TE levels, and skill requirements.
3. **Select the destination facility.** Confirm Manufacturing service availability and the relevant structure bonuses, rigs, taxes, and SCI.
4. **Set input and output locations.** Confirm that the blueprint and inputs are available at the job's destination.
5. **Select job runs.** The Industry window recalculates the required materials, output, duration, and installation cost.
6. **Review the quote.** Confirm the job duration, total installation fee, wallet source, facility, and material quantities before installation.
7. **Install the job.** The blueprint is committed to the job and is unavailable for conflicting use while that job is active.
8. **Monitor progress.** Active jobs appear in the Jobs listing.
9. **Deliver the completed job.** When the job is ready, delivery transfers the output to the selected output location and returns a reusable blueprint when its licensed runs remain.

CCP's Industry UI guide identifies the installed blueprint, input/output locations, facility, activity, job duration, job cost, and job list as the main interface areas. EVE University's guide describes the active job, cancellation, delivery, and blueprint-return workflow. [^ccp-industry-ui] [^eveuni-manufacturing]

### Cancellation risk

EVE University's manufacturing guide states that cancelling a manufacturing job does not refund the materials or installation costs. Do not install a job until its facility, run count, input/output locations, and wallet source have been checked. [^eveuni-manufacturing]

## Material requirements

### Core job-level rule

CCP states that Material Efficiency is applied to the whole job, not independently to each run. The job's material requirement is therefore calculated for the selected run count and then rounded. A single material line requiring exactly one unit per run cannot be reduced below one unit per run by ME. [^ccp-me-research]

For a material with a base requirement (B) units per run and a job with (R) runs, the pre-bonus job quantity is:

```text
Base job quantity = B × R
```

The blueprint ME reduction is:

```text
Blueprint ME factor = 1 - (0.01 × ME research level)
```

This is the blueprint-only component. The maximum BPO ME research level is 10, for a 10% blueprint material reduction. [^ccp-me-research]

### Provisional combined material model

For manufacturing calculations that also include Engineering Complex role bonuses and an eligible Upwell manufacturing material rig, community calculators model the reductions as separate multiplicative factors applied to the job total. One published formula uses a two-decimal intermediate rounding step, a final ceiling, and a minimum of one unit per run. [^eve-industry-formula-c4813] [^eve-omnitool-manufacturing]

A provisional representation is:

```text
Raw material quantity
  = base quantity per run
    × job runs
    × blueprint ME factor
    × structure material factor
    × eligible rig material factor

Required material quantity
  = max(job runs, ceil(round(raw material quantity, 2)))
```

Where applicable:

- Blueprint ME factor is (1 - 0.01 	imes ME level).
- The Engineering Complex role factor is 0.99 for the listed Raitaru, Azbel, and Sotiyo hulls.
- The rig factor depends on the particular rig, item group, and system security class.
- The minimum job requirement is at least one unit per run for the relevant material line.

**Status of this model:** this combined formula is a secondary-source implementation, not a full published CCP specification. The exact intermediate precision, rounding order, eligible item groups, and combined modifier behavior remain in the in-game verification queue. The Industry window's displayed material requirements are authoritative for a specific installed job. [^eve-industry-formula-c4813] [^eve-omnitool-manufacturing] [^ccp-industry-ui]

### Why job batching changes material use

Because material rounding is job-level, dividing a production plan into several smaller jobs can increase aggregate material requirements. For example, a job requiring 10.2 units before rounding consumes 11 units. Three separate jobs each requiring 10.2 units would consume 33 units in aggregate, while a single job with a combined pre-rounding requirement of 30.6 would consume 31 units. This illustrates the rounding principle, not a particular in-game blueprint quote. [^ccp-me-research] [^eveuni-manufacturing]

This has two consequences:

1. Larger batches can reduce rounding loss, provided the job remains within the game's run and duration constraints.
2. BPC run limits, blueprint availability, character job slots, material volume, and job duration can force a production plan into multiple jobs, each with its own rounding.

A calculator should apply rounding separately to each planned job, not once to an entire product demand total.

## Manufacturing time

### Time modifiers

The blueprint's TE, character skills, Engineering Complex role, and eligible manufacturing time rig can all affect manufacturing time.

The currently documented skill effects used in the provisional model are:

| Modifier | Effect |
|---|---|
| Blueprint TE research | 2% manufacturing-time reduction per TE level, up to 20% |
| Industry | 4% manufacturing-time reduction per skill level |
| Advanced Industry | 3% manufacturing and research-time reduction per skill level |
| Engineering Complex role | 15% / 20% / 30% time reduction on Raitaru / Azbel / Sotiyo |
| Eligible manufacturing time rig | Depends on rig type, item group, and system security class |

Blueprint TE levels are described in [Blueprints and Research](../01-foundations/blueprints-and-research.md). Character skill effects are documented in [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md), and structure role/rig effects are documented in [Facilities and Rigs](../01-foundations/facilities-and-rigs.md). [^eveuni-manufacturing] [^eve-industry-formula-c4813]

### Provisional time model

A community-published formula models the time modifiers as multiplicative factors. Using the documented percentage effects:

```text
Job time
  = base time per run
    × job runs
    × blueprint TE factor
    × Industry skill factor
    × Advanced Industry factor
    × structure time factor
    × eligible rig time factor
    × other applicable modifiers
```

For the named effects:

- Blueprint TE factor: (1 - 0.02 	imes TE level).
- Industry factor: (1 - 0.04 	imes Industry level).
- Advanced Industry factor: (1 - 0.03 	imes Advanced Industry level).
- Structure time factor: 0.85 for a Raitaru, 0.80 for an Azbel, and 0.70 for a Sotiyo.
- Rig and other modifier factors must be selected for the actual product and facility.

This is a provisional model for planning, not a claim that every modifier stack and rounding stage has been independently reproduced. Keep job time in seconds for calculations and convert to a readable duration only for display. [^eve-industry-formula-c4813] [^ccp-industry-ui]

## Facility and installation cost

The manufacturing activity must be offered by the facility. An Upwell structure requires the compatible Manufacturing service module to be online. Engineering Complexes have role bonuses; Citadels do not inherit those Engineering Complex bonuses. Specific rigs apply only to supported activity and item groups. [^ccp-manufacturing] [^eveuni-manufacturing]

The manufacturing installation fee is calculated separately from the replacement or acquisition cost of materials. CCP's fee equation uses EIV, the Manufacturing SCI, applicable structure/rig bonuses to the SCI component, facility tax, SCC surcharge, and Alpha-clone tax. The detailed equation and EIV convention are in [Installation Cost Computation](../09-computations/installation-costs.md). [^ccp-viridian-fees]

For a real production decision, use the live Industry job quote for the chosen system, facility, blueprint, run count, clone state, and current tax configuration.

## Production planning considerations

Before installing a batch, evaluate:

1. **Demand:** expected sale or internal consumption quantity, likely delivery window, and market depth.
2. **Blueprint capacity:** BPO single-job availability, BPC licensed runs, ME/TE level, and output per run.
3. **Job fragmentation:** how the required output divides into jobs, including BPC run limits and material rounding per job.
4. **Character capacity:** available Manufacturing slots and Industry/Advanced Industry skill levels.
5. **Materials:** replacement or opportunity cost, input location, hauling volume, and stock availability.
6. **Facility:** required service, structure role, rig scope, security modifiers, SCI, facility tax, and service-module continuity.
7. **Timing:** job duration, production schedule, delivery, and market timing.
8. **Risk:** structure interruption, cancellation cost, asset exposure, and the possibility that the market price changes before delivery.

A product that has a positive theoretical unit margin may still be unattractive when its job requires scarce slots, large working capital, multiple hauls, or a long production cycle.

## Boundaries and unresolved details

This document does not yet provide a complete current catalog of Tech I blueprints, product-specific outputs, all skill prerequisites, exact maximum job runs, or all material/time rig values. Those belong in future SDE-backed product and formula data.

The following combined-model details remain open for independent verification:

- Exact intermediate precision and material rounding sequence for jobs using multiple bonuses.
- Whether the full current rig/security multipliers in community calculators match the in-game Industry quote for every supported item group.
- Exact interaction and rounding order for blueprint TE, character skills, structure role, rigs, and implants.
- Maximum duration/runs permitted for each job and item, including any special cases.
- BPO lock behavior and copy-based parallel manufacturing across personal and corporation hangars.
- Whether cancelled jobs always forfeit all inputs and installation fees in every job circumstance.

## Related concepts

- [Blueprints and Research](../01-foundations/blueprints-and-research.md)
- [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md)
- [Facilities and Rigs](../01-foundations/facilities-and-rigs.md)
- [Installation Cost Computation](../09-computations/installation-costs.md)
- [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)

[^ccp-manufacturing]: CCP Support, Manufacturing (updated 2024-08-29).
[^ccp-blueprints]: CCP Support, Blueprints (updated 2024-08-29).
[^ccp-industry-ui]: CCP Support, Industry User Interface (updated 2024-08-29).
[^ccp-me-research]: CCP Support, Material Efficiency Research (updated 2024-07-15).
[^ccp-te-research]: CCP Support, Time Efficiency Research (updated 2024-07-15).
[^eveuni-manufacturing]: EVE University Wiki, Manufacturing.
[^eveuni-research]: EVE University Wiki, Research.
[^eve-industry-formula-c4813]: C4813.space, EVE Online Industry Formula (2025-07-25). The page identifies itself as an incomplete community-derived formula set; use as an analytical reference, not official documentation.
[^eve-omnitool-manufacturing]: EVE Omnitool, Industry Cost Calculator. Calculator-specific material model; validate against in-game job quotes.
[^ccp-viridian-fees]: CCP, Viridian Expansion Notes (2023-06-09).
