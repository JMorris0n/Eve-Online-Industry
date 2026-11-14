---
type: Computation
title: Hauling Cost and Route Risk
description: Compare self-hauling and courier contracts using trips, time, capital exposure, expected cargo/ship loss, collateral coverage, and direct costs.
tags:
  - computation
  - logistics
  - hauling
  - risk
sources:
  - id: ccp-courier-contracts
    resource: https://support.eveonline.com/hc/en-us/articles/203218982-Courier-Contracts
    title: Courier Contracts | EVE Online Support (updated 2021-08-23)
  - id: ccp-asset-safety
    resource: https://support.eveonline.com/hc/en-us/articles/208289365-Asset-Safety
    title: Asset Safety | EVE Online Support (updated 2026-03-02)
  - id: eveuni-hauling
    resource: https://wiki.eveuniversity.org/Hauling
    title: Hauling | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T11:45:00Z
status: draft
---

## Purpose and scope

This model compares the expected logistics cost to an industrial cargo owner of self-hauling versus hiring a courier. It includes direct costs, pilot time, capital tied up in transit, expected cargo loss, expected ship loss, courier reward, contract fees, and collateral protection.

It does not predict route danger. Loss probabilities are scenario inputs that must be estimated for the specific ship, fit, cargo value, route, time, and current threat environment. Use low/base/high scenarios rather than treating one probability as a universal statistic.

The model is implemented in [`tools/calculations/hauling_cost.py`](../../tools/calculations/hauling_cost.py).

## Shared inputs

| Symbol | Meaning |
|---|---|
| V_c | Total cargo replacement/opportunity value |
| Vol | Total cargo volume in m³ |
| r | Annual cost of capital, decimal |
| H | Transit exposure in hours |
| N | Number of trips or contracts |

The cargo value is not a logistics cost. It is the value exposed to loss and the basis for calculating capital cost.

## Self-haul model

### Trip count

```text
Trips = ceil(total cargo volume / usable cargo capacity)
```

For a simple estimate, assume cargo value is distributed evenly across trips. If high-value items are concentrated in one trip, calculate each trip separately.

### Route loss probability

If per-jump loss probabilities are available and treated as independent:

```text
P_loss_trip = 1 - product(1 - p_jump_i)
```

If only a per-trip estimate is available, use that directly. For N repeated trips with identical per-trip risk:

```text
P_at_least_one_trip_loss
  = 1 - (1 - P_loss_trip)^N
```

This is a scenario model, not a guarantee of statistical independence. Route risk should be estimated from recent activity and the specific ship/cargo profile.

### Expected costs

```text
Direct cost
  = trips × direct cost per trip

Pilot time cost
  = trips × pilot hours per trip × value of pilot time per hour

Expected cargo loss
  = total cargo value × P_loss_trip × cargo loss severity

Expected ship loss
  = trips × P_loss_trip
    × max(ship replacement cost - insurance payout, 0)

Cargo capital cost
  = total cargo value × annual capital rate
    × transit hours per trip / 8,760

Expected self-haul cost
  = direct cost
    + pilot time cost
    + expected cargo loss
    + expected ship loss
    + cargo capital cost
```

Cargo loss severity is normally 1.0 for cargo the owner cannot recover. Use a lower value only when there is a defensible recovery/mitigation assumption. Ship replacement cost should include hull and fit; insurance payout is an offset, not a reason to treat the ship as free.

## Courier model

The courier model is from the cargo owner's perspective.

### Contract count and exposure

```text
Contracts = ceil(total cargo volume / contract capacity)

Cargo value per contract
  = total cargo value / contracts

Expected uncovered cargo loss
  = contracts × failure probability per contract
    × max(cargo value per contract - collateral per contract, 0)
```

Collateral is not a cost paid by the cargo owner when the contract succeeds. It is security posted by the courier and paid to the owner if the contract fails under the contract rules. It only protects the owner up to the collateral amount. [^ccp-courier-contracts]

### Expected costs

```text
Courier reward cost
  = contracts × reward per contract

Contract fee cost
  = contracts × contract creation fee

Cargo capital cost
  = total cargo value × annual capital rate
    × expected delivery exposure hours / 8,760

Expected courier cost
  = reward cost
    + contract fee cost
    + expected uncovered cargo loss
    + cargo capital cost
```

