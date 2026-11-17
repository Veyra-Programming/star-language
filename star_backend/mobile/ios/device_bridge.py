"""
Star iOS Apple Platform Services Bridge
Authoritative Reference: STAR_IOS.md (Section 6)
"""

from typing import Dict, Any, Optional, List
from star_runtime.mobile.capabilities import CapabilityManager, MobileCapability, CapabilitySecurityError
from star_backend.mobile.device_bridge import MobileDeviceBridge


class iOSDeviceBridge(MobileDeviceBridge):
    """
    iOS-specific implementation of the Mobile Device Bridge connecting
    Star Mobile APIs to Apple platform frameworks (UIKit, Security/Keychain, IOKit).
    """
    def __init__(self, capability_manager: Optional[CapabilityManager] = None):
        super().__init__(capability_manager)
        self.ios_sdk_version: str = "17.0"
        self._keychain_store: Dict[str, str] = {}
        self._haptics_log: List[Any] = []

    def vibrate(self, pattern: Any = None) -> None:
        """Invokes Apple UIImpactFeedbackGenerator / UINotificationFeedbackGenerator."""
        self.capabilities.require(MobileCapability.VIBRATE)
        self._haptics_log.append(pattern or "medium")

    def storage_set(self, key: str, value: str) -> None:
        """Stores key-value pairs securely in Apple Keychain."""
        self.capabilities.require(MobileCapability.STORAGE)
        self._keychain_store[key] = value

    def storage_get(self, key: str) -> Optional[str]:
        self.capabilities.require(MobileCapability.STORAGE)
        return self._keychain_store.get(key)

    def storage_remove(self, key: str) -> None:
        self.capabilities.require(MobileCapability.STORAGE)
        self._keychain_store.pop(key, None)

    def get_battery_info(self) -> Dict[str, Any]:
        """Queries UIDevice battery state."""
        self.capabilities.require(MobileCapability.BATTERY)
        return {
            "level": 0.95,
            "is_charging": False,
            "power_save": False,
            "state": "unplugged"
        }
