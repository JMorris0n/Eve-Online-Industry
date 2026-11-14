---
type: Concept
title: Tech II Invention
description: Tech II invention inputs, success probability, required skills, datacores, decryptors, output BPCs, job economics, and production dependencies.
tags:
  - invention
  - tech-ii
  - science
  - datacores
  - decryptors
sources:
  - id: ccp-invention
    resource: https://support.eveonline.com/hc/en-us/articles/203210642-Invention
    title: Invention | EVE Online Support (updated 2024-08-29)
  - id: ccp-decryptors
    resource: https://support.eveonline.com/hc/en-us/articles/203270631-Decryptors
    title: Decryptors | EVE Online Support (updated 2024-08-29)
  - id: ccp-datacores
    resource: https://support.eveonline.com/hc/en-us/articles/203210652-Datacores
    title: Datacores | EVE Online Support (updated 2024-08-29)
  - id: ccp-blueprints
    resource: https://support.eveonline.com/hc/en-us/articles/203269951-Blueprints
    title: Blueprints | EVE Online Support (updated 2024-08-29)
  - id: ccp-activities-jobs
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: ccp-industry-ui
    resource: https://support.eveonline.com/hc/en-us/articles/203270121-Industry-User-Interface
    title: Industry User Interface | EVE Online Support (updated 2024-08-29)
  - id: ccp-phoebe-invention
    resource: https://www.eveonline.com/news/view/patch-notes-for-phoebe
    title: Patch Notes for Phoebe | EVE Online (historical invention formula change)
  - id: eveuni-invention
    resource: https://wiki.eveuniversity.org/Invention
    title: Invention | EVE University Wiki (last modified 2026-10-09)
  - id: eveuni-datacores
    resource: https://wiki.eveuniversity.org/Datacores
    title: Datacores | EVE University Wiki
  - id: eveuni-production-skills
    resource: https://wiki.eveuniversity.org/Skills:Production
    title: Skills:Production | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:25:24Z
status: draft
---

## Summary

Tech II invention converts an eligible Tech I blueprint copy (BPC) into a chance at receiving a limited-run Tech II BPC. The process is probabilistic: the job can fail and produce no output blueprint. A successful job returns a Tech II BPC whose base licensed runs, Material Efficiency (ME), and Time Efficiency (TE) can be modified by an optional decryptor. [^ccp-invention] [^ccp-decryptors]

Invention is a **Science** job type. It shares the character's Science job pool with ME research, TE research, and copying. It does not consume a separate invention-only job pool. [^ccp-activities-jobs]

The input BPC's own ME, TE, and remaining licensed runs do not improve the resulting invention chance or the base quality of the output. One licensed run from the input BPC is consumed for each invention run, whether the attempt succeeds or fails. Datacores and any selected decryptor are also consumed regardless of success. [^ccp-invention] [^eveuni-invention]

## Tech II invention workflow

The normal Tech II invention sequence is:

1. Identify a Tech I item that has an inventible Tech II variant.
2. Obtain a BPC of the corresponding Tech I blueprint.
3. Check the BPC's Invention activity for its required skills and datacores.
4. Obtain the correct datacores and decide whether a decryptor is economically justified.
5. Choose a facility that offers the Invention service and install the job.
6. Select the desired Tech II output when the input blueprint can produce more than one Tech II variant.
7. Review the displayed invention chance, output blueprint details, job duration, inputs, and installation fee.
8. Install the desired number of invention runs.
9. Deliver the completed job and inspect the success/failure result and any resulting Tech II BPC.

CCP documents this general workflow and states that some Tech I BPCs can produce more than one possible Tech II output. The desired result must be selected in the Industry UI before installing the job. [^ccp-invention] [^ccp-industry-ui]

## Required inputs

### Tech I blueprint copy

Tech II invention requires a BPC of the matching Tech I item. A BPO cannot be used directly for the invention activity. Each invention run consumes one licensed run from the input BPC regardless of success. If the input BPC has only one run remaining, it is consumed by the attempt. [^ccp-invention] [^ccp-blueprints]

