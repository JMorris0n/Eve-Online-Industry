---
type: Concept
title: Claims Requiring Verification
description: Documented or legacy claims that still need independent testing or live confirmation.
tags:
  - research
  - verification
generated:
  by: openai/gpt-6
  at: 2026-11-14T10:40:00Z
status: draft
---

## Intake rule

Place imported, legacy, or model-generated claims here when they may be useful but are not yet independently supported. Do not copy them into stable mechanic documents as verified facts. The existence of a source-backed concept does not mean its claims have passed in-game verification.

## Documented claims awaiting independent verification

- [ ] **Tech II invention:** formula, base chances, skill multipliers, decryptor modifiers, output BPC runs/ME/TE, and multi-run input consumption. Documentation exists; verify against the Industry UI and repeated outcomes. See [VP-006](verification-protocols.md#vp-006-tech-ii-invention).
- [ ] **Installation fees:** Manufacturing EIV, activity-specific value bases, SCI, structure/rig modifiers, SCC surcharge, Alpha tax, and regional surcharge. Documentation exists; reconcile with live quotes. See [VP-005](verification-protocols.md#vp-005-installation-fee-and-scc-surcharge).
- [ ] **ME/TE research SCC surcharge:** CCP's latest explicit statement is 2% for ME/TE research, described as temporary in 2025-07. No later official reversal was found as of 2026-11-14; verify the live quote. See [Installation Costs](../01-foundations/installation-costs.md).
- [ ] **Facility role bonuses and rigs:** verify material, time, and fee effects by activity, rig family/size, and security class. See [VP-004](verification-protocols.md#vp-004-facility-role-and-rig-modifiers).
- [ ] **Manufacturing time modifiers:** verify skill, facility, rig, and other modifier stacking against matched Industry quotes.
- [ ] **Reaction formulas:** verify current input/output/fuel quantities, run limits, reactor-family compatibility, and reaction-rig effects using the SDE and live formulas. See [VP-007](verification-protocols.md#vp-007-reaction-formula-and-facility-effects).
- [ ] **Planetary Industry:** rebuild the full schematic/commodity matrix from the current SDE and verify current colony/transfer behavior. Alpha import/export behavior is now source-backed but should be confirmed in the current UI. See [VP-008](verification-protocols.md#vp-008-alpha-pi-importexport-restriction).
- [ ] **Character job capacity:** verify Manufacturing, Science, and Reaction slot counts, Alpha limits, and remote-start ranges for representative skill states. See [VP-003](verification-protocols.md#vp-003-character-job-slots-and-remote-range).
- [ ] **Market fees:** reconcile broker fees, sales tax, relist fees, and skill/standing effects with live order quotes and wallet journal entries.
- [ ] **BPC copying:** verify copy time, copy-specific inputs, inherited ME/TE, and concurrent BPO restrictions. See [VP-002](verification-protocols.md#vp-002-bpc-copying-parameters).
- [ ] **ME material rounding:** verify job-level rounding and single-item-per-run exceptions. See [VP-001](verification-protocols.md#vp-001-me-material-rounding).
- [ ] **SDE/ESI tooling:** run local acquisition/collector scripts and validate build/schema, cache handling, pagination, and hashes. See [VP-009](verification-protocols.md#vp-009-esi-collector-smoke-test) and [VP-010](verification-protocols.md#vp-010-sde-acquisition-and-schema-inspection).

## Tech III production conflicts and open claims

- [ ] CCP Ancient Relics support page (updated 2024-08-29) lists Intact/Malfunctioning/Wrecked base chances of 40%/35%/25%; EVE University Tech 3 Production (last modified 2024-09-22) lists 26%/21%/14%; EVE Ref sampled Small Hull Relic pages show 21%/14% per output. Determine whether SDE values are per-output probabilities rather than total job success chances. Do not use an assumed reconciliation.
- [ ] Capture Industry-window success chances for each relic family/quality with fixed character skills, facility, and optional inputs.
- [ ] Determine current Tech III decryptor availability and effects from the relic job UI; do not transfer the Tech II decryptor table by analogy.
- [ ] Verify exact T3 subsystem and hull datacore quantities, required skills, component recipes, and R.A.M. inputs against current SDE and in-game blueprints.

## Entry format

For each unresolved claim, record proposed wording, origin, affected concept, why it matters, evidence currently available, and the test or source needed to resolve it. Use [Verification Protocols](verification-protocols.md) for repeatable procedures.
