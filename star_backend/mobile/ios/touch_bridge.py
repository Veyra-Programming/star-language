"""
Star iOS UITouch Event Bridge
Authoritative Reference: STAR_IOS.md (Section 5)
"""

from typing import List, Dict, Any, Optional
from star_backend.mobile.events import TouchPhase, TouchPoint, TouchEvent
from star_backend.mobile.gesture_engine import GestureEngine, RecognizedGesture
from star_backend.mobile.event_bridge import MobileEventBridge


class iOSUITouchPhase:
    BEGAN = 0
    MOVED = 1
    ENDED = 2
    CANCELLED = 3


class iOSTouchBridge:
    """
    Translates iOS UITouch events into normalized Star touch streams and gestures.
    """
    def __init__(self, event_bridge: Optional[MobileEventBridge] = None):
        self.event_bridge = event_bridge or MobileEventBridge()

    def handle_ui_touch(
        self,
        phase: int,
        touch_id: int,
        x: float,
        y: float,
        force: float = 1.0
    ) -> List[RecognizedGesture]:
        if phase == iOSUITouchPhase.BEGAN:
            phase_str = "down"
        elif phase == iOSUITouchPhase.MOVED:
            phase_str = "move"
        elif phase == iOSUITouchPhase.ENDED:
            phase_str = "up"
        elif phase == iOSUITouchPhase.CANCELLED:
            phase_str = "cancel"
        else:
            phase_str = "move"

        return self.event_bridge.handle_native_touch(
            phase_str=phase_str,
            pointer_id=touch_id,
            x=x,
            y=y,
            pressure=force
        )
