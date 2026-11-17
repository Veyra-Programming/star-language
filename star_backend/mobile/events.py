"""
Star Mobile Low-Level Touch Event Stream
Authoritative Reference: STAR_MOBILE.md (Section 3.1)
"""

import time
from typing import List, Dict, Any, Optional


class TouchPhase:
    START = "TouchStart"
    MOVE = "TouchMove"
    END = "TouchEnd"
    CANCEL = "TouchCancel"


class TouchPoint:
    def __init__(
        self,
        touch_id: int,
        x: float,
        y: float,
        timestamp: Optional[float] = None,
        pressure: float = 1.0
    ):
        self.touch_id = int(touch_id)
        self.x = float(x)
        self.y = float(y)
        self.timestamp = float(timestamp if timestamp is not None else time.time())
        self.pressure = float(pressure)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.touch_id,
            "x": self.x,
            "y": self.y,
            "timestamp": self.timestamp,
            "pressure": self.pressure
        }

    def __repr__(self) -> str:
        return f"TouchPoint(id={self.touch_id}, x={self.x:.1f}, y={self.y:.1f})"


class TouchEvent:
    def __init__(
        self,
        phase: str,
        touches: List[TouchPoint],
        changed_touches: Optional[List[TouchPoint]] = None
    ):
        self.phase = phase
        self.touches = touches
        self.changed_touches = changed_touches or touches
        self.timestamp = time.time()

    def __repr__(self) -> str:
        return f"TouchEvent(phase={self.phase}, touches={len(self.touches)})"
