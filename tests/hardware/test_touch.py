"""
Hardware Test: Touch & Gesture Recognition Subsystem
"""

import unittest
from star_backend.mobile.event_bridge import MobileEventBridge


class TestTouchHardware(unittest.TestCase):
    def test_touch_tap_recognition(self):
        bridge = MobileEventBridge()
        bridge.handle_native_touch("down", 1, 150.0, 200.0)
        gestures = bridge.handle_native_touch("up", 1, 151.0, 201.0)
        self.assertTrue(any(g.name == "Tap" for g in gestures))

    def test_touch_swipe_recognition(self):
        bridge = MobileEventBridge()
        bridge.handle_native_touch("down", 1, 100.0, 100.0)
        gestures = bridge.handle_native_touch("up", 1, 350.0, 100.0)
        self.assertTrue(any(g.name == "Swipe" for g in gestures))


if __name__ == "__main__":
    unittest.main()
