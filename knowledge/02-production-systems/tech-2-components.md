---
type: Concept
title: Tech II Components
description: Advanced component supply chain for Tech II manufacturing, including moon-material acquisition, composite reactions, component construction, and cost/skill dependencies.
tags:
  - tech-ii
  - components
  - moon-materials
  - reactions
  - manufacturing
sources:
  - id: ccp-manufacturing
    resource: https://support.eveonline.com/hc/en-us/articles/203210292-Manufacturing
    title: Manufacturing | EVE Online Support (updated 2024-08-29)
  - id: ccp-reactions
    resource: https://support.eveonline.com/hc/en-us/articles/115005405785-Reactions
    title: Reactions | EVE Online Support (updated 2024-08-29)
  - id: ccp-blueprints
    resource: https://support.eveonline.com/hc/en-us/articles/203269951-Blueprints
    title: Blueprints | EVE Online Support (updated 2024-08-29)
  - id: ccp-invention
    resource: https://support.eveonline.com/hc/en-us/articles/203210642-Invention
    title: Invention | EVE Online Support (updated 2024-08-29)
  - id: ccp-ram-reform
    resource: https://www.eveonline.com/news/view/building-better-worlds
    title: Building Better Worlds | EVE Online (2014-04-24)
  - id: eveuni-manufacturing
    resource: https://wiki.eveuniversity.org/Manufacturing
    title: Manufacturing | EVE University Wiki (last modified 2026-10-09)
  - id: eveuni-reactions
    resource: https://wiki.eveuniversity.org/Reactions
    title: Reactions | EVE University Wiki (last modified 2025-06-22)
  - id: eveuni-invention
    resource: https://wiki.eveuniversity.org/Invention
    title: Invention | EVE University Wiki (last modified 2026-10-09)
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:25:24Z
status: draft
---

## Summary

Tech II manufacturing extends the manufacturing process with item-specific materials, skills, and supply-chain dependencies. Many Tech II blueprints require a Tech I base item, Advanced Components, Morphite, planetary commodities, Robotic Assembly Modules (R.A.M.), or other inputs. Not every Tech II item requires every category. The selected Tech II blueprint's Manufacturing Bill of Materials in the Industry window is the authoritative recipe for that item. [^eveuni-manufacturing] [^ccp-manufacturing]

Advanced Components are an important shared supply-chain input. They are manufactured from materials produced through composite reactions, which begin with raw moon materials. Other Tech II inputs may be sourced independently or produced through separate chains. The Tech II BPC itself is normally obtained through invention from a Tech I BPC, or purchased from another industrialist; a small number of legacy Tech II BPOs remain in circulation. [^ccp-invention] [^ccp-blueprints] [^eveuni-manufacturing]

This document focuses on the Advanced Component chain and its relationship to final Tech II manufacturing. It does not attempt to enumerate every Tech II product recipe or reproduce the complete reaction database.

## High-level production chain

```text
Raw Moon Ore
    ↓ Reprocess
Raw Moon Materials
    ↓ Intermediate Composite Reactions
Intermediate Composite Materials
    ↓ Composite Reactions
Advanced / Composite Materials
    ↓ Manufacturing from component blueprint
Advanced Components
    ↓
Tech II Manufacturing
    ↑
Tech II BPC + item-specific materials
```

The reaction stages are carried out in a Refinery with the compatible Composite Reactor service online. Advanced Components are then manufactured through the normal Manufacturing activity using their own blueprints and the required composite materials. [^ccp-reactions] [^eveuni-reactions]

The chain is not a single mandatory path for every component. Each component blueprint defines its required composite inputs and other bill-of-material details. Some composite materials are used directly in final Tech II manufacturing as well as in Advanced Component production. [^eveuni-manufacturing] [^eveuni-reactions]

## Stage 1: Raw moon material supply

Raw moon materials originate from moon ore. A corporation or alliance may operate moon extraction through a Refinery fitted with a Moon Drill at an eligible moon-mining beacon, or a manufacturer can purchase raw moon materials from the market. Reprocessing moon ore yields raw moon materials and, in some cases, ordinary minerals. [^eveuni-manufacturing]

