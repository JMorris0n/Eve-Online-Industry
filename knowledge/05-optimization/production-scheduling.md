---
type: Concept
title: Production Scheduling
description: Coordinating Manufacturing, Science, and Reaction jobs, shared assets, material flows, facility locations, and delivery timing.
tags:
  - optimization
  - scheduling
  - production
sources:
  - id: ccp-activities-jobs
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: ccp-manufacturing
    resource: https://support.eveonline.com/hc/en-us/articles/203210292-Manufacturing
    title: Manufacturing | EVE Online Support (updated 2024-08-29)
  - id: ccp-copying
    resource: https://support.eveonline.com/hc/en-us/articles/203210602-Copying
    title: Copying | EVE Online Support (updated 2024-07-15)
  - id: ccp-reactions
    resource: https://support.eveonline.com/hc/en-us/articles/115005405785-Reactions
    title: Reactions | EVE Online Support (updated 2024-08-29)
  - id: eveuni-manufacturing
    resource: https://wiki.eveuniversity.org/Manufacturing
    title: Manufacturing | EVE University Wiki
  - id: eveuni-research
    resource: https://wiki.eveuniversity.org/Research
    title: Research | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T08:00:00Z
status: draft
---

## Purpose

Production scheduling coordinates dependent industrial jobs so that character slots, blueprints, materials, facilities, capital, and logistics are available when required. The problem is a resource-constrained project scheduling problem: jobs have precedence dependencies, durations, and limited resource pools.

A schedule should not merely keep every slot occupied. It should deliver the required output at the required time, at acceptable economic cost and risk.

## Job pools are separate resources

EVE groups industrial jobs into three character-managed pools:

| Pool | Activities | Capacity source |
|---|---|---|
| Manufacturing | Manufacturing | Mass Production and Advanced Mass Production |
| Science | ME/TE research, copying, invention | Laboratory Operation and Advanced Laboratory Operation |
| Reaction | Reaction jobs | Mass Reactions and Advanced Mass Reactions |

Each pool has its own slot-hour budget. A Science job can run concurrently with a Manufacturing job and a Reaction job if their dependencies, assets, and locations permit. A character cannot use an unused Manufacturing slot to install a Science job. [^ccp-activities-jobs]

The maximum slot formulas and current skill constraints are documented in [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md).

## Model each activity as a job node

A scheduling job record should contain:

| Field | Purpose |
|---|---|
| Job ID | Stable identifier for the planned job |
| Activity | Manufacturing, ME, TE, Copying, Invention, or Reaction |
| Resource pool | Manufacturing, Science, or Reaction |
| Duration | Actual Industry quote duration |
| Runs and output | Job runs, output quantity, and expected output |
| Inputs | Material type IDs, quantities, and required location |
| Blueprint asset | BPO or BPC identifier and licensed-run availability |
| Exclusive asset locks | BPO/BPC or other asset that cannot be used concurrently |
| Facility | Structure/station and online service requirement |
| Location | Solar system and station/structure |
| Predecessors | Jobs or transfers that must finish first |
| Installation fee | Current job quote fee |
| Start/end window | Earliest start, deadline, and expected completion |
| Risk flags | Structure state, route exposure, input uncertainty, market risk |

Durations and installation fees should come from the live Industry quote wherever possible. A theoretical formula is useful for planning, but the quote is the operational input.

## Precedence dependencies

A production chain is a directed acyclic graph (DAG) of jobs and transfers. A downstream job cannot start until its required inputs, blueprint, and facility access are available at the destination.

Examples:

- A BPO research job must finish before a new BPC can inherit the improved ME/TE values.
- A Copy job must finish before its BPC output can be used for manufacturing or invention.
- An Invention job must finish successfully before the resulting Tech II BPC can be used for Tech II manufacturing.
- A Reaction job must finish and deliver its output before a downstream component job can consume the material.
- A component job must finish before a final hull or module job can use the component.

The Science, Manufacturing, and Reaction pools can work in parallel when the chain has sufficient inventory buffers. [^ccp-copying] [^ccp-reactions] [^eveuni-research]

