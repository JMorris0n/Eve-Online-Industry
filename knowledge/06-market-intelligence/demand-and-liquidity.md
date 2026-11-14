---
type: Concept
title: Demand and Liquidity
description: Measuring traded volume, transaction frequency, order-book depth, spreads, execution impact, inventory absorption, and market liquidity.
tags:
  - market
  - demand
  - liquidity
sources:
  - id: ccp-esi-api-explorer
    resource: https://esi.evetech.net/ui/?version=latest
    title: ESI API Explorer
  - id: ccp-esi-best-practices
    resource: https://developers.eveonline.com/docs/services/esi/best-practices/
    title: Best Practices for ESI
  - id: ccp-buy-sell-orders
    resource: https://support.eveonline.com/hc/en-us/articles/203218932-Buy-and-Sell-Orders
    title: Buy and Sell Orders | EVE Online Support (updated 2020-03-10)
  - id: eveuni-market
    resource: https://wiki.eveuniversity.org/Market
    title: Trading / Market | EVE University Wiki
  - id: eve-cyno-market-history
    resource: https://data.eve-cyno.dev/docs/tools/get_market_history
    title: EVE-CYNO Data Market History Documentation
  - id: everef-market-history
    resource: https://docs.everef.net/datasets/market-history.html
    title: EVE Ref Market History Dataset Documentation
generated:
  by: openai/gpt-6
  at: 2026-11-14T08:40:00Z
status: draft
---

## Purpose

Demand and liquidity analysis estimates whether a product can be bought or sold in the required quantity, at a realistic price, within an acceptable time. It is essential for manufacturing decisions because a positive unit margin does not guarantee that the full production batch can be liquidated at the displayed top-of-book price.

Liquidity is quantity- and location-dependent. A product can be liquid in one region and illiquid in another, or liquid for a small order but illiquid for a large industrial batch.

## Core market signals

| Signal | What it measures | Main data source |
|---|---|---|
| Daily traded volume | Units that changed hands during a day | ESI market history |
| Daily transaction count | Number of completed market transactions/orders | ESI market history |
| Average transaction size | Approximate units per transaction | Volume ÷ transaction count |
| Bid/ask spread | Difference between best buy and sell prices | Current order book |
| Order-book depth | Quantity available at nearby price levels | Current order book |
| Daily ISK turnover | Approximate ISK value traded per day | Daily volume × representative price |
| Price volatility | Variation in historical transaction prices | ESI market history |
| Order competition | Number of active orders near the best price | Current order book |
| Inventory absorption horizon | Time required for the market to absorb a planned quantity | Historical volume and target market share |

ESI market history provides daily average, highest, lowest, order_count, and volume fields. Volume is the number of units traded. The order_count field is the number of completed market transactions/orders, not the number of currently open orders. Average transaction size can therefore be estimated as volume divided by order_count when order_count is nonzero. [^ccp-esi-api-explorer] [^eve-cyno-market-history]

## Historical volume and transaction frequency

Use multiple time windows rather than relying on a single daily observation:

- 7-day window: recent activity, sensitive to short-term spikes.
- 30-day window: near-term demand and supply context.
- 90-day window: broader baseline and patch/seasonality context.
- Longer history: structural trend, where the current ESI retention permits.

For each window, calculate:
- Total traded units.
- Mean daily volume, including zero-trade days.
- Median daily volume.
- Lower-percentile daily volume, such as the 25th percentile.
- Mean and median daily transaction count.
- Average transaction size.
- Mean daily ISK turnover.

A key data-cleaning issue: ESI market-history results may omit days with no trades. If the returned rows are averaged directly, the result overstates average daily volume. Reconstruct the full calendar window and insert zero-volume days before calculating daily averages and percentiles. [^eve-cyno-market-history]

Transaction count and volume should be read together. A large daily volume with very few transactions can be driven by one or two large trades and may not represent broad, repeatable demand. A high transaction count with modest volume can indicate smaller, more frequent purchases.

## Order-book depth

The current order book shows the quantity available at each price level. It is a snapshot, not a guarantee that the orders will remain available.

For immediate selling, sort eligible buy orders from highest to lowest price. For immediate procurement, sort sell orders from lowest to highest price. The broker's matching rules and buy-order range determine which orders can execute. [^ccp-buy-sell-orders]

### Volume-weighted execution price

For a quantity Q to sell into buy orders:

```text
Gross proceeds(Q)
  = sum over eligible buy orders:
      filled quantity at order price

VWAP sell price(Q)
  = Gross proceeds(Q) / quantity actually filled
```

For procurement, apply the same method to eligible sell orders sorted from lowest to highest price.

If the available order-book depth is smaller than Q, the remaining quantity is not immediately executable at the observed prices. Model the remainder as unsold inventory or a future sell order rather than assigning it the current top-of-book price.

### Spread

When both a best bid and best ask exist:

```text
Midpoint = (best bid + best ask) / 2

Bid/ask spread (%)
  = (best ask - best bid) / midpoint × 100
```

A narrow spread can indicate active competition and easier execution, but it does not prove that enough volume exists. Always evaluate depth alongside spread.

### Depth within a price band

A configurable depth measure can sum order volume within a percentage of the midpoint or best price.

For example:
- Buy depth within 1% of best bid.
- Sell depth within 1% of best ask.
- Total bid/ask depth within 2% of midpoint.

The band is a model parameter, not a CCP mechanic. Use the same band when comparing products or locations.

