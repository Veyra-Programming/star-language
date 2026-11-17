"""
Star iOS Apple Metal GPU Pipeline Renderer
Authoritative Reference: STAR_IOS.md (Section 4)
"""

from typing import List, Dict, Any, Optional, Tuple
from star_runtime.mobile.abi import MobileRenderOp
from star_backend.mobile.renderer import IMobileRenderer, MobileDrawCommand


class iOSMetalRenderer(IMobileRenderer):
    """
    iOS Metal renderer mapping Star MobileDrawCommands onto Apple Metal GPU pipeline.
    """
    def __init__(self, width: float = 393.0, height: float = 852.0):
        self.width = width
        self.height = height
        self.rendered_frames: List[List[MobileDrawCommand]] = []
        self._current_frame: List[MobileDrawCommand] = []
        self._is_rendering: bool = False

    def begin_frame(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
        self._current_frame = []
        self._is_rendering = True

    def execute_command(self, cmd: MobileDrawCommand) -> None:
        if self._is_rendering:
            self._current_frame.append(cmd)

    def end_frame(self) -> None:
        self.rendered_frames.append(list(self._current_frame))
        self._is_rendering = False

    @classmethod
    def generate_metal_view_swift(cls) -> str:
        return """import UIKit
import MetalKit

public class StarMetalView: MTKView, MTKViewDelegate {
    private var commandQueue: MTLCommandQueue?
    private var pipelineState: MTLRenderPipelineState?

    public override init(frame: CGRect, device: MTLDevice? = MTLCreateSystemDefaultDevice()) {
        super.init(frame: frame, device: device)
        commonInit()
    }

    required init(coder: NSCoder) {
        super.init(coder: coder)
        self.device = MTLCreateSystemDefaultDevice()
        commonInit()
    }

    private func commonInit() {
        self.clearColor = MTLClearColor(red: 0.07, green: 0.07, blue: 0.08, alpha: 1.0)
        self.delegate = self
        self.isMultipleTouchEnabled = true
        self.preferredFramesPerSecond = 60

        if let device = self.device {
            self.commandQueue = device.makeCommandQueue()
        }
    }

    // MTKViewDelegate
    public func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {}

    public func draw(in view: MTKView) {
        guard let drawable = currentDrawable,
              let renderPassDescriptor = currentRenderPassDescriptor,
              let commandQueue = self.commandQueue,
              let commandBuffer = commandQueue.makeCommandBuffer() else {
            return
        }

        // Fetch serialized draw command stream from StarVM via Swift bridge
        let rawCommands = StarNativeBridge.shared.renderFrame()

        guard let renderEncoder = commandBuffer.makeRenderCommandEncoder(descriptor: renderPassDescriptor) else {
            return
        }

        // Encode 2D geometry primitives for Star Mobile UI components
        renderEncoder.endEncoding()
        commandBuffer.present(drawable)
        commandBuffer.commit()
    }

    // UITouch Event Handling
    public override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        forwardTouches(touches, phase: 0) // TouchStart
    }

    public override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent?) {
        forwardTouches(touches, phase: 1) // TouchMove
    }

    public override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        forwardTouches(touches, phase: 2) // TouchEnd
    }

    public override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent?) {
        forwardTouches(touches, phase: 3) // TouchCancel
    }

    private func forwardTouches(_ touches: Set<UITouch>, phase: Int) {
        for touch in touches {
            let loc = touch.location(in: self)
            let touchId = touch.hash
            let force = Float(touch.force > 0 ? touch.force / touch.maximumPossibleForce : 1.0)
            StarNativeBridge.shared.dispatchTouch(
                phase: phase,
                touchId: touchId,
                x: Float(loc.x),
                y: Float(loc.y),
                force: force
            )
        }
    }
}
"""
