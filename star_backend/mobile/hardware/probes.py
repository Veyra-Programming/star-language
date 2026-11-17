"""
Star Mobile Hardware Probes Subsystem
Authoritative Reference: STAR_HARDWARE.md (Section 3)
"""

import time
from enum import Enum
from typing import Dict, Any, Optional, List
from star_backend.mobile.hardware.device import MobileDevice
from star_sdk.mobile.device_apis import (
    StorageAPI, BatteryAPI, HapticsAPI, ClipboardAPI,
    ScreenAPI, OrientationAPI, NetworkAPI, CameraAPI, GeolocationAPI
)
from star_runtime.mobile.capabilities import CapabilitySecurityError


class ProbeResultStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    UNAVAILABLE = "UNAVAILABLE"
    FAILED = "FAILED"


class ProbeResult:
    def __init__(
        self,
        capability: str,
        status: ProbeResultStatus,
        value: Any = None,
        latency_ms: float = 0.0,
        error_message: Optional[str] = None
    ):
        self.capability = capability
        self.status = status
        self.value = value
        self.latency_ms = latency_ms
        self.error_message = error_message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capability": self.capability,
            "status": self.status.value,
            "value": self.value,
            "latency_ms": round(self.latency_ms, 2),
            "error_message": self.error_message
        }


class StorageProbe:
    @staticmethod
    def run() -> ProbeResult:
        start = time.perf_counter()
        try:
            StorageAPI.set("__probe_key__", "star_probe_val")
            val = StorageAPI.get("__probe_key__")
            StorageAPI.remove("__probe_key__")
            latency = (time.perf_counter() - start) * 1000.0
            if val == "star_probe_val":
                return ProbeResult("storage", ProbeResultStatus.SUPPORTED, value="Read/Write Verified", latency_ms=latency)
            return ProbeResult("storage", ProbeResultStatus.FAILED, error_message="Value mismatch", latency_ms=latency)
        except CapabilitySecurityError:
            return ProbeResult("storage", ProbeResultStatus.PERMISSION_DENIED, latency_ms=(time.perf_counter() - start) * 1000.0)
        except Exception as e:
            return ProbeResult("storage", ProbeResultStatus.FAILED, error_message=str(e), latency_ms=(time.perf_counter() - start) * 1000.0)


class BatteryProbe:
    @staticmethod
    def run() -> ProbeResult:
        start = time.perf_counter()
        try:
            level = BatteryAPI.level()
            charging = BatteryAPI.is_charging()
            latency = (time.perf_counter() - start) * 1000.0
            return ProbeResult("battery", ProbeResultStatus.SUPPORTED, value={"level": level, "charging": charging}, latency_ms=latency)
        except CapabilitySecurityError:
            return ProbeResult("battery", ProbeResultStatus.PERMISSION_DENIED, latency_ms=(time.perf_counter() - start) * 1000.0)
        except Exception as e:
            return ProbeResult("battery", ProbeResultStatus.FAILED, error_message=str(e), latency_ms=(time.perf_counter() - start) * 1000.0)


class HapticsProbe:
    @staticmethod
    def run() -> ProbeResult:
        start = time.perf_counter()
        try:
            HapticsAPI.impact("medium")
            HapticsAPI.notification("success")
            latency = (time.perf_counter() - start) * 1000.0
            return ProbeResult("haptics", ProbeResultStatus.SUPPORTED, value="Impact & Notification Executed", latency_ms=latency)
        except CapabilitySecurityError:
            return ProbeResult("haptics", ProbeResultStatus.PERMISSION_DENIED, latency_ms=(time.perf_counter() - start) * 1000.0)
        except Exception as e:
            return ProbeResult("haptics", ProbeResultStatus.FAILED, error_message=str(e), latency_ms=(time.perf_counter() - start) * 1000.0)


class ClipboardProbe:
    @staticmethod
    def run() -> ProbeResult:
        start = time.perf_counter()
        try:
            ClipboardAPI.set("Star Hardware Probe")
            val = ClipboardAPI.get()
            latency = (time.perf_counter() - start) * 1000.0
            return ProbeResult("clipboard", ProbeResultStatus.SUPPORTED, value=val, latency_ms=latency)
        except CapabilitySecurityError:
            return ProbeResult("clipboard", ProbeResultStatus.PERMISSION_DENIED, latency_ms=(time.perf_counter() - start) * 1000.0)
        except Exception as e:
            return ProbeResult("clipboard", ProbeResultStatus.FAILED, error_message=str(e), latency_ms=(time.perf_counter() - start) * 1000.0)


