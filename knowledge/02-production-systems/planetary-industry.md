---
type: Concept
title: Planetary Industry
description: Planetary colony mechanics, resource extraction, on-planet processing, skills, routing, storage, customs offices, skyhooks, and export economics.
tags:
  - planetary-industry
  - extraction
  - planetary-production
sources:
  - id: ccp-planetary-interaction
    resource: https://support.eveonline.com/hc/en-us/articles/203269871-Planetary-Interaction
    title: Planetary Interaction | EVE Online Support (updated 2024-03-01)
  - id: ccp-alpha-omega
    resource: https://support.eveonline.com/hc/en-us/articles/213020969-Alpha-and-Omega-Clone
    title: Alpha and Omega Clone | EVE Online Support (updated 2026-02-04)
  - id: ccp-alpha-quick-facts
    resource: https://support.eveonline.com/hc/en-us/articles/213811425-Alpha-Clones-and-Omega-Clone-lapsing-Quick-Facts
    title: Alpha Clones and Omega Clone lapsing - Quick Facts | EVE Online Support (updated 2024-07-15)
  - id: ccp-skyhook
    resource: https://support.eveonline.com/hc/en-us/articles/14339732733724-Orbital-Skyhook
    title: Orbital Skyhook | EVE Online Support (updated 2024-06-11)
  - id: ccp-equinox
    resource: https://www.eveonline.com/news/view/equinox-expansion-notes
    title: Equinox Expansion Notes | EVE Online
  - id: eve-dev-sde
    resource: https://developers.eveonline.com/docs/services/static-data/
    title: EVE Developer Documentation | Static Data Export
  - id: eve-dev-sde-rework
    resource: https://developers.eveonline.com/blog/reworking-the-sde-a-fresh-start-for-static-data
    title: "Reworking the SDE: a fresh start for static data (published 2025-09-22)"
  - id: eveuni-planetary-industry
    resource: https://wiki.eveuniversity.org/Planetary_Industry
    title: Planetary Industry | EVE University Wiki (page flagged for Equinox update)
  - id: eveuni-planetary-buildings
    resource: https://wiki.eveuniversity.org/Planetary_buildings
    title: Planetary Buildings | EVE University Wiki (last modified 2022-10-23)
  - id: eveuni-planet-management
    resource: https://wiki.eveuniversity.org/Command_Center_Upgrades
    title: Skills:Planet Management | EVE University Wiki
  - id: eveuni-customs-office
    resource: https://wiki.eveuniversity.org/Player_Owned_Customs_Office
    title: Player Owned Customs Office | EVE University Wiki
  - id: eveuni-setup
    resource: https://wiki.eveuniversity.org/Setting_up_a_planetary_colony
    title: Setting up a planetary colony | EVE University Wiki
  - id: eveuni-planetary-commodities
    resource: https://wiki.eveuniversity.org/Planetary_Commodities
    title: Planetary Commodities | EVE University Wiki (last modified 2025-08-20)
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:40:00Z
status: draft
---

## Summary

Planetary Industry (PI), historically called Planetary Interaction, is a colony-based production system. Characters deploy a Command Center on a planet, extract raw planetary resources, and optionally process them through on-planet facilities into higher-tier commodities. PI is not a normal blueprint manufacturing activity: planetary processors use built-in schematics rather than player-owned BPOs or BPCs. [^ccp-planetary-interaction] [^eveuni-planetary-buildings]

PI should be modeled as a combination of resource extraction, factory throughput, planetary CPU/powergrid constraints, routing and storage, and customs-office or skyhook logistics. A colony can be an extractor, a factory that imports inputs, or a hybrid.

## Terminology and production flow

| Term | Meaning |
|---|---|
| P0 / R0 | Raw planetary resource extracted by an ECU |
| P1 | Processed Material produced from one P0 resource |
| P2 | Refined Commodity produced from two P1 types |
| P3 | Specialized Commodity produced from two or three P2 types |
| P4 | Advanced Commodity produced from P3 inputs, or P3 plus a P1 input |

The four processing tiers are described in [Planetary Commodities](../03-materials-and-sourcing/planetary-commodities.md). Exact schematic inputs, quantities, and cycle times are static game data and should be taken from the current SDE and checked against the in-game schematic. [^eveuni-planetary-industry] [^eve-dev-sde]

