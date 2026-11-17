"""
Unit Tests for Star Software License Agreement, EULA and CLI
"""

import unittest
import os
import subprocess
import sys


class TestStarLicense(unittest.TestCase):
    def setUp(self):
        self.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def test_license_files_exist(self):
        eula_path = os.path.join(self.repo_root, "EULA.md")
        sla_path = os.path.join(self.repo_root, "STAR_LICENSE_AGREEMENT.md")
        mit_path = os.path.join(self.repo_root, "LICENSE")

        self.assertTrue(os.path.exists(eula_path), "EULA.md should exist")
        self.assertTrue(os.path.exists(sla_path), "STAR_LICENSE_AGREEMENT.md should exist")
        self.assertTrue(os.path.exists(mit_path), "LICENSE should exist")

    def test_sla_contents(self):
        sla_path = os.path.join(self.repo_root, "STAR_LICENSE_AGREEMENT.md")
        with open(sla_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("DUAL LICENSE MODEL", content)
        self.assertIn("MIT License", content)
        self.assertIn("Commercial Deployment", content)
        self.assertIn("Microsoft Visual Studio", content)
        self.assertIn("Android SDK", content)
        self.assertIn("DISCLAIMER OF WARRANTY", content)

    def test_cli_license_status(self):
        cli_py = os.path.join(self.repo_root, "star.py")
        res = subprocess.run([sys.executable, cli_py, "license", "--status"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Star License Status:", res.stdout)


if __name__ == "__main__":
    unittest.main()
