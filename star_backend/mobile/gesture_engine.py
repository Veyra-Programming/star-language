"""
Star Mobile Gesture Recognition Engine
Authoritative Reference: STAR_MOBILE.md (Section 3)
"""

import math
import time
from typing import List, Dict, Any, Optional, Tuple, Callable
from star_backend.mobile.events import TouchPhase, TouchPoint, TouchEvent
from star_sdk.mobile.gestures import (
    GestureType, TapGesture, DoubleTapGesture, LongPressGesture,
    PanGesture, SwipeGesture, PinchGesture, RotateGesture, BaseGestureEvent
)


class RecognizedGesture:
    def __init__(self, name: str, event: BaseGestureEvent):
        self.name = name
        self.event = event

    def __repr__(self) -> str:
        return f"RecognizedGesture({self.name}, {self.event.raw_payload})"


class GestureEngine:
    """
    Stateful multi-touch gesture recognizer that consumes low-level TouchEvents
    and emits high-level Star mobile gestures.
    """
    def __init__(
        self,
        tap_timeout_ms: float = 250.0,
        double_tap_timeout_ms: float = 300.0,
        long_press_timeout_ms: float = 500.0,
        touch_slop_dp: float = 12.0,
        swipe_min_distance_dp: float = 30.0,
        swipe_min_velocity_dp_ms: float = 0.2
    ):
        self.tap_timeout_ms = tap_timeout_ms
        self.double_tap_timeout_ms = double_tap_timeout_ms
        self.long_press_timeout_ms = long_press_timeout_ms
        self.touch_slop_dp = touch_slop_dp
        self.swipe_min_distance_dp = swipe_min_distance_dp
        self.swipe_min_velocity_dp_ms = swipe_min_velocity_dp_ms

        # Touch tracking state
        self._touch_history: Dict[int, List[TouchPoint]] = {}
        self._initial_touches: Dict[int, TouchPoint] = {}
        self._last_tap_time: float = 0.0
        self._last_tap_pos: Optional[Tuple[float, float]] = None
        
        # Multi-touch initial baseline
        self._initial_two_finger_dist: Optional[float] = None
        self._initial_two_finger_angle: Optional[float] = None

        # Gesture listeners
        self._listeners: Dict[str, List[Callable[[BaseGestureEvent], None]]] = {
            GestureType.TAP: [],
            GestureType.DOUBLE_TAP: [],
            GestureType.LONG_PRESS: [],
            GestureType.PAN: [],
            GestureType.SWIPE: [],
            GestureType.PINCH: [],
            GestureType.ROTATE: []
        }

    def on(self, gesture_name: str, callback: Callable[[BaseGestureEvent], None]) -> None:
        if gesture_name not in self._listeners:
            self._listeners[gesture_name] = []
        self._listeners[gesture_name].append(callback)

    def process_touch_event(self, event: TouchEvent) -> List[RecognizedGesture]:
        recognized: List[RecognizedGesture] = []

        if event.phase == TouchPhase.START:
            for pt in event.changed_touches:
                self._touch_history[pt.touch_id] = [pt]
                self._initial_touches[pt.touch_id] = pt

            if len(event.touches) == 2:
                t1, t2 = event.touches[0], event.touches[1]
                self._initial_two_finger_dist = math.hypot(t2.x - t1.x, t2.y - t1.y)
                self._initial_two_finger_angle = math.atan2(t2.y - t1.y, t2.x - t1.x)

        elif event.phase == TouchPhase.MOVE:
            for pt in event.changed_touches:
                if pt.touch_id in self._touch_history:
                    prev = self._touch_history[pt.touch_id][-1]
                    dx = pt.x - prev.x
                    dy = pt.y - prev.y
                    self._touch_history[pt.touch_id].append(pt)

                    # Single finger Pan
                    if len(event.touches) == 1:
                        pan = PanGesture(dx=dx, dy=dy, x=pt.x, y=pt.y)
                        recognized.append(RecognizedGesture(GestureType.PAN, pan))
                        self._emit(GestureType.PAN, pan)

            # Two-finger Pinch & Rotate
            if len(event.touches) == 2 and self._initial_two_finger_dist:
                t1, t2 = event.touches[0], event.touches[1]
                curr_dist = math.hypot(t2.x - t1.x, t2.y - t1.y)
                curr_angle = math.atan2(t2.y - t1.y, t2.x - t1.x)

                if self._initial_two_finger_dist > 0:
                    scale = curr_dist / self._initial_two_finger_dist
                    focal_x = (t1.x + t2.x) / 2.0
                    focal_y = (t1.y + t2.y) / 2.0
                    pinch = PinchGesture(scale=scale, focal_x=focal_x, focal_y=focal_y)
                    recognized.append(RecognizedGesture(GestureType.PINCH, pinch))
                    self._emit(GestureType.PINCH, pinch)

                if self._initial_two_finger_angle is not None:
                    d_theta = math.degrees(curr_angle - self._initial_two_finger_angle)
                    center_x = (t1.x + t2.x) / 2.0
                    center_y = (t1.y + t2.y) / 2.0
                    rot = RotateGesture(angle=d_theta, center_x=center_x, center_y=center_y)
                    recognized.append(RecognizedGesture(GestureType.ROTATE, rot))
                    self._emit(GestureType.ROTATE, rot)

        elif event.phase == TouchPhase.END:
            for pt in event.changed_touches:
                if pt.touch_id in self._initial_touches:
                    start_pt = self._initial_touches[pt.touch_id]
                    dt_ms = (pt.timestamp - start_pt.timestamp) * 1000.0
                    dx = pt.x - start_pt.x
                    dy = pt.y - start_pt.y
                    distance = math.hypot(dx, dy)

                    # 1. Tap & Double Tap & Long Press
                    if distance <= self.touch_slop_dp:
                        if dt_ms >= self.long_press_timeout_ms:
                            long_press = LongPressGesture(x=pt.x, y=pt.y, duration_ms=int(dt_ms))
                            recognized.append(RecognizedGesture(GestureType.LONG_PRESS, long_press))
                            self._emit(GestureType.LONG_PRESS, long_press)
                        elif dt_ms <= self.tap_timeout_ms:
                            # Check for double tap
                            now = pt.timestamp
                            if self._last_tap_pos and (now - self._last_tap_time) * 1000.0 <= self.double_tap_timeout_ms:
                                tap_dist = math.hypot(pt.x - self._last_tap_pos[0], pt.y - self._last_tap_pos[1])
                                if tap_dist <= self.touch_slop_dp * 2:
                                    double_tap = DoubleTapGesture(x=pt.x, y=pt.y)
                                    recognized.append(RecognizedGesture(GestureType.DOUBLE_TAP, double_tap))
                                    self._emit(GestureType.DOUBLE_TAP, double_tap)
                                    self._last_tap_pos = None
                                    self._last_tap_time = 0.0
                                else:
                                    tap = TapGesture(x=pt.x, y=pt.y)
                                    recognized.append(RecognizedGesture(GestureType.TAP, tap))
                                    self._emit(GestureType.TAP, tap)
                                    self._last_tap_pos = (pt.x, pt.y)
                                    self._last_tap_time = now
                            else:
                                tap = TapGesture(x=pt.x, y=pt.y)
                                recognized.append(RecognizedGesture(GestureType.TAP, tap))
                                self._emit(GestureType.TAP, tap)
                                self._last_tap_pos = (pt.x, pt.y)
                                self._last_tap_time = now

                    # 2. Swipe detection
                    elif distance >= self.swipe_min_distance_dp:
                        velocity = distance / max(1.0, dt_ms)
                        if velocity >= self.swipe_min_velocity_dp_ms:
                            if abs(dx) > abs(dy):
                                direction = "right" if dx > 0 else "left"
                            else:
                                direction = "down" if dy > 0 else "up"
                            swipe = SwipeGesture(direction=direction, velocity=velocity, distance=distance)
                            recognized.append(RecognizedGesture(GestureType.SWIPE, swipe))
                            self._emit(GestureType.SWIPE, swipe)

                    # Cleanup tracking
                    self._touch_history.pop(pt.touch_id, None)
                    self._initial_touches.pop(pt.touch_id, None)

            if len(event.touches) < 2:
                self._initial_two_finger_dist = None
                self._initial_two_finger_angle = None

        elif event.phase == TouchPhase.CANCEL:
            self._touch_history.clear()
            self._initial_touches.clear()
            self._initial_two_finger_dist = None
            self._initial_two_finger_angle = None

        return recognized

    def _emit(self, gesture_name: str, event: BaseGestureEvent) -> None:
        for cb in self._listeners.get(gesture_name, []):
            try:
                cb(event)
            except Exception:
                pass

    def reset(self) -> None:
        self._touch_history.clear()
        self._initial_touches.clear()
        self._last_tap_pos = None
        self._last_tap_time = 0.0
        self._initial_two_finger_dist = None
        self._initial_two_finger_angle = None
