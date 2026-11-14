---
type: Concept
title: Science and Invention Throughput
description: Science job-slot allocation, research and copying output rates, invention attempts, expected BPC supply, and Science-pool bottlenecks.
tags:
  - optimization
  - science
  - invention
  - blueprint-copying
sources:
  - id: ccp-activities-jobs
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: ccp-invention
    resource: https://support.eveonline.com/hc/en-us/articles/203210642-Invention
    title: Invention | EVE Online Support (updated 2024-08-29)
  - id: ccp-copying
    resource: https://support.eveonline.com/hc/en-us/articles/203210602-Copying
    title: Copying | EVE Online Support (updated 2024-07-15)
  - id: ccp-me-research
    resource: https://support.eveonline.com/hc/en-us/articles/203210542-Material-Efficiency-Research
    title: Material Efficiency Research | EVE Online Support (updated 2024-07-15)
  - id: ccp-te-research
    resource: https://support.eveonline.com/hc/en-us/articles/203210512-Time-Efficiency-Research
    title: Time Efficiency Research | EVE Online Support (updated 2024-07-15)
  - id: eveuni-research
    resource: https://wiki.eveuniversity.org/Research
    title: Research | EVE University Wiki (last modified 2026-03-21)
  - id: eveuni-invention
    resource: https://wiki.eveuniversity.org/Invention
    title: Invention | EVE University Wiki (last modified 2026-10-09)
  - id: eveuni-science-skills
    resource: https://wiki.eveuniversity.org/Skills:Science
    title: Skills:Science | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T07:40:00Z
status: draft
---

## Purpose

Science and Invention Throughput measures how efficiently a character uses the Science job pool to research BPOs, create BPCs, and generate expected Tech II BPC output through invention.

The Science pool is shared. A character cannot treat ME research, TE research, copying, and invention as four independent job queues. Every Science job consumes the same finite slot-hour budget. [^ccp-activities-jobs]

## Science job-slot capacity

```text
Science slots
  = 1 + Laboratory Operation level
      + Advanced Laboratory Operation level
```

The base capacity is one slot. Laboratory Operation and Advanced Laboratory Operation each add one slot per level, producing a theoretical maximum of 11 concurrent Science jobs at both skills V. Advanced Laboratory Operation requires Laboratory Operation V. [^eveuni-research] [^eveuni-science-skills]

The available Science slot-hour budget over a planning horizon of H days is:

```text
Available Science slot-hours
  = Science slots × 24 × H
```

This budget is consumed by all active Science jobs, including ME research, TE research, copying, and invention.

## Activities and their outputs

| Science activity | Job output | Throughput unit |
|---|---|---|
| ME research | BPO ME level advancement | ME levels per slot-hour |
| TE research | BPO TE level advancement | TE levels per slot-hour |
| Copying | One or more BPCs with licensed runs | BPCs or copied licensed runs per slot-hour |
| Invention | Probabilistic Tech II BPC outputs | Expected successful BPCs or manufacturing runs per slot-hour |

These activities compete for the same Science job slots, but their outputs are not directly interchangeable. A copy job supplies manufacturing or invention BPCs; an invention job supplies Tech II manufacturing runs; a research job improves a BPO's future production economics. [^ccp-activities-jobs]

## Activity throughput model

For any Science job:

```text
Output rate per slot-hour
  = activity output quantity / job duration in hours
```

For a character with S Science slots, the theoretical output rate under continuous use is:

```text
Theoretical activity output per day
  = S × 24 × output rate per slot-hour
```

This assumes the character can install the next job immediately, has the required BPO/BPC and inputs ready, and does not lose capacity to scheduling gaps or remote-location constraints. Use actual Industry quotes for job duration. The exact combined time effects of skills, facility role bonuses, and rigs should not be inferred from a single generic Science time formula.

## ME and TE research throughput

ME and TE research consume Science slots. Each research job advances a BPO's relevant efficiency level and ties up the blueprint while the job is active. The time required increases with research level; later levels take longer than earlier levels. [^ccp-me-research] [^ccp-te-research]

