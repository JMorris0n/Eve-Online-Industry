---
type: Process
title: Tech II Production Playbook
description: Operational workflow from Tech I BPO copying and invention through Tech II manufacturing and sale.
tags:
  - playbook
  - t2
  - copying
  - invention
generated:
  by: openai/gpt-6
  at: 2026-11-14T09:50:00Z
status: draft
---

## Objective

Coordinate the Science and Manufacturing stages required to produce Tech II output while controlling BPC supply, invention variance, component availability, and working capital.

Use this playbook with [Blueprint Copying](../02-production-systems/blueprint-copying.md), [Tech II Invention](../02-production-systems/tech-2-invention.md), [Tech II Components](../02-production-systems/tech-2-components.md), and the throughput concepts.

## Preflight

- Confirm the target Tech II product and its exact input Tech I BPC.
- Confirm the correct Tech I BPO, ME/TE, copy settings, and licensed-run plan.
- Confirm the required Science and Encryption Methods skills.
- Confirm the invention facility, rigs, tax, SCI, and service state.
- Confirm required datacores and any decryptor.
- Confirm component and reaction supply.
- Confirm available Science and Manufacturing slots.
- Record the current invention probability and output preview from the Industry UI.
- Verify current market prices, installation fees, and expected sale liquidity.

## Copying stage

1. Research the BPO first if the planned copy should inherit improved ME/TE.
2. Configure Job Runs and Runs per Copy separately.
3. Confirm the number of BPCs and total licensed-run capacity.
4. Confirm copy inputs and job fee against the Industry quote.
5. Install the copy job and record its expected completion.
6. After delivery, verify BPC count, ME/TE, and licensed runs.

Do not assume an existing BPC inherits later BPO research. Copies retain the values they had when created.

## Invention stage

1. Select the correct Tech I BPC and verify its remaining licensed runs.
2. Select the intended item-specific invention skills and decryptor.
3. Review the displayed success probability and output preview.
4. Confirm datacore, decryptor, and other inputs from the actual job quote.
5. Choose a run count that fits the available BPC runs and Science slots.
6. Install the job and record attempts, inputs, probability, and expected successful outputs.
7. On delivery, record actual successes/failures and the resulting Tech II BPC run/ME/TE values.

Expected successes are not guaranteed successes. Maintain an appropriate BPC buffer and do not schedule final manufacturing as though every invention attempt will succeed.

## Component and reaction stage

- Build or buy required Advanced Components.
- Confirm reaction inputs, reactor family, fuel blocks, and output quantities.
- Use actual facility and job quotes.
- Stage materials at the facility where the downstream job will be installed.
- Avoid double-counting internal component costs when consolidating the full chain.

## Tech II manufacturing stage

1. Confirm Tech II BPC licensed runs and output quantity.
2. Confirm required components and other inputs are present.
3. Obtain the live Manufacturing quote.
4. Check material rounding, installation fee, and job duration.
5. Install jobs within available Manufacturing slots.
6. Record job IDs, inputs, and expected output.
7. Deliver and reconcile output and remaining BPC runs.

## Sale and review

Use [Market Delivery](market-delivery.md) to choose immediate liquidation or sell-order execution. Reconcile invention cost across successful output, not only successful attempts. Include failed-attempt inputs in the expected cost of the successful BPC supply.

Record actual invention success rate, output BPC properties, component costs, job fees, manufacturing time, sale proceeds, and liquidation time.

## Stop conditions

Do not proceed if the invention preview, decryptor output, required inputs, component recipe, or BPC licensed runs are inconsistent with the plan. Record unresolved mechanics in the verification queue rather than silently assuming the calculator is correct.
