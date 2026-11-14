---
type: Computation
title: Research Investment ROI
description: Break-even and lifetime value of incremental ME and TE research on a BPO, including material rounding, slot-hour opportunity cost, and future production volume.
tags:
  - computation
  - research
  - blueprint
  - roi
sources:
  - id: ccp-me-research
    resource: https://support.eveonline.com/hc/en-us/articles/203210542-Material-Efficiency-Research
    title: Material Efficiency Research | EVE Online Support (updated 2024-07-15)
  - id: ccp-te-research
    resource: https://support.eveonline.com/hc/en-us/articles/203210512-Time-Efficiency-Research
    title: Time Efficiency Research | EVE Online Support (updated 2024-07-15)
  - id: ccp-copying
    resource: https://support.eveonline.com/hc/en-us/articles/203210602-Copying
    title: Copying | EVE Online Support (updated 2024-07-15)
  - id: ccp-activities-jobs
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: eveuni-research
    resource: https://wiki.eveuniversity.org/Research
    title: Research | EVE University Wiki (last modified 2026-03-21)
generated:
  by: openai/gpt-6
  at: 2026-11-14T10:20:00Z
status: draft
---

## Purpose

This computation evaluates whether another ME or TE research level on a BPO is economically worthwhile. Research is an investment in future production: it costs installation fees, Science slot-hours, and time during which the BPO may be unavailable for other work. The return is realized only through future production or the value of the improved BPCs copied from that BPO.

Evaluate each next research level incrementally. The value of ME 5 to ME 6 is not necessarily the same as ME 0 to ME 1, and the cost/time of later research levels increases. [^ccp-me-research] [^ccp-te-research]

## Mechanics used by the model

- ME research reduces material requirements by 1% per research level, up to 10 levels.
- TE research reduces manufacturing time by 2% per research level, up to 10 levels.
- Material rounding applies to the total installed job, not independently to each run.
- Certain single-item-per-run inputs are not reduced by ME.
- ME/TE research jobs consume Science capacity.
- A BPC inherits the BPO's ME/TE values at the time it is copied; existing BPCs do not improve when the BPO is researched later.

See [Blueprints and Research](../01-foundations/blueprints-and-research.md) and [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md). [^ccp-me-research] [^ccp-te-research] [^ccp-copying] [^ccp-activities-jobs]

## Required inputs

For the next research level, record:

| Symbol | Input | Source |
|---|---|---|
| ME_0 / TE_0 | Current BPO research levels | Blueprint |
| ME_1 / TE_1 | Proposed next research level | Research plan |
| C_R | Research installation fee | Live Industry quote |
| C_RM | Any consumed research inputs/materials | Live Industry quote and current replacement prices |
| C_A | BPO acquisition cost, only if purchased specifically for this investment | Acquisition price or opportunity cost |
| T_R | Research job duration | Live Industry quote |
| V_S | Opportunity value per Science slot-hour | Best alternative Science activity |
| V_B | Cost of BPO downtime or exclusive asset lock, if applicable | Production schedule |
| J | Expected future Manufacturing jobs using the improved BPO/BPC | Demand and production forecast |
| C_M0 | Material cost per production job at current ME | Current material prices and actual rounded job quantities |
| C_M1 | Material cost per production job at proposed ME | Same inputs, with proposed ME |
| T_M0 | Manufacturing time per job at current TE | Live quote or validated calculation |
| T_M1 | Manufacturing time per job at proposed TE | Same facility/character, proposed TE |
| V_M | Economic value of one Manufacturing slot-hour | Marginal contribution of the best alternative job |

Use the same run count, facility, character, material-price timestamp, and sale assumptions when comparing current and proposed research levels.

## Material Efficiency value

For one representative production job:

```text
ME material saving per job
  = C_M0 - C_M1
```

The material costs must be calculated from the actual rounded job quantities. Do not multiply the ME percentage by the total material bill and assume the result is exact. Small jobs may show no saving because of rounding, and single-item-per-run inputs are unaffected by ME. [^ccp-me-research]

If the BPO will be used for several different batch sizes, calculate savings separately for each realistic job configuration. The effective ME benefit can differ between a small batch and a large batch.

## Time Efficiency value

For one representative Manufacturing job:

```text
Manufacturing time saved per job
  = T_M0 - T_M1

TE time value per job
  = manufacturing time saved in hours × V_M
```

The value of saved time is not automatically ISK. It depends on whether Manufacturing capacity is constrained and whether the saved slot-hours can be used for another profitable job. If the character has idle Manufacturing slots, insufficient materials, or no additional market demand, the immediate economic value of the saved time may be low. [^ccp-te-research]

Use the live quote or a validated time model with the same character, facility, rigs, and system. Do not value TE as if it reduced materials.

## Research investment cost

The direct research investment is:

```text
Direct research investment = C_R + C_RM + C_A
```

For an economic model that includes scarce capacity:

```text
Science slot opportunity cost
  = T_R in hours × V_S

Total research investment
  = C_R + C_RM + C_A + (T_R × V_S) + V_B
```

V_B should be zero unless the BPO is genuinely prevented from generating value elsewhere during the research job. C_A is zero when the BPO is already owned and its acquisition cost is sunk for this decision. Include it when comparing the full purchase-and-research investment. Do not double-count a BPO constraint already reflected in the production schedule.

Research job duration increases with research level. Use the actual quote for the next level rather than assuming a constant duration per level. [^ccp-me-research] [^ccp-te-research]

## Break-even production jobs

For ME research:

