# Deterministic calculations

Calculation scripts use only Python's standard library and keep inputs in JSON files so scenarios can be versioned and reproduced.

## Hauling cost comparison

Run from the repository root:

```powershell
py -3 tools/calculations/hauling_cost.py --config tools/calculations/hauling-cost.example.json
```

The calculator compares self-hauling and hiring a courier from the cargo owner's perspective. It reports:
- Required trips/contracts.
- Probability of at least one loss/failure.
- Direct costs and pilot time cost.
- Expected cargo and ship loss.
- Courier reward, contract fees, and expected uncovered cargo loss.
- Capital cost while cargo is in transit.
- Expected total cost, cost per m³, and cost as a percentage of cargo value.

Edit a copy of the example JSON for a real route and shipment. The probabilities are user-supplied scenario assumptions, not predictions. Run low/base/high cases for route risk and contractor failure. Do not use the illustrative values as route statistics.

The calculator assumes equal cargo value per trip/contract. Split a shipment into separate scenarios if high-value cargo is concentrated in one load or if routes and risk differ.

Run the calculator unit tests from the repository root:

```powershell
py -3 -m unittest discover -s tools/calculations -p "test_*.py"
```

## Manufacturing profitability

Run from the repository root:

```powershell
py -3 tools/calculations/manufacturing_profitability.py --config tools/calculations/manufacturing-profitability.example.json
```

The model reports economic material cost, installation/upstream/logistics costs, modeled realized sales, unsold inventory cost basis, full-batch projected contribution, net margin, ROI, slot-hour and elapsed-hour efficiency, active-operator-hour efficiency when supplied, break-even price, target-margin price, and a maximum affordable unit value for one selected input.

Set `production.active_operator_hours` to the total hands-on operator time attributable to the production plan, in hours. Include attributable evaluation, sourcing, staging, installation, hauling, order maintenance, and reconciliation work. Exclude unattended job duration and passive inventory waiting. Do not count one person's simultaneous alt-character tasks as multiple operator-hours. If this input is omitted or zero, the active-operator-hour metric is reported as null rather than inferred.

Inputs are deliberately explicit:
- Material quantities and values are supplied by the user. Each line can record its valuation basis, location, and source timestamp.
- Installation fees should come from the actual Industry quote.
- Sale fills should reflect actual executions or an explicitly labeled order-book estimate.
- Sales tax is a decimal rate (for example, 3.375% is `0.03375`). Broker, relist, and other fees are entered as ISK amounts.
- The full-batch projection is separate from actual/estimated fills and applies the supplied full-batch fee assumptions.

The example values are illustrative and are not current EVE market prices or live fee quotes. The calculator does not retrieve recipes, prices, job quotes, or market depth.

## Continuous integration

The repository runs its full local validation suite through [GitHub Actions](../../.github/workflows/python-tests.yml) when relevant code or documentation changes are pushed or opened as a pull request, and on manual workflow dispatch. The workflow uses Python 3.12 and executes calculation tests, validation-tool tests, and the local Markdown link checker.

Run the same full suite locally from the repository root:

```powershell
py -3 tools/validation/run_all.py
```

## Market fees and sales tax

Run from the repository root:

```powershell
py -3 tools/calculations/market_fees.py --config tools/calculations/market-fees.example.json
```

The calculator estimates Accounting-adjusted sales tax, NPC station broker fees from Broker Relations and unmodified standings, Upwell structure broker fees from the supplied owner rate plus the SCC component, and order relist fees from the supplied order values and Advanced Broker Relations level. It applies a 100 ISK minimum to non-immediate order creation and relisting when the new order value is positive. The minimum is supported by EVE University's current fee reference; confirm the live quote for low-value orders.

Set `create_non_immediate_order` to false for an immediate fill and `reprice_existing_order` to false when no existing order is being repriced. A non-immediate order creation incurs the broker fee; repricing an existing order incurs the relist fee. Sales tax still applies to the seller when units sell. For a mixed immediate fill and listed remainder, use the actual quote and wallet journal.

The Upwell owner rate and order values must be taken from the live order quote. Use wallet records to reconcile actual fees. The sample is illustrative, not a current structure quote.

## General rules

- Keep money inputs as decimal strings in JSON to avoid binary floating-point error.
- Preserve the input file alongside the output used for a decision.
- Record the date, route, ship/fit, cargo, and source of risk estimates.
- Do not commit private character data, tokens, or raw ESI/SDE snapshots.


## Quote-first single-product evaluation (M4)

Run the synthetic demonstration from the repository root:

```powershell
py -3 tools/calculations/product_evaluation.py `
    --config tools/calculations/product-evaluation.example.json `
    --output data/derived/product-evaluation-example.json
```

The example is synthetic and must not be treated as an EVE price, fee, quote, or recommendation. Replace its recipe, product, quote, sourcing values, and sale assumptions for a real evaluation.

For a real candidate, copy the example JSON to an ignored local file and set:

- The exact manufacturing blueprint type ID, output product type ID, run count, and local normalized SDE recipe JSONL path.
- Blueprint type (BPO/BPC), copy count, ME/TE, and licensed runs where relevant.
- Every quoted job's run count and duration, the critical-path duration, output quantity, installation fee, and complete material bill from the in-game Industry window.
- Each input's replacement/opportunity unit value, valuation basis, timestamp, and procurement location.
- Capital deployed and total attributable active operator-hours. Label the latter `measured` or `estimated`; leave it unknown when it cannot be responsibly estimated.
- One or more sale strategies. Use the v4 target-location order-book estimate for immediate liquidation or a clearly labeled sell-order scenario. Supply tax, broker/relist fees, modeled fills, source timestamp/location, and risk notes.

The tool verifies the selected SDE recipe, publication/completeness state, output yield, job-run coverage, and per-job SDE run limit. It reports the raw SDE base-material quantities alongside the actual Industry-quoted bill. It **does not** derive modified material quantities or job fees from an unverified ME/facility formula. The Industry quote is the costing authority for this first iteration.

Each sale strategy reuses the existing deterministic manufacturing profitability calculator. The report separates observed/estimated fills from a full-batch projection, keeps unsold inventory cost basis visible, reports slot-hours and contribution per active operator-hour when supplied, and does not apply a risk premium. Prices and fill assumptions are inputs, not predictions or guaranteed liquidity.

Run its tests with the standard calculation test command above.
