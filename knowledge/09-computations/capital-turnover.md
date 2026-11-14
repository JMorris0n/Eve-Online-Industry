---
type: Computation
title: Capital Turnover Computation
description: Dated cash-flow and capital-days model for peak working capital, cash conversion time, inventory turnover, and return on deployed capital.
tags:
  - computation
  - capital
  - turnover
sources:
  - id: ccp-asset-safety
    resource: https://support.eveonline.com/hc/en-us/articles/208289365-Asset-Safety
    title: Asset Safety | EVE Online Support (updated 2026-03-02)
  - id: ccp-courier-contracts
    resource: https://support.eveonline.com/hc/en-us/articles/203218982-Courier-Contracts
    title: Courier Contracts | EVE Online Support (updated 2021-08-23)
generated:
  by: openai/gpt-6
  at: 2026-11-14T07:20:00Z
status: draft
---

## Purpose

This computation measures how much capital a production cycle requires, how long the capital remains committed, and how efficiently it generates contribution. It accepts dated cash flows and inventory values; it does not forecast sale prices or guarantee a sale date.

## Required inputs

Each cash-flow event should contain:
- Timestamp.
- Amount (positive for inflow, negative for outflow).
- Event category (procurement, installation fee, logistics, market fee, sale, collateral posted/returned, other).
- Related batch or project ID.
- Whether the event is cash flow or an internal inventory transfer.

Each inventory snapshot should contain:
- Timestamp.
- Item/type ID and quantity.
- Location.
- Chosen valuation basis.
- Inventory value.
- Whether it is raw material, WIP, finished output, or blueprint asset.

## Peak working capital

Sort all cash-flow events by timestamp and calculate the cumulative net cash flow.

```text
Cumulative cash flow(t)
  = sum of all cash flows with timestamp <= t

Peak working capital
  = max(0, -min_t(Cumulative cash flow(t)))
```

This is the maximum net cash deficit reached before proceeds are recovered. Do not add internal transfers as new costs if the underlying material cost has already been counted.

## Capital-days

For each time interval between two consecutive snapshots, let (C_i) be the capital employed during that interval and (d_i) its duration in days.

```text
Capital-days = Σ(C_i × d_i)
```

Capital employed should use a consistent economic or book-value basis. If a batch's capital changes as materials are consumed, output is produced, and sales complete, record the changing inventory/cash position rather than assuming the peak capital was tied up for the entire period.

## Capital efficiency

```text
Cycle ROI (%) = Net contribution / Peak working capital × 100

Contribution per capital-day
  = Net contribution / Capital-days

Simple annualized ROI
  = Cycle ROI × 365 / Cycle duration in days
```

Simple annualized ROI is a comparison metric, not a forecast. It assumes the same cycle could be repeated at the same return and duration. Do not use it as an expected future return when market demand, capital availability, or production capacity would prevent repetition.

## Inventory turnover

For a defined measurement period:

```text
Inventory turnover
  = cost of goods sold / average inventory value

Days inventory outstanding
  = days in period / inventory turnover
```

Use the same valuation convention for cost of goods sold and average inventory. Do not mix adjusted prices, actual acquisition cost, and opportunity cost in one ratio without an explicit reconciliation.

## Cash conversion time

```text
Cash conversion time
  = timestamp of final cash recovery
    - timestamp of first production-cycle cash outflow
```

For a multi-stage operation, report:
- Procurement waiting time.
- Transport time.
- Production time.
- Finished inventory holding time.
- Sales execution time.
- Total cash conversion time.

A batch that is completed but not sold has not completed its cash conversion cycle.

## Collateral treatment

Courier collateral is temporarily committed capital, not automatically a logistics expense. For a contractor, collateral is returned after successful delivery; if the contract fails, it is paid to the issuer. For an issuer, collateral is potential compensation, not a guarantee that the entire package value is covered. [^ccp-courier-contracts]

Model collateral as:
- Cash committed while the contract is active.
- An inflow when returned or paid after failure.
- An opportunity cost during the time it is unavailable.
- An uncovered loss if cargo value exceeds collateral and the package is not delivered.

## Asset safety and inventory location

Capital at risk depends on where assets are stored. Standard Upwell Asset Safety has exceptions for FLEX structures, Abandoned-state destruction, wormhole space, and Pochven. A location-risk model must preserve those exceptions rather than assuming every Upwell asset can be recovered automatically. [^ccp-asset-safety]

## Outputs

Return:
- Peak working capital.
- Average capital employed.
- Capital-days.
- Cycle ROI.
- Contribution per capital-day.
- Inventory turnover.
- Days inventory outstanding.
- Cash conversion time.
- Capital tied up by stage and location.
- Collateral committed and duration.
- Inventory value by location and risk category.
- Data timestamps and valuation assumptions.

## Validation rules

- Cash flows must be timestamped and signed consistently.
- Collateral returned is not revenue.
- Internal transfers are not new external costs.
- Unsold output remains inventory, not realized cash revenue.
- Peak working capital and average capital employed are different measures.
- Annualized returns are descriptive comparisons, not forecasts.
- Use a single declared valuation basis for each calculation.

[^ccp-asset-safety]: CCP Support, Asset Safety (updated 2026-03-02).
[^ccp-courier-contracts]: CCP Support, Courier Contracts (updated 2021-08-23).
