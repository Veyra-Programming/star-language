"""
Unit Tests for Star Mobile Lifecycle Engine & Hooks
"""

import unittest
from star_sdk.mobile.lifecycle import MobileLifecycle, LifecycleState
from star_engine.types import StarBoolean


class TestMobileLifecycle(unittest.TestCase):
    def setUp(self):
        self.lifecycle = MobileLifecycle()

    def test_lifecycle_transitions(self):
        self.assertEqual(self.lifecycle.state, LifecycleState.MOUNTED)

        resumed_called = [False]
        paused_called = [False]

        self.lifecycle.on_resume(lambda: resumed_called.__setitem__(0, True))
        self.lifecycle.on_pause(lambda: paused_called.__setitem__(0, True))

        self.lifecycle.transition_to(LifecycleState.RESUMED)
        self.assertEqual(self.lifecycle.state, LifecycleState.RESUMED)
        self.assertTrue(resumed_called[0])

        self.lifecycle.transition_to(LifecycleState.PAUSED)
        self.assertEqual(self.lifecycle.state, LifecycleState.PAUSED)
        self.assertTrue(paused_called[0])

    def test_back_press_interception(self):
        # Default with no handlers should return False
        self.assertFalse(self.lifecycle.dispatch_back_press())

        # Handler that intercepts back navigation
        self.lifecycle.on_back_press(lambda: True)
        self.assertTrue(self.lifecycle.dispatch_back_press())


if __name__ == "__main__":
    unittest.main()
