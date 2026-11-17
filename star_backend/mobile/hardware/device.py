"""
Star Mobile Hardware Device Model
Authoritative Reference: STAR_HARDWARE.md (Section 1)
"""

from enum import Enum
from typing import Dict, Any, Optional, List
from star_sdk.mobile.dimensions import ScreenMetrics
from star_sdk.mobile.safe_area import SafeAreaInsets


class DevicePlatform(str, Enum):
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"
    DESKTOP = "desktop"


class DeviceExecutionMode(str, Enum):
    SIMULATED = "simulated"
    EMULATOR = "emulator"
    PHYSICAL = "physical"


class DeviceCapabilities:
    def __init__(
        self,
        has_touch: bool = True,
        has_multitouch: bool = True,
        has_haptics: bool = True,
        has_battery: bool = True,
        has_camera: bool = True,
        has_geolocation: bool = True,
        has_network: bool = True,
        has_secure_storage: bool = True,
        has_clipboard: bool = True
    ):
        self.has_touch = has_touch
        self.has_multitouch = has_multitouch
        self.has_haptics = has_haptics
        self.has_battery = has_battery
        self.has_camera = has_camera
        self.has_geolocation = has_geolocation
        self.has_network = has_network
        self.has_secure_storage = has_secure_storage
        self.has_clipboard = has_clipboard

    def to_dict(self) -> Dict[str, bool]:
        return {
            "touch": self.has_touch,
            "multitouch": self.has_multitouch,
            "haptics": self.has_haptics,
            "battery": self.has_battery,
            "camera": self.has_camera,
            "geolocation": self.has_geolocation,
            "network": self.has_network,
            "secure_storage": self.has_secure_storage,
            "clipboard": self.has_clipboard
        }


class MobileDevice:
    """
    Represents a verified physical device, emulator, or simulator target.
    """
    def __init__(
        self,
        device_id: str,
        platform: DevicePlatform,
        mode: DeviceExecutionMode = DeviceExecutionMode.SIMULATED,
        model: str = "Generic Device",
        os_version: str = "1.0",
        metrics: Optional[ScreenMetrics] = None,
        insets: Optional[SafeAreaInsets] = None,
        capabilities: Optional[DeviceCapabilities] = None
    ):
        self.device_id = device_id
        self.platform = platform
        self.mode = mode
        self.model = model
        self.os_version = os_version
        self.metrics = metrics or ScreenMetrics()
        self.insets = insets or SafeAreaInsets()
        self.capabilities = capabilities or DeviceCapabilities()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "platform": self.platform.value,
            "mode": self.mode.value,
            "model": self.model,
            "os_version": self.os_version,
            "viewport": {
                "width_dp": self.metrics.width_dp,
                "height_dp": self.metrics.height_dp,
                "density_scale": self.metrics.density_scale,
                "orientation": self.metrics.orientation
            },
            "safe_area": {
                "top": self.insets.top,
                "bottom": self.insets.bottom,
                "left": self.insets.left,
                "right": self.insets.right
            },
            "capabilities": self.capabilities.to_dict()
        }
