"""
Star Mobile Device Hardware Bridge
Authoritative Reference: STAR_MOBILE_RUNTIME.md (Section 6)
"""

from typing import Dict, Any, Optional, List
from star_runtime.mobile.capabilities import CapabilityManager, MobileCapability, CapabilitySecurityError


class MobileDeviceBridge:
    """
    Capability-gated device hardware bridge coordinating access between Star mobile APIs
    and host platform drivers or simulated environments.
    """
    def __init__(self, capability_manager: Optional[CapabilityManager] = None):
        self.capabilities = capability_manager or CapabilityManager(list(MobileCapability.ALL))
        self._storage_store: Dict[str, str] = {}
        self._clipboard_buffer: str = ""
        self._vibration_history: List[Any] = []

    # Vibration & Haptics
    def vibrate(self, pattern: Any = None) -> None:
        self.capabilities.require(MobileCapability.VIBRATE)
        self._vibration_history.append(pattern or 100)

    # Secure Storage
    def storage_set(self, key: str, value: str) -> None:
        self.capabilities.require(MobileCapability.STORAGE)
        self._storage_store[key] = value

    def storage_get(self, key: str) -> Optional[str]:
        self.capabilities.require(MobileCapability.STORAGE)
        return self._storage_store.get(key)

    def storage_remove(self, key: str) -> None:
        self.capabilities.require(MobileCapability.STORAGE)
        self._storage_store.pop(key, None)

    # Battery
    def get_battery_info(self) -> Dict[str, Any]:
        self.capabilities.require(MobileCapability.BATTERY)
        return {
            "level": 0.85,
            "is_charging": True,
            "power_save": False
        }

    # Clipboard
    def clipboard_set(self, text: str) -> None:
        self.capabilities.require(MobileCapability.CLIPBOARD)
        self._clipboard_buffer = text

    def clipboard_get(self) -> str:
        self.capabilities.require(MobileCapability.CLIPBOARD)
        return self._clipboard_buffer
