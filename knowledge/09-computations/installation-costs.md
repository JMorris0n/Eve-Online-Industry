---
type: Computation
title: Industry Installation Cost Computation
description: General installation-fee equation, manufacturing EIV, activity cost indices, structure modifiers, taxes, and provisional research surcharge exception.
tags:
  - computation
  - industry
  - installation-fees
  - economics
sources:
  - id: ccp-viridian-fees
    resource: https://www.eveonline.com/news/view/viridian-expansion-notes
    title: Viridian Expansion Notes | EVE Online (2023-06-09)
  - id: ccp-scc-baseline
    resource: https://www.eveonline.com/news/view/patch-notes-version-21-06
    title: Patch Notes - Version 21.06 | EVE Online (2024-02-01 change)
  - id: ccp-research-scc-relief
    resource: https://www.eveonline.com/news/view/exploration-and-industry-balance-rework
    title: Exploration and Industry Balance Rework | EVE Online (2025-07-18)
  - id: ccp-exordium-fees
    resource: https://www.eveonline.com/news/view/patch-notes-version-23-02
    title: Patch Notes - Version 23.02 | EVE Online (Exordium industry fee exception)
  - id: ccp-esi-overview
    resource: https://developers.eveonline.com/docs/services/esi/overview/
    title: EVE Swagger Interface (ESI) Overview
  - id: eveuni-manufacturing
    resource: https://wiki.eveuniversity.org/Manufacturing
    title: Manufacturing | EVE University Wiki
  - id: eveuni-research
    resource: https://wiki.eveuniversity.org/Research
    title: Research | EVE University Wiki (last modified 2026-03-21)
  - id: eveuni-structure-browser
    resource: https://wiki.eveuniversity.org/Structure_Browser
    title: Upwell structure | EVE University Wiki
  - id: eve-reactions-calculator-method
    resource: https://reactions.coalition.space/about
    title: EVE Reactions Calculator methodology
  - id: everef-engineering-complexes
    resource: https://everef.net/structures/engineering-complexes
    title: Engineering Complexes | EVE Ref
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:25:24Z
status: draft
---

## Summary

Industry installation fees are not simply a fixed tax or a percentage of the materials actually purchased. CCP's general equation separates a dynamic System Cost Index (SCI) component from facility tax, SCC surcharge, and Alpha-clone tax. CCP also specifies that taxes are applied directly to Estimated Item Value (EIV), not to an SCI-adjusted value. [^ccp-viridian-fees]

The fee model must be parameterized by activity and location. SCI is activity-specific and dynamic. Structure and rig bonuses modify only the SCI component in CCP's fee equation; the facility tax, SCC surcharge, and Alpha-clone tax remain separate EIV-based components. [^ccp-viridian-fees]

## General installation fee equation

CCP's published general equation is:

**Total Installation Fee = EIV × ((SCI × Bonuses) + Facility Tax + SCC + AlphaClone)**

Definitions:

| Variable | Meaning |
|---|---|
| EIV | Estimated Item Value used as the base for the installation-fee calculation |
| SCI | Current System Cost Index for the activity and solar system |
| Bonuses | Applicable facility/structure and rig modifiers to the SCI component |
| Facility Tax | NPC station tax or player-owned facility tax |
| SCC | Secure Commerce Commission surcharge |
| AlphaClone | Alpha-clone tax, where applicable |

The structure and rig modifier should be represented as a multiplier on the SCI term, not subtracted from the tax terms. For example, a 3% reduction to the SCI component is represented by a multiplier of 0.97. Do not subtract three percentage points from the complete fee. [^ccp-viridian-fees] [^everef-engineering-complexes]

## Fee components

### System Cost Index

SCI is a dynamic activity-specific value associated with the solar system where the job is installed. Do not store a single SCI per system for all industry activity types. The Industry UI displays the current facility/activity cost information, and the public ESI route for industry systems exposes system cost indices by activity. ESI is CCP's official REST API for third-party development. [^ccp-esi-overview]

Use the current returned activity index or the in-game job quote. Do not reproduce old community formulas for SCI from historical job-hour ratios: EVE University's Manufacturing page itself warns that its older 28-day square-root description may no longer be correct after CCP changed the formula to make the index more volatile. [^eveuni-manufacturing]

### Structure and rig bonuses

The Bonuses term includes applicable activity-specific structure and rig modifiers.

Engineering Complexes have the following innate installation-cost reductions for Manufacturing and Science jobs:

