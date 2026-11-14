---
type: Process
title: Product Evaluation Playbook
description: Repeatable workflow to evaluate an industrial product before committing capital.
tags:
  - playbook
  - product-selection
generated:
  by: openai/gpt-6
  at: 2026-11-14T09:50:00Z
status: draft
---

## Objective

Determine whether a specific product should be manufactured, bought, or avoided under a defined character, facility, market, and capital situation.

This playbook operationalizes [Product Selection](../06-market-intelligence/product-selection.md), [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md), and [Demand and Liquidity](../06-market-intelligence/demand-and-liquidity.md).

## Required inputs

- Product and type ID.
- Blueprint/formula availability and ME/TE or licensed runs.
- Character skills and free job slots.
- Candidate production facility, system, rig, tax, and service state.
- Input source and market region.
- Output sale region/location.
- Candidate batch size.
- Available working capital and logistics method.
- Expected active operator time for setup and periodic maintenance, recorded as an estimate until measured.

If character or facility information is unavailable, use clearly labeled assumptions and do not describe the result as an executable plan.

## Procedure

### 1. Establish feasibility

- Confirm the blueprint or formula exists and can be used.
- Confirm required skills and job slots.
- Confirm the facility supports the activity and its service is online.
- Confirm the blueprint, formula, and required inputs can be staged at the destination.
- Identify any invention, reaction, copying, or component dependencies.

Reject or defer candidates that fail a hard constraint.

### 2. Build the production plan

- Select a realistic run count.
- Respect BPC licensed runs and job limits.
- Calculate output units, not just blueprint runs.
- Use the exact material quote or a validated calculation.
- Separate jobs where blueprint/BPC or material constraints require it.
- Record the number of slot-hours consumed in each job pool.

### 3. Price the inputs

- Use replacement or opportunity cost, not zero cost for owned materials.
- Use volume-weighted procurement prices for the planned quantity.
- Include upstream reaction, copying, invention, and component costs.
- Include logistics to the production facility.
- Record the source, location, timestamp, and price basis.

### 4. Price the job

- Obtain the live Industry quote.
- Record the activity-specific SCI, structure role, rigs, tax, SCC, and Alpha components.
- Record the job duration and installation fee.
- Do not assume one generic fee formula covers every activity.

### 5. Estimate revenue

Calculate at least two sale paths:
- Immediate liquidation into current buy-order depth.
- Sell order with broker fee, sales tax, expected relist fees, and a plausible fill horizon.

Use quantity-aware VWAP. Keep any unfilled remainder as inventory rather than assigning it the top-of-book price.

### 6. Evaluate liquidity and capital

- Compare planned daily output with conservative daily volume.
- Estimate liquidation days.
- Calculate peak working capital and capital-days.
- Calculate contribution per Manufacturing slot-hour.
- Estimate attributable hands-on operator time for evaluation, sourcing, staging, installation, hauling, order maintenance, and reconciliation.
- Calculate net contribution per active operator-hour when the time estimate is positive. Exclude unattended job duration and passive inventory waiting; do not multiply one person's simultaneous alt-character tasks into multiple operator-hours.
- Keep the raw contribution and explicit risk drivers visible. Until a defensible risk adjustment is calibrated from pilot results, do not invent a risk premium or present an unsupported risk-adjusted number.
- Identify the current bottleneck and expected bottleneck after expansion.

### 7. Stress-test

Run low/base/high scenarios for output price, input price, market volume, fees, logistics, and time to sell. For invention-driven products, include expected failure cost and variance.

### 8. Compare alternatives

Compare:
- Manufacture and sell.
- Buy the finished product.
- Sell the input materials.
- Produce an intermediate internally versus buy it.
- Use the same capital and slots for another product.

### 9. Decide

Use one of:
- **Go:** positive contribution under realistic base and acceptable low-case assumptions, with capacity and capital available.
- **Conditional:** positive expected contribution but one or more unresolved constraints or verification items remain.
- **No-go:** negative contribution, insufficient liquidity, infeasible inputs/facility, or unacceptable risk.

These are project workflow labels, not game mechanics.

## Required evaluation record

Record product/type ID, blueprint/formula ID, candidate runs, output, material bill, job quote, facility assumptions, source/destination market snapshots, fees, logistics, net contribution, margin, attributable active operator-hours, contribution per active operator-hour, slot-hours, capital-days, liquidation horizon, scenario results, confidence/provenance, and unresolved questions. Mark operator time as measured or estimated; leave the active-hour KPI unknown if time cannot be responsibly estimated.

## Stop conditions

Do not commit capital when:
- The job quote differs materially from the calculation and the difference is unexplained.
- The source market lacks sufficient input depth.
- The destination market cannot absorb the planned output.
- Facility access or service state is uncertain.
- A key recipe or success probability is unresolved.
- The low case is unacceptable for the amount of capital exposed.

## Follow-up

After delivery and sale, replace estimates with actual material use, job duration, fee, hauling cost, sale proceeds, and holding time. Feed the differences back into the model.