Character skills that reduce the relevant research duration include:
- **Metallurgy:** reduces ME research time.
- **Research:** reduces TE research time.
- **Advanced Industry:** reduces research time.
- Facility role bonuses and eligible research rigs can also affect job duration.

The per-level skill effects and exact time formula are documented in [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md) and [Facilities and Rigs](../01-foundations/facilities-and-rigs.md). Use the displayed Industry duration for the specific BPO and research level. [^eveuni-research] [^eveuni-science-skills]

Research throughput is measured in BPO levels advanced per Science slot-hour, not finished items per hour. The economic value of a research job is the future material or time saving it creates across the expected lifetime production volume of the BPO. See [Research Investment ROI](../09-computations/research-investment-roi.md).

## Copying throughput

Copying consumes Science capacity and converts a BPO into one or more BPCs. The copy-job interface has two distinct quantities:

- **Job Runs:** number of BPC objects to create.
- **Runs per Copy:** licensed production runs assigned to each created BPC.

For a copy job:

```text
BPCs produced = Job Runs

Copied licensed-run capacity
  = Job Runs × Runs per Copy
```

The total copied licensed-run capacity is the useful throughput measure when BPCs will be used for manufacturing. If a BPC is intended for invention, one licensed run is consumed per invention attempt, so its run capacity can also be expressed as available invention attempts. [^ccp-copying] [^eveuni-research]

CCP states that copy-job input materials, where required, scale with the number of copies produced, not with the licensed runs assigned to each copy. Copy-job duration is based on total licensed runs across all copies. These rules make Job Runs and Runs per Copy separate optimization variables. [^ccp-copying]

The copy duration model and its uncertainty are documented in [Blueprint Copying](../02-production-systems/blueprint-copying.md). Copying should be scheduled to replenish the BPC inventory required by downstream manufacturing and invention, rather than maximizing the number of BPC objects without regard to their run capacity.

## Invention throughput

Tech II invention is a probabilistic Science activity. Each invention run is one attempt and consumes one licensed run from the input Tech I BPC. Datacores and any selected decryptor are consumed regardless of success. A successful attempt produces a Tech II BPC whose licensed runs, ME, and TE depend on the base output and selected decryptor. [^ccp-invention] [^eveuni-invention]

Let:
- N = invention attempts in the job.
- p = displayed success probability per attempt, as a decimal.
- Ro = licensed manufacturing runs on each successful output BPC.
- O = finished units produced per manufacturing run.

Under the independent-attempt expected-value model:

```text
Expected successful BPCs per job = N × p

Expected Tech II manufacturing runs per job
  = N × p × Ro

Expected finished units supported
  = N × p × Ro × O
```

The expected number of successful BPCs is an average over repeated jobs, not a guarantee for any single job. The probability of at least one success in N independent attempts is:

```text
P(at least one success) = 1 - (1 - p)^N
```

Use the success chance shown by the Industry UI and the actual output preview for the selected item/decryptor. The complete Tech II invention mechanics and probability formula are documented in [Tech II Invention](../02-production-systems/tech-2-invention.md). [^ccp-invention] [^eveuni-invention]

### Expected invention throughput per slot-hour

```text
Expected successful BPCs per slot-hour
  = (N × p) / job duration in hours

Expected manufacturing runs per slot-hour
  = (N × p × Ro) / job duration in hours
```

This lets invention output be compared with manufacturing consumption. If invention supplies fewer manufacturing runs per day than the manufacturing operation consumes, the invention stage is the bottleneck unless BPC inventory is drawn down.

## Allocating the Science pool

A Science-focused character may allocate slots among several activities. For example, a character with 11 Science slots could assign two slots to ME/TE research, three to copying, and six to invention. This is an illustrative allocation, not a recommended universal split.

The correct allocation depends on:
- Current BPO research backlog.
- Daily manufacturing demand for BPC runs.
- Expected invention success and output run counts.
- BPC inventory already available.
- Job duration and facility access.
- Installation fees and the value of the character's time.
- Whether buying BPCs or invented outputs is cheaper than producing them internally.

