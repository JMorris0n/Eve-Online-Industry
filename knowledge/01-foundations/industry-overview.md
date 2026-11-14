---
type: Concept
title: Industry Overview
description: High-level map of EVE Online industrial activities, job pools, input sources, production stages, and economic constraints.
tags:
  - industry
  - foundations
  - overview
sources:
  - id: ccp-activities-jobs
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: ccp-manufacturing
    resource: https://support.eveonline.com/hc/en-us/articles/203210292-Manufacturing
    title: Manufacturing | EVE Online Support (updated 2024-08-29)
  - id: ccp-reactions
    resource: https://support.eveonline.com/hc/en-us/articles/115005405785-Reactions
    title: Reactions | EVE Online Support (updated 2024-08-29)
  - id: ccp-planetary-interaction
    resource: https://support.eveonline.com/hc/en-us/articles/203269871-Planetary-Interaction
    title: Planetary Interaction | EVE Online Support (updated 2024-03-01)
  - id: eveuni-industry
    resource: https://wiki.eveuniversity.org/Industry
    title: Industry | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T10:30:00Z
status: draft
---

## Purpose

EVE Online industry is a network of activities that convert resources, blueprints, formulas, and player labor into intermediate and finished goods. Industrial operations range from simple Tech I manufacturing to invention-driven Tech II production, reactions, Tech III chains, capital ships, structures, boosters, and Planetary Industry.

The system is not one manufacturing queue. It contains separate activity types, distinct character job pools, activity-specific facilities, and several independent input supply chains. [^ccp-activities-jobs] [^eveuni-industry]

## Core activity groups

| Activity group | What it does | Main input | Main output |
|---|---|---|---|
| Manufacturing | Builds items from a blueprint | BPO/BPC and materials | Finished item or component |
| Science | Improves BPOs, creates BPCs, or attempts invention | BPO/BPC and activity-specific inputs | Improved BPO, BPC, or invented BPC |
| Reactions | Converts materials using a Reaction Formula | Formula and reaction inputs | Intermediate materials |
| Planetary Industry | Extracts and processes planetary resources | Colony, resources, schematics, and structures | Planetary commodities |
| Reprocessing | Converts eligible items into raw materials | Ore, ice, modules, ships, or salvage where supported | Minerals or other materials |
| Market and logistics | Procures, transfers, and sells inputs/outputs | ISK, orders, cargo, contracts | Materials at the required location and realized proceeds |

CCP formally classifies Manufacturing, Science, and Reaction as separate industry job types. Planetary Industry and reprocessing use different interfaces and mechanics and should not be modeled as if they were ordinary Manufacturing jobs. [^ccp-activities-jobs] [^ccp-manufacturing] [^ccp-reactions] [^ccp-planetary-interaction]

## Character job pools

The three character-managed industry pools are:

- **Manufacturing:** manufacturing jobs.
- **Science:** ME research, TE research, copying, and invention.
- **Reaction:** reaction jobs.

Each pool has its own slot skills and capacity. One pool's unused slots cannot be used by another pool. See [Skills and Job Capacity](skills-and-job-capacity.md).

## Common industrial supply chain

A simplified industrial chain is:

1. **Resource acquisition:** mine ore, harvest gas, extract moon materials, salvage wrecks, operate PI colonies, or buy materials.
2. **Raw-material processing:** reprocess ore/ice, process moon materials, refine gas, or convert raw resources through reactions.
3. **Intermediate production:** build components, planetary commodities, polymers, advanced materials, and other inputs.
4. **Blueprint preparation:** research BPOs, copy BPCs, or obtain BPCs through invention, loyalty stores, contracts, or loot.
5. **Manufacturing:** assemble components and final products.
6. **Distribution:** move output to the required market, corporation, fleet, or customer.
7. **Sale and accounting:** execute market orders/contracts, account for fees, and reconcile realized proceeds.

Not every product uses every stage. A simple Tech I module may require only a BPO, minerals, and a Manufacturing job. A Tech III ship may require relic reverse engineering, salvage, fullerite gas, Hybrid Reactions, Hybrid Components, and final Manufacturing.

