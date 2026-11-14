# Local operating profile

This profile records the constraints that determine whether a manufacturing opportunity is actually executable by this operation. It is local input, not canonical knowledge.

## Create a private copy

From the repository root in PowerShell:

```powershell
New-Item -ItemType Directory -Force local | Out-Null
Copy-Item config/operating-profile.example.json local/operating-profile.json
```

The `local/` directory is excluded by `.gitignore`. Keep the populated profile there. Do not commit it, paste credentials into it, or include character IDs, access tokens, wallet exports, or other account secrets. The public example is deliberately blank.

## Files

- `config/operating-profile.schema.json`: JSON Schema 2020-12 contract.
- `config/operating-profile.example.json`: safe template with three character slots and unknown values.
- `local/operating-profile.json`: your private working copy (not tracked by Git).

## Data-state convention

Every major record has a `state` field:

- `unknown`: not entered or not yet checked.
- `partial`: some values are entered, but the record is incomplete.
- `verified`: checked against an authoritative in-game or account source, with any caveats recorded.

An empty skill map means "not recorded", not "untrained". Skill keys are SDE skill type IDs as strings, for example \`\"16622\": 4\`. Each character has a separate \`skills_state\`: only when it is \`verified\` can an omitted skill be treated as untrained (level zero). A null capacity or capital value means unknown, not zero. The root \`blueprints_state\` and \`facilities_state\` fields indicate whether the corresponding inventory lists are complete; an absent entry is not proof of non-ownership or non-access unless that inventory is verified. Do not mark a record verified merely because a value was estimated.

## Character records

Exactly three character slots are represented. Use labels such as "Manufacturing", "Science", or "Market" if role labels help, but do not assume a character's specialization until its trained skills and available slots have been checked.

Skill levels are integers from 0 to 5, keyed by SDE type ID. The profile records the skills needed by candidate products; it is not necessary to export every skill at the outset. Record \`skills_state\` as \`partial\` while building the relevant skill list and \`verified\` only when the skill inventory is complete enough for absence to mean level zero. The `job_capacity` values are the number of currently free jobs available in Manufacturing, Science, and Reaction, not a theoretical skill-derived maximum. Update them when jobs are installed or completed; use null when the current free count is unknown.

## Blueprints and facilities

Blueprint records use SDE type IDs, distinguish BPO from BPC, and include ME, TE, licensed runs, quantity, and a local location label where known. For a BPO, quantity is the number of owned copies; for a BPC, quantity is the number of copies with the same recorded properties. Keep distinct ME/TE/run variants as separate records.

Facility records describe only facilities you can actually access. Record available services, relevant rigs, system ID, and tax rate only when known. Structure names and access details remain local.

## Market access and logistics

The optional `market_access` section records locations where the operation can actually procure inputs or sell finished output. For each location, record its region ID, solar-system ID, location ID, whether it is an NPC station or Upwell structure, and the roles it supports (`procurement`, `sales`, or both). Mark the section `verified` only when the list is complete for the markets you intend to use. A public regional ESI order does not prove access to an Upwell structure.

The optional `logistics` section records the preferred method (`self_haul`, `courier`, `either`, or `none`), practical route-jump and cargo-volume limits, and the maximum active hauling time you are willing to spend per batch. Unknown values should remain null. These constraints help flag plans that are technically profitable but operationally inconvenient.

## Capital and operating constraints

Use integer ISK values. Keep working capital, liquidity reserve, and maximum capital at risk separate. Operating constraints include active hours per week, maximum acceptable setup time per batch, target liquidation horizon, and qualitative risk tolerance.

These are planning limits, not a request to disclose balances in the public repository. Enter only the amount you intend to allocate to this operation.

## Authentication is not required for manual profile setup

The current profile validator and readiness report do not connect to EVE, inspect the launcher session, or perform EVE SSO. The local profile is populated manually. A successful validation only confirms the file structure and data types; it does not import or verify character/account data.

The current SDE and public regional market-data steps also do not require character authorization. Character-specific and corporation/structure data may require authenticated ESI routes and route-specific OAuth scopes. Optional local SSO is a later roadmap milestone, not a prerequisite for using this template. Do not enter EVE credentials, access tokens, or refresh tokens in the profile.

## Validate the private profile

After entering values, run:

```powershell
py -3 tools/profile/validate_profile.py --profile local/operating-profile.json
```

The validator uses only the Python standard library. It checks the three character slots, skill levels, job-pool capacities, capital fields, operating limits, facilities, and blueprint records. Unknown values may remain null; they are not interpreted as zero. The public example is also covered by automated unit tests.

## Check recipe feasibility

Once the current SDE has been extracted and normalized, compare its recipes with the local profile:

```powershell
py -3 tools/profile/check_feasibility.py \
    --profile local/operating-profile.json \
    --recipes data/derived/industry-recipes.jsonl \
    --output data/derived/feasibility.json
```

Omit `--product-type-id` to evaluate every recipe in the input file. The optional `--product-type-id` filter restricts evaluation to a specific output type ID. The report distinguishes `eligible`, `ineligible`, and `unknown`. It also checks SDE recipe-field completeness: records with omitted/null material, product, or skill arrays cannot be treated as confirmed feasible. Missing blueprints or facilities only count as definite blockers when the corresponding inventory completeness state is `verified`. A character's omitted skill counts as level zero only when that character's `skills_state` is `verified`.

This is a hard-constraint screen only. It does not calculate blueprint ME/TE effects, facility bonuses, job installation fees, material procurement, market access, or profitability. An eligible result means the profile supports the listed static requirements, not that a job can be installed at this moment.

## Current limitations

The profile validator checks structure and field types. The feasibility evaluator distinguishes eligible, ineligible, and unknown character/blueprint/facility requirements, but remains a hard-constraint screen. Neither tool calculates live market access from permissions, procurement cost, installation quotes, logistics cost, or profitability. An eligible result is not a production recommendation.

## Private profile readiness report

After entering local profile data, run:

```powershell
py -3 tools/profile/readiness_report.py `
    --profile local/operating-profile.json
```

The report contains statuses and counts only. It intentionally omits character labels, skill IDs and levels, blueprint type IDs, facility and market names/IDs, and all ISK amounts. You can share the printed readiness report without sending the private profile. A valid schema does not mean the profile is complete: use the `unfilled_areas` list to identify what still needs verification.
