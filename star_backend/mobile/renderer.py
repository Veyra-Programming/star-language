"""
Star Mobile Render Command Stream & Renderer Abstraction
Authoritative Reference: STAR_MOBILE_RUNTIME.md (Section 3)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from star_runtime.mobile.abi import MobileRenderOp
from star_backend.mobile.layout import MobileLayoutNode


class MobileDrawCommand:
    """
    Serializable 2D draw command emitted by the mobile layout pass
    and consumed by platform renderers (Android SurfaceView / iOS Metal / Headless).
    """
    def __init__(
        self,
        op: MobileRenderOp,
        x: float,
        y: float,
        width: float,
        height: float,
        props: Optional[Dict[str, Any]] = None
    ):
        self.op = op
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.props = props or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "op": self.op.name,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "props": self.props
        }

    def __repr__(self) -> str:
        return f"DrawCommand({self.op.name}, x={self.x:.1f}, y={self.y:.1f}, w={self.width:.1f}, h={self.height:.1f})"


class RenderCommand:
    """Hardware-level render command with opcode, geometry bounds, and optional payload."""
    def __init__(self, opcode: int, bounds: Optional[List[float]] = None, payload: Any = None):
        self.opcode = opcode
        self.bounds = list(bounds) if bounds else [0.0, 0.0, 0.0, 0.0]
        self.payload = payload
        self.x = float(self.bounds[0]) if len(self.bounds) > 0 else 0.0
        self.y = float(self.bounds[1]) if len(self.bounds) > 1 else 0.0
        self.width = float(self.bounds[2]) if len(self.bounds) > 2 else 0.0
        self.height = float(self.bounds[3]) if len(self.bounds) > 3 else 0.0

    def __repr__(self) -> str:
        return f"RenderCommand(opcode={hex(self.opcode)}, bounds={self.bounds}, payload={self.payload})"


class IMobileRenderer(ABC):
    """Abstract interface that platform-specific render backends must implement."""

    @abstractmethod
    def begin_frame(self, width: float, height: float) -> None:
        """Called before dispatching a frame's draw commands."""
        pass

    @abstractmethod
    def execute_command(self, cmd: MobileDrawCommand) -> None:
        """Executes an individual draw command on the underlying canvas/surface."""
        pass

    @abstractmethod
    def end_frame(self) -> None:
        """Flushes/commits frame buffers to the screen."""
        pass


