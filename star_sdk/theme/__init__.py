"""
Star SDK Theme System
Authoritative Reference: STAR_UI.md
"""

from typing import Dict, Any
from star_engine.types import (
    StarValue, StarNull, StarText, StarInteger, StarBuiltinFunction, StarModule
)


THEME_PRESETS = {
    "dark": {
        "primary": "#6366f1",
        "secondary": "#a855f7",
        "background": "#0f172a",
        "surface": "#1e293b",
        "surface_variant": "#334155",
        "card_bg": "#1e293b",
        "text": "#f8fafc",
        "text_secondary": "#94a3b8",
        "border": "#334155",
        "border_focus": "#6366f1",
        "accent": "#38bdf8",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "radius_sm": 6,
        "radius_md": 12,
        "radius_lg": 18,
        "font_family": "Inter, system-ui, sans-serif",
        "font_size": 14,
        "mode": "dark"
    },
    "light": {
        "primary": "#4f46e5",
        "secondary": "#9333ea",
        "background": "#f8fafc",
        "surface": "#ffffff",
        "surface_variant": "#f1f5f9",
        "card_bg": "#ffffff",
        "text": "#0f172a",
        "text_secondary": "#64748b",
        "border": "#e2e8f0",
        "border_focus": "#4f46e5",
        "accent": "#0ea5e9",
        "success": "#059669",
        "warning": "#d97706",
        "danger": "#dc2626",
        "radius_sm": 6,
        "radius_md": 12,
        "radius_lg": 18,
        "font_family": "Inter, system-ui, sans-serif",
        "font_size": 14,
        "mode": "light"
    },
    "midnight": {
        "primary": "#818cf8",
        "secondary": "#c084fc",
        "background": "#030712",
        "surface": "#111827",
        "surface_variant": "#1f2937",
        "card_bg": "#0f172a",
        "text": "#f9fafb",
        "text_secondary": "#9ca3af",
        "border": "#374151",
        "border_focus": "#818cf8",
        "accent": "#22d3ee",
        "success": "#34d399",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "radius_sm": 8,
        "radius_md": 14,
        "radius_lg": 20,
        "font_family": "Inter, system-ui, sans-serif",
        "font_size": 14,
        "mode": "dark"
    },
    "aurora": {
        "primary": "#10b981",
        "secondary": "#8b5cf6",
        "background": "#051614",
        "surface": "#0c2824",
        "surface_variant": "#143a34",
        "card_bg": "#0a221f",
        "text": "#f0fdf4",
        "text_secondary": "#6ee7b7",
        "border": "#134e4a",
        "border_focus": "#10b981",
        "accent": "#34d399",
        "success": "#22c55e",
        "warning": "#eab308",
        "danger": "#f43f5e",
        "radius_sm": 8,
        "radius_md": 14,
        "radius_lg": 22,
        "font_family": "Inter, sans-serif",
        "font_size": 14,
        "mode": "dark"
    },
    "sunset": {
        "primary": "#f43f5e",
        "secondary": "#f97316",
        "background": "#1c0b16",
        "surface": "#2d1223",
        "surface_variant": "#431b34",
        "card_bg": "#281020",
        "text": "#fff1f2",
        "text_secondary": "#fca5a5",
        "border": "#5c2447",
        "border_focus": "#f43f5e",
        "accent": "#fb923c",
        "success": "#10b981",
        "warning": "#fbbf24",
        "danger": "#e11d48",
        "radius_sm": 8,
        "radius_md": 14,
        "radius_lg": 20,
        "font_family": "Inter, sans-serif",
        "font_size": 14,
        "mode": "dark"
    },
    "cyberpunk": {
        "primary": "#ff007f",
        "secondary": "#00f0ff",
        "background": "#05050d",
        "surface": "#120f24",
        "surface_variant": "#22193e",
        "card_bg": "#120f24",
        "text": "#00ffcc",
        "text_secondary": "#00d4ff",
        "border": "#ff007f",
        "border_focus": "#00f0ff",
        "accent": "#ffe600",
        "success": "#00ff66",
        "warning": "#ffe600",
        "danger": "#ff0055",
        "radius_sm": 4,
        "radius_md": 8,
        "radius_lg": 12,
        "font_family": "Courier New, monospace",
        "font_size": 14,
        "mode": "dark"
    },
    "nord": {
        "primary": "#88c0d0",
        "secondary": "#81a1c1",
        "background": "#2e3440",
        "surface": "#3b4252",
        "surface_variant": "#434c5e",
        "card_bg": "#3b4252",
        "text": "#eceff4",
        "text_secondary": "#d8dee9",
        "border": "#4c566a",
        "border_focus": "#88c0d0",
        "accent": "#ebcb8b",
        "success": "#a3be8c",
        "warning": "#ebcb8b",
        "danger": "#bf616a",
        "radius_sm": 6,
        "radius_md": 12,
        "radius_lg": 16,
        "font_family": "Inter, sans-serif",
        "font_size": 14,
        "mode": "dark"
    }
}


def create_theme_module() -> StarModule:
    current_theme = dict(THEME_PRESETS["dark"])
    exports: Dict[str, StarValue] = {}

    def _sync_exports():
        for k, v in current_theme.items():
            if isinstance(v, int):
                exports[k] = StarInteger(v)
            else:
                exports[k] = StarText(str(v))

    def _set_mode(*args: StarValue) -> StarValue:
        mode = args[0].to_string() if args else "dark"
        if mode in THEME_PRESETS:
            current_theme.update(THEME_PRESETS[mode])
            _sync_exports()
        return StarNull()

    def _set_preset(*args: StarValue) -> StarValue:
        preset = args[0].to_string() if args else "dark"
        if preset in THEME_PRESETS:
            current_theme.update(THEME_PRESETS[preset])
            _sync_exports()
        return StarNull()

    exports["set_mode"] = StarBuiltinFunction("set_mode", _set_mode)
    exports["set_preset"] = StarBuiltinFunction("set_preset", _set_preset)
    _sync_exports()

    return StarModule("Theme", exports)
