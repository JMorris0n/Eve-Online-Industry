---
type: Concept
title: Capital and Asset Management
description: Working capital, inventory valuation, cash conversion, capital turnover, asset concentration, and capital allocation across industrial projects.
tags:
  - capital
  - economics
  - inventory
  - assets
sources:
  - id: ccp-asset-safety
    resource: https://support.eveonline.com/hc/en-us/articles/208289365-Asset-Safety
    title: Asset Safety | EVE Online Support (updated 2026-03-02)
  - id: ccp-courier-contracts
    resource: https://support.eveonline.com/hc/en-us/articles/203218982-Courier-Contracts
    title: Courier Contracts | EVE Online Support (updated 2021-08-23)
  - id: ccp-esi-overview
    resource: https://developers.eveonline.com/docs/services/esi/overview/
    title: EVE Swagger Interface (ESI) Overview
  - id: ccp-broker-fees
    resource: https://support.eveonline.com/hc/en-us/articles/203218962-Broker-Fee-and-Sales-Tax
    title: Broker Fee and Sales Tax | EVE Online Support (updated 2026-03-02)
generated:
  by: openai/gpt-6
  at: 2026-11-14T07:20:00Z
status: draft
---

## Purpose

Capital and asset management determines how much value is committed to production, how long it remains unavailable, where it is exposed, and how reliably it can be converted back into liquid ISK. A profitable production plan can still be a poor capital allocation if it consumes most available funds, turns over slowly, or concentrates assets in a vulnerable structure.

This concept separates capital employed, working capital, inventory value, cash flow, and economic profit. It supports project selection and scaling; it does not prescribe a personal ISK budget.

## Capital categories

| Category | Examples | Capital concern |
|---|---|---|
| Liquid ISK | Wallet balances | Immediately available for fees, purchases, and emergencies |
| Procurement inventory | Minerals, gas, salvage, PI commodities, components | Value changes with the market and may be difficult to liquidate |
| Work in progress (WIP) | Materials committed to active manufacturing, reaction, or science jobs | Capital is committed until job completion and delivery |
| Finished inventory | Completed ships, modules, components, commodities | Requires a buyer or internal use to recover capital |
| Blueprint assets | BPOs and researched originals | Long-lived capital assets; not a per-batch material cost |
| Blueprint copies | Limited-run BPCs | Consumable production capacity with finite licensed runs |
| Market orders | Listed inventory and buy-order commitments | May remain tied up while waiting for execution |
| Courier collateral | ISK committed by a hauling contractor | Temporarily unavailable until delivery or contract resolution |

The valuation basis for each category must be explicit. See [Industrial Cost Accounting](cost-accounting.md) for replacement cost, opportunity cost, historical cost, and book value.

## Working capital

Working capital is the capital required to fund the production cycle before sales recover the outlay. It includes materials, installation fees, upstream costs, logistics, market-order costs, and any other cash committed before the output is sold.

For a dated cash-flow sequence:

```text
Cumulative cash flow at time t
  = sum of all cash inflows and outflows up to t

Peak working capital
  = maximum absolute value of the negative cumulative cash flow
```

This peak-cash requirement is more useful than summing every input purchase if some costs are recovered before the entire chain is complete.

Keep three views separate:

- **Cash required:** actual ISK that must be available at each stage.
- **Economic capital employed:** replacement/opportunity value of all assets committed, including owned materials.
- **Book value:** value assigned to assets under the chosen accounting convention.

Owned minerals or components may require no new wallet expenditure, but they still consume economic capital because they could have been sold or used elsewhere.

## Inventory management

Inventory should be classified by production role and liquidity:

- Raw materials awaiting production.
- Intermediate commodities and components.
- BPCs and other limited-run production inputs.
- WIP committed to installed jobs.
- Finished output awaiting sale or internal consumption.
- Market-listed inventory.
- Assets in transit or held under courier contract.

A useful inventory record includes item/type ID, quantity, location, replacement value, book value, opportunity cost, acquisition date, intended use, and liquidity classification.

Avoid using a single aggregate ISK value for all inventory. A billion ISK of liquid minerals in a major hub is not equivalent to a billion ISK of niche components in a remote structure. Price, volume, market depth, and location all affect realizable value.

## Capital turnover and cash conversion

The production cycle ties up capital from procurement until the finished output is sold or consumed. The relevant elapsed period may include:

1. Waiting for materials or buy orders.
2. Transporting inputs to the facility.
3. Manufacturing, reactions, copying, research, or invention.
4. Transporting finished output.
5. Waiting for market orders to fill.
6. Recovering the sale proceeds.

A useful cash-conversion measure is the elapsed time from the first material cash outflow to recovery of the final sale proceeds. For a vertically integrated chain, track both the full chain and each stage so bottlenecks can be identified.

Inventory turnover can be measured as:

```text
Inventory turnover
  = cost of goods sold during period
    / average inventory value during period
```

```text
Days inventory outstanding
  = days in measurement period
    / inventory turnover
```

Use consistent valuation conventions and period boundaries. These accounting ratios describe historical performance; they do not guarantee future market demand.

## Capital efficiency metrics

