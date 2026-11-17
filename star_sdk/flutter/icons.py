"""
Star Flutter Vector Icons Registry
Authoritative Reference: STAR_FLUTTER.md
Provides Material Symbols, Cupertino Glyphs, and Universal Icon definitions for Star.
"""

from typing import Dict
from star_engine.types import StarValue, StarText, StarModule


ICON_GLYPHS: Dict[str, str] = {
    # Material Core
    "star": "★",
    "star_border": "☆",
    "star_rounded": "★",
    "favorite": "♥",
    "favorite_border": "♡",
    "check": "✓",
    "check_circle": "✔",
    "close": "✕",
    "add": "+",
    "remove": "−",
    "plus": "+",
    "minus": "−",
    "search": "🔍",
    "settings": "⚙",
    "account_circle": "👤",
    "person": "👤",
    "people": "👥",
    "home": "🏠",
    "menu": "☰",
    "more_vert": "⋮",
    "more_horiz": "…",
    "arrow_forward": "➔",
    "arrow_back": "⬅",
    "arrow_upward": "⬆",
    "arrow_downward": "⬇",
    "chevron_right": "❯",
    "chevron_left": "❮",
    "expand_more": "▼",
    "expand_less": "▲",
    "notifications": "🔔",
    "notifications_active": "🕭",
    "mail": "✉",
    "email": "✉",
    "phone": "📞",
    "camera": "📷",
    "camera_alt": "📷",
    "image": "🖼",
    "videocam": "📹",
    "music_note": "🎵",
    "play_arrow": "▶",
    "pause": "⏸",
    "stop": "⏹",
    "refresh": "↻",
    "sync": "🔄",
    "share": "🔗",
    "delete": "🗑",
    "edit": "✏",
    "file_download": "📥",
    "file_upload": "📤",
    "cloud": "☁",
    "cloud_done": "☁✓",
    "shopping_cart": "🛒",
    "credit_card": "💳",
    "attach_money": "$",
    "payments": "💸",
    "trending_up": "📈",
    "trending_down": "📉",
    "insights": "📊",
    "analytics": "📊",
    "dashboard": "⊞",
    "widgets": "❖",
    "code": "</>",
    "terminal": ">_",
    "security": "🛡",
    "shield": "🛡",
    "lock": "🔒",
    "lock_open": "🔓",
    "fingerprint": "🆔",
    "bolt": "⚡",
    "flash_on": "⚡",
    "wb_sunny": "☀️",
    "nightlight": "🌙",
    "dark_mode": "🌙",
    "light_mode": "☀️",
    "palette": "🎨",
    "format_paint": "🖌",
    "sentiment_satisfied": "😊",
    "info": "ℹ",
    "warning": "⚠",
    "error": "❌",
    "help": "?",
    "battery_charging_full": "🔋",
    "wifi": "📶",
    "bluetooth": "ᛒ",
    "location_on": "📍",
    "gps_fixed": "🎯",
    "flutter": "💙",
    "star_lang": "🌟",
}


def create_icons_module() -> StarModule:
    exports: Dict[str, StarValue] = {}
    for name, glyph in ICON_GLYPHS.items():
        exports[name] = StarText(glyph)
    return StarModule("Icons", exports)

