---
type: Concept
title: Planetary Commodities
description: P0-to-P4 planetary resource and commodity tiers, processor schematics, recipe examples, batch sizes, and industrial uses.
tags:
  - planetary-industry
  - pi
  - commodities
  - recipes
sources:
  - id: eveuni-planetary-commodities
    resource: https://wiki.eveuniversity.org/Planetary_Commodities
    title: Planetary Commodities | EVE University Wiki (last modified 2025-08-20)
  - id: eveuni-planetary-buildings
    resource: https://wiki.eveuniversity.org/Planetary_buildings
    title: Planetary Buildings | EVE University Wiki (last modified 2022-10-23)
  - id: eve-dev-sde
    resource: https://developers.eveonline.com/docs/services/static-data/
    title: EVE Developer Documentation | Static Data Export
  - id: eve-dev-sde-rework
    resource: https://developers.eveonline.com/blog/reworking-the-sde-a-fresh-start-for-static-data
    title: Reworking the SDE: a fresh start for static data (2025-09-22)
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:40:00Z
status: draft
---

## Purpose and scope

Planetary commodities are produced by extracting raw resources from planets and processing them through on-planet facilities. The commodity chain is divided into P0, P1, P2, P3, and P4 tiers. Higher-tier products can be used as inputs to later PI schematics or consumed by other industry activities. [^eveuni-planetary-commodities]

This file records the tier model, standard processor batch structure, and representative recipes. It is not yet a complete machine-generated recipe catalog. The full current recipe matrix must be regenerated from CCP's SDE and checked against in-game schematics.

## Commodity tiers

| Tier | Common name | Input | Processor |
|---|---|---|---|
| P0 / R0 | Raw planetary resource | Extracted by ECU | Extractor |
| P1 | Processed Material | One P0 resource | Basic Industry Facility |
| P2 | Refined Commodity | Two different P1 commodities | Advanced Industry Facility |
| P3 | Specialized Commodity | Two or three P2 commodities | Advanced Industry Facility |
| P4 | Advanced Commodity | Three P3 commodities, or two P3 plus one P1 | High-Tech Production Plant |

A P0 resource is extracted from a planet. Each processing tier advances the commodity one step. A commodity does not need to be processed to P4: many P1, P2, and P3 items have direct uses in other production chains. [^eveuni-planetary-commodities]

## Standard schematic batch sizes

The EVE University commodity and building references document these standard batch patterns. These values are secondary-source-derived and should be cross-checked against the current SDE and live schematic before being used as production-model constants. [^eveuni-planetary-commodities] [^eveuni-planetary-buildings]

| Processing step | Inputs per batch | Output per batch | Cycle time | Processor |
|---|---|---|---|---|
| P0 to P1 | 3,000 units of one P0 | 20 units of one P1 | 30 minutes | Basic |
| P1 to P2 | 40 units of each of two P1 types | 5 units of one P2 | 1 hour | Advanced |
| P2 to P3 | 10 units of each of two or three P2 types | 3 units of one P3 | 1 hour | Advanced |
| P3 to P4 | 6 units of each of three P3 types, or 6 units each of two P3 plus 40 units of one P1 | 1 unit of one P4 | 1 hour | High-Tech |

These are batch quantities, not per-unit recipes. A throughput model must multiply batch requirements by the number of completed schematic cycles and account for the fact that each processor can only run one selected schematic at a time.

## P0 to P1 resource mapping

The following P0-to-P1 mapping is transcribed from the EVE University Planetary Commodities reference. Planet availability and commodity mapping should be validated against the current SDE and in-game planet scan data. [^eveuni-planetary-commodities]

