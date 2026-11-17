"""
Unit Tests for Star Cross-Platform Path Manager
"""

import unittest
from star_distribution.path_manager import PathManager


class TestPathManager(unittest.TestCase):
    def test_get_bin_dir(self):
        bin_dir = PathManager.get_bin_dir("/custom/star")
        self.assertTrue(bin_dir.endswith("bin"))

    def test_configure_path_structure(self):
        res = PathManager.configure_path("/custom/star")
        self.assertIn("bin_dir", res)
        self.assertIn("status", res)


if __name__ == "__main__":
    unittest.main()