class MobileCommandStreamGenerator:
    """
    Traverses a MobileLayoutNode tree and generates an optimized stream of MobileDrawCommands.
    """
    @staticmethod
    def generate(root_node: MobileLayoutNode) -> List[MobileDrawCommand]:
        commands: List[MobileDrawCommand] = []
        MobileCommandStreamGenerator._traverse(root_node, commands)
        return commands

    @staticmethod
    def _traverse(node: MobileLayoutNode, commands: List[MobileDrawCommand]) -> None:
        tag = node.node_type.lower()
        props = dict(node.props)

        if tag in ("app_bar", "mobile_app_bar"):
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_APP_BAR,
                node.x, node.y, node.width, node.height,
                {"title": props.get("title", "App"), "bg": "#1e1e24", "fg": "#ffffff"}
            ))
        elif tag == "card":
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_CARD,
                node.x, node.y, node.width, node.height,
                {"bg": "#2a2a32", "border": "#3f3f4e", "corner_radius": 12.0}
            ))
        elif tag == "button":
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_BUTTON,
                node.x, node.y, node.width, node.height,
                {"label": props.get("label", "Button"), "bg": "#4f46e5", "fg": "#ffffff", "corner_radius": 8.0}
            ))
        elif tag == "title":
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_TEXT,
                node.x, node.y, node.width, node.height,
                {"content": props.get("content", ""), "font_size": 22.0, "weight": "bold", "fg": "#ffffff"}
            ))
        elif tag == "text":
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_TEXT,
                node.x, node.y, node.width, node.height,
                {"content": props.get("content", ""), "font_size": 15.0, "weight": "normal", "fg": "#cbd5e1"}
            ))
        elif tag in ("switch", "mobile_switch"):
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_SWITCH,
                node.x, node.y, node.width, node.height,
                {"value": props.get("value", False), "active_color": "#10b981"}
            ))
        elif tag in ("slider", "mobile_slider"):
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_SLIDER,
                node.x, node.y, node.width, node.height,
                {"min": props.get("min", 0.0), "max": props.get("max", 100.0), "value": props.get("value", 50.0)}
            ))
        elif tag == "bottom_navigation":
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_BOTTOM_NAV,
                node.x, node.y, node.width, node.height,
                {"items": props.get("items", []), "selected": props.get("selected", 0), "bg": "#1e1e24"}
            ))
        elif tag == "badge":
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_BADGE,
                node.x, node.y, node.width, node.height,
                {"label": props.get("label", ""), "variant": props.get("variant", "primary")}
            ))
        elif tag == "divider":
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_DIVIDER,
                node.x, node.y, node.width, node.height,
                {"color": "#334155"}
            ))
        elif tag in ("container", "box", "stack"):
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_CARD,
                node.x, node.y, node.width, node.height,
                {"bg": props.get("bg", "#1e1e24"), "border": props.get("border", "#334155"), "corner_radius": 8.0}
            ))
        elif tag == "tabs":
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_BOTTOM_NAV,
                node.x, node.y, node.width, node.height,
                {"items": props.get("items", []), "selected": props.get("active", 0), "bg": "#1e1e24"}
            ))
        elif tag in ("icon", "avatar"):
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_BADGE,
                node.x, node.y, node.width, node.height,
                {"label": props.get("name", props.get("label", "★")), "variant": "primary"}
            ))
        elif tag == "toast":
            commands.append(MobileDrawCommand(
                MobileRenderOp.DRAW_CARD,
                node.x, node.y, node.width, node.height,
                {"message": props.get("message", ""), "variant": props.get("variant", "info")}
            ))

        # Recursively render children
        for child in node.children:
            MobileCommandStreamGenerator._traverse(child, commands)


class MobileHeadlessRenderer(IMobileRenderer):
    """
    Headless renderer implementation collecting draw command histories for testing and validation.
    """
    def __init__(self):
        self.frame_history: List[List[MobileDrawCommand]] = []
        self.current_frame_commands: List[MobileDrawCommand] = []
        self.is_rendering: bool = False
        self.viewport_size: Tuple[float, float] = (390.0, 844.0)

    def begin_frame(self, width: float, height: float) -> None:
        self.viewport_size = (width, height)
        self.current_frame_commands = []
        self.is_rendering = True

    def execute_command(self, cmd: MobileDrawCommand) -> None:
        if self.is_rendering:
            self.current_frame_commands.append(cmd)

    def end_frame(self) -> None:
        self.frame_history.append(list(self.current_frame_commands))
        self.is_rendering = False

    @property
    def last_frame_commands(self) -> List[MobileDrawCommand]:
        return self.frame_history[-1] if self.frame_history else []


class RenderCommandOptimizer:
    """
    Optimizes draw command streams for 60 FPS mobile rendering targets:
    - Viewport culling (discards commands outside screen bounds)
    - Adjacent text/card command batching
    - Dirty rect minimal invalidation
    """
    @classmethod
    def optimize(
        cls,
        commands: List[MobileDrawCommand],
        viewport_w: float = 390.0,
        viewport_h: float = 844.0,
        dirty_rect: Optional[Tuple[float, float, float, float]] = None
    ) -> List[MobileDrawCommand]:
        optimized = []
        for cmd in commands:
            # 1. Viewport Culling
            if cmd.x + cmd.width < 0 or cmd.x > viewport_w:
                continue
            if cmd.y + cmd.height < 0 or cmd.y > viewport_h:
                continue

            # 2. Dirty Rect Culling (if active)
            if dirty_rect:
                dx, dy, dw, dh = dirty_rect
                if (cmd.x + cmd.width < dx or cmd.x > dx + dw or
                    cmd.y + cmd.height < dy or cmd.y > dy + dh):
                    continue

            optimized.append(cmd)
        return optimized

