---
type: Process
title: Tech I Production Playbook
description: Operational checklist for planning, launching, delivering, and selling Tech I manufacturing jobs.
tags:
  - playbook
  - t1
  - manufacturing
generated:
  by: openai/gpt-6
  at: 2026-11-14T09:50:00Z
status: draft
---

## Objective

Run a repeatable Tech I manufacturing batch with correct materials, facility, job settings, cost capture, and output disposition.

This playbook assumes the product has already passed [Product Evaluation](product-evaluation.md).

## Preflight

### Blueprint and character

- Confirm the correct BPO or BPC and its location.
- Record ME, TE, licensed runs, and output quantity per run.
- Confirm the character has the required skills and a free Manufacturing slot.
- Confirm BPO/BPC concurrent-use and run limits for the selected job.
- Ensure the blueprint and materials will be at the selected facility.

### Facility

- Confirm Manufacturing service is online and accessible.
- Record system, activity SCI, structure role, rig type/size, security class, facility tax, SCC, and Alpha status.
- Confirm structure access and service-module continuity.
- Obtain the live Industry job quote.

### Materials and economics

- Compare quoted material quantities with the planned bill of materials.
- Include owned materials at replacement/opportunity value.
- Confirm sufficient stock for the entire job.
- Record installation fee, duration, and expected output.
- Confirm the intended sale route and market depth.

## Job installation

1. Select the intended blueprint and Manufacturing activity.
2. Enter the planned run count.
3. Confirm output quantity and all material quantities.
4. Compare the Industry quote with the stored calculation.
5. Record the job duration and installation fee.
6. Install the job only after material, blueprint, and facility checks pass.
7. Record the job ID, start time, expected completion, and input stock consumed.

Do not rely on an estimated material formula if the live Industry quote is available. Material rounding is applied per installed job.

## While the job runs

- Track completion time and any operational disruption.
- Avoid assuming the output can be sold at the original market price if the job duration is long.
- Refresh the market snapshot before delivery if prices or volume are volatile.
- Prepare the destination market or hauling plan.

## Delivery and reconciliation

1. Deliver the completed job.
2. Confirm the actual output quantity.
3. Confirm remaining BPC runs or BPO availability.
4. Compare delivered output and actual material use with the quote.
5. Record the final job duration and fee.
6. Move or list output according to the sale plan.
7. Record unsold inventory separately from realized proceeds.

## Post-batch review

Calculate actual net contribution, unit contribution, margin, ISK per slot-hour, peak capital, and liquidation time. Record any variance in materials, job time, fee, price, or volume.

## Stop conditions

Pause before installation if the facility, blueprint, materials, job quote, or sale path differs materially from the approved evaluation. Pause after delivery if the output or material consumption does not match the expected result; investigate before scaling.
