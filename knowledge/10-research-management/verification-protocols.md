---
type: Process
title: Verification Protocols
description: Reproducible in-game and data-pipeline tests for validating industrial mechanics, formulas, and operational assumptions.
tags:
  - verification
  - testing
  - methodology
generated:
  by: openai/gpt-6
  at: 2026-11-14T10:40:00Z
status: draft
---

## Purpose

These protocols turn documented but unverified claims into reproducible tests. A test should isolate one variable at a time, preserve the inputs and observed output, and record enough context for another person to repeat it.

A protocol is not evidence that a claim is correct. A claim becomes verified only after the test is actually performed, its result is recorded, and an independent reviewer checks the evidence.

## General test record

| Field | Required information |
|---|---|
| Test ID | Protocol ID plus a unique run identifier |
| Date/time | UTC timestamp |
| Client build | Current EVE client/build and patch context |
| Character context | Relevant skills and Alpha/Omega state; do not store credentials |
| Facility | Station/structure, system, service module, rig family/size, tax |
| Activity | Manufacturing, research, copying, invention, reaction, PI, or market |
| Item context | Type ID, blueprint/formula ID, ME/TE, licensed runs |
| Inputs | Exact quantities, prices, and source |
| Expected result | Formula and source used for prediction |
| Observed result | Industry/PI UI values, job quote, delivered output |
| Evidence | Screenshots, exported data, job IDs, or source snapshots |
| Conclusion | Pass, fail, inconclusive, or superseded |
| Reviewer | Person who independently reviewed the result |

Never store EVE SSO tokens, refresh tokens, client secrets, or authorization headers in a test record or repository.

## Test design rules

1. Change one variable at a time whenever possible.
2. Keep the character, blueprint, facility, system, job runs, and material prices constant when comparing one modifier.
3. Use the smallest practical job that still exposes the mechanic being tested.
4. Record the live Industry quote before installing a job.
5. Record delivered output and actual consumed inputs after completion.
6. Repeat a test when randomness is involved; do not infer probability from one outcome.
7. Distinguish a failed prediction from a failed game mechanic. The formula or input data may be wrong.
8. Record the exact client build and date because patches can change mechanics.
9. Do not mark a concept verified from model agreement or an unrepeatable anecdote.
10. If the test is too expensive or risky, record the limitation and use a safer representative item.

## VP-001: ME material rounding

**Claims:** ME reduces material requirements by 1% per level; material rounding occurs at the job level; single-item-per-run inputs are not reduced.

**Procedure:**
1. Select a BPO with at least one ordinary material line that produces a fractional quantity at a chosen ME/run count.
2. Record the unresearched material requirement for a fixed job run count.
3. Record the same job at a known ME level.
4. Compare small and larger run counts to expose job-level rounding.
5. Include a material that requires exactly one item per run, where available.
6. Compare the quote with the expected job-level calculation.

**Capture:** BPO type ID, ME, run count, per-run base quantity, quoted quantity, facility, rig, and job ID.

**Pass condition:** The observed material quantities match the documented calculation and rounding behavior for all tested lines.

## VP-002: BPC copying parameters

**Claims:** Job Runs determines the number of BPCs; Runs per Copy determines licensed runs per BPC; copy duration is based on total licensed runs; copy input materials, where required, scale with Job Runs.

**Procedure:**
1. Select a BPO whose Copy activity has a known maximum Runs per Copy.
2. Configure two copy jobs with equal total licensed runs but different Job Runs/Runs per Copy combinations.
3. Record quoted inputs, fee, and duration for both.
4. If the BPO has copy-specific input materials, compare the quantity between configurations.
5. Deliver one job and inspect the number of BPCs, ME/TE, and licensed runs.
6. Repeat with a BPO that requires exceptional copy materials if available.

**Pass condition:** Observed BPC count, licensed runs, inherited ME/TE, input quantities, and time agree with the documented rules.

## VP-003: Character job slots and remote range

**Claims:** Manufacturing, Science, and Reaction use separate slot pools; slot totals follow the documented skill formulas; remote-start skills extend range by five jumps per level.

**Procedure:**
1. Record all six job-slot skill levels and the relevant remote skill levels.
2. Calculate expected slot counts from the formulas.
3. Compare against the Industry window's available/active job counts.
4. Test remote job installation at a location inside the character's range.
5. Where safe, test a location just outside the range.
6. Repeat for each job type that the character can operate.

**Capture:** Skill levels, Alpha/Omega state, active jobs by activity, destination system, jump count, and result.

**Pass condition:** Available job slots and remote-start eligibility match the formulas and skill ranges.

## VP-004: Facility role and rig modifiers

**Claims:** Structure role bonuses and rigs modify activity-specific material use, job time, or installation fees.

**Procedure:**
1. Choose one blueprint/formula and a fixed run count.
2. Obtain a quote at a baseline facility.
3. Obtain a quote at a facility with a known role bonus.
4. Compare a matching facility with and without the relevant rig, if possible.
5. Keep character skills, blueprint quality, system, and run count constant wherever possible.
6. Repeat for different activity types rather than assuming Manufacturing, Science, and Reaction effects are interchangeable.

**Capture:** Facility type, role bonus, service, rig family/size, system security, SCI, material quantity, job duration, and fee.

**Pass condition:** The observed quote differences match the activity-specific documented modifiers.

## VP-005: Installation fee and SCC surcharge

