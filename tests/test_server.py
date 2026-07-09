import unittest

from mcp_server_saxo_openapi.commands import cmd_get_schema, cmd_get_workflow_guide
from mcp_server_saxo_openapi.index import SaxoDocIndex, resolve_spec_dir
from mcp_server_saxo_openapi.pitfalls import PITFALLS_MD
from mcp_server_saxo_openapi.server import (
    get_pitfalls,
    get_saxo_endpoint_spec,
    get_saxo_schema_spec,
    get_saxo_workflow_guide,
    search_saxo_endpoints,
)


class TestIndex(unittest.TestCase):
    def test_bundled_spec_dir_resolves(self) -> None:
        spec_dir = resolve_spec_dir()
        self.assertTrue(spec_dir.endswith("data/json") or spec_dir.endswith("spec/json"))

    def test_index_loads_endpoints(self) -> None:
        index = SaxoDocIndex()
        self.assertGreater(len(index.endpoints), 0)
        self.assertGreater(len(index.schemas), 0)


class TestTools(unittest.TestCase):
    def test_search_orders(self) -> None:
        result = search_saxo_endpoints("orders")
        self.assertIn("POST /trade/v2/orders", result)

    def test_get_endpoint_spec_samples_and_warning(self) -> None:
        result = get_saxo_endpoint_spec("POST", "/trade/v2/orders")
        self.assertIn("CRITICAL WARNING", result)
        self.assertIn("pitfalls.md", result)
        self.assertIn("Request Sample", result)
        self.assertIn("Response Sample", result)

    def test_get_endpoint_spec_openapi_prefix(self) -> None:
        result = get_saxo_endpoint_spec("POST", "/openapi/trade/v2/orders")
        self.assertNotIn("Error:", result)

    def test_get_schema_spec(self) -> None:
        index = SaxoDocIndex()
        sample_key = next(iter(index.schemas))
        result = get_saxo_schema_spec(sample_key)
        self.assertIn("Schema:", result)

    def test_workflow_guide_close_position(self) -> None:
        result = get_saxo_workflow_guide("close_position")
        self.assertIn("Netting", result)

    def test_pitfalls_resource(self) -> None:
        self.assertEqual(get_pitfalls(), PITFALLS_MD)
        self.assertIn("Precheck", get_pitfalls())


if __name__ == "__main__":
    unittest.main()
