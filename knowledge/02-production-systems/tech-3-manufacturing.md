---
type: Concept
title: Tech III Manufacturing
description: Tech III hull and subsystem production, including Hybrid Polymer reactions, Hybrid Tech Components, Ancient Relic reverse engineering, and final manufacturing.
tags:
  - tech-iii
  - manufacturing
  - reverse-engineering
  - wormhole
  - sleeper-salvage
  - reactions
sources:
  - id: ccp-ancient-relics
    resource: https://support.eveonline.com/hc/en-us/articles/203210662-Ancient-Relics
    title: Ancient Relics | EVE Online Support (updated 2024-08-29)
  - id: ccp-blueprints
    resource: https://support.eveonline.com/hc/en-us/articles/203269951-Blueprints
    title: Blueprints | EVE Online Support (updated 2024-08-29)
  - id: ccp-invention
    resource: https://support.eveonline.com/hc/en-us/articles/203210642-Invention
    title: Invention | EVE Online Support (updated 2024-08-29)
  - id: ccp-datacores
    resource: https://support.eveonline.com/hc/en-us/articles/203210652-Datacores
    title: Datacores | EVE Online Support (updated 2024-08-29)
  - id: ccp-reactions
    resource: https://support.eveonline.com/hc/en-us/articles/115005405785-Reactions
    title: Reactions | EVE Online Support (updated 2024-08-29)
  - id: eveuni-tech3
    resource: https://wiki.eveuniversity.org/Tech_3_Production
    title: Tech 3 Production | EVE University Wiki (last modified 2024-09-22)
  - id: eveuni-science-skills
    resource: https://wiki.eveuniversity.org/Skills:Science
    title: Skills:Science | EVE University Wiki
  - id: everef-small-wrecked-hull
    resource: https://everef.net/types/34416
    title: Small Wrecked Hull Section | EVE Ref (SDE-derived)
  - id: everef-small-malfunctioning-hull
    resource: https://everef.net/types/34414
    title: Small Malfunctioning Hull Section | EVE Ref (SDE-derived)
  - id: eve-academy-tech3
    resource: https://www.eveonline.com/eve-academy/careers/industrialist/tech-3-production
    title: Tech 3 Production | EVE Academy
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:30:00Z
status: draft
---

## Summary

Tech III production is a linked industrial chain that converts wormhole resources and Sleeper-derived materials into Tactical Destroyers, Strategic Cruisers, and their subsystems. It combines four distinct operations:

1. **Hybrid Polymer reactions:** Fullerite gases and other inputs are reacted in a Refinery.
2. **Hybrid Tech Component manufacturing:** Hybrid Polymers and Ancient Salvage are manufactured into intermediate components.
3. **Reverse engineering:** Ancient Relics and datacores are consumed in a Science job to attempt to produce a limited-run Tech III BPC.
4. **Final manufacturing:** A Tech III BPC and the required Hybrid Tech Components are used to manufacture the hull or subsystem.

These stages are separate jobs, often performed at different facilities and in different locations. Treat the chain as a supply network, not as one manufacturing activity. [^eveuni-tech3] [^ccp-ancient-relics] [^ccp-reactions]

## Product architecture

There are two product branches:

- **Tactical Destroyers:** a Small Hull Section relic produces a Tactical Destroyer BPC. Tactical Destroyers do not require separately manufactured subsystems.
- **Strategic Cruisers:** a Hull Section relic produces a Strategic Cruiser hull BPC. The four subsystem families are invented and manufactured separately: Core, Defensive, Offensive, and Propulsion.

CCP maps relic families to output categories as follows. [^ccp-ancient-relics]

| Ancient Relic family | Reverse-engineering output |
|---|---|
| Small Hull Section | Tactical Destroyer hull BPC |
| Hull Section | Strategic Cruiser hull BPC |
| Power Cores | Core / Engineering subsystem BPC |
| Armor Nanobot | Defensive subsystem BPC |
| Weapon Subroutines | Offensive subsystem BPC |
| Thruster Sections | Propulsion subsystem BPC |

A complete Strategic Cruiser production plan therefore needs a hull BPC plus one BPC for each of the four subsystem categories, as well as the corresponding components and other manufacturing inputs. Tactical Destroyer production does not include the four-subsystem branch. [^eveuni-tech3]

