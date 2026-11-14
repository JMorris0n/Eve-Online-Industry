---
type: Concept
title: Facilities and Rigs
description: Industry-capable NPC and Upwell facilities, service modules, structure role bonuses, rig compatibility, and activity-specific facility selection.
tags:
  - facilities
  - structures
  - rigs
  - manufacturing
  - research
  - reactions
sources:
  - id: ccp-upwell-structures
    resource: https://support.eveonline.com/hc/en-us/articles/213021829-Upwell-Structures
    title: Upwell Structures | EVE Online Support (updated 2024-07-15)
  - id: ccp-service-modules
    resource: https://support.eveonline.com/hc/en-us/articles/207574929-Service-Modules
    title: Service Modules | EVE Online Support (updated 2024-08-29)
  - id: ccp-upwell-quickfacts
    resource: https://support.eveonline.com/hc/en-us/articles/209985225-Upwell-Structures-Quick-Facts
    title: Upwell Structures - Quick Facts | EVE Online Support (updated 2022-05-10)
  - id: ccp-reactions
    resource: https://support.eveonline.com/hc/en-us/articles/115005405785-Reactions
    title: Reactions | EVE Online Support (updated 2024-08-29)
  - id: eveuni-structure-browser
    resource: https://wiki.eveuniversity.org/Structure_Browser
    title: Upwell structure | EVE University Wiki
  - id: eveuni-upwell-fitting
    resource: https://wiki.eveuniversity.org/Fitting_upwell_structures
    title: Fitting upwell structures | EVE University Wiki (last modified 2025-07-19)
  - id: eveuni-manufacturing
    resource: https://wiki.eveuniversity.org/Manufacturing
    title: Manufacturing | EVE University Wiki
  - id: eveuni-reactions-facilities
    resource: https://wiki.eveuniversity.org/Reactions
    title: Reactions | EVE University Wiki
  - id: everef-engineering-complexes
    resource: https://everef.net/structures/engineering-complexes
    title: Engineering Complexes | EVE Ref (SDE-derived structure attributes)
  - id: everef-refineries
    resource: https://everef.net/structures/refineries
    title: Refineries | EVE Ref (SDE-derived structure attributes)
  - id: everef-engineering-rigs
    resource: https://everef.net/structures/engineering-rigs
    title: Engineering Rigs | EVE Ref
  - id: eve-reactions-calculator-method
    resource: https://reactions.coalition.space/about
    title: EVE Reactions Calculator methodology
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:25:24Z
status: draft
---

## Summary

Industry capability is not determined by the structure name alone. A facility must offer the correct activity service, have the required service module online if it is an Upwell structure, be in a valid location for the activity, and provide the required rig or role bonuses. The best facility is therefore activity-, item-, security-, price-, and risk-dependent. [^ccp-upwell-structures] [^ccp-service-modules] [^ccp-reactions]

The three main industrially relevant Upwell structure families are Citadels, Engineering Complexes, and Refineries. Engineering Complexes have manufacturing and science role bonuses. Refineries support reactions and resource-processing activities, with the Tatara providing a specific reaction-time role bonus. Structure rigs add more specialized effects for selected item groups and job activities. [^everef-engineering-complexes] [^everef-refineries] [^eveuni-upwell-fitting]

## Facility families

| Facility family | Structures | Primary industrial purpose | Important distinction |
|---|---|---|---|
| NPC stations | Faction and corporation stations with an Industry service | Manufacturing, research, copying, invention, and other services where offered | No Upwell structure rig fit; facility tax is an NPC-set rule |
| Citadels | Astrahus (M), Fortizar (L), Keepstar (XL) | General-purpose docking, defense, and services selected through fitted Standup modules | No Engineering Complex manufacturing role bonuses; service-module compatibility and structure-size restrictions still apply |
| Engineering Complexes | Raitaru (M), Azbel (L), Sotiyo (XL) | Manufacturing, blueprint research, copying, invention, and related industry services | Innate manufacturing-material, manufacturing/science-time, and manufacturing/science-cost bonuses |
| Refineries | Athanor (M), Tatara (L) | Moon mining, reprocessing, and reactions | Reaction service modules are restricted to Refineries; the Tatara has a 25% reaction-time role bonus |

CCP classifies the Citadels as defense-focused, Engineering Complexes as manufacturing-focused, and Refineries as focused on moon mining, refining, and reactions. The Engineering Complex and Refinery hulls also impose different docking and hull-construction constraints. [^ccp-upwell-structures]

## Engineering Complex role bonuses

The current structure attributes list the following role bonuses. The material reduction applies to Manufacturing jobs. The time and ISK reductions apply to Manufacturing and Science jobs. These are structure role bonuses, not rig effects. [^everef-engineering-complexes]

| Structure | Size | Manufacturing material requirement | Manufacturing and Science job time | Manufacturing and Science job ISK requirement | Engineering service-module fuel |
|---|---|---:|---:|---:|---:|
| Raitaru | M | 1% reduction | 15% reduction | 3% reduction | 25% reduction |
| Azbel | L | 1% reduction | 20% reduction | 4% reduction | 25% reduction |
| Sotiyo | XL | 1% reduction | 30% reduction | 5% reduction | 25% reduction |

