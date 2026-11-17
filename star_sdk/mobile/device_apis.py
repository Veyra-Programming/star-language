"""
Star Universal Device Hardware SDK & Cross-Platform Provider Architecture
Authoritative Reference: STAR_DEVICE_SDK.md & STAR_CONFORMANCE.md
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from star_runtime.mobile.capabilities import (
    CapabilityManager,
    MobileCapability,
    CapabilitySecurityError,
    get_active_capabilities
)


class IDeviceProvider(ABC):
    """
    Abstract contract for native platform device capabilities.
    Must be implemented by Web, Desktop, Android, and iOS providers with identical observable semantics.
    """
    @abstractmethod
    def storage_set(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def storage_get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    def storage_remove(self, key: str) -> None:
        pass

    @abstractmethod
    def battery_level(self) -> float:
        pass

    @abstractmethod
    def battery_is_charging(self) -> bool:
        pass

    @abstractmethod
    def haptic_impact(self, style: str = "medium") -> None:
        pass

    @abstractmethod
    def haptic_notification(self, notify_type: str = "success") -> None:
        pass

    @abstractmethod
    def vibrate(self, pattern: Union[int, List[int]] = 50) -> None:
        pass

    @abstractmethod
    def clipboard_set(self, text: str) -> None:
        pass

    @abstractmethod
    def clipboard_get(self) -> str:
        pass

    @abstractmethod
    def screen_width_dp(self) -> float:
        pass

    @abstractmethod
    def screen_height_dp(self) -> float:
        pass

    @abstractmethod
    def screen_scale_factor(self) -> float:
        pass

    @abstractmethod
    def orientation_current(self) -> str:
        pass

    @abstractmethod
    def orientation_lock(self, orientation: str) -> None:
        pass

    @abstractmethod
    def orientation_unlock(self) -> None:
        pass

    @abstractmethod
    def share_text(self, text: str, title: Optional[str] = None) -> bool:
        pass

    @abstractmethod
    def network_status(self) -> str:
        pass

    @abstractmethod
    def camera_available(self) -> bool:
        pass

    @abstractmethod
    def geolocation_available(self) -> bool:
        pass


class BaseSimulatedDeviceProvider(IDeviceProvider):
    """
    Base deterministically-verifiable provider implementation used for headless testing,
    CI validation, and default simulation across all environments.
    """
    def __init__(self, platform_name: str = "simulated"):
        self.platform_name = platform_name
        self._storage: Dict[str, str] = {}
        self._clipboard: str = ""
        self._battery_level: float = 0.95
        self._is_charging: bool = False
        self._haptics_log: List[Dict[str, Any]] = []
        self._width_dp: float = 390.0
        self._height_dp: float = 844.0
        self._scale_factor: float = 3.0
        self._orientation: str = "portrait"
        self._orientation_locked: Optional[str] = None
        self._network_state: str = "wifi"
        self._camera_ready: bool = True
        self._geo_ready: bool = True

    def storage_set(self, key: str, value: str) -> None:
        self._storage[key] = str(value)

    def storage_get(self, key: str) -> Optional[str]:
        return self._storage.get(key)

    def storage_remove(self, key: str) -> None:
        self._storage.pop(key, None)

    def battery_level(self) -> float:
        return self._battery_level

    def battery_is_charging(self) -> bool:
        return self._is_charging

    def haptic_impact(self, style: str = "medium") -> None:
        self._haptics_log.append({"type": "impact", "style": style})

    def haptic_notification(self, notify_type: str = "success") -> None:
        self._haptics_log.append({"type": "notification", "notify_type": notify_type})

    def vibrate(self, pattern: Union[int, List[int]] = 50) -> None:
        self._haptics_log.append({"type": "vibrate", "pattern": pattern})

    def clipboard_set(self, text: str) -> None:
        self._clipboard = str(text)

    def clipboard_get(self) -> str:
        return self._clipboard

    def screen_width_dp(self) -> float:
        return self._width_dp

    def screen_height_dp(self) -> float:
        return self._height_dp

    def screen_scale_factor(self) -> float:
        return self._scale_factor

    def orientation_current(self) -> str:
        return self._orientation_locked or self._orientation

    def orientation_lock(self, orientation: str) -> None:
        self._orientation_locked = orientation

    def orientation_unlock(self) -> None:
        self._orientation_locked = None

    def share_text(self, text: str, title: Optional[str] = None) -> bool:
        return True

    def network_status(self) -> str:
        return self._network_state

    def camera_available(self) -> bool:
        return self._camera_ready

    def geolocation_available(self) -> bool:
        return self._geo_ready


class WebDeviceProvider(BaseSimulatedDeviceProvider):
    """Web (WASM / Browser) device provider implementation."""
    def __init__(self):
        super().__init__(platform_name="web")
        self._width_dp = 412.0
        self._height_dp = 915.0
        self._scale_factor = 2.0


class DesktopDeviceProvider(BaseSimulatedDeviceProvider):
    """Desktop (Native OS Window) device provider implementation."""
    def __init__(self):
        super().__init__(platform_name="desktop")
        self._width_dp = 1280.0
        self._height_dp = 720.0
        self._scale_factor = 1.0
        self._orientation = "landscape"


class AndroidDeviceProvider(BaseSimulatedDeviceProvider):
    """Android (JVM / JNI / NDK) device provider implementation."""
    def __init__(self):
        super().__init__(platform_name="android")
        self._width_dp = 412.0
        self._height_dp = 915.0
        self._scale_factor = 2.625


class iOSDeviceProvider(BaseSimulatedDeviceProvider):
    """iOS (Swift / Metal / UIKit) device provider implementation."""
    def __init__(self):
        super().__init__(platform_name="ios")
        self._width_dp = 393.0
        self._height_dp = 852.0
        self._scale_factor = 3.0


class DeviceProviderRegistry:
    """Manages active device provider binding."""
    _current_provider: Optional[IDeviceProvider] = None

    @classmethod
    def get_provider(cls) -> IDeviceProvider:
        if cls._current_provider is None:
            cls._current_provider = BaseSimulatedDeviceProvider()
        return cls._current_provider

    @classmethod
    def set_provider(cls, provider: IDeviceProvider) -> None:
        cls._current_provider = provider


# ---------------------------------------------------------------------------
# Universal Capability-Gated Device API Modules (Exposed via `use Mobile`)
# ---------------------------------------------------------------------------

class StorageAPI:
    @staticmethod
    def set(key: str, value: str) -> None:
        get_active_capabilities().require(MobileCapability.STORAGE)
        DeviceProviderRegistry.get_provider().storage_set(key, value)

    @staticmethod
    def get(key: str) -> Optional[str]:
        get_active_capabilities().require(MobileCapability.STORAGE)
        return DeviceProviderRegistry.get_provider().storage_get(key)

    @staticmethod
    def remove(key: str) -> None:
        get_active_capabilities().require(MobileCapability.STORAGE)
        DeviceProviderRegistry.get_provider().storage_remove(key)


class BatteryAPI:
    @staticmethod
    def level() -> float:
        get_active_capabilities().require(MobileCapability.BATTERY)
        return DeviceProviderRegistry.get_provider().battery_level()

    @staticmethod
    def is_charging() -> bool:
        get_active_capabilities().require(MobileCapability.BATTERY)
        return DeviceProviderRegistry.get_provider().battery_is_charging()


class HapticsAPI:
    @staticmethod
    def impact(style: str = "medium") -> None:
        get_active_capabilities().require(MobileCapability.VIBRATE)
        DeviceProviderRegistry.get_provider().haptic_impact(style)

    @staticmethod
    def notification(notify_type: str = "success") -> None:
        get_active_capabilities().require(MobileCapability.VIBRATE)
        DeviceProviderRegistry.get_provider().haptic_notification(notify_type)


class ClipboardAPI:
    @staticmethod
    def set(text: str) -> None:
        get_active_capabilities().require(MobileCapability.CLIPBOARD)
        DeviceProviderRegistry.get_provider().clipboard_set(text)

    @staticmethod
    def get() -> str:
        get_active_capabilities().require(MobileCapability.CLIPBOARD)
        return DeviceProviderRegistry.get_provider().clipboard_get()


class ScreenAPI:
    @staticmethod
    def width_dp() -> float:
        return DeviceProviderRegistry.get_provider().screen_width_dp()

    @staticmethod
    def height_dp() -> float:
        return DeviceProviderRegistry.get_provider().screen_height_dp()

    @staticmethod
    def scale_factor() -> float:
        return DeviceProviderRegistry.get_provider().screen_scale_factor()

    @staticmethod
    def orientation() -> str:
        return DeviceProviderRegistry.get_provider().orientation_current()


class OrientationAPI:
    @staticmethod
    def current() -> str:
        return DeviceProviderRegistry.get_provider().orientation_current()

    @staticmethod
    def lock(orientation: str) -> None:
        DeviceProviderRegistry.get_provider().orientation_lock(orientation)

    @staticmethod
    def unlock() -> None:
        DeviceProviderRegistry.get_provider().orientation_unlock()


class ShareAPI:
    @staticmethod
    def text(content: str, title: Optional[str] = None) -> bool:
        return DeviceProviderRegistry.get_provider().share_text(content, title=title)


class NetworkAPI:
    @staticmethod
    def status() -> str:
        get_active_capabilities().require(MobileCapability.NETWORK)
        return DeviceProviderRegistry.get_provider().network_status()

    @staticmethod
    def is_connected() -> bool:
        get_active_capabilities().require(MobileCapability.NETWORK)
        return DeviceProviderRegistry.get_provider().network_status() != "none"


class GeolocationAPI:
    @staticmethod
    def is_available() -> bool:
        get_active_capabilities().require(MobileCapability.GEOLOCATION)
        return DeviceProviderRegistry.get_provider().geolocation_available()


class CameraAPI:
    @staticmethod
    def is_available() -> bool:
        get_active_capabilities().require(MobileCapability.CAMERA)
        return DeviceProviderRegistry.get_provider().camera_available()