## Resource constraints

A valid schedule must respect all of the following:

### Character slot constraints

For each pool (p) and planning horizon (H):

```text
Active slot-hours in pool p
  ≤ available slots in pool p × 24 × H
```

Each job consumes one slot in its activity pool for its duration. Different pools are independent, but jobs within the same pool compete for the same slots.

### Blueprint and copy constraints

A BPO has unlimited licensed runs but can be unavailable while being used by an active job. A BPC has finite licensed runs. Multiple BPCs can support parallel manufacturing or invention jobs, subject to character slots and input availability. [^ccp-copying] [^eveuni-manufacturing]

Model BPO/BPC availability as a separate resource constraint rather than assuming that the character's slot count alone determines concurrency. The exact restriction on using one BPO across concurrent activities should be verified for the relevant job types and ownership context.

### Material constraints

All required materials must be present at the destination when the job is installed. Remote-start skills do not move materials or blueprints. A schedule therefore needs transfer nodes or pre-staged inventory when jobs use different locations. [^ccp-manufacturing]

Material quantities must be calculated per installed job, including the game's rounding behavior. Splitting a large production plan into many small jobs can change total material consumption and increase the number of installation fees. [^ccp-copying] [^eveuni-manufacturing]

### Facility constraints

The selected facility must offer the activity and have the relevant service module online. Structure role bonuses, rigs, system cost indices, taxes, and access permissions affect the job's economics or availability. A low-cost facility is not usable if the required blueprint or materials cannot be staged there.

### Capital constraints

A job should not be scheduled merely because a slot is free. The operation must have enough working capital for materials, installation fees, upstream jobs, logistics, and the inventory period before sale proceeds return. See [Capital and Asset Management](../04-industrial-economics/capital-and-asset-management.md).

## Earliest-start scheduling

For a job (j), its earliest feasible start is the latest of:

- Completion of all predecessor jobs.
- Arrival of all required materials.
- Availability of the required blueprint/BPC.
- Availability of a slot in the relevant character pool.
- Availability of the destination facility and service.
- Any user-defined release time or operational window.

Its completion time is:

```text
Job completion = scheduled start + quoted job duration
```

For a simple single-character schedule, maintain three separate slot calendars. Assign each job to the earliest available slot in its pool, but only after its dependencies and required assets are ready.

This greedy earliest-start method is a useful baseline. A more advanced optimizer may reorder jobs to maximize economic contribution, reduce inventory holding time, or meet deadlines.

## Critical path and makespan

The critical path is the longest-duration chain of dependent jobs and transfers. It determines the earliest possible completion time for the overall plan, assuming all resource constraints are met.

The makespan is:

```text
Makespan
  = final completion time - first scheduled start time
```

The sum of all job durations is not the makespan when jobs run in parallel. Conversely, a plan with a short critical path can still be infeasible if several jobs require the same scarce slot or BPO at the same time.

Track:
- Total slot-hours per pool.
- Makespan.
- Critical-path jobs.
- Idle time caused by missing inputs or assets.
- Waiting time caused by full slot pools.
- Inventory held between stages.
- Total installation and logistics cost.

## Batch sizing and release timing

Batch size affects material rounding, job count, installation fees, blueprint usage, and inventory holding time.

Larger jobs may reduce material-rounding loss and reduce the number of job installations. Smaller jobs can reduce peak working capital, create output sooner, or fit limited BPC runs. The best batch size balances these effects.

Use a release policy:
- **Make-to-stock:** produce against a target inventory level or expected demand.
- **Make-to-order:** install production after a sale or confirmed demand signal.
- **Replenishment:** trigger new jobs when inventory falls below a defined threshold.
- **Just-in-time:** schedule upstream outputs to arrive shortly before downstream consumption.

For a replenishment stock:

```text
Reorder point
  = expected daily consumption × replenishment lead time
    + safety stock
```

The safety stock should reflect uncertainty in extraction, reaction/invention success, hauling, facility availability, and market demand.