| Structure | SCI component multiplier | Reduction to SCI component |
|---|---:|---:|
| Raitaru | 0.97 | 3% |
| Azbel | 0.96 | 4% |
| Sotiyo | 0.95 | 5% |

These are reductions to the SCI component only, not the total fee. Applicable cost-optimization rigs may further modify selected manufacturing, copying, ME research, TE research, or invention SCI components. Rig compatibility is activity- and item-specific. [^everef-engineering-complexes] [^eveuni-structure-browser]

Do not apply an Engineering Complex cost bonus to a Refinery or Citadel by analogy. Confirm the selected structure's actual role and the fitted rig's exact activity/type scope.

### Facility tax

CCP's Viridian fee change set the NPC-station facility tax to 0.25% and allowed player-owned Upwell facility owners to set their industry facility tax. The maximum owner-set industry service tax is 10%. These taxes are calculated directly against EIV. The live facility tax shown by the Industry interface is the value to use for a job quote. [^ccp-viridian-fees]

### SCC surcharge

CCP's 2024-02-01 patch notes increased the baseline SCC surcharge from 1.5% to 4%. [^ccp-scc-baseline]

There is a specific documented exception for blueprint Material Efficiency and Time Efficiency research: CCP's 2025-07-18 industry balance post reduced the SCC component for those two research activities to 2% (half the 4% baseline). CCP explicitly described the reduction as temporary. No official removal date is stated in that post. [^ccp-research-scc-relief]

As of this research pass (2026-11-14), the 2% value is the latest explicit CCP statement found for ME and TE research, but it should be treated as provisional until confirmed by the live Industry quote or a newer CCP announcement. Do not extend the 2% exception to copying, invention, or other job types without direct evidence.

### Alpha-clone tax

CCP's Viridian change set the Alpha-clone tax to 0.25%. It is a separate component applied to EIV and applies where the character installing the job is an Alpha clone. [^ccp-viridian-fees]

## Estimated Item Value

For Manufacturing, EVE University describes EIV as the estimated material value of the job based on the blueprint's ME0 material requirements, with no facility or character bonuses applied. The calculation is the sum of each material's quantity multiplied by its CCP adjusted price from ESI. [^eveuni-manufacturing]

**Manufacturing EIV = Σ (ME0 job material quantity × CCP adjusted item price)**

Important distinctions:

- EIV is a standard valuation base for the installation fee, not necessarily the actual amount paid to acquire the materials.
- It is not the cost of the finished item or its expected sale value.
- Do not reduce EIV by the BPO's ME, a structure's material bonus, or a manufacturing rig's material bonus when using the Manufacturing EIV definition above. Those effects change required materials or other job properties, not the stated ME0 valuation basis.
- If materials were mined, reprocessed, purchased earlier, or acquired by contract, their opportunity cost and accounting cost may differ from EIV. See [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md).

ESI's public adjusted-prices route is /markets/prices/. The Industry UI quote is still the practical cross-check for the exact job. [^eveuni-manufacturing] [^ccp-esi-overview]

## Activity-specific cautions

The general fee equation is common, but the job's EIV/process-value basis and SCI activity must not be assumed identical for every job type.

| Activity | Cost-index treatment | Modeling guidance |
|---|---|---|
| Manufacturing | Manufacturing SCI | Use the Manufacturing EIV method above, current SCI, and applicable structure/rig modifiers |
| ME research | Research SCI | Use the actual job quote; the 2% SCC exception is documented by CCP but temporary |
| TE research | Research SCI | Use the actual job quote; the 2% SCC exception is documented by CCP but temporary |
| Copying | Copying SCI | Treat as separate from research; do not reuse Manufacturing EIV without validating the activity's value basis |
| Invention | Invention SCI | Use the actual job quote; cost rigs can be invention-specific |
| Reactions | Reaction SCI | Use reaction formula inputs and run count as the valuation basis in a secondary calculator model; validate against the in-game quote |

The EVE University Research article contains useful secondary calculations for research and copying process values, but it is not a CCP fee specification. Use those equations as an analytical lead, not as a production model until tested against current in-game quotes. [^eveuni-research]

For reactions, the EVE Reactions Calculator documents an EIV method based on reaction runs multiplied by the sum of material quantities and ESI adjusted prices, and a job cost method using the reaction SCI, facility tax, and SCC. This is a secondary, tool-specific method, not a substitute for testing the game's fee quote. [^eve-reactions-calculator-method]

