---
type: Concept
title: Industrial Scaling
description: Scaling production across characters, facilities, regions, and capital while managing bottlenecks, market absorption, and operational risk.
tags:
  - optimization
  - scaling
  - operations
sources:
  - id: ccp-activities-jobs
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: ccp-manufacturing
    resource: https://support.eveonline.com/hc/en-us/articles/203210292-Manufacturing
    title: Manufacturing | EVE Online Support (updated 2024-08-29)
  - id: ccp-esi-overview
    resource: https://developers.eveonline.com/docs/services/esi/overview/
    title: EVE Swagger Interface (ESI) Overview
  - id: ccp-asset-safety
    resource: https://support.eveonline.com/hc/en-us/articles/208289365-Asset-Safety
    title: Asset Safety | EVE Online Support (updated 2026-03-02)
generated:
  by: openai/gpt-6
  at: 2026-11-14T08:20:00Z
status: draft
---

## Purpose

Industrial scaling increases sustainable output by adding or better utilizing characters, job slots, facilities, material supply, capital, and market access. It is not simply a matter of installing more jobs. Each expansion can move the bottleneck to another part of the production chain and can increase logistics, inventory, and operational risk.

Scale only when the current production cell is repeatable, profitable under realistic sale assumptions, and supported by sufficient capital and demand.

## Scaling dimensions

| Dimension | What increases | New constraints introduced |
|---|---|---|
| Skill specialization | Slots and activity efficiency per character | Training time and opportunity cost |
| Additional characters | Independent Manufacturing, Science, and Reaction pools | Character/account cost, training, assets, and coordination |
| Additional facilities | Activity-specific service, role bonuses, rigs, and locations | Asset movement, access, fuel, taxes, and service continuity |
| Additional regions | Sourcing and sales reach | Regional market depth, price differences, and hauling |
| Vertical integration | Control of more input stages | More inventory, skills, job pools, and capital |
| Corporate operation | Shared assets and coordinated production | Permissions, accounting, governance, and concentration risk |

## Character scaling

Each character has independent Manufacturing, Science, and Reaction job pools. Adding another industrial character adds another set of potential job slots, subject to that character's skill levels and the account's training/access constraints. Job slots are not shared between characters. [^ccp-activities-jobs]

A multi-character operation should assign roles based on the bottleneck:
- Manufacturing characters operate final products and components.
- Science characters copy BPOs, research efficiency, and run invention.
- Reaction characters produce composite, hybrid, and biochemical materials.
- Market characters manage order execution and fee-sensitive trade operations.
- PI characters manage colonies and planetary commodity logistics.

A character can specialize in more than one pool, but each role competes for training time and operational attention. See [Character Specialization](character-specialization.md).

## Facility scaling

Additional facilities can increase geographic coverage and provide different:
- Activity-specific System Cost Indices.
- Structure role bonuses.
- Rig effects and security-space multipliers.
- Owner-set facility taxes.
- Market access and input/output proximity.

However, character job slots remain a constraint. Multiple facilities do not create more job slots for one character. Additional characters may be required to exploit multiple locations concurrently. [^ccp-manufacturing]

A facility expansion should have a specific purpose, such as:
- A low-cost Manufacturing location.
- A Refinery with the correct reactor family.
- A research/copying location with appropriate rigs.
- A location near raw materials or a market.
- A backup location for critical production.

Do not add a facility solely because its advertised role bonus is higher. Compare the total landed cost, service continuity, access, taxes, and inventory movement.

## Vertical integration

Vertical integration adds more stages under one operation. A T2 or T3 producer may expand from final manufacturing into copying, invention, reactions, and component production. A PI producer may add extraction, processing, and export rather than purchasing intermediate commodities.

Potential benefits:
- More control over input availability.
- Reduced reliance on thin or unreliable intermediate markets.
- Better coordination of BPC, component, and final-product output.
- Potential capture of margin from intermediate stages.

Potential costs:
- More job slots across multiple pools.
- More skill requirements.
- Higher working capital and WIP inventory.
- Additional facilities and logistics.
- More complex scheduling and quality control.
- Greater exposure to market and structure risk.

Vertical integration should be evaluated stage by stage. If buying an intermediate is cheaper than producing it internally at its opportunity cost, external sourcing may be preferable even in a vertically integrated operation.

## Sustainable output constraint

For a production chain normalized to final-product units per day:

```text
Sustainable output rate
  = minimum of:
    Manufacturing capacity
    Science/BPC supply capacity
    Reaction/intermediate supply capacity
    Raw material procurement capacity
    Facility/service capacity
    Capital-supported capacity
    Logistics capacity
    Market absorption capacity
```

Adding capacity to a stage that is not the bottleneck may create more inventory without increasing final output. The correct expansion target is the current binding constraint or the constraint expected to become binding after expansion.

## Economies and diseconomies of scale

### Potential economies

- Larger procurement volumes may reduce sourcing friction or improve buy-order execution.
- Larger jobs can reduce the number of installations and may reduce material-rounding loss.
- Repeated production can improve slot utilization and reduce idle time.
- Shared logistics and staged inventory can reduce per-unit transport costs.
- Specialized characters can increase throughput in a constrained job pool.

