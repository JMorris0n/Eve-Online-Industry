---
type: Concept
title: Price Analysis
description: Market price definitions, historical trends, order-book valuation, volatility, outlier handling, and price provenance.
tags:
  - market
  - pricing
  - analysis
sources:
  - id: ccp-esi-api-explorer
    resource: https://esi.evetech.net/ui/?version=latest
    title: ESI API Explorer
  - id: ccp-esi-best-practices
    resource: https://developers.eveonline.com/docs/services/esi/best-practices/
    title: Best Practices for ESI
  - id: ccp-viridian-fees
    resource: https://www.eveonline.com/news/view/viridian-expansion-notes
    title: Viridian Expansion Notes | EVE Online (2023-06-09)
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
  at: 2026-11-14T08:50:00Z
status: draft
---

## Purpose

Price analysis turns raw market observations into valuation inputs and decision signals. It must distinguish current executable prices, historical transaction statistics, adjusted prices used by game mechanics, and estimated future prices.

There is no single universally correct "market price." The correct price depends on the decision being made, the quantity, the location, and the execution strategy.

## Price definitions

| Price measure | Definition | Appropriate use |
|---|---|---|
| Best buy price | Highest current eligible buy order | Immediate liquidation for a small quantity |
| Best sell price | Lowest current sell order | Immediate procurement for a small quantity |
| Volume-weighted buy execution price | Average price obtainable by selling a specified quantity into buy orders | Realistic liquidation valuation |
| Volume-weighted sell execution price | Average cost of buying a specified quantity from sell orders | Realistic procurement valuation |
| Historical daily average | ESI daily average field for completed transactions | Trend/context, not a guaranteed execution price |
| Historical high/low | Highest/lowest recorded transaction price for the day | Range and outlier context |
| Adjusted price | CCP-defined price used by mechanics such as EIV | EIV/installation-fee calculations where specified |
| Internal transfer price | Declared value used to transfer materials between internal production stages | Consolidated cost accounting |
| Forecast price | Model estimate for a future sale or purchase | Scenario analysis only |

The ESI market prices endpoint returns average and adjusted prices as separate fields. The adjusted price is not a live buy/sell quote. EIV-based installation costs use CCP-defined adjusted-price valuation, while production profitability should use the selected economic replacement or execution price. [^ccp-esi-api-explorer] [^ccp-viridian-fees]

## Current executable prices

For a defined quantity Q:

- **Procurement value:** walk the eligible sell orders from lowest to highest price until Q units are acquired.
- **Liquidation value:** walk the eligible buy orders from highest to lowest price until Q units are sold.

```text
Procurement VWAP(Q)
  = total ISK paid across filled sell orders / quantity acquired

Liquidation VWAP(Q)
  = total ISK received across filled buy orders / quantity sold
```

If the order book does not contain enough volume, report the unfilled remainder separately. Do not extrapolate the final observed price to inventory that has no current executable order.

For a large production batch, the best bid/ask alone is not sufficient. Use the actual order depth at the chosen location and buy-order range. See [Demand and Liquidity](demand-and-liquidity.md). [^eveuni-market]

## Historical price series

ESI market history provides daily average, high, low, volume, and order_count values for an item in a region. These fields describe completed market activity. The volume is traded units; order_count is the number of completed transactions/orders, not currently open orders. Some data-processing services omit days with no trades, so reconstruct the calendar series and insert zero-volume days before calculating daily averages across a fixed period. [^ccp-esi-api-explorer] [^eve-cyno-market-history]

The ESI schema labels a field average but does not define every detail of its aggregation in the API Explorer. Do not silently relabel it as a median or as a transaction-level VWAP. Preserve the original field name and use a separate calculated metric when another aggregation is required.

## Trend measures

Useful descriptive measures include:

| Measure | Formula or method | Use |
|---|---|---|
| 7-day moving average | Mean of daily price observations over 7 calendar days | Short-term movement |
| 30-day moving average | Mean over 30 calendar days | Near-term baseline |
| 90-day moving average | Mean over 90 calendar days | Broader baseline |
| Median daily average | Median of daily ESI average values in the window | Reduces sensitivity to daily spikes |
| Volume-weighted daily-average proxy | Sum(daily average × daily volume) ÷ total volume | Approximate value-weighted trend |
| Price range | Highest daily high − lowest daily low | Historical range |
| Daily return | (price today ÷ price prior day) − 1 | Period change |
| Log return | ln(price today ÷ price prior day) | Volatility calculation input |
| Rolling volatility | Standard deviation of daily log returns over a fixed window | Price instability |

The volume-weighted daily-average proxy is not an exact transaction-level VWAP unless the underlying daily average has the required aggregation properties. Label it as a proxy.

