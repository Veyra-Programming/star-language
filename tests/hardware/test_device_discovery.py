"""
Hardware Test: Device Discovery Subsystem
"""

import unittest
from star_backend.mobile.hardware.discovery import DeviceDiscoveryManager
from star_backend.mobile.hardware.device import DevicePlatform


class TestDeviceDiscovery(unittest.TestCase):
    def test_discovery_fallback_simulated_baselines(self):
        devices = DeviceDiscoveryManager.discover_all(include_simulated=True)
        self.assertGreaterEqual(len(devices), 2)
        platforms = [d.platform for d in devices]
        self.assertIn(DevicePlatform.ANDROID, platforms)
        self.assertIn(DevicePlatform.IOS, platforms)


if __name__ == "__main__":
    unittest.main()
