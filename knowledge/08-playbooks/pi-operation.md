---
type: Process
title: Planetary Industry Playbook
description: Repeatable colony setup, extraction, routing, processing, collection, and replenishment workflow.
tags:
  - playbook
  - pi
  - extraction
generated:
  by: openai/gpt-6
  at: 2026-11-14T09:50:00Z
status: draft
---

## Objective

Operate PI colonies as a reliable resource and commodity supply chain. The goal may be raw-resource extraction, P1 production, factory-planet processing, or a mixed operation.

Use [Planetary Industry](../02-production-systems/planetary-industry.md) and [Planetary Commodities](../03-materials-and-sourcing/planetary-commodities.md) as the mechanics references.

## Before deployment

- Confirm the target product tier and its current schematic chain.
- Identify suitable planet types and resource availability.
- Confirm Interplanetary Consolidation and Command Center Upgrades levels.
- Confirm the character can import/export under the current clone state.
- Estimate Customs Office/Skyhook access and tax.
- Check the market value of inputs and outputs, including the opportunity cost of extracted P0.
- Decide whether the colony is an extractor, factory, or hybrid.

## Colony construction

1. Carry the matching Command Center to the target system and deploy it on the selected planet.
2. Upgrade the Command Center to the intended level.
3. Place the ECU and position extractor heads over the selected deposit.
4. Place processors, storage, and a Launchpad.
5. Build links and routes between every source and destination.
6. Check CPU and powergrid usage.
7. Check link capacity and buffer capacity.
8. Submit the colony changes and confirm the layout is active.

Do not assume a link automatically creates a route. Verify both.

## Extraction program

1. Select the P0 resource.
2. Scan the deposit and compare alternative head positions.
3. Choose a program duration that matches the intended maintenance schedule.
4. Inspect head overlap and expected cycle output.
5. Route ECU output to storage or a processor with adequate capacity.
6. Install the program and record start/end times.
7. Review actual cycle output and adjust head positions as deposits deplete.

Use actual output history to calibrate the plan. A resource scan is not a guarantee of constant extraction yield.

## Factory processing

- Confirm the selected processor supports the intended schematic.
- Confirm exact input quantities and output batch size from the current schematic.
- Ensure input buffers can hold enough material for continuous operation.
- Ensure processor outputs have a route to storage or Launchpad.
- Match processor counts to upstream supply and downstream demand.
- Avoid overfilling processor input storage.

## Collection and transfer

1. Check Launchpad storage and export quantity.
2. Verify Customs Office or Skyhook access and current displayed tax.
3. Calculate import/export cost separately.
4. Export to space and move goods to the intended market or next planet.
5. Record transfer tax, hauling cost, and inventory movement.
6. Replenish imported inputs for factory planets.

The Command Center rocket is a small export-only fallback, not a substitute for routine Launchpad transfer. Alpha clones cannot import or export PI materials.

## Daily/periodic maintenance

- Check extractor program remaining time.
- Check storage fill levels.
- Check processor input/output and route status.
- Check colony CPU/powergrid if changing the layout.
- Check market prices and export taxes before moving large quantities.
- Record actual P0 output, processed quantities, and idle time.
- Reposition extractor heads when output falls below the planned threshold.

## Post-cycle review

Compare actual extraction, processor cycles, transfer fees, hauling, and sale proceeds with the forecast. Update the colony's sustainable output and cost basis. Do not treat self-extracted P0 as free in profitability analysis.
