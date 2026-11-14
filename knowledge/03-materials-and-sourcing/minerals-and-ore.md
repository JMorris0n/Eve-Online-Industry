---
type: Concept
title: Minerals and Ore
description: Base mineral families, asteroid ore sourcing, mining and compression concepts, reprocessing dependencies, and data-quality caveats.
tags:
  - minerals
  - ore
  - mining
sources:
  - id: eveuni-minerals
    resource: https://wiki.eveuniversity.org/Minerals
    title: Minerals | EVE University Wiki
  - id: eveuni-asteroids-ore
    resource: https://wiki.eveuniversity.org/Asteroids_and_ore
    title: Asteroids and Ore | EVE University Wiki
  - id: eveuni-mining
    resource: https://wiki.eveuniversity.org/Mining
    title: Mining | EVE University Wiki
  - id: eveuni-reprocessing
    resource: https://wiki.eveuniversity.org/Reprocessing
    title: Reprocessing | EVE University Wiki
  - id: ccp-sde-docs
    resource: https://developers.eveonline.com/docs/services/static-data/
    title: Static Data Export Documentation
  - id: ccp-esi-api-explorer
    resource: https://esi.evetech.net/ui/?version=latest
    title: ESI API Explorer
generated:
  by: openai/gpt-6
  at: 2026-11-14T10:50:00Z
status: draft
---

## Purpose

Asteroid ore is a primary source of minerals used in manufacturing. A mining operation can sell raw ore, compress it for transport, or reprocess it into minerals. The economically correct choice depends on ore type, location, mining opportunity cost, reprocessing yield, taxes, logistics, and current market prices.

This document establishes the material taxonomy and sourcing model. It intentionally avoids a fixed ore-location or yield table because community ore tables have documented update warnings after distribution changes. Use the current SDE and in-game mining/reprocessing interfaces for item-level data. [^eveuni-minerals] [^eveuni-asteroids-ore]

## Base minerals

The eight base minerals are:

| Mineral | Industrial role |
|---|---|
| Tritanium | Common mineral input across a wide range of manufacturing |
| Pyerite | Common mineral input |
| Mexallon | Common mineral input |
| Isogen | Common mineral input |
| Nocxium | Higher-tier mineral input |
| Zydrine | Higher-tier mineral input |
| Megacyte | Higher-tier mineral input |
| Morphite | Specialized mineral input, notably associated with Mercoxit reprocessing |

Minerals are inputs to most manufacturing chains. Their value should be based on replacement cost or opportunity cost, not assumed to be free because the operation mined them. [^eveuni-minerals]

## Ore families and sources

Ore types differ in:
- Mineral composition.
- Volume per unit.
- Reprocessing batch and yield.
- Availability by security space, region, anomaly, sovereignty, or special space type.
- Mining crystal and processing-skill requirements.
- Compression and transport economics.

Ore availability is not a single universal table. Asteroid belts, ordinary anomalies, upgraded sovereignty systems, low-security anomalies, wormhole space, and Pochven can have different ore populations. Some ore distribution pages explicitly warn that their location tables need updating after game changes. Do not use an old guide's location table as a live map. [^eveuni-asteroids-ore]

### Common sourcing categories

- **Empire-space ores:** common ores distributed through high-security and faction-space systems.
- **Low-security ores:** additional mineral compositions and higher-risk mining opportunities.
- **Null-security ores:** sovereignty upgrades and anomalies provide specialized ore access.
- **Wormhole ores:** anomaly-based ore sources that can overlap with some null-space ore families.
- **Pochven ores:** specialized ores with distinct mineral compositions.
- **Mercoxit:** a specialized ore source for Morphite and requires the appropriate mining equipment/skill.

The exact type IDs, material yields, and current distribution should be extracted from the current SDE where represented and checked against the live mining interface.

## Mining output

Mining output is affected by the fitted mining module, cycle duration, ship bonuses, character skills, mining crystals, boosts, and any applicable system or structure effects. Ore volume differs by type, so units mined per cycle are not directly comparable between ores.

For throughput comparisons, normalize output to:
- m³ mined per hour.
- Recovered mineral units per hour after reprocessing.
- ISK value per pilot-hour.
- ISK value per m³ moved.
- Risk-adjusted output per operating hour.

Do not compare mining yield using ore units alone when ore volumes differ. [^eveuni-mining]

## Compression

Compression reduces the volume required to move ore or other eligible materials. It is a logistics optimization, not an increase in the ore's intrinsic mineral content. Compare compressed and uncompressed forms using the same underlying batch and reprocessing output.

The value of compression is usually realized through reduced hauling volume, cargo capacity, and transport risk. Include compression access, service availability, and any applicable fee in the landed-cost model. [^eveuni-mining]

## Reprocessing relationship

Reprocessing converts eligible ore into minerals and, for moon ores, moon materials. The amount recovered depends on the input type and the reprocessing setup: facility equipment, structure/rig, character skills, processing skill, and implant. See [Procurement and Reprocessing](procurement-and-reprocessing.md).

Use the actual in-game reprocessing preview for a production decision. The EVE University Reprocessing page flags parts of its material tables for review after historical game changes; do not copy its older ore location/yield tables into the canonical corpus without current verification. [^eveuni-reprocessing]

## Mining versus buying

Compare the economic value of:
1. Selling the raw ore.
2. Reprocessing and selling the recovered minerals.
3. Reprocessing and using minerals internally.
4. Buying the minerals directly and using mining time elsewhere.

A useful decision calculation is:

```text
Net reprocessing value
  = market value of recovered outputs
    - opportunity value of raw ore
    - reprocessing fees/taxes
    - hauling and handling cost
```

For internal manufacturing, value recovered minerals at their replacement/opportunity cost. Mining time, ship loss risk, boosts, and hauling are economic inputs even when no ISK changes hands.

## Data requirements for a canonical ore matrix

A future SDE-derived dataset should include:
- Ore type ID and name.
- Ore group and volume.
- Compressed/uncompressed relationship.
- Reprocessing material outputs and quantities.
- Required processing skill.
- Current known location/anomaly distribution, with source and patch date.
- Mining crystal compatibility.
- Market order/history snapshot and timestamp.

Keep static ore/material data separate from live location availability and market prices.

## Related concepts

- [Moon Materials](moon-materials.md)
- [Procurement and Reprocessing](procurement-and-reprocessing.md)
- [Market Mechanics](../06-market-intelligence/market-mechanics.md)
- [Demand and Liquidity](../06-market-intelligence/demand-and-liquidity.md)
- [ESI and Market Data](../07-tools-and-data/esi-and-market-data.md)

[^eveuni-minerals]: EVE University Wiki, Minerals (accessed 2026-11-14; page notes ore distribution tables need updating after the October 2020 change).
[^eveuni-asteroids-ore]: EVE University Wiki, Asteroids and Ore (accessed 2026-11-14).
[^eveuni-mining]: EVE University Wiki, Mining (accessed 2026-11-14).
[^eveuni-reprocessing]: EVE University Wiki, Reprocessing (accessed 2026-11-14; page notes reprocessing skill content requires review after the December 2021 changes).
[^ccp-sde-docs]: CCP, Static Data Export documentation.
[^ccp-esi-api-explorer]: CCP, ESI API Explorer.
