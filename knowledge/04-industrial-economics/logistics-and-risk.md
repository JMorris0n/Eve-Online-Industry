---
type: Concept
title: Logistics and Risk
description: Industrial asset movement, hauling methods, courier contracts, route exposure, Upwell asset safety, structure continuity, and risk-adjusted logistics costs.
tags:
  - logistics
  - risk
  - hauling
  - asset-safety
sources:
  - id: ccp-courier-contracts
    resource: https://support.eveonline.com/hc/en-us/articles/203218982-Courier-Contracts
    title: Courier Contracts | EVE Online Support (updated 2021-08-23)
  - id: ccp-asset-safety
    resource: https://support.eveonline.com/hc/en-us/articles/208289365-Asset-Safety
    title: Asset Safety | EVE Online Support (updated 2026-03-02)
  - id: ccp-upwell-quick-facts
    resource: https://support.eveonline.com/hc/en-us/articles/209985225-Upwell-Structures-Quick-Facts
    title: Upwell Structures Quick Facts | EVE Online Support
  - id: ccp-structure-deployment
    resource: https://support.eveonline.com/hc/en-us/articles/208289335-Upwell-Structure-Deployment-and-Unanchoring
    title: Upwell Structure Deployment and Unanchoring | EVE Online Support
  - id: eveuni-hauling
    resource: https://wiki.eveuniversity.org/Hauling
    title: Hauling | EVE University Wiki
  - id: eveuni-asset-safety
    resource: https://wiki.eveuniversity.org/Asset_safety
    title: Asset Safety | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T07:10:00Z
status: draft
---

## Purpose

Industrial logistics is the movement and protection of inputs, blueprints, intermediate products, and finished goods between extraction sites, production facilities, and markets. Its economic cost includes more than a courier reward or fuel bill: it also includes time, collateral, working capital, route risk, structure availability, and the possibility of losing assets.

A production plan should evaluate logistics as part of the bill of economics, not as an afterthought.

## Logistics decision types

| Method | Typical use | Main cost/risk variables |
|---|---|---|
| Self-haul | Small/medium loads, flexible timing, controlled asset movement | Ship and fitting cost, time, fuel, route exposure, cargo value |
| Commercial courier contract | Large or inconvenient loads, outsourced transport | Reward, collateral, volume, route, destination access, contractor reliability |
| Buy at destination | Avoid moving low-value bulky inputs | Local price premium, order depth, availability |
| Distributed production | Process materials near extraction or source | Multiple facilities, inter-system transfers, inventory staging, service availability |
| Sell at production location | Avoid outbound hauling | Local market depth, local price, order fees, buyer availability |

The best option depends on the value density of the cargo, the route, the production location, and the value of the player's time. EVE University's hauling guide emphasizes that ship choice depends on space type, cargo size, and cargo value; no one hull is universally best. [^eveuni-hauling]

## Cargo exposure and route risk

The economic exposure of a haul is not just the cargo value. It can include the hauling ship and fit, collateral committed to a courier contract, replacement cost of the assets, and the cost of delayed production if the shipment is lost or late.

Risk varies by space and route:

- **High security:** CONCORD response does not make cargo immune to suicide ganking. Cargo value, ship tank, route activity, and pilot behavior affect exposure.
- **Low security:** gate camps and station/grid control can threaten ships that cannot avoid or survive interception.
- **Null security:** bubbles, camps, sovereignty/coalition access, and route intelligence materially affect risk.
- **Wormhole space:** routes are transient, mass-limited, and can close. A destination structure may have no standard asset safety.
- **Pochven:** asset-safety treatment follows the special ejection rules described by CCP, and route access differs from known space.

These are risk categories, not deterministic loss probabilities. A risk model should use route-specific observations and the current operational situation rather than a universal cargo-value threshold. [^eveuni-hauling] [^ccp-asset-safety]

## Self-hauling economics

For a self-haul, estimate:

```text
Expected logistics cost
  = ship operating/depreciation cost
    + fuel and consumables
    + pilot time opportunity cost
    + expected cargo loss
    + expected ship/fit loss
    + handling and transfer costs
```

For a simplified expected-loss term:

```text
Expected cargo loss = probability of cargo loss × cargo replacement value

Expected ship loss = probability of ship loss ×
  (ship and fit replacement cost - expected insurance recovery)
```

The probability estimates must be tied to the route, cargo profile, ship, fit, and operating behavior. They should not be invented from security status alone. Insurance recovery applies to the ship hull under the relevant insurance rules; it does not reimburse the cargo.

Value density is a useful screening metric:

```text
Cargo value density = cargo replacement value / cargo volume
```

High value-density cargo can justify a different ship, route, or courier method than low-value bulk materials. Blueprint originals, rare components, and compact high-value materials should be evaluated separately from minerals or large-volume PI goods.

## Courier contracts

A courier contract packages the selected items and requires the contractor to post collateral. CCP states that the collateral is returned to the contractor on successful delivery. If the contract fails, the issuer receives the collateral. [^ccp-courier-contracts]

The issuer should set collateral based on the replacement value of the package and the risk of non-delivery. If collateral is below replacement value, the issuer remains exposed to the uncovered amount.

```text
Uncovered cargo exposure
  = max(0, cargo replacement value - courier collateral)
```

Courier contracts can fail if the package is broken open, lost, or not delivered within the contract's delivery window. CCP also documents special behavior when a start or destination structure is destroyed or unanchored. A destination Upwell structure's Delivery Hanger may be unavailable if the structure lacks a Quantum Core or is in Low Power or Abandoned state. [^ccp-courier-contracts]

