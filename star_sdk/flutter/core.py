"""
Star Flutter Core Runtime & Widget Lifecycle
Authoritative Reference: STAR_FLUTTER.md
Provides Flutter-style declarative component models, state containers, and context hierarchy for Star.
"""

from typing import Dict, List, Any, Optional, Callable
from star_engine.types import (
    StarValue, StarNull, StarText, StarInteger, StarDecimal, StarBoolean,
    StarList, StarMap, StarFunction, StarBuiltinFunction, StarModule,
    StarVirtualNode, StarComponentInstance
)


def _val_to_py(val: Any) -> Any:
    if isinstance(val, (StarInteger, StarDecimal)):
        return val.value
    elif isinstance(val, StarBoolean):
        return val.value
    elif isinstance(val, StarText):
        return val.value
    elif isinstance(val, StarList):
        return [_val_to_py(x) for x in val.elements]
    elif isinstance(val, StarMap):
        return {k: _val_to_py(v) for k, v in val.entries.items()}
    elif isinstance(val, StarNull):
        return None
    return val


class BuildContext:
    """Provides build tree contextual environment, theme tokens, and media query bounds."""
    def __init__(self, platform: str = "desktop", theme: Optional[Dict[str, Any]] = None, width: float = 800.0, height: float = 600.0):
        self.platform = platform
        self.theme = theme or {}
        self.width = width
        self.height = height

    def to_star_map(self) -> StarMap:
        return StarMap({
            "platform": StarText(self.platform),
            "width": StarDecimal(self.width),
            "height": StarDecimal(self.height),
            "is_mobile": StarBoolean(self.platform in ("android", "ios")),
            "is_desktop": StarBoolean(self.platform in ("desktop", "windows", "macos", "linux")),
            "is_web": StarBoolean(self.platform == "web"),
        })


class EdgeInsets:
    """Flutter EdgeInsets geometry utility."""
    @staticmethod
    def all(value: float) -> Dict[str, float]:
        return {"top": value, "right": value, "bottom": value, "left": value}

    @staticmethod
    def symmetric(vertical: float = 0.0, horizontal: float = 0.0) -> Dict[str, float]:
        return {"top": vertical, "right": horizontal, "bottom": vertical, "left": horizontal}

    @staticmethod
    def only(top: float = 0.0, right: float = 0.0, bottom: float = 0.0, left: float = 0.0) -> Dict[str, float]:
        return {"top": top, "right": right, "bottom": bottom, "left": left}


class BorderRadius:
    """Flutter BorderRadius corner rounding utility."""
    @staticmethod
    def circular(radius: float) -> Dict[str, float]:
        return {"topLeft": radius, "topRight": radius, "bottomRight": radius, "bottomLeft": radius}

    @staticmethod
    def only(topLeft: float = 0.0, topRight: float = 0.0, bottomRight: float = 0.0, bottomLeft: float = 0.0) -> Dict[str, float]:
        return {"topLeft": topLeft, "topRight": topRight, "bottomRight": bottomRight, "bottomLeft": bottomLeft}


class TextStyle:
    """Flutter TextStyle typographic definition."""
    def __init__(self, fontSize: float = 14.0, fontWeight: str = "normal", color: str = "#ffffff", fontStyle: str = "normal", height: float = 1.2):
        self.fontSize = fontSize
        self.fontWeight = fontWeight
        self.color = color
        self.fontStyle = fontStyle
        self.height = height

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fontSize": self.fontSize,
            "fontWeight": self.fontWeight,
            "color": self.color,
            "fontStyle": self.fontStyle,
            "height": self.height
        }


class BoxDecoration:
    """Flutter BoxDecoration background, border, gradient, and shadow wrapper."""
    def __init__(self, color: str = "", borderRadius: Optional[Dict[str, float]] = None, border: Optional[Dict[str, Any]] = None, gradient: Optional[Dict[str, Any]] = None, boxShadow: Optional[List[Dict[str, Any]]] = None):
        self.color = color
        self.borderRadius = borderRadius or BorderRadius.circular(0)
        self.border = border or {}
        self.gradient = gradient or {}
        self.boxShadow = boxShadow or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "color": self.color,
            "borderRadius": self.borderRadius,
            "border": self.border,
            "gradient": self.gradient,
            "boxShadow": self.boxShadow
        }

