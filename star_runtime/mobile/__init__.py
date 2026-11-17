"""
Star Runtime Mobile ABI & Capability Subsystem
Authoritative Reference: STAR_MOBILE_RUNTIME.md
"""

from star_runtime.mobile.abi import (
    MOBILE_ABI_VERSION, MOBILE_ABI_MAGIC, MobileRenderOp, MobileABI
)
from star_runtime.mobile.capabilities import (
    MobileCapability, CapabilityManager, CapabilitySecurityError
)

__all__ = [
    "MOBILE_ABI_VERSION",
    "MOBILE_ABI_MAGIC",
    "MobileRenderOp",
    "MobileABI",
    "MobileCapability",
    "CapabilityManager",
    "CapabilitySecurityError"
]