The decision to mine or buy raw moon materials is an economic and operational choice:

- **In-house extraction** provides supply control but requires structure investment, moon access, fuel, operational coverage, and defense of the extraction/refinery infrastructure.
- **Market procurement** avoids operating the extraction chain but exposes the manufacturer to market depth, regional price volatility, and hauling costs.
- **Buying reprocessed raw materials** separates moon extraction from reaction operations and can reduce the number of production activities the manufacturer must manage.

The economic model should value self-extracted or self-reprocessed inputs at replacement/opportunity cost, not automatically at zero because no ISK was paid to acquire them. See [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md).

Detailed moon distribution, ore reprocessing yields, security restrictions, extraction cycles, and moon composition belong in [Moon Materials](../03-materials-and-sourcing/moon-materials.md). This document does not assume that all moon materials can be sourced from the same region or moon.

## Stage 2: Intermediate composite reactions

Raw moon materials are combined into intermediate materials using composite reaction formulas. CCP states that reactions are conducted only in Refineries with the appropriate reactor installed and online; the Composite Reactor is the family used for moon-material reactions in the Tech II supply chain. Reactors can only be installed in systems with a security rating of 0.4 or lower. [^ccp-reactions]

The EVE University reaction reference describes a common intermediate reaction batch as producing 200 units of output from 100 units of each required input, plus five appropriate fuel blocks. There are item-specific exceptions, including Oxy-Organic Solvents, which uses a much larger input quantity and produces a smaller output batch. Treat the current reaction formula's Bill of Materials as the recipe authority rather than applying a blanket 100/200 rule to every formula. [^eveuni-reactions]

Intermediate materials include examples such as Caesarium Cadmide, Carbon Polymers, Ceramic Powder, Crystallite Alloy, Dysporite, Ferrofluid, Hexite, and other moon-derived compounds. The full current formula matrix is maintained in the [Reactions](../02-production-systems/reactions.md) concept and should be represented as structured recipe data rather than manually duplicated across every product document.

## Stage 3: Composite reactions

Intermediate materials are combined into composite materials using additional composite reaction formulas. The input and output quantities vary by formula. Some recipes use two intermediate inputs; others require three or four. The typical formula consumes five matching fuel blocks, but the special Pressurized Oxidizer and Reinforced Carbon Fiber reactions have their own input rules and do not use fuel blocks according to the EVE University reaction table. [^eveuni-reactions]

Composite materials include:
- Racial or commonly race-associated composites such as Crystalline Carbonide, Fernite Carbide, Titanium Carbide, and Tungsten Carbide.
- Shared composites such as Fermionic Condensates, Ferrogel, Fullerides, Hypersynaptic Fibers, Nanotransistors, Phenolic Composites, and Sylramic Fibers.
- Other specialized materials used by selected component and item recipes.

Do not infer a component's material requirements solely from its race. The actual component blueprint determines whether it uses one or several composite materials, and some materials are shared across racial production lines. [^eveuni-reactions]

## Stage 4: Advanced Component manufacturing

Advanced Components are manufactured in normal Manufacturing jobs using component blueprints. EVE University's Manufacturing reference describes these as the most common component category used in Tech II production, especially Tech II ships, which can require many different component types and substantial quantities. [^eveuni-manufacturing]

The component blueprint's Manufacturing activity lists:
- Required composite materials.
- Any other required materials.
- Required science or construction skills.
- Material Efficiency and Time Efficiency values, if available on the blueprint.
- Output quantity per run and base manufacturing time.

The relevant Science skill is component-specific. Check the component blueprint rather than assuming one universal component skill. The current skill and recipe mapping should be captured from the in-game blueprint/Industry interface or current SDE data before building a component matrix. [^eveuni-manufacturing]

Advanced Component jobs are Manufacturing jobs, not Reaction jobs. They consume Manufacturing capacity and use the normal Manufacturing service and facility-selection rules. The reaction steps that produce the input materials use Reaction jobs and the separate Reaction job pool. See [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md) and [Facilities and Rigs](../01-foundations/facilities-and-rigs.md). [^ccp-manufacturing] [^ccp-reactions]