| Metric | Formula | What it measures |
|---|---|---|
| Cycle ROI | Net contribution ÷ peak capital deployed | Return on the capital required for one cycle |
| Capital-days | Sum of capital employed × days held for each time interval | Time-weighted capital commitment |
| Contribution per capital-day | Net contribution ÷ capital-days | Return relative to both amount and holding time |
| Capital turnover | Cost of goods sold ÷ average inventory | How quickly inventory value is converted into sales |
| Cash conversion time | Final cash recovery time − first cash outflow time | How long funds remain committed |
| Slot efficiency | Net contribution ÷ manufacturing slot-hours | Return on a constrained character job slot |

Do not compare two projects using ROI alone. A small project can have a high percentage ROI but produce little ISK, while a larger project can produce more ISK but tie up capital for longer. Use absolute contribution, peak capital, capital-days, slot-hours, and liquidity together.

## Capital allocation

When comparing projects, consider:

1. Expected net contribution under realistic sale execution.
2. Peak working capital and reserve requirements.
3. Capital-days and expected cash conversion time.
4. Manufacturing, science, and reaction slot usage.
5. Liquidity and the ability to exit inventory.
6. Asset concentration and route/structure exposure.
7. Alternative use of the same materials, blueprints, character slots, and ISK.

A useful rule is to preserve a liquidity reserve for fees, unexpected input shortages, logistics, and price changes. Do not commit all available capital to inventory simply because a product has a positive modeled margin.

## Blueprint and research investment

A BPO purchase and its research are capital investments, not ordinary recurring material costs. For short-run batch decisions, exclude sunk acquisition cost when comparing marginal production against buying the finished item. For long-run investment decisions, measure the expected contribution attributable to the blueprint over its useful production life.

A simple amortization view is:

```text
Blueprint investment cost per planned output unit
  = (BPO acquisition cost + research investment)
    / expected lifetime output units
```

This is an accounting allocation, not a direct in-game fee. The expected lifetime output quantity must reflect market demand, blueprint utilization, competition, and the possibility that the blueprint's economic value changes.

BPCs differ: their finite licensed runs are consumed through production and should be treated as a limited production input. If acquired from the market or produced through copying/invention, include their opportunity or replacement cost in the production plan.

## Asset concentration and recovery

Location and structure state affect how much capital is exposed. Standard Upwell Asset Safety does not cover every asset in every location:

- Specialized Upwell FLEX structures are excluded from standard Asset Safety.
- Assets in wormhole space and Pochven are ejected into containers rather than moved to standard Asset Safety.
- Assets in a structure destroyed while Abandoned do not automatically enter Asset Safety.
- Boarded ships are not moved into Asset Safety. [^ccp-asset-safety]

Courier contracts also create distinct exposure. The issuer receives collateral if a contract fails, but any package value above collateral remains uncovered. The contractor's collateral is temporarily tied up until delivery or failure resolution. [^ccp-courier-contracts]

Do not concentrate irreplaceable BPOs, all production inputs, and all finished inventory in one structure solely for convenience. Diversification can reduce catastrophic exposure, but additional locations increase logistics and management costs. The optimal balance depends on the asset's value, location, access, and recovery options.

## Buy versus build and liquidity reserve

A make-or-buy decision should compare the full economic cost of producing an intermediate with its replacement price at the destination. If buying is cheaper, building may still be justified by supply reliability, market depth, or the value of consuming otherwise idle slots. Conversely, building a component internally does not make it free; its opportunity cost is the value of the inputs and production capacity used.

Before scaling a production line, reserve capital for:
- Input inventory and replenishment.
- Industry installation fees.
- Market broker fees and sales taxes.
- Courier collateral and hauling costs.
- Structure fuel/service disruptions.
- Unplanned market price changes.
- Inventory that takes longer than expected to sell.

## Boundaries and unresolved details

This document defines the accounting and planning framework. It does not set a universal target ROI, maximum inventory concentration, or minimum cash reserve. Those depend on the user's actual capital, risk tolerance, product mix, and operating environment.

Open work:
- Build a capital-turnover computation using dated cash flows and capital-days.
- Add asset and inventory location data to the future ESI/character-data workflow.
- Add scenario-based inventory liquidity and liquidation estimates.
- Validate a worked production cycle with actual cash-flow timestamps and sale records.
- Model blueprint investment ROI separately from recurring batch contribution.

## Related concepts

- [Industrial Cost Accounting](cost-accounting.md)
- [Manufacturing Profitability](manufacturing-profitability.md)
- [Market Fees and Taxation](market-fees-and-taxation.md)
- [Logistics and Risk](logistics-and-risk.md)
- [Market Location Economics](market-location-economics.md)
- [Research Investment ROI](../09-computations/research-investment-roi.md)
- [Capital Turnover Computation](../09-computations/capital-turnover.md)

[^ccp-asset-safety]: CCP Support, Asset Safety (updated 2026-03-02).
[^ccp-courier-contracts]: CCP Support, Courier Contracts (updated 2021-08-23).
[^ccp-esi-overview]: CCP, EVE Developer Documentation, ESI Overview.
[^ccp-broker-fees]: CCP Support, Broker Fee and Sales Tax (updated 2026-03-02).
