---
type: Concept
title: Third-Party Industry Tools
description: Evaluation of EVE Online industry calculators, market tools, PI planners, local asset managers, and AI/MCP integrations.
tags:
  - tools
  - industry
  - market
  - pi
sources:
  - id: eveuni-third-party-tools
    resource: https://wiki.eveuniversity.org/Third-party_tools
    title: Third-Party Tools | EVE University Wiki
  - id: eve-retroindustry
    resource: https://everetroindustry.github.io/
    title: EVE Retroindustry (v0.11.47 released 2026-11-12)
  - id: eve-cookbook
    resource: https://evecookbook.com/
    title: EVE Cookbook (v1.4.9 changelog 2026-10-01)
  - id: eve-omnitool
    resource: https://eve-omnitool.com/
    title: EVE Omnitool
  - id: evecalc
    resource: https://evecalc.uk/
    title: EVE Online Industry Calc
  - id: eve-industry-calculator
    resource: https://www.eveonline-industry.com/
    title: EVE Online Industry Calculator
  - id: eve-nexus-pi
    resource: https://www.evenexus.app/pi/planner
    title: EvE Nexus Planetary Industry Planner
  - id: eve-pi-tool
    resource: https://evepitool.com/
    title: EvePiTool
  - id: eve-industry-scanner
    resource: https://wiki.eveuniversity.org/Third-party_tools
    title: EVE Industry Scanner (listed as beta 2026-05-27)
  - id: eve-industry-forum-tools
    resource: https://forums.eveonline.com/t/tool-eve-omnitool-com-free-market-industry-live-intel-tool-for-eve/519645
    title: EVE Omnitool developer forum thread (2026-10-25)
generated:
  by: openai/gpt-6
  at: 2026-11-14T09:40:00Z
status: draft
---

## Purpose

Third-party tools can accelerate blueprint planning, material shopping, market analysis, PI layout planning, character inventory review, and production scheduling. They are useful as independent calculators and operational interfaces, but their outputs are estimates based on their own data sources, update cadence, assumptions, and formula implementations.

The knowledge base remains the canonical record of mechanics, assumptions, source lineage, and verified calculations. A third-party tool is a supporting implementation, not the authority for a game mechanic.

## Evaluation criteria

Evaluate each tool against:

1. **Coverage:** manufacturing, reactions, invention, copying/research, PI, reprocessing, market data, logistics.
2. **Data source:** CCP SDE, ESI, Fuzzwork, market snapshots, manually entered data, or another provider.
3. **Freshness:** market cache age, SDE build, ESI cache handling, and patch-update cadence.
4. **Formula transparency:** whether the tool exposes material rounding, job cost, time modifiers, taxes, and assumptions.
5. **Character integration:** ESI SSO scopes, linked characters, corporation data, and asset synchronization.
6. **Privacy/storage:** local-only, browser storage, cloud storage, token handling, analytics, and retention.
7. **Export/integration:** CSV, JSON, API, MCP, copy/paste, or local database.
8. **Maintenance:** release history, changelog, issue reporting, and developer activity.
9. **Cost and limits:** free features, subscription requirements, and usage caps.
10. **Independent verification:** whether its result can be compared against an in-game Industry quote.

## Current tool shortlist

The entries below were checked on 2026-11-14. Features and availability can change. This is a functional shortlist, not a ranking or endorsement.

### EVE Retroindustry

- Website: https://everetroindustry.github.io/
- Type: Local desktop/mobile industrial management application.
- Current version observed: v0.11.47, released 2026-11-12.
- License: MIT; source code is linked from the project site.
- Platforms listed: Windows, Linux, and experimental Android.
- Advertised coverage: blueprint costs to raw materials, market prices, character assets/blueprints/skills, industry jobs, market orders, contracts, wallets, and PI colonies.
- Data model: ESI-connected but locally stored; the project describes itself as no-account/no-cloud.
- Security note: the project states that Windows binaries are not code-signed and may trigger Windows SmartScreen or antivirus warnings. Verify release checksums and inspect the source/release provenance before authorizing EVE SSO.
- Potential use: local inventory and character-state reference, especially when keeping operational data off a third-party cloud service.

### EVE Cookbook

