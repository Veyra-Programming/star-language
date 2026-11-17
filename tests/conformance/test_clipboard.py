"""
Cross-Platform Conformance Test: Clipboard Contract
"""

import unittest
from tests.conformance import ALL_PROVIDERS
from star_sdk.mobile.device_apis import DeviceProviderRegistry, ClipboardAPI
from star_runtime.mobile.capabilities import get_active_capabilities, MobileCapability, CapabilitySecurityError


class TestClipboardConformance(unittest.TestCase):
    def test_clipboard_contract_across_all_providers(self):
        for name, provider_cls in ALL_PROVIDERS:
            with self.subTest(provider=name):
                provider = provider_cls()
                DeviceProviderRegistry.set_provider(provider)

                ClipboardAPI.set("Star Universal Text")
                self.assertEqual(ClipboardAPI.get(), "Star Universal Text")

    def test_clipboard_capability_security_enforcement(self):
        caps = get_active_capabilities()
        caps.revoke(MobileCapability.CLIPBOARD)

        with self.assertRaises(CapabilitySecurityError):
            ClipboardAPI.set("Secret")

        with self.assertRaises(CapabilitySecurityError):
            ClipboardAPI.get()

        caps.grant(MobileCapability.CLIPBOARD)


if __name__ == "__main__":
    unittest.main()
