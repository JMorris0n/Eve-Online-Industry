---
type: Concept
title: Market Fees and Taxation
description: EVE market broker fees, transaction taxes, order modification fees, NPC station and Upwell structure differences, and relevant trade skills.
tags:
  - market
  - fees
  - taxation
  - trading
sources:
  - id: ccp-broker-fees
    resource: https://support.eveonline.com/hc/en-us/articles/203218962-Broker-Fee-and-Sales-Tax
    title: Broker Fee and Sales Tax | EVE Online Support (updated 2026-03-02)
  - id: ccp-buy-sell-orders
    resource: https://support.eveonline.com/hc/en-us/articles/203218932-Buy-and-Sell-Orders
    title: Buy and Sell Orders | EVE Online Support (updated 2020-03-10)
  - id: eveuni-market
    resource: https://wiki.eveuniversity.org/Market
    title: Trading | EVE University Wiki
  - id: eveuni-tax
    resource: https://wiki.eveuniversity.org/Tax
    title: Tax | EVE University Wiki
  - id: eveuni-trade-skills
    resource: https://wiki.eveuniversity.org/Skills:Trade
    title: Skills:Trade | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:50:00Z
status: draft
---

## Summary

EVE market transaction costs have three distinct components:

1. **Broker fee:** paid when creating a non-immediate market order.
2. **Sales tax (transaction tax):** paid by the seller when an item is sold.
3. **Relist fee:** paid when modifying the price of an existing order.

These costs have different triggers, bases, and skill modifiers. A profitability model must not collapse them into one generic market-tax percentage. CCP's current Broker Fee and Sales Tax support article was updated 2026-03-02 and is the primary source for the current NPC broker-fee formula and sales-tax baseline. [^ccp-broker-fees]

## Broker fee

A broker fee is due when a non-immediate buy or sell order is created. It is calculated from the total order value. CCP lists a 3% starting rate for NPC stations. Broker Relations reduces the fee by 0.3 percentage points per level. Unmodified standings with the NPC station's owner corporation and faction can reduce it further. [^ccp-broker-fees]

CCP's published NPC station formula is:

```text
Broker fee rate (%)
  = 3%
    - (0.3% × Broker Relations level)
    - (0.03% × unmodified faction standing)
    - (0.02% × unmodified corporation standing)
```

The maximum documented standing reductions are 0.3 percentage points from faction standing and 0.2 percentage points from corporation standing. At Broker Relations V and maximum relevant standings, the minimum NPC station broker fee is 1%. Skills that improve effective standings, such as Connections or Diplomacy, do not affect this broker-fee calculation because CCP uses unmodified standings. [^ccp-broker-fees]

The broker fee is paid when the order is created. If an order is modified to a different price, an additional fee is due. A broker fee is not the same as sales tax, and a non-immediate sell order can incur both.

### Upwell structure markets

Broker fees on Upwell structure markets differ from NPC stations:

- 0.5% of the fee goes to an NPC as an ISK sink.
- The remainder goes to the structure owner.
- Broker Relations does not apply to Upwell structure orders. [^ccp-broker-fees]

EVE University's market reference describes the Upwell broker fee as a 0.5% SCC component plus the owner-set percentage, which can vary by standings. Confirm the live structure fee before placing a large order. [^eveuni-market] [^eveuni-tax]

## Sales tax

Sales tax is charged when an item is sold and is paid by the seller. CCP lists a 7.5% starting rate. The Accounting skill reduces the rate, with CCP documenting a minimum of 3.37% at Accounting V. The tax is deducted automatically from the sale proceeds. [^ccp-broker-fees]

The common formula represented by the skill description is:

```text
Sales tax rate = 7.5% × (1 - 0.11 × Accounting level)
```

At Accounting V:

```text
7.5% × (1 - 0.55) = 3.375%
```

CCP displays the minimum as 3.37%. For exact wallet reconciliation, use the transaction record and the actual tax charged rather than assuming the interface's displayed percentage preserves all internal precision. [^ccp-broker-fees] [^eveuni-trade-skills]

Sales tax is charged to the seller whether the sale is fulfilled immediately against an existing buy order or completes later through a listed sell order. A buyer should not subtract the seller's transaction tax from the buyer's acquisition cost as a separate fee paid by the buyer.

## Relist fee

When a market order's price is modified, CCP charges another broker fee according to a relist formula. CCP defines:

