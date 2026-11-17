"""
Star Mobile 2D Layout & Hit-Testing Engine
Authoritative Reference: STAR_MOBILE.md (Section 5 & 6)
"""

from typing import List, Dict, Any, Optional, Tuple, Callable
from star_engine.types import StarVirtualNode, StarValue
from star_sdk.mobile.dimensions import ScreenMetrics, Dimension, DimensionUnit
from star_sdk.mobile.safe_area import SafeAreaInsets


class MobileLayoutNode:
    def __init__(
        self,
        node_type: str,
        x: float = 0.0,
        y: float = 0.0,
        width: float = 0.0,
        height: float = 0.0,
        props: Optional[Dict[str, Any]] = None,
        virtual_node: Optional[StarVirtualNode] = None
    ):
        self.node_type = node_type
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.props = props or {}
        self.virtual_node = virtual_node
        self.children: List["MobileLayoutNode"] = []
        self.parent: Optional["MobileLayoutNode"] = None

    @property
    def hit_bounds(self) -> Tuple[float, float, float, float]:
        """
        Enforces minimum 44x44 DP touch target for accessibility on interactive components.
        """
        min_size = 44.0 if self.is_interactive else 0.0
        eff_w = max(self.width, min_size)
        eff_h = max(self.height, min_size)
        offset_x = (eff_w - self.width) / 2.0
        offset_y = (eff_h - self.height) / 2.0
        return (self.x - offset_x, self.y - offset_y, eff_w, eff_h)

    @property
    def is_interactive(self) -> bool:
        if not self.virtual_node:
            return False
        return (
            bool(self.virtual_node.listeners) or
            self.node_type in ("button", "switch", "slider", "input", "bottom_navigation")
        )

    def contains_point(self, px: float, py: float) -> bool:
        hx, hy, hw, hh = self.hit_bounds
        return hx <= px <= (hx + hw) and hy <= py <= (hy + hh)

    def __repr__(self) -> str:
        return f"MobileLayoutNode({self.node_type}, x={self.x:.1f}, y={self.y:.1f}, w={self.width:.1f}, h={self.height:.1f})"


