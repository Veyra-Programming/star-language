"""
Cross-Platform Conformance Test: Gestures Contract
"""

import unittest
from star_backend.mobile.event_bridge import MobileEventBridge


class TestGesturesConformance(unittest.TestCase):
    def test_tap_recognition(self):
        bridge = MobileEventBridge()
        bridge.handle_native_touch("down", pointer_id=1, x=100.0, y=100.0)
        gestures = bridge.handle_native_touch("up", pointer_id=1, x=101.0, y=101.0)
        self.assertTrue(any(g.name == "Tap" for g in gestures))

    def test_swipe_recognition(self):
        bridge = MobileEventBridge()
        bridge.handle_native_touch("down", pointer_id=1, x=100.0, y=100.0)
        gestures = bridge.handle_native_touch("up", pointer_id=1, x=350.0, y=100.0)
        self.assertTrue(any(g.name == "Swipe" for g in gestures))


if __name__ == "__main__":
    unittest.main()
