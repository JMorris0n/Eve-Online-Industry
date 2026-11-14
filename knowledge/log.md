# Knowledge Base Log

## 2026-11-14

- Initialized the EVE Online industrial knowledge repository scaffold.
- Established OKF v0.2 as the target format.
- Added governance, source-quality, LLM-collaboration, concept, and handoff templates.
- Created a comprehensive topic map and initial research backlog.
- Researched and replaced the Blueprints and Research placeholder with a source-backed draft covering BPOs, BPCs, ME/TE research, material rounding, and copying behavior.
- Added CCP source URLs, source update dates, and a current 2026 LP-store BPC example to the official source catalog.
- Researched and replaced the Skills and Job Capacity placeholder with a source-backed draft covering Manufacturing, Science, and Reaction pools, slot formulas, prerequisites, remote operation, and Alpha limits.
- Added CCP and EVE University source entries for skill and job-capacity research.
- Researched Facilities and Rigs, documenting Upwell families, engineering/refinery roles, industrial service modules, job interruption risks, rig specificity, and reaction rig distinctions.
- Replaced Installation Cost Computation with the CCP fee formula, EIV basis, tax components, structure SCI bonuses, ESI inputs, and activity-specific exceptions.
- Added Industrial Cost Accounting conventions to distinguish EIV from acquisition, replacement, and opportunity cost.
- Added unresolved questions for temporary ME/TE SCC relief, non-manufacturing EIV/value bases, and live verification of rig stacking and location-specific modifiers.
- Researched and replaced the Tech I Manufacturing placeholder with a source-backed draft covering job installation and delivery, BPO/BPC use, output-per-run, per-job material rounding, skill/structure/rig time and material models, and planning constraints.
- Added CCP Industry UI and additional community formula/calculator references. The combined material/time formulas are labeled provisional pending controlled in-game quotes.
- Added research questions for 30-day job-duration limits, BPO concurrency, and precise modifier/rounding behavior.
- Corrected an Upwell rig uniqueness description to match CCP's rule that two rigs affecting the same attribute cannot be equipped together.
- Normalized the Upwell structure-browser source identifier in Installation Cost Computation.
- Researched and replaced the Tech II Invention placeholder with a source-backed draft covering required inputs/skills, the current skill-adjusted success formula, base chance categories, decryptor modifiers, output BPC runs/ME/TE, and expected-cost calculations.
- Added official CCP invention, decryptor, datacore, and historical Phoebe patch-note sources, plus a current EVE University invention reference last modified 2026-10-09.
- Added open verification questions for probability rounding/capping and multi-run datacore/decryptor consumption.
- Researched and created a dedicated Blueprint Copying concept documenting the separate Job Runs and Runs per Copy fields, BPC inheritance, licensed-run limits, exceptional input scaling, base copy-time model, related skills, and operational purposes.
- Linked Blueprint Copying from the production systems index and Tech I Manufacturing guide. Clarified invention expected-cost allocation so multi-run datacore/decryptor quantities must come from actual job inputs.
- Added verification questions for copy-time modifiers, same-BPO concurrency, and the copy-specific input/fee scaling model.
- Researched and replaced the Tech II Components placeholder with a source-backed draft covering raw moon materials, intermediate/composite reactions, Advanced Component manufacturing, Tech II final input categories, skill dependencies, R.A.M. material behavior, and vertical-integration decisions.
- Added CCP's historical R.A.M./R.Db conversion reference and documented the limits of historical damage-per-run mechanic claims.
- Added an open question for a type-level, versioned Tech II component/recipe/skill dataset and independent quote validation.
- Researched and replaced the Reactions placeholder with a source-backed draft covering reactor families, Refinery/security constraints, reaction job lifecycle, moon-material intermediate/composite reaction tables, special reaction exceptions, Hybrid and Biochemical/Molecular-Forged families, and reaction economics.
- Linked the reaction and Tech II component concepts, added the EVE Omnitool reaction calculator to the community reference catalog, and recorded open questions for SDE/in-game recipe validation and a complete Molecular-Forged formula catalog.
- Documentation milestones do not constitute independent in-game verification; all three new concepts remain draft.
- Refreshed Facilities and Rigs against current SDE-derived structure and rig attributes, added manufacturing versus reaction security multipliers, and corrected rig uniqueness to same rig type including T1/T2 variants.
- Researched and replaced the Tech III Manufacturing placeholder with a source-backed four-stage production chain, relic/output mapping, sourcing, skill dependencies, and expected-attempt framework.
- Recorded a material conflict: CCP's Ancient Relics article lists 40%/35%/25% base success chances, while EVE University and sampled SDE relic outputs show different percentages. No formula was inferred; live Industry-window verification remains open.

- Researched and replaced the Planetary Industry placeholder with a source-backed colony, extraction, processor, skill, routing, export, tax, Skyhook, and Alpha-restriction concept.
- Replaced the Planetary Commodities placeholder with P0-P4 tiers, P0-to-P1 mapping, P1-to-P4 recipe reference tables, and standard schematic batch structures. These remain draft pending reconciliation against the post-2025 CCP SDE.
- Added CCP Planetary Interaction, Orbital Skyhook, Equinox, and current SDE documentation to the source catalog. Recorded the EVE University PI overview's explicit Equinox-update warning and the 2025 SDE schema break.

- Researched and replaced the Market Fees and Taxation placeholder using CCP's March 2026 fee article and official order-matching/relist documentation. Documented NPC station, Upwell structure, Accounting, Broker Relations, and relist mechanics.
- Researched and replaced the Manufacturing Profitability placeholder with batch-level economic cost, net proceeds, contribution, margin, ROI, slot-hour, break-even, and sensitivity frameworks.
- Replaced the Manufacturing Profitability Computation placeholder with deterministic input schemas and equations. Updated navigation and backlog; live fee/market validation and a worked current-price example remain open.