This model does not include a separate courier reliability penalty beyond the failure probability and uncovered cargo value. Add a stockout, production-delay, or market-opportunity penalty if a late delivery would cause additional loss.

## Comparison and decision

```text
Logistics cost per m³
  = expected logistics cost / total cargo volume

Logistics cost as % of cargo value
  = expected logistics cost / total cargo value

Difference
  = self-haul expected cost - courier expected cost
```

A positive difference means the courier estimate is lower. A negative difference means self-hauling is lower. The lowest expected cost is not always the best choice if the route-risk estimate is unreliable or the delivery window has operational value.

Also compare:
- Delivery time and scheduling flexibility.
- Structure destination access and service state.
- Collateral relative to cargo replacement value.
- Contractor reliability and contract expiry.
- Pilot attention and opportunity cost.
- Risk of a structure becoming inaccessible or entering Asset Safety. [^ccp-asset-safety]

## Worked example

Illustrative assumptions only:

- Cargo value: 1,000,000,000 ISK.
- Cargo volume: 20,000 m³.
- Self-haul capacity: 50,000 m³, one trip.
- Self-haul pilot time: 1.5 hours at 5,000,000 ISK/hour.
- Direct self-haul cost: 500,000 ISK.
- Per-trip loss probability: 1.5%.
- Ship replacement cost: 150,000,000 ISK.
- Insurance payout: 40,000,000 ISK.
- Transit exposure: 1.5 hours.
- Annual capital rate: 10%.

Self-haul expected cargo loss is 15,000,000 ISK. Expected net ship loss is 1,650,000 ISK. Pilot time costs 7,500,000 ISK. Direct cost is 500,000 ISK. Cargo capital cost is approximately 17,123 ISK. Total expected self-haul cost is approximately 24,667,123 ISK.

Assume instead:
- One courier contract.
- Reward: 12,000,000 ISK.
- Creation fee: 100,000 ISK.
- Collateral: 800,000,000 ISK.
- Failure probability: 1%.
- Expected delivery exposure: 48 hours.

Expected uncovered cargo loss is 1% × (1,000,000,000 - 800,000,000) = 2,000,000 ISK. Cargo capital cost is approximately 547,945 ISK. Total expected courier cost is approximately 14,647,945 ISK.

Under these assumptions the courier is cheaper by about 10.0 million ISK. The result is highly sensitive to the failure probability, collateral, reward, and time value assumptions.

## Sensitivity analysis

At minimum, calculate low/base/high cases for:
- Per-trip route loss probability.
- Cargo loss severity.
- Ship replacement cost and insurance payout.
- Pilot time value.
- Courier failure probability.
- Collateral relative to cargo value.
- Delivery exposure time.
- Annual cost of capital.

Do not present a single expected-cost value without its scenario assumptions.

## Limitations

- Route risk is an input, not an output inferred from jump count alone.
- The model assumes equal cargo value per trip/contract unless trips are calculated separately.
- The self-haul expected ship loss model assumes the ship is replaced after a loss and later trips continue.
- Courier failure probability is an estimate; the model does not infer contractor reliability.
- Courier collateral offsets only the cargo value it covers; it does not automatically compensate for production delay or lost market opportunity.
- The model excludes ship fitting/depreciation, cyno/fuel costs, route scouting, hauling alt training, and special transport services unless entered as direct costs.
- Asset Safety is a separate recovery mechanism with its own timing and fees; it is not cargo insurance. [^ccp-asset-safety]

## Related concepts

- [Logistics and Risk](../04-industrial-economics/logistics-and-risk.md)
- [Capital and Asset Management](../04-industrial-economics/capital-and-asset-management.md)
- [Market Location Economics](../04-industrial-economics/market-location-economics.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)
- [Capital Turnover](capital-turnover.md)

[^ccp-courier-contracts]: CCP Support, Courier Contracts (updated 2021-08-23).
[^ccp-asset-safety]: CCP Support, Asset Safety (updated 2026-03-02).
[^eveuni-hauling]: EVE University Wiki, Hauling (accessed 2026-11-14).
