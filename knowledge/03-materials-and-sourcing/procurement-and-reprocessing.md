---
type: Concept
title: Procurement and Reprocessing
description: Industrial material sourcing, replacement cost, ore/ice/moon reprocessing, scrapmetal processing, facility yield, and procurement decisions.
tags:
  - procurement
  - reprocessing
  - sourcing
  - costs
sources:
  - id: eveuni-reprocessing
    resource: https://wiki.eveuniversity.org/Reprocessing
    title: Reprocessing | EVE University Wiki (page carries a review warning)
  - id: eveuni-resource-skills
    resource: https://wiki.eveuniversity.org/Skills:Resource_Processing
    title: Skills:Resource Processing | EVE University Wiki
  - id: eveuni-minerals
    resource: https://wiki.eveuniversity.org/Minerals
    title: Minerals | EVE University Wiki
  - id: eveuni-compression
    resource: https://wiki.eveuniversity.org/Compression
    title: Compression | EVE University Wiki
  - id: ccp-esi-api-explorer
    resource: https://esi.evetech.net/ui/?version=latest
    title: ESI API Explorer
  - id: ccp-sde-docs
    resource: https://developers.eveonline.com/docs/services/static-data/
    title: Static Data Export Documentation
generated:
  by: openai/gpt-6
  at: 2026-11-14T11:00:00Z
status: draft
---

## Purpose

Procurement determines how an industrial operation obtains the materials it needs. Reprocessing converts eligible raw materials or items into recovered materials. Both decisions should be evaluated using opportunity cost and the actual facility/character configuration.

A material is not free because it was mined, looted, extracted, or produced by another character in the same corporation. Its economic cost is the value of the best alternative use or sale.

## Procurement channels

| Channel | Typical inputs | Main economic consideration |
|---|---|---|
| Market purchase | Minerals, moon materials, gas, salvage, PI, components | Quantity-aware buy cost, fees, and location |
| Mining | Asteroid ore, ice, Mercoxit | Pilot time, ship/fit, boosts, risk, compression, and hauling |
| Moon mining | Moon ore and moon materials | Refinery/Moon Drill operation, extraction cycle, mining, and reprocessing |
| Gas harvesting | Mykoserocin, Cytoserocin, Fullerites | Site access, harvesting time, ship risk, and logistics |
| Salvaging | Ancient Salvage and other salvage | Site completion time, salvage access, and export risk |
| Planetary Industry | Planetary commodities | Colony setup, extraction, processor idle time, customs tax, and transfer |
| Reactions | Intermediate/advanced materials | Formula inputs, fuel, reactor service, and installation fee |
| NPC/LP/loot sources | Datacores, special components, BPCs, trade goods | Acquisition restrictions, opportunity cost, and volume |

Use the correct acquisition route for each material. A market buy order is not a guaranteed procurement price for a large quantity; calculate the volume-weighted cost through eligible sell orders. See [Market Mechanics](../06-market-intelligence/market-mechanics.md) and [Demand and Liquidity](../06-market-intelligence/demand-and-liquidity.md).

## Material valuation

Choose one consistent valuation basis:

- **Replacement cost:** current cost to buy the same material at the production location.
- **Opportunity cost:** net value of the best alternative use or sale.
- **Historical cost:** actual acquisition price, useful for cash-flow records.
- **Internal transfer price:** a declared price for materials moved between stages of one production chain.

For consolidated manufacturing profitability, avoid double-counting internally produced intermediates. If moon materials are reacted into a composite material and then manufactured into a component, count the original material value and conversion costs once in the final chain.

## Reprocessing categories

Reprocessing behavior differs by input class:

| Input class | Output | Main skill/facility dependencies |
|---|---|---|
| Asteroid ore | Minerals | Reprocessing, Reprocessing Efficiency, relevant Ore Processing skill, facility/rig, implant |
| Ice | Ice products | Reprocessing skills, Ice Processing, facility/rig, implant |
| Moon ore | Moon materials and, for some ores, minerals | Generic reprocessing skills, moon-ore class skill, facility/rig, implant |
| Modules/ships and other eligible scrapmetal | Minerals | Scrapmetal Processing and base equipment yield |
| Other eligible materials | Item-specific output | Check the live Reprocessing window and SDE |

Do not assume the same yield formula applies to ore, ice, moon ore, and scrapmetal. The in-game Reprocessing window displays the exact output for the current character and facility.

## Reprocessing yield model

The EVE University Reprocessing page documents the following general structure for Upwell ore/ice/moon-ore yield. The page currently carries an update warning related to the December 2021 ore-processing skill changes, so treat the formula below as a secondary-source model pending in-game verification. [^eveuni-reprocessing]

```text
Yield (%)
  = (50 + Rm)
    × (1 + Sec)
    × (1 + Sm)
    × (1 + R × 0.03)
    × (1 + Re × 0.02)
    × (1 + Op × 0.02)
    × (1 + Im)
```

