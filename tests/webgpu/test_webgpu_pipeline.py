"""
Unit Tests for Star WebGPU Acceleration Engine
"""

import unittest
from star_backend.webgpu.shaders import UI_VERTEX_SHADER, UI_FRAGMENT_SDF_SHADER, BLUR_COMPUTE_SHADER
from star_backend.webgpu.pipeline import WebGPUPipeline
from star_backend.webgpu.renderer import WebGPURenderer
from star_backend.mobile.renderer import RenderCommand


class TestWebGPUPipeline(unittest.TestCase):
    def test_wgsl_shader_integrity(self):
        self.assertIn("@vertex", UI_VERTEX_SHADER)
        self.assertIn("@fragment", UI_FRAGMENT_SDF_SHADER)
        self.assertIn("@compute", BLUR_COMPUTE_SHADER)

    def test_pipeline_descriptor(self):
        pipeline = WebGPUPipeline(390, 844)
        desc = pipeline.get_pipeline_descriptor()
        self.assertEqual(desc["layout"], "auto")
        self.assertEqual(desc["primitive"]["topology"], "triangle-list")

    def test_webgpu_render_frame_batching(self):
        renderer = WebGPURenderer(390, 844)
        cmds = [
            RenderCommand(0x71, [0, 0, 390, 100]), # draw_rect
            RenderCommand(0x71, [0, 100, 390, 200]),
            RenderCommand(0x73, [50, 50, 0, 0], "Click Me") # draw_text
        ]
        res = renderer.render_frame(cmds)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["gpu_render_passes"], 1)
        self.assertEqual(res["instanced_batches"], 2)


if __name__ == "__main__":
    unittest.main()