## Colony deployment and capacity

A colony begins with a Command Center that matches the planet type. The Command Center supplies the colony's CPU and powergrid budget. Every building and planetary link consumes part of that budget, so the maximum layout is constrained by both structure placement and the available CPU/powergrid. [^eveuni-planetary-buildings] [^eveuni-setup]

The Command Center must be carried to the target system and deployed in space. After deployment, the colony can be edited through Planet Mode. Changes must be submitted before they become active. The Command Center can be upgraded in place; it cannot simply be moved to another location on the same planet. [^eveuni-planetary-buildings] [^eveuni-setup]

### Planet-management skills

| Skill | Effect | Important distinction |
|---|---|---|
| Interplanetary Consolidation | Adds one additional planet per level, up to six total planets | Controls colony count, not buildings per planet |
| Command Center Upgrades | Unlocks higher Command Center levels with more CPU and powergrid | Controls colony layout capacity |
| Remote Sensing | Allows resource scans at greater light-year distances | Scan range is in light-years, not gate jumps |
| Planetology | Improves resource scan resolution | Improves interpretation of resource distribution, not extraction output directly |
| Advanced Planetology | Further improves scan resolution | Requires Planetology IV |

EVE University lists Remote Sensing scan ranges of 1, 3, 5, 7, and 9 light-years at levels I through V. Interplanetary Consolidation allows one additional planet per level, to a maximum of six. These skill descriptions and prerequisites should be checked against the current in-game skill browser before a character plan is finalized. [^eveuni-planet-management]

Planetology and Advanced Planetology affect how accurately the player can interpret resource scans. They do not directly increase the output of a running extractor program. Do not model scan resolution as an extraction-yield multiplier. [^eveuni-planet-management]

## Planetary structures

| Structure | Primary function |
|---|---|
| Command Center | Supplies colony CPU and powergrid; provides limited storage and a small export launch |
| Extractor Control Unit (ECU) | Installs an extraction program for one selected P0 resource |
| Extractor Heads | Positionable heads deployed by an ECU to extract from selected areas |
| Basic Industry Facility (BIF) | Converts P0 into P1 |
| Advanced Industry Facility (AIF) | Converts P1 into P2 or P2 into P3 |
| High-Tech Production Plant (HTPP) | Converts P3 inputs, optionally with a P1 input, into P4 |
| Storage Facility | Provides an intermediate buffer for materials |
| Launchpad | Provides a larger buffer and the normal customs-office import/export interface |
| Links | Connect buildings and carry routed materials between them |

A Command Center, Launchpad, or Storage Facility can provide buffers. A Launchpad is the normal choice for routine imports and exports. Storage is particularly important between extractors and processors because processor input storage is limited; routing an uncontrolled surplus directly into a full or busy processor can destroy excess materials. [^eveuni-planetary-buildings] [^eveuni-setup]

## Extraction programs

An ECU is configured for a selected P0 resource. The player chooses an extraction program, positions extractor heads within the ECU's operating area, selects a program duration, and creates routes for the extracted material. EVE University's building reference documents a maximum of ten heads per ECU and programs up to 14 days; confirm current limits in the live ECU interface before using them in a simulator. [^eveuni-planetary-buildings]

Extractor yield is not a constant rate. The extraction program consists of cycles whose yields vary over time as the selected resource deposit is depleted and replenished. Head placement, overlap, extraction-area size, resource concentration, and program duration affect the resulting output. A scan is a forecast of the resource distribution, not a guarantee that the same amount will be extracted in every cycle. [^eveuni-planetary-buildings] [^eveuni-setup]

Shorter programs generally allow more frequent repositioning and can provide higher hourly extraction, but require more player attention. Longer programs reduce management frequency while spreading extraction over a longer period. This is an operational trade-off, not a universal rule that the shortest program always produces the best colony.

The extraction output must have a valid route to a destination. A route requires a connected link path. A link by itself does not define which product moves along it. Verify both links and routes after changing a colony layout. [^eveuni-planetary-buildings]

## On-planet processing

Processors run built-in schematics. They are not manufacturing jobs installed through the normal Industry job system, and they do not consume character Manufacturing job slots. Their throughput is determined by schematic batch sizes and cycle times, processor count, input availability, routing, and colony capacity. [^eveuni-planetary-buildings] [^eveuni-planetary-commodities]