## Stage 1: Hybrid Polymer reactions

Hybrid Polymers are produced by reacting Fullerite gas inputs with the required reaction materials. Fullerite gases are associated with wormhole-space gas harvesting. The resulting Hybrid Polymers are inputs to Hybrid Tech Component manufacturing. [^eveuni-tech3]

The reaction stage requires a Refinery in a system where reactions are permitted, an online Standup Hybrid Reactor service module, a Hybrid Polymer reaction formula, formula-specific inputs and fuel blocks, and an available Reaction job slot. CCP states that reaction reactors can only be installed in Refineries located in systems with a security rating of 0.4 or lower. The Standup Hybrid Reactor is distinct from the Standup Composite Reactor used for moon-material reactions. [^ccp-reactions] [^eveuni-tech3]

The Tatara has a 25% reaction-time role bonus compared with the Athanor. Reaction rigs can further affect Hybrid Reaction material usage and time, but are family-specific. See [Facilities and Rigs](../01-foundations/facilities-and-rigs.md) and [Reactions](reactions.md). [^eveuni-tech3]

Do not use a reaction formula's market name or output family as a substitute for checking its actual input recipe. The full set of Hybrid Polymer formulas belongs in the reaction recipe dataset and must be reconciled against current static data and in-game formula windows.

## Stage 2: Hybrid Tech Component manufacturing

Hybrid Tech Components are intermediate components used in final Tech III hull and subsystem manufacturing. Their inputs are drawn from two broad categories: [^eveuni-tech3]

- **Hybrid Polymers:** produced by Stage 1 reactions or purchased from the market.
- **Ancient Salvage:** recovered by salvaging Sleeper wrecks in wormhole space or purchased from the market.

Hybrid Tech Component BPOs can be researched and copied like other BPOs. Manufacturing uses the normal Industry workflow and a facility with the required manufacturing service. EVE University lists the following general skill requirements for Hybrid Tech Component BPOs: Industry V, Electromagnetic Physics II, and one additional field or racial engineering skill at II, as specified by the particular component blueprint. The additional skill differs among component blueprints. The actual BPO's required-skills and bill-of-materials panels are the operational authority. [^eveuni-tech3]

Advanced Component Manufacturing rigs can improve eligible Hybrid Tech Component manufacturing. The exact rig must match the facility size and component activity. Structure role bonuses and character manufacturing skills also apply where the job quote indicates. See [Facilities and Rigs](../01-foundations/facilities-and-rigs.md). [^eveuni-tech3]

## Stage 3: Reverse engineering Ancient Relics

Reverse engineering consumes an Ancient Relic to attempt to create a limited-run Tech III BPC. It is a Science job. CCP's blueprint taxonomy identifies Ancient Relics as the source for Tech III hull and subsystem invention; relics are not BPOs and cannot be researched or copied as ordinary blueprint originals. [^ccp-blueprints] [^ccp-invention]

### Relic family and output mapping

| Ancient Relic family | Result |
|---|---|
| Small Hull Section | Tactical Destroyer hull |
| Hull Section | Strategic Cruiser hull |
| Power Cores | Core / Engineering subsystem |
| Armor Nanobot | Defensive subsystem |
| Weapon Subroutines | Offensive subsystem |
| Thruster Sections | Propulsion subsystem |

### Relic quality, output runs, and published base chance

CCP's Ancient Relics support page gives the following quality table: [^ccp-ancient-relics]

| Relic quality | Licensed runs on successful BPC | CCP-published base success chance |
|---|---:|---:|
| Intact | 20 | 40% |
| Malfunctioning | 10 | 35% |
| Wrecked | 3 | 25% |

The relic's family determines the possible output category; its quality determines the licensed runs and the published base chance.

### Important conflict: CCP support article versus SDE-derived output probabilities

The EVE University Tech 3 Production page, last modified 2024-09-22, lists 26%, 21%, and 14% as the Intact, Malfunctioning, and Wrecked base chances. EVE Ref's current SDE-derived item pages also show 21% and 14% as the per-output probabilities for Small Malfunctioning and Small Wrecked Hull Sections. These conflict with CCP's support article, updated 2024-08-29, which lists 40%, 35%, and 25%. [^ccp-ancient-relics] [^eveuni-tech3] [^everef-small-malfunctioning-hull] [^everef-small-wrecked-hull]

