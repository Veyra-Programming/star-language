"""
Cross-Platform Conformance Test: Orientation Contract
"""

import unittest
from tests.conformance import ALL_PROVIDERS
from star_sdk.mobile.device_apis import DeviceProviderRegistry, OrientationAPI


class TestOrientationConformance(unittest.TestCase):
    def test_orientation_contract_across_all_providers(self):
        for name, provider_cls in ALL_PROVIDERS:
            with self.subTest(provider=name):
                provider = provider_cls()
                DeviceProviderRegistry.set_provider(provider)

                current = OrientationAPI.current()
                self.assertIn(current, ["portrait", "landscape", "landscape_left", "landscape_right", "portrait_upside_down"])

                OrientationAPI.lock("landscape")
                self.assertEqual(OrientationAPI.current(), "landscape")

                OrientationAPI.unlock()
                self.assertIsNotNone(OrientationAPI.current())


if __name__ == "__main__":
    unittest.main()
