"""
Star SDK Mobile Dimensions & Screen Metrics Subsystem
Authoritative Reference: STAR_MOBILE.md (Section 5)
"""

import re
from typing import Union, Tuple


class DimensionUnit:
    DP = "dp"    # Density-independent Pixels (160 dpi baseline)
    SP = "sp"    # Scale-independent Pixels (font accessibility)
    PERCENT = "%" # Percentage of parent container
    PX = "px"    # Raw physical pixels


class Dimension:
    def __init__(self, value: float, unit: str = DimensionUnit.DP):
        self.value = float(value)
        self.unit = unit

    @classmethod
    def parse(cls, dim_str: Union[str, int, float]) -> "Dimension":
        if isinstance(dim_str, (int, float)):
            return cls(float(dim_str), DimensionUnit.DP)
        
        s = str(dim_str).strip().lower()
        if s.endswith("dp"):
            return cls(float(s[:-2].strip()), DimensionUnit.DP)
        elif s.endswith("sp"):
            return cls(float(s[:-2].strip()), DimensionUnit.SP)
        elif s.endswith("%"):
            return cls(float(s[:-1].strip()), DimensionUnit.PERCENT)
        elif s.endswith("px"):
            return cls(float(s[:-2].strip()), DimensionUnit.PX)
        
        try:
            return cls(float(s), DimensionUnit.DP)
        except ValueError:
            raise ValueError(f"Invalid dimension format: '{dim_str}'")

    def resolve_to_px(self, metrics: "ScreenMetrics", parent_size_px: float = 0.0) -> float:
        if self.unit == DimensionUnit.DP:
            return self.value * metrics.density_scale
        elif self.unit == DimensionUnit.SP:
            return self.value * metrics.density_scale * metrics.font_scale
        elif self.unit == DimensionUnit.PERCENT:
            return (self.value / 100.0) * parent_size_px
        elif self.unit == DimensionUnit.PX:
            return self.value
        return self.value

    def __repr__(self) -> str:
        return f"Dimension({self.value}{self.unit})"


class ScreenMetrics:
    """Represents mobile physical screen and virtual density configuration."""
    def __init__(
        self,
        width_dp: float = 390.0,    # Default iPhone 14/15 or Pixel 7 baseline
        height_dp: float = 844.0,
        density_scale: float = 2.0,  # xhdpi / 2x scale
        font_scale: float = 1.0,
        orientation: str = "portrait"
    ):
        self.width_dp = float(width_dp)
        self.height_dp = float(height_dp)
        self.density_scale = float(density_scale)
        self.font_scale = float(font_scale)
        self.orientation = orientation.lower()

    @property
    def width_px(self) -> float:
        return self.width_dp * self.density_scale

    @property
    def height_px(self) -> float:
        return self.height_dp * self.density_scale

    def rotate(self, mode: str = "toggle") -> None:
        if mode == "toggle":
            self.orientation = "landscape" if self.orientation == "portrait" else "portrait"
        elif mode in ("portrait", "landscape"):
            self.orientation = mode
        
        # Swap width and height if orientation changed
        if (self.orientation == "landscape" and self.width_dp < self.height_dp) or \
           (self.orientation == "portrait" and self.width_dp > self.height_dp):
            self.width_dp, self.height_dp = self.height_dp, self.width_dp

    def copy(self) -> "ScreenMetrics":
        return ScreenMetrics(
            width_dp=self.width_dp,
            height_dp=self.height_dp,
            density_scale=self.density_scale,
            font_scale=self.font_scale,
            orientation=self.orientation
        )
