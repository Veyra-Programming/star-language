"""
Star Mobile Hardware Discovery Manager
Authoritative Reference: STAR_HARDWARE.md (Section 2)
"""

import os
import subprocess
import shutil
import re
from typing import List, Dict, Any, Optional
from star_backend.mobile.hardware.device import (
    MobileDevice, DevicePlatform, DeviceExecutionMode, DeviceCapabilities
)
from star_sdk.mobile.dimensions import ScreenMetrics
from star_sdk.mobile.safe_area import SafeAreaInsets


class DeviceDiscoveryManager:
    """
    Discovers physical and emulated mobile devices via ADB and Apple xcrun.
    """

    @classmethod
    def _get_adb_binary(cls) -> Optional[str]:
        if shutil.which("adb"):
            return "adb"
        try:
            from star_backend.mobile.android.sdk import AndroidSDK
            sdk = AndroidSDK.find_sdk()
            if sdk and sdk.has_adb and sdk.adb_path and os.path.exists(sdk.adb_path):
                return sdk.adb_path
        except Exception:
            pass
        # Common locations on Windows
        for p in (r"E:\platform-tools-latest-windows\platform-tools\adb.exe",
                  r"C:\platform-tools\adb.exe",
                  r"E:\platform-tools\adb.exe"):
            if os.path.exists(p):
                return p
        return None

    @classmethod
    def discover_android_devices(cls) -> List[MobileDevice]:
        devices = []
        adb_bin = cls._get_adb_binary()
        if not adb_bin:
            return devices

        try:
            res = subprocess.run([adb_bin, "devices", "-l"], capture_output=True, text=True, timeout=6)
            lines = res.stdout.strip().splitlines()
            for line in lines[1:]: # Skip header
                line = line.strip()
                if not line or "offline" in line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    dev_id = parts[0]
                    status = parts[1].lower()
                    mode = DeviceExecutionMode.EMULATOR if "emulator" in dev_id else DeviceExecutionMode.PHYSICAL
                    model = "Android Device"
                    for p in parts[2:]:
                        if p.startswith("model:"):
                            model = p.split(":", 1)[1]
                    
                    if status != "device":
                        model = f"{model} [{status.upper()} - Unlock screen & tap Allow]"

                    devices.append(MobileDevice(
                        device_id=dev_id,
                        platform=DevicePlatform.ANDROID,
                        mode=mode,
                        model=model,
                        os_version="Android 14/15",
                        metrics=ScreenMetrics(width_dp=412.0, height_dp=915.0, density_scale=2.625),
                        insets=SafeAreaInsets(top=48.0, bottom=24.0, left=0.0, right=0.0)
                    ))
        except Exception:
            pass

        return devices

    @classmethod
    def discover_ios_devices(cls) -> List[MobileDevice]:
        devices = []
        if not shutil.which("xcrun"):
            return devices

        try:
            res = subprocess.run(["xcrun", "simctl", "list", "devices", "booted"], capture_output=True, text=True, timeout=2)
            lines = res.stdout.strip().splitlines()
            for line in lines:
                line = line.strip()
                match = re.search(r"([A-Za-z0-9\s]+)\s+\(([A-F0-9\-]+)\)\s+\(Booted\)", line)
                if match:
                    name, udid = match.group(1), match.group(2)
                    devices.append(MobileDevice(
                        device_id=udid,
                        platform=DevicePlatform.IOS,
                        mode=DeviceExecutionMode.EMULATOR,
                        model=name.strip(),
                        os_version="iOS 17.x",
                        metrics=ScreenMetrics(width_dp=393.0, height_dp=852.0, density_scale=3.0),
                        insets=SafeAreaInsets(top=59.0, bottom=34.0, left=0.0, right=0.0)
                    ))
        except Exception:
            pass

        return devices

    @classmethod
    def discover_all(cls, include_simulated: bool = True) -> List[MobileDevice]:
        discovered = cls.discover_android_devices() + cls.discover_ios_devices()

        if include_simulated:
            # Provide high-fidelity simulated hardware baselines for headless/CI runs
            sim_android = MobileDevice(
                device_id="sim-android-pixel8",
                platform=DevicePlatform.ANDROID,
                mode=DeviceExecutionMode.SIMULATED,
                model="Pixel 8 (Verified Baseline)",
                os_version="Android 14.0",
                metrics=ScreenMetrics(width_dp=412.0, height_dp=915.0, density_scale=2.625),
                insets=SafeAreaInsets(top=48.0, bottom=24.0, left=0.0, right=0.0)
            )
            sim_ios = MobileDevice(
                device_id="sim-ios-iphone15pro",
                platform=DevicePlatform.IOS,
                mode=DeviceExecutionMode.SIMULATED,
                model="iPhone 15 Pro (Verified Baseline)",
                os_version="iOS 17.4",
                metrics=ScreenMetrics(width_dp=393.0, height_dp=852.0, density_scale=3.0),
                insets=SafeAreaInsets(top=59.0, bottom=34.0, left=0.0, right=0.0)
            )
            existing_ids = {d.device_id for d in discovered}
            for sim in (sim_android, sim_ios):
                if sim.device_id not in existing_ids:
                    discovered.append(sim)

        return discovered
