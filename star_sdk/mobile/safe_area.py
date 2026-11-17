"""
Star SDK Mobile Safe Area Inset Model
Authoritative Reference: STAR_MOBILE.md (Section 5.2)
"""

from typing import Tuple
from star_sdk.mobile.dimensions import ScreenMetrics


class SafeAreaInsets:
    """
    Represents hardware display insets (notches, dynamic islands, home bars) in DP.
    """
    def __init__(self, top: float = 47.0, bottom: float = 34.0, left: float = 0.0, right: float = 0.0):
        self.top = float(top)
        self.bottom = float(bottom)
        self.left = float(left)
        self.right = float(right)

    def to_tuple(self) -> Tuple[float, float, float, float]:
        return (self.top, self.bottom, self.left, self.right)

    def calculate_safe_bounds(self, metrics: ScreenMetrics) -> Tuple[float, float, float, float]:
        """
        Returns (safe_x, safe_y, safe_width, safe_height) in DP.
        """
        safe_x = self.left
        safe_y = self.top
        safe_w = max(0.0, metrics.width_dp - self.left - self.right)
        safe_h = max(0.0, metrics.height_dp - self.top - self.bottom)
        return (safe_x, safe_y, safe_w, safe_h)

    def apply_to_rect(self, x: float, y: float, width: float, height: float) -> dict:
        return {
            "x": float(x) + self.left,
            "y": float(y) + self.top,
            "width": max(0.0, float(width) - self.left - self.right),
            "height": max(0.0, float(height) - self.top - self.bottom)
        }

    def __repr__(self) -> str:
        return f"SafeAreaInsets(top={self.top}dp, bottom={self.bottom}dp, left={self.left}dp, right={self.right}dp)"
