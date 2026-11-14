---
type: Concept
title: Manufacturing Throughput
description: Manufacturing output rates, character job-slot utilization, blueprint availability, batch sizing, parallel jobs, and production bottlenecks.
tags:
  - optimization
  - manufacturing
  - throughput
sources:
  - id: ccp-manufacturing
    resource: https://support.eveonline.com/hc/en-us/articles/203210292-Manufacturing
    title: Manufacturing | EVE Online Support (updated 2024-08-29)
  - id: ccp-activities
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: ccp-blueprints
    resource: https://support.eveonline.com/hc/en-us/articles/203269951-Blueprints
    title: Blueprints | EVE Online Support (updated 2024-08-29)
  - id: eveuni-manufacturing
    resource: https://wiki.eveuniversity.org/Manufacturing
    title: Manufacturing | EVE University Wiki
  - id: eveuni-production-skills
    resource: https://wiki.eveuniversity.org/Skills:Production
    title: Skills:Production | EVE University Wiki
  - id: eveuni-research
    resource: https://wiki.eveuniversity.org/Research
    title: Research | EVE University Wiki
  - id: eve-industry-formula-c4813
    resource: https://www.c4813.space/eve-online-industry-formula/
    title: EVE Online Industry Formula | C4813.space (2025-07-25)
  - id: eve-omnitool-manufacturing
    resource: https://eve-omnitool.com/industry/manufacturing/cost
    title: EVE Omnitool Industry Cost Calculator
generated:
  by: openai/gpt-6
  at: 2026-11-14T07:30:00Z
status: draft
---

## Purpose

Manufacturing throughput measures how much output a production operation can deliver over time, given job duration, character job slots, blueprint availability, materials, facility configuration, and capital.

The theoretical maximum is not necessarily the practical output rate. The true bottleneck may be a character's Manufacturing slots, a single BPO, limited BPC runs, missing inputs, working capital, facility access, or the ability to sell finished output.

## Core quantities

| Quantity | Definition |
|---|---|
| Manufacturing run | One execution of the blueprint's recipe |
| Output per run | Number of finished units produced by one run |
| Job output | Runs in the job multiplied by output per run |
| Job duration | Time from job start to completion |
| Slot-hours | Character Manufacturing slot time consumed by the job |
| Wall-clock time | Elapsed time between the start and completion of a production plan |
| Throughput | Delivered output units per unit of elapsed time |

A blueprint run is not necessarily one finished unit. Use the output quantity from the blueprint. [^eveuni-manufacturing]

## Character job-slot capacity

Manufacturing uses its own character job pool. The slot formula is:

```text
Manufacturing slots
  = 1 + Mass Production level + Advanced Mass Production level
```

The base slot is one. Mass Production and Advanced Mass Production each add one slot per skill level, to a theoretical maximum of 11 at both skills V. These slots are character capacity, not a facility job limit. [^ccp-activities] [^eveuni-production-skills]

CCP states that facilities offering Manufacturing have no separate time restriction or limit on the number of Manufacturing jobs that can be installed there. The character's available slots, required materials, blueprint, destination, and facility service are the relevant constraints. [^ccp-manufacturing]

A job occupies one Manufacturing slot while active. Manufacturing slots are independent from Science and Reaction slots, so a character can run activities in different pools concurrently, subject to the capacity of each pool. [^ccp-activities]

## Single-job throughput

For one job:

```text
Job output units = job runs × output units per run

Output rate per slot-hour
  = job output units / job duration in hours

Theoretical output per day per slot
  = output rate per slot-hour × 24
```

This is a continuous-utilization rate. It assumes a new job can be installed immediately when the previous job completes, all inputs and blueprints are ready, and the slot is never idle.

If a job produces 500 units in 10 hours:

- Output rate: 50 units per slot-hour.
- Theoretical output per day per continuously utilized slot: 1,200 units.

This is an illustrative arithmetic example, not an in-game product quote.

## Multi-slot throughput

For a character with (S) Manufacturing slots, a simplified theoretical capacity for identical jobs of duration (T) hours and output (Q) units is:

```text
Theoretical output per day
  = S × (24 / T) × Q
```

