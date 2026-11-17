"""
Star Mobile Headless Simulation & Test Runtime
Authoritative Reference: STAR_MOBILE.md (Section 8)
"""

import time
from typing import List, Dict, Any, Optional, Tuple, Callable
from star_engine.types import StarVirtualNode, StarValue, StarNull
from star_sdk.mobile.dimensions import ScreenMetrics
from star_sdk.mobile.safe_area import SafeAreaInsets
from star_sdk.mobile.lifecycle import get_lifecycle, LifecycleState
from star_sdk.mobile.gestures import BaseGestureEvent
from star_backend.mobile.events import TouchPhase, TouchPoint, TouchEvent
from star_backend.mobile.gesture_engine import GestureEngine, RecognizedGesture
from star_backend.mobile.layout import MobileLayoutEngine, MobileLayoutNode


class MobileHeadlessRuntime:
    """
    Headless Mobile Runtime facilitating programmatic simulation of touch gestures,
    device rotations, lifecycle states, layout passes, and reactive UI reconciliation.
    """
    def __init__(
        self,
        metrics: Optional[ScreenMetrics] = None,
        insets: Optional[SafeAreaInsets] = None
    ):
        self.metrics = metrics or ScreenMetrics()
        self.insets = insets or SafeAreaInsets()
        self.lifecycle = get_lifecycle()
        self.gesture_engine = GestureEngine()
        self.layout_engine = MobileLayoutEngine(self.metrics, self.insets)

        self.current_vnode: Optional[StarVirtualNode] = None
        self.current_layout: Optional[MobileLayoutNode] = None
        self.rendered_frames: int = 0
        self.gesture_log: List[RecognizedGesture] = []
        self._touch_counter: int = 1

        # Register gesture forwarder
        for g_type in ("Tap", "DoubleTap", "LongPress", "Pan", "Swipe", "Pinch", "Rotate"):
            self.gesture_engine.on(g_type, self._on_gesture_recognized)

    def _on_gesture_recognized(self, event: BaseGestureEvent) -> None:
        self.gesture_log.append(RecognizedGesture(event.gesture_type, event))

    def mount(self, root_vnode: StarVirtualNode) -> MobileLayoutNode:
        """Mounts a virtual DOM node tree and calculates the initial mobile layout."""
        self.lifecycle.transition_to(LifecycleState.RESUMED)
        self.current_vnode = root_vnode
        self.current_layout = self.layout_engine.compute_layout(root_vnode)
        self.rendered_frames += 1
        return self.current_layout

    def update(self, root_vnode: StarVirtualNode) -> MobileLayoutNode:
        """Re-computes layout upon reactive state changes."""
        self.current_vnode = root_vnode
        self.current_layout = self.layout_engine.compute_layout(root_vnode)
        self.rendered_frames += 1
        return self.current_layout

    # Gesture & Touch Simulation APIs
    def simulate_touch_event(self, phase: str, touch_coords: List[Tuple[float, float]]) -> List[RecognizedGesture]:
        now = time.time()
        touches = [
            TouchPoint(touch_id=i + 1, x=coords[0], y=coords[1], timestamp=now)
            for i, coords in enumerate(touch_coords)
        ]
        ev = TouchEvent(phase=phase, touches=touches)
        return self.gesture_engine.process_touch_event(ev)

    def simulate_tap(self, x: float, y: float) -> Tuple[List[RecognizedGesture], Optional[MobileLayoutNode]]:
        """Simulates a tap at (x, y) in DP coordinates and dispatches click listener if hit."""
        t0 = time.time()
        p1 = TouchPoint(1, x, y, timestamp=t0)
        self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.START, [p1]))

        p2 = TouchPoint(1, x, y, timestamp=t0 + 0.05) # 50ms tap duration
        gestures = self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.END, [p2]))

        # Hit test and dispatch click listener
        hit_node = None
        if self.current_layout:
            hit_node = self.layout_engine.hit_test(self.current_layout, x, y)
            if hit_node and hit_node.virtual_node:
                listener = hit_node.virtual_node.listeners.get("click")
                if listener:
                    listener.call([]) if hasattr(listener, "call") else listener()
        return gestures, hit_node

    def simulate_double_tap(self, x: float, y: float) -> List[RecognizedGesture]:
        t0 = time.time()
        # Tap 1
        self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.START, [TouchPoint(1, x, y, timestamp=t0)]))
        self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.END, [TouchPoint(1, x, y, timestamp=t0 + 0.04)]))
        # Tap 2 within 100ms
        t1 = t0 + 0.1
        self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.START, [TouchPoint(1, x, y, timestamp=t1)]))
        gestures = self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.END, [TouchPoint(1, x, y, timestamp=t1 + 0.04)]))
        return gestures

    def simulate_long_press(self, x: float, y: float, duration_ms: int = 600) -> List[RecognizedGesture]:
        t0 = time.time()
        self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.START, [TouchPoint(1, x, y, timestamp=t0)]))
        gestures = self.gesture_engine.process_touch_event(
            TouchEvent(TouchPhase.END, [TouchPoint(1, x, y, timestamp=t0 + (duration_ms / 1000.0))])
        )
        return gestures

    def simulate_swipe(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        duration_ms: float = 100.0
    ) -> List[RecognizedGesture]:
        t0 = time.time()
        t_end = t0 + (duration_ms / 1000.0)
        p1 = TouchPoint(1, start_x, start_y, timestamp=t0)
        self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.START, [p1]))

        mid_x = (start_x + end_x) / 2.0
        mid_y = (start_y + end_y) / 2.0
        p_mid = TouchPoint(1, mid_x, mid_y, timestamp=t0 + (duration_ms / 2000.0))
        self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.MOVE, [p_mid]))

        p2 = TouchPoint(1, end_x, end_y, timestamp=t_end)
        return self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.END, [p2]))

    def simulate_pinch(
        self,
        center_x: float,
        center_y: float,
        start_dist: float,
        end_dist: float
    ) -> List[RecognizedGesture]:
        t0 = time.time()
        # Two fingers starting at start_dist / 2 from center
        t1_0 = TouchPoint(1, center_x - (start_dist / 2.0), center_y, timestamp=t0)
        t2_0 = TouchPoint(2, center_x + (start_dist / 2.0), center_y, timestamp=t0)
        self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.START, [t1_0, t2_0]))

        # Two fingers moving to end_dist / 2 from center
        t1_1 = TouchPoint(1, center_x - (end_dist / 2.0), center_y, timestamp=t0 + 0.1)
        t2_1 = TouchPoint(2, center_x + (end_dist / 2.0), center_y, timestamp=t0 + 0.1)
        gestures = self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.MOVE, [t1_1, t2_1]))

        self.gesture_engine.process_touch_event(TouchEvent(TouchPhase.END, [t1_1, t2_1]))
        return gestures

    # Lifecycle & Device Management
    def transition_lifecycle(self, state: str) -> None:
        self.lifecycle.transition_to(state)

    def simulate_back_press(self) -> bool:
        return self.lifecycle.dispatch_back_press()

    def rotate_device(self, mode: str = "toggle") -> MobileLayoutNode:
        self.metrics.rotate(mode)
        self.layout_engine = MobileLayoutEngine(self.metrics, self.insets)
        if self.current_vnode:
            self.current_layout = self.layout_engine.compute_layout(self.current_vnode)
        return self.current_layout
