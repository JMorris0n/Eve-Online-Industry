# Local EVE SSO and null-sec operating-data plan

**Status:** Approved strategic direction. The first local, read-only PKCE importer is implemented and regression-tested; live character authorization and snapshot verification remain pending.  
**Decision date:** 2026-11-14  
**Purpose:** Replace manual transcription of character-specific data with narrowly scoped, read-only EVE SSO/ESI imports while keeping credentials and personal operating data on the user's machine.

## Strategic direction

The operating strategy has three complementary tracks:

1. **Alliance-local supply:** Use resources available through alliance miners, salvage/loot buyback, and local markets to manufacture doctrine items and ships when the finished product earns an acceptable return after valuing inputs at their real acquisition or opportunity cost.
2. **Value-added export:** Acquire local inputs, manufacture higher-value-density products, and sell them in better-paying markets. Compare alliance courier services against self-hauling, including fees, cargo capacity, active travel time, market fees, delivery time, and risk.
3. **Other high-attention-efficiency opportunities:** Evaluate independent manufacturing, reactions, invention, copying, research, market/order work, and other opportunities when expected net contribution justifies capital, job slots, logistics, and active operator time.

The ranking objective remains **unadjusted net contribution per active operator-hour**. Secondary measures include capital-days, peak capital at risk, Manufacturing/Science/Reaction slot-hours, turnover/liquidation horizon, liquidity, and low/base/high outcomes. Do not count self-mined or buyback-sourced inputs as free: use actual acquisition cost or defensible foregone-sale value.

Alliance identity, doctrines, staging, buyback schedules, structure access, market rules, and courier services are not known yet. Do not select doctrine products or assume a null-sec market before those facts are available. Prepare the personal character baseline now; ingest alliance-specific data after joining.

## ESI data available per character

ESI is character-oriented and has no account-level endpoint. Each of the three industrial characters therefore needs its own SSO authorization, even if they belong to one EVE account. The same local application can be reused for all three authorizations.

| Data required | ESI endpoint | Minimum scope | Project use |
|---|---|---|---|
| Trained skill inventory | `GET /characters/{character_id}/skills/` | `esi-skills.read_skills.v1` | Import every trained skill ID, level, and skill points into the local profile |
| Skill queue | `GET /characters/{character_id}/skillqueue/` | `esi-skills.read_skillqueue.v1` | Reconcile skill completions that may not yet appear in the skills endpoint |
| Personal blueprint inventory | `GET /characters/{character_id}/blueprints/` | `esi-characters.read_blueprints.v1` | Import blueprint type, location, BPO/BPC quantity, ME, TE, and remaining runs |
| Personal assets | `GET /characters/{character_id}/assets/` | `esi-assets.read_assets.v1` | Locate stored inputs, components, ships, and useful inventory; resolve location/item names where supported |
| Personal industry jobs | `GET /characters/{character_id}/industry/jobs/` | `esi-industry.read_character_jobs.v1` | Identify active jobs, activity, blueprint, facility, runs, status, and expected completion |
| Search known accessible Upwell structures | `GET /characters/{character_id}/search/` with `categories=structure` | `esi-search.search_structures.v1` | Resolve structure IDs by a known or supplied structure-name query |
| Resolve a known Upwell structure | `GET /universe/structures/{structure_id}/` | `esi-universe.read_structures.v1` | Retrieve structure name, system, type, and owner when the character has docking access |
| Public industry facility directory | `GET /industry/facilities/` | Public; no SSO scope | Discover publicly accessible industrial facilities and published facility data |

The skills endpoint can be stale for skills that completed while a character was offline. Import the skill queue as well and reconcile entries whose completion time has passed; mark ambiguous results for in-game verification rather than treating them as confirmed.

The skills and industry-jobs endpoints do not directly promise a current free-slot counter. The project should derive maximum job capacity from verified skill state and subtract relevant active jobs only after the applicable slot rules have been verified. Keep derived values and calculation provenance separate from API-reported facts.

## Facility-access limitation

ESI cannot simply return a complete list of every Upwell structure a character is allowed to dock at or use for industry.

- `/industry/facilities/` is a public facility directory. It does not prove a particular character can dock at or use every listed facility.
- Authenticated character search can search for structures accessible to that character, but it is a name-based search, not a universal ACL inventory endpoint.
- The authenticated structure resolver works only when the character has docking access to the specified structure ID.
- A structure's existence or docking access does not, by itself, prove that its Industry service is installed, fueled, available to the character, or economically attractive.
- Current industry jobs and asset locations can reveal facilities already used, but do not prove access to every other facility.