class MobileLayoutEngine:
    def __init__(self, metrics: Optional[ScreenMetrics] = None, insets: Optional[SafeAreaInsets] = None):
        self.metrics = metrics or ScreenMetrics()
        self.insets = insets or SafeAreaInsets()

    def compute_layout(self, root: StarVirtualNode) -> MobileLayoutNode:
        return self._layout_node(
            root,
            x=0.0,
            y=0.0,
            available_width=self.metrics.width_dp,
            available_height=self.metrics.height_dp
        )

    def _layout_node(
        self,
        vnode: StarVirtualNode,
        x: float,
        y: float,
        available_width: float,
        available_height: float
    ) -> MobileLayoutNode:
        tag = vnode.tag.lower()
        props = dict(vnode.props)

        # 1. SafeArea Container
        if tag == "safe_area":
            safe_x = x + self.insets.left
            safe_y = y + self.insets.top
            safe_w = max(0.0, available_width - self.insets.left - self.insets.right)
            safe_h = max(0.0, available_height - self.insets.top - self.insets.bottom)

            node = MobileLayoutNode(tag, x=x, y=y, width=available_width, height=available_height, props=props, virtual_node=vnode)
            curr_y = safe_y
            for child_vnode in vnode.children:
                child_node = self._layout_node(child_vnode, safe_x, curr_y, safe_w, safe_h)
                child_node.parent = node
                node.children.append(child_node)
                curr_y += child_node.height + 12.0 # Standard 12dp spacing
            return node

        # 2. AppBar Component
        elif tag in ("app_bar", "mobile_app_bar"):
            bar_height = 56.0 # Standard 56dp mobile app bar
            node = MobileLayoutNode(tag, x=x, y=y, width=available_width, height=bar_height, props=props, virtual_node=vnode)
            # Layout child actions / leading
            curr_x = x + 16.0
            for child_vnode in vnode.children:
                child_node = self._layout_node(child_vnode, curr_x, y + 8.0, 40.0, 40.0)
                child_node.parent = node
                node.children.append(child_node)
                curr_x += child_node.width + 8.0
            return node

        # 3. Bottom Navigation Bar
        elif tag == "bottom_navigation":
            bar_height = 64.0 + self.insets.bottom
            node = MobileLayoutNode(tag, x=x, y=available_height - bar_height, width=available_width, height=bar_height, props=props, virtual_node=vnode)
            return node

        # 4. Column Container
        elif tag in ("column", "container"):
            padding = 16.0
            inner_w = max(0.0, available_width - (padding * 2))
            curr_y = y + padding
            node = MobileLayoutNode(tag, x=x, y=y, width=available_width, height=0.0, props=props, virtual_node=vnode)
            for child_vnode in vnode.children:
                child_node = self._layout_node(child_vnode, x + padding, curr_y, inner_w, available_height)
                child_node.parent = node
                node.children.append(child_node)
                curr_y += child_node.height + 12.0
            node.height = max(curr_y - y, 40.0)
            return node

        # 5. Row Container
        elif tag == "row":
            padding = 8.0
            node = MobileLayoutNode(tag, x=x, y=y, width=available_width, height=48.0, props=props, virtual_node=vnode)
            child_count = max(1, len(vnode.children))
            item_w = max(40.0, (available_width - (padding * (child_count + 1))) / child_count)
            curr_x = x + padding
            max_h = 44.0
            for child_vnode in vnode.children:
                child_node = self._layout_node(child_vnode, curr_x, y + padding, item_w, available_height)
                child_node.parent = node
                node.children.append(child_node)
                curr_x += child_node.width + padding
                max_h = max(max_h, child_node.height)
            node.height = max_h + (padding * 2)
            return node

        # 6. ScrollView Container
        elif tag in ("scroll_view", "scroll"):
            padding = 12.0
            node = MobileLayoutNode(tag, x=x, y=y, width=available_width, height=available_height, props=props, virtual_node=vnode)
            curr_y = y + padding
            for child_vnode in vnode.children:
                child_node = self._layout_node(child_vnode, x + padding, curr_y, available_width - (padding * 2), available_height)
                child_node.parent = node
                node.children.append(child_node)
                curr_y += child_node.height + 12.0
            # props track content_height for scrolling mechanics
            node.props["content_height"] = curr_y - y
            return node

        # 7. Card Container
        elif tag == "card":
            padding = 16.0
            node = MobileLayoutNode(tag, x=x, y=y, width=available_width, height=0.0, props=props, virtual_node=vnode)
            curr_y = y + padding
            for child_vnode in vnode.children:
                child_node = self._layout_node(child_vnode, x + padding, curr_y, available_width - (padding * 2), available_height)
                child_node.parent = node
                node.children.append(child_node)
                curr_y += child_node.height + 8.0
            node.height = max(curr_y - y + padding, 60.0)
            return node

        # 8. Leaf Components
        elif tag == "title":
            return MobileLayoutNode(tag, x=x, y=y, width=available_width, height=36.0, props=props, virtual_node=vnode)
        elif tag == "text":
            return MobileLayoutNode(tag, x=x, y=y, width=available_width, height=24.0, props=props, virtual_node=vnode)
        elif tag == "button":
            return MobileLayoutNode(tag, x=x, y=y, width=available_width, height=48.0, props=props, virtual_node=vnode)
        elif tag == "input":
            return MobileLayoutNode(tag, x=x, y=y, width=available_width, height=52.0, props=props, virtual_node=vnode)
        elif tag in ("switch", "mobile_switch"):
            return MobileLayoutNode(tag, x=x, y=y, width=51.0, height=31.0, props=props, virtual_node=vnode)
        elif tag in ("slider", "mobile_slider"):
            return MobileLayoutNode(tag, x=x, y=y, width=available_width, height=44.0, props=props, virtual_node=vnode)
        elif tag == "badge":
            return MobileLayoutNode(tag, x=x, y=y, width=70.0, height=28.0, props=props, virtual_node=vnode)
        elif tag == "divider":
            return MobileLayoutNode(tag, x=x, y=y, width=available_width, height=1.0, props=props, virtual_node=vnode)
        else:
            return MobileLayoutNode(tag, x=x, y=y, width=available_width, height=44.0, props=props, virtual_node=vnode)

    def hit_test(self, root_node: MobileLayoutNode, x: float, y: float) -> Optional[MobileLayoutNode]:
        """
        Performs deep-first reverse hit testing to identify targeted component.
        """
        for child in reversed(root_node.children):
            hit = self.hit_test(child, x, y)
            if hit:
                return hit

        if root_node.contains_point(x, y) and root_node.is_interactive:
            return root_node
        return None
