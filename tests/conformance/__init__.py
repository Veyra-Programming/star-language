"""
Star Cross-Platform Conformance Test Suite
Authoritative Reference: STAR_CONFORMANCE.md
"""

from star_sdk.mobile.device_apis import (
    WebDeviceProvider, DesktopDeviceProvider, AndroidDeviceProvider, iOSDeviceProvider
)

ALL_PROVIDERS = [
    ("Web", WebDeviceProvider),
    ("Desktop", DesktopDeviceProvider),
    ("Android", AndroidDeviceProvider),
    ("iOS", iOSDeviceProvider)
]
