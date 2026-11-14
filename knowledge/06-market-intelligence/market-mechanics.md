---
type: Concept
title: Market Mechanics
description: EVE market orders, matching, regional scope, buy-order range, market history, ESI access, and order execution constraints.
tags:
  - market
  - mechanics
  - orders
sources:
  - id: ccp-buy-sell-orders
    resource: https://support.eveonline.com/hc/en-us/articles/203218932-Buy-and-Sell-Orders
    title: Buy and Sell Orders | EVE Online Support (updated 2020-03-10)
  - id: ccp-broker-fees
    resource: https://support.eveonline.com/hc/en-us/articles/203218962-Broker-Fee-and-Sales-Tax
    title: Broker Fee and Sales Tax | EVE Online Support (updated 2026-03-02)
  - id: ccp-esi-overview
    resource: https://developers.eveonline.com/docs/services/esi/overview/
    title: EVE Swagger Interface (ESI) Overview
  - id: ccp-esi-best-practices
    resource: https://developers.eveonline.com/docs/services/esi/best-practices/
    title: Best Practices for ESI
  - id: ccp-esi-api-explorer
    resource: https://esi.evetech.net/ui/?version=latest
    title: ESI API Explorer
  - id: eveuni-market
    resource: https://wiki.eveuniversity.org/Market
    title: Trading / Market | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T08:30:00Z
status: draft
---

## Purpose

The EVE market is an order-matching system. Players create buy orders that offer ISK for items and sell orders that offer items for ISK. Orders are associated with a location, region, price, quantity, and (for buy orders) an eligible range. The market broker attempts to match new or modified orders immediately before listing any unfilled remainder. [^ccp-buy-sell-orders]

For industrial planning, the market is both a procurement system and a sales channel. A displayed price is not guaranteed revenue: execution depends on order depth, location, buy-order range, market fees, and the quantity available at the price.

## Buy orders and sell orders

| Attribute | Buy order | Sell order |
|---|---|---|
| Purpose | Offers ISK to acquire an item | Offers an item for sale |
| Location | Order is placed at a station/structure | Item is sold from the station/structure where the order is placed |
| Range | Can specify where sellers may deliver | Does not move the item away from its order location |
| Price | Maximum price the buyer offers | Minimum price the seller asks |
| Immediate matching | Matches eligible sell orders at or below the bid | Matches eligible buy orders at or above the ask |

CCP states that buy orders can specify a range, while sell orders are fulfilled at the station where they were created. Only repackaged, stackable items can be sold on the market. Assembled ships/modules and used BPOs/BPCs cannot be sold through the market; use contracts or another supported transfer method. [^ccp-buy-sell-orders]

## Immediate order matching

When a buy or sell order is created or modified, the broker first attempts to match it against existing orders. The matching rules determine both which orders are filled and the execution price. [^ccp-buy-sell-orders]

### Creating or changing a sell order

The broker considers buy orders that:
- Have a range that includes the sell-order location.
- Offer at least the seller's asking price.

The highest eligible buy order is filled first. The seller receives the price specified by the new sell order, not the higher bid price. If the sell order has more units than the first buy order wants, the broker continues to the next-highest eligible buy order until the sell order is filled or no eligible buy orders remain. Any remainder is listed as a sell order.

### Creating or changing a buy order

The broker considers sell orders offering the item at or below the new buy-order price. The lowest eligible sell order is filled first. The seller receives the price specified by the new buy order, not the lower ask price. If the buy order wants more units than the first sell order can supply, the broker continues to the next-lowest sell order. Any unfilled remainder is listed as a buy order.

This means a market order can execute immediately at the order creator's specified price, even when the opposing order offers a better price. Do not assume that crossing the spread automatically gives the buyer or seller the opposing order's price. [^ccp-buy-sell-orders]

## Market scope and location

Market orders are organized by region, while each order is anchored to a station or player-owned structure. A buy order's range determines which locations can fulfill it. A sell order remains tied to its listing location.

A region-wide market price is therefore not a single physical pool of inventory. The buyer or seller must still account for:
- The location of the order.
- The buy-order delivery range.
- The location where the output must be collected.
- The cost and risk of moving items between systems.
- Whether the player has access to the station or Upwell structure.

Remote market skills allow eligible characters to place or manage orders from a distance, but do not move the items. See [Market Location Economics](../04-industrial-economics/market-location-economics.md). [^eveuni-market]

## Market order fields

For a standard market order, the important fields include:
- Type ID of the item.
- Order ID.
- Region and location ID.
- Buy or sell order flag.
- Price per unit.
- Remaining volume.
- Total volume.
- Range for buy orders.
- Issued and expiry times.
- Minimum volume, where applicable.

For execution analysis, the most useful values are price, remaining volume, location, and range. A top-of-book price without available volume is not enough to value a production batch.

## Market history

Regional market history provides daily statistics for an item, including:
- Average price.
- Highest price.
- Lowest price.
- Daily traded volume.
- Order count.

