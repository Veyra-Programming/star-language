"""
Star Terminal UI (TUI) TrueColor Visual Renderer
Authoritative Reference: STAR_UI.md
"""

import re
import shutil
from typing import List, Dict, Any, Optional, Tuple
from star_engine.types import (
    StarVirtualNode, StarComponentInstance, StarValue, StarNull
)
from star_sdk.theme import THEME_PRESETS

ANSI_REGEX = re.compile(r'\x1b\[[0-9;]*m')


def strip_ansi(s: str) -> str:
    return ANSI_REGEX.sub('', s)


def visible_len(s: str) -> int:
    return len(strip_ansi(s))


def _hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    hex_code = hex_code.lstrip('#')
    if len(hex_code) == 3:
        hex_code = ''.join([c * 2 for c in hex_code])
    if len(hex_code) < 6:
        return (200, 200, 200)
    try:
        return int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16)
    except Exception:
        return (200, 200, 200)


def fg(hex_code: str) -> str:
    r, g, b = _hex_to_rgb(hex_code)
    return f"\x1b[38;2;{r};{g};{b}m"


def bg(hex_code: str) -> str:
    r, g, b = _hex_to_rgb(hex_code)
    return f"\x1b[48;2;{r};{g};{b}m"


RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"

ICON_MAP: Dict[str, str] = {
    "star": "★",
    "heart": "♥",
    "check": "✓",
    "close": "✕",
    "cross": "✕",
    "search": "🔍",
    "settings": "⚙",
    "user": "👤",
    "bell": "🔔",
    "arrow_right": "➔",
    "arrow_left": "⬅",
    "chevron_right": "❯",
    "chevron_left": "❮",
    "plus": "＋",
    "minus": "－",
    "refresh": "↻",
    "shield": "🛡",
    "zap": "⚡",
    "home": "🏠",
    "code": "</>",
    "info": "ℹ",
    "alert": "⚠",
    "chart": "📊",
    "sparkles": "✨",
    "moon": "🌙",
    "sun": "☀️"
}