- Website: https://evecookbook.com/
- Type: Web industry calculator with API and MCP integration.
- Advertised coverage: manufacturing, reactions, detailed build steps, Science research/copying/invention, decryptor comparisons, stock-aware shopping lists, and job/character data after EVE SSO linking.
- Data sources: the site states that blueprint/material definitions come from CCP's SDE and that market prices use Jita buy/sell orders from ESI, refreshed about hourly.
- AI integration: the 2026-10-01 changelog introduced an MCP server for AI assistants and a separate account MCP endpoint for a linked character's industry jobs and skills.
- Limitations: its market-price source is Jita, so it is not a substitute for a region/location-specific market analysis. Results are estimates and should be checked in game.
- Privacy note: the site is a free, non-commercial fan tool. Review its current terms and privacy policy before linking an EVE character or using the account MCP endpoint.

### EVE Omnitool

- Website: https://eve-omnitool.com/
- Type: Web market, industry, and live-intelligence tool.
- Advertised coverage: market scanning, arbitrage, industry build-cost calculations, reaction profitability, reprocessing, hauling, and other market/operational views.
- Recent development: the developer's 2026-10-25 forum post describes public player-structure market support and expanded manufacturing/reaction calculators.
- Data limitations: the service states that prices and other figures are snapshots, not a live feed; each screen indicates data age.
- Potential use: independent market-depth and build-cost cross-check.
- Privacy note: review current terms and EVE SSO scopes before linking a character.

### EVE Online Industry Calc (EVECalc)

- Website: https://evecalc.uk/
- Type: Web multi-blueprint manufacturing calculator.
- Advertised coverage: multi-blueprint build planning, combined material requirements, job installation costs, facility bonuses, market orders, stock-aware shopping lists, profitability research, and ESI-linked character assets/skills.
- Potential use: checking large multi-blueprint jobs where materials from multiple blueprints can be consolidated before calculating requirements.
- Limitations: the developer describes it as actively developed and changing frequently. Verify results and review the linked-character permissions and data policy before connecting EVE SSO.

### EVE Online Industry Calculator

- Website: https://www.eveonline-industry.com/
- Type: Web blueprint and PI calculators.
- Advertised coverage: T1/T2/T3 manufacturing, build costs, market prices, system indices, structure/rig settings, component build-versus-buy, and PI chain profitability.
- Market data: the site describes cached market prices and optional premium asset synchronization.
- Potential use: quick independent blueprint and PI comparison.
- Limitations: check the timestamp of cached prices and ensure facility taxes/rigs match the actual structure.

### EvE Nexus PI Planner

- Website: https://www.evenexus.app/pi/planner
- Type: Browser-based PI chain planner.
- Advertised coverage: interactive P1-P4 production chains, factory counts, buy-versus-produce inputs, bottleneck warnings, and profit estimates.
- Price assumptions: the tool states that it uses The Forge prices via Fuzzwork. Its default P0 assumption is that raw materials are extracted by the user and therefore have no market cost.
- Important limitations: the tool's own methodology says it excludes extraction effort and hauling and uses default character fee assumptions unless configured. Treat its output as an upper-bound planning estimate, not realized colony profit.

### EvePiTool

- Website: https://evepitool.com/
- Type: Planetary Industry planner.
- Advertised coverage: planet/system import, P0 resource price comparison, and PI chain planning.
- Potential use: supplementary resource and colony planning.
- Limitations: validate market timestamps, planet-resource assumptions, and recipe data before using it for a production decision.

### EVE Industry Scanner

- Reference: EVE University third-party tools directory.
- Status observed: listed as beta on 2026-05-27.
- Advertised coverage: SDE manufacturing, reaction, and PI recipes compared with live ESI orders across several market hubs, with profit/ISK-hour sorting and optional SSO watchlist/buildability hints.
- Limitations: beta status and cached market prices require independent verification before operational reliance.

## Tool-to-task fit

