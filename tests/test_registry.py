"""
Unit Tests for Star 1.0 Package Registry Subsystem
"""

import unittest
from star_runtime.registry import PackageRegistry


class TestPackageRegistry(unittest.TestCase):
    def test_search_catalog(self):
        results = PackageRegistry.search("http")
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "http")

    def test_search_by_category(self):
        results = PackageRegistry.search("", category="database")
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "sqlite")

    def test_ui_packages_expansion(self):
        ui_pkgs = PackageRegistry.search("", category="ui")
        self.assertGreaterEqual(len(ui_pkgs), 300)
        # Verify picker, chart, and table domains exist
        picker_res = PackageRegistry.search("picker")
        self.assertGreaterEqual(len(picker_res), 5)
        chart_res = PackageRegistry.search("chart")
        self.assertGreaterEqual(len(chart_res), 15)

    def test_ecosystem_catalog_integrity(self):
        for pkg in PackageRegistry.ECOSYSTEM_CATALOG:
            self.assertIn("name", pkg)
            self.assertIn("version", pkg)
            self.assertIn("category", pkg)
            self.assertIn("description", pkg)


if __name__ == "__main__":
    unittest.main()