## Stage 5: Final Tech II manufacturing

The final Tech II blueprint normally comes from invention. CCP describes invention as producing a limited-run Tech II BPC from an eligible Tech I BPC; a few legacy Tech II BPOs remain with their current owners, and no new Tech II BPOs are made available. [^ccp-blueprints] [^ccp-invention]

The final Tech II job's materials are product-specific. Common categories include:

| Input category | Typical source | Notes |
|---|---|---|
| Tech II BPC | Invention or purchase from another player | Required for most Tech II manufacture; output runs/ME/TE depend on invention result and decryptor |
| Matching Tech I item | Tech I manufacturing or market purchase | Required by many, but not all, Tech II blueprints |
| Advanced Components | Advanced Component BPO + composite materials | Common in Tech II modules and ships; exact component types are item-specific |
| Morphite | Market or mining/reprocessing supply chains | Used by many Tech II recipes; quantity varies |
| Planetary commodities | Planetary Industry or market | Some recipes include items such as Construction Blocks |
| R.A.M. | R.A.M. BPO or market | Consumed as an ordinary Manufacturing input; type is item-specific |
| Other materials | Market, harvesting, reprocessing, or other production | Check the exact blueprint Bill of Materials |

An example from EVE University's Manufacturing guide is a Tech II Nanofiber Internal Structure requiring a matching Tech I Nanofiber Internal Structure, R.A.M.-Armor/Hull Tech, Morphite, and planetary Construction Blocks. This is an example only, not a generic recipe for Tech II modules. [^eveuni-manufacturing]

### Required skills

Tech II manufacturing has more item-specific skill requirements than ordinary Tech I manufacturing. For non-ship Tech II products, the cited EVE University reference states that two advanced Science skills are generally required and that they are the same fields used for invention. The exact skills and levels vary by blueprint. [^eveuni-manufacturing] [^eveuni-invention]

Tech II ship manufacturing also has ship-focused skill requirements. The EVE University manufacturing reference lists Mechanical Engineering and the relevant racial Starship Engineering skill, plus the appropriate Advanced Ship Construction skill for the ship size/category. Blueprint-specific skill requirements take precedence over any generalized list. [^eveuni-manufacturing]

Many relevant Science skills also reduce manufacturing time per level, but the exact combination and its rounding must be based on the blueprint and the current skill rules. The current document does not attempt to provide a full skill table for every Tech II item.

## R.A.M. inputs

Robotic Assembly Modules are specialized Manufacturing materials used by some Tech II production jobs. They are not reusable tools that become damaged during each run under the current industry system.

CCP's 2014 *Building Better Worlds* dev blog explains the removal of the old damage-per-run mechanic: R.A.M. and R.Db requirements were converted into fixed material quantities, with the R.A.M. and R.Db blueprints' output quantities adjusted to preserve the intended loss ratio. The current model is therefore ordinary material consumption shown in the blueprint's Bill of Materials. [^ccp-ram-reform]

Use the exact R.A.M. type and required quantity shown for the selected job. Do not apply the historic damage percentage or assume that a partially damaged R.A.M. can be repaired and reused. The old damage-per-run system is historical context only.

## Sourcing and vertical-integration decisions

An industrialist does not need to own every stage of the chain. Each stage can be performed internally or sourced externally:

| Stage | In-house option | Procurement option |
|---|---|---|
| Raw moon materials | Own/participate in moon extraction and reprocessing | Buy raw moon materials or reprocessed outputs |
| Intermediate materials | Run composite reactions | Buy intermediate materials |
| Composite materials | Run composite reactions | Buy composite materials |
| Advanced Components | Manufacture component blueprints | Buy Advanced Components |
| Final Tech II item | Manufacture from a Tech II BPC | Buy the finished item |
| Tech II BPC | Invention from Tech I BPC | Buy BPC packs or rare legacy BPO output |

