import unittest

from mcp_server_saxo_openapi.server import (
    get_openapi_spec,
    get_pitfalls,
    get_saxo_endpoint_spec,
    search_saxo_endpoints,
)
from mcp_server_saxo_openapi.spec_loader import normalize_path, resolve_openapi_json_path


class TestSpecLoader(unittest.TestCase):
    def test_bundled_json_resolves(self) -> None:
        path = resolve_openapi_json_path()
        self.assertIsNotNone(path)
        assert path is not None
        self.assertTrue(path.is_file())

    def test_normalize_path_strips_openapi_prefix(self) -> None:
        self.assertEqual(normalize_path("/openapi/trade/v2/orders"), "/trade/v2/orders")
        self.assertEqual(normalize_path("trade/v2/orders"), "/trade/v2/orders")


class TestTools(unittest.TestCase):
    def test_search_orders(self) -> None:
        result = search_saxo_endpoints("orders")
        self.assertIn("POST /trade/v2/orders", result)

    def test_get_endpoint_spec_includes_response_and_warning(self) -> None:
        result = get_saxo_endpoint_spec("POST", "/trade/v2/orders")
        self.assertIn("## Responses", result)
        self.assertIn("CRITICAL WARNING", result)
        self.assertIn("pitfalls.md", result)

    def test_get_endpoint_spec_accepts_openapi_prefix(self) -> None:
        result = get_saxo_endpoint_spec("POST", "/openapi/trade/v2/orders")
        self.assertNotIn("Error:", result)
        self.assertIn("/trade/v2/orders", result)

    def test_pitfalls_not_empty(self) -> None:
        pitfalls = get_pitfalls()
        self.assertIn("Netting", pitfalls)
        self.assertIn("Precheck", pitfalls)

    def test_openapi_spec_loads(self) -> None:
        spec = get_openapi_spec()
        self.assertIn("paths", spec)
        self.assertIn("/trade/v2/orders", spec["paths"])


if __name__ == "__main__":
    unittest.main()
