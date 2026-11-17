"""
Star WebGPU Acceleration Subsystem
Authoritative Reference: STAR_WEBGPU.md
"""

from star_backend.webgpu.shaders import UI_VERTEX_SHADER, UI_FRAGMENT_SDF_SHADER, BLUR_COMPUTE_SHADER
from star_backend.webgpu.pipeline import WebGPUPipeline
from star_backend.webgpu.renderer import WebGPURenderer

__all__ = [
    "UI_VERTEX_SHADER",
    "UI_FRAGMENT_SDF_SHADER",
    "BLUR_COMPUTE_SHADER",
    "WebGPUPipeline",
    "WebGPURenderer"
]
