"""
Hardware Test: Mobile Host Lifecycle
"""

import unittest
from star_sdk.mobile.lifecycle import MobileLifecycle, LifecycleState
from star_backend.mobile.lifecycle_bridge import MobileLifecycleBridge


class TestLifecycleHardware(unittest.TestCase):
    def test_lifecycle_host_transitions(self):
        lc = MobileLifecycle()
        bridge = MobileLifecycleBridge(lc)

        bridge.on_native_resume()
        self.assertEqual(lc.state, LifecycleState.RESUMED)

        bridge.on_native_pause()
        self.assertEqual(lc.state, LifecycleState.PAUSED)

        bridge.on_native_destroy()
        self.assertEqual(lc.state, LifecycleState.DETACHED)


if __name__ == "__main__":
    unittest.main()
