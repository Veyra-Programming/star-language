"""
Star Mobile Capability & Permission Security Subsystem
Authoritative Reference: STAR_MOBILE.md (Section 7) & STAR_MOBILE_RUNTIME.md
"""

from typing import Set, List, Dict, Any, Optional
from star_engine.errors import StarRuntimeError


class MobileCapability:
    VIBRATE = "vibrate"
    STORAGE = "storage"
    BATTERY = "battery"
    CAMERA = "camera"
    GEOLOCATION = "geolocation"
    NETWORK = "network"
    CLIPBOARD = "clipboard"
    NOTIFICATIONS = "notifications"

    ALL = {
        VIBRATE, STORAGE, BATTERY, CAMERA,
        GEOLOCATION, NETWORK, CLIPBOARD, NOTIFICATIONS
    }


class CapabilitySecurityError(StarRuntimeError):
    """Raised when an application attempts to access an undeclared hardware capability."""
    def __init__(self, capability: str, reason: str = ""):
        msg = f"Security Violation: Access to mobile capability '{capability}' was denied."
        if reason:
            msg += f" Reason: {reason}"
        super().__init__(msg)
        self.capability = capability


class CapabilityManager:
    """
    Enforces security boundary by checking application capability declarations
    before granting access to native hardware APIs.
    """
    def __init__(self, declared_capabilities: Optional[List[str]] = None):
        self._granted: Set[str] = set()
        if declared_capabilities:
            for cap in declared_capabilities:
                c = cap.lower().strip()
                if c in MobileCapability.ALL:
                    self._granted.add(c)
                else:
                    # Allow custom capabilities
                    self._granted.add(c)

    def has_capability(self, capability: str) -> bool:
        return capability.lower().strip() in self._granted

    def require(self, capability: str) -> None:
        c = capability.lower().strip()
        if c not in self._granted:
            raise CapabilitySecurityError(
                capability=c,
                reason=f"Capability '{c}' is not declared in the application manifest."
            )

    def grant(self, capability: str) -> None:
        self._granted.add(capability.lower().strip())

    def revoke(self, capability: str) -> None:
        self._granted.discard(capability.lower().strip())

    def get_declared_list(self) -> List[str]:
        return sorted(list(self._granted))

    def __repr__(self) -> str:
        return f"CapabilityManager(granted={list(self._granted)})"


_ACTIVE_CAPABILITIES: Optional[CapabilityManager] = None


def get_active_capabilities() -> CapabilityManager:
    """Returns the currently active application capability manager singleton."""
    global _ACTIVE_CAPABILITIES
    if _ACTIVE_CAPABILITIES is None:
        _ACTIVE_CAPABILITIES = CapabilityManager(list(MobileCapability.ALL))
    return _ACTIVE_CAPABILITIES


def set_active_capabilities(manager: Optional[CapabilityManager]) -> None:
    """Sets the active application capability manager singleton."""
    global _ACTIVE_CAPABILITIES
    _ACTIVE_CAPABILITIES = manager


def reset_active_capabilities() -> None:
    """Resets the active capability manager with all standard capabilities."""
    global _ACTIVE_CAPABILITIES
    _ACTIVE_CAPABILITIES = CapabilityManager(list(MobileCapability.ALL))
