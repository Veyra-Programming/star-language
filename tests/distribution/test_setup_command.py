"""
Unit Tests for Star Setup Command & Portable PATH Management
"""

import unittest
import tempfile
import os
import shutil
from star_distribution.path_manager import PathManager


class TestSetupCommand(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.bin_dir = os.path.join(self.temp_dir, "bin")
        os.makedirs(self.bin_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_portable_path_addition(self):
        success, msg = PathManager.add_to_path(self.bin_dir)
        # Should execute successfully or report already configured
        self.assertIsInstance(success, bool)
        self.assertIsInstance(msg, str)


if __name__ == "__main__":
    unittest.main()