**Claims:** Installation fees use EIV, activity SCI, applicable structure/rig cost modifiers, facility tax, SCC surcharge, Alpha tax, and any region-specific surcharge. The latest CCP statement describes a temporary 2% ME/TE research SCC surcharge rather than the 4% baseline.

**Procedure:**
1. Select a representative Manufacturing job and record the full quote.
2. Record the same data for a ME research job and a TE research job.
3. Record copying, invention, and reaction quotes where available.
4. Capture EIV or the UI's process-value basis, SCI, facility tax, structure/rig effects, SCC, Alpha state, and region.
5. Compare the calculated fee with the quote.
6. Repeat at an NPC station and an Upwell facility if possible.

**Capture:** Activity, EIV/process value, SCI, taxes, rig/role, system, clone state, quote fee, and calculated fee.

**Pass condition:** The fee model reconciles with the live quote. Keep activity-specific EIV and SCC values separate if the UI shows different treatment.

## VP-006: Tech II invention

**Claims:** Invention chance formula, item category base chance, skill multipliers, decryptor effects, input consumption, and output BPC properties.

**Procedure:**
1. Select an inventible Tech I BPC and record its item type and remaining runs.
2. Record the required Encryption Methods and Science skills.
3. Record the Industry UI success chance with no decryptor.
4. Record chance and output preview for each decryptor under test.
5. Record the exact input quantities for a multi-run job.
6. Deliver the job and record successes, failures, and output BPC runs/ME/TE.
7. Repeat enough attempts to compare observed results with the expected binomial distribution.

**Capture:** Product, skills, chance, decryptor, attempts, datacores, BPC runs consumed, job fee, duration, output count, output BPC properties.

**Pass condition:** UI chance/output preview and observed input/output behavior match the documented formula and item-specific rules. Random outcomes alone do not prove or disprove the probability formula.

## VP-007: Reaction formula and facility effects

**Claims:** Reaction inputs/outputs/fuel, reactor-family restrictions, Reactions skill time bonus, Tatara role bonus, and reaction rig effects.

**Procedure:**
1. Select one formula and record its reactor family.
2. Confirm the Refinery service and system security.
3. Record the formula's input, output, and fuel quantities for a fixed run count.
4. Obtain a quote at a baseline facility.
5. Compare an eligible Tatara or rigged Refinery quote while keeping other variables constant.
6. Deliver the job and reconcile actual inputs, fuel, output, duration, and fee.

**Capture:** Formula ID, reactor family, facility, system, rig, Reactions skill, run count, inputs, fuel, output, time, and fee.

**Pass condition:** The observed recipe and quote match the formula and documented facility/skill modifiers.

## VP-008: Alpha PI import/export restriction

**Claims:** Alpha clones can import materials into a colony but cannot export colony goods.

**Procedure:**
1. Review the current CCP Alpha/Omega support page and quick facts.
2. With an Alpha clone, inspect the colony transfer interface.
3. Confirm whether importing to the colony is available.
4. Confirm whether exporting colony goods is blocked.
5. Repeat after the character becomes Omega only if available and safe.

**Capture:** Clone state, UI action availability, transfer direction, and date/client build.

**Pass condition:** Observed import/export permissions match current CCP clone-state documentation.

## VP-009: ESI collector smoke test

**Claims:** The local collector respects compatibility dates, cache headers, ETags, X-Pages, rate limits, and stores provenance.

**Procedure:**
1. Configure one region and one common item type ID.
2. Run the collector with a reviewed compatibility date.
3. Inspect the timestamped output directory and manifest.
4. Confirm market order pages, market history, system indices, and adjusted-price output are valid JSON.
5. Run a second time before cache expiry and confirm cache hits.
6. Run after expiry and confirm conditional requests where the endpoint supports them.
7. Confirm no EVE SSO token or private character data is requested.

**Capture:** Config, compatibility date, manifest, request log, file hashes, response headers, and errors.

**Pass condition:** Data parses, cache behavior is correct, pagination is complete, and provenance is preserved.

## VP-010: SDE acquisition and schema inspection

**Claims:** The local SDE downloader resolves the current build, verifies the archive, and preserves build/hash metadata.

**Procedure:**
1. Run the downloader for JSONL.
2. Record the build number and manifest.
3. Confirm SHA-256 and ZIP integrity test pass.
4. Run the archive inspector.
5. Record relevant filenames and sample records for types, blueprints, reaction formulas, and planetary schematics.
6. Compare the observed layout with CCP's current SDE schema documentation before implementing parsers.

**Capture:** Build number, archive URL, hash, manifest, inspector output, and schema documentation version.

**Pass condition:** The archive is valid and the current schema is understood well enough to write a deterministic parser.

## Test result template

Copy this block into a dated test record:

```yaml
test_id: VP-000
run_id: YYYYMMDD-001
date_utc: YYYY-MM-DDTHH:MM:SSZ
client_build:
character_context:
  clone_state:
  relevant_skills: {}
facility:
  name:
  system:
  service:
  rigs: []
activity:
item_type_id:
blueprint_or_formula_id:
job_settings: {}
expected:
  source:
  values: {}
observed:
  values: {}
evidence:
  - path_or_url:
result: pending
reviewer:
notes:
```

## Related concepts

- [Claims Requiring Verification](claims-requiring-verification.md)
- [Open Questions](open-questions.md)
- [Research Backlog](research-backlog.md)
- [Data Quality and Reconciliation](../07-tools-and-data/data-quality.md)
- [Research Standards](../00-governance/research-standards.md)
