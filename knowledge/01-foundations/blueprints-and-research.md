---
type: Concept
title: Blueprints and Research
description: Blueprint originals, blueprint copies, ME and TE research, copying behavior, and blueprint acquisition paths.
tags:
  - blueprints
  - research
  - manufacturing
sources:
  - id: ccp-blueprints
    resource: https://support.eveonline.com/hc/en-us/articles/203269951-Blueprints
    title: Blueprints | EVE Online Support (updated 2024-08-29)
  - id: ccp-me-research
    resource: https://support.eveonline.com/hc/en-us/articles/203210542-Material-Efficiency-Research
    title: Material Efficiency Research | EVE Online Support (updated 2024-07-15)
  - id: ccp-te-research
    resource: https://support.eveonline.com/hc/en-us/articles/203210512-Time-Efficiency-Research
    title: Time Efficiency Research | EVE Online Support (updated 2024-07-15)
  - id: ccp-copying
    resource: https://support.eveonline.com/hc/en-us/articles/203210602-Copying
    title: Copying | EVE Online Support (updated 2024-07-15)
  - id: ccp-activities
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: ccp-fractured-skies
    resource: https://www.eveonline.com/news/view/fractured-skies-expansion-notes
    title: Fractured Skies Expansion Notes | EVE Online (2026-11-06)
generated:
  by: process:starter-scaffold
  at: 2026-11-14T06:04:20Z
status: draft
---

## Summary

Blueprints define most player manufacturing and several other industry activities. The main distinction is between a **Blueprint Original (BPO)**, which can be researched and copied, and a **Blueprint Copy (BPC)**, which has a finite number of licensed production runs and carries the efficiency values it had when copied. Material Efficiency (ME) reduces job material requirements; Time Efficiency (TE) reduces manufacturing job duration. These are separate effects and should be modeled independently. [^ccp-blueprints] [^ccp-me-research] [^ccp-te-research]

This document records CCP's published rules and their directly derived formulas. It does not yet model character skills, facility/rig bonuses, installation fees, or the complete economic value of researching a particular BPO.

## Blueprint types and purpose

CCP's industry documentation distinguishes these blueprint-related objects and activities: [^ccp-blueprints]

| Object | Manufacturing | Research/copying | Invention/reaction role |
|---|---|---|---|
| Blueprint Original (BPO) | Unlimited licensed production runs | Can receive ME and TE research; can be copied | A Tech I BPO can be copied to produce a BPC that may be used for Tech II invention |
| Blueprint Copy (BPC) | Limited licensed production runs | Cannot be researched further or copied as an original | Tech I BPCs are used for Tech II invention; invented Tech II BPCs are used for Tech II manufacturing |
| Ancient relic | Not a manufacturing blueprint | Not researched or copied as a BPO | Used for invention of Tech III ship and subsystem BPCs |
| Reaction formula | Not a manufacturing blueprint | Not ME/TE researched or copied as a BPO | Used to install reaction jobs |

Not every player-produced item is blueprint-based. CCP explicitly identifies Planetary Interaction as an example of an activity that produces items without a corresponding blueprint. [^ccp-blueprints]

### Availability and acquisition

CCP's support article states that most Tech I BPOs are available through market sell orders, existing Tech II BPOs remain with their current owners with no new Tech II BPOs planned, and no Tech III BPOs are available. It lists copying, loot drops, and invention among BPC acquisition routes. [^ccp-blueprints]

Do not treat that list as exhaustive for every item. CCP's November 2026 *Fractured Skies* expansion notes specifically state that BPCs for the four new Navy attack battlecruisers can be purchased from their respective faction Loyalty Point stores. Blueprint acquisition therefore needs to be checked for the particular item and source, rather than inferred from the general taxonomy. [^ccp-fractured-skies]

## Material Efficiency research

ME research is performed on BPOs only. A BPO can receive 10 ME research steps. Each step reduces the required materials by 1%, giving a maximum blueprint ME reduction of 10%. Research steps take progressively longer; CCP describes ME research time as increasing exponentially with each subsequent level. [^ccp-me-research]

### ME calculation

For the ME effect alone:

```text
ME factor = 1 - (0.01 × ME research steps)

Job materials before rounding
  = blueprint material requirement for the selected job
    × ME factor
```

The blueprint material requirement in this expression is the requirement for the **entire job**, including its selected number of runs. ME is applied to the job total, not independently to each run. [^ccp-me-research]

**Example**

Assume the blueprint requires 10 units of a material per run and the job is set to 20 runs:

- Unresearched job requirement: 10 × 20 = 200 units.
- At 6 ME research steps: 200 × (1 - 0.06) = 188 units.
- ME saving: 12 units.

This isolates the ME effect. Other applicable industry modifiers are outside the scope of this calculation.

### Rounding and minimum requirements

CCP states that calculated material quantities are rounded up. Its example is 14.4 units of Tritanium becoming 15 units for the job. Because rounding is applied after the job total is calculated, a small job may show no material saving even when the blueprint has ME research. [^ccp-me-research]

CCP also states that a material required as a whole, single item per production run is not reduced by ME. Its example is a Tech I hull consumed as an input to a Tech II ship: producing 10 Paladins still requires 10 Apocalypse hulls, regardless of ME bonuses. Do not assume every material line can be reduced below its per-run single-item requirement. [^ccp-me-research]

