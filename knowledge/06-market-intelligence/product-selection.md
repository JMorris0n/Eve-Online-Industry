---
type: Concept
title: Product Selection
description: Screening and ranking industrial products by contribution, throughput, capital intensity, liquidity, sourcing, skills, and risk.
tags:
  - market
  - product-selection
  - strategy
sources:
  - id: ccp-esi-api-explorer
    resource: https://esi.evetech.net/ui/?version=latest
    title: ESI API Explorer
  - id: ccp-broker-fees
    resource: https://support.eveonline.com/hc/en-us/articles/203218962-Broker-Fee-and-Sales-Tax
    title: Broker Fee and Sales Tax | EVE Online Support (updated 2026-03-02)
  - id: eveuni-manufacturing
    resource: https://wiki.eveuniversity.org/Manufacturing
    title: Manufacturing | EVE University Wiki
  - id: eveuni-market
    resource: https://wiki.eveuniversity.org/Market
    title: Trading / Market | EVE University Wiki
  - id: eveuni-hauling
    resource: https://wiki.eveuniversity.org/Hauling
    title: Hauling | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T09:10:00Z
status: draft
---

## Purpose

Product selection identifies which items are worth producing under a defined character, facility, capital, location, and market environment. The best product is not necessarily the item with the highest unit margin or highest sale price. It is the product that delivers the best risk-adjusted contribution while fitting the operation's constrained resources.

Product selection is therefore a multi-criteria decision, not a single profit-per-unit ranking.

## Required feasibility filters

Before calculating profitability, confirm that the product is operationally feasible:

1. A suitable BPO/BPC or reaction formula is available.
2. The character has the required skills and job slots.
3. The required Manufacturing, Science, or Reaction service is available at an accessible facility.
4. Required materials can be sourced in sufficient quantities.
5. The blueprint/formula supports the required output and batch size.
6. The product can be moved to a market or consumed internally.
7. The operation has enough capital for materials, fees, logistics, and inventory holding.

A product that fails a hard feasibility constraint should not be ranked as if it were ready for production.

## Product evaluation dimensions

| Dimension | Metric | Why it matters |
|---|---|---|
| Profitability | Net contribution and net margin | Measures economic value created |
| Active-attention efficiency | Net contribution per active operator-hour | Values the user's limited hands-on time and operational attention |
| Manufacturing efficiency | ISK per Manufacturing slot-hour | Values scarce character capacity |
| Science/reaction dependency | Expected BPC or reaction output per slot-hour | Identifies upstream bottlenecks |
| Capital intensity | Peak working capital and capital-days | Measures cash and inventory commitment |
| Liquidity | Conservative daily volume and order-book depth | Estimates whether output can be sold |
| Market competition | Nearby order count and depth | Indicates pricing pressure |
| Material availability | Input depth and sourcing reliability | Prevents job starvation |
| Logistics | Cost per m³ and route exposure | Measures location penalty |
| Operational risk | Structure, market, and transport exposure | Captures downside not visible in unit margin |
| Strategic value | Internal demand or chain dependency | Values products consumed by the operation itself |

Calculate the metrics using [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md), [Demand and Liquidity](demand-and-liquidity.md), [Price Analysis](price-analysis.md), and [Market Location Economics](../04-industrial-economics/market-location-economics.md).

## Product screening workflow

### 1. Generate a candidate universe

Start with products that the operation can actually produce:
- Items with accessible BPOs/BPCs.
- Items supported by current character skills.
- Products compatible with available facilities and rigs.
- Components or intermediates required by an existing production chain.
- PI commodities or reaction products that can be sourced and processed reliably.

Do not screen only by market price. The blueprint, facility, and skill constraints determine whether the product is feasible.

### 2. Estimate the complete production cost

For each candidate, calculate:
- Exact material quantities after ME and game rounding.
- Material replacement/opportunity cost at the chosen location.
- Installation fees from the Industry quote.
- Copying and invention costs where applicable.
- Reaction or component costs for upstream intermediates.
- Market fees, hauling, and handling.
- Expected failed-attempt cost for probabilistic invention.
- Capital tied up until the output sells.

Use a consistent transfer-price method for internal intermediates to avoid double-counting.

### 3. Estimate realistic revenue

Use the intended sales path:
- Immediate liquidation into current buy-order depth.
- Sell order at a plausible price with broker/relist fees and a fill horizon.
- Internal consumption at replacement or opportunity cost.

Do not multiply total output by the best displayed buy or sell price unless that order has enough eligible volume for the full quantity.

### 4. Measure market absorption

Compare planned daily output with conservative daily volume and available depth.

```text
Planned market share
  = planned daily output / conservative daily traded volume
```

A high planned share indicates that the operation may become the market. Reduce the planned output, use multiple regions, or select another product if the market cannot absorb the batch without price impact.

### 5. Evaluate capital and capacity

Record:
- Peak working capital.
- Capital-days and expected cash conversion time.
- Manufacturing slot-hours.
- Science slot-hours.
- Reaction slot-hours.
- Expected units per day.
- Expected days to liquidate output.