class ScreenProbe:
    @staticmethod
    def run() -> ProbeResult:
        start = time.perf_counter()
        try:
            w = ScreenAPI.width_dp()
            h = ScreenAPI.height_dp()
            scale = ScreenAPI.scale_factor()
            orientation = ScreenAPI.orientation()
            latency = (time.perf_counter() - start) * 1000.0
            return ProbeResult("screen", ProbeResultStatus.SUPPORTED, value={
                "width_dp": w,
                "height_dp": h,
                "scale_factor": scale,
                "orientation": orientation
            }, latency_ms=latency)
        except Exception as e:
            return ProbeResult("screen", ProbeResultStatus.FAILED, error_message=str(e), latency_ms=(time.perf_counter() - start) * 1000.0)


class OrientationProbe:
    @staticmethod
    def run() -> ProbeResult:
        start = time.perf_counter()
        try:
            current = OrientationAPI.current()
            OrientationAPI.lock("landscape")
            OrientationAPI.unlock()
            latency = (time.perf_counter() - start) * 1000.0
            return ProbeResult("orientation", ProbeResultStatus.SUPPORTED, value={"initial": current, "lockable": True}, latency_ms=latency)
        except Exception as e:
            return ProbeResult("orientation", ProbeResultStatus.FAILED, error_message=str(e), latency_ms=(time.perf_counter() - start) * 1000.0)


class NetworkProbe:
    @staticmethod
    def run() -> ProbeResult:
        start = time.perf_counter()
        try:
            status = NetworkAPI.status()
            latency = (time.perf_counter() - start) * 1000.0
            return ProbeResult("network", ProbeResultStatus.SUPPORTED, value={"state": status}, latency_ms=latency)
        except CapabilitySecurityError:
            return ProbeResult("network", ProbeResultStatus.PERMISSION_DENIED, latency_ms=(time.perf_counter() - start) * 1000.0)
        except Exception as e:
            return ProbeResult("network", ProbeResultStatus.FAILED, error_message=str(e), latency_ms=(time.perf_counter() - start) * 1000.0)


class CameraProbe:
    @staticmethod
    def run() -> ProbeResult:
        start = time.perf_counter()
        try:
            ready = CameraAPI.is_available()
            latency = (time.perf_counter() - start) * 1000.0
            status = ProbeResultStatus.SUPPORTED if ready else ProbeResultStatus.UNAVAILABLE
            return ProbeResult("camera", status, value={"available": ready}, latency_ms=latency)
        except CapabilitySecurityError:
            return ProbeResult("camera", ProbeResultStatus.PERMISSION_DENIED, latency_ms=(time.perf_counter() - start) * 1000.0)
        except Exception as e:
            return ProbeResult("camera", ProbeResultStatus.FAILED, error_message=str(e), latency_ms=(time.perf_counter() - start) * 1000.0)


class GeolocationProbe:
    @staticmethod
    def run() -> ProbeResult:
        start = time.perf_counter()
        try:
            ready = GeolocationAPI.is_available()
            latency = (time.perf_counter() - start) * 1000.0
            status = ProbeResultStatus.SUPPORTED if ready else ProbeResultStatus.UNAVAILABLE
            return ProbeResult("geolocation", status, value={"available": ready}, latency_ms=latency)
        except CapabilitySecurityError:
            return ProbeResult("geolocation", ProbeResultStatus.PERMISSION_DENIED, latency_ms=(time.perf_counter() - start) * 1000.0)
        except Exception as e:
            return ProbeResult("geolocation", ProbeResultStatus.FAILED, error_message=str(e), latency_ms=(time.perf_counter() - start) * 1000.0)


class HardwareProbeSuite:
    """Runs all standardized hardware capability probes."""
    @classmethod
    def run_all(cls) -> List[ProbeResult]:
        return [
            StorageProbe.run(),
            BatteryProbe.run(),
            HapticsProbe.run(),
            ClipboardProbe.run(),
            ScreenProbe.run(),
            OrientationProbe.run(),
            NetworkProbe.run(),
            CameraProbe.run(),
            GeolocationProbe.run()
        ]
