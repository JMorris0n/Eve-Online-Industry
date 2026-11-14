---
type: Concept
title: Character Specialization
description: Industrial role design, skill priorities, marginal skill value, and allocation of job capacity across characters.
tags:
  - optimization
  - characters
  - skills
sources:
  - id: ccp-activities-jobs
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: eveuni-production-skills
    resource: https://wiki.eveuniversity.org/Skills:Production
    title: Skills:Production | EVE University Wiki (last modified 2025-09-09)
  - id: eveuni-science-skills
    resource: https://wiki.eveuniversity.org/Skills:Science
    title: Skills:Science | EVE University Wiki
  - id: eveuni-resource-skills
    resource: https://wiki.eveuniversity.org/Skills:Resource_Processing
    title: Skills: Resource Processing | EVE University Wiki
  - id: eveuni-trade-skills
    resource: https://wiki.eveuniversity.org/Skills:Trade
    title: Skills:Trade | EVE University Wiki
  - id: eveuni-planet-management
    resource: https://wiki.eveuniversity.org/Command_Center_Upgrades
    title: Skills:Planet Management | EVE University Wiki
  - id: eveuni-invention
    resource: https://wiki.eveuniversity.org/Invention
    title: Invention | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T08:10:00Z
status: draft
---

## Purpose

Character specialization assigns training and job capacity to the industrial activities that create the most value for an operation. The objective is not to train every industrial skill to V by default. It is to train the skills that remove the current bottleneck or improve the economics of the character's actual production plan.

Each character has independent Manufacturing, Science, and Reaction job pools. Skills, assets, and access determine how effectively those pools can be used. [^ccp-activities-jobs]

## Role profiles

These profiles are templates for planning, not mandatory character builds. A character can cover several roles, but skill training time and job-slot utilization determine whether that breadth is worthwhile.

### Manufacturing specialist

Primary functions:
- Manufacturing T1 and T2 components, ships, modules, and other products.
- Running multiple Manufacturing jobs concurrently.
- Starting jobs remotely within the character's range.
- Reducing job duration and material/time inefficiency where applicable.

Priority skills:
- Industry and Advanced Industry for manufacturing duration.
- Mass Production and Advanced Mass Production for Manufacturing slots.
- Supply Chain Management for remote job installation.
- Item-specific construction skills required by the target blueprints.

Mass Production V unlocks Advanced Mass Production. The basic and advanced slot skills increase concurrent job count; Industry and Advanced Industry reduce job duration. Do not treat these effects as interchangeable. [^eveuni-production-skills]

### Science and invention specialist

Primary functions:
- ME and TE research.
- BPO copying.
- Tech II invention and BPC generation.
- Remote Science job installation.

Priority skills:
- Laboratory Operation and Advanced Laboratory Operation for Science slots.
- Scientific Networking for remote job start.
- Metallurgy and Research for ME/TE research duration.
- Science for copying duration.
- Advanced Industry for applicable Manufacturing and research time effects.
- Item-specific Science and Encryption Methods skills for invention probability.

Research Project Management increases the number of R&D agents a character can use. It does not increase the character's normal Industry Science job slots. [^eveuni-science-skills] [^eveuni-invention]

### Reaction specialist

Primary functions:
- Composite, Hybrid, and Biochemical/Molecular-Forged reactions.
- Producing intermediate materials for Tech II, Tech III, and booster chains.
- Remote reaction job management.

Priority skills:
- Reactions for reaction time reduction and formula prerequisites.
- Mass Reactions and Advanced Mass Reactions for Reaction slots.
- Remote Reactions for remote job management.
- The relevant reactor family, formula, refinery, and structure access.

Reactions reduces reaction time; Mass Reactions and Advanced Mass Reactions add Reaction slots. Remote Reactions does not transport inputs or outputs. [^eveuni-resource-skills]

### Market and trade specialist

Primary functions:
- Placing and modifying market orders.
- Managing buy/sell execution across a chosen market range.
- Reducing broker fees and sales taxes.

Priority skills:
- Accounting for sales-tax reduction.
- Broker Relations for NPC station broker-fee reduction.
- Advanced Broker Relations for relist-fee reduction.
- Trade-range skills such as Marketing, Procurement, Daytrading, Visibility, and related skills when remote order management is operationally important.

Upwell structure broker fees do not receive the Broker Relations skill reduction. Trade skills should be selected according to the actual order-management workflow and current market rules. [^eveuni-trade-skills]

### Planetary Industry specialist

Primary functions:
- Managing multiple colonies.
- Improving Command Center CPU/powergrid capacity.
- Scanning planets and planning extraction layouts.
- Managing Customs Office/Skyhook transfers.

Priority skills:
- Interplanetary Consolidation for additional planets.
- Command Center Upgrades for colony CPU/powergrid.
- Remote Sensing for scan distance.
- Planetology and Advanced Planetology for scan resolution.
- Customs Code Expertise for the CONCORD portion of high-security PI export tax.

Planetology skills improve scan interpretation; they do not directly multiply extractor output. [^eveuni-planet-management]

## Skill categories and marginal effects

| Skill category | Main effect | When it is valuable |
|---|---|---|
| Job-slot skills | Add concurrent jobs | When the corresponding pool is consistently slot-constrained |
| Job-time skills | Reduce duration of selected activities | When slot-hours limit output or a deadline is important |
| Invention skills | Increase success probability | When invention is a material bottleneck and expected cost is sensitive to probability |
| Remote-start skills | Increase job-start range | When travel time or remote facility access is a recurring constraint |
| Market-fee skills | Reduce transaction costs | When market turnover and order volume justify training |
| PI skills | Add colonies or improve colony capacity/scans | When PI extraction/factory throughput is part of the operation |
| Item-specific construction skills | Unlock or improve specific production | When the target product requires them |

