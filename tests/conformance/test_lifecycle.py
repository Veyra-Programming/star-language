"""
Cross-Platform Conformance Test: Lifecycle State Machine Contract
"""

import unittest
from star_sdk.mobile.lifecycle import MobileLifecycle, LifecycleState
from star_backend.mobile.lifecycle_bridge import MobileLifecycleBridge


class TestLifecycleConformance(unittest.TestCase):
    def test_lifecycle_transitions(self):
        lifecycle = MobileLifecycle()
        bridge = MobileLifecycleBridge(lifecycle)

        self.assertEqual(lifecycle.state, LifecycleState.MOUNTED)

        bridge.on_native_resume()
        self.assertEqual(lifecycle.state, LifecycleState.RESUMED)

        bridge.on_native_pause()
        self.assertEqual(lifecycle.state, LifecycleState.PAUSED)

        bridge.on_native_destroy()
        self.assertEqual(lifecycle.state, LifecycleState.DETACHED)


if __name__ == "__main__":
    unittest.main()
