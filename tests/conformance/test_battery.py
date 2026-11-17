"""
Cross-Platform Conformance Test: Battery Contract
"""

import unittest
from tests.conformance import ALL_PROVIDERS
from star_sdk.mobile.device_apis import DeviceProviderRegistry, BatteryAPI
from star_runtime.mobile.capabilities import get_active_capabilities, MobileCapability, CapabilitySecurityError


class TestBatteryConformance(unittest.TestCase):
    def test_battery_contract_across_all_providers(self):
        for name, provider_cls in ALL_PROVIDERS:
            with self.subTest(provider=name):
                provider = provider_cls()
                DeviceProviderRegistry.set_provider(provider)

                level = BatteryAPI.level()
                self.assertIsInstance(level, float)
                self.assertTrue(0.0 <= level <= 1.0)

                charging = BatteryAPI.is_charging()
                self.assertIsInstance(charging, bool)

    def test_battery_capability_security_enforcement(self):
        caps = get_active_capabilities()
        caps.revoke(MobileCapability.BATTERY)

        with self.assertRaises(CapabilitySecurityError):
            BatteryAPI.level()

        with self.assertRaises(CapabilitySecurityError):
            BatteryAPI.is_charging()

        caps.grant(MobileCapability.BATTERY)


if __name__ == "__main__":
    unittest.main()
