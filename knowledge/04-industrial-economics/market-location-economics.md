---
type: Concept
title: Market Location Economics
description: Choosing production, sourcing, and sales locations using activity-specific system cost indices, facility fees, market depth, and logistics.
tags:
  - market
  - location
  - industry
  - logistics
sources:
  - id: ccp-manufacturing
    resource: https://support.eveonline.com/hc/en-us/articles/203210292-Manufacturing
    title: Manufacturing | EVE Online Support (updated 2024-08-29)
  - id: ccp-viridian-fees
    resource: https://www.eveonline.com/news/view/viridian-expansion-notes
    title: Viridian Expansion Notes | EVE Online (2023-06-09)
  - id: ccp-esi-overview
    resource: https://developers.eveonline.com/docs/services/esi/overview/
    title: EVE Swagger Interface (ESI) Overview
  - id: ccp-market-price-data
    resource: https://esi.evetech.net/ui/?version=latest
    title: ESI API Explorer
  - id: eveuni-manufacturing
    resource: https://wiki.eveuniversity.org/Manufacturing
    title: Manufacturing | EVE University Wiki
  - id: eveuni-market
    resource: https://wiki.eveuniversity.org/Market
    title: Trading | EVE University Wiki
  - id: eveuni-industry-location
    resource: https://wiki.eveuniversity.org/Industry
    title: Industry | EVE University Wiki
  - id: eve-omnitool-manufacturing
    resource: https://eve-omnitool.com/industry/manufacturing/cost
    title: EVE Omnitool Industry Cost Calculator
  - id: eo-map-industry
    resource: https://eo-map.com/industry-cost-index/
    title: EVE Online Industry Cost Index Map | EO-Map
generated:
  by: openai/gpt-6
  at: 2026-11-14T07:00:00Z
status: draft
---

## Purpose

The best industrial location is not necessarily the system with the lowest installation cost or the region with the highest displayed sell price. A useful location decision compares the full cost of sourcing inputs, installing jobs, moving assets, and selling output under realistic market depth and risk.

A manufacturing location and a sales location can be different. Remote job-start skills allow a character to install jobs away from their current system, but they do not move blueprints, materials, or finished goods. CCP requires the blueprint and required materials to be at the destination facility. [^ccp-manufacturing]

## The location decision has four dimensions

1. **Job installation economics:** activity-specific System Cost Index (SCI), structure role bonus, eligible rigs, facility tax, SCC surcharge, and Alpha tax.
2. **Input procurement:** local replacement prices, order depth, number of suppliers, and the cost of transporting inputs to the facility.
3. **Output realization:** local buy-order depth, sell-order competition, sales tax, broker fees, and the time required to sell.
4. **Logistics and operational risk:** route distance, cargo volume, ship/hauler capability, collateral, security status, structure access, and service-module continuity.

A location comparison that considers only the SCI or only the market sell price is incomplete. [^ccp-viridian-fees] [^eveuni-manufacturing] [^eveuni-market]

## System Cost Index

The SCI is activity-specific and dynamic. A system can have different indices for Manufacturing, Reaction, Invention, Copying, ME Research, and TE Research. Always compare the index for the actual job activity rather than treating the system as having one universal industry-cost percentage. [^ccp-esi-overview] [^eveuni-manufacturing]

The public ESI resource `GET /industry/systems/` exposes current system cost-index data by activity for supported systems. It is suitable for automated location comparisons, subject to the ESI cache and update behavior. The published system data does not include wormhole-space systems; use the in-game Industry quote for a wormhole facility. [^ccp-esi-overview] [^ccp-market-price-data] [^eveuni-industry-location]

Do not reproduce historical SCI formulas from old guides. EVE University's Manufacturing page warns that the older 28-day square-root description may no longer be correct after CCP changed the SCI formula to make it more volatile. Use the current ESI value or the Industry window instead of inferring the index from historical job hours. [^eveuni-manufacturing]

## Facility comparison

For each candidate facility, capture:

| Field | Why it matters |
|---|---|
| Solar system and region | Determines SCI, market region, and route |
| Activity | SCI and rig applicability differ by activity |
| Facility type and structure | Determines available services and role bonuses |
| Online service module | Determines whether the required activity is currently available |
| Structure role bonus | Modifies the relevant job property or SCI component |
| Rig type and size | Determines activity/item eligibility and effect strength |
| System security class | Changes the strength of some structure rig effects |
| Facility tax | Owner-set or NPC facility fee component |
| Asset access and permissions | Determines whether the character/corporation can use the facility |
| Fuel and service continuity | Determines operational availability and interruption exposure |

The Industry installation-fee equation is documented in [Installation Cost Computation](../09-computations/installation-costs.md). Raitaru, Azbel, and Sotiyo role bonuses, as well as security-specific rig effects, are documented in [Facilities and Rigs](../01-foundations/facilities-and-rigs.md). Do not assume the facility with the lowest SCI has the lowest total job fee.

## Market location and regional price data

Market prices must be tied to a location and price definition.

| Price input | Use |
|---|---|
| Lowest sell order | Estimate the cost of buying inputs immediately |
| Highest buy order | Estimate proceeds from immediately selling output |
| Sell-order depth | Estimate the quantity available at each ask price |
| Buy-order depth | Estimate the quantity that can be liquidated at each bid price |
| Daily history | Understand realized trade prices, volume, and price variation |
| Adjusted price | Industry EIV and other CCP-defined valuation bases, not a substitute for current market price |

ESI provides public regional market orders and historical market data, while the adjusted-price resource is separate. ESI is CCP's official REST interface. Record the region, item type ID, market side, quantity/depth, retrieval time, and cache information for each value. [^ccp-esi-overview] [^ccp-market-price-data]