### Potential diseconomies

- Larger output can exceed local market demand and depress realized prices.
- More inventory increases working capital and price exposure.
- More jobs can increase installation fees and operational complexity.
- Multiple locations require hauling, access management, and stock reconciliation.
- Concentrating assets in a single Upwell structure can increase catastrophic loss exposure.
- A high-volume operation can become dependent on one scarce input, facility service, or BPC source.

Scale should be measured by incremental net contribution, not gross production volume.

## Incremental expansion test

For a proposed expansion from operation A to operation B:

```text
Incremental contribution
  = expected contribution(B) - expected contribution(A)

Incremental peak capital
  = peak working capital(B) - peak working capital(A)

Incremental capital efficiency
  = incremental contribution / incremental capital-days
```

Also calculate:
- Added Manufacturing, Science, and Reaction slot-hours.
- Additional facility and service costs.
- Added hauling and asset exposure.
- Additional inventory required.
- Expected market absorption and sale delay.
- Expected change in product price caused by greater supply.

An expansion is attractive only if its incremental return justifies the additional capital, time, risk, and management effort compared with alternative uses of those resources.

## Scaling phases

### Phase 1: Prove one production cell

Establish one repeatable product or production chain. Verify job costs, material quantities, job durations, market fees, and realized sale proceeds.

### Phase 2: Remove the measured bottleneck

Add the skill, BPC supply, material procurement, facility, or capital that limits output. Avoid expanding every stage simultaneously.

### Phase 3: Replicate the cell

Use additional characters or facilities to replicate a proven schedule. Keep product recipes, price inputs, and job assumptions versioned.

### Phase 4: Integrate upstream stages

Add reactions, components, invention, or PI only when their internal cost and reliability compare favorably with external sourcing.

### Phase 5: Regionalize or corporatize

Expand to additional regions or shared corporate operations only when the gains in supply, market reach, or specialization exceed the added logistics and governance costs.

## Operational controls at scale

A larger operation should maintain:
- A stable product/type ID and blueprint registry.
- Character skill and job-slot capacity records.
- Facility and service-module registry.
- Material stock by location and intended use.
- BPO/BPC licensed-run inventory.
- Active job and dependency schedule.
- Market order and price snapshots.
- Cash-flow, capital-days, and batch profitability history.
- Courier contracts, collateral, and in-transit asset records.
- Structure state and asset-safety exposure.

The knowledge base should keep the mechanics and calculation assumptions separate from current operational data. Live prices, character skills, job quotes, and inventory should be refreshed rather than hardcoded into evergreen concept documents. ESI is the preferred public data interface for supported character, market, and industry data. [^ccp-esi-overview]

## Risk and concentration

Scaling increases the amount of value exposed to a single event. Diversify critical assets and inventory when the reduction in concentration risk justifies the additional logistics cost.

Standard Upwell Asset Safety has important exceptions for FLEX structures, Abandoned-state destruction, wormhole space, and Pochven. A scaled operation must not assume that every stored asset will be automatically recoverable. [^ccp-asset-safety]

Consider separate locations for:
- Irreplaceable or high-value BPOs.
- Bulk raw materials.
- WIP and active-job inputs.
- Finished goods awaiting sale.
- Backup stock and emergency production inputs.

The exact layout depends on route security, structure access, asset value, and operational complexity.

## Scaling decision checklist

Before adding a character, facility, region, or production stage:

1. Identify the current bottleneck using actual throughput data.
2. Quantify the expected incremental output.
3. Confirm downstream market demand or internal consumption.
4. Calculate incremental contribution and peak working capital.
5. Calculate incremental slot-hours and capital-days.
6. Include additional facility, market, and logistics costs.
7. Evaluate asset concentration and route risk.
8. Confirm the expansion can be managed and monitored.
9. Define a rollback or exit path if the market or facility conditions change.
10. Re-measure the bottleneck after expansion.

## Open verification and planning work

- Build a multi-character capacity model using current character skill data.
- Compare a single broad character with specialized Manufacturing/Science/Reaction characters.
- Add facility and regional capacity to the production scheduler.
- Model market absorption limits and price impact from larger output volumes.
- Add a corporate asset/permissions model for shared BPOs and inventory.
- Build an expansion scenario using actual operating data rather than theoretical maximum slots.

## Related concepts

- [Character Specialization](character-specialization.md)
- [Manufacturing Throughput](manufacturing-throughput.md)
- [Science and Invention Throughput](science-and-invention-throughput.md)
- [Reaction Throughput](reaction-throughput.md)
- [Production Scheduling](production-scheduling.md)
- [Capital and Asset Management](../04-industrial-economics/capital-and-asset-management.md)
- [Logistics and Risk](../04-industrial-economics/logistics-and-risk.md)
- [Market Location Economics](../04-industrial-economics/market-location-economics.md)

[^ccp-activities-jobs]: CCP Support, Activities and Job Types (updated 2024-08-29).
[^ccp-manufacturing]: CCP Support, Manufacturing (updated 2024-08-29).
[^ccp-esi-overview]: CCP, EVE Developer Documentation, ESI Overview.
[^ccp-asset-safety]: CCP Support, Asset Safety (updated 2026-03-02).