## Market absorption and liquidation horizon

Historical volume is a proxy for demand, not a guarantee that a new producer can capture all of it. The operation should choose a conservative target share of observed daily volume.

Let:
- Q = quantity the operation intends to sell.
- ADV = average daily traded volume over the chosen window.
- s = assumed share of daily volume the operation can capture.

```text
Estimated liquidation days
  = Q / (ADV × s)
```

Use a range of target shares for low/base/high scenarios. Do not assume a new producer can capture 100% of historical volume without affecting price or displacing competitors.

For production planning, compare:
- Planned daily output.
- Conservative daily market volume.
- Current buy-order depth.
- Existing sell-order depth.
- Estimated liquidation days.
- The likely effect of adding the operation's own inventory to supply.

If output accumulates faster than the market can absorb it, the operation is building inventory rather than generating cash.

## Liquidity classification

A qualitative classification is often more useful than a single arbitrary liquidity score.

| Class | Typical indicators | Production implication |
|---|---|---|
| Deep | Consistent volume, many transactions, tight spread, substantial bid/ask depth | Larger batches may be supportable |
| Moderate | Regular trades but limited depth or variable spread | Batch size should be tied to conservative volume |
| Thin | Low/irregular volume, wide spread, shallow book, few transactions | Small batches, longer sale horizon, or avoid production |
| Episodic | Large spikes separated by little activity | Do not extrapolate peak-day demand |

These labels should be defined by project-specific thresholds and the product's price/volume profile. A single universal threshold would misclassify different market segments.

## Volatility and demand quality

Daily average, high, and low prices can be used to identify large price swings, but they do not reveal the full distribution of trades. For robust analysis:
- Use rolling windows.
- Compare median/mean daily prices where the underlying source permits.
- Calculate daily returns and a rolling volatility measure.
- Flag unusually large price/volume spikes.
- Compare current order depth with historical turnover.
- Treat very low transaction counts as a warning that one trade can dominate the daily statistics.

High volume is not always stable demand. It may reflect patch-driven speculation, temporary shortages, a single large buyer, or inventory liquidation. Separate recurring demand from one-time events where possible.

## Supply pressure and order competition

The order book can indicate current competition:
- Number of sell orders near the best ask.
- Quantity offered near the best ask.
- Number of buy orders near the best bid.
- Quantity demanded near the best bid.
- Concentration of orders at one location.
- Frequency of price changes, where a third-party snapshot service records them.

A large sell wall near the best ask can make a producer's output harder to sell even when historical volume is high. A large buy wall can support liquidation, but it may disappear before the batch is delivered.

ESI regional order snapshots and historical volume should be stored separately. Historical data is a longer-term demand signal; the order book is a short-lived execution signal. [^ccp-esi-best-practices] [^everef-market-history]

## Industrial batch sizing

A batch should be sized against conservative demand and realistic execution depth.

A basic maximum daily production target is:

```text
Target daily output
  ≤ conservative ADV × selected market share
```

A batch size should also consider:
- Manufacturing job run limits and BPC licensed runs.
- Material rounding and number of separate jobs.
- Installation fees.
- Peak working capital.
- Time required to move output to the market.
- Market depth at the time of sale.
- Expected time to sell the output.
- Price risk during the holding period.

The batch with the highest theoretical margin may be inferior if its inventory takes too long to liquidate.

## Data collection and reproducibility

For each product/region observation, store:
- Type ID and product name.
- Region ID and region name.
- Observation timestamp and ESI cache headers.
- Daily volume and transaction count.
- Daily high, low, and average.
- Best bid and ask.
- Depth at selected price bands.
- Price/volume window and zero-trade-day treatment.
- Market data source and retrieval version.

Respect ESI cache headers and ETags. Do not poll faster than the endpoint's Expires value. For large market-history archives, account for the fact that new data can be discovered later and historical archive files may be updated in place. [^ccp-esi-best-practices] [^everef-market-history]

## Common errors

1. Treating top-of-book price as executable for the full production batch.
2. Treating daily volume as guaranteed demand available to one producer.
3. Averaging only returned ESI history rows without inserting zero-trade days.
4. Treating order_count as active open orders rather than completed transactions.
5. Treating order count and volume as interchangeable.
6. Ignoring average transaction size and whale-driven activity.
7. Using a narrow spread as proof of deep liquidity.
8. Ignoring current buy/sell depth and relying only on historical averages.
9. Assuming regional history is station-specific.
10. Ignoring the effect of the producer's own supply on market prices.

## Related concepts

- [Market Mechanics](market-mechanics.md)
- [Price Analysis](price-analysis.md)
- [Regional Arbitrage](regional-arbitrage.md)
- [Product Selection](product-selection.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)
- [Market Location Economics](../04-industrial-economics/market-location-economics.md)

[^ccp-esi-api-explorer]: CCP, ESI API Explorer (accessed 2026-11-14).
[^ccp-esi-best-practices]: CCP, EVE Developer Documentation, Best Practices for ESI.
[^ccp-buy-sell-orders]: CCP Support, Buy and Sell Orders (updated 2020-03-10).
[^eveuni-market]: EVE University Wiki, Trading / Market (accessed 2026-11-14).
[^eve-cyno-market-history]: EVE-CYNO Data, Market History documentation (accessed 2026-11-14).
[^everef-market-history]: EVE Ref, Market History dataset documentation (accessed 2026-11-14).