| P0 resource | P1 processed material |
|---|---|
| Microorganisms | Bacteria |
| Carbon Compounds | Biofuels |
| Planktic Colonies | Biomass |
| Non-CS Crystals | Chiral Structures |
| Ionic Solutions | Electrolytes |
| Autotrophs | Industrial Fibers |
| Reactive Gas | Oxidizing Compound |
| Noble Gas | Oxygen |
| Suspended Plasma | Plasmoids |
| Noble Metals | Precious Metals |
| Complex Organisms | Proteins |
| Base Metals | Reactive Metals |
| Felsic Magma | Silicon |
| Heavy Metals | Toxic Metals |
| Aqueous Liquids | Water |

## P1 to P2 schematic recipes

Each P2 schematic combines two different P1 commodities. The following recipe pairs are transcribed from the EVE University Planetary Commodities reference. Exact input quantities are covered in the batch table above and must be checked against the current schematic. [^eveuni-planetary-commodities]

| P1 input A | P1 input B | P2 output |
|---|---|---|
| Precious Metals | Biofuels | Biocells |
| Toxic Metals | Reactive Metals | Construction Blocks |
| Chiral Structures | Toxic Metals | Consumer Electronics |
| Water | Electrolytes | Coolant |
| Toxic Metals | Precious Metals | Enriched Uranium |
| Proteins | Bacteria | Fertilizer |
| Biomass | Proteins | Genetically Enhanced Livestock |
| Biofuels | Proteins | Livestock |
| Precious Metals | Reactive Metals | Mechanical Parts |
| Silicon | Industrial Fibers | Microfiber Shielding |
| Silicon | Chiral Structures | Miniature Electronics |
| Reactive Metals | Bacteria | Nanites |
| Oxygen | Oxidizing Compound | Oxides |
| Industrial Fibers | Oxidizing Compound | Polyaramids |
| Industrial Fibers | Biofuels | Polytextiles |
| Electrolytes | Plasmoids | Rocket Fuel |
| Silicon | Oxidizing Compound | Silicate Glass |
| Water | Plasmoids | Superconductors |
| Biomass | Oxygen | Supertensile Plastics |
| Oxygen | Electrolytes | Synthetic Oil |
| Water | Bacteria | Test Cultures |
| Chiral Structures | Plasmoids | Transmitter |
| Biomass | Bacteria | Viral Agent |
| Water | Reactive Metals | Water-Cooled CPU |

## P2 to P3 schematic recipes

Each P3 schematic combines two or three P2 inputs. [^eveuni-planetary-commodities]

| P2 input A | P2 input B | P2 input C | P3 output |
|---|---|---|---|
| Nanites | Livestock | Construction Blocks | Biotech Research Reports |
| Silicate Glass | Rocket Fuel | | Camera Drones |
| Oxides | Coolant | | Condensates |
| Test Cultures | Synthetic Oil | Fertilizer | Cryoprotectant Solution |
| Supertensile Plastics | Microfiber Shielding | | Data Chips |
| Oxides | Biocells | Superconductors | Gel-Matrix Biopaste |
| Water-Cooled CPU | Transmitter | | Guidance Systems |
| Polytextiles | Viral Agent | Transmitter | Hazmat Detection Systems |
| Polyaramids | Genetically Enhanced Livestock | | Hermetic Membranes |
| Polyaramids | Transmitter | | High-Tech Transmitters |
| Fertilizer | Polytextiles | | Industrial Explosives |
| Biocells | Silicate Glass | | Neocoms |
| Microfiber Shielding | Enriched Uranium | | Nuclear Reactors |
| Supertensile Plastics | Mechanical Parts | Miniature Electronics | Planetary Vehicles |
| Mechanical Parts | Consumer Electronics | | Robotics |
| Construction Blocks | Miniature Electronics | | Smartfab Units |
| Water-Cooled CPU | Coolant | Consumer Electronics | Supercomputers |
| Supertensile Plastics | Test Cultures | | Synthetic Synapses |
| Biocells | Nanites | | Transcranial Microcontrollers |
| Synthetic Oil | Superconductors | | Ukomi Superconductors |
| Livestock | Viral Agent | | Vaccines |

## P3 to P4 schematic recipes

