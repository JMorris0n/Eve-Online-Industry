---
type: Concept
title: Manufacturing Profitability
description: Economic evaluation of manufacturing batches, including output valuation, input opportunity cost, installation and market fees, break-even pricing, margins, throughput, and capital use.
tags:
  - economics
  - manufacturing
  - profitability
  - margin
sources:
  - id: eveuni-manufacturing
    resource: https://wiki.eveuniversity.org/Manufacturing
    title: Manufacturing | EVE University Wiki
  - id: ccp-viridian-fees
    resource: https://www.eveonline.com/news/view/viridian-expansion-notes
    title: Viridian Expansion Notes | EVE Online (2023-06-09)
  - id: ccp-broker-fees
    resource: https://support.eveonline.com/hc/en-us/articles/203218962-Broker-Fee-and-Sales-Tax
    title: Broker Fee and Sales Tax | EVE Online Support (updated 2026-03-02)
  - id: ccp-buy-sell-orders
    resource: https://support.eveonline.com/hc/en-us/articles/203218932-Buy-and-Sell-Orders
    title: Buy and Sell Orders | EVE Online Support (updated 2020-03-10)
  - id: ccp-esi-overview
    resource: https://developers.eveonline.com/docs/services/esi/overview/
    title: EVE Swagger Interface (ESI) Overview
  - id: eveuni-research
    resource: https://wiki.eveuniversity.org/Research
    title: Research | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:50:00Z
status: draft
---

## Purpose

Manufacturing profitability answers a specific question:

**If this production plan is completed and its output is sold under a stated execution strategy, how much economic value does it create, how much capital does it tie up, and what constraints limit repeating it?**

A useful model must distinguish economic profit from cash flow, and must account for input opportunity cost, job installation fees, market fees, logistics, output quantities, and the time/capital required. The valuation conventions are established in [Industrial Cost Accounting](cost-accounting.md). [^ccp-viridian-fees]

## Unit of analysis

The preferred unit is a **production batch**: one or more manufacturing jobs grouped into a defined output plan. A batch can contain several jobs because of BPC run limits, available blueprint copies, character job slots, job duration limits, or material availability.

Do not assume one blueprint run equals one finished unit. For each job:

```text
Job output units = job runs × blueprint output quantity per run

Batch output units = sum of output units from all jobs
```

Use the actual delivered output quantity. If only part of the batch is sold, calculate realized contribution on sold units using an allocated cost basis, and retain the remaining units as inventory rather than treating them as cash revenue. For planning, calculate expected batch contribution assuming the intended quantity is eventually sold.

## Economic batch cost

For a production batch:

```text
Economic batch cost
  = input opportunity/replacement cost
  + installation fees
  + allocated upstream production/invention/copying costs
  + logistics and handling costs
  + other variable costs
```

### Input opportunity or replacement cost

Value materials at the price required to replace them at the production location or at the best realistic alternative use. Self-mined, self-reprocessed, self-produced, or previously purchased materials are not free. The selected valuation convention must be explicit and consistent. [^ccp-viridian-fees]

### Installation fees

Use the live Industry quote for each installed job. The fee is separate from material value and must be counted once. The general fee equation and Manufacturing EIV convention are documented in [Industry Installation Cost Computation](../09-computations/installation-costs.md).

### Upstream chain costs

For a multi-stage chain, either:
- evaluate the complete chain using external inputs and final output, or
- value intermediate products at a consistent transfer price/opportunity cost.

Do not count both an intermediate product's full internal production cost and the same raw inputs again in the final product's cost. Internal transfers must be eliminated when consolidating a vertically integrated chain.

For invention-driven production, allocate expected failed-attempt costs across successful BPC output using the actual success probability and output licensed runs. See [Invention Economics Computation](../09-computations/invention-economics.md). For reaction/component chains, value intermediate outputs consistently rather than treating them as free.

### Logistics and handling

Include hauling, courier contracts, collateral risk, container/packaging constraints, asset-transfer costs, and any market-location transfer costs. A market price at a distant hub is not the same as realizable proceeds at the production location.

## Revenue and market execution

Gross revenue is not automatically the displayed regional sell price multiplied by output units. Choose an execution strategy:

- **Immediate sale:** model the available buy-order depth and the volume-weighted price actually available for the quantity.
- **Sell order:** model a plausible sell price and fill horizon, then include broker fees and expected relist fees.
- **Internal consumption:** value output at its replacement cost or at the opportunity cost of not selling it.

For a completed sale:

```text
Gross sale value = sum(quantity sold × realized execution price)

Net sale proceeds
  = gross sale value
    - sales tax
    - broker fees
    - relist fees
    - other sale/contract costs
```

CCP charges sales tax to the seller when an item sells. Broker fees apply when non-immediate market orders are created, and relist fees apply when an order's price is changed. See [Market Fees and Taxation](market-fees-and-taxation.md). [^ccp-broker-fees] [^ccp-buy-sell-orders]

## Profit and margin metrics

| Metric | Formula | Interpretation |
|---|---|---|
| Net contribution | Net sale proceeds − economic batch cost | Economic value created by the batch |
| Unit contribution | Net contribution ÷ actual output units | Contribution per produced unit |
| Net margin | Net contribution ÷ gross sale value | Profit as a share of gross sales |
| ROI on capital | Net contribution ÷ capital deployed | Return on the working capital committed |
| ISK per manufacturing slot-hour | Net contribution ÷ total manufacturing slot-hours consumed | Efficiency of scarce character job capacity |
| ISK per active operator-hour | Net contribution ÷ hands-on operator hours attributable to the plan | Efficiency of the user's limited attention and operational labor |
| ISK per wall-clock hour | Net contribution ÷ elapsed critical-path time | Rate of value creation over real elapsed time |

