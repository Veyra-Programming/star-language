"""
Star Desktop Native Runtime & Layout Engine
Authoritative Reference: STAR_DESKTOP.md
"""

import math
from typing import Dict, List, Any, Optional, Tuple, Callable
from star_engine.types import (
    StarValue, StarVirtualNode, StarComponentInstance, StarComponent,
    StarFunction, StarBuiltinFunction, StarNull
)
from star_backend.desktop.window import DesktopWindow
from star_backend.desktop.events import DesktopEventManager, DesktopEvent
from star_sdk.theme import THEME_PRESETS


class LayoutNode:
    def __init__(self, vnode: StarVirtualNode, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        self.vnode = vnode
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children: List['LayoutNode'] = []
        self.node_id = f"{vnode.tag}_{id(vnode)}"


class DesktopRuntime:
    def __init__(self, window: Optional[DesktopWindow] = None, theme_mode: str = "dark", headless: bool = False):
        self.theme = THEME_PRESETS.get(theme_mode, THEME_PRESETS["dark"])
        self.window = window or DesktopWindow(
            title="Star Desktop Application",
            width=840,
            height=640,
            bg_color=self.theme["background"],
            headless=headless
        )
        self.events = DesktopEventManager()
        self.root_component: Optional[Any] = None
        self.root_vnode: Optional[StarVirtualNode] = None
        self.layout_root: Optional[LayoutNode] = None
        self.interactive_elements: List[Tuple[int, int, int, int, Any, str]] = []  # (x1, y1, x2, y2, callback, tag)
        self.hovered_tag: Optional[str] = None
        self.anim_phase: float = 0.0
        self.has_active_animations: bool = False
        self.padding = 24
        self.spacing = 14

        self.window.bind_click(self._handle_window_click)
        self.window.bind_motion(self._handle_window_motion)
        self.window.bind_resize(self._handle_window_resize)
        self.window.start_ticker(fps=60, callback=self._on_anim_tick)

    def _on_anim_tick(self, dt: float):
        self.anim_phase += dt
        if self.has_active_animations:
            self.render()

    def mount(self, app_or_component: Any):
        self.root_component = app_or_component
        if isinstance(app_or_component, StarComponentInstance):
            app_or_component.on_reconcile = self._on_component_reconcile
            self.root_vnode = app_or_component.current_vdom
        elif isinstance(app_or_component, StarVirtualNode):
            self.root_vnode = app_or_component
        self.render()

    def _on_component_reconcile(self, instance: StarComponentInstance, old_vdom: Optional[StarVirtualNode]):
        self.root_vnode = instance.current_vdom
        self.render()

    def render(self):
        if not self.root_vnode:
            return

        self.window.clear()
        self.interactive_elements.clear()

        # Layout Pass
        content_width = max(self.window.width - (self.padding * 2), 100)
        self.layout_root = self._compute_layout(self.root_vnode, self.padding, self.padding, content_width)

        # Paint Pass
        self._paint_node(self.layout_root)
        self.window.update()

    def _compute_layout(self, vnode: StarVirtualNode, x: int, y: int, max_width: int) -> LayoutNode:
        style = vnode.props.get("style", {}) if isinstance(vnode.props.get("style"), dict) else {}
        
        # Style overrides
        pad = style.get("padding", self.spacing if vnode.tag in ("card", "container", "box") else 0)
        gap = style.get("gap", self.spacing)
        custom_w = style.get("width")
        custom_h = style.get("height")
        
        node_w = int(custom_w) if custom_w is not None and isinstance(custom_w, (int, float)) else max_width
        node = LayoutNode(vnode, x=x, y=y, width=node_w)

        if vnode.tag in ("column", "scroll", "list_view", "single_child_scroll_view", "material_app", "cupertino_app", "fluent_app", "center", "padding", "align", "sized_box", "expanded", "gesture_detector", "animated_container", "hero"):
            curr_y = y + pad
            inner_w = max(node_w - (pad * 2), 10)
            for child in vnode.children:
                if isinstance(child, StarVirtualNode):
                    child_layout = self._compute_layout(child, x + pad, curr_y, inner_w)
                    node.children.append(child_layout)
                    curr_y += child_layout.height + gap
            content_h = (curr_y - y) + pad - (gap if node.children else 0)
            node.height = int(custom_h) if custom_h is not None and isinstance(custom_h, (int, float)) else max(content_h, 0)

        elif vnode.tag == "row":
            valid_children = [c for c in vnode.children if isinstance(c, StarVirtualNode)]
            num_children = len(valid_children)
            inner_w = max(node_w - (pad * 2), 10)
            avail_w = inner_w - (gap * max(num_children - 1, 0))
            
            # Check for flex expansion in children
            flex_total = 0
            fixed_w_total = 0
            for c in valid_children:
                c_style = c.props.get("style", {}) if isinstance(c.props.get("style"), dict) else {}
                c_flex = c_style.get("flex", 1 if c.tag == "spacer" else None)
                if c_flex is not None:
                    flex_total += float(c_flex)
                elif c.tag == "badge":
                    fixed_w_total += len(c.props.get("label", "")) * 8 + 24
                elif c.tag == "icon":
                    fixed_w_total += c.props.get("size", 20) + 12
                elif c.tag == "avatar":
                    fixed_w_total += c.props.get("size", 40) + 8
                elif c_style.get("width") is not None:
                    fixed_w_total += int(c_style.get("width"))

            remaining_w = max(avail_w - fixed_w_total, 0)
            curr_x = x + pad
            max_h = 0

            for child in valid_children:
                c_style = child.props.get("style", {}) if isinstance(child.props.get("style"), dict) else {}
                c_flex = c_style.get("flex", 1 if child.tag == "spacer" else None)
                
                if c_flex is not None and flex_total > 0:
                    child_w = int(remaining_w * (float(c_flex) / flex_total))
                elif c_style.get("width") is not None:
                    child_w = int(c_style.get("width"))
                elif child.tag == "badge":
                    child_w = len(child.props.get("label", "")) * 8 + 24
                elif child.tag == "icon":
                    child_w = child.props.get("size", 20) + 8
                elif child.tag == "avatar":
                    child_w = child.props.get("size", 40) + 8
                elif child.tag == "switch" or child.tag == "mobile_switch":
                    child_w = 48
                elif flex_total == 0:
                    child_w = avail_w // max(num_children, 1)
                else:
                    child_w = avail_w // max(num_children, 1)

                child_layout = self._compute_layout(child, curr_x, y + pad, max(child_w, 10))
                node.children.append(child_layout)
                curr_x += child_layout.width + gap
                max_h = max(max_h, child_layout.height)

            node.height = int(custom_h) if custom_h is not None and isinstance(custom_h, (int, float)) else (max_h + (pad * 2))

        elif vnode.tag in ("card", "container", "box", "scaffold", "app_bar"):
            inner_w = max(node_w - (pad * 2), 10)
            curr_y = y + pad
            # For scaffold, lay out appBar, body, children
            scaffold_children = []
            if vnode.tag == "scaffold":
                if isinstance(vnode.props.get("appBar"), StarVirtualNode):
                    scaffold_children.append(vnode.props["appBar"])
                if isinstance(vnode.props.get("body"), StarVirtualNode):
                    scaffold_children.append(vnode.props["body"])
            for child in (scaffold_children or vnode.children):
                if isinstance(child, StarVirtualNode):
                    child_layout = self._compute_layout(child, x + pad, curr_y, inner_w)
                    node.children.append(child_layout)
                    curr_y += child_layout.height + gap
            content_h = (curr_y - y) + pad - (gap if node.children else 0)
            node.height = int(custom_h) if custom_h is not None and isinstance(custom_h, (int, float)) else max(content_h, 40)

        elif vnode.tag == "stack":
            inner_w = max(node_w - (pad * 2), 10)
            max_h = 0
            for child in vnode.children:
                if isinstance(child, StarVirtualNode):
                    child_layout = self._compute_layout(child, x + pad, y + pad, inner_w)
                    node.children.append(child_layout)
                    max_h = max(max_h, child_layout.height)
            node.height = int(custom_h) if custom_h is not None and isinstance(custom_h, (int, float)) else (max_h + (pad * 2))

        elif vnode.tag == "grid":
            cols = max(1, vnode.props.get("columns", 2))
            valid_children = [c for c in vnode.children if isinstance(c, StarVirtualNode)]
            inner_w = max(node_w - (pad * 2), 10)
            col_gap = gap
            row_gap = gap
            col_w = (inner_w - (col_gap * (cols - 1))) // cols
            
            curr_x = x + pad
            curr_y = y + pad
            row_max_h = 0
            
            for i, child in enumerate(valid_children):
                col_idx = i % cols
                if col_idx == 0 and i > 0:
                    curr_x = x + pad
                    curr_y += row_max_h + row_gap
                    row_max_h = 0
                
                child_layout = self._compute_layout(child, curr_x, curr_y, col_w)
                node.children.append(child_layout)
                row_max_h = max(row_max_h, child_layout.height)
                curr_x += col_w + col_gap
                
            total_h = (curr_y - y) + row_max_h + pad if valid_children else pad * 2
            node.height = int(custom_h) if custom_h is not None and isinstance(custom_h, (int, float)) else total_h

        elif vnode.tag == "spacer":
            size_prop = vnode.props.get("size")
            node.height = int(size_prop) if size_prop is not None else 16
            node.width = int(size_prop) if size_prop is not None else max_width

        elif vnode.tag == "title":
            level = vnode.props.get("level", 1)
            node.height = 42 if level == 1 else (36 if level == 2 else 30)

        elif vnode.tag == "text":
            node.height = 24

        elif vnode.tag == "button":
            node.height = 42

        elif vnode.tag == "input":
            node.height = 42

        elif vnode.tag == "badge":
            node.height = 26

        elif vnode.tag in ("switch", "mobile_switch"):
            node.height = 26
            node.width = 48

        elif vnode.tag in ("slider", "mobile_slider"):
            node.height = 26

        elif vnode.tag == "tabs":
            node.height = 40

        elif vnode.tag == "toast":
            node.height = 44

        elif vnode.tag == "spinner":
            size = vnode.props.get("size", 24)
            node.height = size
            node.width = size

        elif vnode.tag == "avatar":
            size = vnode.props.get("size", 40)
            node.height = size
            node.width = size

        elif vnode.tag == "icon":
            size = vnode.props.get("size", 20)
            node.height = size
            node.width = size

        elif vnode.tag == "image":
            node.height = int(vnode.props.get("height", 100)) if vnode.props.get("height") else 100

        elif vnode.tag == "divider":
            node.height = 12

        elif vnode.tag == "progress":
            node.height = 16

        elif vnode.tag == "checkbox":
            node.height = 26

        elif vnode.tag in ("shimmer", "skeleton"):
            self.has_active_animations = True
            node.height = int(vnode.props.get("height", 24))
            custom_w = vnode.props.get("width")
            if custom_w is not None:
                node.width = int(custom_w)
            for child in vnode.children:
                if isinstance(child, StarVirtualNode):
                    node.children.append(self._compute_layout(child, x, y, node.width))

        elif vnode.tag in ("animated_opacity", "animated_scale", "animated_slide", "animated_rotation", "animated_container", "pulse", "bounce", "shake", "glow", "ripple", "tooltip"):
            self.has_active_animations = True
            custom_h = vnode.props.get("height")
            custom_w = vnode.props.get("width")
            child_w = int(custom_w) if custom_w is not None else max_width
            max_child_h = 0
            for child in vnode.children:
                if isinstance(child, StarVirtualNode):
                    child_layout = self._compute_layout(child, x, y, child_w)
                    node.children.append(child_layout)
                    max_child_h = max(max_child_h, child_layout.height)
            node.height = int(custom_h) if custom_h is not None else max(max_child_h, 30)

        elif vnode.tag in ("modal", "dialog"):
            node.width = min(540, max_width)
            node.height = 280
            for child in vnode.children:
                if isinstance(child, StarVirtualNode):
                    node.children.append(self._compute_layout(child, x + 20, y + 60, node.width - 40))

        elif vnode.tag == "accordion":
            is_open = bool(vnode.props.get("expanded", False))
            header_h = 42
            inner_h = 0
            if is_open:
                curr_y = y + header_h + 10
                for child in vnode.children:
                    if isinstance(child, StarVirtualNode):
                        child_layout = self._compute_layout(child, x + 16, curr_y, max_width - 32)
                        node.children.append(child_layout)
                        inner_h += child_layout.height + 8
                        curr_y += child_layout.height + 8
            node.height = header_h + (inner_h + 16 if is_open else 0)

        elif vnode.tag == "dropdown":
            node.height = 42

        elif vnode.tag == "breadcrumbs":
            node.height = 24

        elif vnode.tag == "pagination":
            node.height = 36

        elif vnode.tag == "table":
            rows = vnode.props.get("rows", [])
            node.height = 36 + len(rows) * 28 + 16

        elif vnode.tag == "code_block":
            code = vnode.props.get("code", "")
            lines = code.split("\n")
            node.height = max(60, 36 + len(lines) * 18 + 12)

        elif vnode.tag == "segmented_control":
            node.height = 36

        elif vnode.tag == "stepper":
            node.height = 56

        elif vnode.tag == "rating":
            node.height = 28

        elif vnode.tag == "fab":
            node.height = 56
            node.width = 56

        elif vnode.tag == "bottom_sheet":
            node.height = 220
            for child in vnode.children:
                if isinstance(child, StarVirtualNode):
                    node.children.append(self._compute_layout(child, x + 20, y + 20, max_width - 40))

        else:
            node.height = 30

        return node

    def _paint_node(self, node: LayoutNode):
        v = node.vnode
        x, y, w, h = node.x, node.y, node.width, node.height
        style = v.props.get("style", {}) if isinstance(v.props.get("style"), dict) else {}

        # Style properties
        bg = style.get("bg", style.get("background"))
        fg = style.get("fg", style.get("color"))
        radius = style.get("radius", style.get("corner_radius", 12))
        border = style.get("border", style.get("border_color"))

        if v.tag == "card":
            card_bg = bg or self.theme.get("card_bg", self.theme["surface"])
            card_border = border or self.theme["border"]
            
            # Check for linear gradient in bg
            if isinstance(card_bg, (list, tuple)) and len(card_bg) >= 2:
                self.window.draw_gradient_rect(x, y, w, h, card_bg[0], card_bg[1], corner_radius=radius)
            else:
                self.window.draw_card(x, y, w, h, bg=card_bg, border=card_border, corner_radius=radius)
            for child in node.children:
                self._paint_node(child)

        elif v.tag in ("container", "box"):
            if bg:
                if isinstance(bg, (list, tuple)) and len(bg) >= 2:
                    self.window.draw_gradient_rect(x, y, w, h, bg[0], bg[1], corner_radius=radius)
                else:
                    self.window.draw_rect(x, y, w, h, fill=bg, outline=border or "", corner_radius=radius)
            for child in node.children:
                self._paint_node(child)

        elif v.tag in ("column", "row", "stack", "grid", "scroll"):
            # Stack paints children in Z-index order (0 to end)
            for child in node.children:
                self._paint_node(child)

        elif v.tag == "title":
            content = v.props.get("content", "")
            level = v.props.get("level", 1)
            fsize = 24 if level == 1 else (20 if level == 2 else 16)
            self.window.draw_text(x, y, content, size=fsize, fill=fg or self.theme["text"], weight="bold")

        elif v.tag == "text":
            content = v.props.get("content", "")
            fsize = style.get("font_size", 14)
            self.window.draw_text(x, y, content, size=fsize, fill=fg or self.theme.get("text_secondary", self.theme["text"]))

        elif v.tag in ("button", "fab"):
            label = v.props.get("label", "Button" if v.tag == "button" else "＋ FAB")
            btn_w = w
            btn_bg = bg or (self.theme["accent"] if v.tag == "fab" else self.theme["primary"])
            btn_fg = fg or "#ffffff"
            btn_tag = f"{v.tag}:{label}_{id(v)}"
            is_hovered = (self.hovered_tag == btn_tag)
            self.window.draw_button(x, y, btn_w, h, label, bg=btn_bg, fg=btn_fg, corner_radius=radius, is_hovered=is_hovered)
            if "click" in v.listeners:
                self.interactive_elements.append((x, y, x + btn_w, y + h, v.listeners["click"], btn_tag))

        elif v.tag == "list_tile":
            title = str(v.props.get("title", ""))
            subtitle = str(v.props.get("subtitle", ""))
            self.window.draw_text(x, y, title, size=15, fill=self.theme["primary"], weight="bold")
            if subtitle:
                self.window.draw_text(x, y + 18, subtitle, size=12, fill=self.theme.get("text_secondary", "#94a3b8"))
            for child in node.children:
                self._paint_node(child)
            if "click" in v.listeners:
                self.interactive_elements.append((x, y, x + w, y + h, v.listeners["click"], f"list_tile_{id(v)}"))

        elif v.tag == "badge":
            label = v.props.get("label", "")
            variant = v.props.get("variant", "primary")
            variant_map = {
                "primary": self.theme["primary"],
                "accent": self.theme["accent"],
                "success": self.theme.get("success", "#10b981"),
                "warning": self.theme.get("warning", "#f59e0b"),
                "danger": self.theme.get("danger", "#ef4444"),
                "info": self.theme["accent"]
            }
            badge_bg = bg or variant_map.get(variant, self.theme["primary"])
            badge_w = self.window.draw_badge(x, y, label, bg=badge_bg, fg=fg or "#ffffff")
            node.width = badge_w

        elif v.tag == "icon":
            name = v.props.get("name", "star")
            size = v.props.get("size", 20)
            color = v.props.get("color") or fg or self.theme["accent"]
            self.window.draw_icon(x + (w // 2), y + (h // 2), name, size=size, fill=color)

        elif v.tag == "avatar":
            label = v.props.get("label", "U")
            size = v.props.get("size", 40)
            self.window.draw_avatar(x, y, size=size, label=label, bg=bg or self.theme["primary"], fg=fg or "#ffffff")

        elif v.tag in ("switch", "mobile_switch"):
            active = bool(v.props.get("value", False))
            active_col = self.theme.get("success", "#10b981")
            self.window.draw_switch(x, y, w, h, active=active, active_color=active_col, inactive_color=self.theme["border"])
            sw_tag = f"switch:{id(v)}"
            
            def _toggle_switch():
                v.props["value"] = not active
                if "change" in v.listeners and v.listeners["change"]:
                    self._dispatch_event(v.listeners["change"])
            
            self.interactive_elements.append((x, y, x + w, y + h, _toggle_switch, sw_tag))

        elif v.tag in ("slider", "mobile_slider"):
            val = float(v.props.get("value", 50.0))
            min_v = float(v.props.get("min", 0.0))
            max_v = float(v.props.get("max", 100.0))
            self.window.draw_slider(x, y, w, h, value=val, min_v=min_v, max_v=max_v, active_color=self.theme["primary"], bg_color=self.theme["border"])
            sl_tag = f"slider:{id(v)}"
            
            def _slider_click(cx: int):
                frac = max(0.0, min(1.0, (cx - x) / float(w) if w > 0 else 0.0))
                new_val = min_v + frac * (max_v - min_v)
                v.props["value"] = new_val
                if "change" in v.listeners and v.listeners["change"]:
                    self._dispatch_event(v.listeners["change"])
                    
            self.interactive_elements.append((x, y, x + w, y + h, _slider_click, sl_tag))

        elif v.tag == "tabs":
            items = v.props.get("items", [])
            active_idx = v.props.get("active", 0)
            self.window.draw_tabs(x, y, w, h, tabs=items, active_idx=active_idx, bg=self.theme["surface"], active_bg=self.theme["primary"], fg=self.theme["text"])
            if items:
                tab_w = w // len(items)
                for idx, label in enumerate(items):
                    tx = x + (idx * tab_w)
                    
                    def _make_tab_handler(target_idx):
                        def _tab_click():
                            v.props["active"] = target_idx
                            if "select" in v.listeners and v.listeners["select"]:
                                self._dispatch_event(v.listeners["select"])
                        return _tab_click
                        
                    self.interactive_elements.append((tx, y, tx + tab_w, y + h, _make_tab_handler(idx), f"tab:{label}_{idx}"))

        elif v.tag == "toast":
            message = v.props.get("message", "")
            variant = v.props.get("variant", "info")
            self.window.draw_toast(x, y, w, h, message=message, variant=variant, bg=self.theme["surface"], border=self.theme["border"])

        elif v.tag == "spinner":
            size = v.props.get("size", 24)
            color = v.props.get("color") or self.theme["primary"]
            self.window.draw_spinner(x, y, size=size, color=color)

        elif v.tag == "image":
            src = v.props.get("src", "")
            fit = v.props.get("fit", "cover")
            self.window.draw_image(x, y, w, h, src=src, fit=fit)

        elif v.tag == "divider":
            self.window.draw_divider(x, y + 4, w, color=border or self.theme["border"])

        elif v.tag == "input":
            placeholder = v.props.get("placeholder", "")
            self.window.draw_input(x, y, w, h, placeholder=placeholder, bg=self.theme["surface"], border=self.theme["border"])

        elif v.tag == "checkbox":
            label = v.props.get("label", "")
            checked = bool(v.props.get("checked", False))
            self.window.draw_rect(x, y + 3, 18, 18, fill=self.theme["primary"] if checked else self.theme["surface"], outline=self.theme["border"], corner_radius=4)
            if checked:
                self.window.draw_text(x + 4, y + 3, "✓", size=11, fill="#ffffff", weight="bold")
            self.window.draw_text(x + 28, y + 4, label, size=13, fill=self.theme["text"])
            
            def _toggle_cb():
                v.props["checked"] = not checked
                if "change" in v.listeners and v.listeners["change"]:
                    self._dispatch_event(v.listeners["change"])
            self.interactive_elements.append((x, y, x + w, y + h, _toggle_cb, f"checkbox:{label}"))

        elif v.tag == "progress":
            val = v.props.get("value", 0)
            max_v = v.props.get("max", 100)
            self.window.draw_rect(x, y, w, h, fill=self.theme["surface"], corner_radius=8)
            frac = max(0.0, min(1.0, val / float(max_v) if max_v > 0 else 0.0))
            fill_w = int(frac * w)
            if fill_w > 0:
                self.window.draw_gradient_rect(x, y, fill_w, h, self.theme["primary"], self.theme["secondary"], corner_radius=8)

        elif v.tag in ("shimmer", "skeleton"):
            rad = v.props.get("radius", 8)
            self.window.draw_shimmer(x, y, w, h, corner_radius=rad, phase=self.anim_phase * 1.5)
            for child in node.children:
                self._paint_node(child)

        elif v.tag in ("animated_opacity", "animated_scale", "animated_slide", "animated_rotation", "animated_container"):
            # Smoothly transform child bounding geometry
            for child in node.children:
                self._paint_node(child)

        elif v.tag == "pulse":
            min_s = float(v.props.get("min_scale", 0.95))
            max_s = float(v.props.get("max_scale", 1.05))
            osc = (math.sin(self.anim_phase * 4.0) + 1.0) / 2.0
            scale = min_s + osc * (max_s - min_s)
            for child in node.children:
                self._paint_node(child)

        elif v.tag == "glow":
            glow_col = v.props.get("color", "#00f0ff")
            blur = v.props.get("blur", 16)
            self.window.draw_glow_rect(x, y, w, h, fill=bg or self.theme["surface"], glow_color=glow_col, glow_size=blur, corner_radius=radius)
            for child in node.children:
                self._paint_node(child)

        elif v.tag in ("modal", "dialog"):
            is_open = bool(v.props.get("open", True))
            title = v.props.get("title", "Dialog")
            if is_open:
                self.window.draw_modal(x, y, w, h, title=title, is_open=True)
                for child in node.children:
                    self._paint_node(child)
                close_x = max(20, (self.window.width - w) // 2) + w - 30
                close_y = max(40, (self.window.height - h) // 2) + 16
                def _close_modal():
                    v.props["open"] = False
                    if "close" in v.listeners and v.listeners["close"]:
                        self._dispatch_event(v.listeners["close"])
                self.interactive_elements.append((close_x, close_y, close_x + 20, close_y + 20, _close_modal, f"modal_close:{id(v)}"))

        elif v.tag == "accordion":
            title = v.props.get("title", "")
            is_open = bool(v.props.get("expanded", False))
            self.window.draw_accordion(x, y, w, h, title=title, is_open=is_open)
            if is_open:
                for child in node.children:
                    self._paint_node(child)
            def _toggle_accordion():
                v.props["expanded"] = not is_open
                if "toggle" in v.listeners and v.listeners["toggle"]:
                    self._dispatch_event(v.listeners["toggle"])
            self.interactive_elements.append((x, y, x + w, y + 42, _toggle_accordion, f"accordion:{title}"))

        elif v.tag == "dropdown":
            items = v.props.get("items", [])
            sel_idx = v.props.get("selected", 0)
            placeholder = v.props.get("placeholder", "Select...")
            is_open = bool(v.props.get("open", False))
            self.window.draw_dropdown(x, y, w, h, items=items, selected_idx=sel_idx, placeholder=placeholder, is_open=is_open)
            def _toggle_dd():
                v.props["open"] = not is_open
            self.interactive_elements.append((x, y, x + w, y + h, _toggle_dd, f"dropdown:{id(v)}"))

        elif v.tag == "tooltip":
            text = v.props.get("text", "")
            pos = v.props.get("position", "top")
            for child in node.children:
                self._paint_node(child)
            tip_tag = f"tooltip:{id(v)}"
            if self.hovered_tag == tip_tag:
                self.window.draw_tooltip(x + (w // 2), y, text=text, position=pos)
            self.interactive_elements.append((x, y, x + w, y + h, lambda: None, tip_tag))

        elif v.tag == "breadcrumbs":
            items = v.props.get("items", [])
            self.window.draw_breadcrumbs(x, y, items=items)

        elif v.tag == "segmented_control":
            items = v.props.get("items", [])
            sel_idx = v.props.get("selected", 0)
            self.window.draw_segmented_control(x, y, w, h, items=items, selected_idx=sel_idx)
            if items:
                seg_w = (w - 4) // len(items)
                for idx, item in enumerate(items):
                    sx = x + 2 + (idx * seg_w)
                    def _make_seg_handler(target_idx):
                        def _seg_click():
                            v.props["selected"] = target_idx
                            if "select" in v.listeners and v.listeners["select"]:
                                self._dispatch_event(v.listeners["select"])
                        return _seg_click
                    self.interactive_elements.append((sx, y, sx + seg_w, y + h, _make_seg_handler(idx), f"seg:{item}_{idx}"))

        elif v.tag == "stepper":
            steps = v.props.get("steps", [])
            cur_step = v.props.get("current", 0)
            self.window.draw_stepper(x, y, w, steps=steps, current_step=cur_step)

        elif v.tag == "rating":
            score = float(v.props.get("value", 0.0))
            max_s = int(v.props.get("max", 5))
            self.window.draw_rating(x, y, score=score, max_stars=max_s)
            for star_i in range(max_s):
                star_x = x + (star_i * 24)
                def _make_star_handler(star_val):
                    def _rate():
                        v.props["value"] = float(star_val)
                        if "change" in v.listeners and v.listeners["change"]:
                            self._dispatch_event(v.listeners["change"])
                    return _rate
                self.interactive_elements.append((star_x, y, star_x + 22, y + 22, _make_star_handler(star_i + 1), f"star:{id(v)}_{star_i}"))

        elif v.tag == "code_block":
            code = v.props.get("code", "")
            lang = v.props.get("language", "star")
            self.window.draw_code_block(x, y, w, h, code=code, lang=lang)

        elif v.tag == "table":
            headers = v.props.get("headers", [])
            rows = v.props.get("rows", [])
            self.window.draw_table(x, y, w, h, headers=headers, rows=rows)

        elif v.tag == "bottom_sheet":
            is_open = bool(v.props.get("open", False))
            if is_open:
                sheet_y = self.window.height - h
                self.window.draw_rect(0, 0, self.window.width, self.window.height, fill="#050811")
                self.window.draw_rect(0, sheet_y, self.window.width, h, fill="#0f172a", outline="#00f0ff", corner_radius=20)
                self.window.draw_rect((self.window.width - 48) // 2, sheet_y + 8, 48, 4, fill="#334155", corner_radius=2)
                for child in node.children:
                    self._paint_node(child)

        elif v.tag == "marquee":
            txt = v.props.get("text", "")
            self.has_active_animations = True
            shift = int((self.anim_phase * 40.0) % max(1, w + len(txt) * 8))
            self.window.draw_rect(x, y, w, h, fill="#0f172a", outline="#334155", corner_radius=6)
            self.window.draw_text(x + w - shift, y + (h // 2), txt, size=12, fill="#38bdf8", anchor="w")

        elif v.tag == "confetti":
            self.has_active_animations = True
            count = v.props.get("count", 30)
            colors = ["#ec4899", "#00f0ff", "#10b981", "#f59e0b", "#8b5cf6"]
            for ci in range(count):
                cx = (x + int((ci * 73 + self.anim_phase * 60) % max(1, w)))
                cy = (y + int((ci * 47 + self.anim_phase * 90) % max(1, h)))
                col = colors[ci % len(colors)]
                self.window.draw_rect(cx, cy, 6, 6, fill=col, corner_radius=1)

    def _dispatch_event(self, callback: Any, arg: Any = None):
        if callable(callback):
            if arg is not None:
                try:
                    callback(arg)
                except TypeError:
                    callback()
            else:
                callback()
        elif isinstance(callback, (StarFunction, StarBuiltinFunction)):
            from star_engine.interpreter import Interpreter
            interp = Interpreter()
            if hasattr(callback, "body"):
                for s in callback.body:
                    interp.execute(s, callback.closure_env)

    def _handle_window_motion(self, x: int, y: int):
        new_hover = None
        for x1, y1, x2, y2, callback, tag in self.interactive_elements:
            if x1 <= x <= x2 and y1 <= y <= y2:
                new_hover = tag
                break
        if new_hover != self.hovered_tag:
            self.hovered_tag = new_hover
            self.render()

    def _handle_window_click(self, x: int, y: int):
        for x1, y1, x2, y2, callback, tag in self.interactive_elements:
            if x1 <= x <= x2 and y1 <= y <= y2:
                if tag.startswith("slider:"):
                    self._dispatch_event(callback, x)
                else:
                    self._dispatch_event(callback)
                self.render()
                break

    def _handle_window_resize(self, w: int, h: int):
        self.render()

    def simulate_click(self, tag_or_label: str) -> bool:
        for x1, y1, x2, y2, callback, tag in self.interactive_elements:
            if tag_or_label in tag:
                self._dispatch_event(callback)
                self.render()
                return True
        return False

