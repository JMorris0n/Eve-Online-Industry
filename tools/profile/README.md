# Local operating profile

The operating profile records the constraints that determine whether an industry opportunity is executable by this operation. The populated profile, import manifest, and raw character snapshots are private local data, not canonical project knowledge.

## Quick start: sync the three characters

Run these commands from the repository root in PowerShell.

First, make sure you have the latest code and that all three refresh-token entries are present:

~~~powershell
git pull --ff-only origin main
py -3 tools/esi/sso_local.py list
~~~

The list should show three authorized characters. Do not paste the list into a public issue or commit it; it contains character identifiers and names.

Fetch one read-only ESI snapshot for each authorized character. Use a compatibility date that has been reviewed in the ESI API Explorer. The following is the date already used for this project:

~~~powershell
py -3 tools/esi/sso_local.py sync --compatibility-date 2026-11-13
~~~

Build the private operating profile and redacted readiness report from those snapshots:

~~~powershell
py -3 tools/profile/import_esi_profile.py
~~~

Validate the populated profile:

~~~powershell
py -3 tools/profile/validate_profile.py --profile local/operating-profile.json
~~~

The importer also writes the readiness report. To regenerate it later without reimporting ESI data:

~~~powershell
py -3 tools/profile/readiness_report.py --profile local/operating-profile.json --output local/profile-readiness.json
~~~

The importer is an offline transformation. It reads the local authorized-character registry and timestamped snapshots; it does not contact EVE, refresh tokens, or upload any data.

## Files and privacy boundary

- config/operating-profile.schema.json: JSON Schema 2020-12 contract.
- config/operating-profile.example.json: safe template with three character slots and unknown values.
- data/private/esi/authorized-characters.json: local character registry created by the SSO tool.
- data/private/esi/snapshots/: timestamped raw ESI responses and per-file hashes.
- data/private/esi/profile-import-manifest.json: local mapping between character IDs and profile slots, import provenance, counts, and warnings.
- local/operating-profile.json: populated private profile. It contains character labels, skill IDs and levels, blueprint type IDs, local location references, and manual operating inputs.
- local/profile-readiness.json: deliberately redacted summary that can be shared for review.

The data/private/ and local/ directories and the local SSO configuration are excluded by .gitignore. Never commit or upload the populated profile, import manifest, raw snapshots, SSO configuration, refresh tokens, asset exports, or other account data. Share only local/profile-readiness.json after checking that it contains no private details.

The importer preserves manual profile sections such as capital, operating constraints, facilities, market access, and logistics. It replaces the imported character skills, current free-slot values, and personal blueprint records from the latest validated snapshots. It maintains stable profile-slot assignments using the private import manifest.

## What the importer populates

### Skills

