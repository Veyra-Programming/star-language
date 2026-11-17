"""
Unit Tests for Star Mobile Capability & Permission Security Subsystem
"""

import unittest
from star_runtime.mobile.capabilities import CapabilityManager, MobileCapability, CapabilitySecurityError
from star_backend.mobile.device_bridge import MobileDeviceBridge


class TestMobileCapabilities(unittest.TestCase):
    def test_permission_granted(self):
        manager = CapabilityManager([MobileCapability.VIBRATE, MobileCapability.STORAGE])
        self.assertTrue(manager.has_capability(MobileCapability.VIBRATE))
        self.assertTrue(manager.has_capability(MobileCapability.STORAGE))
        self.assertFalse(manager.has_capability(MobileCapability.CAMERA))

        # Accessing storage should succeed
        bridge = MobileDeviceBridge(manager)
        bridge.storage_set("user", "Alex")
        self.assertEqual(bridge.storage_get("user"), "Alex")

    def test_permission_denied_raises_security_error(self):
        # Only vibrate granted, storage not granted
        manager = CapabilityManager([MobileCapability.VIBRATE])
        bridge = MobileDeviceBridge(manager)

        with self.assertRaises(CapabilitySecurityError) as ctx:
            bridge.storage_get("user")
        self.assertEqual(ctx.exception.capability, MobileCapability.STORAGE)

    def test_runtime_capability_grant_and_revoke(self):
        manager = CapabilityManager([])
        self.assertFalse(manager.has_capability(MobileCapability.BATTERY))

        manager.grant(MobileCapability.BATTERY)
        self.assertTrue(manager.has_capability(MobileCapability.BATTERY))

        bridge = MobileDeviceBridge(manager)
        info = bridge.get_battery_info()
        self.assertIn("level", info)

        manager.revoke(MobileCapability.BATTERY)
        self.assertFalse(manager.has_capability(MobileCapability.BATTERY))


if __name__ == "__main__":
    unittest.main()