The input BPC's ME and TE levels do not affect the invention success chance or the baseline quality of the output. Its remaining runs determine how many invention attempts can be installed from that copy. [^eveuni-invention]

### Datacores

Datacores are mandatory invention inputs. A job normally requires datacores from two different fields, with the exact types and quantities displayed in the blueprint's Invention tab and in the Industry job setup. The fields correspond to the science skills required for the item. [^ccp-datacores] [^ccp-invention]

CCP documents these acquisition channels:

- Factional Warfare militia Loyalty Point stores.
- Research and Development agents, provided the character has the relevant research relationship and field skill.
- Hacking containers in Data Sites.

R&D agents provide datacores in exchange for Research Points and ISK. The exact cost and quantity required for an invention attempt should be read from the current blueprint and job setup rather than inferred from another product. [^ccp-datacores]

Datacores are consumed regardless of invention success. They are therefore part of every attempt's economic cost, not only successful outputs. [^ccp-invention]

### Decryptors

Decryptors are optional invention inputs. They modify:
- The invention success probability.
- The resulting Tech II BPC's licensed-run modifier.
- The resulting Tech II BPC's ME modifier.
- The resulting Tech II BPC's TE modifier.

A decryptor is consumed with the invention job regardless of success. The eight currently documented variants and their effects are listed below. [^ccp-decryptors]

## Decryptor effects

CCP's decryptor table specifies the probability multiplier, maximum-run modifier, ME modifier, and PE (time-efficiency) modifier. The probability column's parenthetical multiplier is the factor applied to the skill-adjusted base chance.

| Decryptor | Probability factor | Output run modifier | ME modifier | TE / PE modifier |
|---|---:|---:|---:|---:|
| Augmentation | 0.6 | +9 | -2 | +2 |
| Optimized Augmentation | 0.9 | +7 | +2 | 0 |
| Symmetry | 1.0 | +2 | +1 | +8 |
| Process | 1.1 | 0 | +3 | +6 |
| Accelerant | 1.2 | +1 | +2 | +10 |
| Parity | 1.5 | +3 | +1 | -2 |
| Attainment | 1.8 | +4 | -1 | +4 |
| Optimized Attainment | 1.9 | +2 | +1 | -2 |

The decryptor is a trade-off, not a universal upgrade. Some improve probability at the cost of fewer output runs or lower ME/TE; others add many runs but reduce the success multiplier. The appropriate option depends on the output's value, the required number of Tech II manufacturing runs, material intensity, and the cost of the decryptor. [^ccp-decryptors]

### Base output BPC

EVE University documents the following baseline for successful Tech II invention without a decryptor:

- Most Tech II items produce a 10-run BPC.
- Tech II ships and rigs produce a 1-run BPC.
- The resulting BPC is described as ME 2% and TE 4%.
- The output BPC cannot be researched or copied; it is used for manufacturing.

The selected decryptor's run, ME, and TE modifiers change these baseline output values. Because the CCP decryptor support article lists modifier values but does not restate every item's baseline output, use the specific blueprint preview in the Industry UI as the final check for a given output. [^eveuni-invention] [^ccp-decryptors] [^ccp-industry-ui]

## Required skills

The exact required skills are item-specific and are displayed in the input BPC's Invention tab. In general, the character needs:

- The racial Encryption Methods skill associated with the item's technology/faction.
- The two advanced Science skills associated with the datacore fields used by the invention.
- Other prerequisite support skills shown by the actual blueprint, commonly including Mechanics V, Power Grid Management V, and CPU Management V for many Tech II invention jobs.

Higher levels in the required Encryption Methods and Science skills increase invention probability. They do not reduce material requirements or directly improve the output BPC's ME/TE; those output characteristics are determined by the base output and decryptor. [^eveuni-invention]

