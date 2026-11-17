"""
Star 0.9.0 Release Candidate Certification Test Suite
Authoritative Reference: STAR_ABI.md & STAR_RELEASE.md
"""

import unittest
from star_runtime.abi import ABI_VERSION
from star_runtime.mobile.abi import MOBILE_ABI_VERSION
from star_runtime.mobile.isolation import RuntimeFaultBarrier
from star_backend.mobile.renderer import RenderCommandOptimizer, MobileDrawCommand
from star_runtime.mobile.abi import MobileRenderOp
from star_backend.mobile.certification import ReleaseCertificationEngine


class TestReleaseCandidate(unittest.TestCase):
    def test_abi_versions_locked(self):
        self.assertEqual(ABI_VERSION, 1)
        self.assertEqual(MOBILE_ABI_VERSION, 1)

    def test_runtime_fault_isolation(self):
        def crashing_op():
            raise RuntimeError("Simulated crash")

        result = RuntimeFaultBarrier.execute_safely("test_crash", crashing_op, fallback_val="recovered")
        self.assertEqual(result, "recovered")

    def test_render_command_optimizer_culling(self):
        commands = [
            MobileDrawCommand(MobileRenderOp.DRAW_CARD, 0, 0, 100, 100),
            MobileDrawCommand(MobileRenderOp.DRAW_CARD, 0, 2000, 100, 100) # Offscreen
        ]
        optimized = RenderCommandOptimizer.optimize(commands, viewport_w=390.0, viewport_h=844.0)
        self.assertEqual(len(optimized), 1)

    def test_full_release_candidate_certification(self):
        status = ReleaseCertificationEngine.certify("examples/mobile/benchmark.star")
        self.assertEqual(status, 0)


if __name__ == "__main__":
    unittest.main()