Accordingly, facility status must be stored as `verified`, `partial`, or `unknown`. Never infer complete facility access from the public directory alone. After the alliance is known, facility names/IDs can be imported from its documentation or supplied in-game, searched against the character, and checked against published facility/service data. Corporation structure endpoints are a separate permission path and may require specific corporate roles; they are not part of the initial character-only scope set.

## Scopes deliberately deferred

Do not request every available ESI permission. The initial authorization should request only the seven character read/search scopes listed above.

Defer until the use case exists:

- Structure-market orders: `esi-markets.structure_markets.v1`, after target structures and market access are known.
- Corporation assets, blueprints, jobs, facilities, or structures: separate corporation scopes and applicable corporate roles; membership alone does not imply access.
- Wallet, mail, contacts, location tracking, or any write/action scope: not required for the current manufacturing data import.
- Alliance buyback rules, doctrine fittings, courier rates, staging policies, and shared-resource terms: obtain from alliance documents, market/contract data, or user-supplied exports as appropriate. SSO does not automatically expose every alliance program or permissioned corporate record.

## Local security and data boundaries

- Register one EVE SSO application using **Authentication & API Access** and the native/desktop Authorization Code with PKCE flow.
- Use a local loopback callback URI that exactly matches the URI registered in the developer portal. The implementation will use `http://127.0.0.1:8765/callback/`.
- Use PKCE S256, random state, exact redirect matching, and validation of the returned EVE SSO token.
- Do not use or store the application client secret in a native PKCE flow.
- Store refresh tokens in the operating system credential store (Windows Credential Manager on the user's Windows machine), not in the repository, Dropbox, or exported reports.
- Store raw authenticated ESI responses and normalized character profiles under Git-ignored `data/private/` and `local/` paths.
- No character IDs, names, skill lists, blueprint IDs, assets, location IDs, refresh tokens, or balances may enter tracked Git files by default.
- Do not upload raw authenticated snapshots or the populated operating profile to Dropbox. Share only deliberately redacted readiness summaries.
- Public SDE and public ESI collection/calculation must remain functional when SSO is disconnected or authorization is revoked.

## Implementation sequence

1. [x] Build a local PKCE authorization client and OS credential-store integration. The helper is implemented in `tools/esi/sso_local.py`; live SSO exchange still awaits user application registration.
2. [ ] Authorize each of the three characters individually using the minimum scope set.
3. Import and validate skills, skill queue, blueprints, assets, and active industry jobs into timestamped local snapshots.
4. Populate the local operating profile from those snapshots, while retaining original source responses for reproducibility.
5. Build facility discovery using the public facilities directory plus targeted character structure searches; explicitly retain gaps in facility coverage.
6. Verify job-capacity calculations and a sample of imported blueprint/asset data against the in-game client.
7. After the alliance is selected, ingest doctrine fittings, buyback prices/terms, staging markets, accessible facilities/services, and courier/self-haul constraints.
8. Then select candidates across alliance-local manufacture, higher-value export production, and other opportunistic work. Run fresh market collection only for selected candidate routes, inputs, outputs, and quantities.

## Verification and stop conditions

- Every snapshot records character identity, authorization scopes, retrieval time, endpoint URL, ESI cache metadata/ETag where available, compatibility date, and source hashes.
- Missing scopes, stale skills, incomplete pagination, inaccessible structures, and partial asset locations must be explicit. Never silently convert them into zero or no-access.
- Authentication is read-only. No market orders, industry jobs, contracts, or in-game actions are created by this integration.
- Authorization failure or revocation must leave local files intact and must not trigger repeated login prompts.
- A successful SSO token is not proof of alliance program eligibility or facility service access.

## Official references

- [CCP EVE SSO documentation](https://developers.eveonline.com/docs/services/sso/)
- [CCP native/desktop PKCE flow](https://docs.esi.evetech.net/docs/sso/native_sso_flow.html)
- [CCP SSO application creation guide](https://docs.esi.evetech.net/docs/sso/creating_sso_application.html)
- [CCP ESI quick reference](https://developers.eveonline.com/blog/esi-quick-reference-for-new-developers)
- [CCP authenticated structure search](https://developers.eveonline.com/blog/simplify-esi-queries-by-using-search)
- [ESI structure resolution and discovery limitations](https://docs.esi.evetech.net/docs/scenarios/resolve_structure_ids.html)
- [ESI API Explorer](https://esi.evetech.net/ui/?version=latest)
