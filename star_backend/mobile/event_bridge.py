"""
Star Mobile Native Event Bridge
Authoritative Reference: STAR_MOBILE_RUNTIME.md (Section 4)
"""

import time
from typing import List, Dict, Any, Optional, Tuple, Callable
from star_backend.mobile.events import TouchPhase, TouchPoint, TouchEvent
from star_backend.mobile.gesture_engine import GestureEngine, RecognizedGesture
from star_backend.mobile.layout import MobileLayoutEngine, MobileLayoutNode


class MobileEventBridge:
    """
    Translates raw platform OS touch inputs into Star touch events and dispatches
    recognized gestures to active UI layout nodes and event listeners.
    """
    def __init__(self, gesture_engine: Optional[GestureEngine] = None):
        self.gesture_engine = gesture_engine or GestureEngine()
        self._active_layout: Optional[MobileLayoutNode] = None
        self._layout_engine: Optional[MobileLayoutEngine] = None
        self._active_native_touches: Dict[int, TouchPoint] = {}

    def attach_layout(self, layout_root: MobileLayoutNode, layout_engine: MobileLayoutEngine) -> None:
        self._active_layout = layout_root
        self._layout_engine = layout_engine

    def handle_native_touch(
        self,
        phase_str: str,
        pointer_id: int,
        x: float,
        y: float,
        pressure: float = 1.0
    ) -> List[RecognizedGesture]:
        now = time.time()
        pt = TouchPoint(touch_id=pointer_id, x=x, y=y, timestamp=now, pressure=pressure)

        if phase_str == "down":
            self._active_native_touches[pointer_id] = pt
            phase = TouchPhase.START
        elif phase_str == "move":
            self._active_native_touches[pointer_id] = pt
            phase = TouchPhase.MOVE
        elif phase_str in ("up", "ended"):
            self._active_native_touches.pop(pointer_id, None)
            phase = TouchPhase.END
        elif phase_str == "cancel":
            self._active_native_touches.pop(pointer_id, None)
            phase = TouchPhase.CANCEL
        else:
            phase = TouchPhase.MOVE

        all_touches = list(self._active_native_touches.values())
        if phase == TouchPhase.END and pt not in all_touches:
            # Include released point in the event touches for gesture calculation
            all_touches.append(pt)

        event = TouchEvent(phase=phase, touches=all_touches, changed_touches=[pt])
        gestures = self.gesture_engine.process_touch_event(event)

        # If a tap was recognized, hit test and dispatch
        for g in gestures:
            if g.name == "Tap" and self._active_layout and self._layout_engine:
                hit = self._layout_engine.hit_test(self._active_layout, pt.x, pt.y)
                if hit and hit.virtual_node:
                    click_fn = hit.virtual_node.listeners.get("click")
                    if click_fn:
                        click_fn.call([]) if hasattr(click_fn, "call") else click_fn()

        return gestures
