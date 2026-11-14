---
type: Concept
title: Industrial Cost Accounting
description: Cost basis, opportunity cost, input valuation, installation fees, realized profit, and inventory accounting conventions.
tags:
  - economics
  - accounting
  - costs
sources:
  - id: eveuni-manufacturing
    resource: https://wiki.eveuniversity.org/Manufacturing
    title: Manufacturing | EVE University Wiki
  - id: ccp-viridian-fees
    resource: https://www.eveonline.com/news/view/viridian-expansion-notes
    title: Viridian Expansion Notes | EVE Online (2023-06-09)
  - id: ccp-esi-overview
    resource: https://developers.eveonline.com/docs/services/esi/overview/
    title: EVE Swagger Interface (ESI) Overview
  - id: ccp-market-price-data
    resource: https://esi.evetech.net/ui/?version=latest
    title: ESI API Explorer
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:25:24Z
status: draft
---

## Summary

Industrial profitability depends on choosing a consistent valuation basis. A calculation that mixes CCP adjusted prices, actual acquisition prices, regional sell prices, and opportunity costs without labeling them can produce a mathematically consistent but economically misleading result.

This document establishes the terminology for later cost and profitability models. The current industry installation-fee mechanics are documented separately in [Installation Cost Computation](../09-computations/installation-costs.md).

## Distinct valuation concepts

| Term | Meaning | Appropriate use |
|---|---|---|
| CCP adjusted price | CCP's adjusted item valuation published through ESI | Industry EIV inputs and official fee models where specified |
| Market sell price | Current lowest sell order in the selected market | Estimating the price to buy materials immediately |
| Market buy price | Current highest buy order in the selected market | Estimating proceeds from immediate sale |
| Actual acquisition cost | Price and fees actually paid to obtain the inventory | Historical accounting and wallet reconciliation |
| Replacement cost | Current cost to replenish the same inventory | Planning a repeat production cycle |
| Opportunity cost | Value sacrificed by consuming an asset instead of its best realistic alternative use | Decisions involving self-mined, self-produced, or otherwise owned materials |
| EIV | CCP's Estimated Item Value used for industry installation fees | Fee calculation, not a claim about the operator's actual cost |
| Book value | The chosen accounting value assigned to an asset in the user's own records | Inventory and realized-profit reporting |

CCP adjusted price is not the same as regional market price. EIV is not necessarily the actual wallet cost of materials. The Manufacturing reference describes Manufacturing EIV using ME0 material quantities and CCP adjusted prices; actual material procurement decisions should be evaluated separately. [^eveuni-manufacturing] [^ccp-viridian-fees]

## Recommended accounting views

A single product evaluation should preserve at least three separate outputs:

1. **Economic production margin:** expected sale proceeds less the opportunity or replacement value of inputs, production fee, logistics, and selling costs.
2. **Cash-flow margin:** wallet proceeds less the actual cash paid during the period, adjusted for any inventory purchased earlier.
3. **Realized accounting profit:** sale proceeds less the chosen book value of inventory consumed and the fees attributable to that sale.

These values can differ materially. For example, a miner who consumes self-mined ore may have paid zero ISK at the moment of production, but the ore still has an opportunity cost because it could have been sold.

## Input valuation policy

For strategic production decisions, use replacement cost as the default input value unless the user explicitly asks for a cash-flow or historical-cost view. Replacement cost should use a named location, market side, data retrieval time, and a declared execution method.

For a quick liquidation comparison:
- Compare expected sell-order proceeds with current buy orders.
- Account for volume and market depth rather than assuming the entire quantity can transact at one displayed price.
- Distinguish a sell order's listed price from its after-fee proceeds.
- Include haul, collateral, and contract costs where relevant.

For historical reporting, preserve actual acquisition prices and fees. Do not overwrite a recorded purchase price whenever market prices change.

## Fees and cost attribution

Installation fees, market broker fees, sales taxes, hauling costs, and other transaction costs should be separate line items. CCP's industry fee equation contains EIV, activity SCI and applicable bonuses, facility tax, SCC surcharge, and Alpha-clone tax. The facility/structure portion is documented in [Installation Cost Computation](../09-computations/installation-costs.md). [^ccp-viridian-fees]

Do not count an installation fee both as part of job cost and as a second generic overhead percentage. When comparing products, attribute a fee once to the job or batch that incurred it.

## Production batch cost model

A later computation can represent the economic cost of a production batch as:

**Economic batch cost = input opportunity cost + job installation fees + ancillary job costs + logistics and handling costs**

Market sale fees belong on the selling side unless the chosen reporting convention combines them into net realized proceeds.

A per-unit economic cost is the batch cost divided by the actual delivered output quantity, not automatically the number of blueprint runs. For invention and manufacturing chains, intermediate outputs, failures, waste, and unused materials must be treated explicitly.

## Data provenance

Every price value used in a model should record:
- Item/type identifier.
- Region or system, if the value is regional.
- Market side or price definition.
- Quantity/depth assumption.
- Data provider.
- Retrieval timestamp.
- Whether the value is adjusted price, current order price, historical average, or actual transaction cost.

ESI is CCP's official REST API for third-party development. It provides public price-data routes and other market/system data through the API Explorer. Record the retrieval timestamp and ESI compatibility date when using the data programmatically. [^ccp-esi-overview] [^ccp-market-price-data]

## Limitations

This document does not yet prescribe a single book-keeping system for all future dashboards or tools. The user-facing calculator should allow the user to select replacement-cost, actual-acquisition-cost, or opportunity-cost inputs. Default strategic recommendations should use replacement/opportunity cost rather than treating owned materials as free.

## Related concepts

- [Installation Cost Computation](../09-computations/installation-costs.md)
- [Manufacturing Profitability](manufacturing-profitability.md)
- [Market Fees and Taxation](market-fees-and-taxation.md)
- [Capital and Asset Management](capital-and-asset-management.md)

[^eveuni-manufacturing]: EVE University Wiki, Manufacturing.
[^ccp-viridian-fees]: CCP, Viridian Expansion Notes (2023-06-09).
[^ccp-esi-overview]: CCP, EVE Developer Documentation, EVE Swagger Interface (ESI) Overview.
[^ccp-market-price-data]: CCP, ESI API Explorer.
