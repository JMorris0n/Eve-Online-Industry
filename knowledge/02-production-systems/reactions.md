---
type: Concept
title: Reactions
description: Reaction formulas, reactor families, security/location restrictions, composite moon-material processing, biochemical and hybrid reactions, inputs, outputs, and operational economics.
tags:
  - reactions
  - moon-materials
  - tech-ii
  - tech-iii
  - boosters
sources:
  - id: ccp-reactions
    resource: https://support.eveonline.com/hc/en-us/articles/115005405785-Reactions
    title: Reactions | EVE Online Support (updated 2024-08-29)
  - id: ccp-upwell-structures
    resource: https://support.eveonline.com/hc/en-us/articles/213021829-Upwell-Structures
    title: Upwell Structures | EVE Online Support (updated 2024-07-15)
  - id: ccp-service-modules
    resource: https://support.eveonline.com/hc/en-us/articles/207574929-Service-Modules
    title: Service Modules | EVE Online Support (updated 2024-08-29)
  - id: ccp-activities-jobs
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: eveuni-reactions
    resource: https://wiki.eveuniversity.org/Reactions
    title: Reactions | EVE University Wiki (last modified 2025-06-22)
  - id: eveuni-manufacturing
    resource: https://wiki.eveuniversity.org/Manufacturing
    title: Manufacturing | EVE University Wiki (last modified 2026-10-09)
  - id: eve-reactions-calculator-method
    resource: https://reactions.coalition.space/about
    title: EVE Reactions Calculator methodology
  - id: eve-omnitool-reactions
    resource: https://eve-omnitool.com/industry/manufacturing/reactions
    title: Reactions Calculator | EVE Omnitool
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:25:24Z
status: draft
---

## Summary

A reaction is an industrial job that transforms inputs into reaction products using a Reaction Formula. Reaction Formulas resemble blueprints but cannot be researched, copied, or invented. Reactions are a distinct **Reaction** job type, separate from Manufacturing and Science. [^ccp-reactions] [^ccp-activities-jobs]

Reactions supply intermediate materials for several production chains:

- **Tech II:** composite reactions convert raw moon materials into intermediate and composite materials used directly or in Advanced Component manufacturing.
- **Tech III:** hybrid reactions convert wormhole Fullerite gases into Hybrid Polymers used for Hybrid Tech Components.
- **Boosters and biochemical products:** biochemical reactions convert known-space gas and other inputs into booster materials and specified biochemical products.
- **Newer molecular-forged products:** CCP's Reactions article also identifies molecular-forged industrial materials such as Neurolink Enhancers, Neurolink Stabilizers, and Isotropic materials.

The reaction formula, compatible reactor, input materials, fuel type, and facility bonuses must match the intended reaction family. A Refinery that can perform one reaction family is not necessarily fitted to perform another. [^ccp-reactions] [^eveuni-reactions]

## Reactor families and facility restrictions

Reactions can only be performed in an Upwell Refinery with the compatible reactor service module fitted and online. CCP states that reactors can only be installed in systems with a security rating of 0.4 or lower. [^ccp-reactions]

| Reactor family | Main reaction inputs | Main outputs / use |
|---|---|---|
| Standup Composite Reactor | Raw moon materials and intermediate composite materials | Intermediate and composite materials for Tech II production |
| Standup Hybrid Reactor | Fullerite gases from wormhole space, fuel blocks, and minerals | Hybrid Polymers for Tech III components |
| Standup Biochemical Reactor | Cytoserocin and Mykoserocin gases, specified Fullerite gases, fuel blocks, and other commodities | Booster materials and specified biochemical/molecular-forged industrial products |

The Industry facility browser's Reactions column and the selected formula's activity eligibility should be used to identify a compatible facility. Structures may be configured for only one reactor family or may have bonuses for only one family. The family name in the formula must match the service the Refinery can run. [^eveuni-reactions]

### Structure role and rig effects