Do not silently reconcile these values or use the older community figures in an expected-value model. The SDE item pages may be displaying a probability per possible output rather than the total job success probability, but that interpretation has not been established here. Record the success chance shown by the live Industry window for each relic family and quality, and compare it with the SDE output probabilities before publishing a final formula.

### Inputs and skill requirements

CCP states that reverse-engineering jobs require the datacores listed by the relic's bill of materials. The required datacores correspond to the relevant science fields. Datacores are consumed regardless of job success. The relic itself is also consumed by the job. [^ccp-datacores] [^ccp-invention]

EVE University identifies Sleeper Encryption Methods as the common skill for Ancient Relic reverse engineering, with additional relic-specific science skills. The relic's own required-skills panel identifies the exact requirements for that particular output family. Examples of relevant fields include Mechanical Engineering, Plasma Physics, Quantum Physics, Hydromagnetic Physics, Rocket Science, and subsystem technology skills. Treat the relic's in-game required-skills panel as authoritative if a community skill table conflicts with it. [^eveuni-tech3] [^eveuni-science-skills]

### Job behavior and expected output

A reverse-engineering attempt is a probabilistic Science job. A failed attempt produces no BPC, but the consumed relic and datacores are not returned. [^ccp-invention] [^ccp-datacores]

The Industry interface displays the current success chance. Because the published support and SDE-derived probabilities conflict, this document does not provide a success formula. Record the displayed chance and exact input set when testing.

A first-pass expected-attempt model can be written without assuming a particular probability formula:

```text
Expected attempts per successful BPC = 1 / p

Expected relic and datacore cost per successful BPC
  = (relic cost + required datacore cost + optional input cost) / p
```

Here, p is the actual success probability displayed by the Industry UI for the selected relic, character, facility, and optional inputs. This is an expected-value model, not a guarantee that a specific number of attempts will produce a success.

## Stage 4: Final hull and subsystem manufacturing

The invented BPC is used in a normal Manufacturing job. The required inputs include the relevant Hybrid Tech Components and any additional items listed on that specific blueprint. Tech III hulls also require R.A.M.- Starship Tech according to the EVE University production reference; do not assume this item is required for every subsystem blueprint. [^eveuni-tech3]

EVE University's production reference lists these construction requirements: [^eveuni-tech3]

| Product | Key listed skill requirements |
|---|---|
| Tactical Destroyer hull | Industry V; Mechanical Engineering IV; Advanced Small Ship Construction V; relevant racial Starship Engineering V |
| Strategic Cruiser hull | Industry V; Mechanical Engineering IV; Advanced Medium Ship Construction V; relevant racial Starship Engineering V |
| Strategic Cruiser subsystem | Industry IV; Mechanical Engineering IV; Advanced Medium Ship Construction IV; relevant racial Starship Engineering IV; corresponding Core, Defensive, Offensive, or Propulsion Subsystem Technology I; Jury Rigging V |

The relevant racial Starship Engineering skill is determined by the hull or subsystem blueprint. Confirm exact prerequisites on the blueprint itself before planning a character skill queue.

The production reference identifies Advanced Small Ship Manufacturing rigs for Tactical Destroyers, Advanced Medium Ship Manufacturing rigs for Strategic Cruiser hulls, and Advanced Component Manufacturing rigs for subsystems. Rig applicability is item-group-specific. [^eveuni-tech3]

Final hull and subsystem production is separate from the component stage. A Strategic Cruiser is not complete merely because its hull BPC and hull manufacturing inputs are available; the four subsystem products must also be built or acquired for a fully assembled ship.

## Resource sourcing and logistics

| Input | Primary source described by references | Industrial role |
|---|---|---|
| Fullerite gases | Wormhole gas sites | Hybrid Polymer reactions |
| Ancient Salvage | Salvaging Sleeper wrecks in wormhole space | Hybrid Tech Components |
| Ancient Relics | Wormhole relic exploration sites; some special Sleeper-site containers | Reverse engineering |
| T3 subsystem datacores | Sleeper data sites | Reverse engineering |
| Standard datacores | Market, Factional Warfare LP stores, R&D agents, and data sites | Reverse engineering inputs |
| Fuel blocks and minerals | Market or player production | Reaction inputs |
| Hybrid Polymers | Player reactions or market | Hybrid Tech Components |

