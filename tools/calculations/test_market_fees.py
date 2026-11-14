"""Unit tests for market fee and sales tax calculations."""

import copy
import json
import unittest
from pathlib import Path

from market_fees import calculate


EXAMPLE = Path(__file__).with_name("market-fees.example.json")


class MarketFeeTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_npc_station_example(self):
        result = calculate(self.config)
        self.assertEqual(result["rates"]["sales_tax_rate"], "0.03375")
        self.assertEqual(result["rates"]["broker_fee_rate"], "0.01055")
        self.assertEqual(result["fees"]["order_creation_broker_fee_isk"], "1055000.00")
        self.assertEqual(result["fees"]["relist_fee_isk"], "263750.00")
        self.assertEqual(result["fees"]["sales_tax_on_sale_value_isk"], "4050000.00")

    def test_maximum_standings_reach_one_percent_floor(self):
        config = copy.deepcopy(self.config)
        config["character"]["unmodified_faction_standing"] = "10"
        config["character"]["unmodified_corporation_standing"] = "10"
        result = calculate(config)
        self.assertEqual(result["rates"]["broker_fee_rate"], "0.01")

    def test_upwell_uses_owner_rate_plus_scc_component(self):
        config = copy.deepcopy(self.config)
        config["market"] = {"type": "upwell_structure", "owner_broker_rate": "0.02"}
        result = calculate(config)
        self.assertEqual(result["rates"]["broker_fee_rate"], "0.025")
        self.assertEqual(result["fees"]["order_creation_broker_fee_isk"], "2500000.00")

    def test_immediate_fill_has_no_order_creation_or_relist_fee(self):
        config = copy.deepcopy(self.config)
        config["order"]["create_non_immediate_order"] = False
        config["order"]["reprice_existing_order"] = False
        result = calculate(config)
        self.assertEqual(result["fees"]["order_creation_broker_fee_isk"], "0.00")
        self.assertEqual(result["fees"]["relist_fee_isk"], "0.00")
        self.assertEqual(result["fees"]["sales_tax_on_sale_value_isk"], "4050000.00")

    def test_invalid_skill_level_is_rejected(self):
        config = copy.deepcopy(self.config)
        config["character"]["accounting_level"] = 6
        with self.assertRaises(ValueError):
            calculate(config)

    def test_invalid_market_type_is_rejected(self):
        config = copy.deepcopy(self.config)
        config["market"]["type"] = "other"
        with self.assertRaises(ValueError):
            calculate(config)


if __name__ == "__main__":
    unittest.main()