Invention job count is controlled by Laboratory Operation and Advanced Laboratory Operation. Invention shares the Science pool with copying and blueprint research. Advanced Industry and eligible facility bonuses can reduce science-job time; see [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md) and [Facilities and Rigs](../01-foundations/facilities-and-rigs.md). [^ccp-activities-jobs] [^eveuni-production-skills]

## Success probability

CCP's historical Phoebe patch notes document the current structure of the skill modifier and the change to the base invention chance categories. EVE University's October 2026 invention reference reproduces the formula and current base chance table. [^ccp-phoebe-invention] [^eveuni-invention]

Let:

- (B) = base invention chance for the item category, expressed as a decimal.
- (S_1) = first required Science skill level.
- (S_2) = second required Science skill level.
- (E) = required racial Encryption Methods skill level.
- (D) = decryptor probability multiplier; use 1.0 if no decryptor is used.

Then the documented formula is:

```text
Skill modifier = 1 + (S1 + S2) / 30 + E / 40

Invention chance
  = Base chance × Skill modifier × Decryptor probability multiplier
```

### Base probability categories

| Tech II product category | Base chance |
|---|---:|
| Modules, rigs, and ammunition | 34% |
| Frigates and destroyers | 30% |
| Cruisers, battlecruisers, mining barges, and haulers | 26% |
| Battleships | 22% |
| Freighters | 18% |

These category values are reproduced from the current EVE University invention page and correspond to the historical CCP Phoebe adjustment. The table is for Tech II invention categories; the same article also gives different base chances for Tech III relic types, which are outside this document's Tech II scope. [^ccp-phoebe-invention] [^eveuni-invention]

### Worked probability example

Assume a module has a 34% base chance, the character has both required Science skills at IV, the corresponding Encryption Methods skill at III, and no decryptor.

```text
Skill modifier
  = 1 + (4 + 4) / 30 + 3 / 40
  = 1.3416667

Invention chance
  = 0.34 × 1.3416667 × 1.0
  = 0.4561667
  = 45.6167%
```

This is a formula example, not a live UI quote. For a real job, compare the formula's result with the chance displayed by the Industry UI. Do not add a Tech I meta-item bonus: CCP's Phoebe notes state that meta items can no longer be used for invention. [^ccp-phoebe-invention] [^ccp-invention]

## Expected cost and output economics

Invention is probabilistic, so the correct unit economics are based on expected successful outputs, not on the cost of a single attempt.

For one attempt, define:

- (C_{BPC}) = economic value of the one licensed run consumed from the Tech I BPC.
- (C_{DC}) = cost of the datacores consumed.
- (C_D) = decryptor cost, or zero if none is selected.
- (C_F) = invention installation fee.
- (C_O) = other attempt-level costs.

Then:

```text
Cost per attempt = C_BPC + C_DC + C_D + C_F + C_O

Expected attempts per successful output = 1 / p

Expected cost per successful output BPC
  = Cost per attempt / p
```

Here (p) is the success probability expressed as a decimal between 0 and 1. This expected-value equation assumes repeated attempts have independent outcomes and the same probability and cost. The per-attempt allocation must use the actual number of datacores and decryptors consumed by the selected multi-run job; do not assume the optional-item quantity scales one-for-one with invention runs until confirmed in the live Industry UI. Use the live chance and job quote when populating the model.

If the successful output BPC has (R_{out}) licensed manufacturing runs:

```text
Expected invention cost per output run
  = Expected cost per successful output BPC / R_out
```

This is only the invention component of Tech II unit cost. The completed Tech II manufacturing chain must add the required Tech II components, minerals, other inputs, Manufacturing job installation fees, logistics, and selling costs. See [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md) and [Tech II Components](tech-2-components.md).

### Decryptor selection decision

Do not choose a decryptor solely because it produces the highest displayed probability or the most output runs. Compare the expected cost per usable Tech II manufacturing run after considering:

- Decryptor purchase cost.
- Change in invention probability.
- Change in resulting BPC licensed runs.
- Change in ME and TE of the resulting BPC.
- Value and time cost of the Tech I BPC run consumed per attempt.
- Datacore cost and invention installation fee.
- Whether the increased output runs match actual production demand and manufacturing capacity.