- The Tatara has a 25% reaction-time role bonus; the Athanor does not have the same reaction-time role bonus. See [Facilities and Rigs](../01-foundations/facilities-and-rigs.md).
- Reaction rigs are specific to the reactor family. A Composite Reactor rig does not improve Hybrid or Biochemical reactions.
- The EVE Reactions Calculator documents its reaction rig method as 2% material reduction for T1 and 2.4% for T2 Reactor Efficiency rigs; time rigs as 20% for T1 and 24% for T2; and a 1.1 security modifier in null-security and wormhole space versus 1.0 in low-security space. These are secondary calculator values and must be checked against the current fitted rig and in-game job quote. [^eve-reactions-calculator-method]
- The system cost index for Reactions is associated with reaction work in the system. EVE University notes that the Reactions SCI is not calculated separately by reaction family. [^eveuni-reactions]

## Reaction job setup and lifecycle

1. Select the correct Reaction Formula.
2. Choose the number of runs.
3. Select input and output locations.
4. Select the appropriate corporation wallet, where applicable.
5. Confirm the refinery has the compatible reactor online and is accessible.
6. Review the required materials, fuel blocks, duration, and installation fee.
7. Install the job and monitor it in the Jobs section.
8. Deliver the completed job and inspect the output.

The job is independent from Manufacturing and Science job pools. Reaction slot capacity is controlled by Mass Reactions and Advanced Mass Reactions. The Reactions skill reduces reaction time by 4% per skill level; Remote Reactions allows remote job start/delivery at five jumps per level, up to 25 jumps at V. See [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md). [^ccp-activities-jobs] [^eveuni-reactions]

Hybrid and composite reaction formulas are seeded on the NPC market. Biochemical reaction formula acquisition is different: EVE University's reference describes certain biochemical formulas as exploration-site drops rather than ordinary seeded market items. Check the exact formula before assuming how it is acquired. [^eveuni-reactions]

## Tech II composite reaction chain

The common Tech II moon-material path has four stages:

```text
Moon Ore
   ↓ Reprocessing
Raw Moon Materials
   ↓ Intermediate Composite Reactions
Intermediate Composite Materials
   ↓ Composite Reactions
Composite Materials
   ↓ Manufacturing
Advanced Components
   ↓ Manufacturing with Tech II BPC
Tech II Product
```

Some composite materials are used directly in final Tech II jobs, not only in Advanced Components. The final product blueprint's Manufacturing Bill of Materials is authoritative for whether it requires a component, a direct composite material, or both. [^eveuni-manufacturing] [^eveuni-reactions]

### Intermediate composite reactions

A typical intermediate recipe consumes 100 units of each of two raw moon-material inputs and five appropriate fuel blocks, producing 200 units of intermediate material. The table below is transcribed from the EVE University reaction reference. Treat the specific Reaction Formula in game as the final authority for inputs and outputs. [^eveuni-reactions]

| Intermediate material | Fuel block | Raw input 1 | Raw input 2 | Output |
|---|---|---|---|---:|
| Caesarium Cadmide | Oxygen | Cadmium | Caesium | 200 |
| Carbon Fiber | Helium | Hydrocarbons | Evaporite Deposits | 200 |
| Carbon Polymers | Helium | Hydrocarbons | Silicates | 200 |
| Ceramic Powder | Hydrogen | Evaporite Deposits | Silicates | 200 |
| Crystallite Alloy | Helium | Cobalt | Cadmium | 200 |
| Dysporite | Helium | Mercury | Dysprosium | 200 |
| Fernite Alloy | Hydrogen | Scandium | Vanadium | 200 |
| Ferrofluid | Hydrogen | Hafnium | Dysprosium | 200 |
| Fluxed Condensates | Oxygen | Neodymium | Thulium | 200 |
| Hexite | Nitrogen | Chromium | Platinum | 200 |
| Hyperflurite | Nitrogen | Vanadium | Promethium | 200 |
| Neo Mercurite | Helium | Mercury | Neodymium | 200 |
| Platinum Technite | Nitrogen | Platinum | Technetium | 200 |
| Promethium Mercurite | Helium | Mercury | Promethium | 200 |
| Prometium | Oxygen | Cadmium | Prometium | 200 |
| Rolled Tungsten Alloy | Nitrogen | Tungsten | Platinum | 200 |
| Silicon Diborite | Oxygen | Evaporite Deposits | Silicates | 200 |
| Solerium | Oxygen | Chromium | Caesium | 200 |
| Sulfuric Acid | Nitrogen | Atmospheric Gases | Evaporite Deposits | 200 |
| Thermosetting Polymer | Oxygen | Atmospheric Gases | Silicates | 200 |
| Thulium Hafnite | Hydrogen | Hafnium | Thulium | 200 |
| Titanium Chromide | Oxygen | Chromium | Titanium | 200 |
| Vanadium Hafnite | Hydrogen | Vanadium | Hafnium | 200 |