The contract issuer should verify:
- Package volume and replacement value.
- Collateral amount.
- Reward and delivery time.
- Start and destination structures.
- Whether the destination is in wormhole space.
- Whether the destination's Delivery Hanger is online.
- Whether the courier can realistically traverse the route.
- Whether a delay would interrupt an active production chain.

Collateral is not a transport fee. It is capital temporarily committed by the contractor and a security amount that can compensate the issuer if the contract fails. Reward, collateral, and cargo value must be modeled separately.

## Upwell Asset Safety

Asset Safety is a recovery mechanism for eligible assets stored in standard Upwell Structures. It is not a guarantee that all industrial assets are recoverable.

CCP's current Asset Safety article states: [^ccp-asset-safety]

- Asset Safety is available in standard Upwell Structures but not specialized Upwell FLEX structures.
- It normally triggers when a structure is destroyed or unanchored, or when manually activated.
- It does not automatically trigger when a structure in Abandoned state is destroyed.
- In wormhole space and Pochven, assets that would normally enter Asset Safety are instead ejected into containers around the structure.
- Boarded ships are not moved into Asset Safety.
- After five days, assets can be moved to an eligible destination. If not manually moved within 20 days after creation, the system automatically moves them according to the origin space rules.

CCP's Upwell quick facts confirm that in known space, destroyed structures in Abandoned state eject assets, while structures in other states normally send eligible assets to Asset Safety. [^ccp-upwell-quick-facts]

A structure can enter Abandoned state after it has not consumed fuel from service modules for seven days. The structure's operational state is therefore a material logistics risk, especially when valuable BPOs, materials, or finished products are staged in a player-owned facility. [^ccp-asset-safety]

Do not treat wormhole or Pochven Upwell storage as protected by standard Asset Safety. A structure loss can expose the stored assets to immediate recovery by other players. Also distinguish personal assets, corporation assets, ships in hangars, ships boarded by pilots, and assets in specialized FLEX structures.

## Industrial continuity risk

A production chain can be interrupted by more than a missing input:

- Facility service module offline or unfueled.
- Structure entering Low Power or Abandoned state.
- Structure destruction, unanchoring, or ownership/access change.
- Courier contract delay or failure.
- Market supply interruption.
- Route closure or loss of wormhole access.
- Market price movement while materials or output are in transit.
- Character job-slot or blueprint availability constraints.

A resilient plan should avoid concentrating all critical blueprints, input inventory, and finished output in one vulnerable location. The appropriate degree of separation depends on hauling cost, asset value, facility access, and the risk of structure failure.

## Risk-adjusted logistics model

For a candidate transport plan:

```text
Risk-adjusted logistics cost
  = direct transport cost
    + time opportunity cost
    + expected uncovered cargo loss
    + expected ship/fit loss
    + collateral financing cost
    + expected delay/disruption cost
```

For courier transport, direct transport cost includes the reward. Collateral financing cost is the opportunity cost of the ISK locked while the contract is active. Expected uncovered cargo loss should reflect the contract's collateral and the probability of failure. For self-hauling, include the expected cargo and ship losses separately.

The risk-adjusted cost is an expected-value model. It does not remove tail risk: a low-probability loss can still be financially catastrophic if the exposed assets are large relative to available capital.

## Operational controls

1. Keep a location and replacement-value inventory of critical blueprints, materials, components, and finished goods.
2. Stage only the inventory required for near-term jobs at a vulnerable facility.
3. Check structure power state, service-module state, docking/access permissions, and destination Delivery Hanger before dispatch.
4. Use collateral appropriate to the replacement value of courier packages.
5. Confirm route, volume, delivery window, and destination before accepting or issuing a contract.
6. Avoid placing irreplaceable or high-value assets in wormhole/Pochven Upwell structures under the assumption that standard Asset Safety will protect them.
7. Include the cost of moving materials to a low-SCI system when comparing it with a closer, higher-SCI facility.
8. Record actual loss, delay, and courier costs to improve future estimates.

## Boundaries and unresolved details

This document defines the risk model and major asset-safety/courier mechanics. It does not prescribe ship fits, exact safe cargo values, route-specific loss probabilities, insurance values, or a universal hauling cost per cubic meter. Those depend on the selected route, ship, fit, cargo, and current environment.

Open work:
- Build a configurable hauling cost model by ship class, cargo volume, route length, and pilot time.
- Add route risk observations from zKillboard or other reliable current sources, without treating kill counts as direct loss probabilities.
- Add a courier contract quote comparison with collateral coverage and destination structure checks.
- Model structure interruption and inventory concentration for a selected industrial staging plan.
- Confirm any changes to asset-safety timing or structure-state rules from future CCP patches.

## Related concepts

- [Market Location Economics](market-location-economics.md)
- [Capital and Asset Management](capital-and-asset-management.md)
- [Facilities and Rigs](../01-foundations/facilities-and-rigs.md)
- [Industrial Cost Accounting](cost-accounting.md)
- [Manufacturing Profitability](manufacturing-profitability.md)

[^ccp-courier-contracts]: CCP Support, Courier Contracts (updated 2021-08-23).
[^ccp-asset-safety]: CCP Support, Asset Safety (updated 2026-03-02).
[^ccp-upwell-quick-facts]: CCP Support, Upwell Structures Quick Facts (accessed 2026-11-14).
[^ccp-structure-deployment]: CCP Support, Upwell Structure Deployment and Unanchoring (accessed 2026-11-14).
[^eveuni-hauling]: EVE University Wiki, Hauling (accessed 2026-11-14).
[^eveuni-asset-safety]: EVE University Wiki, Asset Safety (accessed 2026-11-14).