A decryptor with fewer output runs may still produce the best expected cost if it raises success probability substantially. A decryptor that adds many output runs may lower invention cost per manufacturing run but may create inventory that is slow to sell.

## Invention job installation and result

Invention is a Science activity. The job uses the same Science job slot pool as ME research, TE research, and copying. The selected facility must offer the Invention activity, and the required inputs must be available in the chosen input location. Engineering Complex service modules, role bonuses, and invention-specific rigs can affect job duration and installation costs; the relevant facility rules are in [Facilities and Rigs](../01-foundations/facilities-and-rigs.md). [^ccp-invention] [^ccp-activities-jobs]

The Industry UI displays the success chance and allows optional decryptor selection. When the selected Tech I item can produce multiple Tech II products, choose the intended outcome before starting the job. The final success/failure state and the resulting blueprint are inspected after job delivery. [^ccp-invention] [^ccp-industry-ui]

## Important distinctions and common errors

1. **One invention run is one attempt.** It consumes one run from the input Tech I BPC even if the attempt fails.
2. **Failure still costs materials.** Datacores and any selected decryptor are consumed regardless of success.
3. **Input ME/TE do not carry through.** The input Tech I BPC's ME, TE, and remaining runs do not change the base invented output.
4. **Decryptor probability is a multiplier.** For example, a +50% probability decryptor uses a 1.5 factor, not an additional 50 percentage points.
5. **Decryptors also change output quality and run count.** Probability alone does not describe the economic result.
6. **The output run count is product-dependent.** Most invented Tech II BPCs have 10 runs before decryptor modifiers; ships and rigs start at one.
7. **Invention is not manufacturing.** A successful attempt creates a Tech II BPC. A separate Manufacturing job is required to produce the finished item.
8. **Tech II BPCs are not researchable.** Their efficiency values are fixed by the invention result and decryptor modifier.

## Boundaries and unresolved details

This document covers ordinary Tech II invention. It does not yet cover Tech III reverse engineering, ancient relic condition categories, full Tech II production chains, item-specific skill matrices, or a live market-driven decryptor optimizer.

The following need further verification before a deterministic invention calculator is treated as production-ready:

- Exact probability display precision and any cap/rounding behavior when the calculated probability approaches or exceeds 100%.
- Exact datacore and decryptor quantities consumed for a multi-run invention job.
- Item-specific skill requirements and base chance categories for newer or unusual Tech II products.
- The exact output BPC runs/ME/TE shown in the current Industry UI for every decryptor/product family.
- Invention job duration, installation fee, and structure/rig stacking against live quotes.

## Related concepts

- [Blueprints and Research](../01-foundations/blueprints-and-research.md)
- [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md)
- [Facilities and Rigs](../01-foundations/facilities-and-rigs.md)
- [Tech I Manufacturing](tech-1-manufacturing.md)
- [Tech II Components](tech-2-components.md)
- [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)

[^ccp-invention]: CCP Support, Invention (updated 2024-08-29).
[^ccp-decryptors]: CCP Support, Decryptors (updated 2024-08-29).
[^ccp-datacores]: CCP Support, Datacores (updated 2024-08-29).
[^ccp-blueprints]: CCP Support, Blueprints (updated 2024-08-29).
[^ccp-activities-jobs]: CCP Support, Activities and Job Types (updated 2024-08-29).
[^ccp-industry-ui]: CCP Support, Industry User Interface (updated 2024-08-29).
[^ccp-phoebe-invention]: CCP, Patch Notes for Phoebe (invention formula, base chances, multiple-run invention jobs, and removal of meta-item invention bonuses).
[^eveuni-invention]: EVE University Wiki, Invention (last modified 2026-10-09).
[^eveuni-datacores]: EVE University Wiki, Datacores.
[^eveuni-production-skills]: EVE University Wiki, Skills:Production.