Where:

| Variable | Meaning | Values documented by EVE University |
|---|---|---|
| Rm | Rig modifier, percentage points | 0 no rig, 1 T1 rig, 3 T2 rig |
| Sec | Security modifier | 0.00 high-sec, 0.06 low-sec, 0.12 null/W-space; only applies with rigs |
| Sm | Structure modifier | 0.00 other Upwell, 0.02 Athanor, 0.055 Tatara |
| R | Reprocessing skill level | 0–5; +3% per level |
| Re | Reprocessing Efficiency level | 0–5; +2% per level |
| Op | Applicable Ore Processing skill level | 0–5; +2% per level |
| Im | Reprocessing implant modifier | 0.00, 0.01, 0.02, or 0.04 |

The formula is not a substitute for the live preview. Confirm the exact facility base yield, rig modifier, structure modifier, and applicable skill in the current client before using it in a profitability model. [^eveuni-reprocessing] [^eveuni-resource-skills]

### NPC station yield and tax

EVE University documents NPC reprocessing equipment base efficiencies between 30% and 50%. The station's reprocessing tax is separate from the yield and depends on the pilot's or corporation's standing with the station owner. The cited page states that tax begins at 5% at zero standing and falls to zero at 6.67 standing. Because the page carries a review warning, verify the live Reprocessing window before using these values in an economic calculation. [^eveuni-reprocessing]

### Scrapmetal reprocessing

Modules, ships, and other eligible scrapmetal use a separate formula. The EVE University reference states that Scrapmetal Processing increases the base equipment yield by 2% per skill level and that the formula is not affected by the ore-processing rigs, structure bonuses, or reprocessing implants. Do not apply the ore/ice/moon formula to scrapmetal. Verify the current result in the live UI. [^eveuni-reprocessing] [^eveuni-resource-skills]

## Reprocessing decision

For an input batch:

```text
Net reprocessing advantage
  = value of recovered outputs
    - opportunity value of input batch
    - reprocessing tax/fee
    - hauling and handling cost
```

Use the current output quantities from the Reprocessing UI and quantity-aware prices for each recovered material. If the output contains several co-products, do not assign the entire input cost independently to each output. For internal accounting, use a consistent joint-cost allocation method, such as relative net realizable value, and retain the unallocated total for reconciliation.

## Compression and transport

Compression reduces volume and can make mining outputs easier to move. It does not automatically make the compressed material more valuable. Compare:
- Volume before and after compression.
- Compression access/service and any cost.
- Hauling capacity and route risk.
- Whether the destination has a better sale price or reprocessing yield.
- The current reprocessing output for compressed and uncompressed forms.

See [Minerals and Ore](minerals-and-ore.md) and [Logistics and Risk](../04-industrial-economics/logistics-and-risk.md). [^eveuni-compression]

## Procurement workflow

1. Identify the exact material type ID and required quantity.
2. Compare direct market purchase, internal production, and reprocessing.
3. Calculate market procurement VWAP for the planned quantity.
4. For mined/extracted materials, calculate opportunity cost and operating cost.
5. Obtain a live reprocessing quote for the actual character and facility.
6. Calculate recovered outputs and their sale/replacement values.
7. Include tax, fee, compression, and logistics.
8. Select the lowest total economic cost, not the lowest displayed unit price.
9. Store source timestamps, facility configuration, skill state, and calculation version.

## Data requirements

The procurement/reprocessing dataset should retain:
- Input type ID, quantity, and volume.
- Reprocessing facility and base yield.
- Character skills and implants.
- Rig/structure/security modifiers.
- Exact UI output quantities.
- Tax and fee.
- Market valuation basis and timestamp.
- Compression state and logistics.
- Source and verification status.

## Related concepts

- [Minerals and Ore](minerals-and-ore.md)
- [Moon Materials](moon-materials.md)
- [Gas and Fullerites](gas-and-fullerites.md)
- [Sleeper Salvage](sleeper-salvage.md)
- [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md)
- [Market Mechanics](../06-market-intelligence/market-mechanics.md)
- [ESI and Market Data](../07-tools-and-data/esi-and-market-data.md)

[^eveuni-reprocessing]: EVE University Wiki, Reprocessing (accessed 2026-11-14; page carries an update warning for ore-processing skill changes).
[^eveuni-resource-skills]: EVE University Wiki, Skills: Resource Processing (accessed 2026-11-14).
[^eveuni-minerals]: EVE University Wiki, Minerals (accessed 2026-11-14).
[^eveuni-compression]: EVE University Wiki, Compression (accessed 2026-11-14).
[^ccp-esi-api-explorer]: CCP, ESI API Explorer.
[^ccp-sde-docs]: CCP, Static Data Export documentation.