A regional sell price is not automatically realizable. If a production batch is larger than the available buy-order depth, the remainder may need to be listed or sold at lower price levels. Use volume-weighted execution estimates instead of multiplying the entire batch by the top bid or lowest ask. [^eveuni-market]

## Total landed cost

For a candidate production location (L):

```text
Total landed production cost(L)
  = input replacement/opportunity cost at source
  + input procurement fees
  + inbound logistics
  + industry installation fees at L
  + facility and service costs
  + outbound logistics
  + market fees at sale location
```

The model should preserve the distinction between input price and transport cost. For example, buying a material cheaply in one region and hauling it to a low-SCI system may be worse than buying locally if the transport cost, time, collateral exposure, and working capital exceed the savings.

For a completed product, compare at least:
- Produce and sell at the same location.
- Buy inputs at a market hub, haul to the production facility, then haul output back.
- Source inputs near the facility and sell output at the nearest liquid market.
- Use a market facility with a different fee schedule if its owner-set rate and access conditions are favorable.

## Break-even location comparison

For two candidate locations A and B:

```text
Location advantage of A over B
  = total landed cost(B) - total landed cost(A)
```

A positive value means A is cheaper under the declared assumptions. This is not a universal facility ranking; it depends on the selected item, activity, run count, material source, market route, and execution strategy.

A useful first filter is to calculate the maximum additional logistics cost that a lower-SCI facility can tolerate:

```text
Maximum extra logistics cost
  = installation fee at higher-cost location
    - installation fee at lower-cost location
```

If the additional hauling, collateral, and time cost exceeds this amount, the lower-SCI location is not economically preferable on installation savings alone.

## Security and structure considerations

Security status changes more than travel risk. Some Upwell rig effects are stronger in low security, null security, and wormhole space, but rig families do not all share the same scaling. Manufacturing rig scaling and reaction rig scaling are distinct. Use the activity-specific values in [Facilities and Rigs](../01-foundations/facilities-and-rigs.md), and verify the actual job quote. [^eveuni-manufacturing] [^eve-omnitool-manufacturing]

A remote manufacturing facility may reduce job fees but increase hauling and asset exposure. A facility in a high-traffic system may have higher SCI but lower input acquisition and output delivery costs. The location decision is an optimization over all these costs, not a race to the lowest SCI.

## Remote installation and asset movement

Supply Chain Management, Scientific Networking, and Remote Reactions expand where a character can start relevant jobs. They do not move assets. The blueprint and materials must already be available at the destination facility. Finished goods remain at the selected output location until transported or sold. [^ccp-manufacturing]

Remote market skills also do not transport inventory. They allow eligible orders to be created or managed from a distance, subject to skill range and market rules. The goods remain in their actual station or structure location. [^eveuni-market]

## Practical location-selection workflow

1. Select the item and activity.
2. Identify candidate facilities that support the activity and have the required service online.
3. Retrieve the current activity-specific SCI for each candidate system.
4. Record facility role bonus, rig type/security modifier, tax, and current service state.
5. Price the input bill of materials at the source location using the intended buy strategy.
6. Calculate inbound logistics and asset staging cost.
7. Retrieve the output market order book and estimate realistic sale proceeds at each candidate sales location.
8. Calculate sales tax, broker fees, relist fees, and any market-transfer costs.
9. Add outbound logistics, risk, and working-capital time.
10. Compare total landed cost, contribution, slot-hour efficiency, and capital turnover.

## Data freshness and reproducibility

Store a location quote as a timestamped observation. At minimum, record:
- System and region.
- Facility/structure identifier.
- Activity and current SCI.
- Structure role and rig configuration.
- Facility tax and SCC/Alpha fee assumptions.
- Market region, station/structure, order side, price, volume, and retrieval time.
- Logistics route, cargo volume, collateral, and assumed hauling cost.

The in-game Industry quote should be treated as the final source for installation fees. ESI and market tools are inputs for comparison and automation, not substitutes for a quote immediately before job installation.

## Boundaries and open work

This document defines the location-economics framework. It does not rank systems or trade hubs, since those rankings change with activity, market conditions, structure access, and logistics assumptions.

Open work:
- Build a current ESI collector for system SCI and market orders/history.
- Add a region/system/station model for price provenance and facility access.
- Verify the current ESI system-index coverage and caching behavior.
- Build a location-comparison worksheet using one representative manufacturing product.
- Add hauling cost and route-risk models to the logistics concept.

## Related concepts

- [Industrial Cost Accounting](cost-accounting.md)
- [Market Fees and Taxation](market-fees-and-taxation.md)
- [Manufacturing Profitability](manufacturing-profitability.md)
- [Facilities and Rigs](../01-foundations/facilities-and-rigs.md)
- [Installation Cost Computation](../09-computations/installation-costs.md)
- [Logistics and Risk](logistics-and-risk.md)

[^ccp-manufacturing]: CCP Support, Manufacturing (updated 2024-08-29).
[^ccp-viridian-fees]: CCP, Viridian Expansion Notes (2023-06-09).
[^ccp-esi-overview]: CCP, EVE Developer Documentation, ESI Overview.
[^ccp-market-price-data]: CCP, ESI API Explorer.
[^eveuni-manufacturing]: EVE University Wiki, Manufacturing (accessed 2026-11-14).
[^eveuni-market]: EVE University Wiki, Trading / Market (accessed 2026-11-14).
[^eveuni-industry-location]: EVE University Wiki, Industry (accessed 2026-11-14).
[^eve-omnitool-manufacturing]: EVE Omnitool, Industry Cost Calculator (accessed 2026-11-14).
[^eo-map-industry]: EO-Map, EVE Online Industry Cost Index Map (accessed 2026-11-14).