## Inputs and materials

Industrial inputs can originate from:
- Asteroid ore and ice.
- Moon ore and processed moon materials.
- Known-space mykoserocin/cytoserocin gas.
- Wormhole fullerite gas.
- Sleeper salvage.
- Planetary commodities.
- NPC-sold trade goods and datacores.
- Loot, relics, loyalty stores, and contracts.
- Existing market inventory and player-produced intermediates.

Materials are not economically free because they are mined, extracted, looted, or produced internally. Their relevant cost is the replacement value or opportunity cost of the best alternative use. See [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md).

## Main industrial product families

| Product family | Typical dependencies | Dedicated concepts |
|---|---|---|
| Tech I items | BPO/BPC, minerals, Manufacturing | [Tech I Manufacturing](../02-production-systems/tech-1-manufacturing.md) |
| Tech II items | T1 BPC, invention, datacores, decryptors, advanced components | [Tech II Invention](../02-production-systems/tech-2-invention.md), [Tech II Components](../02-production-systems/tech-2-components.md) |
| Tech III ships/subsystems | Relics, reverse engineering, Sleeper salvage, fullerites, Hybrid Reactions and Components | [Tech III Manufacturing](../02-production-systems/tech-3-manufacturing.md) |
| Capital ships | Capital components, minerals, capital ship construction skills, specialized facilities | [Advanced Manufacturing](../02-production-systems/advanced-manufacturing.md) |
| Upwell structures | Structure components, PI materials, minerals, specialized assembly | [Advanced Manufacturing](../02-production-systems/advanced-manufacturing.md) |
| Combat boosters | Known-space gas, biochemical reactions, Drug Manufacturing | [Advanced Manufacturing](../02-production-systems/advanced-manufacturing.md) |
| Planetary commodities | Planetary resources and schematics | [Planetary Industry](../02-production-systems/planetary-industry.md) |

The exact product recipes and required skills are item-specific. Use the current SDE and the in-game Industry interface rather than hardcoding category assumptions.

## Economic and operational constraints

A production plan must account for:
- Blueprint quality and licensed runs.
- Character skills and available job slots.
- Facility services, role bonuses, rigs, taxes, and system cost indices.
- Material availability and job-level rounding.
- Science/reaction dependencies and probabilistic invention.
- Working capital and inventory holding time.
- Logistics, structure continuity, and asset risk.
- Market liquidity, order-book depth, and price impact.

The slowest or most constrained stage limits sustainable output. A full Manufacturing queue does not help if invention cannot supply BPCs, reactions cannot supply components, or the market cannot absorb finished inventory.

## Data and source model

Use CCP's SDE for static definitions such as types, blueprints, reaction formulas, and planetary schematics. Use ESI and the live Industry/PI interface for current market, system-index, character, facility, and job information. See [ESI and Market Data](../07-tools-and-data/esi-and-market-data.md).

Keep game mechanics, derived calculations, strategy, and hypotheses separate. See [Data Quality and Reconciliation](../07-tools-and-data/data-quality.md).

## Related concepts

- [Blueprints and Research](blueprints-and-research.md)
- [Skills and Job Capacity](skills-and-job-capacity.md)
- [Facilities and Rigs](facilities-and-rigs.md)
- [Advanced Manufacturing](../02-production-systems/advanced-manufacturing.md)
- [Production Systems](../02-production-systems/index.md)
- [Materials and Sourcing](../03-materials-and-sourcing/index.md)
- [Industrial Economics](../04-industrial-economics/index.md)
- [Optimization](../05-optimization/index.md)

[^ccp-activities-jobs]: CCP Support, Activities and Job Types (updated 2024-08-29).
[^ccp-manufacturing]: CCP Support, Manufacturing (updated 2024-08-29).
[^ccp-reactions]: CCP Support, Reactions (updated 2024-08-29).
[^ccp-planetary-interaction]: CCP Support, Planetary Interaction (updated 2024-03-01).
[^eveuni-industry]: EVE University Wiki, Industry (accessed 2026-11-14).