## Scheduling objectives

A schedule can optimize different objectives. Do not assume they produce the same job order.

| Objective | Primary metric | Trade-off |
|---|---|---|
| Maximize profit | Net contribution over horizon | May leave low-margin jobs idle |
| Maximize throughput | Finished units per day | May favor high-volume, low-margin products |
| Maximize slot efficiency | ISK per slot-hour | Can tie up capital or create unsold inventory |
| Minimize makespan | Time to final delivery | May require more inventory or parallel jobs |
| Minimize working capital | Peak capital deployed | May lengthen the production cycle |
| Minimize risk | Expected loss and asset exposure | May increase hauling or facility costs |

For a profit-focused operation, a useful ranking input is marginal net contribution per constrained slot-hour, but it must be adjusted for job dependencies, output demand, capital, and asset constraints.

## Example scheduling logic

A simplified pipeline might have:
1. Copy a Tech I BPO into several BPCs.
2. Run invention on some copies.
3. React Hybrid Polymers in a Reaction slot pool.
4. Manufacture Hybrid Tech Components in Manufacturing slots.
5. Manufacture final Tech III products from the resulting BPCs and components.

Copying, invention, and reactions can run in parallel if the inputs and locations are ready. Final manufacturing waits until both the invented BPC and required components are available. The schedule should maintain enough BPC and component inventory to avoid starving final manufacturing, but not so much that capital is unnecessarily tied up.

This is an example of the scheduling structure, not a fixed recommended order or batch size.

## Replanning triggers

Recalculate the schedule when:
- A job succeeds or fails unexpectedly.
- An invention attempt produces fewer BPCs than expected.
- A structure service goes offline or changes state.
- Material prices or availability change materially.
- A courier contract is delayed or fails.
- A market order fills faster/slower than expected.
- A BPO/BPC or character slot becomes unavailable.
- A patch changes formula inputs, job duration, fees, or facility eligibility.

Keep the original schedule and the revised schedule so the project can measure forecast error and improve future estimates.

## Output format for a production schedule

A useful schedule export should include:
- Job ID and activity.
- Pool and slot assignment.
- Start and completion timestamps.
- Facility and system.
- BPO/BPC and licensed runs.
- Inputs and required quantities.
- Predecessor jobs and transfer dependencies.
- Expected output and uncertainty.
- Installation fee and material cost.
- Inventory buffer before and after the job.
- Critical-path status and delay risk.

The schedule should be reproducible from saved inputs and job quotes, not merely a manually maintained list of start times.

## Verification requirements

- Confirm the exact concurrent-use restrictions for a BPO across Manufacturing, copying, and research activities.
- Confirm maximum runs and duration limits for representative job types.
- Test whether all relevant Science activities can be installed remotely under Scientific Networking.
- Validate the schedule model against a mixed-pool plan with real job quotes.
- Compare predicted material totals for single large jobs versus multiple smaller jobs.
- Record actual idle time, completion times, and inventory buffers for a real production cycle.

## Related concepts

- [Manufacturing Throughput](manufacturing-throughput.md)
- [Science and Invention Throughput](science-and-invention-throughput.md)
- [Reaction Throughput](reaction-throughput.md)
- [Character Specialization](character-specialization.md)
- [Industrial Scaling](industrial-scaling.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)
- [Capital and Asset Management](../04-industrial-economics/capital-and-asset-management.md)
- [Logistics and Risk](../04-industrial-economics/logistics-and-risk.md)

[^ccp-activities-jobs]: CCP Support, Activities and Job Types (updated 2024-08-29).
[^ccp-manufacturing]: CCP Support, Manufacturing (updated 2024-08-29).
[^ccp-copying]: CCP Support, Copying (updated 2024-07-15).
[^ccp-reactions]: CCP Support, Reactions (updated 2024-08-29).
[^eveuni-manufacturing]: EVE University Wiki, Manufacturing (accessed 2026-11-14).
[^eveuni-research]: EVE University Wiki, Research (accessed 2026-11-14).
