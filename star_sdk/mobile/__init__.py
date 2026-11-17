"""
Star SDK Mobile Module
Authoritative Reference: STAR_MOBILE.md & STAR_DEVICE_SDK.md
"""

from typing import Dict, List, Any, Optional
from star_engine.types import (
    StarValue, StarNull, StarText, StarInteger, StarDecimal, StarBoolean,
    StarList, StarMap, StarFunction, StarBuiltinFunction, StarModule,
    StarVirtualNode
)
from star_sdk.mobile.lifecycle import get_lifecycle, LifecycleState
from star_sdk.mobile.dimensions import ScreenMetrics
from star_sdk.mobile.safe_area import SafeAreaInsets
from star_sdk.mobile.components import (
    make_safe_area, make_scroll_view, make_app_bar,
    make_bottom_navigation, make_switch, make_slider, make_action_sheet
)
from star_sdk.mobile.device_apis import (
    IDeviceProvider, BaseSimulatedDeviceProvider,
    WebDeviceProvider, DesktopDeviceProvider, AndroidDeviceProvider, iOSDeviceProvider,
    DeviceProviderRegistry,
    StorageAPI, BatteryAPI, HapticsAPI, ClipboardAPI, ScreenAPI,
    OrientationAPI, ShareAPI, NetworkAPI, GeolocationAPI, CameraAPI
)

# Global active metrics
_CURRENT_METRICS = ScreenMetrics()
_CURRENT_INSETS = SafeAreaInsets()


def get_current_metrics() -> ScreenMetrics:
    return _CURRENT_METRICS


def get_current_insets() -> SafeAreaInsets:
    return _CURRENT_INSETS