**Special intermediate:** Oxy-Organic Solvents is documented as an exception to the normal 100 + 100 input pattern. The EVE University table gives 2,000 Atmospheric Gases and 2,000 Hydrocarbons with five Oxygen Fuel Blocks for 10 units of output. [^eveuni-reactions]

### Composite reactions

Composite reactions combine intermediate materials into composite materials. The standard pattern is 100 units of each listed input plus five fuel blocks, but output quantity and the number of inputs vary by formula. Some composites require three or four intermediate materials. [^eveuni-reactions]

| Composite material | Output | Fuel block | Input intermediates |
|---|---:|---|---|
| Crystalline Carbonide | 10,000 | Helium | Crystallite Alloy + Carbon Polymers |
| Fermionic Condensates | 200 | Helium | Caesarium Cadmide + Dysporite + Fluxed Condensates + Prometium |
| Fernite Carbide | 10,000 | Hydrogen | Fernite Alloy + Ceramic Powder |
| Ferrogel | 400 | Hydrogen | Hexite + Hyperflurite + Ferrofluid + Prometium |
| Fullerides | 3,000 | Nitrogen | Carbon Polymers + Platinum Technite |
| Hypersynaptic Fibers | 750 | Oxygen | Vanadium Hafnite + Solerium + Dysporite |
| Nanotransistors | 1,500 | Nitrogen | Sulfuric Acid + Platinum Technite + Neo Mercurite |
| Nonlinear Metamaterials | 300 | Nitrogen | Titanium Chromide + Ferrofluid |
| Phenolic Composites | 2,200 | Oxygen | Silicon Diborite + Caesarium Cadmide + Vanadium Hafnite |
| Photonic Metamaterials | 300 | Oxygen | Crystallite Alloy + Thulium Hafnite |
| Plasmonic Metamaterials | 300 | Hydrogen | Fernite Alloy + Neo Mercurite |
| Sylramic Fibers | 6,000 | Helium | Ceramic Powder + Hexite |
| Terahertz Metamaterials | 300 | Helium | Rolled Tungsten Alloy + Promethium Mercurite |
| Titanium Carbide | 10,000 | Oxygen | Titanium Chromide + Silicon Diborite |
| Tungsten Carbide | 10,000 | Nitrogen | Rolled Tungsten Alloy + Sulfuric Acid |

The table reports outputs and required inputs, not a substitute for checking the formula's current in-game quantity fields. In particular, some reactions have multiple inputs and different material outputs. [^eveuni-reactions]

### Special composite reactions

Two additional formulas documented by EVE University use 200 units of each of two intermediate materials plus Oxy-Organic Solvents and do not require fuel blocks. Each produces 200 units of output:

| Composite | Input 1 | Input 2 | Special input | Output |
|---|---|---|---|---:|
| Pressurized Oxidizer | Carbon Polymers | Sulfuric Acid | Oxy-Organic Solvents | 200 |
| Reinforced Carbon Fiber | Carbon Fiber | Thermosetting Polymer | Oxy-Organic Solvents | 200 |

Verify the actual per-run formula in the Industry interface before creating a reaction batch. [^eveuni-reactions]

## Hybrid reactions and the Tech III chain

Hybrid reactions use Fullerite gases harvested from wormhole gas sites to produce Hybrid Polymers. The polymers become inputs to Hybrid Tech Components used for Tech III ships and subsystems. Hybrid formulas also require the matching Fuel Block type and specified minerals. [^ccp-reactions] [^eveuni-reactions]

Hybrid reactions are a separate supply chain from moon-material composite reactions. Do not substitute Composite Reactor rigs, intermediate materials, or fuel-block assumptions from the Tech II chain into Hybrid reaction models.

## Biochemical and molecular-forged reactions

