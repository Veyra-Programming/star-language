"""
Star iOS Native Backend Subsystem
Authoritative Reference: STAR_IOS.md
"""

from star_backend.mobile.ios.swift_bridge import SwiftNativeBridge
from star_backend.mobile.ios.view_controller import StarViewController
from star_backend.mobile.ios.metal_renderer import iOSMetalRenderer
from star_backend.mobile.ios.touch_bridge import iOSTouchBridge, iOSUITouchPhase
from star_backend.mobile.ios.device_bridge import iOSDeviceBridge
from star_backend.mobile.ios.xcode_generator import XcodeProjectGenerator
from star_backend.mobile.ios.builder import iOSBuilder

__all__ = [
    "SwiftNativeBridge",
    "StarViewController",
    "iOSMetalRenderer",
    "iOSTouchBridge",
    "iOSUITouchPhase",
    "iOSDeviceBridge",
    "XcodeProjectGenerator",
    "iOSBuilder"
]