These role bonuses do not make a facility universally superior:

- The 1% material bonus is modest and only applies to manufacturing materials.
- The time bonus applies to Manufacturing and Science jobs, so it can also improve research/copying/invention throughput when that structure offers the necessary services.
- The ISK reduction modifies the SCI-derived component of the installation fee. Taxes and SCC surcharges are separate components and are not reduced by this role bonus. See [Installation Cost Computation](../09-computations/installation-costs.md).
- Raitaru, Azbel, and Sotiyo are different hull sizes, and their structures have different construction/docking limits. These limits matter for capital and supercapital production chains, not just industrial efficiency. [^eveuni-structure-browser]

## Refinery role bonuses and reaction services

Athanors and Tataras can fit reaction service modules. CCP states that reactions can only be run in a Refinery with a reactor fitted and online, and that reactors can only be installed in systems with a security rating of 0.4 or lower. CCP lists three reactor families: [^ccp-reactions]

- **Standup Biochemical Reactor:** biochemical reactions for booster-related chemistry and specified molecular-forged industrial products, including Neurolink Enhancers, Neurolink Stabilizers, and Isotropic materials.
- **Standup Composite Reactor:** moon-material reactions used in Tech II intermediate materials.
- **Standup Hybrid Reactor:** fullerite-gas reactions used in Tech III materials.

The reactor family must match the reaction formula. A Refinery does not become capable of every reaction simply because it has an online reactor. [^ccp-reactions] [^eveuni-reactions-facilities]

| Refinery | Size | Reaction service | Reaction-time role bonus |
|---|---|---|---:|
| Athanor | M | Yes, with a compatible online reactor | None listed |
| Tatara | L | Yes, with a compatible online reactor | 25% reduction |

The current SDE-derived structure attribute table lists a 0.75 reaction-time multiplier for the Tatara and no equivalent reaction-time role reduction for the Athanor. [^everef-refineries]

Reaction rigs have their own security-space modifiers and should not inherit manufacturing rig multipliers by assumption. The EVE Reactions Calculator documents the following reaction-rig methodology: T1 material rigs provide 2% and T2 provide 2.4%; T1 time rigs provide 20% and T2 provide 24%; low-security space uses a 1.0 rig modifier, while null-security and wormhole space use 1.1. This is a secondary calculator's SDE-based method, so use the in-game Industry quote as final authority for a real job. [^eve-reactions-calculator-method]

## Upwell service modules

Service modules add functionality to an Upwell structure. The fact that a hull can fit a module does not mean every service is compatible with every structure. CCP explicitly notes that some services have structure-specific restrictions and that a service fitted to a structure it was not designed for may not receive the structure's relevant service bonus. [^ccp-service-modules]

The important industrial services are:

| Service module | Activity enabled | Compatibility notes |
|---|---|---|
| Standup Manufacturing Plant | Manufacturing other than capital/supercapital hull construction | General manufacturing service; capital shipyards are separate services |
| Standup Capital Shipyard | Capital ship manufacturing | Large and XL structures only; not permitted in high-security space |
| Standup Supercapital Shipyard | Supercapital ship manufacturing | Sotiyo only; requires the Supercapital Construction Facilities sovereignty upgrade |
| Standup Research Lab | ME research, TE research, and blueprint copying | Research activity service |
| Standup Invention Lab | Invention | Separate from the Research Lab |
| Standup Biochemical Reactor | Biochemical reactions | Refineries only; not high-security space |
| Standup Composite Reactor | Composite reactions | Refineries only; not high-security space |
| Standup Hybrid Reactor | Hybrid reactions | Refineries only; not high-security space |
| Standup Moon Drill | Moon mining | Refinery anchored at the relevant moon-mining beacon |

The module compatibility and capital-service restrictions above are documented in EVE University's fitting reference. CCP independently confirms the three reaction reactor families and the 0.4-or-lower security restriction. [^eveuni-upwell-fitting] [^ccp-reactions]

### Service-module fuel and job interruption risk

An Upwell structure itself does not consume fuel, but each online service module does. CCP states that onlining a service consumes three days' worth of fuel up front; after that, the service consumes fuel hourly. Fuel use differs by service and may be affected by structure bonuses. [^ccp-service-modules]

The operational consequences are important:

- If a Manufacturing or Research service module goes offline, the associated jobs pause until service is restored.
- If the relevant module is removed, or the structure is destroyed, the affected jobs are cancelled.
- CCP's Quick Facts article states that cancelled jobs do not refund materials. [^ccp-upwell-quickfacts]

A facility's advertised activity capability is not enough. Check that the correct service is online for the full expected job duration, and consider structure vulnerability, owner access policies, and fuel supply continuity.

## Structure rigs

The Engineering Complex and Refinery hulls listed in the SDE-derived structure tables each have three rig slots and 400 calibration points. Rigs are size-specific: medium structures use medium rigs, large structures use large rigs, and XL structures use XL rigs. [^everef-engineering-complexes] [^everef-refineries]

