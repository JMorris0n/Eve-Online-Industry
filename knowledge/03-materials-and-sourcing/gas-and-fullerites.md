---
type: Concept
title: Gas and Fullerites
description: Known-space mykoserocin/cytoserocin and wormhole fullerite gas sources, harvesting, and industrial uses.
tags:
  - gas
  - fullerites
  - boosters
  - tech-iii
sources:
  - id: eveuni-gas-harvesting
    resource: https://wiki.eveuniversity.org/Gas_cloud_harvesting
    title: Gas Cloud Harvesting | EVE University Wiki
  - id: eveuni-wormhole-gas
    resource: https://wiki.eveuniversity.org/Wormhole_gas_sites
    title: Wormhole Gas Sites | EVE University Wiki
  - id: ccp-reactions
    resource: https://support.eveonline.com/hc/en-us/articles/115005405785-Reactions
    title: Reactions | EVE Online Support (updated 2024-08-29)
  - id: eveuni-t3-production
    resource: https://wiki.eveuniversity.org/Tech_3_Production
    title: Tech 3 Production | EVE University Wiki
  - id: ccp-sde-docs
    resource: https://developers.eveonline.com/docs/services/static-data/
    title: Static Data Export Documentation
generated:
  by: openai/gpt-6
  at: 2026-11-14T10:50:00Z
status: draft
---

## Purpose

Harvestable gas is a specialized industrial resource. Known-space Mykoserocin and Cytoserocin support combat booster and Neurolink Enhancer production, while wormhole Fullerites support Tech III and capital production chains. Gas is harvested from cosmic signatures and then used directly or processed through reaction formulas. [^eveuni-gas-harvesting] [^ccp-reactions]

## Three industrial gas families

| Family | Typical source | Main industrial uses |
|---|---|---|
| Mykoserocin | Known-space nebula gas sites | Synth combat boosters and Neurolink Enhancers |
| Cytoserocin | Known-space nebula gas sites | Standard combat boosters and Neurolink Enhancers |
| Fullerites | Wormhole-space Fullerite Reservoirs | Hybrid Polymers for Tech III production and selected capital/Neurolink chains |

The exact gas type determines the reaction formula and product. Do not treat the three families as interchangeable.

## Site discovery and harvesting

Gas sites are cosmic signatures that must be probe-scanned. Known-space gas sites are commonly called nebulae; wormhole gas sites are Fullerite Reservoirs. Gas is collected with Gas Cloud Harvester modules. The in-game probe scanner may also label combat/hacking sites as chemical labs; those are not ordinary harvestable gas sites. [^eveuni-gas-harvesting]

Gas harvesting is not identical to asteroid mining. The module, skill, ship, cloud, and site conditions differ. Mining critical-hit behavior introduced for asteroid mining does not automatically apply to gas harvesting; check the current gas-harvesting rules rather than extrapolating from ore mining.

### Site risk

- Mykoserocin nebulae can occur in high-, low-, and null-security space; many are not guarded by NPCs.
- Cytoserocin sites can be unstable and may damage a ship during harvesting.
- Fullerite reservoirs are found in wormhole space. Sleeper defenders can appear after a delay, so a gas-harvesting operation must account for the site's escalation and combat risk.
- Valuable Fullerite Reservoir variants are associated with higher-class wormholes and shattered wormhole systems.

Exact site names, gas flavors, constellation locations, cloud quantities, damage behavior, and Sleeper spawn timing are patch-sensitive. Use the current probe scanner and current site data rather than treating community location lists as exhaustive. [^eveuni-gas-harvesting] [^eveuni-wormhole-gas]

## Gas volume and logistics

Mykoserocin and Cytoserocin have a standard volume of 10 m³ per unit. Fullerite volumes vary by type, commonly from 1 to 10 m³ per unit. Use the item's current Show Info and SDE volume rather than assuming every gas type has the same cargo footprint. [^eveuni-gas-harvesting]

Gas has a high opportunity cost when it feeds valuable reaction chains. Compare the cost of harvesting, hauling, and processing against the market replacement cost of the same gas.

## Industrial processing chains

### Combat boosters

1. Harvest Mykoserocin or Cytoserocin.
2. Run the applicable Biochemical Reaction to create booster-related biochemical materials.
3. Manufacture the booster using the correct blueprint and required skills.

Mykoserocin is used for synth booster production; Cytoserocin supports stronger booster variants. The exact gas inputs and outputs are formula-specific. [^eveuni-gas-harvesting] [^ccp-reactions]

### Tech III production

1. Harvest Fullerite gas in wormhole space.
2. Run Hybrid Reactions to create Hybrid Polymers.
3. Combine Hybrid Polymers and Ancient Salvage in Manufacturing to create Hybrid Components.
4. Use the components with an invented/reverse-engineered Tech III BPC to manufacture the final hull or subsystem.

This is a multi-stage chain; gas alone is not a finished Tech III material. [^eveuni-t3-production]

### Capital and Neurolink Enhancer production

Some Mykoserocin and Fullerite gases are inputs to Neurolink Enhancers used in capital ship production. The relevant reaction formula and output quantities are item-specific and should be extracted from the current SDE. [^eveuni-gas-harvesting] [^ccp-reactions]

## Procurement and valuation

For a gas input, compare:
- Direct market purchase cost.
- Harvesting time and ship/fit cost.
- Site risk and expected loss.
- Transport volume and route exposure.
- Reaction facility and fuel costs.
- Market liquidity of the resulting reaction product.

If the gas is harvested internally, value it at the best alternative sale value or replacement cost. Do not treat self-harvested gas as free.

## Data requirements

A canonical gas dataset should include:
- Gas type ID, name, and volume.
- Family: Mykoserocin, Cytoserocin, or Fullerite.
- Associated site type and known location data, with source/version date.
- Reaction formulas consuming the gas.
- Output material IDs and quantities.
- Required reactor family and fuel.
- Market orders/history and observation timestamps.

Keep static gas/reaction data separate from live site availability and market prices.

## Related concepts

- [Reactions](../02-production-systems/reactions.md)
- [Advanced Manufacturing](../02-production-systems/advanced-manufacturing.md)
- [Tech III Manufacturing](../02-production-systems/tech-3-manufacturing.md)
- [Sleeper Salvage](sleeper-salvage.md)
- [Procurement and Reprocessing](procurement-and-reprocessing.md)
- [Market Mechanics](../06-market-intelligence/market-mechanics.md)

[^eveuni-gas-harvesting]: EVE University Wiki, Gas Cloud Harvesting (accessed 2026-11-14; page includes current 2026 Catalyst gas-harvesting notes).
[^eveuni-wormhole-gas]: EVE University Wiki, Wormhole Gas Sites (accessed 2026-11-14).
[^ccp-reactions]: CCP Support, Reactions (updated 2024-08-29).
[^eveuni-t3-production]: EVE University Wiki, Tech 3 Production (accessed 2026-11-14).
[^ccp-sde-docs]: CCP, Static Data Export documentation.
