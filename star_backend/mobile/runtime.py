"""
Star Mobile Unified Execution Runtime
Authoritative Reference: STAR_MOBILE_RUNTIME.md (Section 2)
"""

from typing import Optional, List, Dict, Any, Tuple
from star_engine.ir import CompiledModule
from star_engine.vm import StarVM
from star_engine.types import StarVirtualNode, StarValue
from star_engine.parser import Parser
from star_engine.lexer import Lexer
from star_engine.interpreter import Interpreter

from star_runtime.mobile.abi import MOBILE_ABI_VERSION, MobileRenderOp
from star_runtime.mobile.capabilities import CapabilityManager, MobileCapability
from star_sdk.mobile.dimensions import ScreenMetrics
from star_sdk.mobile.safe_area import SafeAreaInsets
from star_sdk.mobile.lifecycle import get_lifecycle, MobileLifecycle, LifecycleState
from star_backend.mobile.layout import MobileLayoutEngine, MobileLayoutNode
from star_backend.mobile.gesture_engine import GestureEngine, RecognizedGesture
from star_backend.mobile.event_bridge import MobileEventBridge
from star_backend.mobile.lifecycle_bridge import MobileLifecycleBridge
from star_backend.mobile.device_bridge import MobileDeviceBridge
from star_backend.mobile.renderer import (
    IMobileRenderer, MobileHeadlessRenderer, MobileCommandStreamGenerator, MobileDrawCommand
)
from star_backend.mobile.packaging import MobileBundle, MobilePackager


class MobileRuntime:
    """
    Core execution runtime hosting the Star VM, layout engine, render pipeline,
    gesture recognition, capability gating, and native OS event bridges.
    """
    def __init__(
        self,
        metrics: Optional[ScreenMetrics] = None,
        insets: Optional[SafeAreaInsets] = None,
        renderer: Optional[IMobileRenderer] = None,
        capabilities: Optional[CapabilityManager] = None
    ):
        self.metrics = metrics or ScreenMetrics()
        self.insets = insets or SafeAreaInsets()
        self.capabilities = capabilities or CapabilityManager(list(MobileCapability.ALL))
        self.renderer = renderer or MobileHeadlessRenderer()

        # Subsystem engines
        self.layout_engine = MobileLayoutEngine(self.metrics, self.insets)
        self.gesture_engine = GestureEngine()
        self.event_bridge = MobileEventBridge(self.gesture_engine)
        self.lifecycle_bridge = MobileLifecycleBridge()
        self.device_bridge = MobileDeviceBridge(self.capabilities)

        # Execution state
        self.current_bundle: Optional[MobileBundle] = None
        self.current_root_vnode: Optional[StarVirtualNode] = None
        self.current_layout: Optional[MobileLayoutNode] = None
        self.last_draw_commands: List[MobileDrawCommand] = []
        self.frame_count: int = 0

    def load_bundle_from_file(self, bundle_path: str) -> None:
        packager = MobilePackager()
        bundle = packager.load_bundle(bundle_path)
        self.load_bundle(bundle)

    def load_bundle(self, bundle: MobileBundle) -> None:
        self.current_bundle = bundle
        # Configure capabilities from manifest
        self.capabilities = CapabilityManager(bundle.manifest.permissions)
        self.device_bridge = MobileDeviceBridge(self.capabilities)

        # Deserialize bytecode and execute initial frame
        result = None
        try:
            compiled_module = CompiledModule.deserialize(bundle.bytecode_bytes)
            vm = StarVM(compiled_module)
            result = vm.run()
        except Exception:
            result = None

        if isinstance(result, StarVirtualNode):
            self.render_node(result)
        elif bundle.source_code:
            # Fallback to source interpreter if root node returned
            interp = Interpreter(filename=bundle.manifest.entry)
            lexer = Lexer(bundle.source_code, filename=bundle.manifest.entry)
            parser = Parser(lexer.tokenize(), source_code=bundle.source_code, filename=bundle.manifest.entry)
            root_v = interp.interpret(parser.parse())
            if isinstance(root_v, StarVirtualNode):
                self.render_node(root_v)

    def render_node(self, vnode: StarVirtualNode) -> List[MobileDrawCommand]:
        """Calculates layout and executes a complete render frame dispatch."""
        self.current_root_vnode = vnode
        self.current_layout = self.layout_engine.compute_layout(vnode)
        self.event_bridge.attach_layout(self.current_layout, self.layout_engine)

        # Generate draw commands
        commands = MobileCommandStreamGenerator.generate(self.current_layout)
        self.last_draw_commands = commands

        # Dispatch to renderer
        self.renderer.begin_frame(self.metrics.width_dp, self.metrics.height_dp)
        for cmd in commands:
            self.renderer.execute_command(cmd)
        self.renderer.end_frame()

        self.frame_count += 1
        return commands

    def dispatch_touch(
        self,
        phase_str: str,
        pointer_id: int,
        x: float,
        y: float,
        pressure: float = 1.0
    ) -> List[RecognizedGesture]:
        gestures = self.event_bridge.handle_native_touch(
            phase_str=phase_str,
            pointer_id=pointer_id,
            x=x,
            y=y,
            pressure=pressure
        )
        return gestures

    def rotate_display(self, mode: str = "toggle") -> None:
        self.metrics.rotate(mode)
        self.layout_engine = MobileLayoutEngine(self.metrics, self.insets)
        if self.current_root_vnode:
            self.render_node(self.current_root_vnode)
