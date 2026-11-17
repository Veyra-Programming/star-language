"""
Star SDK Mobile Lifecycle Subsystem
Authoritative Reference: STAR_MOBILE.md (Section 4)
"""

from typing import List, Callable, Dict, Any, Optional
from star_engine.types import StarValue, StarNull, StarBoolean, StarBuiltinFunction


class LifecycleState:
    MOUNTED = "mounted"
    RESUMED = "resumed"       # Active foreground
    PAUSED = "paused"         # In background
    DETACHED = "detached"     # Destroyed/terminated


class MobileLifecycle:
    def __init__(self):
        self.state = LifecycleState.MOUNTED
        self._resume_callbacks: List[Callable[[], Any]] = []
        self._pause_callbacks: List[Callable[[], Any]] = []
        self._back_press_callbacks: List[Callable[[], Any]] = []
        self._memory_warning_callbacks: List[Callable[[], Any]] = []

    def on_resume(self, callback: Callable[[], Any]) -> None:
        self._resume_callbacks.append(callback)

    def on_pause(self, callback: Callable[[], Any]) -> None:
        self._pause_callbacks.append(callback)

    def on_back_press(self, callback: Callable[[], Any]) -> None:
        self._back_press_callbacks.append(callback)

    def on_memory_warning(self, callback: Callable[[], Any]) -> None:
        self._memory_warning_callbacks.append(callback)

    def transition_to(self, new_state: str) -> None:
        old_state = self.state
        if old_state == new_state:
            return

        self.state = new_state
        if new_state == LifecycleState.RESUMED:
            for cb in self._resume_callbacks:
                cb()
        elif new_state == LifecycleState.PAUSED:
            for cb in self._pause_callbacks:
                cb()

    def dispatch_back_press(self) -> bool:
        """Returns True if the event was handled/consumed, preventing default OS back navigation."""
        handled = False
        for cb in self._back_press_callbacks:
            res = cb()
            if res is True or (isinstance(res, StarBoolean) and res.value is True):
                handled = True
        return handled

    def dispatch_memory_warning(self) -> None:
        for cb in self._memory_warning_callbacks:
            cb()

    def reset(self) -> None:
        self.state = LifecycleState.MOUNTED
        self._resume_callbacks.clear()
        self._pause_callbacks.clear()
        self._back_press_callbacks.clear()
        self._memory_warning_callbacks.clear()


# Global lifecycle instance
_GLOBAL_LIFECYCLE = MobileLifecycle()


def get_lifecycle() -> MobileLifecycle:
    return _GLOBAL_LIFECYCLE
