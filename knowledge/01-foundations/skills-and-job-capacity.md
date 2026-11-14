---
type: Concept
title: Skills and Job Capacity
description: Character-level manufacturing, science, and reaction job limits, skill prerequisites, remote installation range, and relevant time modifiers.
tags:
  - skills
  - capacity
  - manufacturing
  - science
  - reactions
sources:
  - id: ccp-activities-jobs
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: ccp-manufacturing
    resource: https://support.eveonline.com/hc/en-us/articles/203210292-Manufacturing
    title: Manufacturing | EVE Online Support (updated 2024-08-29)
  - id: ccp-industrialist-academy
    resource: https://www.eveonline.com/eve-academy/careers/industrialist
    title: Industrialist | EVE Academy
  - id: eveuni-production
    resource: https://wiki.eveuniversity.org/Production
    title: Manufacturing | EVE University Wiki (last modified 2025-09-09)
  - id: eveuni-research
    resource: https://wiki.eveuniversity.org/Research
    title: Research | EVE University Wiki (last modified 2026-03-21)
  - id: eveuni-reactions
    resource: https://wiki.eveuniversity.org/Reactions
    title: Reactions | EVE University Wiki (last modified 2025-06-22)
  - id: eveuni-production-skills
    resource: https://wiki.eveuniversity.org/Skills:Production
    title: Skills:Production | EVE University Wiki (last modified 2025-09-09)
  - id: eveuni-science-skills
    resource: https://wiki.eveuniversity.org/Skills:Science
    title: Skills:Science | EVE University Wiki (last modified 2024-06-28)
  - id: eveuni-resource-skills
    resource: https://wiki.eveuniversity.org/Skills:Resource_Processing
    title: Skills:Resource Processing | EVE University Wiki (last modified 2026-01-27)
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:12:17Z
status: draft
---

## Summary

Industrial job capacity is a character-level limit on how many jobs of a given type the character can have active at once. EVE classifies work into three job types: **Manufacturing**, **Science**, and **Reaction**. Each type has its own skill-defined slot budget. Manufacturing and Science jobs do not consume each other's available slots; Reaction is listed as a separate job type with its own slot skills. [^ccp-activities-jobs]

Each pool starts with one job slot. Two skills add one slot per level to that pool, producing a maximum of 11 Manufacturing, 11 Science, and 11 Reaction jobs per character when the relevant skills are all trained to V. The combined nominal capacity is therefore 33 concurrent jobs across the three pools. [^eveuni-production] [^eveuni-research] [^eveuni-reactions]

These are character job limits, not a count of physical factory slots at a facility. CCP states that facilities offering manufacturing have no time restriction or limit on the number of Manufacturing jobs that can be installed there; the character's skills, location, blueprint, materials, and facility service are separate constraints. [^ccp-manufacturing]

## Job categories and slot formulas

| Job type | Activities | Slot formula | Maximum |
|---|---|---|---:|
| Manufacturing | Manufacturing jobs | 1 + Mass Production level + Advanced Mass Production level | 11 |
| Science | ME research, TE research, copying, invention | 1 + Laboratory Operation level + Advanced Laboratory Operation level | 11 |
| Reaction | Reaction jobs | 1 + Mass Reactions level + Advanced Mass Reactions level | 11 |

Each slot skill contributes one additional simultaneous job per skill level. The advanced slot skill requires the basic slot skill at V. Therefore, the formula assumes a character can train both component skills to their stated levels. [^ccp-activities-jobs] [^eveuni-production] [^eveuni-research] [^eveuni-reactions]

**Example capacity calculations**

- Manufacturing: Mass Production V and Advanced Mass Production IV = 1 + 5 + 4 = **10 jobs**.
- Science: Laboratory Operation V and Advanced Laboratory Operation III = 1 + 5 + 3 = **9 jobs**.
- Reactions: Mass Reactions V and Advanced Mass Reactions V = 1 + 5 + 5 = **11 jobs**.

A character with all six slot skills at V has a nominal total capacity of 33 concurrent jobs, distributed as 11 per job type. This total is a sum of the three separately listed job pools, not a separate character skill.

## Manufacturing capacity

### Slot skills

| Skill | Slot effect | Prerequisite | Alpha access |
|---|---|---|---|
| Mass Production | +1 Manufacturing job per level, up to +5 | Industry III | Trainable to III |
| Advanced Mass Production | +1 Manufacturing job per level, up to +5 | Mass Production V | Not trainable by Alpha |

Mass Production V provides six total Manufacturing slots when counting the base slot. Advanced Mass Production then increases the maximum to 11. Advanced Mass Production IV gives 10 total slots. [^eveuni-production-skills]