For each stage, compare the economic value of the inputs with the market value of the output, installation fees, fuel, hauling, job-slot opportunity cost, working capital, and risk. Producing a component internally is not automatically cheaper than buying it. A fully integrated chain can also tie up more capital and create longer inventory exposure than buying intermediate materials as needed.

A reasonable first profitability model should calculate the marginal cost of producing one Advanced Component from purchased composite inputs, then compare it with the market's executable acquisition price. Only after that comparison should the model decide whether to add reaction stages or moon extraction.

## Cost attribution

For a final Tech II item, preserve separate cost categories:

```text
Expected Tech II unit cost =
    expected invention cost per usable manufacturing run
  + Tech II manufacturing inputs
  + manufacturing installation fee
  + logistics and handling
  + attributable market/sales costs
```

If Advanced Components are manufactured internally, their cost basis must include their composite inputs, component manufacturing fee, and the chosen opportunity/replacement value of inputs. If composite inputs are made internally, include raw moon materials, fuel blocks, reaction job fees, reaction rig/facility effects, and logistics. Avoid counting a material's cost again at each stage if the downstream component valuation already includes the upstream cost.

Use [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md) for replacement cost, opportunity cost, acquisition cost, and realized accounting conventions. Use [Installation Cost Computation](../09-computations/installation-costs.md) for activity-specific installation fees.

## Data model requirements

A future component/Tech II recipe dataset should store each blueprint or reaction formula as a distinct recipe record with:

- Product type ID and name.
- Activity type (Manufacturing, Reaction, Invention, etc.).
- Blueprint/formula type ID.
- Runs per job and output quantity per run.
- Material input type IDs and base quantities per run.
- Required skills and levels.
- ME/TE eligibility and effects, where applicable.
- Required facility service and reactor family, where applicable.
- Applicable rig family and product-group constraints.
- Source version or SDE build identifier.
- Retrieval timestamp and verification status.

This structure will support recipe expansion from a finished Tech II product to Advanced Components, composite materials, intermediate reaction materials, and raw moon materials without hard-coding the same recipe in several concept files.

## Limitations and open verification work

- The Tech II item Bill of Materials is blueprint-specific; broad category statements are not enough for an exact build cost.
- The EVE University Manufacturing and Reactions pages are community-maintained references. Their content is useful for supply-chain structure and recipe context, but the in-game Industry UI and current SDE should be used to verify a particular item or reaction.
- Exact Advanced Component skill requirements and material rounding have not been captured as a type-by-type dataset.
- The document does not list every Intermediate and Composite reaction formula; the Reactions concept will own the detailed formula catalog.
- No production recipe has been independently tested in-game as part of this research pass.
- The 2014 CCP R.A.M. dev blog describes a historical system change; current R.A.M. consumption should still be checked against current blueprint bills of materials.

## Related concepts

- [Tech II Invention](tech-2-invention.md)
- [Blueprint Copying](blueprint-copying.md)
- [Tech I Manufacturing](tech-1-manufacturing.md)
- [Reactions](reactions.md)
- [Moon Materials](../03-materials-and-sourcing/moon-materials.md)
- [Facilities and Rigs](../01-foundations/facilities-and-rigs.md)
- [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md)
- [Installation Cost Computation](../09-computations/installation-costs.md)

[^ccp-manufacturing]: CCP Support, Manufacturing (updated 2024-08-29).
[^ccp-reactions]: CCP Support, Reactions (updated 2024-08-29).
[^ccp-blueprints]: CCP Support, Blueprints (updated 2024-08-29).
[^ccp-invention]: CCP Support, Invention (updated 2024-08-29).
[^ccp-ram-reform]: CCP, Building Better Worlds (2014-04-24), removal of the old R.A.M./R.Db damage-per-run mechanic and conversion to material requirements.
[^eveuni-manufacturing]: EVE University Wiki, Manufacturing (last modified 2026-10-09).
[^eveuni-reactions]: EVE University Wiki, Reactions (last modified 2025-06-22).
[^eveuni-invention]: EVE University Wiki, Invention (last modified 2026-10-09).
[^eveuni-ram]: EVE University Wiki, Robotic Assembly Modules.
