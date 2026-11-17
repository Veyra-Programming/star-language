"""
Unit Tests for Star Mobile Gesture Recognition Engine
"""

import unittest
import time
from star_backend.mobile.events import TouchPhase, TouchPoint, TouchEvent
from star_backend.mobile.gesture_engine import GestureEngine, RecognizedGesture
from star_sdk.mobile.gestures import GestureType


class TestMobileGestures(unittest.TestCase):
    def setUp(self):
        self.engine = GestureEngine()

    def test_tap_recognition(self):
        t0 = 1000.0
        p1 = TouchPoint(1, 100.0, 150.0, timestamp=t0)
        self.engine.process_touch_event(TouchEvent(TouchPhase.START, [p1]))

        # Release at almost same position within 50ms
        p2 = TouchPoint(1, 102.0, 151.0, timestamp=t0 + 0.05)
        gestures = self.engine.process_touch_event(TouchEvent(TouchPhase.END, [p2]))

        self.assertEqual(len(gestures), 1)
        self.assertEqual(gestures[0].name, GestureType.TAP)
        self.assertAlmostEqual(gestures[0].event.x, 102.0)
        self.assertAlmostEqual(gestures[0].event.y, 151.0)

    def test_double_tap_recognition(self):
        t0 = 2000.0
        # Tap 1
        self.engine.process_touch_event(TouchEvent(TouchPhase.START, [TouchPoint(1, 100.0, 100.0, timestamp=t0)]))
        self.engine.process_touch_event(TouchEvent(TouchPhase.END, [TouchPoint(1, 100.0, 100.0, timestamp=t0 + 0.04)]))

        # Tap 2 within 150ms
        t1 = t0 + 0.15
        self.engine.process_touch_event(TouchEvent(TouchPhase.START, [TouchPoint(1, 102.0, 101.0, timestamp=t1)]))
        gestures = self.engine.process_touch_event(TouchEvent(TouchPhase.END, [TouchPoint(1, 102.0, 101.0, timestamp=t1 + 0.04)]))

        self.assertEqual(len(gestures), 1)
        self.assertEqual(gestures[0].name, GestureType.DOUBLE_TAP)

    def test_long_press_recognition(self):
        t0 = 3000.0
        self.engine.process_touch_event(TouchEvent(TouchPhase.START, [TouchPoint(1, 50.0, 50.0, timestamp=t0)]))
        # Release after 600ms
        gestures = self.engine.process_touch_event(
            TouchEvent(TouchPhase.END, [TouchPoint(1, 52.0, 51.0, timestamp=t0 + 0.6)])
        )

        self.assertEqual(len(gestures), 1)
        self.assertEqual(gestures[0].name, GestureType.LONG_PRESS)
        self.assertGreaterEqual(gestures[0].event.duration_ms, 500)

    def test_swipe_recognition_horizontal(self):
        t0 = 4000.0
        self.engine.process_touch_event(TouchEvent(TouchPhase.START, [TouchPoint(1, 50.0, 200.0, timestamp=t0)]))
        # Quick swipe right (dx = 150dp, dt = 100ms)
        gestures = self.engine.process_touch_event(
            TouchEvent(TouchPhase.END, [TouchPoint(1, 200.0, 205.0, timestamp=t0 + 0.1)])
        )

        self.assertEqual(len(gestures), 1)
        self.assertEqual(gestures[0].name, GestureType.SWIPE)
        self.assertEqual(gestures[0].event.direction, "right")
        self.assertGreater(gestures[0].event.velocity, 0.2)

    def test_pan_recognition(self):
        t0 = 5000.0
        self.engine.process_touch_event(TouchEvent(TouchPhase.START, [TouchPoint(1, 100.0, 100.0, timestamp=t0)]))
        
        # Move
        gestures = self.engine.process_touch_event(
            TouchEvent(TouchPhase.MOVE, [TouchPoint(1, 110.0, 120.0, timestamp=t0 + 0.05)])
        )

        self.assertEqual(len(gestures), 1)
        self.assertEqual(gestures[0].name, GestureType.PAN)
        self.assertAlmostEqual(gestures[0].event.dx, 10.0)
        self.assertAlmostEqual(gestures[0].event.dy, 20.0)

    def test_pinch_recognition(self):
        t0 = 6000.0
        # Two fingers starting 100dp apart
        t1 = TouchPoint(1, 100.0, 200.0, timestamp=t0)
        t2 = TouchPoint(2, 200.0, 200.0, timestamp=t0)
        self.engine.process_touch_event(TouchEvent(TouchPhase.START, [t1, t2]))

        # Two fingers spreading to 200dp apart (2x scale)
        t1_moved = TouchPoint(1, 50.0, 200.0, timestamp=t0 + 0.05)
        t2_moved = TouchPoint(2, 250.0, 200.0, timestamp=t0 + 0.05)
        gestures = self.engine.process_touch_event(TouchEvent(TouchPhase.MOVE, [t1_moved, t2_moved]))

        pinch_gestures = [g for g in gestures if g.name == GestureType.PINCH]
        self.assertTrue(len(pinch_gestures) > 0)
        self.assertAlmostEqual(pinch_gestures[0].event.scale, 2.0)


if __name__ == "__main__":
    unittest.main()
