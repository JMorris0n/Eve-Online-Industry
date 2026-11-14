"""Unit tests for public ESI collector helpers without network access."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from collect_public_market_data import (
    ESIClient, endpoint_url, parse_http_date, retry_after_seconds, save_response,
)


class ESICollectorTests(unittest.TestCase):
    def test_endpoint_url_encodes_query_parameters(self):
        url = endpoint_url("/markets/100/orders/", {
            "datasource": "tranquility", "order_type": "all", "type_id": 34,
        })
        self.assertTrue(url.startswith("https://esi.evetech.net/markets/100/orders/?"))
        self.assertIn("type_id=34", url)
        self.assertIn("order_type=all", url)

    def test_public_base_url_uses_unversioned_esi_host(self):
        url = endpoint_url("/industry/systems/")
        self.assertEqual(url, "https://esi.evetech.net/industry/systems/")
        self.assertNotIn("/latest/", url)

    def test_save_response_preserves_requested_and_matched_compatibility_dates(self):
        with tempfile.TemporaryDirectory() as temp:
            info = {
                "url": "https://esi.evetech.net/industry/systems/",
                "status": 200,
                "retrieved_at": "2026-11-14T17:28:08Z",
                "from_cache": False,
                "requested_compatibility_date": "2026-11-13",
                "matched_compatibility_date": "2020-01-01",
                "sha256": "abc123",
                "headers": {"expires": "Sat, 14 Nov 2026 18:25:10 GMT", "etag": "tag"},
            }
            summary = save_response(Path(temp), "sample.json", [], info)
        self.assertEqual(summary["requested_compatibility_date"], "2026-11-13")
        self.assertEqual(summary["matched_compatibility_date"], "2020-01-01")

    def test_parse_http_date_handles_invalid_and_valid_values(self):
        self.assertIsNone(parse_http_date(None))
        self.assertIsNone(parse_http_date("not a date"))
        self.assertEqual(
            parse_http_date("Fri, 14 Nov 2026 10:00:00 GMT").isoformat(),
            "2026-11-14T10:00:00+00:00",
        )

    def test_retry_after_numeric_seconds(self):
        self.assertEqual(retry_after_seconds("12.5"), 12.5)
        self.assertEqual(retry_after_seconds("-1"), 0.0)
        self.assertIsNone(retry_after_seconds("bad"))

    def test_get_pages_uses_x_pages_and_collects_every_page(self):
        with tempfile.TemporaryDirectory() as temp:
            client = ESIClient(Path(temp), "2026-11-13", "test-agent")
            client.get_json = Mock(side_effect=[
                ([{"order": 1}], {"headers": {"x-pages": "3"}}),
                ([{"order": 2}], {"headers": {"x-pages": "3"}}),
                ([{"order": 3}], {"headers": {"x-pages": "3"}}),
            ])
            pages = client.get_pages("https://example.invalid/orders")
        self.assertEqual([page[0][0]["order"] for page in pages], [1, 2, 3])
        self.assertEqual(client.get_json.call_count, 3)
        self.assertTrue(client.get_json.call_args_list[1].args[0].endswith("?page=2"))
        self.assertTrue(client.get_json.call_args_list[2].args[0].endswith("?page=3"))


if __name__ == "__main__":
    unittest.main()