Rigs are specialized by activity and item group. EVE University's fitting reference distinguishes, among others: [^eveuni-upwell-fitting]

- Manufacturing material-efficiency rigs.
- Manufacturing time-efficiency rigs.
- Capital and advanced-component manufacturing rigs.
- Ship, ammunition, drone/fighter, structure, and equipment manufacturing rigs.
- Blueprint-copy cost and time rigs.
- ME and TE research cost and time rigs.
- Invention cost and time rigs.
- Separate biochemical, composite, and hybrid reaction material/time rigs.

A rig is not a generic percentage bonus to all industry. A ship manufacturing rig, for example, should not be assumed to improve module manufacturing. Likewise, an ME-research rig and an invention rig affect different activities. A calculator or profitability model must select the rig by its supported activity and product group, not merely by the structure having a rig fitted.

### Rig compatibility and uniqueness

- A rig must match the structure's size and rig category.
- A structure has only three rig slots, so fitting a rig is an opportunity cost against other rig effects.
- Two rigs that affect the same attribute cannot be equipped together, including Tech I and Tech II variants of the same rig effect.
- Rigs improve selected activity parameters; they do not add job slots. Job-slot limits are character-level and documented in [Skills and Job Capacity](skills-and-job-capacity.md). [^ccp-upwell-quickfacts] [^eveuni-upwell-fitting]

### Security-space effects

Structure rig effects can vary by security class and rig family. Reaction rig scaling is explicitly different from the commonly quoted manufacturing rig scaling. Do not apply a single universal high-sec/low-sec/null-sec multiplier to all structure rigs. For reaction modeling, use the reaction-specific method and security modifiers documented above. For other rig families, use the specific rig's current in-game attributes or SDE-backed data rather than copying a multiplier from another activity. [^eve-reactions-calculator-method] [^everef-engineering-rigs]

## Facility selection workflow

For a production, research, invention, or reaction job, evaluate the candidate facility in this order:

1. **Activity compatibility:** does the facility offer the exact activity, and is the required service module online?
2. **Item compatibility:** does the facility's structure type and service support this blueprint, hull size, reaction family, and item group?
3. **Structure bonuses:** identify innate role bonuses for this activity. Engineering Complexes and Tataras have different role bonuses.
4. **Rig applicability:** verify the fitted rigs apply to the exact activity and product group. Do not infer applicability from the rig name alone.
5. **Live installation fee:** compare SCI, structure-cost multipliers, owner facility tax, SCC surcharge, and Alpha status using the in-game quote. See [Installation Cost Computation](../09-computations/installation-costs.md).
6. **Time and materials:** compare the actual job time and material quantity displayed by the Industry window, including character skills, blueprint ME/TE, role bonuses, and rig effects.
7. **Access and operational risk:** verify ACL access, asset location, service-module fuel continuity, structure vulnerability, logistics, and the risk of an interruption.

The Structure Browser and Industry facility list are useful for discovering structures and their services, but the final job quote and the actual fitted rig/service configuration should decide the specific operation. [^eveuni-structure-browser]

## Boundaries and open verification work

This document does not yet enumerate every rig variant, exact rig percentage, affected item group, or combined-bonus stacking calculation. The complete set is large and changes through SDE updates. It also does not attempt to evaluate player structure access risk or the value of fuel logistics for a specific corporation.

The following should be independently checked in game or against a current SDE snapshot before building a deterministic facility optimizer:

- The exact rig bonuses and affected type groups for each rig candidate.
- Security modifiers for non-reaction rig families.
- How multiple applicable bonuses combine and how material/time rounding is applied.
- Actual structure service availability and owner-set installation taxes.
- The exact availability of a service module on a particular structure and system.

## Related concepts

- [Blueprints and Research](blueprints-and-research.md)
- [Skills and Job Capacity](skills-and-job-capacity.md)
- [Installation Cost Computation](../09-computations/installation-costs.md)
- [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md)
- [Reactions](../02-production-systems/reactions.md)

[^ccp-upwell-structures]: CCP Support, Upwell Structures (updated 2024-07-15).
[^ccp-service-modules]: CCP Support, Service Modules (updated 2024-08-29).
[^ccp-upwell-quickfacts]: CCP Support, Upwell Structures - Quick Facts (updated 2022-05-10).
[^ccp-reactions]: CCP Support, Reactions (updated 2024-08-29).
[^eveuni-structure-browser]: EVE University Wiki, Upwell structure / Structure Browser.
[^eveuni-upwell-fitting]: EVE University Wiki, Fitting upwell structures (last modified 2025-07-19).
[^eveuni-manufacturing]: EVE University Wiki, Manufacturing.
[^eveuni-reactions-facilities]: EVE University Wiki, Reactions.
[^everef-engineering-complexes]: EVE Ref, Engineering Complexes (SDE-derived structure attributes).
[^everef-refineries]: EVE Ref, Refineries (SDE-derived structure attributes).
[^everef-engineering-rigs]: EVE Ref, Engineering Rigs (SDE-derived rig attributes).
[^eve-reactions-calculator-method]: EVE Reactions Calculator, methodology.
