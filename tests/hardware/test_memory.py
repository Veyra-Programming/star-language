"""
Hardware Test: Low Memory Warning Event Forwarding
"""

import unittest
from star_sdk.mobile.lifecycle import MobileLifecycle
from star_backend.mobile.lifecycle_bridge import MobileLifecycleBridge


class TestMemoryHardware(unittest.TestCase):
    def test_memory_warning_delivery(self):
        lc = MobileLifecycle()
        bridge = MobileLifecycleBridge(lc)

        warned = [False]
        lc.on_memory_warning(lambda: warned.__setitem__(0, True))

        bridge.on_native_memory_warning()
        self.assertTrue(warned[0])


if __name__ == "__main__":
    unittest.main()