class TUIRenderer:
    """
    Renders Star Virtual Node component trees into 24-bit TrueColor ANSI terminal output.
    """

    def __init__(self, theme_mode: str = "dark", max_width: int = 78):
        self.theme = THEME_PRESETS.get(theme_mode, THEME_PRESETS["dark"])
        self.max_width = max_width

    def render(self, root: Any, width: Optional[int] = None) -> str:
        w = width or self.max_width
        vnode = None
        if isinstance(root, StarComponentInstance):
            vnode = root.current_vdom
        elif isinstance(root, StarVirtualNode):
            vnode = root
        elif hasattr(root, "render_decl") and hasattr(root, "closure_env"):
            # StarComponent definition - auto-instantiate
            from star_engine.interpreter import Interpreter
            from star_engine.ast_nodes import CallNode, IdentifierNode
            from star_engine.tokens import SourceLocation
            from star_engine.environment import Environment
            interp = Interpreter()
            call = CallNode(location=SourceLocation("<tui>", 1, 1, 0), callee=IdentifierNode(location=SourceLocation("<tui>", 1, 1, 0), name=root.name), arguments=[])
            temp_env = Environment(parent=root.closure_env)
            temp_env.define(root.name, root, is_constant=True)
            res = interp.evaluate(call, temp_env)
            if isinstance(res, (StarVirtualNode, StarComponentInstance)):
                return self.render(res, width=w)

        if not vnode:
            return f"{DIM}[Empty UI Tree]{RESET}"

        lines = self._render_node(vnode, w)
        return "\n".join(lines)

    def print_preview(self, root: Any, title: str = "Star UI Terminal Preview"):
        import sys
        if hasattr(sys.stdout, "reconfigure"):
            try:
                sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass

        rendered = self.render(root)
        border_col = fg(self.theme["primary"])
        title_col = fg(self.theme["accent"])
        accent_col = fg(self.theme["secondary"])

        print(f"\n{border_col}╔{'═' * (self.max_width - 2)}╗{RESET}")
        header_text = f" ⭐ {title} "
        left_pad = (self.max_width - 2 - len(header_text)) // 2
        right_pad = (self.max_width - 2 - len(header_text) - left_pad)
        print(f"{border_col}║{RESET}{' ' * left_pad}{BOLD}{title_col}{header_text}{RESET}{' ' * right_pad}{border_col}║{RESET}")
        print(f"{border_col}╠{'═' * (self.max_width - 2)}╣{RESET}")
        
        for line in rendered.split("\n"):
            vlen = visible_len(line)
            pad = max(0, self.max_width - 4 - vlen)
            print(f"{border_col}║{RESET}  {line}{' ' * pad}{border_col}║{RESET}")
            
        print(f"{border_col}╚{'═' * (self.max_width - 2)}╝{RESET}\n")

    def _render_node(self, vnode: StarVirtualNode, width: int) -> List[str]:
        tag = vnode.tag.lower()
        props = vnode.props
        style = props.get("style", {}) if isinstance(props.get("style"), dict) else {}

        if tag in ("column", "scroll"):
            res: List[str] = []
            for child in vnode.children:
                if isinstance(child, StarVirtualNode):
                    res.extend(self._render_node(child, width))
            return res

        elif tag == "row":
            valid_children = [c for c in vnode.children if isinstance(c, StarVirtualNode)]
            if not valid_children:
                return []
            
            # Simple horizontal inline layout for small widgets
            inline_parts = []
            all_inline = True
            for c in valid_children:
                if c.tag in ("badge", "button", "switch", "mobile_switch", "icon", "avatar", "text", "spacer"):
                    rendered_c = self._render_node(c, 24)
                    inline_parts.append(" ".join(rendered_c))
                else:
                    all_inline = False
                    break
            
            if all_inline:
                return ["  ".join(inline_parts)]
            
            # Multi-column layout side-by-side for cards
            col_count = len(valid_children)
            col_w = max(16, (width - (2 * (col_count - 1))) // col_count)
            cols_rendered = [self._render_node(c, col_w) for c in valid_children]
            
            max_lines = max(len(cr) for cr in cols_rendered)
            combined: List[str] = []
            for line_idx in range(max_lines):
                row_pieces = []
                for c_idx, cr in enumerate(cols_rendered):
                    piece = cr[line_idx] if line_idx < len(cr) else ""
                    vlen = visible_len(piece)
                    pad = max(0, col_w - vlen)
                    row_pieces.append(piece + (" " * pad))
                combined.append("  ".join(row_pieces))
            return combined

        elif tag == "grid":
            cols = max(1, props.get("columns", 2))
            valid_children = [c for c in vnode.children if isinstance(c, StarVirtualNode)]
            if not valid_children:
                return []
            
            col_w = max(16, (width - (2 * (cols - 1))) // cols)
            combined: List[str] = []
            
            for i in range(0, len(valid_children), cols):
                chunk = valid_children[i:i + cols]
                chunk_rendered = [self._render_node(c, col_w) for c in chunk]
                max_lines = max(len(cr) for cr in chunk_rendered)
                for line_idx in range(max_lines):
                    row_pieces = []
                    for cr in chunk_rendered:
                        piece = cr[line_idx] if line_idx < len(cr) else ""
                        vlen = visible_len(piece)
                        pad = max(0, col_w - vlen)
                        row_pieces.append(piece + (" " * pad))
                    combined.append("  ".join(row_pieces))
            return combined

        elif tag in ("card", "container", "box", "stack"):
            border_c = fg(self.theme["border"])
            inner_w = max(10, width - 4)
            inner_lines: List[str] = []
            for child in vnode.children:
                if isinstance(child, StarVirtualNode):
                    inner_lines.extend(self._render_node(child, inner_w))

            lines = []
            lines.append(f"{border_c}╭{'─' * (width - 2)}╮{RESET}")
            for il in inner_lines:
                vlen = visible_len(il)
                pad = max(0, width - 4 - vlen)
                lines.append(f"{border_c}│{RESET} {il}{' ' * pad} {border_c}│{RESET}")
            lines.append(f"{border_c}╰{'─' * (width - 2)}╯{RESET}")
            return lines

        elif tag == "title":
            content = props.get("content", "")
            level = props.get("level", 1)
            t_col = fg(self.theme["primary"]) if level == 1 else fg(self.theme["accent"])
            prefix = "🌟 " if level == 1 else "▶ "
            return [f"{BOLD}{t_col}{prefix}{content}{RESET}"]

        elif tag == "text":
            content = props.get("content", "")
            txt_col = fg(self.theme.get("text_secondary", self.theme["text"]))
            return [f"{txt_col}{content}{RESET}"]

        elif tag == "button":
            label = props.get("label", "Button")
            btn_bg = bg(self.theme["primary"])
            btn_fg = fg("#ffffff")
            return [f"{btn_bg}{btn_fg}{BOLD}  [ ❯ {label} ]  {RESET}"]

        elif tag == "badge":
            label = props.get("label", "")
            variant = props.get("variant", "primary")
            variant_map = {
                "primary": self.theme["primary"],
                "accent": self.theme["accent"],
                "success": self.theme.get("success", "#10b981"),
                "warning": self.theme.get("warning", "#f59e0b"),
                "danger": self.theme.get("danger", "#ef4444"),
                "info": self.theme["accent"]
            }
            b_color = variant_map.get(variant, self.theme["primary"])
            return [f"{bg(b_color)}{fg('#0f172a')}{BOLD}  ● {label}  {RESET}"]

        elif tag in ("switch", "mobile_switch"):
            active = bool(props.get("value", False))
            if active:
                return [f"{bg(self.theme.get('success', '#10b981'))}{fg('#ffffff')}{BOLD} [● ON ] {RESET}"]
            else:
                return [f"{bg(self.theme['border'])}{fg('#94a3b8')} [ OFF ○] {RESET}"]

        elif tag in ("slider", "mobile_slider"):
            val = float(props.get("value", 50.0))
            min_v = float(props.get("min", 0.0))
            max_v = float(props.get("max", 100.0))
            span = max_v - min_v if max_v > min_v else 1.0
            frac = max(0.0, min(1.0, (val - min_v) / span))
            total_slots = max(10, width - 18)
            filled = int(frac * total_slots)
            empty = total_slots - filled
            bar = f"{fg(self.theme['primary'])}{'━' * filled}●{fg(self.theme['border'])}{'─' * empty}{RESET}"
            return [f"[{bar}] {BOLD}{int(val)}{RESET}"]

        elif tag == "tabs":
            items = props.get("items", [])
            active_idx = props.get("active", 0)
            tab_strs = []
            for idx, it in enumerate(items):
                if idx == active_idx:
                    tab_strs.append(f"{bg(self.theme['primary'])}{fg('#ffffff')}{BOLD}  {it}  {RESET}")
                else:
                    tab_strs.append(f"{fg('#94a3b8')}  {it}  {RESET}")
            return ["│".join(tab_strs)]

        elif tag == "toast":
            msg = props.get("message", "")
            variant = props.get("variant", "info")
            v_col = fg(self.theme.get("success" if variant == "success" else "accent", "#38bdf8"))
            return [f"{v_col}📢 [{variant.upper()}]{RESET} {BOLD}{msg}{RESET}"]

        elif tag == "progress":
            val = float(props.get("value", 0))
            max_v = float(props.get("max", 100))
            frac = max(0.0, min(1.0, val / max_v if max_v > 0 else 0.0))
            total_bar = max(8, width - 14)
            filled_slots = int(frac * total_bar)
            empty_slots = total_bar - filled_slots
            pct = int(frac * 100)
            bar_fill = f"{fg(self.theme['primary'])}{'█' * filled_slots}"
            bar_empty = f"{fg(self.theme['border'])}{'░' * empty_slots}{RESET}"
            return [f"[{bar_fill}{bar_empty}] {BOLD}{pct}%{RESET}"]

        elif tag in ("material_app", "cupertino_app", "fluent_app"):
            res: List[str] = []
            for child in vnode.children:
                if isinstance(child, StarVirtualNode):
                    res.extend(self._render_node(child, width))
            return res

        elif tag == "scaffold":
            res: List[str] = []
            # Check for appBar in props or children
            app_bar = props.get("appBar") or props.get("navigationBar")
            if isinstance(app_bar, StarVirtualNode):
                res.extend(self._render_node(app_bar, width))
                res.append(f"{fg(self.theme['border'])}{'─' * width}{RESET}")

            # Body in props or children
            body = props.get("body") or props.get("child")
            if isinstance(body, StarVirtualNode):
                res.extend(self._render_node(body, width))
            for child in vnode.children:
                if isinstance(child, StarVirtualNode) and child != app_bar and child != body:
                    res.extend(self._render_node(child, width))

            # Floating Action Button or Bottom Navigation
            fab = props.get("floatingActionButton")
            if isinstance(fab, StarVirtualNode):
                fab_rendered = self._render_node(fab, width)
                res.append(f"{' ' * max(0, width - 20)}{''.join(fab_rendered)}")

            bottom_nav = props.get("bottomNavigationBar")
            if isinstance(bottom_nav, StarVirtualNode):
                res.append(f"{fg(self.theme['border'])}{'─' * width}{RESET}")
                res.extend(self._render_node(bottom_nav, width))
            return res

        elif tag == "app_bar":
            title = props.get("title", "")
            if isinstance(title, StarVirtualNode):
                title_lines = self._render_node(title, width - 10)
                title_str = " ".join(title_lines)
            else:
                title_str = str(title)
            bar_bg = bg(self.theme.get("primary", "#6366f1"))
            bar_fg = fg("#ffffff")
            header_line = f"  🌟 {title_str}  "
            pad = max(0, width - visible_len(header_line))
            return [f"{bar_bg}{bar_fg}{BOLD}{header_line}{' ' * pad}{RESET}"]

        elif tag in ("center", "padding", "align", "sized_box", "expanded", "gesture_detector", "animated_container", "hero", "single_child_scroll_view"):
            res: List[str] = []
            for child in vnode.children:
                if isinstance(child, StarVirtualNode):
                    res.extend(self._render_node(child, width))
            return res

        elif tag == "list_tile":
            title = str(props.get("title", ""))
            subtitle = str(props.get("subtitle", ""))
            t_col = fg(self.theme.get("primary", "#6366f1"))
            sub_col = fg(self.theme.get("text_secondary", "#94a3b8"))
            res = [f"{t_col}❯ {BOLD}{title}{RESET}"]
            if subtitle:
                res.append(f"  {sub_col}{subtitle}{RESET}")
            return res

        elif tag == "fab":
            btn_bg = bg(self.theme.get("accent", "#06b6d4"))
            btn_fg = fg("#0f172a")
            return [f"{btn_bg}{btn_fg}{BOLD}  [ ✚ FAB ]  {RESET}"]

        elif tag == "icon":
            glyph = props.get("glyph")
            if not glyph:
                name = props.get("name", "star").lower()
                glyph = ICON_MAP.get(name, "★")
            return [f"{fg(self.theme['accent'])}{glyph}{RESET}"]

        elif tag == "avatar":
            label = props.get("label", "U")
            initials = label[:2].upper()
            return [f"{bg(self.theme['primary'])}{fg('#ffffff')}{BOLD} ({initials}) {RESET}"]

        elif tag == "divider":
            border_c = fg(self.theme["border"])
            return [f"{border_c}{'─' * width}{RESET}"]

        elif tag == "input":
            placeholder = props.get("placeholder", "...")
            return [f"{fg('#64748b')}[✎ {placeholder}]{RESET}"]

        elif tag == "checkbox":
            label = props.get("label", "")
            checked = bool(props.get("checked", False))
            mark = f"{fg(self.theme['primary'])}[✓]{RESET}" if checked else f"{fg(self.theme['border'])}[ ]{RESET}"
            return [f"{mark} {label}"]

        elif tag == "spacer":
            return [""]

        else:
            return [f"{DIM}<{tag}>{RESET}"]