- Researched and replaced the Market Location Economics placeholder with a source-backed framework for activity-specific SCI, facility selection, ESI market data, remote installation, logistics, and total landed cost. A live location comparison remains open until current market and facility data are selected.

- Researched and replaced the Logistics and Risk placeholder with self-haul economics, courier-contract collateral/failure behavior, route exposure, Upwell Asset Safety exceptions, and risk-adjusted logistics cost formulas. Live route-specific risk and hauling-cost calibration remain open.

- Researched and replaced the Capital and Asset Management placeholder with working-capital, inventory, capital-turnover, asset-concentration, and capital-allocation guidance.
- Replaced the Capital Turnover Computation placeholder with dated cash-flow, peak working capital, capital-days, inventory-turnover, collateral, and cash-conversion formulas. Live production-cycle validation remains open.

- Researched and replaced the Manufacturing Throughput placeholder with slot-capacity formulas, job/output rate calculations, BPO/BPC parallelism constraints, batch-rounding considerations, and normalized bottleneck analysis. Independent in-game schedule and quote validation remains open.

- Researched and replaced the Science and Invention Throughput placeholder with shared Science slot-hour budgeting, ME/TE research and copying output rates, expected invention BPC/run formulas, and Science-to-Manufacturing bottleneck analysis. Live mixed-schedule validation remains open.

- Researched and replaced the Reaction Throughput placeholder with Reaction slot-hour budgeting, formula input/output rates, reactor and security constraints, time/material rig effects, and normalized reaction-chain bottleneck analysis. Live formula/rig quote validation remains open.

- Researched and replaced the Production Scheduling placeholder with a resource-constrained scheduling framework for Manufacturing, Science, and Reaction pools, including dependencies, blueprint/material/facility constraints, critical path, batch release, and replanning.

- Researched and replaced the Character Specialization placeholder with role profiles for Manufacturing, Science/Invention, Reactions, Market/Trade, and PI, plus a marginal skill-value framework and multi-character role allocation principles.

- Researched and replaced the Industrial Scaling placeholder with a framework for character/facility/region expansion, vertical integration, sustainable output constraints, economies/diseconomies, incremental capital return, and asset concentration controls.

- Researched and replaced the Market Mechanics placeholder with CCP order-matching rules, buy/sell order location/range behavior, regional market history, adjusted-price distinctions, ESI endpoints, and cache-handling requirements.

- Researched and replaced the Demand and Liquidity placeholder with historical volume/transaction analysis, order-book depth, VWAP execution, spread, liquidation horizon, volatility, and market absorption metrics. Clarified that ESI order_count represents completed transactions rather than currently open orders.

- Researched and replaced the Price Analysis placeholder with executable price definitions, historical trend measures, volume-weighted execution valuation, volatility, outlier handling, adjusted-price/EIV separation, and data-provenance rules.

- Researched and replaced the Regional Arbitrage placeholder with a quantity-aware model for source procurement, destination liquidation, market fees, hauling, risk-adjusted loss, capital time, and false-arbitrage screening.

- Researched and replaced the Product Selection placeholder with a multi-criteria framework for feasibility, contribution, slot/capital efficiency, liquidity, make-versus-buy, portfolio risk, and Pareto screening. Live product ranking remains open until a market region, character skills, and operating constraints are selected.

- Researched and replaced the ESI and Market Data placeholder with current ESI versioning/compatibility dates, OpenAPI transition, SSO scopes, caching, rate limiting, pagination, industrial endpoint map, and SDE/ESI separation. Implementation remains open.

- Researched and replaced the Data Quality and Reconciliation placeholder with claim classes, evidence hierarchy, source/ESI/SDE provenance, freshness, normalization, validation dimensions, conflict resolution, and verification-state controls.

- Researched and replaced the Third-Party Industry Tools placeholder with a current tool survey covering EVE Retroindustry, EVE Cookbook/MCP, EVE Omnitool, EVECalc, EVE Online Industry Calculator, and PI planners. Recorded data freshness, feature scope, privacy, SSO, and verification caveats.

- Added draft operational playbooks for product evaluation, Tech I/II production, PI, reactions, and market delivery; indexed them and retained draft status pending live workflow validation.
- Added Q-014 to record the operating-environment inputs needed for a real product-ranking example. Continued work can proceed on generic mechanics and data tooling without blocking on those details.

- Corrected an Alpha-clone PI restriction after checking CCP's current February 2026 Alpha/Omega article and July 2024 quick facts: Alpha clones can import materials into colonies but cannot export colony goods. Updated the Planetary Industry concept, PI playbook, character specialization guidance, and official source catalog; the older PI support article's broader wording is now explicitly noted as less precise.

- Added local CCP SDE acquisition tooling: a standard-library downloader that records build/URL/hash metadata and verifies ZIP integrity, plus an archive inspector. Added usage documentation and ignored raw/generated data paths in Git.
- Updated the root README to reflect the current research repository state and local SDE workflow.

- Resolved the SCC surcharge research question at the documentation level: CCP's 2025-07-18 post reduced ME/TE research surcharge from 4% to 2% and described the reduction as temporary. No later official reversal was found as of 2026-11-14; live in-game quote verification remains open. Replaced the Installation Costs foundation placeholder with an overview linking to the detailed fee computation.

- Added a standard-library, read-only ESI collector for public market orders/history, adjusted prices, and industry system indices. It pins an explicit compatibility date, respects cache/ETag headers, handles X-Pages, honors 429 Retry-After, stops on 420 error-limit responses, and writes timestamped raw data with hashes/provenance. Local execution and schema validation remain open.
