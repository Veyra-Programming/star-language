"""
Star Mobile Hardware Verification Subsystem
Authoritative Reference: STAR_HARDWARE.md
"""

from star_backend.mobile.hardware.device import (
    MobileDevice, DevicePlatform, DeviceExecutionMode, DeviceCapabilities
)
from star_backend.mobile.hardware.discovery import DeviceDiscoveryManager
from star_backend.mobile.hardware.probes import HardwareProbeSuite, ProbeResult, ProbeResultStatus
from star_backend.mobile.hardware.session import HardwareVerificationSession
from star_backend.mobile.hardware.metrics import HardwarePerformanceMetrics, PerformanceProfiler
from star_backend.mobile.hardware.recorder import HardwareSessionRecorder
from star_backend.mobile.hardware.runner import HardwareTestRunner

__all__ = [
    "MobileDevice",
    "DevicePlatform",
    "DeviceExecutionMode",
    "DeviceCapabilities",
    "DeviceDiscoveryManager",
    "HardwareProbeSuite",
    "ProbeResult",
    "ProbeResultStatus",
    "HardwareVerificationSession",
    "HardwarePerformanceMetrics",
    "PerformanceProfiler",
    "HardwareSessionRecorder",
    "HardwareTestRunner"
]