P4 commodities are produced in a High-Tech Production Plant. The following recipes are transcribed from the EVE University Planetary Commodities reference. [^eveuni-planetary-commodities]

| P3 input A | P3 input B | P1 or P3 input C | P4 output |
|---|---|---|---|
| Neocoms | Data Chips | High-Tech Transmitters | Broadcast Node |
| Gel-Matrix Biopaste | Hazmat Detection Systems | Planetary Vehicles | Integrity Response Drones |
| Industrial Explosives | Ukomi Superconductors | Reactive Metals (P1) | Nano-Factory |
| Condensates | Robotics | Bacteria (P1) | Organic Mortar Applicators |
| Synthetic Synapses | Guidance Systems | Transcranial Microcontrollers | Recursive Computing Module |
| Camera Drones | Nuclear Reactors | Hermetic Membranes | Self-Harmonizing Power Core |
| Smartfab Units | Vaccines | Water (P1) | Sterile Conduits |
| Supercomputers | Biotech Research Reports | Cryoprotectant Solution | Wetware Mainframe |

## Commodity uses

PI commodities are intermediate industrial materials, not merely products for direct sale. Depending on the item, they are used in Tech II components and research components, structure fuel and construction, sovereignty structures and upgrades, capital and ship components, Nanite Repair Paste, implants, boosters, and other specialized products. A commodity's value therefore depends on both market demand and its downstream use. [^eveuni-planetary-commodities]

## Volume compression and production economics

The early PI tiers generally reduce the volume of material being moved. The community reference gives these standard batch volumes:

- P0 to P1: 3,000 P0 units (15 m³) become 20 P1 units (3.8 m³).
- P1 to P2: 40 units each of two P1 inputs (15.2 m³ combined) become 5 P2 units (3.75 m³).
- P2 to P3: 10 units each of two or three P2 inputs become 3 P3 units.
- P3 to P4: 6 units each of three P3 inputs, or two P3 inputs plus one P1 input, become 1 P4 unit.

Volume compression is not monotonically favorable at every stage. P4 units are large and some recipes can produce a higher output volume than the combined inputs. Do not assume processing to the highest possible tier always improves logistics or profit. [^eveuni-planetary-commodities]

A sound PI economic model should include opportunity cost of extracted P0 resources, factory cycle throughput and idle time, import/export taxes at each planet, link and buffer losses, transport costs and risk between planets, and market liquidity at each tier.

## Source quality and limitations

The Planetary Commodities reference was last modified 2025-08-20. EVE University's main Planetary Industry overview currently carries a warning that it needs updating for Equinox-era changes. This file therefore treats the commodity mapping as a useful secondary reference, not as a final current recipe database.

CCP's SDE is the authoritative static-data source for schematic names, input/output quantities, cycle times, and associated planetary building types. CCP reworked the SDE in September 2025 and made the new schema incompatible with older formats. A recipe extraction tool must use the current JSON Lines or YAML schema and record the SDE build number. [^eve-dev-sde] [^eve-dev-sde-rework]

## Open verification tasks

- Rebuild the P0-P4 recipe matrix from the current CCP SDE.
- Compare every schematic's input quantities, output quantity, cycle time, and required processor type against the in-game UI.
- Confirm whether the P0-to-P4 mappings and recipe quantities changed after the 2025 SDE rework or Equinox.
- Add stable type IDs and schematic IDs to the recipe catalog.
- Add planet-type availability for each P0 resource using current static data and in-game scans.
- Build a normalized machine-readable dataset for later calculations, while retaining this Markdown file as the human-readable reference.

[^eveuni-planetary-commodities]: EVE University Wiki, Planetary Commodities (last modified 2025-08-20).
[^eveuni-planetary-buildings]: EVE University Wiki, Planetary Buildings (last modified 2022-10-23).
[^eve-dev-sde]: EVE Developer Documentation, Static Data Export.
[^eve-dev-sde-rework]: EVE Developer Documentation, Reworking the SDE: a fresh start for static data (2025-09-22).
