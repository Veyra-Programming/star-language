"""
Hardware Test: Multi-Touch & Pointer Tracking
"""

import unittest
from star_backend.mobile.event_bridge import MobileEventBridge


class TestMultiTouchHardware(unittest.TestCase):
    def test_two_pointer_tracking(self):
        bridge = MobileEventBridge()
        bridge.handle_native_touch("down", 1, 100.0, 100.0)
        bridge.handle_native_touch("down", 2, 200.0, 200.0)

        # Move pointers apart (Pinch out)
        bridge.handle_native_touch("move", 1, 80.0, 80.0)
        bridge.handle_native_touch("move", 2, 250.0, 250.0)

        bridge.handle_native_touch("up", 1, 80.0, 80.0)
        bridge.handle_native_touch("up", 2, 250.0, 250.0)


if __name__ == "__main__":
    unittest.main()
