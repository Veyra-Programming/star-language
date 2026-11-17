"""
Star Mobile Runtime Application Binary Interface (ABI)
Authoritative Reference: STAR_MOBILE.md & STAR_MOBILE_RUNTIME.md
"""

from enum import Enum, auto
from typing import Dict, Any, List, Optional, Tuple

MOBILE_ABI_VERSION = 1
MOBILE_ABI_MAGIC = b"STARMB01"


class MobileRenderOp(Enum):
    CLEAR = auto()
    CLIP_RECT = auto()
    DRAW_RECT = auto()
    DRAW_TEXT = auto()
    DRAW_CARD = auto()
    DRAW_BUTTON = auto()
    DRAW_APP_BAR = auto()
    DRAW_BADGE = auto()
    DRAW_DIVIDER = auto()
    DRAW_INPUT = auto()
    DRAW_SWITCH = auto()
    DRAW_SLIDER = auto()
    DRAW_BOTTOM_NAV = auto()


class MobileABI:
    """
    Specification of Mobile Runtime ABI Version 1 constants,
    structures, and interface contracts.
    """
    VERSION = MOBILE_ABI_VERSION
    MAGIC = MOBILE_ABI_MAGIC

    @staticmethod
    def get_abi_metadata() -> Dict[str, Any]:
        return {
            "abi_version": MOBILE_ABI_VERSION,
            "runtime_type": "mobile",
            "render_engine": "command_stream_v1",
            "min_touch_target_dp": 44.0,
            "supported_orientations": ["portrait", "landscape"],
            "supported_units": ["dp", "sp", "%", "px"]
        }
