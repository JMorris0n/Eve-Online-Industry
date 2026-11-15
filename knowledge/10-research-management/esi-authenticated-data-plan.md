# Local EVE SSO and null-sec operating-data plan

**Status:** Approved strategic direction. The local PKCE SSO client and snapshot-to-profile importer are implemented and regression-tested. The first three-character live sync and profile import are complete. The latest redacted readiness report is schema-valid with zero errors and confirms verified skill inventories for all three characters (358, 55, and 59 known skills), with all three Manufacturing, Science, and Reaction pools reporting available capacity on every character. Slot 2's previously pending completed skill-queue level was applied after the user logged into that character and refreshed only its snapshot; no reauthorization was required. Personal blueprint coverage is verified for 375 records, while operation-wide blueprint coverage remains partial because corporation-owned blueprints are not included. Personal assets are normalized into a local, location-aware ledger; the latest redacted report confirms 3,681 asset records and 168 candidate stock lines, all on character slot 1. The candidate lines remain unconfirmed pending in-game location, quantity, and Industry-input checks. In-game job-slot reconciliation, facility/market access, and manual operating inputs remain open. 
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
| Active and trained skill levels | `GET /characters/{character_id}/skills/` | `esi-skills.read_skills.v1` | Import active skill levels for current capability and use trained levels to reconcile the skill queue |
| Skill queue | `GET /characters/{character_id}/skillqueue/` | `esi-skills.read_skillqueue.v1` | Reconcile skill completions that may not yet appear in the skills endpoint |
| Personal blueprint inventory | `GET /characters/{character_id}/blueprints/` | `esi-characters.read_blueprints.v1` | Import blueprint type, location, BPO/BPC quantity, ME, TE, and remaining runs |
| Personal assets | `GET /characters/{character_id}/assets/` | `esi-assets.read_assets.v1` | Locate stored inputs, components, ships, and useful inventory; resolve location/item names where supported |
| Personal industry jobs | `GET /characters/{character_id}/industry/jobs/` | `esi-industry.read_character_jobs.v1` | Derive current free job slots from active, paused, and ready job records; the sync requests recent completed jobs as well |
| Search known accessible Upwell structures | `GET /characters/{character_id}/search/` with `categories=structure` | `esi-search.search_structures.v1` | Resolve structure IDs by a known or supplied structure-name query |
| Resolve a known Upwell structure | `GET /universe/structures/{structure_id}/` | `esi-universe.read_structures.v1` | Retrieve structure name, system, type, and owner when the character has docking access |
| Public industry facility directory | `GET /industry/facilities/` | Public; no SSO scope | Discover publicly accessible industrial facilities and published facility data |

The skills endpoint exposes both `active_skill_level` and `trained_skill_level`. Active level can be lower than trained level because of Alpha clone limits or active expert systems; use active level for current recipe eligibility and job-slot bonuses. Use trained level when checking whether a queue entry with a finish time in the past is reflected by the skills response. Import the skill queue as well and mark ambiguous results partial rather than treating them as confirmed.

The skills and industry-jobs endpoints do not directly promise a current free-slot counter. The importer derives theoretical job capacity from active skill levels and subtracts occupied jobs by pool: Manufacturing = 1 + Mass Production + Advanced Mass Production; Science = 1 + Laboratory Operation + Advanced Laboratory Operation; Reaction = 1 + Mass Reactions + Advanced Mass Reactions. CCP documents these job categories and per-level skill additions in [Activities and Job Types](https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types). Activity IDs 1, 3, 4, 5, 7, 8, and 9 map respectively to Manufacturing, Science research/copying/reverse engineering/invention, and Reaction. Jobs in active, paused, or ready status occupy a slot; delivered, cancelled, and reverted jobs do not.

### Completed skill training while a character is offline

