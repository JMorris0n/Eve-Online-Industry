---
type: Concept
title: Advanced Manufacturing
description: Taxonomy of capital ship, structure, booster, Tech II, Tech III, and specialist manufacturing chains and their facility dependencies.
tags:
  - manufacturing
  - advanced
  - capital-ships
  - structures
  - boosters
sources:
  - id: ccp-manufacturing
    resource: https://support.eveonline.com/hc/en-us/articles/203210292-Manufacturing
    title: Manufacturing | EVE Online Support (updated 2024-08-29)
  - id: ccp-reactions
    resource: https://support.eveonline.com/hc/en-us/articles/115005405785-Reactions
    title: Reactions | EVE Online Support (updated 2024-08-29)
  - id: ccp-upwell-structures
    resource: https://support.eveonline.com/hc/en-us/articles/213021829-Upwell-Structures
    title: Upwell Structures | EVE Online Support (updated 2024-07-15)
  - id: ccp-upwell-quick-facts
    resource: https://support.eveonline.com/hc/en-us/articles/209985225-Upwell-Structures-Quick-Facts
    title: Upwell Structures - Quick Facts | EVE Online Support (updated 2022-05-10)
  - id: eveuni-manufacturing
    resource: https://wiki.eveuniversity.org/Manufacturing
    title: Manufacturing | EVE University Wiki
  - id: eveuni-structure-browser
    resource: https://wiki.eveuniversity.org/Structure_Browser
    title: Upwell Structures | EVE University Wiki
  - id: eveuni-production-skills
    resource: https://wiki.eveuniversity.org/Skills:Production
    title: Skills:Production | EVE University Wiki
  - id: eveuni-reactions
    resource: https://wiki.eveuniversity.org/Reactions
    title: Reactions | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T10:30:00Z
status: draft
---

## Purpose

Advanced manufacturing is not one separate industry activity. It is a collection of product families whose production chains require additional inputs, skills, reactions, or specialized facilities beyond ordinary Tech I manufacturing.

The key planning task is to map each product to its actual upstream dependencies and required activity services. Product-level recipes and input quantities should be taken from the current SDE and verified against the in-game Industry interface.

## Product-family map

| Product family | Typical chain | Special constraints |
|---|---|---|
| Tech II items | T1 BPC → invention → T2 BPC → T2 components/materials → final Manufacturing | Science capacity, invention probability, advanced components |
| Tech III ships/subsystems | Ancient relic → reverse engineering → T3 BPC; fullerite reactions → Hybrid materials → Hybrid Components → final Manufacturing | Relic type, Sleeper salvage, Hybrid Reactor, Science/Reaction capacity |
| Capital ships | Minerals and capital components → capital ship Manufacturing | Capital Ship Construction skill, Capital Shipyard service, eligible Engineering Complex |
| Supercapital ships | Capital components and supercapital-specific materials → supercapital Manufacturing | Supercapital Construction service, Sotiyo, sovereignty upgrade |
| Upwell structures | PI-heavy structure components and other materials → structure Manufacturing | Manufacturing service, structure components, final assembly location |
| Combat boosters | Mykoserocin/cytoserocin gas → biochemical reactions → booster Manufacturing | Biochemical Reactor, Drug Manufacturing skill, security-space restriction |
| Faction/storyline products | Item-specific BPC and rare components → Manufacturing | Special BPC source, rare inputs, item-specific skills |

This table is a dependency map, not a complete bill of materials. The exact inputs, skill levels, run limits, and facility services depend on the item. [^eveuni-manufacturing] [^ccp-manufacturing] [^ccp-reactions]

## Tech II manufacturing

Tech II manufacturing normally requires an invented Tech II BPC and advanced components, with additional materials depending on the product. The T1 BPO is copied into a T1 BPC, invention attempts produce a T2 BPC, and the T2 BPC is used for the final Manufacturing job.

