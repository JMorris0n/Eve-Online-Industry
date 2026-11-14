---
type: Computation
title: Manufacturing Profitability Computation
description: Deterministic batch-level manufacturing profitability, net proceeds, unit margins, break-even prices, slot-hour efficiency, and capital return.
tags:
  - computation
  - manufacturing
  - profitability
sources:
  - id: ccp-broker-fees
    resource: https://support.eveonline.com/hc/en-us/articles/203218962-Broker-Fee-and-Sales-Tax
    title: Broker Fee and Sales Tax | EVE Online Support (updated 2026-03-02)
  - id: ccp-buy-sell-orders
    resource: https://support.eveonline.com/hc/en-us/articles/203218932-Buy-and-Sell-Orders
    title: Buy and Sell Orders | EVE Online Support (updated 2020-03-10)
  - id: ccp-viridian-fees
    resource: https://www.eveonline.com/news/view/viridian-expansion-notes
    title: Viridian Expansion Notes | EVE Online (2023-06-09)
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:50:00Z
status: draft
---

## Purpose

This computation converts a defined production batch, timestamped price inputs, live job quotes, and a declared sale strategy into reproducible profitability metrics. It is a deterministic calculation once its inputs are fixed. It does not predict future market prices or guarantee that output will sell at the assumed price.

## Required input groups

### Production plan

| Input | Description |
|---|---|
| product type ID | Stable SDE item identifier |
| blueprint type ID | Blueprint or BPC identifier |
| jobs | One record per planned manufacturing job |
| runs per job | Selected licensed manufacturing runs |
| output per run | Units produced per run |
| delivered output | Actual output units after job delivery |

### Material valuation

Each material line should contain:
- Material type ID.
- Quantity required by the exact job quote or validated recipe model.
- Unit price.
- Price basis: replacement sell price, opportunity value, actual acquisition cost, or internal transfer price.
- Market region/location and market side.
- Price retrieval timestamp and data provider.

### Installation and upstream costs

For every job or upstream activity, record:
- Installation fee from the Industry quote.
- Activity type and solar system.
- Facility/structure identifier.
- SCI and facility tax.
- Applicable role/rig modifiers.
- SCC and Alpha-clone fee components.
- Allocated invention, copying, reaction, or component costs.
- Logistics and handling costs.

### Sale strategy

Declare one of:
- Immediate sale to buy orders.
- Sell order.
- Internal consumption.
- Contract or other off-market disposition.

For market sales, record actual or estimated fill quantities, execution prices, sales tax, broker fee, and relist fee. Do not use one sell price for all output if the expected order-book depth requires multiple price levels.

## Core equations

Let:
- (Q) = total delivered output units.
- (q_i) = required quantity of input material (i).
- (p_i) = selected economic unit value of input (i).
- (F_j) = installation fee for job (j).
- (U) = allocated upstream costs not already represented in the material inputs.
- (L) = logistics and handling costs.
- (G) = gross realized sale value.
- (T) = sales tax.
- (B) = broker fees.
- (R) = relist fees.
- (O) = other sale-side costs.

```text
Material cost = Σ(q_i × p_i)

Economic batch cost
  = Material cost
    + Σ(F_j)
    + U
    + L

Gross sale value
  = Σ(quantity sold at price level k × execution price k)

Net sale proceeds
  = G - T - B - R - O

Net contribution
  = Net sale proceeds - Economic batch cost

Unit contribution
  = Net contribution / delivered output units
```

If not all delivered units have sold, calculate realized contribution on sold units and retain unsold inventory as inventory. Do not treat unsold output as cash revenue.

## Fee calculation inputs

Use the actual transaction fee inputs for the selected market route. CCP's current support page lists sales tax at 7.5% before Accounting and a minimum of 3.37% at Accounting V. NPC station broker fees start at 3% and are reduced by Broker Relations and unmodified standings. Upwell structure orders use a different broker-fee rule and do not receive the Broker Relations skill reduction. [^ccp-broker-fees]

For an order that is modified, CCP defines the relist fee using the effective broker-fee rate and relist discount:

```text
Relist fee
  = max(0, BR × (P2 - P1))
    + (1 - RD) × BR × P2
```

Here, P1 and P2 are the existing and new order values. Use the exact order quote for the actual fee. [^ccp-buy-sell-orders]

## Profitability metrics

```text
Net margin (%) = Net contribution / Gross sale value × 100

ROI on capital (%) = Net contribution / Capital deployed × 100

ISK per manufacturing slot-hour
  = Net contribution / Total manufacturing slot-hours

ISK per wall-clock hour
  = Net contribution / Elapsed critical-path hours
```

Total manufacturing slot-hours are the sum of job durations across all jobs. Elapsed critical-path hours are the wall-clock time from the start of the plan until the final required job is complete. These are not interchangeable when jobs run in parallel.

## Break-even price

For a simplified case with a single proportional sale fee rate (f), no fixed sale fees, and all output sold:

```text
Break-even price per unit
  = Economic batch cost / (Q × (1 - f))
```

If the sale strategy incurs separate proportional sales tax and broker fee rates:

```text
f = sales tax rate + broker fee rate + other proportional fee rates
```

This simplification is valid only when all included rates apply to the same gross sale-value base. Relist fees, minimum fees, mixed order fills, or fees on different bases must be calculated separately and included as fixed/explicit costs.

## Maximum affordable input price

For one target input material (x), with all other costs and expected proceeds known:

```text
Maximum unit value for input x
  = (Net sale proceeds - other batch costs)
    / required quantity of input x
```

This is a decision threshold. If the current replacement or opportunity price exceeds this amount, buying or consuming that input makes the batch uneconomic under the selected sale scenario.

## Data validation rules

- All quantities must use the same unit basis as the blueprint or SDE.
- Apply material rounding separately to each installed job, not once to the aggregate product demand.
- Use actual output units, not just blueprint runs.
- Include each installation fee once.
- Do not count internal transfer prices and the same upstream external costs twice.
- Do not value owned materials at zero by default.
- Use a price timestamp and location for every market input.
- Use order-book depth or a volume-weighted execution estimate for batches that exceed top-of-book volume.
- Keep market fees separate from industry installation fees.
- Preserve the sale strategy used to produce the result.

## Outputs

The computation should return:
- Delivered output units.
- Material cost by item and total.
- Installation fees by job and total.
- Upstream and logistics costs.
- Gross sale value and net sale proceeds.
- Broker, sales, and relist fees separately.
- Net contribution and unit contribution.
- Net margin and ROI on capital.
- Manufacturing slot-hours and ISK per slot-hour.
- Elapsed critical-path time and ISK per wall-clock hour.
- Break-even sale price.
- Maximum affordable input prices for selected bottleneck materials.
- Price timestamps, locations, assumptions, and source provenance.

## Limitations

This version defines the deterministic calculation structure. It does not include a live market data client, a current ESI adjusted-price ingestion process, product-specific blueprint recipes, invention expected-cost allocation, or multi-stage optimization. Those will be added as separate inputs and computation modules.

[^ccp-broker-fees]: CCP Support, Broker Fee and Sales Tax (updated 2026-03-02).
[^ccp-buy-sell-orders]: CCP Support, Buy and Sell Orders (updated 2020-03-10).
[^ccp-viridian-fees]: CCP, Viridian Expansion Notes (2023-06-09).
