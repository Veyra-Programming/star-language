"""
Star OmniEngine 2.0 GN (Generation Next) — Universal Execution, Parallel Fibers & Polyglot Compute Grid
Authoritative Reference: STAR_OMNI_SPEC.md
"""

from star_engine.omni.jit import TieredJITEngine, HotspotProfile
from star_engine.omni.fiber import FiberScheduler, OmniFiber, OmniChannel, FiberState
from star_engine.omni.memory import ArenaAllocator, BorrowedBuffer
from star_engine.omni.grid import OmniCluster, OmniNode
from star_engine.omni.ffi import PolyglotFFIEngine, NativeFunctionWrapper

__all__ = [
    "TieredJITEngine",
    "HotspotProfile",
    "FiberScheduler",
    "OmniFiber",
    "OmniChannel",
    "FiberState",
    "ArenaAllocator",
    "BorrowedBuffer",
    "OmniCluster",
    "OmniNode",
    "PolyglotFFIEngine",
    "NativeFunctionWrapper",
]