- (BR): the effective broker-fee rate at the station or structure.
- (RD): the character's relist discount, affected by Advanced Broker Relations.
- (P_1): the existing order value before the change.
- (P_2): the order value after the change.

The CCP formula is:

```text
Relist fee
  = max(0, BR × (P2 - P1))
    + (1 - RD) × BR × P2
```

The first term charges the full broker-fee rate on any increase in order value. The second term charges the discounted broker fee on the new order value. [^ccp-buy-sell-orders]

EVE University documents a base relist discount of 50%, increased by 6 percentage points per level of Advanced Broker Relations, to 80% at level V. This is a secondary-source detail; the current order-modification quote is authoritative. [^eveuni-trade-skills] [^ccp-buy-sell-orders]

A price change is not free. Repeatedly undercutting competitors can consume the margin that the order was intended to earn. Before modifying an order, compare the relist fee with the expected benefit of the new price and the cost of cancelling and creating a new order.

## Immediate matching and order execution

CCP describes the market as a brokered order-matching system. When an order is created or changed, the system first attempts to match it against existing orders before listing any unfilled remainder. [^ccp-buy-sell-orders]

- A new or modified sell order can match eligible buy orders. The highest eligible buy order is filled first, but the seller receives the price offered by the sell order.
- A new or modified buy order can match eligible sell orders. The lowest eligible sell order is filled first, but the seller receives the price offered by the buy order.
- Any unfilled remainder is listed as an order if it is not immediately matched. [^ccp-buy-sell-orders]

This matters when estimating realized sale revenue. A displayed top-of-book price does not guarantee that the entire production batch will sell at that price. Check available order volume and the order's matching behavior.

## Fee treatment by transaction path

| Transaction path | Broker fee | Sales tax | Relist fee |
|---|---|---|---|
| Immediate sale into existing buy orders | No non-immediate order fee for the immediate fill | Seller pays tax on completed sale | None unless modifying a pre-existing order |
| Create a sell order that remains listed | Fee on order creation | Seller pays tax as units sell | Applies when order price is modified |
| Immediate purchase from existing sell orders | No non-immediate order fee for the immediate fill | Seller pays tax, not buyer | None unless modifying a pre-existing order |
| Create a buy order that remains listed | Fee on order creation | Seller pays tax when buy order is filled | Applies when order price is modified |

The table is a transaction-cost classification. Exact fee handling for mixed immediate fills and unfilled remainders should be checked against the order quote and wallet journal.

## Profitability implications

For a manufacturer selling completed output:

- **Immediate liquidation:** estimate proceeds from available buy-order depth and subtract sales tax. This avoids the cost and delay of creating a non-immediate sell order, but may realize a lower price.
- **Sell-order strategy:** estimate proceeds at a realistic sell price, then subtract sales tax, initial broker fee, and any expected relist fees. Account for the time the inventory may remain unsold.
- **Buy-side sourcing:** include broker fees if placing non-immediate buy orders. An immediate purchase against existing sell orders does not incur the same order-creation broker fee.
- **Upwell market:** use the structure's current owner fee and do not apply Broker Relations to it.

Market fees are distinct from Industry installation fees. Industry installation fees are incurred when a production/science/reaction job is installed; market fees are incurred when market orders are created, modified, or filled. See [Installation Cost Computation](../09-computations/installation-costs.md).

## Source and data limitations

The CCP Broker Fee and Sales Tax page was updated 2026-03-02 and is the primary source for the rates and NPC broker-fee formula. CCP's Buy and Sell Orders article was last updated 2020-03-10 but is still the linked official source for matching and relist-fee mechanics. EVE University provides supporting details for Upwell owner-set fees and Advanced Broker Relations. Verify any large transaction against the live order window and wallet journal.

## Related concepts

- [Industrial Cost Accounting](cost-accounting.md)
- [Manufacturing Profitability](manufacturing-profitability.md)
- [Market Location Economics](market-location-economics.md)
- [Installation Cost Computation](../09-computations/installation-costs.md)

[^ccp-broker-fees]: CCP Support, Broker Fee and Sales Tax (updated 2026-03-02).
[^ccp-buy-sell-orders]: CCP Support, Buy and Sell Orders (updated 2020-03-10).
[^eveuni-market]: EVE University Wiki, Trading / Market (accessed 2026-11-14).
[^eveuni-tax]: EVE University Wiki, Tax (accessed 2026-11-14).
[^eveuni-trade-skills]: EVE University Wiki, Skills:Trade (accessed 2026-11-14).