Biochemical reactions use Cytoserocin and Mykoserocin gases harvested in known space to create booster-related materials. Some formulas require additional commodities and fuel blocks. The resulting pure booster materials are later used in Manufacturing jobs for final boosters. [^ccp-reactions] [^eveuni-reactions]

CCP's official support article also describes the Biochemical Reactor family as supporting specified Neurolink Enhancers, Neurolink Stabilizers, and Isotropic materials. The EVE University reaction reference groups the newer formula families under Molecular-Forged reactions, with inputs spanning known-space gases or wormhole Fullerites, fuel blocks, and special commodities. These are distinct recipes and should be represented individually in the recipe data rather than being treated as one generic biochemical formula. [^ccp-reactions] [^eveuni-reactions]

## Reaction economics

A reaction's economic contribution is not the selling price of its output minus the ISK paid at the moment the inputs entered a hangar. A complete evaluation should value:

- Raw inputs at market replacement cost or opportunity cost.
- Fuel blocks consumed by the formula.
- Reaction job installation fee, including activity SCI and applicable facility/rig terms.
- Reaction job time and the character's Reaction slot opportunity cost.
- Hauling and asset exposure between raw material sources, refineries, and component manufacturing facilities.
- The output's executable sale value and realistic market depth.

A reaction-only operation may buy raw moon materials, run reactions, and sell the intermediate or composite outputs. The relevant comparison is the net value of the processed output against the value of the raw input materials and all conversion costs. [^eveuni-reactions]

Use the current Industry quote for the exact formula, system, refinery, clone state, and online reactor. The fee model and live inputs are described in [Installation Cost Computation](../09-computations/installation-costs.md). The reaction formula should be costed by its actual input/output quantities and not by a generic assumption that all reactions use the same batch size.

## Formula data and maintenance policy

Reaction recipes change independently of explanatory prose. A future structured recipe catalog should store:

- Reaction Formula type ID and name.
- Reactor family.
- Input type IDs and quantities per run.
- Fuel block type and quantity.
- Output type ID and quantity.
- Formula family (composite, hybrid, biochemical, or molecular-forged).
- SDE build/version and retrieval timestamp.
- Source and verification status.

The tables above are a readable baseline for the Tech II moon-material chain. They are not a substitute for versioned SDE data and in-game verification. Detailed moon ore sourcing and reprocessing data belongs in [Moon Materials](../03-materials-and-sourcing/moon-materials.md); Advanced Component build recipes belong in [Tech II Components](tech-2-components.md).

## Limitations and unresolved verification

- EVE University's Reactions article is last modified 2025-06-22. Its tables need comparison with the current SDE and in-game formulas before they are used to drive an unattended calculator.
- The reaction family and reactor compatibility rules are supported by CCP, but the full recipe list and yield quantities in this document are from a community reference.
- Reaction rig percentages are cited from a third-party calculator's methodology. Verify the exact current rig and security modifier in game.
- No live in-game reaction quote or controlled batch verification was performed in this research pass.
- The current formula availability and acquisition routes for all Biochemical and Molecular-Forged formulas need item-level verification.

## Related concepts

- [Tech II Components](tech-2-components.md)
- [Facilities and Rigs](../01-foundations/facilities-and-rigs.md)
- [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md)
- [Moon Materials](../03-materials-and-sourcing/moon-materials.md)
- [Gas and Fullerites](../03-materials-and-sourcing/gas-and-fullerites.md)
- [Installation Cost Computation](../09-computations/installation-costs.md)
- [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md)

[^ccp-reactions]: CCP Support, Reactions (updated 2024-08-29).
[^ccp-upwell-structures]: CCP Support, Upwell Structures (updated 2024-07-15).
[^ccp-service-modules]: CCP Support, Service Modules (updated 2024-08-29).
[^ccp-activities-jobs]: CCP Support, Activities and Job Types (updated 2024-08-29).
[^eveuni-reactions]: EVE University Wiki, Reactions (last modified 2025-06-22).
[^eveuni-manufacturing]: EVE University Wiki, Manufacturing (last modified 2026-10-09).
[^eve-reactions-calculator-method]: EVE Reactions Calculator, methodology.
[^eve-omnitool-reactions]: EVE Omnitool, Reactions Calculator.