A product with a high margin but very long holding time may be inferior to a lower-margin product with faster capital turnover.

### 6. Stress-test the result

At minimum, test:
- Lower output price.
- Higher input prices.
- Lower market volume.
- Reduced order-book depth.
- Higher facility tax or SCI.
- Increased hauling cost.
- Longer production or sale delay.
- Invention failure variance where applicable.

A product should not be selected solely because its base-case calculation is positive.

## Ranking and Pareto analysis

A single weighted score can hide important trade-offs. A better first pass is to identify the Pareto-efficient set across:

- Net contribution per batch.
- Net contribution per active operator-hour, with time quality labeled as measured or estimated.
- ISK per constrained slot-hour.
- Contribution per capital-day.
- Conservative liquidation horizon.
- Peak capital required.
- Risk-adjusted expected loss.

A candidate is dominated if another candidate performs at least as well on every chosen metric and better on at least one, under the same assumptions. Dominated products can usually be removed from the shortlist.

For the remaining products, choose according to the operation's actual constraint:
- Capital-constrained: favor higher contribution per capital-day and lower peak capital.
- Slot-constrained: favor higher contribution per relevant slot-hour.
- Market-constrained: favor products with deeper demand and lower planned market share.
- Logistics-constrained: favor higher value density or local sourcing.
- Supply-constrained: favor products with reliable inputs or internal intermediate production.

## Make-versus-buy comparison

A product should be manufactured only if its complete economic production cost compares favorably with buying the finished product or selling the inputs.

For a candidate batch:

```text
Manufacturing advantage
  = expected net sale proceeds from manufactured output
    - total economic production cost
    - expected net proceeds from selling the input materials directly
```

If the manufacturing advantage is negative, producing the item destroys value relative to selling the inputs under the same assumptions. The operation may still manufacture it for strategic reasons, but that reason should be explicit.

## Portfolio selection

A portfolio of products can reduce dependence on one market, input, or production chain. However, diversification also spreads capital, increases inventory complexity, and may reduce scale economies.

A practical portfolio should consider:
- Shared inputs and common intermediate components.
- Competition for the same job slots.
- Overlapping market demand.
- Correlated input/output price exposure.
- Facility and logistics overlap.
- Ability to redirect materials if one product becomes unprofitable.

Avoid selecting several products that appear diversified but all depend on the same scarce moon material, reaction output, or market hub.

## Selection output

For each shortlisted product, preserve:
- Type ID and blueprint/formula ID.
- Candidate quantity and batch structure.
- Character skills and job-slot assumptions.
- Facility, system, role, rig, tax, and SCI.
- Material inputs and timestamped prices.
- Installation, market, and logistics costs.
- Sale strategy and executable order-book depth.
- Net contribution, margin, ROI, active operator-hours, net contribution per active operator-hour, slot-hour efficiency, and capital-days.
- Conservative daily volume and estimated liquidation days.
- Low/base/high scenario results.
- Unresolved assumptions and source provenance.

This allows the product ranking to be regenerated when prices, fees, skills, or facilities change.

## Common errors

1. Ranking products by unit margin alone.
2. Treating gross market price as realizable revenue.
3. Ignoring liquidity and order-book depth.
4. Ignoring capital-days and inventory holding time.
5. Failing to value owned materials at opportunity cost.
6. Double-counting internally produced intermediates.
7. Ignoring BPC, Science, or Reaction bottlenecks.
8. Selecting products with thin markets and assuming the entire batch will sell.
9. Ignoring the effect of the operation's own output on market prices.
10. Failing to stress-test the result for price, volume, and logistics changes.

## Boundaries and unresolved details

This document defines the product-selection framework. It does not rank current EVE products because that requires live market data, product-specific blueprints, facility quotes, and a stated operating environment.

Open work:
- Build a product candidate scanner using SDE type/blueprint data and ESI market data.
- Add a normalized product metric table for contribution, active operator-hours, contribution per active operator-hour, slot-hours, capital-days, liquidity, and explicit risk indicators.
- Add configurable constraints for character skills, facilities, and capital.
- Run a real candidate ranking after the operating region, character skills, and available capital are supplied or connected.

## Related concepts

- [Market Mechanics](market-mechanics.md)
- [Demand and Liquidity](demand-and-liquidity.md)
- [Price Analysis](price-analysis.md)
- [Regional Arbitrage](regional-arbitrage.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)
- [Character Specialization](../05-optimization/character-specialization.md)
- [Industrial Scaling](../05-optimization/industrial-scaling.md)

[^ccp-esi-api-explorer]: CCP, ESI API Explorer (accessed 2026-11-14).
[^ccp-broker-fees]: CCP Support, Broker Fee and Sales Tax (updated 2026-03-02).
[^eveuni-manufacturing]: EVE University Wiki, Manufacturing (accessed 2026-11-14).
[^eveuni-market]: EVE University Wiki, Trading / Market (accessed 2026-11-14).
[^eveuni-hauling]: EVE University Wiki, Hauling (accessed 2026-11-14).