The upstream chain includes:
- Tech I BPO research and copying.
- Science job slots and invention skills.
- Datacores and optional decryptors.
- Advanced Components, often supplied by Composite Reactions and component Manufacturing.
- Final Tech II Manufacturing.

Use [Tech II Invention](tech-2-invention.md) and [Tech II Components](tech-2-components.md) for the detailed mechanics.

## Tech III manufacturing

Tech III production is a distinct four-stage chain:
1. Obtain an ancient relic.
2. Reverse engineer it to produce a limited-run Tech III BPC.
3. Source Sleeper salvage, fullerite gas, and other materials; run Hybrid Reactions and manufacture Hybrid Components.
4. Manufacture the final ship or subsystem.

Tech III uses ancient relics and reverse engineering rather than ordinary T1-to-T2 invention. See [Tech III Manufacturing](tech-3-manufacturing.md), [Sleeper Salvage](../03-materials-and-sourcing/sleeper-salvage.md), and [Gas and Fullerites](../03-materials-and-sourcing/gas-and-fullerites.md).

## Capital ship manufacturing

Capital ship production adds skill and facility constraints to ordinary blueprint manufacturing.

EVE University's Production skill reference documents Capital Ship Construction as a specialized skill with Mechanics V, Industry V, and Advanced Industry V prerequisites. The skill level gates product families:
- Level I: capital-sized ship components, capital-sized modules/weapons, freighters, Orca, and Tech I/faction fighters.
- Level III: carriers, dreadnoughts, and force auxiliaries.
- Level IV: supercarriers, Rorqual, and jump freighters.
- Level V: titans. [^eveuni-production-skills]

The facility must offer the appropriate capital ship manufacturing service. EVE University documents the Standup Capital Shipyard service as available only on Large and Extra Large Engineering Complexes and not in high-security space. Supercapital manufacturing requires the Standup Supercapital Shipyard service on a Sotiyo and the relevant sovereignty infrastructure upgrade. Verify the current service/module availability in the structure browser and live Industry UI before planning a job. [^eveuni-structure-browser]

Capital production has large material and capital requirements, long job durations, and significant logistics exposure. The correct planning unit is the complete hull chain, including capital components and intermediate inputs, not merely the final blueprint's direct mineral bill.

## Upwell structure manufacturing

Upwell structures are manufactured from sub-components. EVE University notes that structure components use substantial Planetary Industry materials and can be purchased or manufactured separately. CCP's Upwell quick facts state that both structure components and final structures can be manufactured in NPC stations or Upwell structures offering an online Manufacturing service. [^eveuni-structure-browser] [^ccp-upwell-quick-facts]

A structure build therefore requires:
- The structure blueprint and all required component/material inputs.
- A facility with the Manufacturing service online.
- A location that can stage the large volume of inputs and final output.
- A logistics plan for the finished structure and deployment components.
- The quantum core, service modules, and fuel required for deployment/online operation, where applicable.

Manufacturing the structure is separate from anchoring and operating it. Do not treat the manufacturing bill as the total cost of deploying a working Upwell structure.

## Combat booster manufacturing

Combat boosters use mykoserocin and cytoserocin gas harvested from known-space gas sites. These gases are distinct from wormhole fullerites used in Tech III production. The gas is processed into biochemical materials through reactions in a Refinery with a compatible Biochemical Reactor; the resulting materials are then used in booster Manufacturing. [^ccp-reactions] [^eveuni-reactions] [^eveuni-manufacturing]

The Drug Manufacturing skill is required for booster manufacturing. The biochemical reactor service is only available at Refineries, and CCP's reaction documentation states that reactors can only be installed in systems with security 0.4 or lower. [^eveuni-production-skills] [^ccp-reactions]

Booster chains should be modeled as separate gas procurement, reaction, and Manufacturing stages. Include the opportunity cost of gas and any required additional reaction input materials.

## Faction and storyline production