For mixed jobs, calculate total slot-hours:

```text
Total slot-hours = sum(job duration in hours)

Available slot-hours over horizon H days
  = S × 24 × H

Slot utilization
  = total active slot-hours / available slot-hours
```

The elapsed completion time of a schedule is not the sum of all job durations when jobs run in parallel. It is the makespan: the time from the first job start until the final required job completes.

Use both metrics:
- **Slot-hours** measure consumption of the character's constrained job capacity.
- **Makespan** measures the calendar time until the production plan is complete.

## Blueprint availability and parallel production

Character job slots do not guarantee that the required blueprint can support all those jobs concurrently.

- A BPO has unlimited licensed runs, but EVE University's manufacturing/research guidance states that a single BPO can be used for only one active Manufacturing job at a time.
- A BPC has a finite licensed-run count and can be used only within that limit.
- Multiple BPCs can support parallel Manufacturing jobs, subject to the character's slots, materials, and facility access.
- Copying a BPO into multiple BPCs can therefore increase parallel production capacity, but copying consumes Science job slots and adds time and cost. [^ccp-blueprints] [^eveuni-research]

This creates a coupled production system: a character may have spare Manufacturing slots but insufficient BPC supply, or may have enough BPCs but insufficient Science capacity to replenish them.

For a BPC with (R_c) licensed runs and an output quantity (O) per run:

```text
Maximum units from one BPC = Rc × O
```

A production plan requiring more runs than the BPC's licensed capacity must use additional copies or separate jobs. Model each BPC's run capacity explicitly.

## Job duration and modifiers

Manufacturing duration depends on the blueprint's base time, selected run count, blueprint TE, character skills, structure role bonuses, and eligible manufacturing time rigs. The named effects and provisional formulas are documented in [Tech I Manufacturing](../02-production-systems/tech-1-manufacturing.md), [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md), and [Facilities and Rigs](../01-foundations/facilities-and-rigs.md).

Do not calculate throughput from the unmodified blueprint time if the job will be installed in a researched BPO, skilled character, and rigged Engineering Complex. Use the actual job quote when available. The combined time-modifier stacking and rounding model remains provisional pending independent comparison against in-game Industry quotes. [^eve-industry-formula-c4813] [^eve-omnitool-manufacturing]

## Batch sizing and material rounding

Larger jobs can reduce aggregate material rounding loss because ME and other material reductions are applied to the total job requirement before the final quantity is rounded. However, a production plan may be forced into multiple jobs by:

- BPC licensed-run limits.
- Maximum job run or duration limits.
- Blueprint availability and concurrent-use restrictions.
- Character job-slot availability.
- Material volume or stock availability.
- Facility and logistics constraints.

Material rounding is applied separately to each installed job. A plan split across multiple jobs can therefore consume more material than one equivalent large job. [^ccp-blueprints] [^eveuni-manufacturing]

The throughput optimizer should not combine jobs into one theoretical batch unless the blueprint, BPC, and game job limits permit it.

## Bottleneck analysis

Practical manufacturing throughput is constrained by the slowest required stage or resource:

| Constraint | Diagnostic question | Possible response |
|---|---|---|
| Character slots | Are all Manufacturing slots continuously occupied? | Train slot skills or add a production character |
| Job duration | Is long job time limiting units per slot-day? | Improve TE, skills, structure, or rig where economical |
| Blueprint availability | Is one BPO or too few BPCs serializing work? | Copy the BPO or acquire additional BPCs |
| Science capacity | Can copying/invention replenish BPCs fast enough? | Increase Science capacity or buy copies |
| Material supply | Are jobs idle due to missing inputs? | Improve procurement, sourcing, or buffer inventory |
| Facility service | Is the required Manufacturing service online and accessible? | Use a suitable alternative facility |
| Capital | Can the operation fund materials and installation fees? | Reduce batch size, shorten inventory cycle, or secure more working capital |
| Logistics | Are inputs or output delayed in transit? | Stage inventory closer to facilities or market |
| Market demand | Can the output be sold at the planned rate? | Reduce production rate or choose a more liquid product |