For a planning horizon H, total Science slot-hours allocated across all activities cannot exceed:

```text
Σ Science job slot-hours
  ≤ Science slots × 24 × H
```

An optimizer should allocate slot-hours to the activity with the highest marginal economic value, subject to required production dependencies and inventory targets.

## Cross-pool bottleneck: invention to manufacturing

Science and Manufacturing are separate pools. This allows a character to run invention jobs while manufacturing previously invented BPCs. However, the sustainable output of the combined operation is constrained by both pools.

A simplified Tech II pipeline is:
1. Copying produces Tech I BPCs.
2. Invention consumes Tech I BPC runs and produces expected Tech II BPCs.
3. Manufacturing consumes Tech II BPC runs and produces finished items.

Normalize each stage to equivalent finished Tech II units per day:

```text
Sustainable Tech II output rate
  = minimum of:
    Tech I BPC supply rate
    invention-supported Tech II run rate
    manufacturing output rate
    material supply rate
    capital-supported rate
    market absorption rate
```

This is a bottleneck model. Inventory buffers can temporarily allow downstream stages to exceed upstream throughput, but they do not increase the long-run sustainable rate.

## Remote installation

Scientific Networking allows Science jobs to be started remotely, subject to its skill level and jump range. The skill does not move BPOs, BPCs, datacores, decryptors, or other required inputs. The required assets must already be at the destination facility. See [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md). [^eveuni-research] [^eveuni-science-skills]

## Common optimization errors

1. Treating invention as a separate job pool rather than part of Science.
2. Comparing Science and Manufacturing slot counts without converting each activity to equivalent output per day.
3. Treating invention success as guaranteed rather than probabilistic.
4. Ignoring failed attempts when estimating datacore, decryptor, and BPC consumption.
5. Producing too many low-run BPCs and increasing handling overhead.
6. Producing BPCs with too few licensed runs for the planned manufacturing batch.
7. Failing to account for the time required to copy or invent the BPCs consumed by manufacturing.
8. Treating a full Science slot schedule as optimal even when some activities have little marginal economic value.
9. Assuming remote-start skills transport blueprints or inputs.
10. Using an invention probability formula without checking the current Industry UI result.

## Verification requirements

The throughput framework uses documented activity types, skill slot formulas, and the current Tech II invention model. It still needs independent testing for:
- ME/TE research duration across several levels and facilities.
- Copy duration for different Job Runs and Runs per Copy combinations.
- Invention duration and the exact inputs consumed by multi-run jobs.
- Invention output BPC run/ME/TE results across decryptors and item categories.
- Combined Science time modifiers from skills, structure role, and rigs.
- Actual slot utilization in a mixed research/copy/invention schedule.

## Related concepts

- [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md)
- [Blueprints and Research](../01-foundations/blueprints-and-research.md)
- [Blueprint Copying](../02-production-systems/blueprint-copying.md)
- [Tech II Invention](../02-production-systems/tech-2-invention.md)
- [Tech III Manufacturing](../02-production-systems/tech-3-manufacturing.md)
- [Manufacturing Throughput](manufacturing-throughput.md)
- [Production Scheduling](production-scheduling.md)
- [Invention Economics Computation](../09-computations/invention-economics.md)
- [Research Investment ROI](../09-computations/research-investment-roi.md)

[^ccp-activities-jobs]: CCP Support, Activities and Job Types (updated 2024-08-29).
[^ccp-invention]: CCP Support, Invention (updated 2024-08-29).
[^ccp-copying]: CCP Support, Copying (updated 2024-07-15).
[^ccp-me-research]: CCP Support, Material Efficiency Research (updated 2024-07-15).
[^ccp-te-research]: CCP Support, Time Efficiency Research (updated 2024-07-15).
[^eveuni-research]: EVE University Wiki, Research (last modified 2026-03-21).
[^eveuni-invention]: EVE University Wiki, Invention (last modified 2026-10-09).
[^eveuni-science-skills]: EVE University Wiki, Skills:Science (accessed 2026-11-14).
