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

The model reports economic material cost, installation/upstream/logistics costs, modeled realized sales, unsold inventory cost basis, full-batch projected contribution, net margin, ROI, slot-hour and elapsed-hour efficiency, break-even price, target-margin price, and a maximum affordable unit value for one selected input.

Inputs are deliberately explicit:
- Material quantities and values are supplied by the user. Each line can record its valuation basis, location, and source timestamp.
- Installation fees should come from the actual Industry quote.
- Sale fills should reflect actual executions or an explicitly labeled order-book estimate.
- Sales tax is a decimal rate (for example, 3.375% is `0.03375`). Broker, relist, and other fees are entered as ISK amounts.
- The full-batch projection is separate from actual/estimated fills and applies the supplied full-batch fee assumptions.

The example values are illustrative and are not current EVE market prices or live fee quotes. The calculator does not retrieve recipes, prices, job quotes, or market depth.

## Continuous integration

The repository runs the standard-library unit tests through [GitHub Actions](../../.github/workflows/python-tests.yml) on pushes and pull requests that change `tools/calculations/`, and on manual workflow dispatch. The workflow uses Python 3.12.

Run the same suite locally from the repository root:

```powershell
py -3 -m unittest discover -s tools/calculations -p "test_*.py" -v
```

## General rules

- Keep money inputs as decimal strings in JSON to avoid binary floating-point error.
- Preserve the input file alongside the output used for a decision.
- Record the date, route, ship/fit, cargo, and source of risk estimates.
- Do not commit private character data, tokens, or raw ESI/SDE snapshots.