A useful first approximation is:

```text
Practical throughput
  = minimum of:
    character job-slot capacity
    blueprint/BPC capacity
    material supply capacity
    facility/service capacity
    capital-supported capacity
    market absorption capacity
```

These capacities must be converted to the same output unit and time horizon before taking the minimum.

## Throughput across a production chain

For a product requiring multiple stages, calculate each stage's output rate in equivalent final-product units.

Example chain:
- Copying or invention produces BPCs.
- Reactions produce intermediate materials.
- Component manufacturing consumes those materials.
- Final manufacturing produces the sellable product.

The chain's sustainable output rate cannot exceed the lowest normalized stage rate. If component manufacturing can supply 100 final products per day but invention supports only 40 BPC runs per day, the BPC supply constrains final output. If the BPC has multiple licensed runs, convert BPC production into equivalent final-product run capacity before comparing.

Do not add slot counts across different job pools as though they were interchangeable. Manufacturing, Science, and Reaction each have their own slots and their own job durations.

## Scheduling and utilization

A simple production schedule should:
1. Identify required jobs and dependencies.
2. Record each job's duration, run count, output, inputs, blueprint/BPC, and job pool.
3. Allocate jobs to available character slots.
4. Ensure the blueprint and materials are available at the selected facility.
5. Respect BPC licensed-run limits and any one-BPO/one-active-job restriction.
6. Avoid leaving a slot idle while a ready job is waiting.
7. Include time for copying, invention, reactions, and logistics when they are prerequisites.
8. Track delivery and market-sale timing separately from job completion.

The full scheduling problem is more complex than simply dividing output by job duration when jobs have different run sizes, shared blueprints, shared materials, and dependencies. See [Production Scheduling](production-scheduling.md).

## Economic throughput metrics

Use output rate alongside profitability:

- Units per manufacturing slot-hour.
- ISK contribution per manufacturing slot-hour.
- Units per wall-clock day.
- ISK contribution per wall-clock day.
- Material consumed per finished unit.
- Working capital required per unit of sustainable daily throughput.
- BPC licensed runs consumed per day.
- Fraction of available Manufacturing slot-hours used.

A product with the highest unit margin may not maximize total ISK per day if it uses long jobs, scarce BPCs, or high working capital. Throughput and profitability must be evaluated together.

## Verification requirements

The document uses published skill effects and community-derived combined time/material formulas. These still need validation against the in-game Industry quote. Specifically:
- Compare job duration for representative blueprint TE, Industry, Advanced Industry, structure, and rig combinations.
- Confirm actual BPO concurrent-use restrictions and behavior with multiple BPCs.
- Confirm current maximum runs and maximum job duration for representative blueprint categories.
- Compare theoretical slot utilization with actual delivery and re-install overhead.
- Verify material rounding for the same production plan split into different job sizes.

## Related concepts

- [Tech I Manufacturing](../02-production-systems/tech-1-manufacturing.md)
- [Blueprints and Research](../01-foundations/blueprints-and-research.md)
- [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md)
- [Facilities and Rigs](../01-foundations/facilities-and-rigs.md)
- [Blueprint Copying](../02-production-systems/blueprint-copying.md)
- [Science and Invention Throughput](science-and-invention-throughput.md)
- [Production Scheduling](production-scheduling.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)

[^ccp-manufacturing]: CCP Support, Manufacturing (updated 2024-08-29).
[^ccp-activities]: CCP Support, Activities and Job Types (updated 2024-08-29).
[^ccp-blueprints]: CCP Support, Blueprints (updated 2024-08-29).
[^eveuni-manufacturing]: EVE University Wiki, Manufacturing (accessed 2026-11-14).
[^eveuni-production-skills]: EVE University Wiki, Skills:Production (accessed 2026-11-14).
[^eveuni-research]: EVE University Wiki, Research (accessed 2026-11-14).
[^eve-industry-formula-c4813]: C4813.space, EVE Online Industry Formula (2025-07-25), community-derived combined job formula.
[^eve-omnitool-manufacturing]: EVE Omnitool, Industry Cost Calculator (accessed 2026-11-14), calculator-specific model.
