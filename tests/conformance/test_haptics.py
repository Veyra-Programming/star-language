"""
Cross-Platform Conformance Test: Haptics & Vibration Contract
"""

import unittest
from tests.conformance import ALL_PROVIDERS
from star_sdk.mobile.device_apis import DeviceProviderRegistry, HapticsAPI
from star_runtime.mobile.capabilities import get_active_capabilities, MobileCapability, CapabilitySecurityError


class TestHapticsConformance(unittest.TestCase):
    def test_haptics_contract_across_all_providers(self):
        for name, provider_cls in ALL_PROVIDERS:
            with self.subTest(provider=name):
                provider = provider_cls()
                DeviceProviderRegistry.set_provider(provider)

                HapticsAPI.impact("light")
                HapticsAPI.impact("medium")
                HapticsAPI.impact("heavy")
                HapticsAPI.notification("success")
                HapticsAPI.notification("warning")
                HapticsAPI.notification("error")

                self.assertGreaterEqual(len(provider._haptics_log), 6)

    def test_haptics_capability_security_enforcement(self):
        caps = get_active_capabilities()
        caps.revoke(MobileCapability.VIBRATE)

        with self.assertRaises(CapabilitySecurityError):
            HapticsAPI.impact("medium")

        with self.assertRaises(CapabilitySecurityError):
            HapticsAPI.notification("success")

        caps.grant(MobileCapability.VIBRATE)


if __name__ == "__main__":
    unittest.main()