The importer records the active_skill_level from ESI for every skill in each character's returned skill inventory. This is the level currently usable by the character. ESI's active_skill_level can be lower than trained_skill_level because of Alpha clone limits or active expert systems. The trained level is used only to detect a skill-queue entry whose finish time has passed but whose trained level is not yet reflected by the skills endpoint. See the [ESI skills response schema](https://esi.evetech.net/ui/?version=latest#/Skills/get_characters_character_id_skills).

An empty skill map means "not recorded", not "untrained". Each character has a separate skills_state; only when it is verified can an omitted skill be treated as level zero. A stale snapshot, malformed queue entry, or completed-but-unreflected queue entry lowers the state to partial.

### Current job capacity

The importer derives free jobs by activity pool from the ESI active skill levels and the jobs returned for that character:

| Pool | Maximum jobs |
|---|---|
| Manufacturing | 1 + Mass Production level + Advanced Mass Production level |
| Science | 1 + Laboratory Operation level + Advanced Laboratory Operation level |
| Reaction | 1 + Mass Reactions level + Advanced Mass Reactions level |

These skills add one concurrent job per active skill level. The activity-to-pool mapping follows CCP's [Activities and Job Types](https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types) reference. Manufacturing, Science, and Reaction are separate pools.

Jobs with status active, paused, or ready count as occupying a slot. Jobs with status delivered, cancelled, or reverted do not. Unknown statuses or activity IDs prevent the importer from claiming a fully known free-slot count.

The importer requests completed jobs as well as current jobs so recent ready/completed records are not silently omitted. CCP's ESI documentation limits completed-job history to the past 90 days. Verify the in-game Industry window if a character may have a ready-to-deliver job older than 90 days; ESI history alone cannot rule that out. The readiness report carries this limitation.

The job_capacity values in the profile are current free jobs, not the theoretical maximum. They should be refreshed after jobs are installed or delivered. A null value means unknown, not zero.

### Blueprints

The importer captures the three authorized characters' **personal** blueprint inventories and distinguishes BPOs from BPCs using ESI's blueprint run/quantity markers. A BPO normally has `quantity = -1` and `runs = -1`; a BPC has `quantity = -2` and non-negative `runs`. ESI also permits a positive `quantity` with `runs = -1` for a stack of fresh, unworked BPOs. The importer preserves that positive stack quantity instead of rejecting the record or treating it as a BPC. It retains type ID, BPO/BPC type, copy runs, ME, TE, count, and the local ESI location reference.

blueprints_state remains partial by design because this first import does not retrieve corporation-owned blueprints. The private import manifest and redacted readiness report identify this coverage boundary. An absent personal blueprint is not proof that the corporation does not own or provide one.

The personal blueprint endpoint is authoritative for the returned character inventory, but a blueprint's location does not establish that the character can access an Industry service at that location.

### Assets and industry facilities

The raw personal asset responses are retained in the local snapshots for later location and stock analysis. This first profile importer records asset-record counts but does not yet normalize assets into a material-stock ledger or infer usable input quantities.

The public /industry/facilities/ endpoint is also captured. It does not prove a character can dock at a listed structure, use its Industry service, or access every structure in its corporation/alliance. Therefore facilities_state remains unknown until targeted access and service checks are completed. Structure access must not be inferred from the public directory or from a name search alone.

## Data-state convention

Every major record has a state field:

- unknown: not entered or not yet checked.
- partial: some values are known, but the record is incomplete or has a stated coverage limitation.
- verified: checked against an authoritative in-game or account source, with material caveats recorded.

A null capacity or capital value means unknown, not zero. The root blueprints_state and facilities_state fields indicate whether the corresponding operation-wide inventories are complete. Do not mark a record verified merely because a value was estimated or because a public list exists.

## Manual operating inputs still required

The importer does not infer:

- Working capital, liquidity reserve, or maximum capital at risk.
- Active operator-hours available per week, setup-time tolerance, or target liquidation horizon.
- Risk tolerance.
- Which market locations can actually be used for procurement and sales.
- Facility access, installed Industry services, rig profiles, taxes, or structure ACLs.
- Whether hauling will use personal transport or an alliance courier, and the practical cargo, route, and active-time limits.
- Corporation-owned blueprint inventory or corporation-owned assets/jobs.

Keep these values unknown until they are checked or explicitly selected as operating constraints. These are planning limits, not a request to disclose total account balances; enter only the capital actually allocated to this operation.

## Manual profile setup or recovery

If you need a fresh blank profile, create a private copy of the example:

~~~powershell
New-Item -ItemType Directory -Force local | Out-Null
Copy-Item config/operating-profile.example.json local/operating-profile.json
~~~

This is not normally required before the ESI import. The importer uses the existing local/operating-profile.json when present; otherwise it starts from the public example. Existing valid manual sections are preserved.

Skill keys are SDE skill type IDs as decimal strings. For a manually entered or corrected level, use the character's current active level, not an inactive trained level. Do not infer one character's level from another character.

Facility records should describe only locations where access and Industry services have been confirmed. Market access should distinguish NPC stations from Upwell structures and record whether each location is usable for procurement, sales, or both. Logistics values should remain null until the method, route, cargo constraints, and active hauling time are known.

## SDE skill-requirements reference

The recipe-derived skill reference remains useful for understanding which skills the public SDE assigns to each recipe. It is not needed to populate character skills after the ESI import.

~~~powershell
py -3 tools/sde/build_skill_requirements.py --input data/derived/industry-recipes.jsonl --output data/derived/skill-requirements.json --activity all
~~~

The resulting file describes public recipe requirements only. It does not reveal what any character has trained or currently has active.

## Validate profile and screen recipe feasibility

Validate the private profile:

~~~powershell
py -3 tools/profile/validate_profile.py --profile local/operating-profile.json
~~~

The feasibility screen compares the static SDE recipe requirements with the known character skills, blueprint coverage, and facilities:

~~~powershell
py -3 tools/profile/check_feasibility.py --profile local/operating-profile.json --recipes data/derived/industry-recipes.jsonl --output data/derived/feasibility.json
~~~

Omit --product-type-id to evaluate every recipe in the input file. The optional --product-type-id filter restricts evaluation to a specific output type ID. The report distinguishes eligible, ineligible, and unknown. A missing blueprint or facility is only a definite blocker when the corresponding inventory completeness state is verified. A character's omitted skill counts as level zero only when that character's skills_state is verified.

This is a hard-constraint screen. It does not calculate blueprint ME/TE effects, facility bonuses, job installation fees, material procurement, market access, logistics, or profitability. An eligible result means the profile supports the listed static requirements, not that a job can be installed or that the product is profitable.

## Redacted readiness report

The readiness report contains statuses and counts only. It intentionally omits character labels and IDs, skill IDs and levels, blueprint type IDs, facility/market names and IDs, and all ISK amounts. It includes the snapshot freshness count, personal-blueprint coverage, and the facility/job-history caveats. Share this report for review; do not share the private profile or raw ESI data.