| Task | Candidate tools | Verification requirement |
|---|---|---|
| Multi-blueprint manufacturing | EVE Retroindustry, EVE Cookbook, EVECalc, EVE Omnitool | Compare materials/job fee with in-game quote |
| Research and invention | EVE Cookbook, EVE Retroindustry | Compare success chance, inputs, output BPC, and job duration |
| Reactions | EVE Cookbook, EVE Omnitool, EVE Industry Scanner | Compare formula, fuel, job duration, rig, and installation fee |
| PI chains | EvE Nexus, EvePiTool, EVE Industry Calculator, EVE Retroindustry | Reconcile schematic inputs/outputs with current SDE and live PI UI |
| Market analysis | EVE Omnitool, EVE Cookbook, EVE Tycoon, ISK.GG | Check data age, location, order depth, and ESI cache |
| Local character/asset management | EVE Retroindustry | Review source, checksums, and OAuth scopes |
| AI-assisted industrial queries | EVE Cookbook MCP | Review MCP tools, account scopes, data retention, and calculation assumptions |

## Recommended validation workflow

1. Select a representative blueprint, reaction, or PI chain.
2. Record the current in-game Industry/PI quote and the selected facility/rig/tax configuration.
3. Run the same scenario through at least two independent tools where possible.
4. Compare exact material quantities, job duration, installation fee, and market valuation separately.
5. Identify whether a difference comes from data freshness, formula assumptions, or a calculation error.
6. Record the validated result and any tool-specific caveat in the relevant concept or verification log.

Do not average conflicting calculator outputs. Reconcile the underlying inputs and formulas.

## Security and privacy checklist

Before linking EVE SSO to any tool:
- Review the exact scopes requested.
- Prefer read-only scopes.
- Confirm whether character, corporation, asset, wallet, or location data is stored locally or remotely.
- Read the current privacy policy and terms.
- Check token revocation and deletion procedures.
- Avoid linking a character to a tool solely to test a public calculator.
- Never paste EVE SSO tokens or client secrets into this repository or an LLM prompt.

For local applications:
- Verify the official release source.
- Check published checksums/signatures.
- Review source code and dependencies where practical.
- Understand where tokens and cached data are stored.
- Keep backups of local databases before upgrades.

## Project integration policy

The repository should not become dependent on one third-party calculator. Use tools to discover, compare, and cross-check. Keep core formulas and data provenance in the repository so the project remains portable if a service disappears, changes pricing, changes its API, or alters its assumptions.

Future automation should prefer:
1. Direct CCP SDE and ESI ingestion.
2. Local deterministic computations.
3. Third-party tools as independent cross-checks.
4. Human verification for high-impact or ambiguous mechanics.

## Open evaluation tasks

- Test one representative T1 manufacturing build in EVE Cookbook, EVE Omnitool, EVECalc, and the in-game Industry window.
- Test a reaction formula in two calculators and compare with the in-game quote.
- Test one PI chain against current SDE schematics and the in-game PI interface.
- Review EVE Retroindustry source/release and local token-storage behavior before recommending it for character data.
- Evaluate EVE Cookbook MCP scope requirements and whether it can be used safely in the user's multi-model workflow.
- Record tool version, data timestamp, and exact assumptions for every comparison.

## Related concepts

- [ESI and Market Data](esi-and-market-data.md)
- [Data Quality and Reconciliation](data-quality.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)
- [Market Mechanics](../06-market-intelligence/market-mechanics.md)
- [Planetary Industry](../02-production-systems/planetary-industry.md)

[^eveuni-third-party-tools]: EVE University Wiki, Third-Party Tools (accessed 2026-11-14).
[^eve-retroindustry]: EVE Retroindustry project website, v0.11.47 (released 2026-11-12).
[^eve-cookbook]: EVE Cookbook website and changelog (v1.4.9, 2026-10-01).
[^eve-omnitool]: EVE Omnitool website and terms (accessed 2026-11-14).
[^evecalc]: EVE Online Industry Calc (accessed 2026-11-14).
[^eve-industry-calculator]: EVE Online Industry Calculator (accessed 2026-11-14).
[^eve-nexus-pi]: EvE Nexus PI Planner (accessed 2026-11-14).
[^eve-pi-tool]: EvePiTool (accessed 2026-11-14).
[^eve-industry-scanner]: EVE University third-party tools directory (beta status noted 2026-05-27).
[^eve-industry-forum-tools]: EVE Online Forums, EVE Omnitool developer thread (2026-10-25).
