"""
Star SDK Mobile Gestures & Event Definitions
Authoritative Reference: STAR_MOBILE.md (Section 3)
"""

from typing import Dict, Any, List, Optional, Callable
from star_engine.types import (
    StarValue, StarText, StarInteger, StarDecimal, StarBoolean,
    StarMap, StarList
)


class GestureType:
    TAP = "Tap"
    DOUBLE_TAP = "DoubleTap"
    LONG_PRESS = "LongPress"
    PAN = "Pan"
    SWIPE = "Swipe"
    PINCH = "Pinch"
    ROTATE = "Rotate"


class BaseGestureEvent:
    def __init__(self, gesture_type: str, raw_payload: Optional[Dict[str, Any]] = None):
        self.gesture_type = gesture_type
        self.raw_payload = raw_payload or {}

    def to_star_map(self) -> StarMap:
        entries: Dict[str, StarValue] = {
            "type": StarText(self.gesture_type)
        }
        for k, v in self.raw_payload.items():
            if isinstance(v, (int, float)):
                entries[k] = StarDecimal(float(v)) if isinstance(v, float) else StarInteger(int(v))
            elif isinstance(v, bool):
                entries[k] = StarBoolean(v)
            elif isinstance(v, str):
                entries[k] = StarText(v)
            elif isinstance(v, list):
                entries[k] = StarList([StarText(str(item)) for item in v])
        return StarMap(entries)


class TapGesture(BaseGestureEvent):
    def __init__(self, x: float, y: float):
        super().__init__(GestureType.TAP, {"x": x, "y": y})
        self.x = float(x)
        self.y = float(y)


class DoubleTapGesture(BaseGestureEvent):
    def __init__(self, x: float, y: float):
        super().__init__(GestureType.DOUBLE_TAP, {"x": x, "y": y})
        self.x = float(x)
        self.y = float(y)


class LongPressGesture(BaseGestureEvent):
    def __init__(self, x: float, y: float, duration_ms: int):
        super().__init__(GestureType.LONG_PRESS, {"x": x, "y": y, "duration_ms": duration_ms})
        self.x = float(x)
        self.y = float(y)
        self.duration_ms = int(duration_ms)


class PanGesture(BaseGestureEvent):
    def __init__(self, dx: float, dy: float, x: float, y: float):
        super().__init__(GestureType.PAN, {"dx": dx, "dy": dy, "x": x, "y": y})
        self.dx = float(dx)
        self.dy = float(dy)
        self.x = float(x)
        self.y = float(y)


class SwipeGesture(BaseGestureEvent):
    def __init__(self, direction: str, velocity: float, distance: float = 0.0):
        super().__init__(GestureType.SWIPE, {
            "direction": direction,
            "velocity": velocity,
            "distance": distance
        })
        self.direction = direction
        self.velocity = float(velocity)
        self.distance = float(distance)


class PinchGesture(BaseGestureEvent):
    def __init__(self, scale: float, focal_x: float, focal_y: float):
        super().__init__(GestureType.PINCH, {
            "scale": scale,
            "focal_x": focal_x,
            "focal_y": focal_y
        })
        self.scale = float(scale)
        self.focal_x = float(focal_x)
        self.focal_y = float(focal_y)


class RotateGesture(BaseGestureEvent):
    def __init__(self, angle: float, center_x: float, center_y: float):
        super().__init__(GestureType.ROTATE, {
            "angle": angle,
            "center_x": center_x,
            "center_y": center_y
        })
        self.angle = float(angle)
        self.center_x = float(center_x)
        self.center_y = float(center_y)