```text
ME break-even jobs
  = total research investment / ME material saving per job
```

For TE research:

```text
TE break-even jobs
  = total research investment / TE time value per job
```

If the per-job benefit is zero or negative, the next level has no finite break-even under the current assumptions.

Round the required number of jobs up to the next whole job for planning. The expected future job count must be based on realistic demand and BPO/BPC supply, not the theoretical maximum output of the character.

## Combined ME and TE research

If the proposed investment includes both an ME and TE level, compare the combined research investment with the combined per-job benefit:

```text
Combined saving per production job
  = ME material saving per job
    + TE time value per job

Combined research investment
  = ME research investment + TE research investment

Break-even jobs
  = combined research investment / combined saving per job
```

Do not combine research costs if the two jobs would occur at different times or use different Science slot opportunities without reflecting that schedule.

## Lifetime net value and ROI

For J expected future production jobs:

```text
Total expected benefit
  = J × saving per production job

Net research value
  = total expected benefit - total research investment

Research ROI
  = net research value / total research investment
```

This simple ROI is undiscounted. If benefits occur over a long horizon, use a discounted cash-flow model:

```text
NPV
  = sum of future per-job savings discounted to today
    - research investment
```

State the discount rate and production schedule explicitly. Do not compare an undiscounted research investment with a discounted alternative.

## Worked ME example

The following values are illustrative assumptions. They are not current prices or a live job quote.

Assume:
- Research installation fee and any research inputs: 18,000,000 ISK.
- Science slot opportunity cost: 6,000,000 ISK.
- Total research investment: 24,000,000 ISK.
- Current ME material cost for a representative job: 100,000,000 ISK.
- Proposed ME level reduces the actual rounded job material cost to 98,800,000 ISK.
- Expected future production volume: 30 equivalent jobs.

Then:

```text
ME saving per job
  = 100,000,000 - 98,800,000
  = 1,200,000 ISK

Break-even jobs
  = 24,000,000 / 1,200,000
  = 20 jobs

Expected benefit over 30 jobs
  = 30 × 1,200,000
  = 36,000,000 ISK

Net research value
  = 36,000,000 - 24,000,000
  = 12,000,000 ISK

ROI
  = 12,000,000 / 24,000,000
  = 50%
```

The material saving must be recalculated using actual rounded quantities for the proposed batch. If the 1.2 million ISK saving disappears for smaller batches, the break-even result changes.

## Worked TE example

The following values are illustrative assumptions.

Assume:
- Research investment: 15,000,000 ISK.
- Proposed TE level saves 1.5 hours per Manufacturing job.
- The operation can use saved Manufacturing capacity for work worth 800,000 ISK per slot-hour.
- Expected future jobs: 20.

Then:

```text
TE time value per job
  = 1.5 × 800,000
  = 1,200,000 ISK

Break-even jobs
  = 15,000,000 / 1,200,000
  = 12.5, rounded up to 13 jobs

Expected benefit over 20 jobs
  = 20 × 1,200,000
  = 24,000,000 ISK

Net research value
  = 24,000,000 - 15,000,000
  = 9,000,000 ISK

ROI
  = 9,000,000 / 15,000,000
  = 60%
```

If the Manufacturing slot would otherwise remain idle, V_M may be close to zero and the TE investment may not pay back in economic terms.

## BPO and BPC timing

Research on a BPO does not retroactively improve BPCs that already exist. A research plan must therefore account for:
- Existing BPC inventory with old ME/TE.
- Future copies created after research completes.
- Whether the BPO is needed for active jobs during the research window.
- Whether BPC production can be staged ahead of the research job.
- Whether a different BPO or purchased BPC can supply production while research is underway. [^ccp-copying]

For a BPO that is used only to create copies, the research investment benefits future copies, not copies already in storage.

## Decision rule

A research level is economically justified when:
- The expected future production volume exceeds the break-even volume.
- The BPO will remain useful for that volume.
- The material/time saving survives job rounding and actual facility modifiers.
- The Science slot and BPO downtime opportunity costs are included.
- The operation has enough market demand and capital to realize the future savings.

Research can still be strategically justified for BPC resale, future flexibility, or long-term asset value, but those benefits should be explicitly valued rather than hidden in a manufacturing margin.

## Model limitations and verification

- Use live Industry quotes for research duration and installation fee.
- Confirm actual rounded material quantities at the intended batch size.
- Verify single-item-per-run material exceptions.
- Confirm the BPO's availability/concurrency restrictions for the planned job sequence.
- Include the temporary ME/TE research SCC surcharge as a configurable fee component; confirm the live quote.
- Compare the expected future job count with actual demand and BPC production.
- Track realized material and time savings after research.

## Related concepts

- [Blueprints and Research](../01-foundations/blueprints-and-research.md)
- [Blueprint Copying](../02-production-systems/blueprint-copying.md)
- [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md)
- [Science and Invention Throughput](../05-optimization/science-and-invention-throughput.md)
- [Installation Cost Computation](installation-costs.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)
- [Production Scheduling](../05-optimization/production-scheduling.md)

[^ccp-me-research]: CCP Support, Material Efficiency Research (updated 2024-07-15).
[^ccp-te-research]: CCP Support, Time Efficiency Research (updated 2024-07-15).
[^ccp-copying]: CCP Support, Copying (updated 2024-07-15).
[^ccp-activities-jobs]: CCP Support, Activities and Job Types (updated 2024-08-29).
[^eveuni-research]: EVE University Wiki, Research (last modified 2026-03-21).