- Basic Industry Facilities process P0 into P1.
- Advanced Industry Facilities process P1 into P2 or P2 into P3.
- High-Tech Production Plants process P3 inputs, or two P3 inputs plus a P1 input, into P4.
- High-Tech Production Plants can only be placed on Barren or Temperate planets according to the community building reference. Verify current placement restrictions in game. [^eveuni-planetary-buildings] [^eveuni-planetary-commodities]

A processor can only buffer a limited quantity of input. The building reference warns that sending more material than a processor can accept can result in excess material being lost. Use a Launchpad or Storage Facility as a buffer when extractor output is uneven or exceeds factory consumption. [^eveuni-planetary-buildings]

## Links, routes, and colony engineering

Links connect planetary buildings. Routes specify which commodity moves over the connected network and to which destination. Links have finite throughput; multiple routes sharing a link can create a bottleneck. Longer links consume more colony CPU and powergrid, so compact layouts reduce infrastructure overhead. [^eveuni-planetary-buildings]

A colony design should therefore be checked against four independent constraints:

1. **CPU:** building and link CPU usage must fit the upgraded Command Center budget.
2. **Powergrid:** building and link powergrid usage must fit the upgraded Command Center budget.
3. **Link capacity:** the shared link paths must carry the required commodity volume.
4. **Buffer capacity:** storage and processor input/output limits must absorb timing differences between extraction and production.

A layout that fits CPU and powergrid can still underperform because of insufficient link capacity, missing routes, full storage, or mismatched factory throughput.

## Customs offices, launches, and Orbital Skyhooks

PI materials must be moved from the planetary surface to space before they can be used elsewhere. There are two main paths:

- **Command Center launch:** a small export-only rocket launch. CCP states that launched containers remain in space for five days before degrading and being removed. [^ccp-planetary-interaction]
- **Launchpad through an orbital structure:** the Launchpad interfaces with the planet's orbital Customs Office or, in player-owned sovereign null security space, an Orbital Skyhook. This is the normal route for larger exports and is also the route used to import materials to a planet. [^ccp-planetary-interaction] [^ccp-skyhook]

The Orbital Skyhook replaced the orbital Customs Office in player-owned sovereign null security space. It retains customs-office functionality for PI and is required for planetary-resource access in that space. Only one Skyhook can be attached to a planet, and it can only be deployed in player-owned sovereign null security space. [^ccp-skyhook]

A Skyhook also produces separate sovereignty resources: Power, Workforce, and Reagents, depending on planet type. These are not the same thing as P0 planetary commodities and should not be mixed into the PI commodity recipe system. [^ccp-skyhook]

### Tax considerations

CCP states that exporting from a high-security planet incurs both the Customs Office owner tax and a CONCORD tax. Training Customs Code Expertise reduces the CONCORD portion. The actual Customs Office or Skyhook rate and the applicable fees should be checked in the live transfer interface. Do not assume that the owner tax is reduced by Customs Code Expertise. [^ccp-planetary-interaction]

Import and export fees are an important part of multi-planet production economics. A factory planet that imports several intermediate products can pay repeated transfer charges before the finished commodity is exported. Record the displayed rate for each planet and calculate import and export costs separately.

### Alpha clone restriction

CCP's current Alpha and Omega clone-state article states that Alpha clones can perform Planetary Industry actions but cannot export from their colonies. CCP's Alpha quick-facts article clarifies that Alpha clones can import materials into colonies but cannot export assets from them. The older Planetary Interaction support article uses broader wording that can be read as restricting both directions; for current clone-state behavior, use the newer clone-state article and quick facts. [^ccp-alpha-omega] [^ccp-alpha-quick-facts] [^ccp-planetary-interaction]

Operational implication: an Alpha character can import inputs and manage colony activity, but cannot complete the export leg needed to retrieve and sell the colony's output. A sale-oriented PI workflow therefore requires an Omega character to export goods.

## Planetary Industry after Equinox

Equinox introduced the Orbital Skyhook and new colony resources in sovereign null security space. The Skyhook is both a PI customs interface and a sovereignty-resource structure. Its Power, Workforce, and Reagents are separate from the normal P0-to-P4 PI commodity chain. [^ccp-skyhook] [^ccp-equinox]

