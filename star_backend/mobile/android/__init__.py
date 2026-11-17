"""
Star Android Native Backend Subsystem
Authoritative Reference: STAR_ANDROID.md
"""

from star_backend.mobile.android.jni_bridge import AndroidJNIBridge
from star_backend.mobile.android.activity import StarActivity
from star_backend.mobile.android.surface_renderer import AndroidSurfaceRenderer
from star_backend.mobile.android.input_bridge import AndroidInputBridge, AndroidMotionEventAction
from star_backend.mobile.android.device_bridge import AndroidDeviceBridge
from star_backend.mobile.android.project_generator import AndroidProjectGenerator
from star_backend.mobile.android.signing import AndroidSigner, AndroidSigningConfig, AndroidSigningError
from star_backend.mobile.android.builder import AndroidBuilder

__all__ = [
    "AndroidJNIBridge",
    "StarActivity",
    "AndroidSurfaceRenderer",
    "AndroidInputBridge",
    "AndroidMotionEventAction",
    "AndroidDeviceBridge",
    "AndroidProjectGenerator",
    "AndroidSigner",
    "AndroidSigningConfig",
    "AndroidSigningError",
    "AndroidBuilder"
]