def create_mobile_module() -> StarModule:
    exports: Dict[str, StarValue] = {}
    lifecycle = get_lifecycle()

    # Lifecycle APIs
    def _on_resume(*args: StarValue) -> StarValue:
        if args and isinstance(args[0], (StarFunction, StarBuiltinFunction)):
            fn = args[0]
            lifecycle.on_resume(lambda: fn.call([]) if isinstance(fn, StarFunction) else fn.func())
        return StarNull()

    def _on_pause(*args: StarValue) -> StarValue:
        if args and isinstance(args[0], (StarFunction, StarBuiltinFunction)):
            fn = args[0]
            lifecycle.on_pause(lambda: fn.call([]) if isinstance(fn, StarFunction) else fn.func())
        return StarNull()

    def _on_back_press(*args: StarValue) -> StarValue:
        if args and isinstance(args[0], (StarFunction, StarBuiltinFunction)):
            fn = args[0]
            lifecycle.on_back_press(lambda: fn.call([]) if isinstance(fn, StarFunction) else fn.func())
        return StarNull()

    def _on_memory_warning(*args: StarValue) -> StarValue:
        if args and isinstance(args[0], (StarFunction, StarBuiltinFunction)):
            fn = args[0]
            lifecycle.on_memory_warning(lambda: fn.call([]) if isinstance(fn, StarFunction) else fn.func())
        return StarNull()

    # Screen Metrics
    screen_exports: Dict[str, StarValue] = {
        "width_dp": StarBuiltinFunction("width_dp", lambda *args: StarDecimal(ScreenAPI.width_dp())),
        "height_dp": StarBuiltinFunction("height_dp", lambda *args: StarDecimal(ScreenAPI.height_dp())),
        "scale_factor": StarBuiltinFunction("scale_factor", lambda *args: StarDecimal(ScreenAPI.scale_factor())),
        "orientation": StarBuiltinFunction("orientation", lambda *args: StarText(ScreenAPI.orientation())),
        "rotate": StarBuiltinFunction("rotate", lambda *args: (
            _CURRENT_METRICS.rotate(args[0].to_string() if args else "toggle"),
            StarText(_CURRENT_METRICS.orientation)
        )[1])
    }
    exports["Screen"] = StarModule("Screen", screen_exports)

    # Storage APIs (Capability-Gated)
    storage_exports: Dict[str, StarValue] = {
        "set": StarBuiltinFunction("set", lambda *args: (
            StorageAPI.set(args[0].to_string(), args[1].to_string()) if len(args) >= 2 else None,
            StarNull()
        )[1]),
        "get": StarBuiltinFunction("get", lambda *args: (
            StarText(StorageAPI.get(args[0].to_string()) or "") if args and StorageAPI.get(args[0].to_string()) is not None else StarNull()
        )),
        "remove": StarBuiltinFunction("remove", lambda *args: (
            StorageAPI.remove(args[0].to_string()) if args else None,
            StarNull()
        )[1]),
        "clear": StarBuiltinFunction("clear", lambda *args: StarNull())
    }
    exports["Storage"] = StarModule("Storage", storage_exports)

    # Battery APIs (Capability-Gated)
    battery_exports: Dict[str, StarValue] = {
        "level": StarBuiltinFunction("level", lambda *args: StarDecimal(BatteryAPI.level())),
        "is_charging": StarBuiltinFunction("is_charging", lambda *args: StarBoolean(BatteryAPI.is_charging())),
        "power_save": StarBuiltinFunction("power_save", lambda *args: StarBoolean(False))
    }
    exports["Battery"] = StarModule("Battery", battery_exports)

    # Orientation APIs
    orientation_exports: Dict[str, StarValue] = {
        "current": StarBuiltinFunction("current", lambda *args: StarText(OrientationAPI.current())),
        "lock": StarBuiltinFunction("lock", lambda *args: (
            OrientationAPI.lock(args[0].to_string()) if args else None,
            StarText(OrientationAPI.current())
        )[1]),
        "unlock": StarBuiltinFunction("unlock", lambda *args: (
            OrientationAPI.unlock(),
            StarText(OrientationAPI.current())
        )[1])
    }
    exports["Orientation"] = StarModule("Orientation", orientation_exports)

    # Haptics & Vibration (Capability-Gated)
    def _vibrate(*args: StarValue) -> StarValue:
        pattern = int(args[0].value) if args and isinstance(args[0], (StarInteger, StarDecimal)) else 50
        DeviceProviderRegistry.get_provider().vibrate(pattern)
        return StarNull()

    haptics_exports: Dict[str, StarValue] = {
        "impact": StarBuiltinFunction("impact", lambda *args: (
            HapticsAPI.impact(args[0].to_string() if args else "medium"),
            StarNull()
        )[1]),
        "notification": StarBuiltinFunction("notification", lambda *args: (
            HapticsAPI.notification(args[0].to_string() if args else "success"),
            StarNull()
        )[1])
    }
    exports["Vibrate"] = StarBuiltinFunction("Vibrate", _vibrate)
    exports["Haptics"] = StarModule("Haptics", haptics_exports)

    # Clipboard APIs (Capability-Gated)
    clipboard_exports: Dict[str, StarValue] = {
        "set": StarBuiltinFunction("set", lambda *args: (
            ClipboardAPI.set(args[0].to_string()) if args else None,
            StarNull()
        )[1]),
        "get": StarBuiltinFunction("get", lambda *args: StarText(ClipboardAPI.get()))
    }
    exports["Clipboard"] = StarModule("Clipboard", clipboard_exports)

    # Share API
    share_exports: Dict[str, StarValue] = {
        "text": StarBuiltinFunction("text", lambda *args: StarBoolean(
            ShareAPI.text(args[0].to_string(), args[1].to_string() if len(args) > 1 else None) if args else False
        ))
    }
    exports["Share"] = StarModule("Share", share_exports)

    # Network API (Capability-Gated)
    network_exports: Dict[str, StarValue] = {
        "status": StarBuiltinFunction("status", lambda *args: StarText(NetworkAPI.status())),
        "is_connected": StarBuiltinFunction("is_connected", lambda *args: StarBoolean(NetworkAPI.is_connected()))
    }
    exports["Network"] = StarModule("Network", network_exports)

    # Bind Lifecycle Functions
    exports["on_resume"] = StarBuiltinFunction("on_resume", _on_resume)
    exports["on_pause"] = StarBuiltinFunction("on_pause", _on_pause)
    exports["on_back_press"] = StarBuiltinFunction("on_back_press", _on_back_press)
    exports["on_memory_warning"] = StarBuiltinFunction("on_memory_warning", _on_memory_warning)

    return StarModule("Mobile", exports)


__all__ = [
    "create_mobile_module",
    "get_current_metrics",
    "get_current_insets",
    "ScreenMetrics",
    "SafeAreaInsets",
    "StorageAPI",
    "BatteryAPI",
    "HapticsAPI",
    "ClipboardAPI",
    "ScreenAPI",
    "OrientationAPI",
    "ShareAPI",
    "NetworkAPI",
    "GeolocationAPI",
    "CameraAPI",
    "IDeviceProvider",
    "BaseSimulatedDeviceProvider",
    "WebDeviceProvider",
    "DesktopDeviceProvider",
    "AndroidDeviceProvider",
    "iOSDeviceProvider",
    "DeviceProviderRegistry"
]
