---
type: Concept
title: Community References
description: Catalog of community-maintained references and their known limitations.
tags:
  - references
  - community
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:25:24Z
status: draft
---

## Catalog policy

Add sources only after confirming that the URL resolves and the source is relevant. Prefer direct source URLs over search result URLs.

For each source, record:
- Stable source ID.
- Publisher or maintainer.
- Title.
- Canonical URL.
- Source type.
- Publication or update date when available.
- Accessed date.
- Scope and known limitations.

Do not use this catalog as evidence for a game mechanic. Individual concept files must identify which source supports each claim and record source limitations.

## EVE University skill and industry references

| Source ID | Reference | Last modified | Use in this knowledge base |
|---|---|---|---|
| eveuni-production | [Manufacturing](https://wiki.eveuniversity.org/Production) | 2025-09-09 | Manufacturing slot counts, Mass Production and Advanced Mass Production, Supply Chain Management range |
| eveuni-research | [Research](https://wiki.eveuniversity.org/Research) | 2026-03-21 | Science slot counts, research/copying skill effects, Scientific Networking, BPO usage constraints |
| eveuni-reactions | [Reactions](https://wiki.eveuniversity.org/Reactions) | 2025-06-22 | Reaction slot counts, reaction duration skill, remote reaction management |
| eveuni-production-skills | [Skills:Production](https://wiki.eveuniversity.org/Skills:Production) | 2025-09-09 | Manufacturing skill prerequisites, effects, and Alpha training limits |
| eveuni-science-skills | [Skills:Science](https://wiki.eveuniversity.org/Skills:Science) | 2024-06-28 | Science support skills, prerequisites, and Alpha training limits |
| eveuni-resource-skills | [Skills: Resource Processing](https://wiki.eveuniversity.org/Skills:Resource_Processing) | 2026-01-27 | Reaction skills and remote reaction prerequisites and Alpha limits |
| eveuni-structure-browser | [Upwell structure / Structure Browser](https://wiki.eveuniversity.org/Structure_Browser) | Accessed 2026-11-14 | Engineering Complex and Refinery role bonuses, structure roles and hull limitations |
| eveuni-upwell-fitting | [Fitting upwell structures](https://wiki.eveuniversity.org/Fitting_upwell_structures) | 2025-07-19 | Service-module compatibility, industrial service types, activity-specific rig families |
| eveuni-manufacturing | [Manufacturing](https://wiki.eveuniversity.org/Manufacturing) | Accessed 2026-11-14 | Manufacturing EIV definition, installation fee components, and warning about stale SCI derivation |
| eveuni-reactions-facilities | [Reactions](https://wiki.eveuniversity.org/Reactions) | Accessed 2026-11-14 | Reactor types and reaction facility constraints |

## Invention references

| Source ID | Reference | Last modified / accessed | Use and limitations |
|---|---|---|---|
| eveuni-invention | [Invention](https://wiki.eveuniversity.org/Invention) | 2026-10-09 | Current skill-adjusted invention probability formula, category base chances, input/output BPC behavior, baseline runs/ME/TE, and decryptor planning. Community educational reference. |
| eveuni-datacores | [Datacores](https://wiki.eveuniversity.org/Datacores) | Accessed 2026-11-14 | Datacore fields, requirements, and invention acquisition routes. |

## Manufacturing formula and calculator references

| Source ID | Reference | Published / accessed | Use and limitations |
|---|---|---|---|
| eve-industry-formula-c4813 | [EVE Online Industry Formula](https://www.c4813.space/eve-online-industry-formula/) | 2025-07-25 | Community spreadsheet formulas for material/time multipliers, rounding, job cost, and job duration limits. The author describes the collection as incomplete; validate formulas in game. |
| eve-omnitool-manufacturing | [EVE Omnitool Industry Cost Calculator](https://eve-omnitool.com/industry/manufacturing/cost) | Accessed 2026-11-14 | Current community calculator description of per-job material rounding, minimum one unit per run, BPC batch fragmentation, rig multipliers, and job costing. Calculator methodology is not CCP specification. |

## SDE-derived and calculator references

| Source ID | Reference | Accessed | Use and limitations |
|---|---|---|---|
| everef-engineering-complexes | [Engineering Complexes](https://everef.net/structures/engineering-complexes) | 2026-11-14 | EVE Ref presents SDE-derived role bonuses, rig sizes, slots and calibration. Structured secondary reference, not CCP policy documentation. |
| everef-refineries | [Refineries](https://everef.net/structures/refineries) | 2026-11-14 | EVE Ref presents Athanor/Tatara attributes including reaction-time multiplier and rig slots. |
| everef-engineering-rigs | [Engineering Rigs](https://everef.net/structures/engineering-rigs) | 2026-11-14 | SDE-derived rig effects; exact type scopes should be checked against current in-game attributes. |
| eve-reactions-calculator-method | [EVE Reactions Calculator methodology](https://reactions.coalition.space/about) | 2026-11-14 | Documents reaction rig, time, material, EIV and fee calculations; calculator-specific methodology, not official game policy. |

## Source limitations

EVE University is a community educational resource. EVE Ref is a structured SDE-derived reference. The EVE Reactions Calculator explains its own algorithm. These sources help identify item attributes and model mechanics, but the current in-game Industry UI is authoritative for an actual job quote and a real facility's configured services, rigs, and taxes.
