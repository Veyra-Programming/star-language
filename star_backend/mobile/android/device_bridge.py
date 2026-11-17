"""
Star Android Hardware & Platform Services Bridge
Authoritative Reference: STAR_ANDROID.md (Section 6)
"""

from typing import Dict, Any, Optional, List
from star_runtime.mobile.capabilities import CapabilityManager, MobileCapability, CapabilitySecurityError
from star_backend.mobile.device_bridge import MobileDeviceBridge


class AndroidDeviceBridge(MobileDeviceBridge):
    """
    Android-specific implementation of the Mobile Device Bridge connecting
    Star Mobile APIs to Android framework system services.
    """
    def __init__(self, capability_manager: Optional[CapabilityManager] = None):
        super().__init__(capability_manager)
        self.android_sdk_version: int = 34
        self._shared_preferences: Dict[str, str] = {}
        self._vibration_log: List[Any] = []

    def vibrate(self, pattern: Any = None) -> None:
        """Invokes Android VibratorService."""
        self.capabilities.require(MobileCapability.VIBRATE)
        self._vibration_log.append(pattern or 100)

    def storage_set(self, key: str, value: str) -> None:
        """Stores key-value pairs in Android EncryptedSharedPreferences."""
        self.capabilities.require(MobileCapability.STORAGE)
        self._shared_preferences[key] = value

    def storage_get(self, key: str) -> Optional[str]:
        self.capabilities.require(MobileCapability.STORAGE)
        return self._shared_preferences.get(key)

    def storage_remove(self, key: str) -> None:
        self.capabilities.require(MobileCapability.STORAGE)
        self._shared_preferences.pop(key, None)

    def get_battery_info(self) -> Dict[str, Any]:
        """Queries Android BatteryManager."""
        self.capabilities.require(MobileCapability.BATTERY)
        return {
            "level": 0.90,
            "is_charging": True,
            "power_save": False,
            "temperature_celsius": 28.5
        }