Historical statistics describe completed market activity, not current executable liquidity. The volume field is the number of units traded; order_count is the number of completed market transactions/orders, not the number of active open orders. Average transaction size can be approximated as volume divided by order_count when order_count is nonzero. A daily average may be distorted by a small number of trades, while a high or low may represent only a small fraction of daily volume. Interpret history alongside current order depth and market context. [^ccp-esi-api-explorer] [^eveuni-market]

Do not treat order count as the number of units traded. ESI's daily history fields distinguish traded volume from order count.

## ESI market data

CCP's ESI provides the public and authorized API surface used by third-party tools. Relevant market resources include: [^ccp-esi-overview] [^ccp-esi-api-explorer]

| Resource | Purpose | Data type |
|---|---|---|
| GET /markets/{region_id}/orders/ | Current regional buy/sell orders | Current order book |
| GET /markets/{region_id}/history/?type_id=... | Daily market statistics for one item in a region | Historical price/volume |
| GET /markets/prices/ | Adjusted and average price values | CCP valuation reference |
| GET /markets/structures/{structure_id}/ | Orders in a player-owned structure | Structure-specific market orders, subject to authorization |

The exact endpoint parameters and authorization scopes should be taken from the current ESI API Explorer rather than copied from old third-party wrappers. Some structure order resources require authorization and access to the relevant structure.

### ESI caching and request behavior

ESI returns cache metadata such as Expires, Last-Modified, and ETag where supported. The Expires header indicates when updated data should become available. Do not poll a resource more frequently than its cache policy permits. ESI also uses compatibility-date versioning, recommends a pinned X-Compatibility-Date header, and now applies route-dependent rate limits. Respect cache headers, Retry-After, and error-limit responses. See [ESI and Market Data](../07-tools-and-data/esi-and-market-data.md) for the current integration contract. [^ccp-esi-best-practices]

For an automated market collector:
1. Store the response timestamp and cache headers.
2. Reuse ETags and send If-None-Match where supported.
3. Respect Expires and rate-limit/error-limit headers.
4. Handle pagination for large regional order books.
5. Store the region, type ID, order side, location, price, and volume.
6. Keep market history separate from current order snapshots.

## Adjusted price versus market price

The ESI market prices resource includes adjusted price and average price. These are distinct from the live best buy/sell orders and the daily market-history average. Adjusted price is a CCP-defined valuation input used by other game systems, including Industry EIV calculations; it is not automatically the price at which a manufacturer can buy or sell an item.

Use:
- Current buy orders for immediate liquidation estimates.
- Current sell orders for immediate procurement estimates.
- Historical averages and volume for trend/context.
- Adjusted price only for the game mechanics that explicitly use it, such as EIV-based installation costs.

See [Installation Cost Computation](../09-computations/installation-costs.md) and [Price Analysis](price-analysis.md). [^ccp-esi-api-explorer]

## Market fees

Broker fees, sales tax, and relist fees are separate from order matching. Broker fees apply when non-immediate orders are created, sales tax applies when items sell, and relist fees apply when existing order prices are modified. The current rates and formulas are documented in [Market Fees and Taxation](../04-industrial-economics/market-fees-and-taxation.md). [^ccp-broker-fees]

## Common errors

1. Treating the highest buy order as guaranteed revenue for the entire batch.
2. Treating the lowest sell order as a guaranteed procurement price for the entire input quantity.
3. Assuming a crossing order receives the opposing order's price.
4. Ignoring buy-order range and the physical location of sell orders.
5. Treating daily average price as current executable price.
6. Treating adjusted price as a market quote.
7. Ignoring ESI cache headers and pagination.
8. Assuming public regional order data exposes every player-owned structure order.
9. Forgetting that sell orders remain at the location where they were created.
10. Ignoring broker fees, sales tax, and relist fees.

## Related concepts

- [Demand and Liquidity](demand-and-liquidity.md)
- [Price Analysis](price-analysis.md)
- [Market Fees and Taxation](../04-industrial-economics/market-fees-and-taxation.md)
- [Market Location Economics](../04-industrial-economics/market-location-economics.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)
- [ESI and Market Data](../07-tools-and-data/esi-and-market-data.md)

## Source limitations

CCP's Buy and Sell Orders support article was last updated 2020-03-10. It remains the official source linked by CCP's current fee documentation for order matching and relisting. ESI's current API Explorer is the source for live endpoint parameters and authorization scopes. The current ESI cache headers must be honored at runtime.

[^ccp-buy-sell-orders]: CCP Support, Buy and Sell Orders (updated 2020-03-10).
[^ccp-broker-fees]: CCP Support, Broker Fee and Sales Tax (updated 2026-03-02).
[^ccp-esi-overview]: CCP, EVE Developer Documentation, ESI Overview.
[^ccp-esi-best-practices]: CCP, EVE Developer Documentation, Best Practices for ESI.
[^ccp-esi-api-explorer]: CCP, ESI API Explorer (accessed 2026-11-14).
[^eveuni-market]: EVE University Wiki, Trading / Market (accessed 2026-11-14).
