"""Unit tests for the manufacturing profitability calculator."""

import copy
import json
import unittest
from pathlib import Path

from manufacturing_profitability import calculate


EXAMPLE = Path(__file__).with_name("manufacturing-profitability.example.json")


class ManufacturingProfitabilityTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_example_batch_projection(self):
        result = calculate(self.config)
        projected = result["full_batch_projection"]
        self.assertEqual(result["batch_costs"]["economic_batch_cost_isk"], "810000.00")
        self.assertEqual(projected["gross_sale_value_isk"], "1100000.00")
        self.assertEqual(projected["sales_tax_isk"], "37125.00")
        self.assertEqual(projected["projected_contribution_isk"], "247875.00")
        self.assertEqual(projected["break_even_unit_price_isk"], "843.41")
        self.assertEqual(projected["target_margin_unit_price_isk"], "940.17")
        self.assertEqual(
            projected["maximum_affordable_input"]["maximum_unit_value_isk"],
            "7.48",
        )

    def test_partial_sales_keep_unsold_inventory_cost(self):
        result = calculate(self.config)
        sales = result["realized_sales"]
        self.assertEqual(sales["sold_units"], "700")
        self.assertEqual(sales["unsold_units"], "300")
        self.assertEqual(sales["unsold_inventory_cost_basis_isk"], "243000.00")

    def test_sales_cannot_exceed_output(self):
        config = copy.deepcopy(self.config)
        config["sale"]["fills"][0]["quantity"] = "1001"
        with self.assertRaises(ValueError):
            calculate(config)

    def test_tax_rate_must_be_valid(self):
        config = copy.deepcopy(self.config)
        config["sale"]["sales_tax_rate"] = "1.01"
        with self.assertRaises(ValueError):
            calculate(config)

    def test_negative_material_cost_is_rejected(self):
        config = copy.deepcopy(self.config)
        config["materials"][0]["unit_value_isk"] = "-1"
        with self.assertRaises(ValueError):
            calculate(config)


if __name__ == "__main__":
    unittest.main()
