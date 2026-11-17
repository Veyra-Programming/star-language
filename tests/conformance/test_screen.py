"""
Cross-Platform Conformance Test: Screen Metrics Contract
"""

import unittest
from tests.conformance import ALL_PROVIDERS
from star_sdk.mobile.device_apis import DeviceProviderRegistry, ScreenAPI


class TestScreenConformance(unittest.TestCase):
    def test_screen_metrics_contract_across_all_providers(self):
        for name, provider_cls in ALL_PROVIDERS:
            with self.subTest(provider=name):
                provider = provider_cls()
                DeviceProviderRegistry.set_provider(provider)

                width = ScreenAPI.width_dp()
                height = ScreenAPI.height_dp()
                scale = ScreenAPI.scale_factor()
                orient = ScreenAPI.orientation()

                self.assertGreater(width, 0.0)
                self.assertGreater(height, 0.0)
                self.assertGreater(scale, 0.0)
                self.assertIn(orient, ["portrait", "landscape"])


if __name__ == "__main__":
    unittest.main()