### Remote job installation

**Supply Chain Management** allows the character to start Manufacturing jobs outside the current solar system. Without it, Manufacturing jobs can be started only in the character's current solar system. Each skill level adds five jumps of range, up to 25 jumps at V. CCP explicitly notes that this range is not limited to a single region. [^ccp-manufacturing] [^eveuni-production-skills]

Prerequisites listed by EVE University are Industry III and Mass Production IV. Supply Chain Management is not trainable by Alpha characters. [^eveuni-production-skills]

The remote-start skill does not move materials or blueprints. CCP requires the blueprint and the materials needed for the job to be available at the destination location, and the destination facility must offer the Manufacturing service. [^ccp-manufacturing]

## Science capacity

### Included activities

CCP assigns the following activities to the Science job type:

- Material Efficiency research.
- Time Efficiency research.
- Blueprint copying.
- Invention.

They share the character's Science job pool rather than receiving separate pools for each activity. [^ccp-activities-jobs]

### Slot skills

| Skill | Slot effect | Prerequisite | Alpha access |
|---|---|---|---|
| Laboratory Operation | +1 Science job per level, up to +5 | Science III | Not trainable by Alpha |
| Advanced Laboratory Operation | +1 Science job per level, up to +5 | Laboratory Operation V | Not trainable by Alpha |

The base slot plus Laboratory Operation V permits six simultaneous Science jobs. Advanced Laboratory Operation can raise the pool to 11. [^eveuni-research] [^eveuni-science-skills]

### Remote job installation

**Scientific Networking** allows Science jobs to be started outside the character's current solar system. Without it, the character can start research jobs only within the current solar system. Each level adds five jumps of range, up to 25 jumps at V. Laboratory Operation IV is the listed prerequisite. The skill is not trainable by Alpha characters. [^eveuni-research] [^eveuni-science-skills]

This is a job-starting range skill. It does not transport the blueprint, research materials, or other required inputs to the destination.

## Reaction capacity

### Slot skills

| Skill | Slot effect | Prerequisite | Alpha access |
|---|---|---|---|
| Mass Reactions | +1 Reaction job per level, up to +5 | Reactions III | Not trainable by Alpha |
| Advanced Mass Reactions | +1 Reaction job per level, up to +5 | Reactions III and Mass Reactions V | Not trainable by Alpha |

The base slot plus Mass Reactions V permits six concurrent Reaction jobs. Advanced Mass Reactions increases the pool to 11. [^eveuni-reactions] [^eveuni-resource-skills]

### Remote job installation

**Remote Reactions** allows reaction jobs to be started and completed remotely. Each level adds five jumps of range, to a maximum of 25 jumps at V. Its listed prerequisite is Reactions IV, and it is not trainable by Alpha characters. [^eveuni-reactions] [^eveuni-resource-skills]

### Reaction time modifier

The separate **Reactions** skill reduces reaction time by 4% per skill level. Reactions III is required to train Mass Reactions; Reactions IV is required for Remote Reactions. The Reactions skill itself does not add job slots. [^eveuni-reactions] [^eveuni-resource-skills]

## Skills that change job duration, not slot count

Do not confuse job-slot skills with skills that make a particular job faster. The following skills affect job duration but do not increase the number of simultaneous jobs in the formulas above.

| Skill | Documented effect | Job type |
|---|---|---|
| Industry | 4% reduction in Manufacturing time per level | Manufacturing |
| Advanced Industry | 3% reduction in Manufacturing and research time per level | Manufacturing and Science |
| Science | 5% reduction in blueprint-copying time per level | Copying |
| Research | 5% reduction in Time Efficiency research time per level | TE research |
| Metallurgy | 5% reduction in Material Efficiency research time per level | ME research |
| Reactions | 4% reduction in reaction time per level | Reaction |

The Advanced Industry skill requires Industry III. Research requires Science III, and Metallurgy requires Science IV. The cited skill references document these percentage effects; combined modifier stacking is deliberately not calculated here because the complete job-time model also needs to account for activity-specific, facility, rig, implant, and other applicable modifiers. [^eveuni-production-skills] [^eveuni-research] [^eveuni-science-skills] [^eveuni-resource-skills]

## Alpha and Omega capacity notes

The skill tables cited above list these Alpha training limits:

- **Manufacturing:** Mass Production can be trained to III, while Advanced Mass Production and Supply Chain Management are not trainable by Alpha. The corresponding slot maximum is therefore four Manufacturing jobs.
- **Science:** Laboratory Operation and Advanced Laboratory Operation are not trainable by Alpha. The slot budget remains the base one Science job.
- **Reaction:** Mass Reactions and Advanced Mass Reactions are not trainable by Alpha. The slot budget remains the base one Reaction job.

