"""Unit tests for the hauling cost scenario calculator."""

import copy
import json
import unittest
from decimal import Decimal
from pathlib import Path

from hauling_cost import calculate


EXAMPLE = Path(__file__).with_name("hauling-cost.example.json")


class HaulingCostTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_example_scenario_totals(self):
        result = calculate(self.config)
        self.assertEqual(result["self_haul"]["trips"], 1)
        self.assertEqual(result["self_haul"]["expected_total_cost_isk"], "24667123.29")
        self.assertEqual(result["courier"]["expected_total_cost_isk"], "14647945.21")
        self.assertEqual(result["comparison"]["lower_expected_cost"], "courier")

    def test_multiple_self_haul_trips_increase_ship_exposure(self):
        config = copy.deepcopy(self.config)
        config["self_haul"]["capacity_m3"] = "5000"
        result = calculate(config)
        self.assertEqual(result["self_haul"]["trips"], 4)
        self.assertEqual(
            result["self_haul"]["probability_at_least_one_trip_loss"],
            str((Decimal("1") - (Decimal("1") - Decimal("0.015")) ** 4).normalize()),
        )

    def test_full_collateral_removes_uncovered_cargo_loss(self):
        config = copy.deepcopy(self.config)
        config["courier"]["collateral_isk_per_contract"] = "1000000000"
        result = calculate(config)
        self.assertEqual(
            result["courier"]["expected_uncovered_cargo_loss_isk"], "0.00"
        )

    def test_invalid_loss_probability_is_rejected(self):
        config = copy.deepcopy(self.config)
        config["self_haul"]["loss_probability_per_trip"] = "1.01"
        with self.assertRaises(ValueError):
            calculate(config)

    def test_insurance_cannot_exceed_ship_replacement_cost(self):
        config = copy.deepcopy(self.config)
        config["self_haul"]["insurance_payout_isk"] = "200000000"
        with self.assertRaises(ValueError):
            calculate(config)


if __name__ == "__main__":
    unittest.main()
