"""
Star WebGPU Pipeline & Render Pass State
Authoritative Reference: STAR_WEBGPU.md (Section 3)
"""

from typing import Dict, Any, List
from star_backend.webgpu.shaders import UI_VERTEX_SHADER, UI_FRAGMENT_SDF_SHADER, BLUR_COMPUTE_SHADER


class WebGPUPipeline:
    """
    Manages WebGPU pipeline layouts, vertex buffers, and bind groups.
    """

    def __init__(self, width: int = 390, height: int = 844, scale: float = 3.0):
        self.width = width
        self.height = height
        self.scale = scale
        self.vertex_shader_source = UI_VERTEX_SHADER
        self.fragment_shader_source = UI_FRAGMENT_SDF_SHADER
        self.blur_shader_source = BLUR_COMPUTE_SHADER
        self.is_initialized = True

    def get_pipeline_descriptor(self) -> Dict[str, Any]:
        return {
            "layout": "auto",
            "vertex": {
                "module": "vs_main",
                "buffers": [
                    {
                        "arrayStride": 32, # 2 floats pos, 2 floats uv, 4 floats color
                        "stepMode": "vertex",
                        "attributes": [
                            {"format": "float32x2", "offset": 0, "shaderLocation": 0},
                            {"format": "float32x2", "offset": 8, "shaderLocation": 1},
                            {"format": "float32x4", "offset": 16, "shaderLocation": 2}
                        ]
                    }
                ]
            },
            "fragment": {
                "module": "fs_main",
                "targets": [{"format": "bgra8unorm"}]
            },
            "primitive": {
                "topology": "triangle-list",
                "cullMode": "none"
            }
        }
