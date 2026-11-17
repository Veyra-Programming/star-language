"""
Unit Tests for Star Production Manifest Subsystem
"""

import unittest
from star_distribution.manifest import DistributionManifest


class TestDistributionManifest(unittest.TestCase):
    def test_manifest_serialization(self):
        m = DistributionManifest(
            name="Star-SDK",
            version="1.0.1",
            target_platform="windows-x64",
            core_abi=1,
            mobile_abi=1,
            binaries=["bin/star.exe", "bin/starc.exe"],
            file_checksums={"bin/star.exe": "abc123hash"}
        )
        json_str = m.to_json()
        self.assertIn("windows-x64", json_str)
        self.assertIn("1.0.1", json_str)

        loaded = DistributionManifest.from_json(json_str)
        self.assertEqual(loaded.version, "1.0.1")
        self.assertEqual(loaded.core_abi, 1)
        self.assertEqual(loaded.binaries, ["bin/star.exe", "bin/starc.exe"])


if __name__ == "__main__":
    unittest.main()
