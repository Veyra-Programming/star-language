"""
Star Mobile Native Lifecycle Bridge
Authoritative Reference: STAR_MOBILE_RUNTIME.md (Section 5)
"""

from typing import Optional
from star_sdk.mobile.lifecycle import get_lifecycle, MobileLifecycle, LifecycleState


class MobileLifecycleBridge:
    """
    Coordinates host operating system lifecycle events (Android Activity / iOS App Delegate)
    with the Star Mobile application lifecycle state machine.
    """
    def __init__(self, lifecycle: Optional[MobileLifecycle] = None):
        self.lifecycle = lifecycle or get_lifecycle()

    def on_native_resume(self) -> None:
        """Host app came to foreground / became active."""
        self.lifecycle.transition_to(LifecycleState.RESUMED)

    def on_native_pause(self) -> None:
        """Host app moved to background / lost focus."""
        self.lifecycle.transition_to(LifecycleState.PAUSED)

    def on_native_destroy(self) -> None:
        """Host app is terminating."""
        self.lifecycle.transition_to(LifecycleState.DETACHED)

    def on_native_back_press(self) -> bool:
        """Host back button was pressed. Returns True if consumed by Star app."""
        return self.lifecycle.dispatch_back_press()

    def on_native_memory_warning(self) -> None:
        """Host system signaled low memory condition."""
        self.lifecycle.dispatch_memory_warning()