## Worked Manufacturing example

This is an arithmetic illustration only, not a live quote.

Assumptions:

- Manufacturing EIV: 100,000,000 ISK.
- Manufacturing SCI: 5% (0.05).
- Facility: Raitaru, with its 3% SCI-component reduction (0.97 multiplier).
- Facility tax: 1% (0.01).
- SCC: 4% (0.04).
- Alpha-clone tax: 0%.

Calculation:

- Adjusted SCI component: 0.05 × 0.97 = 0.0485 (4.85%).
- Total fee rate: 0.0485 + 0.01 + 0.04 + 0 = 0.0985 (9.85%).
- Installation fee: 100,000,000 × 0.0985 = **9,850,000 ISK**.

The 3% Raitaru role bonus reduces the SCI component from 5.00% to 4.85%. It does not reduce the 1% facility tax or 4% SCC surcharge. This distinction is the principal reason to preserve CCP's parenthesized equation exactly.

## Special location and temporary exceptions

CCP's Version 23.02 patch notes document an additional 5% increase to manufacturing, ME research, TE research, and invention installation fees in Exordium, the designated starter-space region. Treat that as a location-specific exception and use the in-game job quote when operating there. Do not apply it globally. [^ccp-exordium-fees]

Likewise, treat the 2% ME/TE research SCC surcharge as a temporary exception, not a permanent baseline. The 4% general baseline and 2% research-specific exception must remain separate configuration values until CCP clarifies or changes the policy.

## Live data inputs and reproducibility

A future deterministic fee calculator should accept at minimum:

- Activity type.
- Solar system and current activity SCI.
- Blueprint/type and job runs.
- Base material quantities and adjusted item prices, where that activity uses an EIV calculation.
- Structure family and hull size.
- Applicable structure role bonus.
- Exact fitted rig and its activity/item-group scope.
- Facility owner tax or NPC facility tax.
- SCC surcharge for the activity.
- Alpha-clone status.
- Any location-specific policy such as Exordium.

The ESI overview identifies ESI as CCP's official REST API and provides the API Explorer. Use the current industry systems endpoint for SCI and current adjusted prices for EIV inputs. ESI is versioned; a production integration should record its compatibility date and response retrieval time. [^ccp-esi-overview]

For verification and reproducibility, record the job's Industry UI quote at the same time as the ESI data, including the facility, activity, system, and character clone state. This permits a later comparison between the model and the actual fee.

## Limitations and unresolved questions

- **Temporary SCC relief:** confirm whether the ME/TE research SCC reduction is still 2% on 2026-11-14; CCP described it as temporary. The current document deliberately leaves this as an open verification item.
- **Research/copy/invention value basis:** the exact activity-specific value basis and fee rounding need to be measured against current in-game job quotes.
- **Rig stacking:** cost rigs are activity-specific; their stacking with structure cost bonuses should be validated for representative activity/type combinations.
- **Special regions:** the Exordium +5% installation fee must be preserved as a regional rule rather than baked into a universal tax rate.
- **Rounding:** do not assume a rounding order or precision until confirmed from the displayed job quote and a reproducible set of jobs.

## Related concepts

- [Facilities and Rigs](../01-foundations/facilities-and-rigs.md)
- [Blueprints and Research](../01-foundations/blueprints-and-research.md)
- [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md)
- [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)

[^ccp-viridian-fees]: CCP, Viridian Expansion Notes (2023-06-09), Industry Job Installation Fee.
[^ccp-scc-baseline]: CCP, Patch Notes - Version 21.06 (2024-02-01.1), SCC surcharge change from 1.5% to 4%.
[^ccp-research-scc-relief]: CCP, Exploration and Industry Balance Rework (2025-07-18), Industry Tax Relief - SCC Surcharge Cut.
[^ccp-exordium-fees]: CCP, Patch Notes - Version 23.02, Exordium starter-space industry installation fee changes.
[^ccp-esi-overview]: CCP, EVE Developer Documentation, EVE Swagger Interface (ESI) Overview.
[^eveuni-manufacturing]: EVE University Wiki, Manufacturing.
[^eveuni-research]: EVE University Wiki, Research (last modified 2026-03-21).
[^eveuni-structure-browser]: EVE University Wiki, Upwell structure / Structure Browser.
[^eve-reactions-calculator-method]: EVE Reactions Calculator, methodology.
[^everef-engineering-complexes]: EVE Ref, Engineering Complexes (SDE-derived role attributes).
