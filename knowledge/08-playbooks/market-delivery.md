---
type: Process
title: Market Delivery Playbook
description: Moving finished goods to market and executing immediate sales, sell orders, or courier delivery.
tags:
  - playbook
  - market
  - logistics
generated:
  by: openai/gpt-6
  at: 2026-11-14T09:50:00Z
status: draft
---

## Objective

Convert finished inventory into realized ISK while controlling market fees, execution price, liquidity, hauling cost, and asset exposure.

Use [Market Mechanics](../06-market-intelligence/market-mechanics.md), [Demand and Liquidity](../06-market-intelligence/demand-and-liquidity.md), [Market Fees and Taxation](../04-industrial-economics/market-fees-and-taxation.md), and [Logistics and Risk](../04-industrial-economics/logistics-and-risk.md).

## Preflight

- Confirm item type, quantity, volume, and current location.
- Choose the destination region and station/structure.
- Check current buy/sell order depth and historical volume.
- Calculate VWAP for the actual quantity.
- Check market fees at the selected location.
- Decide whether to sell locally or haul to another market.
- Confirm courier collateral, reward, route, and destination access if using a contract.
- Record the timestamp and source of every price input.

## Choose an execution path

### Immediate sale

Use when liquidity and available buy-order depth support the batch and immediate cash recovery is preferred.

- Calculate liquidation VWAP through eligible buy orders.
- Include sales tax.
- Do not include a non-immediate sell-order broker fee for the immediate fill.
- Record any quantity that cannot be filled immediately.

### Sell order

Use when the expected price premium justifies waiting and paying the order fees.

- Set an ask price based on current competition and realistic demand.
- Include initial broker fee and sales tax.
- Estimate the sale horizon from conservative daily volume.
- Set a review threshold for modifying or cancelling the order.
- Calculate the relist fee before changing price.
- Do not repeatedly undercut without checking the remaining margin.

### Courier contract

Use when moving the inventory is cheaper or safer than self-hauling.

- Set collateral against replacement value.
- Set reward and delivery window.
- Confirm package volume and destination.
- Check destination structure state and Delivery Hanger availability.
- Record collateral and expected delivery time.
- Include uncovered exposure and collateral opportunity cost.

## Order execution

1. Recheck the order book immediately before placing the order.
2. Confirm the selected station/structure and buy-order range.
3. Verify the price and quantity that will execute immediately.
4. Verify any unfilled remainder and resulting listed order.
5. Confirm broker fee and sales tax in the order/wallet UI.
6. Save the order ID and creation timestamp.
7. Monitor fills, expiry, and market changes.

## Repricing rules

Before modifying an order:
- Calculate the exact relist fee.
- Compare the fee with the expected benefit of the new price.
- Check order depth and competitor volume.
- Consider cancelling rather than paying repeated relist fees.
- Avoid repricing based only on a one-tick undercut if the product is thinly traded.

## Reconciliation

Record:
- Quantity sold and remaining.
- Actual execution prices.
- Sales tax, broker fees, and relist fees.
- Hauling reward/fuel/time and any collateral resolution.
- Net proceeds and realized contribution.
- Days from production completion to full sale.
- Any price or volume difference from the forecast.

Update the market and profitability datasets with actual outcomes. Unsold inventory is not realized revenue.
