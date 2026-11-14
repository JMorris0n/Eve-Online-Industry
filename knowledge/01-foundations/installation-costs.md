---
type: Concept
title: Installation Costs
description: Overview of EVE industry job installation fee components, activity-specific cost indices, taxes, and exceptions.
tags:
  - costs
  - industry
  - installation-fees
sources:
  - id: ccp-viridian-fees
    resource: https://www.eveonline.com/news/view/viridian-expansion-notes
    title: Viridian Expansion Notes | EVE Online (2023-06-09)
  - id: ccp-scc-baseline
    resource: https://www.eveonline.com/news/view/patch-notes-version-21-06
    title: Patch Notes - Version 21.06 (2024-02-01 change)
  - id: ccp-research-scc-relief
    resource: https://www.eveonline.com/news/view/exploration-and-industry-balance-rework
    title: Exploration and Industry Balance Rework (2025-07-18)
  - id: ccp-exordium-fees
    resource: https://www.eveonline.com/news/view/patch-notes-version-23-02
    title: Patch Notes - Version 23.02 | EVE Online
generated:
  by: openai/gpt-6
  at: 2026-11-14T10:00:00Z
status: draft
---

## Summary

An Industry installation fee is calculated from the job's Estimated Item Value (EIV), the activity-specific System Cost Index (SCI), applicable structure/rig cost modifiers, facility tax, the SCC surcharge, and any applicable Alpha-clone or regional surcharge. It is not simply a percentage of the actual ISK paid for materials. [^ccp-viridian-fees]

The general CCP equation is:

```text
Total Installation Fee
  = EIV × ((SCI × applicable cost modifiers)
           + Facility Tax
           + SCC Surcharge
           + Alpha-clone Tax
           + applicable regional surcharge)
```

Structure and rig cost bonuses modify the SCI component, not the separate tax components. The current SCI is activity-specific and changes over time. Use the live Industry quote and current ESI data rather than hardcoding an index. [^ccp-viridian-fees]

## Important current fee values

| Component | Published value or treatment | Notes |
|---|---|---|
| NPC facility tax | 0.25% | CCP's Viridian change |
| Upwell facility tax | Owner-set, up to 10% | Check the selected facility |
| Alpha-clone tax | 0.25% | Separate EIV-based component |
| SCC surcharge baseline | 4% | CCP raised it in February 2024 |
| ME research SCC surcharge | 2% | CCP reduced it from 4% in July 2025; explicitly described as temporary |
| TE research SCC surcharge | 2% | Same temporary research-specific reduction |
| Exordium regional surcharge | +5% | Applies to manufacturing, ME research, TE research, and invention in that region |

The 2% ME/TE research value is the latest explicit CCP statement found as of 2026-11-14. Because CCP described it as temporary, retain it as a separate configurable value and confirm it in the live Industry quote. Do not apply it to copying, invention, or reactions without direct evidence. [^ccp-scc-baseline] [^ccp-research-scc-relief] [^ccp-exordium-fees]

## Estimated Item Value

For Manufacturing, EVE University documents EIV as the sum of ME0 job material quantities multiplied by CCP adjusted prices. EIV is a fee valuation basis, not the actual procurement cost, opportunity cost, or sale value of the product. [^ccp-viridian-fees]

Other activities can have different value bases. Do not reuse the Manufacturing EIV calculation for ME/TE research, copying, invention, or reactions without validating the activity's current calculation.

## Operational requirements

Before installing a job:
1. Select the correct activity and destination system.
2. Confirm the current activity SCI.
3. Confirm the facility tax, structure role, and exact fitted rigs.
4. Confirm the character's Alpha/Omega state.
5. Check any region-specific fee exception.
6. Obtain and record the live Industry quote.

The detailed equations, variable definitions, activity-specific cautions, and worked example are in [Industry Installation Cost Computation](../09-computations/installation-costs.md).

## Verification status

The published fee framework is documented, but exact EIV/process-value bases, rounding, and structure/rig interactions for every activity still require comparison against live Industry quotes. The 2% ME/TE research surcharge also requires current in-game confirmation because CCP described the reduction as temporary.

[^ccp-viridian-fees]: CCP, Viridian Expansion Notes (2023-06-09).
[^ccp-scc-baseline]: CCP, Patch Notes - Version 21.06 (2024-02-01.1), SCC surcharge increased to 4%.
[^ccp-research-scc-relief]: CCP, Exploration and Industry Balance Rework (2025-07-18), SCC surcharge reduced to 2% for ME and TE research, described as temporary.
[^ccp-exordium-fees]: CCP, Patch Notes - Version 23.02, Exordium regional industry fee changes.
