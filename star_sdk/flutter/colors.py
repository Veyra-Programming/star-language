"""
Star Flutter Color Palette & Design Tokens
Authoritative Reference: STAR_FLUTTER.md
Provides complete Material 3, Cupertino, and Fluent color swatches for Star.
"""

from typing import Dict, Any
from star_engine.types import StarValue, StarText, StarModule, StarBuiltinFunction, StarInteger, StarDecimal


PALETTE = {
    # Primary Swatches
    "indigo": "#6366f1",
    "indigoAccent": "#818cf8",
    "indigoLight": "#c7d2fe",
    "indigoDark": "#3730a3",
    "blue": "#3b82f6",
    "blueAccent": "#60a5fa",
    "lightBlue": "#0ea5e9",
    "cyan": "#06b6d4",
    "teal": "#14b8a6",
    "green": "#22c55e",
    "lightGreen": "#84cc16",
    "lime": "#a3e635",
    "yellow": "#eab308",
    "amber": "#f59e0b",
    "orange": "#f97316",
    "deepOrange": "#ff5722",
    "red": "#ef4444",
    "pink": "#ec4899",
    "purple": "#a855f7",
    "deepPurple": "#7c3aed",
    "violet": "#8b5cf6",
    "emerald": "#10b981",
    "rose": "#f43f5e",
    "fuchsia": "#d946ef",
    
    # Neutrals
    "slate": "#64748b",
    "slateDark": "#0f172a",
    "slateLight": "#f1f5f9",
    "grey": "#9ca3af",
    "greyLight": "#e5e7eb",
    "greyDark": "#374151",
    "blueGrey": "#64748b",
    "brown": "#78350f",
    
    # Monochrome & System
    "black": "#000000",
    "black87": "rgba(0, 0, 0, 0.87)",
    "black54": "rgba(0, 0, 0, 0.54)",
    "black38": "rgba(0, 0, 0, 0.38)",
    "black12": "rgba(0, 0, 0, 0.12)",
    "white": "#ffffff",
    "white70": "rgba(255, 255, 255, 0.70)",
    "white54": "rgba(255, 255, 255, 0.54)",
    "white30": "rgba(255, 255, 255, 0.30)",
    "white10": "rgba(255, 255, 255, 0.10)",
    "transparent": "transparent",
    
    # Semantic Material 3 Roles
    "primary": "#6366f1",
    "onPrimary": "#ffffff",
    "primaryContainer": "#e0e7ff",
    "onPrimaryContainer": "#1e1b4b",
    "secondary": "#06b6d4",
    "onSecondary": "#ffffff",
    "secondaryContainer": "#cffafe",
    "onSecondaryContainer": "#164e63",
    "tertiary": "#ec4899",
    "onTertiary": "#ffffff",
    "error": "#ef4444",
    "onError": "#ffffff",
    "background": "#0b0f19",
    "onBackground": "#f8fafc",
    "surface": "#131b2e",
    "onSurface": "#f1f5f9",
    "surfaceVariant": "#1e293b",
    "onSurfaceVariant": "#cbd5e1",
    "outline": "#475569",
    "outlineVariant": "#334155",
}


def create_colors_module() -> StarModule:
    exports: Dict[str, StarValue] = {}
    for name, hex_code in PALETTE.items():
        exports[name] = StarText(hex_code)

    def _color_from_argb(*args: StarValue) -> StarValue:
        if len(args) == 4:
            a, r, g, b = [int(getattr(x, "value", 255)) for x in args]
            return StarText(f"#{r:02x}{g:02x}{b:02x}")
        elif len(args) == 1:
            val = int(getattr(args[0], "value", 0))
            return StarText(f"#{val & 0xFFFFFF:06x}")
        return StarText("#ffffff")

    exports["fromARGB"] = StarBuiltinFunction("fromARGB", _color_from_argb)
    exports["fromRGB"] = StarBuiltinFunction("fromRGB", lambda *args: _color_from_argb(StarInteger(255), *args))
    return StarModule("Colors", exports)