Some faction, storyline, and COSMOS products use special BPCs and rare components obtained through missions, data sites, relic sites, loyalty stores, or other item-specific sources. Their skill requirements can extend beyond ordinary Industry skills. EVE University's Manufacturing reference documents examples of storyline production requiring racial Encryption Methods and specialized technology skills. [^eveuni-manufacturing]

Do not assume every faction item follows the ordinary Tech II invention chain. Verify the specific BPC's Manufacturing activity and input bill.

## Facility and service matrix

| Activity | Typical facility/service | Important restriction |
|---|---|---|
| Standard Manufacturing | NPC station or Upwell Manufacturing service | Structure service must be online |
| Capital ship Manufacturing | Capital Shipyard service | Large/XL Engineering Complex; not high-sec |
| Supercapital Manufacturing | Supercapital Shipyard service | Sotiyo and sovereignty upgrade |
| Composite Reactions | Refinery with Composite Reactor | System security 0.4 or lower |
| Hybrid Reactions | Refinery with Hybrid Reactor | System security 0.4 or lower |
| Biochemical Reactions | Refinery with Biochemical Reactor | System security 0.4 or lower |
| Tech II invention | Facility with Invention service | Science inputs and Science slot |
| Blueprint research/copying | Facility with Research service | Science inputs and Science slot |

CCP and EVE University document the service-module and refinery constraints. The current structure browser and Industry window remain the operational check for a specific facility. [^ccp-upwell-structures] [^eveuni-structure-browser] [^ccp-reactions]

## Economic implications

Advanced product families amplify upstream dependencies. A high-margin final item may be constrained by:
- Scarce or volatile moon materials.
- Gas or Sleeper salvage supply.
- PI component availability.
- Science job slots and invention success variance.
- Reaction slots and reactor compatibility.
- Capital shipyard or structure service access.
- Large working-capital and logistics requirements.
- Thin market liquidity for high-value finished goods.

Use a full-chain model and normalize each stage into final-product units per day. Compare internal production against buying intermediate components or the finished product.

## Data and verification requirements

- Use the current SDE to build item-level blueprint, reaction, and schematic matrices.
- Verify special skill prerequisites against the in-game skill browser.
- Verify service-module eligibility and security restrictions against current CCP documentation and the structure browser.
- Obtain live job quotes for facility tax, SCI, rig effects, and installation fees.
- Keep capital, structure, and booster recipes separate from ordinary T1/T2 recipes.
- Record patch/version context for any item-specific exception.

## Related concepts

- [Tech I Manufacturing](tech-1-manufacturing.md)
- [Tech II Invention](tech-2-invention.md)
- [Tech II Components](tech-2-components.md)
- [Tech III Manufacturing](tech-3-manufacturing.md)
- [Reactions](reactions.md)
- [Planetary Industry](planetary-industry.md)
- [Minerals and Ore](../03-materials-and-sourcing/minerals-and-ore.md)
- [Moon Materials](../03-materials-and-sourcing/moon-materials.md)
- [Gas and Fullerites](../03-materials-and-sourcing/gas-and-fullerites.md)
- [Sleeper Salvage](../03-materials-and-sourcing/sleeper-salvage.md)

[^ccp-manufacturing]: CCP Support, Manufacturing (updated 2024-08-29).
[^ccp-reactions]: CCP Support, Reactions (updated 2024-08-29).
[^ccp-upwell-structures]: CCP Support, Upwell Structures (updated 2024-07-15).
[^ccp-upwell-quick-facts]: CCP Support, Upwell Structures - Quick Facts (updated 2022-05-10).
[^eveuni-manufacturing]: EVE University Wiki, Manufacturing (accessed 2026-11-14).
[^eveuni-structure-browser]: EVE University Wiki, Upwell Structures / Structure Browser (accessed 2026-11-14).
[^eveuni-production-skills]: EVE University Wiki, Skills:Production (last modified 2025-09-09).
[^eveuni-reactions]: EVE University Wiki, Reactions (last modified 2025-06-22).
