"""
Cross-Platform Conformance Test: Storage Contract
"""

import unittest
from tests.conformance import ALL_PROVIDERS
from star_sdk.mobile.device_apis import DeviceProviderRegistry, StorageAPI
from star_runtime.mobile.capabilities import get_active_capabilities, MobileCapability, CapabilitySecurityError


class TestStorageConformance(unittest.TestCase):
    def test_storage_contract_across_all_providers(self):
        for name, provider_cls in ALL_PROVIDERS:
            with self.subTest(provider=name):
                provider = provider_cls()
                DeviceProviderRegistry.set_provider(provider)

                # 1. Normal set/get/remove
                StorageAPI.set("auth_token", "sec_token_999")
                self.assertEqual(StorageAPI.get("auth_token"), "sec_token_999")

                StorageAPI.set("auth_token", "updated_token_111")
                self.assertEqual(StorageAPI.get("auth_token"), "updated_token_111")

                StorageAPI.remove("auth_token")
                self.assertIsNone(StorageAPI.get("auth_token"))

    def test_storage_capability_security_enforcement(self):
        caps = get_active_capabilities()
        caps.revoke(MobileCapability.STORAGE)

        with self.assertRaises(CapabilitySecurityError):
            StorageAPI.set("key", "val")

        with self.assertRaises(CapabilitySecurityError):
            StorageAPI.get("key")

        with self.assertRaises(CapabilitySecurityError):
            StorageAPI.remove("key")

        caps.grant(MobileCapability.STORAGE)


if __name__ == "__main__":
    unittest.main()
