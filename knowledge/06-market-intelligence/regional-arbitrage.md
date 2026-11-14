---
type: Concept
title: Regional Arbitrage
description: Evaluating regional price spreads after order-book depth, market fees, hauling, collateral, risk, and capital time.
tags:
  - market
  - arbitrage
  - logistics
sources:
  - id: ccp-buy-sell-orders
    resource: https://support.eveonline.com/hc/en-us/articles/203218932-Buy-and-Sell-Orders
    title: Buy and Sell Orders | EVE Online Support (updated 2020-03-10)
  - id: ccp-broker-fees
    resource: https://support.eveonline.com/hc/en-us/articles/203218962-Broker-Fee-and-Sales-Tax
    title: Broker Fee and Sales Tax | EVE Online Support (updated 2026-03-02)
  - id: ccp-esi-api-explorer
    resource: https://esi.evetech.net/ui/?version=latest
    title: ESI API Explorer
  - id: ccp-esi-best-practices
    resource: https://developers.eveonline.com/docs/services/esi/best-practices/
    title: Best Practices for ESI
  - id: eveuni-hauling
    resource: https://wiki.eveuniversity.org/Hauling
    title: Hauling | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T09:00:00Z
status: draft
---

## Purpose

Regional arbitrage attempts to capture a price difference between two market locations by buying in one location and selling in another. The visible spread is only a starting signal. A valid arbitrage estimate must account for executable order-book depth, market fees, transport cost, route risk, collateral, time, and the possibility that prices change before the goods arrive.

EVE market orders are regional, while individual orders remain tied to a station or structure. A cross-region trade therefore requires moving the goods between regions; buy orders do not automatically collect items from another region. [^ccp-buy-sell-orders]

## Arbitrage components

For a source location A and destination location B:

```text
Gross price spread
  = destination sale value - source purchase cost

Net arbitrage contribution
  = destination net proceeds
    - source total acquisition cost
    - logistics cost
    - risk-adjusted loss allowance
    - other carrying/handling costs
```

The source and destination values must be calculated for the same quantity Q using the actual order books, not the top price alone.

## Source acquisition value

For the source location:
1. Identify eligible sell orders for immediate procurement or decide to place a buy order.
2. Calculate the volume-weighted procurement cost for Q units.
3. Include broker fees if creating a non-immediate buy order.
4. Include any local transfer or pickup cost.
5. Confirm the goods can be collected and moved.

An immediate purchase from existing sell orders does not incur the same order-creation broker fee as a non-immediate buy order. The seller pays sales tax on the completed sale. [^ccp-broker-fees]

## Destination liquidation value

For the destination:
1. Query eligible buy orders for immediate liquidation or choose a sell-order strategy.
2. Calculate the volume-weighted liquidation proceeds for Q units.
3. Include sales tax.
4. Include broker fees for non-immediate sell orders.
5. Include expected relist fees if the order is likely to be modified.
6. Account for the expected time required to sell the full quantity.

A top buy order that covers only a small fraction of Q cannot be used as the sale price for the entire shipment. If the order book is insufficient, model the remainder as inventory awaiting sale. [^ccp-buy-sell-orders] [^ccp-broker-fees]

## Transport and risk-adjusted cost

Transport cost should include:
- Courier reward or self-haul operating cost.
- Fuel and consumables.
- Ship depreciation or replacement cost.
- Pilot time opportunity cost.
- Courier collateral financing cost, where applicable.
- Expected cargo loss and uncovered contract exposure.
- Expected delay or production interruption.
- Asset transfer and handling costs.

For a simplified risk term:

```text
Expected loss
  = probability of loss × uncovered economic exposure
```

The loss probability must be route-, ship-, cargo-, and operating-condition-specific. Do not assign a universal loss probability based only on security status. See [Logistics and Risk](../04-industrial-economics/logistics-and-risk.md). [^eveuni-hauling]

## Full landed arbitrage model

Let:
- Q = quantity transported.
- C_A(Q) = total source acquisition cost for Q.
- R_B(Q) = destination gross liquidation value for Q.
- F_B(Q) = destination sales tax, broker, and relist fees.
- L(Q) = transport and handling cost.
- X(Q) = risk-adjusted expected loss and delay cost.
- K(Q) = capital opportunity cost over the holding period.