ESI documents an expected difference between the skills and skillqueue endpoints. A skillqueue entry whose `finish_date` is in the past is complete, but the new level may not yet appear in `/skills`; ESI states that it is applied the next time that character logs in. The skills endpoint documentation explicitly says to apply past-finish queue entries over the returned skills list to derive the current trained-skill state. See the [ESI skillqueue route](https://esi.evetech.net/ui/?version=latest#/Skills/get_characters_character_id_skillqueue) and [ESI skills route](https://esi.evetech.net/ui/?version=latest#/Skills/get_characters_character_id_skills).

The current importer deliberately marks this condition partial instead of guessing the active level, which can differ from trained level under clone restrictions or temporary effects. If the redacted readiness report contains `completed_skill_queue_level_not_reflected` for a character slot:

1. Identify that slot's character locally using `data/private/esi/profile-import-manifest.json`. Do not share the mapping.
2. Log into that EVE character once so the completed training is applied.
3. Run a targeted snapshot sync for that character with `py -3 tools/esi/sso_local.py sync --character-id CHARACTER_ID --compatibility-date 2026-11-13`.
4. Re-run `py -3 tools/profile/import_esi_profile.py`, validate the private profile, and regenerate the redacted readiness report.

The `--character-id` option refreshes only the selected character. Existing fresh snapshots for the other characters remain in use. This condition does not require a new SSO authorization. The ESI cache transition to event-based invalidation is separate from this game-state behavior; CCP's [2026-01-27 caching update](https://developers.eveonline.com/blog/smarter-caching-when-events-drive-invalidation) describes how skill and skillqueue endpoint caches are invalidated.

The local sync requests completed job records to avoid silently omitting recent ready-to-deliver jobs. ESI completed-job history is limited to the past 90 days. If a ready-to-deliver job may be older than 90 days, reconcile the calculated free slots against the in-game Industry window before treating the slot count as definitive. Keep derived values and calculation provenance separate from API-reported facts.

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
- Use PKCE S256, random state, exact redirect matching, and validation of the returned EVE SSO token. CCP documents the accepted JWT `iss` claim as either `https://login.eveonline.com` or `login.eveonline.com`, with no trailing slash.
- Do not use or store the application client secret in a native PKCE flow.
- Store refresh tokens in the operating system credential store (Windows Credential Manager on the user's Windows machine), not in the repository, Dropbox, or exported reports.
- Store raw authenticated ESI responses and normalized character profiles under Git-ignored `data/private/` and `local/` paths.
- No character IDs, names, skill lists, blueprint IDs, assets, location IDs, refresh tokens, or balances may enter tracked Git files by default.
- Do not upload raw authenticated snapshots or the populated operating profile to Dropbox. Share only deliberately redacted readiness summaries.
- Public SDE and public ESI collection/calculation must remain functional when SSO is disconnected or authorization is revoked.

## Implementation sequence

1. [x] Build a local PKCE authorization client and OS credential-store integration in `tools/esi/sso_local.py`; validate issuer, audience, scopes, callback state, and PKCE.
2. [x] Complete separate authorization grants for all three characters. The user reports all three authorizations succeeded; the local registry can be checked with `py -3 tools/esi/sso_local.py list`.
3. [x] Implement an offline snapshot-to-profile importer with snapshot hash/freshness checks, active-skill normalization, job-slot derivation, personal blueprint normalization, and redacted readiness output. Regression tests cover these transformations.
4. [x] Run the first live three-character ESI sync; the redacted readiness report confirms three fresh snapshots and no stale snapshots.
5. [x] Execute the local profile importer and review the redacted readiness report; it is schema-valid with zero validation errors and confirms 375 personal blueprint records.
6. [x] Resolve the partial skills state for character slot 2. The user logged into that character and refreshed only its snapshot; the latest readiness report now verifies skill and capacity state for all three characters.
7. [ ] Reconcile derived free job capacity against the in-game Industry window for each character, including any ready-to-deliver jobs older than ESI's 90-day completed-job history window.
8. [x] Run the local personal asset ledger against the three character snapshots; it produced 3,681 records and 168 conservative candidate stock lines.
9. [x] Review the redacted asset-ledger readiness report. All three snapshots are fresh; the 168 candidate stock lines are concentrated on character slot 1.
10. [ ] Generate a private item/location reconciliation CSV with SDE item names and resolved NPC station names. Keep the CSV local because it contains exact IDs and quantities.
11. [ ] Reconcile candidate locations and quantities against the in-game inventory and check whether selected inputs appear as available in the Industry UI. Keep non-station and ambiguous locations excluded.
12. [ ] Review personal blueprint counts against the client and confirm that personal blueprints are excluded from material-stock candidates.
13. [ ] Build facility discovery using the public facilities directory plus targeted character structure searches; explicitly retain gaps in facility coverage.
14. [ ] After the alliance is selected, ingest doctrine fittings, buyback prices/terms, staging markets, accessible facilities/services, and courier/self-haul constraints.
15. [ ] Then select candidates across alliance-local manufacture, higher-value export production, and other opportunistic work. Run fresh market collection only for selected candidate routes, inputs, outputs, and quantities.

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
