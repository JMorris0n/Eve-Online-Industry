---
type: Handoff
title: EVE Online Industry Research and Decision-Support Project Handoff
description: Current objectives, milestone status, evidence, privacy boundaries, and prioritized next actions for a continuing LLM.
generated:
  by: openai/gpt-6
  at: 2026-11-15T21:05:22Z
status: active
---

# EVE Online Industry Research: Milestone Review and LLM Handoff

**Review timestamp:** 2026-11-15 21:05 UTC  
**Repository:** `JMorris0n/Eve-Online-Industry`  
**Current main commit:** `77c2e959449121cea8ac07d46622b069f93240bd`  
**Latest validation:** GitHub Actions run [43748078973](https://github.com/JMorris0n/Eve-Online-Industry/actions/runs/43748078973), completed successfully.

## 1. Executive summary

The project has moved beyond static industrial-mechanics research and now has a functioning, tested foundation for **personalized EVE industry decision support**. Public SDE data is parsed and audited, bounded regional market data has been collected, the three-character read-only ESI integration is working, a private operating profile is populated, personal blueprints and assets are imported, and the quote-first single-product evaluator is implemented.

The current state is **strong on data acquisition and engineering infrastructure, incomplete on operational verification and business decisions**. No product has yet passed a real worked evaluation with current quotes, verified facilities, realistic procurement, and market exit. No production pilot has been completed. Therefore, the project cannot yet make a defensible recommendation about what to manufacture.

The highest-value next work is not more broad encyclopedia research or a general product scanner. It is to close the minimum operational evidence gaps, select one realistic pilot product, and prove the evaluator against actual in-game quotes and current market data.

### Critical privacy note

The user uploaded `asset-stock-reconciliation.csv` to the Dropbox root. This CSV contains private inventory detail: item names, type IDs, exact quantities, and NPC station names/IDs. The repository explicitly requires this file to remain local under ignored `local/` and never be uploaded or committed.

Dropbox metadata reports a `parent_shared_folder_id`. That does **not** prove the file has a public or anyone-with-link URL, but it places the file in a shared-folder context where other folder members may have access. No shared-link enumeration or public-link check was performed in this review. The recommended remediation is to remove the Dropbox copy and retain the local file only. Do not copy row-level details, item names, station names, IDs, or quantities into GitHub, a public handoff, or future prompts.

The redacted `asset-ledger-readiness.json` is the correct shareable artifact. The full asset ledger and the CSV are not.

## 2. Overall objectives

### North-star objective

Answer this operational question:

> Given the actual characters, skills, blueprints, usable facilities, market access, capital, and logistics, what should this operation manufacture now to maximize realistic net contribution for the active time invested?

A related workflow should evaluate a nominated product or batch and answer:

- What should be purchased versus manufactured?
- Which character and facility should perform each job?
- What quantity should be run?
- What cash is committed, and for how long?
- How should the finished output be sold or liquidated?
- How much active attention is required?
- What are the low, base, and high outcomes, and what facts remain uncertain?

The system must be able to recommend **no production** when evidence, liquidity, margin, or operating constraints do not support a good opportunity.

### Primary ranking measure

Maximize **unadjusted net contribution per active operator-hour**:

```text
net contribution after variable costs / active operator-hours
```

Count active time spent sourcing, evaluating, staging, installing jobs, hauling, adjusting market orders, and reconciling results. Do not count unattended production duration as active labor. Simultaneous alt-character actions performed by one person count as one operator-hour, not one hour per character. Do not treat self-mined or self-sourced inputs as free; value them at acquisition cost or reasonable opportunity cost.

Do not hide an invented risk premium in the ranking. Display risk drivers and low/base/high cases separately until real pilot observations support a defensible risk adjustment.

### Secondary measures and constraints

- Net contribution per batch.
- Manufacturing, Science, and Reaction slot-hours.
- Peak capital committed, capital-days, and contribution per capital-day.
- Material procurement depth and actual buy-side fill quality.
- Market liquidity, turnover, expected liquidation time, and realistic sale quantity.
- Fees, relist costs, hauling/handling costs, and operational complexity.
- Inventory concentration and the risk of unsold output.

### Three strategic tracks

1. **Alliance-local production:** make doctrine or replacement goods near the relevant staging environment when actual demand, local input supply, and fees support it.
2. **Value-added export:** source goods locally, manufacture higher-value output, then move it to a market with better realized economics.
3. **Other high-attention-efficiency work:** independent manufacturing, reactions, invention, copying, research, and market activity where returns justify the added jobs and management.

Do not assume an alliance, doctrine set, staging system, buyback program, shared corporation inventory, courier service, or structure access. These remain user/environment dependencies.

## 3. Milestone review

| Milestone | Status | Assessment |
|---|---|---|
| M0: Confirm operating objective | Agreed, mostly complete | Strategic objective and ranking principles are accepted. Detailed capital, time, risk, and liquidation thresholds remain unknown. |
| M1: Validate public data foundation | Completed for bounded scope | Current SDE build 3698585 was downloaded, integrity-checked, parsed, and audited. A bounded ESI market sample and schema-v4 summaries were reviewed. The market sample is stale for live execution. |
| M2: Define local operating profile | In progress | Three-character SSO/import and profile pipeline is working. Personal blueprints and assets are imported. Actual job-slot verification, stock reconciliation, facilities, markets, and manual operating inputs remain open. |
| M3: Doctrine and market context | Deferred / dependency-gated | Requires the target alliance, doctrine set, staging environment, and target market arrangement. A generic import format can be developed independently if useful. |
| M4: Practical single-product evaluator | In progress | Quote-first evaluator and exact-quantity v4 market adapters exist. No complete real-product worked example has passed quote, cost, sale, time, and sensitivity reconciliation. |
| M5: Candidate scanner and ranker | Not started | Correctly waits on M2 and a proven M4 evaluator. |
| M6: Limited production pilot | Not started | Requires a candidate that passes the evaluator and a confirmed operating environment. |
| M7: Local decision-support tool | Not started | Should be built incrementally after M4/M5 prove value. A CLI/report is preferred before a graphical application. |
| M8: Optional local EVE SSO integration | Core technical implementation complete; evidence path folded into M2 | PKCE, token validation/refresh, OS keyring, three character grants, snapshot importer, and redacted readiness are implemented. Do not mistake implementation completion for complete operational verification. |

### M0: objective agreed

The user has explicitly prioritized low-attention realistic economics over theoretical maximum margin. Predictable turnover and semi-passive operation are preferred. Unnecessary vertical integration and self-mining as a required supply strategy are de-emphasized. Detailed thresholds remain unconfigured.

### M1: public data foundation completed within scope

- Current SDE build **3698585** was obtained and parsed.
- The recipe parser produced **5,022** manufacturing/reaction records and the reviewed audit found no duplicate blueprint/activity keys or structural errors. The audit still reports incomplete or unpublished recipe/type/skill references; candidate filtering must preserve these exceptions.
- Public ESI collection and schema-v4 summary generation were exercised for a bounded sample.
- Range handling, order minimum-volume rules, exact-quantity buy-side sweeps, history coverage, and provenance were reviewed.
- The The Forge order snapshot in the M1 sample is stale. It is evidence of a working pipeline, not a live quote or current recommendation.

### M2: local profile progress

**Verified implementation/data:**

- Read-only local EVE SSO using Authorization Code with PKCE, JWT validation, refresh-token rotation, and OS-backed credential storage.
- All three character authorization grants completed.
- Three-character sync and offline profile import completed.
- Skill inventories verified for all three characters: **358, 55, and 59 known skills**.
- All nine character/activity pools (Manufacturing, Science, Reaction for each character) report available capacity from the ESI-derived profile.
- Personal blueprint inventory: **375 records**. Corporation-owned blueprints are not imported, so operation-wide blueprint coverage is partial.
- Asset ledger built from personal snapshots: **3,681 asset records**.
- Latest redacted asset readiness report: all three asset snapshots fresh at generation time; 3,657 locations resolved and 24 unresolved-parent records; 183 candidate asset records grouped into 168 candidate stock lines.
- Candidate stock is concentrated on character slot 1. Slots 2 and 3 have no candidate material-stock lines in this snapshot.
- The private reconciliation CSV has been generated and structurally inspected. It has 168 rows, 151 distinct type IDs, 16 distinct NPC station locations, 183 source asset records, and fully resolved item/station names. All in-game verification columns are blank.

**Still unverified:** ESI's 90-day completed-job history cannot rule out older ready-to-deliver jobs. The derived nine free-slot pools must be compared with the in-game Industry UI. Personal blueprint counts should also be checked against the client. Facility access remains unknown; the public facilities endpoint does not establish character access or installed Industry services.

### M3: alliance dependency

No alliance or staging context is recorded in the canonical project data. Do not fabricate one. Doctrine demand is a candidate signal, not proof of sales. When the user supplies the operating context, capture doctrine fittings, local demand/buyback terms, target markets, facility/service access, and hauling options separately.

### M4: evaluator state

The quote-first evaluator currently:
- Validates a normalized SDE recipe against actual Industry-window quote output and material quantities.
- Uses explicit installation-fee inputs rather than an unverified fee estimate.
- Supports exact-quantity local ask sweeps and rejects incomplete procurement quantities.
- Supports immediate liquidation using range-eligible bid sweeps, preserving partially sold remainder as inventory.
- Supports a separate sell-order scenario with explicit prices/fees.
- Records source timestamps and hashes and warns on stale market summaries.

Still required: one real worked product/batch, intermediate buy-versus-build comparison, actual quote and fee reconciliation, active operator time, capital-days, slot-hours, liquidation horizon, and low/base/high cases. Unattended job time must not substitute for active time.

## 4. Asset reconciliation interpretation

The redacted readiness report and the detailed reconciliation export answer different questions:

- The readiness report is safe to share and reports aggregate counts/freshness only.
- The reconciliation CSV is a private row-level convenience export with item names, type IDs, station names/IDs, quantities, and source-record counts.

The ledger candidate rule is deliberately conservative about location and asset identity: non-singleton, non-blueprint stack records whose complete location chain resolves to an NPC station and uses the standard Hangar flag throughout. Cargo, deliveries, corporation divisions, specialized holds, stale data, and unresolved locations are excluded.

**That rule does not classify an item as a manufacturing input.** It merely finds stackable personal assets in standard station hangars. The export is a heterogeneous inventory list. Items may be finished modules, ships, ammunition, consumables, materials, or other stackable goods. Only a subset may intersect actual SDE recipe material requirements. It also does not prove current in-game quantity, access, Industry service access, or job-input eligibility.

Do not manually audit all 168 lines before selecting a useful pilot. First intersect locally held types with the SDE recipe catalog and owned blueprint inventory. Then focus in-game inventory verification on the subset needed for a specific product and batch. For every input that will offset procurement cost, confirm its location and quantity in the client and that the intended Industry job can actually select it.

## 5. Remaining work, prioritized

### P0: Remediate the private CSV upload

1. Remove `asset-stock-reconciliation.csv` from Dropbox and retain it only at ignored `local/asset-stock-reconciliation.csv`.
2. Do not commit or re-upload the CSV, asset ledger, populated operating profile, raw snapshots, SSO configuration, or token data.
3. The uploaded file's Dropbox metadata included a parent shared-folder ID. This is not proof of a public link; it does mean the shared-folder membership boundary should be considered. If other people have access to that parent folder, assume they may have been able to access the file while it was there.
4. The safe shareable file is the identifier-free `asset-ledger-readiness.json`.

### P1: Close operational evidence gaps in M2

1. Reconcile each character's Manufacturing, Science, and Reaction free-slot counts against the in-game Industry UI. Include any ready-to-deliver jobs older than 90 days.
2. Verify the personal blueprint inventory against the client. Keep corporation blueprint coverage marked partial.
3. Discover facilities using the public facility directory and targeted searches/resolution, but mark only actual character access and usable Industry services as verified.
4. Establish procurement/sale market access separately for NPC stations and Upwell structures.
5. Enter only operation-allocated capital, liquidity reserve, maximum capital at risk, active operator-hour budget, setup tolerance, target liquidation horizon, risk tolerance, and hauling constraints. Do not request total account balances when an allocated working budget is sufficient.

### P2: Turn the local inventory into product-relevant evidence

1. Use the local asset ledger/CSV and local `data/derived/industry-recipes.jsonl` to intersect candidate held types with recipe material inputs and outputs.
2. Compare held inventory types with the personal blueprint catalog to identify plausible output families, but remember that the personal blueprint set is not operation-wide.
3. Separate raw inputs, intermediate components, finished outputs, consumables, and unrelated assets. Do not interpret a generic candidate state as usable industrial stock.
4. Select one candidate product/batch that has a plausible market, accessible blueprint, skill feasibility, and realistic facility route.
5. Only then verify the specific in-game inventory lines needed for that batch. Record sanitized confirmation results rather than sharing the CSV.

### P3: Establish target demand and logistics

When the alliance/environment is known:
- Import a small doctrine fitting sample and normalize its item type IDs.
- Identify staging market and accessible facilities/services.
- Capture buyback rules, local sell/buy behavior, courier terms, or own-haul route assumptions.
- Distinguish private structure market access from public regional-market observations.
- Avoid adding corporation or structure-market SSO scopes until an actual workflow requires them and access is justified.

### P4: Complete M4 real-product evaluation

- Generate a fresh market sample for only the selected product, required inputs, output, quantity, and target locations.
- Capture actual Industry quote output, material bill, duration, installation fees, and blueprint ME/TE facts from the client.
- Compare buying intermediates against manufacturing them.
- Add realistic output liquidation, fees, hauling, working capital, active operator time, slot-hours, and low/base/high cases.
- Do not treat stale snapshots, displayed top-of-book prices, or unfilled sell orders as realized revenue.

### P5: Only then start M5-M7

Build an explainable scanner once the single-product evaluator is proven. Complete a limited pilot before building a dashboard. The deterministic calculation/reporting system should remain useful without an LLM.

## 6. Immediate next steps for the continuing LLM

Use this sequence rather than restarting research:

1. **Privacy cleanup first:** tell the user the Dropbox CSV is a policy exception and recommend removing it from Dropbox. Do not delete it yourself without explicit authorization.
2. Ask the user to continue using the local copy only. No new SSO authorization or asset-ledger rebuild is needed merely to read the existing CSV.
3. Prefer a local recipe-input overlap analysis over a 168-line manual inventory audit. Use the local private ledger, SDE recipe JSONL, and personal blueprint data. Output should be local and should not contain row-level data in Git.
4. Reconcile the nine job-capacity pools and personal blueprint counts in-game, returning only sanitized outcomes.
5. Determine facility/market access and the minimum operating constraints.
6. Choose one real product and complete M4 using fresh, targeted market data and actual Industry quotes.
7. Advance M3/M5 only as the operating context justifies.

### Commands already available to the user

From the repository root:

```powershell
git pull --ff-only origin main
```

The CSV exporter is already in `main`:

```powershell
py -3 tools/profile/export_asset_reconciliation.py `
    --ledger data/private/esi/asset-ledger.json `
    --sde-dir data/raw/sde/3698585/extracted `
    --output local/asset-stock-reconciliation.csv
```

Do not rerun the exporter unless the local SDE path or source ledger needs refreshing. If the SDE build directory differs, use the actual extracted build directory. Public ESI station-name lookups can be skipped with `--no-station-name-lookup`.

## 7. Architecture, privacy, and evidence rules

### Local/private data

Keep these local and Git-ignored:
- `data/private/esi/authorized-characters.json`
- `data/private/esi/snapshots/`
- `data/private/esi/profile-import-manifest.json`
- `data/private/esi/asset-ledger.json`
- `local/operating-profile.json`
- `local/profile-readiness.json`
- `local/asset-ledger-readiness.json`
- `local/asset-stock-reconciliation.csv`
- Any token, credentials, wallet/balance export, private orders, exact asset rows, and private structure details.

Only intentionally redacted reports are shareable, after inspection.

### ESI integration boundaries

- The integration is read-only.
- It does not place orders, create industry jobs, create contracts, or perform in-game actions.
- Personal character endpoints do not include corporation-owned assets, blueprints, jobs, or facility ACLs.
- The public `/industry/facilities/` directory does not prove docking/service access.
- ESI completed-job history is limited to 90 days.
- Do not request extra corporation or structure-market scopes until a known operational need exists.

### Evidence discipline

- Keep facts, derived values, estimates, and unknowns separate.
- A successful parser, import, or test suite proves software behavior, not that inventory is currently usable or an item is profitable.
- A candidate asset is not an eligible job input.
- A skill/blueprint feasibility result is not an Industry quote.
- A market order book is not realized sale volume.
- A job's elapsed duration is not active operator time.
- An old market snapshot is not a current quote.
- Never fill unknown capital, risk, logistics, or access with plausible-sounding assumptions.

## 8. Current repository references

- [Operational roadmap](operational-roadmap.md)
- [Authenticated ESI data plan](esi-authenticated-data-plan.md)
- [Research backlog](research-backlog.md)
- [Public data foundation audit](data-foundation-audit.md)
- [Local profile and asset tools](../../tools/profile/README.md)
- [Local SDE tools](../../tools/sde/README.md)
- [Chronological knowledge log](../log.md)

### Key implementation files

- `tools/esi/sso_local.py`: local PKCE SSO and ESI snapshot sync.
- `tools/profile/import_esi_profile.py`: three-character snapshot-to-profile import.
- `tools/profile/readiness_report.py`: redacted profile readiness.
- `tools/profile/build_asset_ledger.py`: private personal asset/location ledger.
- `tools/profile/summarize_asset_ledger.py`: identifier-free asset summary.
- `tools/profile/export_asset_reconciliation.py`: private local stock review CSV.
- Quote-first evaluator: inspect the current operational roadmap/backlog for its current command and input contract before running it.
- `tools/sde/parse_industry_recipes.py`: SDE manufacturing/reaction normalization.
- `tools/profile/check_feasibility.py`: hard-constraint feasibility screen.

## 9. Known limits and open dependencies

- The target alliance, doctrine list, staging environment, and corporation resources are not yet supplied.
- The facility inventory remains unknown/zero verified.
- Market access is not entered.
- Working capital and liquidity reserve are unknown.
- Active operator-hours, setup tolerance, risk tolerance, liquidation horizon, and hauling logistics are unknown.
- Personal blueprints are imported, but corporation-owned blueprint coverage remains partial.
- Candidate inventory is personal character inventory only.
- Job capacity is ESI-derived, not yet reconciled with the in-game Industry UI.
- The last bounded market sample is stale for live decision-making.
- No real product has passed M4's full worked-example acceptance.
- No manufacturing pilot has been completed.
- No profitability or opportunity recommendation is currently justified.

## 10. Handoff instruction to the next LLM

Continue from repository main at commit `77c2e959449121cea8ac07d46622b069f93240bd`. Read this handoff, the roadmap, the ESI data plan, and the local profile README before changing priorities. Do not redo completed public-data or SSO implementation work. Do not ask for private files to be uploaded. Use code/tests/docs to reduce user effort, preserve the local-only boundary, and choose the next step by expected decision value per user/operator-hour. The immediate strategic target is one defensible M4 worked product, not completion of every industrial research topic.