For each trend metric, preserve the window length, calendar treatment, source field, and handling of no-trade days. Do not compare two price series calculated with different conventions.

## Outlier and event handling

Price and volume spikes may be caused by:
- Patch notes or balance changes.
- New product introduction or removal.
- Temporary supply interruption.
- Large one-off purchases or liquidations.
- Market manipulation or low-liquidity price prints.
- Changes in production demand or input costs.
- Changes in taxes, facility fees, or market access.

Do not automatically delete outliers. Flag them, inspect the corresponding volume and transaction count, and compare with order-book snapshots and patch history. A high price on one trade with little volume should not dominate an industrial sale forecast.

Use multiple scenarios:
- **Low case:** conservative price and/or lower-percentile historical volume.
- **Base case:** current depth and a robust historical reference.
- **High case:** favorable price supported by evidence, not merely the highest historical print.

## Volatility and price risk

For a daily price series (P_t), calculate log returns:

```text
r_t = ln(P_t / P_(t-1))
```

A rolling standard deviation of r_t provides a descriptive volatility measure. It is not a probability forecast and should not be interpreted as a guarantee that prices remain within a fixed range.

For manufacturing, price risk is especially important when:
- Inputs are purchased well before production completes.
- Job durations are long.
- Output is bulky or slow to sell.
- A product has few daily transactions.
- The product is exposed to patch or balance changes.
- The operation holds large quantities of WIP or finished inventory.

The model should stress-test both input-price increases and output-price declines. Input and output prices may move together or independently.

## Adjusted price and EIV

Adjusted price is a separate CCP valuation measure. It should be used only where the game mechanic specifies it, such as the EIV component of Industry installation-cost calculations. It should not replace:
- The best sell price when procuring materials.
- The best buy price when liquidating output.
- A volume-weighted execution price for a large quantity.
- A chosen opportunity-cost valuation for owned materials.

See [Installation Cost Computation](../09-computations/installation-costs.md). [^ccp-viridian-fees]

## Inventory valuation

Choose the price measure according to the accounting purpose:

- **Replacement cost:** current cost to acquire equivalent material at the relevant location.
- **Opportunity cost:** value of the best alternative use or sale.
- **Historical cost:** actual acquisition cost, retained for cash-flow/accounting records.
- **Liquidation value:** expected proceeds from selling the quantity under a stated execution strategy.
- **Adjusted price:** CCP-defined value for mechanics that explicitly use it.

Do not mix these measures in one profitability calculation without labeling and reconciling them. See [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md).

## Price provenance and data quality

Every price observation should retain:
- Type ID and item name.
- Region and, for current orders, location ID.
- Market side: buy or sell.
- Quantity and order-book depth.
- Price field and calculation method.
- Observation timestamp.
- ESI cache expiry and ETag where available.
- Retrieval source and data version.
- Zero-trade-day and outlier handling.
- Any conversion or normalization applied.

Respect ESI cache headers and ETags. EVE Ref documents that archived market-history records may be discovered after an archive is initially generated and that past daily files can be updated in place. A historical data pipeline should therefore reconcile archive updates rather than assuming a daily file is immutable. [^ccp-esi-best-practices] [^everef-market-history]

## Common errors

1. Treating adjusted price as a current market price.
2. Treating daily average as guaranteed executable price.
3. Calling the ESI average a median without evidence.
4. Calculating a daily average over only days with trades.
5. Ignoring order-book depth for large quantities.
6. Using a historical high as the expected sale price.
7. Ignoring volume and transaction count when assessing price spikes.
8. Mixing regions or locations without recording the distinction.
9. Comparing price series built with different windows or data-cleaning rules.
10. Using a stale price observation without checking ESI cache metadata.

## Related concepts

- [Market Mechanics](market-mechanics.md)
- [Demand and Liquidity](demand-and-liquidity.md)
- [Regional Arbitrage](regional-arbitrage.md)
- [Product Selection](product-selection.md)
- [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)
- [Installation Cost Computation](../09-computations/installation-costs.md)

[^ccp-esi-api-explorer]: CCP, ESI API Explorer (accessed 2026-11-14).
[^ccp-esi-best-practices]: CCP, EVE Developer Documentation, Best Practices for ESI.
[^ccp-viridian-fees]: CCP, Viridian Expansion Notes (2023-06-09).
[^eveuni-market]: EVE University Wiki, Trading / Market (accessed 2026-11-14).
[^eve-cyno-market-history]: EVE-CYNO Data, Market History documentation (accessed 2026-11-14).
[^everef-market-history]: EVE Ref, Market History dataset documentation (accessed 2026-11-14).