The exact effects and prerequisites are recorded in [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md), [Tech II Invention](../02-production-systems/tech-2-invention.md), and the trade/planet-management skill references. [^eveuni-production-skills] [^eveuni-science-skills] [^eveuni-resource-skills] [^eveuni-trade-skills] [^eveuni-planet-management]

## Marginal skill-value model

For a proposed skill level increase:

```text
Marginal skill value
  = expected economic contribution with new skill
    - expected economic contribution at current skill
```

A simple training-efficiency measure is:

```text
Incremental contribution per training day
  = marginal skill value / skill training time in days
```

The value horizon must be explicit. A skill that adds one Manufacturing slot may be valuable if the character has enough materials, blueprints, capital, and demand to keep it occupied. The same slot has little immediate value if the character already has idle capacity.

For a time-reduction skill, estimate the additional output or time saved over the planned production horizon. A time reduction does not necessarily increase profit if another stage is the bottleneck or the finished product cannot be sold faster.

## Slot-skill priority

A job-slot skill should be prioritized when:
1. The corresponding job pool is consistently near full utilization.
2. The operation has enough inputs and blueprints to use the additional slot.
3. The added slot can be used without creating excess inventory.
4. The marginal contribution exceeds the cost/opportunity cost of training.

The advanced slot skills require the basic slot skill at V. Training the base skill to V therefore has two effects: it adds the fifth slot from that skill and unlocks the advanced slot skill. The advanced skill then adds up to five more slots. [^eveuni-production-skills] [^eveuni-science-skills] [^eveuni-resource-skills]

Do not automatically train all three job-slot pools to maximum on every character. A specialized character may be better served by maximizing only the pool that supports its role.

## Multi-character role allocation

Because job slots are character-specific, additional industrial characters can add parallel capacity. The most useful allocation depends on which pool is constrained:

- A manufacturing character can focus on Manufacturing slots and time modifiers.
- A science character can focus on copying, invention, and research.
- A reaction character can focus on Reaction slots and reaction-time reduction.
- A market character can manage trade orders and fees.
- A PI character can operate colonies and export/import workflows.

A single character can train multiple roles, but spreading training across all roles may delay access to high-value skill thresholds. Separate characters can increase total job-slot capacity, but they add account/character management, asset movement, and operational overhead. These costs belong in [Industrial Scaling](industrial-scaling.md).

## Skill planning workflow

1. Measure current Manufacturing, Science, and Reaction slot utilization.
2. Identify the actual production-chain bottleneck.
3. Identify the skill levels that directly affect that bottleneck.
4. Calculate the marginal contribution of the next skill level.
5. Compare incremental value with training time and skillbook cost.
6. Check prerequisite skills and the value of reaching level V to unlock an advanced skill.
7. Consider whether another character or buying the intermediate product would be more efficient.
8. Recalculate after the skill is trained because the bottleneck may move to another stage.

## Common errors

1. Training job-slot skills before the character has enough materials, blueprints, or capital to use the added slots.
2. Confusing slot skills with time-reduction skills.
3. Assuming Research Project Management adds Science job slots.
4. Assuming remote-start skills transport blueprints, materials, or output.
5. Training invention skills without a reliable supply of input BPCs and datacores.
6. Training reaction skills without access to a compatible Refinery and reactor service.
7. Training PI skills without a plan for Customs Office/Skyhook transfers and commodity sales.
8. Evaluating a skill only by its nominal percentage bonus instead of its marginal effect on the complete production chain.

## Boundaries and unresolved details

This document is a general role and skill-value framework. It does not generate a personalized skill queue or calculate exact skill training times. Those require a character's current skills, attributes/implants, account state, target products, and planned facilities.

Open work:
- Build a skill-plan calculator from a character's ESI skill data and a selected production workload.
- Compare one broadly trained character against separate manufacturing/science/reaction characters.
- Quantify the value of market and PI skills for a selected operation.
- Include character/account management and training costs in the multi-character scaling model.

## Related concepts

- [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md)
- [Manufacturing Throughput](manufacturing-throughput.md)
- [Science and Invention Throughput](science-and-invention-throughput.md)
- [Reaction Throughput](reaction-throughput.md)
- [Production Scheduling](production-scheduling.md)
- [Industrial Scaling](industrial-scaling.md)
- [Capital and Asset Management](../04-industrial-economics/capital-and-asset-management.md)

[^ccp-activities-jobs]: CCP Support, Activities and Job Types (updated 2024-08-29).
[^eveuni-production-skills]: EVE University Wiki, Skills:Production (last modified 2025-09-09).
[^eveuni-science-skills]: EVE University Wiki, Skills:Science (last modified 2024-06-28).
[^eveuni-resource-skills]: EVE University Wiki, Skills: Resource Processing (last modified 2026-01-27).
[^eveuni-trade-skills]: EVE University Wiki, Skills:Trade (accessed 2026-11-14).
[^eveuni-planet-management]: EVE University Wiki, Skills:Planet Management (accessed 2026-11-14).
[^eveuni-invention]: EVE University Wiki, Invention (last modified 2026-10-09).
