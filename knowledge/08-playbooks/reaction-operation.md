---
type: Process
title: Reaction Operation Playbook
description: Operational workflow for sourcing inputs, scheduling, running, and collecting reaction jobs.
tags:
  - playbook
  - reactions
generated:
  by: openai/gpt-6
  at: 2026-11-14T09:50:00Z
status: draft
---

## Objective

Run reaction jobs reliably in a compatible Upwell Refinery while controlling formula inputs, fuel blocks, facility effects, job slots, and downstream demand.

Use [Reactions](../02-production-systems/reactions.md), [Reaction Throughput](../05-optimization/reaction-throughput.md), and [Facilities and Rigs](../01-foundations/facilities-and-rigs.md).

## Preflight

- Identify the exact Reaction Formula and reactor family.
- Confirm the target system is eligible for reactions.
- Confirm the Refinery has the compatible reactor service online.
- Confirm the character's Reaction slots and Reactions skill.
- Record Tatara/Athanor role, rig family/size, security class, SCI, tax, and service state.
- Obtain the live Industry quote.
- Confirm all formula inputs and fuel blocks are available at the facility.
- Confirm output storage, downstream demand, and transport plan.

## Install and operate

1. Select the formula and confirm the correct activity.
2. Enter the run count.
3. Compare the displayed input, fuel, and output quantities with the stored recipe.
4. Compare job duration and fee with the planned values.
5. Install the job and record job ID, inputs, start time, and expected completion.
6. Monitor facility service state and structure risk.
7. Deliver the completed job and verify output and remaining input stock.

## Scheduling and inventory

- Allocate Reaction slots according to output demand and contribution per slot-hour.
- Maintain enough input stock to avoid slot idle time.
- Avoid producing intermediates faster than downstream consumption or market absorption.
- Coordinate reaction completion with component Manufacturing schedules.
- Keep formula families and rig applicability separate.
- Include hauling and working capital in the batch economics.

## Reconciliation

Record actual output, fuel blocks consumed, material use, duration, installation fee, and any discrepancy from the quote. If a formula or rig result differs from the model, stop scaling that formula until the difference is explained.

## Stop conditions

Do not install if the refinery service, reactor family, system security, rig configuration, inputs, or fee quote is uncertain. Record the question in the verification queue.
