"""
Unit Tests for Microsoft Visual Studio & Windows Toolchain Discovery
"""

import unittest
from star_backend.desktop.visual_studio import VisualStudioToolchain


class TestVisualStudioToolchain(unittest.TestCase):
    def test_find_toolchain_discovery(self):
        toolchain = VisualStudioToolchain.find_toolchain()
        self.assertIsNotNone(toolchain)
        self.assertIsInstance(toolchain, VisualStudioToolchain)

    def test_toolchain_info_structure(self):
        toolchain = VisualStudioToolchain.find_toolchain()
        info = toolchain.get_toolchain_info()
        self.assertIn("is_installed", info)
        self.assertIn("vs_version", info)
        self.assertIn("model", info)
        self.assertIn("Visual Studio Optional", info["model"])


if __name__ == "__main__":
    unittest.main()