These metrics answer different questions. A high-margin product can have poor slot-hour efficiency if it ties up jobs for a long time. A low-margin product can still be attractive if it has high throughput, low capital requirements, and reliable liquidity.

For concurrent jobs, total slot-hours and elapsed critical-path time are not the same. If three jobs each run for ten hours in parallel, the plan consumes 30 manufacturing slot-hours but may have a ten-hour elapsed production time.
Active operator-hours are different again: count attributable hands-on work such as evaluation, sourcing, staging, installing jobs, hauling, maintaining orders, and reconciling sales. Do not count unattended job time or passive inventory waiting, and do not count one operator's simultaneous alt-character activity multiple times. The product scanner should rank raw net contribution per active operator-hour when that input is known, while retaining slot-hour, capital, liquidity, and elapsed-time measures as separate constraints. If active time is unknown, leave the KPI unknown rather than substituting elapsed time.

## Break-even price

If all sale-side costs are proportional percentages of gross sale value and there are no fixed transaction charges:

```text
Break-even sale price per unit
  = economic batch cost
    / (output units × (1 - sales tax rate - broker fee rate - other proportional sale rates))
```

For an immediate sale into buy orders, the broker fee for creating a non-immediate sell order is omitted. For a sell-order strategy, include the applicable broker fee and expected relist costs. If fees are tiered, fixed, or charged on a different base, solve using the actual fee equations instead of this simplified expression. [^ccp-broker-fees] [^ccp-buy-sell-orders]

A target-margin price can be solved by replacing the break-even cost numerator with the cost divided by (1 - m), where (m) is the desired net margin on gross sale value, then accounting for proportional fees. Implement the full algebra in the deterministic computation file.

## Working capital and time

Capital deployed should include the replacement value of inputs and any cash paid before output is sold. A batch can be profitable on paper but unattractive if it ties up capital for a long period or requires a large amount of inventory before the first sale.

Track at least:

- Peak input inventory value.
- Installation fees paid at job start.
- Market-order broker fees paid before sales complete.
- Expected production time and delivery time.
- Expected inventory holding time.
- Expected time to sell the completed output.
- Capital recovered after each sale.

Do not treat the blueprint's full purchase price as a variable batch cost each time it is used. Treat blueprint acquisition and research as an investment, then evaluate its amortization or return separately from short-run marginal contribution.

## Sensitivity and uncertainty

At minimum, evaluate low/base/high scenarios for:

- Output sale price and market depth.
- Material replacement prices.
- Facility tax and SCI.
- Market broker fee and sales tax.
- Logistics cost.
- Production and sale delay.

For each scenario, record which input drives the result. A single displayed profit number without timestamped prices and assumptions is not reproducible.

Market liquidity matters. If the batch is larger than available buy-order depth, the remaining units may sell at lower prices or require a sell order and waiting time. Use volume-weighted execution estimates rather than a single top-of-book quote. [^ccp-buy-sell-orders]

## Decision framework

A production plan is generally worth advancing only if:

1. Net contribution is positive under a realistic sale execution scenario.
2. The expected margin remains positive under reasonable adverse price and fee changes.
3. The plan does not consume more manufacturing slots, capital, or logistics capacity than its alternatives justify.
4. The expected return compares favorably with buying the finished item or selling the inputs.
5. The production and sale horizon is acceptable for the capital committed.

The comparison should include the alternative of selling the inputs directly. Manufacturing is not economically justified merely because it converts materials into a more expensive finished item.

## Boundaries and dependencies

This concept establishes the model structure. Product-specific data, complete price acquisition, live fee calculation, invention success, and logistics costs are supplied by separate concepts and computation inputs.

- [Industrial Cost Accounting](cost-accounting.md)
- [Market Fees and Taxation](market-fees-and-taxation.md)
- [Tech I Manufacturing](../02-production-systems/tech-1-manufacturing.md)
- [Blueprint Copying](../02-production-systems/blueprint-copying.md)
- [Tech II Invention](../02-production-systems/tech-2-invention.md)
- [Installation Cost Computation](../09-computations/installation-costs.md)
- [Manufacturing Profitability Computation](../09-computations/manufacturing-profitability.md)

## Open verification tasks

- Compare calculated material requirements and installation fees against actual Industry quotes for representative BPO/BPC jobs.
- Verify exact market fee treatment for mixed immediate fills and unfilled order remainder.
- Add current market depth and volume-weighted execution-price inputs.
- Validate whether the planned batch can sell in the target time window.
- Add production chain support for reactions, invention, Tech II components, Tech III, and PI.
- Build a representative worked product example using live data after the user supplies or selects a target market/location.

[^ccp-viridian-fees]: CCP, Viridian Expansion Notes (2023-06-09).
[^ccp-broker-fees]: CCP Support, Broker Fee and Sales Tax (updated 2026-03-02).
[^ccp-buy-sell-orders]: CCP Support, Buy and Sell Orders (updated 2020-03-10).
[^ccp-esi-overview]: CCP, EVE Developer Documentation, ESI Overview.
[^eveuni-manufacturing]: EVE University Wiki, Manufacturing.
[^eveuni-research]: EVE University Wiki, Research.
