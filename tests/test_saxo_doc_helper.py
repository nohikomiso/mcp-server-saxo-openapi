#!/usr/bin/env python3
"""Unit tests for saxo_doc_helper (Normalizer, Did-you-mean, depth collapse)."""

from __future__ import annotations

import json
import os
import tempfile
import unittest

import saxo_doc_helper as helper
from saxo_doc_helper.index import SaxoDocIndex, resolve_spec_dir


SAMPLE_SPEC = {
    "service": "trade",
    "category": "orders",
    "endpoints": [
        {
            "name": "Place a new order",
            "method": "POST",
            "path": "/trade/v2/orders",
            "url": "https://example.test/orders",
            "parameters": [
                {
                    "name": "AccountKey",
                    "type": "AccountKey",
                    "origin": "Body",
                    "description": "Account key.",
                    "children": [],
                },
                {
                    "name": "AlgoOrderData",
                    "type": "AlgorithmicOrderData",
                    "origin": "Body",
                    "description": "Algo order spec.",
                    "link": "/schema-algorithmicorderdata",
                    "children": [
                        {
                            "name": "StrategyName",
                            "type": "String",
                            "origin": "Sub",
                            "description": "Strategy id.",
                            "children": [],
                        }
                    ],
                },
            ],
            "request_sample": {"AccountKey": "abc", "Amount": 1},
            "response_sample": {"OrderId": "123"},
        },
        {
            "name": "Get balances",
            "method": "GET",
            "path": "/port/v1/balances",
            "url": "https://example.test/balances",
            "parameters": [],
            "request_sample": None,
            "response_sample": {"CashBalance": 0},
        },
    ],
}


class NormalizerTests(unittest.TestCase):
    def test_normalize_method(self) -> None:
        self.assertEqual(helper.normalize_method("post"), "POST")
        self.assertEqual(helper.normalize_method("  get "), "GET")

    def test_normalize_path(self) -> None:
        self.assertEqual(helper.normalize_path("trade/v2/orders"), "/trade/v2/orders")
        self.assertEqual(helper.normalize_path("/trade/v2/orders/"), "/trade/v2/orders")
        self.assertEqual(
            helper.normalize_path(
                "https://gateway.saxobank.com/sim/openapi/trade/v2/orders"
            ),
            "/trade/v2/orders",
        )

    def test_normalize_schema_name(self) -> None:
        self.assertEqual(
            helper.normalize_schema_name("AlgorithmicOrderData"), "algorithmicorderdata"
        )


class SaxoDocHelperCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        spec_dir = os.path.join(self.tmp.name, "json", "trade")
        os.makedirs(spec_dir)
        with open(os.path.join(spec_dir, "orders.json"), "w", encoding="utf-8") as f:
            json.dump(SAMPLE_SPEC, f)
        self.index = SaxoDocIndex(os.path.join(self.tmp.name, "json"))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_search_endpoints(self) -> None:
        out = helper.cmd_search_endpoints(self.index, "orders")
        self.assertIn("POST /trade/v2/orders", out)
        self.assertIn("Place a new order", out)

    def test_get_endpoint_exact(self) -> None:
        out = helper.cmd_get_endpoint(self.index, "post", "trade/v2/orders")
        self.assertIn("Name: Place a new order", out)
        self.assertIn("AccountKey", out)
        self.assertIn("Request Sample:", out)
        self.assertIn('"OrderId": "123"', out)

    def test_get_endpoint_depth_collapse(self) -> None:
        out = helper.cmd_get_endpoint(self.index, "POST", "/trade/v2/orders", depth=0)
        self.assertIn("Nested parameters collapsed.", out)
        self.assertIn("[Refer to Schema: algorithmicorderdata]", out)

    def test_get_endpoint_depth_expand(self) -> None:
        out = helper.cmd_get_endpoint(self.index, "POST", "/trade/v2/orders", depth=1)
        self.assertIn("StrategyName", out)

    def test_get_endpoint_did_you_mean(self) -> None:
        out = helper.cmd_get_endpoint(self.index, "POST", "/trade/v2/order")
        self.assertIn("not found", out)
        self.assertIn("Did you mean", out)
        self.assertIn("POST /trade/v2/orders", out)

    def test_get_schema(self) -> None:
        out = helper.cmd_get_schema(self.index, "algorithmicorderdata")
        self.assertIn("Schema: AlgorithmicOrderData", out)
        self.assertIn("StrategyName", out)

    def test_get_schema_not_found(self) -> None:
        out = helper.cmd_get_schema(self.index, "nonexistent_schema_xyz")
        self.assertIn("not found", out)


class PackagedSpecSmokeTests(unittest.TestCase):
    def test_resolve_spec_dir_loads_endpoints(self) -> None:
        spec_dir = resolve_spec_dir()
        self.assertTrue(os.path.isdir(spec_dir), f"spec dir missing: {spec_dir}")
        index = SaxoDocIndex(spec_dir)
        self.assertGreater(len(index.endpoints), 0)
        out = helper.cmd_search_endpoints(index, "orders")
        self.assertIn("endpoint", out.lower())


if __name__ == "__main__":
    unittest.main()
