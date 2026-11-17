"""
Star Android MotionEvent Input Bridge
Authoritative Reference: STAR_ANDROID.md (Section 5)
"""

from typing import List, Dict, Any, Optional
from star_backend.mobile.events import TouchPhase, TouchPoint, TouchEvent
from star_backend.mobile.gesture_engine import GestureEngine, RecognizedGesture
from star_backend.mobile.event_bridge import MobileEventBridge


class AndroidMotionEventAction:
    ACTION_DOWN = 0
    ACTION_UP = 1
    ACTION_MOVE = 2
    ACTION_CANCEL = 3
    ACTION_POINTER_DOWN = 5
    ACTION_POINTER_UP = 6


class AndroidInputBridge:
    """
    Translates Android MotionEvents into normalized Star touch streams and gestures.
    """
    def __init__(self, event_bridge: Optional[MobileEventBridge] = None):
        self.event_bridge = event_bridge or MobileEventBridge()

    def handle_motion_event(
        self,
        action: int,
        pointer_id: int,
        x: float,
        y: float,
        pressure: float = 1.0
    ) -> List[RecognizedGesture]:
        if action in (AndroidMotionEventAction.ACTION_DOWN, AndroidMotionEventAction.ACTION_POINTER_DOWN):
            phase_str = "down"
        elif action == AndroidMotionEventAction.ACTION_MOVE:
            phase_str = "move"
        elif action in (AndroidMotionEventAction.ACTION_UP, AndroidMotionEventAction.ACTION_POINTER_UP):
            phase_str = "up"
        elif action == AndroidMotionEventAction.ACTION_CANCEL:
            phase_str = "cancel"
        else:
            phase_str = "move"

        return self.event_bridge.handle_native_touch(
            phase_str=phase_str,
            pointer_id=pointer_id,
            x=x,
            y=y,
            pressure=pressure
        )
