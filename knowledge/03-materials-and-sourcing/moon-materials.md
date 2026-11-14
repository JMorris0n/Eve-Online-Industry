---
type: Concept
title: Moon Materials
description: Moon extraction, moon ore classes, reprocessing skill groups, and reaction supply-chain role.
tags:
  - moon-mining
  - moon-ore
  - materials
sources:
  - id: ccp-moon-mining
    resource: https://support.eveonline.com/hc/en-us/articles/115005404229-Moon-Mining
    title: Moon Mining | EVE Online Support (updated 2024-08-29)
  - id: eveuni-moon-mining
    resource: https://wiki.eveuniversity.org/Moon_mining
    title: Moon Mining | EVE University Wiki
  - id: eveuni-reactions
    resource: https://wiki.eveuniversity.org/Reactions
    title: Reactions | EVE University Wiki
  - id: ccp-reactions
    resource: https://support.eveonline.com/hc/en-us/articles/115005405785-Reactions
    title: Reactions | EVE Online Support (updated 2024-08-29)
  - id: ccp-sde-docs
    resource: https://developers.eveonline.com/docs/services/static-data/
    title: Static Data Export Documentation
generated:
  by: openai/gpt-6
  at: 2026-11-14T10:50:00Z
status: draft
---

## Purpose

Moon mining supplies specialized materials used in Tech II production and other industrial chains. Moon-specific ore is extracted through Upwell Refineries and a Standup Moon Drill, then fractured into an asteroid field for mining. The mined ore is reprocessed into moon materials and, for some ores, standard minerals. [^ccp-moon-mining]

## Extraction infrastructure and schedule

- A Refinery must be deployed near a Moon Mining Beacon and fitted with an online Standup Moon Drill.
- Moon Mining Beacons exist in systems with security 0.5 or lower.
- The extraction schedule can be set from 6 to 56 days.
- Longer extraction schedules pull larger moon chunks.
- After extraction completes, the structure owner can fracture the chunk into a mineable asteroid field.
- If not manually fractured, the chunk is automatically fractured approximately three hours after extraction completion; refinery rigs can modify this timing.
- The resulting moon-ore field remains available for a limited period and can be mined by eligible pilots.
- The refinery's corporation moon-mining ledger records mining activity from the field. [^ccp-moon-mining] [^eveuni-moon-mining]

Metenox Moon Drills provide an alternative automated extraction path. Their output and efficiency should be modeled separately from a player-operated Refinery/Moon Drill operation. [^eveuni-moon-mining]

## Moon ore classes

Moon ore is grouped into five rarity classes:

| Class | Rarity label | Primary material tier |
|---|---|---|
| R4 | Ubiquitous | Hydrocarbons, Silicates, Evaporite Deposits, Atmospheric Gases |
| R8 | Common | Cobalt, Scandium, Tungsten, Titanium |
| R16 | Uncommon | Chromium, Cadmium, Platinum, Vanadium |
| R32 | Rare | Technetium, Mercury, Caesium, Hafnium |
| R64 | Exceptional | Promethium, Neodymium, Dysprosium, Thulium |

The class name identifies the tier of moon material, not a guaranteed quantity per unit of ore. Exact ore-to-material outputs and ore quality modifiers should be sourced from the current SDE and confirmed in the reprocessing preview. [^eveuni-moon-mining]

### Ore families

| Class | Ore types |
|---|---|
| R4 | Bitumens, Coesite, Sylvite, Zeolites |
| R8 | Cobaltite, Euxenite, Scheelite, Titanite |
| R16 | Chromite, Otavite, Sperrylite, Vanadinite |
| R32 | Carnotite, Cinnabar, Pollucite, Zircon |
| R64 | Loparite, Monazite, Xenotime, Ytterbite |

All five classes occur in low-security and null-security space. High-security and wormhole space are limited to R4 moon ores according to the EVE University moon-mining reference. Verify current availability with live moon scans and current game data. [^eveuni-moon-mining]

## Moon scanning and deposit composition

Survey probes can reveal the relative composition of a moon's products. The export includes ore names, ore type IDs, relative quantities, and system/planet/moon IDs. These data are suitable for a local moon-resource database, but the percentage composition is not itself a guarantee of the final extracted volume or reprocessed material output. [^eveuni-moon-mining]

For a moon comparison, calculate:
- Expected ore volume per extraction schedule.
- Ore composition by type.
- Reprocessing output at the actual facility/skill configuration.
- Market value of recovered moon materials and standard minerals.
- Refinery fuel, tax, rig, extraction, and operational costs.
- Mining and hauling time/risk.

## Reprocessing and skill groups

CCP lists five moon ore processing skills, one for each class:

- Ubiquitous Moon Ore Processing.
- Common Moon Ore Processing.
- Uncommon Moon Ore Processing.
- Rare Moon Ore Processing.
- Exceptional Moon Ore Processing.

Each skill applies to its corresponding moon-ore class. The exact yield also depends on the reprocessing facility, rigs, generic reprocessing skills, and applicable implants. Use the live reprocessing preview and [Procurement and Reprocessing](procurement-and-reprocessing.md). [^ccp-moon-mining]

## Industrial uses

Moon materials are used in reaction chains that supply:
- Intermediate materials for Tech II production.
- Composite materials.
- Advanced Components used in Tech II manufacturing.
- Other specialized industrial products.

The reaction chain is not a direct one-step ore-to-component conversion. Moon ore must be reprocessed, moon materials reacted into intermediate/composite materials, and the resulting composites manufactured into components. [^ccp-reactions] [^eveuni-reactions]

See [Reactions](../02-production-systems/reactions.md) and [Tech II Components](../02-production-systems/tech-2-components.md).

## Economic considerations

Moon ore has value as a source of several co-products. Do not value a moon solely by its rarest material. The full recovered basket, reprocessing yield, market demand, and hauling cost determine economic value.

For a moon-mining operation, compare:
- The opportunity cost of selling raw moon ore.
- The net value of reprocessed materials.
- The cost of running the Refinery and Moon Drill.
- The value of the corporation's mining output and any tax/revenue-share arrangement.
- The market absorption of the resulting moon materials.

## Source limitations and data policy

The EVE University Moon Mining page currently carries an update warning. Use it for terminology and a broad ore-class taxonomy, but prioritize CCP's Moon Mining support article for extraction mechanics and the in-game moon scan/reprocessing interface for live values. Do not copy static moon compositions or reprocessing quantities without current data validation.

## Related concepts

- [Minerals and Ore](minerals-and-ore.md)
- [Reactions](../02-production-systems/reactions.md)
- [Tech II Components](../02-production-systems/tech-2-components.md)
- [Procurement and Reprocessing](procurement-and-reprocessing.md)
- [Market Mechanics](../06-market-intelligence/market-mechanics.md)

[^ccp-moon-mining]: CCP Support, Moon Mining (updated 2024-08-29).
[^eveuni-moon-mining]: EVE University Wiki, Moon Mining (accessed 2026-11-14; page currently carries an update warning).
[^eveuni-reactions]: EVE University Wiki, Reactions (accessed 2026-11-14).
[^ccp-reactions]: CCP Support, Reactions (updated 2024-08-29).
[^ccp-sde-docs]: CCP, Static Data Export documentation.