```text
Net arbitrage contribution
  = R_B(Q) - F_B(Q) - C_A(Q) - L(Q) - X(Q) - K(Q)
```

The capital cost K should not double-count the same financing cost already included elsewhere. If capital time is handled through capital-days, use one consistent method.

Useful secondary metrics:
- Net contribution per m³.
- Net contribution per trip.
- Net contribution per capital-day.
- Return on peak capital deployed.
- Estimated days from purchase to full liquidation.
- Percentage of shipment immediately executable at destination.

## Break-even source price

If destination proceeds and all non-source costs are known:

```text
Maximum source acquisition cost
  = destination net proceeds
    - logistics
    - risk allowance
    - carrying/handling costs
```

For a unit-level threshold:

```text
Maximum source price per unit
  = maximum source acquisition cost / Q
```

This threshold is the maximum economically acceptable purchase cost under the selected destination sale scenario. If the source sell price exceeds it, the trade is not profitable at that quantity and route.

## Quantity and capacity effects

The best arbitrage quantity is not necessarily the largest available quantity. Larger shipments can:
- Reduce transport cost per unit.
- Require a larger ship or multiple trips.
- Increase collateral and cargo exposure.
- Consume more working capital.
- Exceed destination buy-order depth.
- Take longer to liquidate and increase price risk.

Calculate net contribution at several candidate quantities. The marginal units may have lower destination proceeds if they consume progressively worse buy-order levels.

## Same-region station arbitrage

A price difference can exist between stations or structures in the same region. The market is regionally organized, but orders are location-specific. A buy order's range can allow sellers to deliver to the order location; a sell order remains at its listing location. Moving inventory between stations can still be required to complete the trade. [^ccp-buy-sell-orders]

Do not confuse remote order management with asset movement. Remote trade skills allow eligible order actions from a distance; they do not move goods between locations.

## Data and execution workflow

1. Select the item type ID and candidate source/destination regions or locations.
2. Retrieve current buy and sell orders for both sides.
3. Calculate source procurement VWAP for the candidate quantity.
4. Calculate destination liquidation VWAP and unfilled remainder.
5. Calculate market fees for the selected transaction path.
6. Estimate transport cost, cargo volume, route, collateral, and time.
7. Estimate risk-adjusted exposure and capital holding time.
8. Calculate net contribution, ROI, ISK/m³, and liquidation horizon.
9. Compare low/base/high price and volume scenarios.
10. Refresh data immediately before committing capital and dispatching the shipment.

Respect ESI cache headers and request limits. Store the source region, location, order-book snapshot time, price/volume, and cache metadata for every candidate. [^ccp-esi-api-explorer] [^ccp-esi-best-practices]

## Common false-arbitrage signals

1. A large gap between best ask and best bid with insufficient order depth.
2. A high destination price based on a single small order.
3. A low source price that cannot supply the required quantity.
4. A destination buy order whose range does not cover the shipment's delivery location.
5. A destination market with low historical volume and long liquidation time.
6. A trade whose transport cost exceeds the spread.
7. A route whose expected loss or collateral exposure is not included.
8. A price gap that disappears before arrival.
9. A trade that is profitable only before sales tax, broker fees, and relisting.
10. A trade that ties up capital longer than the expected return justifies.

## Related concepts

- [Market Mechanics](market-mechanics.md)
- [Demand and Liquidity](demand-and-liquidity.md)
- [Price Analysis](price-analysis.md)
- [Market Location Economics](../04-industrial-economics/market-location-economics.md)
- [Market Fees and Taxation](../04-industrial-economics/market-fees-and-taxation.md)
- [Logistics and Risk](../04-industrial-economics/logistics-and-risk.md)
- [Capital and Asset Management](../04-industrial-economics/capital-and-asset-management.md)

[^ccp-buy-sell-orders]: CCP Support, Buy and Sell Orders (updated 2020-03-10).
[^ccp-broker-fees]: CCP Support, Broker Fee and Sales Tax (updated 2026-03-02).
[^ccp-esi-api-explorer]: CCP, ESI API Explorer (accessed 2026-11-14).
[^ccp-esi-best-practices]: CCP, EVE Developer Documentation, Best Practices for ESI.
[^eveuni-hauling]: EVE University Wiki, Hauling (accessed 2026-11-14).
