---
type: Concept
title: Sleeper Salvage
description: Sleeper wreck salvage, Ancient Salvage materials, blue-loot distinction, and Tech III component supply.
tags:
  - sleepers
  - salvage
  - tech-iii
sources:
  - id: ccp-salvaging
    resource: https://support.eveonline.com/hc/en-us/articles/213014209-Salvaging
    title: Salvaging | EVE Online Support (updated 2024-07-15)
  - id: eveuni-sleepers
    resource: https://wiki.eveuniversity.org/Sleepers
    title: Sleepers | EVE University Wiki
  - id: eveuni-salvaging
    resource: https://wiki.eveuniversity.org/Guide_To_Salvaging
    title: Salvaging | EVE University Wiki
  - id: eveuni-t3-production
    resource: https://wiki.eveuniversity.org/Tech_3_Production
    title: Tech 3 Production | EVE University Wiki (last modified 2024-09-22)
  - id: ccp-sde-docs
    resource: https://developers.eveonline.com/docs/services/static-data/
    title: Static Data Export Documentation
generated:
  by: openai/gpt-6
  at: 2026-11-14T11:00:00Z
status: draft
---

## Purpose

Sleeper salvage is a specialized input stream for Tech III production. Sleepers are encountered in wormhole-space sites; their wrecks can be salvaged for Ancient Salvage materials used to manufacture Hybrid Tech Components. These components are then used in Tech III hull and subsystem manufacturing. [^eveuni-sleepers] [^eveuni-t3-production]

## Sleeper wrecks and salvage

Sleeper NPCs appear in wormhole-space cosmic signatures and anomalies. Their wrecks can contain:
- **Blue loot:** Sleeper Components and other NPC buyback items that are sold to designated NPC stations or on the player market.
- **Ancient Salvage:** salvage materials recovered from wrecks and used in Tech III component production.

Blue loot and Ancient Salvage are separate economic streams. Do not count blue-loot NPC buyback value as a material input to Hybrid Component manufacturing. [^eveuni-sleepers]

## Salvaging mechanics

A Salvager module or Salvaging Drone attempts to access the salvageable components in a wreck. CCP states that:
- Each wreck has a predetermined amount of salvageable components.
- Skills and rigs improve the chance of successfully accessing salvage and allow access to more difficult wrecks.
- Better skills/equipment do not increase the amount of salvage contained in the wreck.
- A failed access attempt does not consume the salvage or reduce the amount available.
- Salvage is free-for-all; the first pilot to successfully salvage a wreck receives its salvage. [^ccp-salvaging]

The salvage skill and rig investment therefore improves access reliability and time, not the intrinsic salvage quantity of a particular wreck.

## Industrial role

Ancient Salvage is combined with Hybrid Polymers to manufacture Hybrid Tech Components. Hybrid Polymers are created by reacting Fullerite gases in a Refinery with a Hybrid Reactor. The component BPOs are then used in ordinary Manufacturing jobs. [^eveuni-t3-production]

The simplified chain is:

```text
Wormhole gas sites
  → Fullerite gas
  → Hybrid Reactions
  → Hybrid Polymers

Sleeper combat sites
  → Sleeper wrecks
  → Ancient Salvage

Hybrid Polymers + Ancient Salvage
  → Hybrid Tech Components
  → Tech III hulls and subsystems
```

The Tech III BPC supply is a parallel chain: ancient relics are reverse-engineered into limited-run BPCs. See [Tech III Manufacturing](../02-production-systems/tech-3-manufacturing.md).

## Salvage families and data requirements

The exact Ancient Salvage items and quantities depend on the wreck/site distribution. A canonical data matrix should record:
- Salvage type ID and name.
- Sleeper NPC class/faction and site family.
- Expected occurrence or quantity, where a reliable source exists.
- Hybrid Component BPOs that consume the salvage.
- Market value and regional liquidity.
- Source and last verification date.

Do not use generic Tech I/Tech II faction salvage tables as a substitute for Sleeper Ancient Salvage. Do not hardcode a salvage distribution from an old guide without a current SDE or reproducible source.

## Risk and logistics

Sleeper sites are combat sites, not passive salvage fields. The value of salvage must account for:
- Combat ship and fit costs.
- Site completion time and risk.
- Salvage ship or module opportunity cost.
- Wormhole access, scouting, rolling, and transport.
- Cargo volume and export logistics.
- Risk of losing both combat and salvage ships.

The economic value of salvage is its opportunity cost: the best alternative sale value or replacement cost of the same materials.

## Source limitations

The EVE University Sleepers and Tech 3 Production pages carry update warnings or older last-modified dates. Use them for the broad chain and terminology, but verify exact site distribution, item quantities, and current T3 recipe data against the SDE and in-game blueprints. CCP's Salvaging support article is the primary source for the salvage-access mechanics.

## Related concepts

- [Gas and Fullerites](gas-and-fullerites.md)
- [Tech III Manufacturing](../02-production-systems/tech-3-manufacturing.md)
- [Advanced Manufacturing](../02-production-systems/advanced-manufacturing.md)
- [Reactions](../02-production-systems/reactions.md)
- [Procurement and Reprocessing](procurement-and-reprocessing.md)

[^ccp-salvaging]: CCP Support, Salvaging (updated 2024-07-15).
[^eveuni-sleepers]: EVE University Wiki, Sleepers (accessed 2026-11-14; page carries a game-change update warning).
[^eveuni-salvaging]: EVE University Wiki, Salvaging (accessed 2026-11-14).
[^eveuni-t3-production]: EVE University Wiki, Tech 3 Production (last modified 2024-09-22).
[^ccp-sde-docs]: CCP, Static Data Export documentation.