These Alpha totals are derived from the listed skill access limits and the slot formulas, not from a separate CCP-published Alpha job-slot table. Treat them as secondary-source-derived values and confirm the character's actual skill eligibility in game before using them in a plan. [^eveuni-production-skills] [^eveuni-science-skills] [^eveuni-resource-skills]

Omega characters can train the advanced slot skills, subject to their prerequisites, to reach 11 jobs in each category.

## Important distinctions and common modeling errors

1. **Slots are not output.** A job can contain multiple production runs. Job count measures concurrent jobs, not units produced or ISK earned.
2. **Job pools are activity-specific.** ME research, TE research, copying, and invention all consume Science capacity; they do not each have their own separate slot cap.
3. **Facility capacity is not character capacity.** Do not interpret job slot skills as increasing the number of jobs a structure can accept.
4. **Remote-start skills do not haul assets.** Required blueprints and inputs must already be at the correct location.
5. **A slot skill is not a time skill.** Mass Production adds slots; Industry and Advanced Industry reduce manufacturing time.
6. **Research Project Management is unrelated to the Science job-slot formula.** It increases the number of R&D agents a character can use, not the character's number of Industry Science jobs. [^eveuni-science-skills]
7. **A BPO can be a separate bottleneck.** EVE University notes that one BPO can be used for only one active Manufacturing job at a time; copying it into multiple BPCs can allow parallel manufacturing jobs, provided the character also has available slots and sufficient materials. [^eveuni-research]

## Formulas for later throughput models

Let:

- (M) = Mass Production skill level.
- (AM) = Advanced Mass Production skill level.
- (L) = Laboratory Operation skill level.
- (AL) = Advanced Laboratory Operation skill level.
- (R) = Mass Reactions skill level.
- (AR) = Advanced Mass Reactions skill level.

Then:

```text
Manufacturing slots = 1 + M + AM
Science slots       = 1 + L + AL
Reaction slots      = 1 + R + AR
```

Each skill level is bounded by its in-game maximum of V. The advanced skill cannot be trained until the base slot skill reaches V. For a character with a valid skill plan, the sum of all three pools is:

```text
Total industry job capacity
  = Manufacturing slots + Science slots + Reaction slots
```

At all six slot skills V, the theoretical total is 33. The formulas describe maximum simultaneous job counts; they do not incorporate job duration, number of runs per job, material availability, facility availability, or capital constraints.

## Research limitations and verification tasks

- CCP's official job-type and Manufacturing support articles were last updated in August 2024. They are the primary source for the activity/job-type mapping and Manufacturing remote-start conditions, but not a current detailed skill database.
- EVE University's skill-reference pages have different last-modified dates: Manufacturing skills (2025-09-09), Research (2026-03-21), Reactions (2025-06-22), Science skills (2024-06-28), and Resource Processing skills (2026-01-27). Where a skill detail is not stated in CCP support, it is attributed to these secondary references.
- No independently recorded in-game test has yet been performed for the slot formulas, Alpha limits, or remote-start ranges.
- Facility eligibility and job prerequisites remain activity- and structure-specific. The relevant structure/service documentation belongs in [Facilities and Rigs](facilities-and-rigs.md).

## Sources and notes

CCP's EVE Academy page provides a high-level official introduction to industrial support skills. The detailed per-level bonuses, skill prerequisites, jump ranges, and Alpha training limits in this document rely on the EVE University skill-reference pages where CCP's support page does not enumerate them. Recheck exact skill information against the in-game skill browser when applying the document to a character plan.

[^ccp-activities-jobs]: CCP Support, Activities and Job Types (updated 2024-08-29).
[^ccp-manufacturing]: CCP Support, Manufacturing (updated 2024-08-29).
[^ccp-industrialist-academy]: CCP, EVE Academy: Industrialist.
[^eveuni-production]: EVE University Wiki, Manufacturing (last modified 2025-09-09).
[^eveuni-research]: EVE University Wiki, Research (last modified 2026-03-21).
[^eveuni-reactions]: EVE University Wiki, Reactions (last modified 2025-06-22).
[^eveuni-production-skills]: EVE University Wiki, Skills:Production (last modified 2025-09-09).
[^eveuni-science-skills]: EVE University Wiki, Skills:Science (last modified 2024-06-28).
[^eveuni-resource-skills]: EVE University Wiki, Skills:Resource Processing (last modified 2026-01-27).