## Time Efficiency research

TE research is performed on BPOs only. A BPO can receive 10 TE research steps. Each step reduces manufacturing time by 2%, giving a maximum blueprint TE reduction of 20%. Each subsequent TE research step takes longer than the previous one. [^ccp-te-research]

### TE calculation

For the TE effect alone:

```text
TE factor = 1 - (0.02 × TE research steps)

Job time
  = blueprint manufacturing run time
    × number of production runs
    × TE factor
```

CCP specifies that the TE reduction is applied to the whole manufacturing job, not separately to each run. [^ccp-te-research]

**Example**

Assume the blueprint's manufacturing run time is 1,200 seconds and the job is set to 10 runs:

- Unresearched job time: 1,200 × 10 = 12,000 seconds.
- At 5 TE research steps: 12,000 × (1 - 0.10) = 10,800 seconds.
- Time saved: 1,200 seconds (20 minutes).

This isolates the TE effect. Other applicable skill, facility, or rig time modifiers are not modeled here.

## Research inputs

Most ME and TE research jobs on Tech I BPOs do not require additional materials or trained skills solely to perform the research. CCP notes exceptions, usually involving Tech II BPOs and the Prototype Cloaking Device BPO. Those jobs can require Reports, R.Db materials, and relevant skills. Check the actual blueprint's Bill of Materials and the Industry window rather than assuming every research job is material-free. [^ccp-me-research] [^ccp-te-research]

## Copying behavior

Copying creates one or more BPCs from a BPO. Each produced copy receives the BPO's ME and TE values **at the time the copy is made**. Research performed on the BPO afterward does not retroactively change copies that already exist. BPCs cannot be researched further. [^ccp-copying]

A BPC has a finite number of licensed production runs. When its final licensed run is consumed, it is not returned at job delivery and is destroyed. [^ccp-copying]

The copy-job interface has two distinct quantities: [^ccp-copying]

- **Job Runs:** the number of BPCs to create.
- **Runs per Copy:** the number of licensed production runs assigned to each created BPC, subject to the maximum listed for the BPO's Copy activity.

If a copy job requires input materials, CCP states that those inputs vary with the number of copies produced, not with the licensed production runs assigned to each copy. Copy-job duration is based on the total licensed production runs across all copies. [^ccp-copying]

## Industry job categories

CCP groups manufacturing, science, and reaction activities into distinct job types. Manufacturing includes manufacturing; science includes ME research, TE research, copying, and invention; reaction is its own job type. Manufacturing jobs do not compete with science jobs for their respective job availability. The relevant character skills determine how many jobs can be run in parallel. The exact skill limits and remote-management rules are documented separately in [Skills and Job Capacity](/01-foundations/skills-and-job-capacity.md). [^ccp-activities]

## Practical implications

1. **Research the original, then copy it.** An improved BPO produces improved future copies. Existing BPCs retain the values they had when copied.
2. **Do not value ME only by its percentage.** Material rounding can erase a small nominal saving on short jobs, and single-item-per-run inputs are not reduced.
3. **Value TE as a throughput effect.** TE reduces the time of the whole manufacturing job; its economic value depends on whether saved job time can be used productively.
4. **Treat BPC acquisition as item-specific.** Copies can come from several routes, including copying, invention, loot, and specific LP-store offers.
5. **Keep ME and TE separate.** One changes material requirements; the other changes manufacturing duration. They have different economic consequences.

## Boundaries and unresolved details

This concept intentionally does not yet calculate:

- Character skill modifiers to manufacturing material or time.
- Facility, structure, rig, security-space, or system effects.
- Industry installation fees, SCC surcharges, or activity cost indices.
- Blueprint research job duration by blueprint rank.
- Whether the next ME or TE step is economically worthwhile for a particular production plan.
- Item-specific exceptions outside the CCP pages cited here.

These belong in [Skills and Job Capacity](/01-foundations/skills-and-job-capacity.md), [Facilities and Rigs](/01-foundations/facilities-and-rigs.md), [Installation Costs](/01-foundations/installation-costs.md), and the industrial economics and optimization concepts.

## Sources and notes

- CCP's support articles are the primary source for the rules summarized here. Their displayed update dates are July and August 2024, so the article age is recorded rather than hidden.
- CCP's *Fractured Skies* expansion notes are a newer, item-specific example of LP-store BPC acquisition, published 2026-11-06.
- The research status remains **draft**. The calculations are direct algebraic translations of CCP's stated percentage effects; they have not been independently tested in-game.

[^ccp-blueprints]: Blueprints | EVE Online Support (updated 2024-08-29)
[^ccp-me-research]: Material Efficiency Research | EVE Online Support (updated 2024-07-15)
[^ccp-te-research]: Time Efficiency Research | EVE Online Support (updated 2024-07-15)
[^ccp-copying]: Copying | EVE Online Support (updated 2024-07-15)
[^ccp-activities]: Activities and Job Types | EVE Online Support (updated 2024-08-29)
[^ccp-fractured-skies]: Fractured Skies Expansion Notes | EVE Online (2026-11-06)
