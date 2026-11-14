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

An empty skill map means "not recorded", not "untrained". A null capacity or capital value means unknown, not zero. Do not mark a record verified merely because a value was estimated.

## Character records

Exactly three character slots are represented. Use labels such as "Manufacturing", "Science", or "Market" if role labels help, but do not assume a character's specialization until its trained skills and available slots have been checked.

Skill levels are integers from 0 to 5. The profile records the skills needed by the candidate products; it is not necessary to export every skill at the outset. Job capacities are separate fields for Manufacturing, Science, and Reaction.

## Blueprints and facilities

Blueprint records use SDE type IDs, distinguish BPO from BPC, and include ME, TE, licensed runs, quantity, and a local location label where known. For a BPO, quantity is the number of owned copies; for a BPC, quantity is the number of copies with the same recorded properties. Keep distinct ME/TE/run variants as separate records.

Facility records describe only facilities you can actually access. Record available services, relevant rigs, system ID, and tax rate only when known. Structure names and access details remain local.

## Capital and operating constraints

Use integer ISK values. Keep working capital, liquidity reserve, and maximum capital at risk separate. Operating constraints include active hours per week, maximum acceptable setup time per batch, target liquidation horizon, and qualitative risk tolerance.

These are planning limits, not a request to disclose balances in the public repository. Enter only the amount you intend to allocate to this operation.

## Validate the private profile

After entering values, run:

```powershell
py -3 tools/profile/validate_profile.py --profile local/operating-profile.json
```

The validator uses only the Python standard library. It checks the three character slots, skill levels, job-pool capacities, capital fields, operating limits, facilities, and blueprint records. Unknown values may remain null; they are not interpreted as zero. The public example is also covered by automated unit tests.

## Current limitations

This is the first profile contract and structural validator, not yet a feasibility engine. The next implementation step is to use the profile to distinguish eligible, ineligible, and unknown character/blueprint/facility requirements. Do not use the template as a profitability recommendation by itself.