CCP's Datacores article confirms that reverse-engineering datacores are specified by the relic and its required fields. EVE University documents wormhole exploration and Sleeper salvage as major sourcing routes. [^ccp-datacores] [^eveuni-tech3]

T3 production is logistics-intensive because the chain combines wormhole-origin materials, reaction facilities, component manufacturing, and Science jobs. A vertically integrated producer must decide whether to harvest, react, salvage, invent, and manufacture internally or buy selected intermediates. This is a make-or-buy decision at each stage, not necessarily an all-or-nothing choice.

## Operational planning model

Model each stage independently and then connect the outputs:

1. **Reaction plan:** reaction formula, gas/mineral/fuel inputs, reaction rig, Refinery, system cost index, tax, and expected output.
2. **Component plan:** Hybrid Tech Component recipes, Ancient Salvage, Polymer requirements, BPO ME/TE, manufacturing rig, and component job slots.
3. **Reverse-engineering plan:** relic family/quality, datacores, optional inputs, current displayed success chance, Science slots, and expected BPC runs.
4. **Final manufacturing plan:** hull/subsystem BPC runs, component stock, R.A.M. requirements where applicable, character skills, manufacturing rig, and final facility.
5. **Logistics plan:** transport volume, wormhole route risk, input staging, output staging, and the value of buying intermediates instead of moving them.

For a successful BPC with r licensed runs, the maximum output from that copy is r manufacturing runs. Actual output quantity per manufacturing run is determined by the blueprint. Keep BPC licensed runs, manufacturing job runs, and units produced as separate quantities.

## Related concepts

- [Reactions](reactions.md)
- [Tech II Components](tech-2-components.md)
- [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md)
- [Facilities and Rigs](../01-foundations/facilities-and-rigs.md)
- [Sleeper Salvage](../03-materials-and-sourcing/sleeper-salvage.md)
- [Gas and Fullerites](../03-materials-and-sourcing/gas-and-fullerites.md)
- [Blueprints and Research](../01-foundations/blueprints-and-research.md)
- [Tech II Invention](tech-2-invention.md)

## Open verification tasks

- Reconcile CCP's 40%/35%/25% Ancient Relic base chances with SDE per-output probabilities and live Industry-window results.
- Record live Industry-window success chances for each relic family and quality with fixed skill and facility conditions.
- Determine the exact effect of Sleeper Encryption Methods and relic-specific science skills on reverse-engineering chance.
- Determine whether and how optional decryptors modify Tech III reverse-engineering chance, output runs, ME, and TE. Do not assume the Tech II decryptor table applies.
- Build a current SDE-derived recipe and required-skill matrix for all Hybrid Tech Components.
- Verify whether R.A.M.- Starship Tech is required for all current T3 hull blueprints and confirm precise quantities by blueprint.
- Verify final manufacturing facility restrictions and rig applicability for each T3 hull and subsystem group.
- Build a representative full-chain cost model with live market prices, facility quotes, and material rounding.

## Sources and notes

CCP's support pages are primary evidence for relic mapping, licensed runs, published base chances, consumed inputs, and datacore requirements. EVE University provides a useful production-chain and skill overview but contains a base-chance table that conflicts with CCP's support page. EVE Ref exposes item-level SDE data and also shows different per-output probabilities for sampled relics. The conflict is explicitly unresolved rather than silently choosing one value.

[^ccp-ancient-relics]: CCP Support, Ancient Relics (updated 2024-08-29).
[^ccp-blueprints]: CCP Support, Blueprints (updated 2024-08-29).
[^ccp-invention]: CCP Support, Invention (updated 2024-08-29).
[^ccp-datacores]: CCP Support, Datacores (updated 2024-08-29).
[^ccp-reactions]: CCP Support, Reactions (updated 2024-08-29).
[^eveuni-tech3]: EVE University Wiki, Tech 3 Production (last modified 2024-09-22).
[^eveuni-science-skills]: EVE University Wiki, Skills:Science (accessed 2026-11-14).
[^everef-small-wrecked-hull]: EVE Ref, Small Wrecked Hull Section (SDE-derived item attributes; accessed 2026-11-14).
[^everef-small-malfunctioning-hull]: EVE Ref, Small Malfunctioning Hull Section (SDE-derived item attributes; accessed 2026-11-14).
