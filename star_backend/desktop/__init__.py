"""
Star Desktop Native Backend
Authoritative Reference: STAR_DESKTOP.md
"""

from star_backend.desktop.window import DesktopWindow
from star_backend.desktop.events import DesktopEventManager, DesktopEvent
from star_backend.desktop.runtime import DesktopRuntime
from star_backend.desktop.compiler import DesktopCompiler
from star_backend.desktop.builder import DesktopBuilder

__all__ = [
    "DesktopWindow",
    "DesktopEventManager",
    "DesktopEvent",
    "DesktopRuntime",
    "DesktopCompiler",
    "DesktopBuilder"
]