The EVE University Planetary Industry overview currently carries an explicit warning that it needs updating for Equinox and new resources/structures. Use it for basic pre-Equinox concepts only where corroborated by current CCP material or the live client. Do not rely on its old statements about nullsec customs offices, colony resources, or current system restrictions without checking the current game. [^eveuni-planetary-industry]

## Data sources and reproducibility

CCP's Static Data Export is the canonical source for static schematic data. The developer documentation says the SDE is distributed in JSON Lines and YAML formats and changes with game updates. The SDE was substantially reworked in September 2025, so older parsers and community CSV conversions may not be compatible with the new schema. [^eve-dev-sde] [^eve-dev-sde-rework]

For PI, the SDE data model should be used to build a reproducible commodity and schematic catalog. The relevant current schema includes planetary schematic definitions, associated pin/building types, and input/output product quantities. Preserve the SDE build identifier and extraction date whenever generating derived recipe tables.

The in-game PI window remains the operational source for current planet scans, live colony state, available facilities, and actual customs-office or skyhook transfer rates.

## Operational checklist

Before activating or modifying a colony:

1. Confirm planet type and deploy the matching Command Center.
2. Check available CPU and powergrid at the current Command Center level.
3. Confirm the resource type and deposit location.
4. Position extractor heads and inspect overlap penalties.
5. Choose an extraction duration that matches the intended maintenance schedule.
6. Route extractor output to storage or a processor with sufficient capacity.
7. Verify every link, route, and link-capacity bottleneck.
8. Match processor count and schematic cycles to expected input supply.
9. Confirm Launchpad storage and the orbital Customs Office or Skyhook access/tax.
10. Record the colony's actual output over multiple cycles before using forecast extraction as a production commitment.

## Related concepts

- [Planetary Commodities](../03-materials-and-sourcing/planetary-commodities.md)
- [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md)
- [Installation Costs](../01-foundations/installation-costs.md)
- [Tech II Components](tech-2-components.md)
- [Tech III Manufacturing](tech-3-manufacturing.md)

## Open verification tasks

- Confirm the current maximum extractor heads and extraction-program duration in the live client.
- Verify current Command Center CPU/powergrid values and building costs against the current SDE.
- Confirm current High-Tech Production Plant placement restrictions and all processor cycle times.
- Reconcile all P0-P4 schematics and quantities against the current SDE.
- Verify Customs Code Expertise's current exact per-level effect and distinguish NPC tax from owner-set tax.
- Confirm import/export fee calculation for Customs Offices and Skyhooks after Equinox.
- Verify current Alpha clone PI restrictions in the live client.
- Determine whether any Equinox-era changes affect planet eligibility, extraction output, or colony restrictions.

[^ccp-planetary-interaction]: CCP Support, Planetary Interaction (updated 2024-03-01).
[^ccp-alpha-omega]: CCP Support, Alpha and Omega Clone (updated 2026-02-04).
[^ccp-alpha-quick-facts]: CCP Support, Alpha Clones and Omega Clone lapsing - Quick Facts (updated 2024-07-15).
[^ccp-skyhook]: CCP Support, Orbital Skyhook (updated 2024-06-11).
[^ccp-equinox]: EVE Online, Equinox Expansion Notes.
[^eve-dev-sde]: EVE Developer Documentation, Static Data Export.
[^eve-dev-sde-rework]: EVE Developer Documentation, Reworking the SDE: a fresh start for static data (2025-09-22).
[^eveuni-planetary-industry]: EVE University Wiki, Planetary Industry (page explicitly flagged for Equinox update; accessed 2026-11-14).
[^eveuni-planetary-buildings]: EVE University Wiki, Planetary Buildings (last modified 2022-10-23).
[^eveuni-planet-management]: EVE University Wiki, Skills:Planet Management (accessed 2026-11-14).
[^eveuni-customs-office]: EVE University Wiki, Player Owned Customs Office (accessed 2026-11-14).
[^eveuni-setup]: EVE University Wiki, Setting up a planetary colony (accessed 2026-11-14).
[^eveuni-planetary-commodities]: EVE University Wiki, Planetary Commodities (last modified 2025-08-20).
