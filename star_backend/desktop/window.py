"""
Star Desktop Windowing Abstraction
Authoritative Reference: STAR_DESKTOP.md
"""

import sys
import time
from typing import Optional, Callable, Dict, Any, List, Tuple


ICON_GLYPHS: Dict[str, str] = {
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


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    if len(hex_color) < 6:
        return (0, 0, 0)
    try:
        return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    except Exception:
        return (0, 0, 0)


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{max(0, min(255, r)):02x}{max(0, min(255, g)):02x}{max(0, min(255, b)):02x}"


def _interpolate_color(c1: str, c2: str, factor: float) -> str:
    r1, g1, b1 = _hex_to_rgb(c1)
    r2, g2, b2 = _hex_to_rgb(c2)
    factor = max(0.0, min(1.0, factor))
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return _rgb_to_hex(r, g, b)


class DesktopWindow:
    def __init__(self, title: str = "Star Application", width: int = 800, height: int = 600, bg_color: str = "#0f172a", headless: bool = False):
        self.title = title
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.headless = headless
        self.is_running = False
        self.click_handlers: List[Callable[[int, int], None]] = []
        self.motion_handlers: List[Callable[[int, int], None]] = []
        self.key_handlers: List[Callable[[str], None]] = []
        self.resize_handlers: List[Callable[[int, int], None]] = []
        self.draw_commands: List[Dict[str, Any]] = []

        self._tk_root = None
        self._tk_canvas = None
        if not self.headless:
            try:
                import tkinter as tk
                self._tk_root = tk.Tk()
                self._tk_root.title(self.title)
                self._tk_root.geometry(f"{self.width}x{self.height}")
                self._tk_root.configure(bg=self.bg_color)

                self._tk_canvas = tk.Canvas(
                    self._tk_root,
                    width=self.width,
                    height=self.height,
                    bg=self.bg_color,
                    highlightthickness=0
                )
                self._tk_canvas.pack(fill=tk.BOTH, expand=True)

                self._tk_canvas.bind("<Button-1>", self._on_tk_click)
                self._tk_canvas.bind("<Motion>", self._on_tk_motion)
                self._tk_root.bind("<Key>", self._on_tk_key)
                self._tk_root.bind("<Configure>", self._on_tk_resize)
            except Exception:
                # Fallback to virtual headless window surface
                self._tk_root = None
                self._tk_canvas = None
                self.headless = True

    def _on_tk_click(self, event):
        for h in self.click_handlers:
            h(event.x, event.y)

    def _on_tk_motion(self, event):
        for h in self.motion_handlers:
            h(event.x, event.y)

    def _on_tk_key(self, event):
        for h in self.key_handlers:
            h(event.char or event.keysym)

    def _on_tk_resize(self, event):
        if event.widget == self._tk_root:
            if event.width != self.width or event.height != self.height:
                self.width = event.width
                self.height = event.height
                for h in self.resize_handlers:
                    h(self.width, self.height)

    def bind_click(self, handler: Callable[[int, int], None]):
        self.click_handlers.append(handler)

    def bind_motion(self, handler: Callable[[int, int], None]):
        self.motion_handlers.append(handler)

    def bind_key(self, handler: Callable[[str], None]):
        self.key_handlers.append(handler)

    def bind_resize(self, handler: Callable[[int, int], None]):
        self.resize_handlers.append(handler)

    def clear(self):
        self.draw_commands.clear()
        if self._tk_canvas:
            self._tk_canvas.delete("all")

    def draw_rect(self, x: int, y: int, w: int, h: int, fill: str = "#1e293b", outline: str = "", corner_radius: int = 0):
        self.draw_commands.append({
            "type": "rect", "x": x, "y": y, "w": w, "h": h,
            "fill": fill, "outline": outline, "radius": corner_radius
        })
        if not self._tk_canvas or w <= 0 or h <= 0:
            return

        r = min(corner_radius, min(w, h) // 2)
        if r <= 2:
            kwargs: Dict[str, Any] = {"fill": fill}
            if outline:
                kwargs["outline"] = outline
            else:
                kwargs["outline"] = fill
            self._tk_canvas.create_rectangle(x, y, x + w, y + h, **kwargs)
        else:
            # Pixel-perfect rounded rectangle with 4 corner arcs + center fill
            d = 2 * r
            # Corner arcs
            self._tk_canvas.create_arc(x, y, x + d, y + d, start=90, extent=90, fill=fill, outline="")
            self._tk_canvas.create_arc(x + w - d, y, x + w, y + d, start=0, extent=90, fill=fill, outline="")
            self._tk_canvas.create_arc(x + w - d, y + h - d, x + w, y + h, start=270, extent=90, fill=fill, outline="")
            self._tk_canvas.create_arc(x, y + h - d, x + d, y + h, start=180, extent=90, fill=fill, outline="")
            # Center fill rectangles
            self._tk_canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=fill, outline="")
            self._tk_canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=fill, outline="")

            # Border outline if present
            if outline and outline != fill:
                self._tk_canvas.create_arc(x, y, x + d, y + d, start=90, extent=90, style="arc", outline=outline)
                self._tk_canvas.create_arc(x + w - d, y, x + w, y + d, start=0, extent=90, style="arc", outline=outline)
                self._tk_canvas.create_arc(x + w - d, y + h - d, x + w, y + h, start=270, extent=90, style="arc", outline=outline)
                self._tk_canvas.create_arc(x, y + h - d, x + d, y + h, start=180, extent=90, style="arc", outline=outline)
                self._tk_canvas.create_line(x + r, y, x + w - r, y, fill=outline)
                self._tk_canvas.create_line(x + w, y + r, x + w, y + h - r, fill=outline)
                self._tk_canvas.create_line(x + r, y + h, x + w - r, y + h, fill=outline)
                self._tk_canvas.create_line(x, y + r, x, y + h - r, fill=outline)

    def draw_gradient_rect(self, x: int, y: int, w: int, h: int, c1: str, c2: str, horizontal: bool = True, corner_radius: int = 0):
        self.draw_commands.append({
            "type": "gradient_rect", "x": x, "y": y, "w": w, "h": h,
            "c1": c1, "c2": c2, "horizontal": horizontal, "radius": corner_radius
        })
        if not self._tk_canvas or w <= 0 or h <= 0:
            return

        steps = 16
        if horizontal:
            step_w = max(1, w // steps)
            for i in range(steps):
                curr_x = x + (i * step_w)
                curr_w = step_w if i < steps - 1 else (x + w - curr_x)
                if curr_w <= 0:
                    break
                color = _interpolate_color(c1, c2, i / float(steps - 1))
                r = corner_radius if (i == 0 or i == steps - 1) else 0
                self.draw_rect(curr_x, y, curr_w, h, fill=color, corner_radius=r)
        else:
            step_h = max(1, h // steps)
            for i in range(steps):
                curr_y = y + (i * step_h)
                curr_h = step_h if i < steps - 1 else (y + h - curr_y)
                if curr_h <= 0:
                    break
                color = _interpolate_color(c1, c2, i / float(steps - 1))
                r = corner_radius if (i == 0 or i == steps - 1) else 0
                self.draw_rect(x, curr_y, w, curr_h, fill=color, corner_radius=r)

    def draw_shadow(self, x: int, y: int, w: int, h: int, corner_radius: int = 8, elevation: int = 2):
        self.draw_commands.append({
            "type": "shadow", "x": x, "y": y, "w": w, "h": h,
            "radius": corner_radius, "elevation": elevation
        })
        if not self._tk_canvas or w <= 0 or h <= 0:
            return

        # Multi-layered soft drop shadow
        layers = min(elevation, 3)
        shadow_colors = ["#070b14", "#0b1120", "#0f172a"]
        for i in range(layers):
            offset_y = (i + 1) * 2
            spread = (layers - i) * 2
            col = shadow_colors[min(i, len(shadow_colors) - 1)]
            self.draw_rect(x - spread, y + offset_y, w + (spread * 2), h, fill=col, corner_radius=corner_radius + 2)

    def draw_text(self, x: int, y: int, text: str, font: str = "Inter", size: int = 14, fill: str = "#f8fafc", anchor: str = "nw", weight: str = "normal"):
        self.draw_commands.append({
            "type": "text", "x": x, "y": y, "text": text,
            "font": font, "size": size, "fill": fill, "anchor": anchor, "weight": weight
        })
        if self._tk_canvas:
            font_tuple = (font, size, weight) if weight and weight != "normal" else (font, size)
            self._tk_canvas.create_text(x, y, text=text, fill=fill, font=font_tuple, anchor=anchor)

    def draw_button(self, x: int, y: int, w: int, h: int, label: str, bg: str = "#6366f1", fg: str = "#ffffff", corner_radius: int = 8, is_hovered: bool = False):
        button_bg = bg
        if is_hovered:
            button_bg = _interpolate_color(bg, "#ffffff", 0.15)
        self.draw_shadow(x, y, w, h, corner_radius=corner_radius, elevation=2 if is_hovered else 1)
        self.draw_rect(x, y, w, h, fill=button_bg, corner_radius=corner_radius)
        tx = x + (w // 2)
        ty = y + (h // 2)
        self.draw_text(tx, ty, label, size=13, fill=fg, anchor="center", weight="bold")

    def draw_card(self, x: int, y: int, w: int, h: int, bg: str = "#1e293b", border: str = "#334155", corner_radius: int = 12, elevation: int = 2):
        if elevation > 0:
            self.draw_shadow(x, y, w, h, corner_radius=corner_radius, elevation=elevation)
        self.draw_rect(x, y, w, h, fill=bg, outline=border, corner_radius=corner_radius)

    def draw_badge(self, x: int, y: int, label: str, bg: str = "#4f46e5", fg: str = "#ffffff") -> int:
        pad_x = 12
        pad_y = 4
        text_len = len(label) * 8
        w = text_len + (pad_x * 2)
        h = 24
        self.draw_rect(x, y, w, h, fill=bg, corner_radius=12)
        self.draw_text(x + (w // 2), y + (h // 2), label, size=11, fill=fg, anchor="center", weight="bold")
        return w

    def draw_divider(self, x: int, y: int, w: int, color: str = "#334155"):
        self.draw_commands.append({"type": "divider", "x": x, "y": y, "w": w, "color": color})
        if self._tk_canvas:
            self._tk_canvas.create_line(x, y, x + w, y, fill=color)

    def draw_input(self, x: int, y: int, w: int, h: int, placeholder: str = "", text: str = "", bg: str = "#1e293b", border: str = "#334155"):
        self.draw_rect(x, y, w, h, fill=bg, outline=border, corner_radius=8)
        display_text = text if text else placeholder
        color = "#f8fafc" if text else "#64748b"
        self.draw_text(x + 14, y + (h // 2), display_text, size=13, fill=color, anchor="w")

    def draw_icon(self, x: int, y: int, name: str, size: int = 18, fill: str = "#38bdf8"):
        glyph = ICON_GLYPHS.get(name.lower(), "★")
        self.draw_commands.append({"type": "icon", "x": x, "y": y, "name": name, "glyph": glyph, "size": size, "fill": fill})
        self.draw_text(x, y, glyph, size=size, fill=fill, anchor="center")

    def draw_avatar(self, x: int, y: int, size: int = 40, label: str = "U", bg: str = "#6366f1", fg: str = "#ffffff"):
        self.draw_rect(x, y, size, size, fill=bg, corner_radius=size // 2)
        initials = label[:2].upper() if label else "U"
        self.draw_text(x + (size // 2), y + (size // 2), initials, size=max(11, size // 3), fill=fg, anchor="center", weight="bold")

    def draw_switch(self, x: int, y: int, w: int = 48, h: int = 26, active: bool = False, active_color: str = "#10b981", inactive_color: str = "#334155"):
        self.draw_commands.append({"type": "switch", "x": x, "y": y, "w": w, "h": h, "active": active})
        bg = active_color if active else inactive_color
        r = h // 2
        self.draw_rect(x, y, w, h, fill=bg, corner_radius=r)
        thumb_r = (h - 6) // 2
        thumb_x = x + w - (thumb_r * 2) - 3 if active else x + 3
        thumb_y = y + 3
        self.draw_rect(thumb_x, thumb_y, thumb_r * 2, thumb_r * 2, fill="#ffffff", corner_radius=thumb_r)

    def draw_slider(self, x: int, y: int, w: int, h: int = 24, value: float = 50.0, min_v: float = 0.0, max_v: float = 100.0, active_color: str = "#6366f1", bg_color: str = "#334155"):
        self.draw_commands.append({"type": "slider", "x": x, "y": y, "w": w, "h": h, "value": value, "min": min_v, "max": max_v})
        track_h = 6
        track_y = y + (h - track_h) // 2
        self.draw_rect(x, track_y, w, track_h, fill=bg_color, corner_radius=3)
        span = max_v - min_v if max_v > min_v else 1.0
        frac = max(0.0, min(1.0, (value - min_v) / span))
        fill_w = int(w * frac)
        if fill_w > 0:
            self.draw_rect(x, track_y, fill_w, track_h, fill=active_color, corner_radius=3)
        knob_r = 7
        knob_x = x + fill_w - knob_r
        knob_y = y + (h // 2) - knob_r
        self.draw_rect(knob_x, knob_y, knob_r * 2, knob_r * 2, fill="#ffffff", outline=active_color, corner_radius=knob_r)

    def draw_tabs(self, x: int, y: int, w: int, h: int, tabs: List[str], active_idx: int = 0, bg: str = "#1e293b", active_bg: str = "#6366f1", fg: str = "#f8fafc"):
        self.draw_commands.append({"type": "tabs", "x": x, "y": y, "w": w, "h": h, "tabs": tabs, "active": active_idx})
        self.draw_rect(x, y, w, h, fill=bg, corner_radius=8)
        if not tabs:
            return
        tab_w = w // len(tabs)
        for i, tab_label in enumerate(tabs):
            tx = x + (i * tab_w)
            if i == active_idx:
                self.draw_rect(tx + 2, y + 2, tab_w - 4, h - 4, fill=active_bg, corner_radius=6)
                self.draw_text(tx + (tab_w // 2), y + (h // 2), tab_label, size=12, fill="#ffffff", anchor="center", weight="bold")
            else:
                self.draw_text(tx + (tab_w // 2), y + (h // 2), tab_label, size=12, fill="#94a3b8", anchor="center")

    def draw_toast(self, x: int, y: int, w: int, h: int, message: str, variant: str = "info", bg: str = "#1e293b", border: str = "#334155"):
        self.draw_commands.append({"type": "toast", "x": x, "y": y, "w": w, "h": h, "message": message, "variant": variant})
        variant_colors = {
            "info": "#38bdf8",
            "success": "#10b981",
            "warning": "#f59e0b",
            "danger": "#ef4444"
        }
        accent = variant_colors.get(variant, "#38bdf8")
        self.draw_shadow(x, y, w, h, corner_radius=10, elevation=2)
        self.draw_rect(x, y, w, h, fill=bg, outline=border, corner_radius=10)
        self.draw_rect(x + 2, y + 6, 4, h - 12, fill=accent, corner_radius=2)
        self.draw_text(x + 18, y + (h // 2), message, size=12, fill="#f8fafc", anchor="w", weight="bold")

    def draw_spinner(self, x: int, y: int, size: int = 24, color: str = "#6366f1"):
        self.draw_commands.append({"type": "spinner", "x": x, "y": y, "size": size, "color": color})
        if self._tk_canvas:
            self._tk_canvas.create_arc(x, y, x + size, y + size, start=45, extent=270, style="arc", outline=color, width=3)

    def draw_image(self, x: int, y: int, w: int, h: int, src: str = "", fit: str = "cover"):
        self.draw_commands.append({"type": "image", "x": x, "y": y, "w": w, "h": h, "src": src, "fit": fit})
        # Render clean frame with image placeholder glyph
        self.draw_rect(x, y, w, h, fill="#1e293b", outline="#334155", corner_radius=8)
        self.draw_icon(x + (w // 2), y + (h // 2) - 6, "sparkles", size=18, fill="#64748b")
        if src:
            filename = src.split("/")[-1].split("\\")[-1]
            self.draw_text(x + (w // 2), y + (h // 2) + 12, filename[:16], size=10, fill="#94a3b8", anchor="center")

    def draw_shimmer(self, x: int, y: int, w: int, h: int, corner_radius: int = 8, phase: float = 0.0):
        self.draw_commands.append({"type": "shimmer", "x": x, "y": y, "w": w, "h": h, "radius": corner_radius, "phase": phase})
        # Base subtle dark surface
        self.draw_rect(x, y, w, h, fill="#1e293b", corner_radius=corner_radius)
        # Dynamic wave highlight sweep
        wave_pos = (phase % 1.0)
        sweep_x = int(x + (w * wave_pos) - (w // 4))
        sweep_w = max(20, w // 3)
        if sweep_x + sweep_w > x and sweep_x < x + w:
            draw_x = max(x, sweep_x)
            draw_w = min(x + w, sweep_x + sweep_w) - draw_x
            if draw_w > 0:
                self.draw_rect(draw_x, y, draw_w, h, fill="#334155", corner_radius=corner_radius)

    def draw_skeleton(self, x: int, y: int, w: int, h: int, corner_radius: int = 6, phase: float = 0.0):
        self.draw_shimmer(x, y, w, h, corner_radius=corner_radius, phase=phase)

    def draw_glow_rect(self, x: int, y: int, w: int, h: int, fill: str = "#0f172a", glow_color: str = "#00f0ff", glow_size: int = 16, corner_radius: int = 12):
        self.draw_commands.append({"type": "glow_rect", "x": x, "y": y, "w": w, "h": h, "glow": glow_color, "size": glow_size})
        # Soft outer luminous halo
        layers = min(4, max(1, glow_size // 4))
        for i in range(layers, 0, -1):
            spread = i * 3
            interp = _interpolate_color(self.bg_color, glow_color, 0.08 * (layers - i + 1))
            self.draw_rect(x - spread, y - spread, w + (spread * 2), h + (spread * 2), fill=interp, corner_radius=corner_radius + spread)
        self.draw_rect(x, y, w, h, fill=fill, outline=glow_color, corner_radius=corner_radius)

    def draw_modal(self, x: int, y: int, w: int, h: int, title: str = "Dialog", is_open: bool = True):
        self.draw_commands.append({"type": "modal", "x": x, "y": y, "w": w, "h": h, "title": title, "open": is_open})
        if not is_open:
            return
        # Semi-transparent dark backdrop overlay
        self.draw_rect(0, 0, self.width, self.height, fill="#050811")
        # Elevated dialog box
        dialog_x = max(20, (self.width - w) // 2)
        dialog_y = max(40, (self.height - h) // 2)
        self.draw_shadow(dialog_x, dialog_y, w, h, corner_radius=16, elevation=3)
        self.draw_rect(dialog_x, dialog_y, w, h, fill="#0f172a", outline="#00f0ff", corner_radius=16)
        # Header title
        self.draw_text(dialog_x + 20, dialog_y + 18, title, size=16, fill="#f8fafc", weight="bold")
        self.draw_icon(dialog_x + w - 24, dialog_y + 26, "close", size=14, fill="#94a3b8")
        self.draw_divider(dialog_x, dialog_y + 48, w, color="#1e293b")

    def draw_accordion(self, x: int, y: int, w: int, h: int, title: str, is_open: bool = False):
        self.draw_commands.append({"type": "accordion", "x": x, "y": y, "w": w, "h": h, "title": title, "open": is_open})
        header_h = 42
        self.draw_rect(x, y, w, header_h, fill="#1e293b", outline="#334155", corner_radius=8)
        self.draw_text(x + 16, y + (header_h // 2), title, size=13, fill="#f8fafc", anchor="w", weight="bold")
        glyph = "v" if is_open else ">"
        self.draw_text(x + w - 20, y + (header_h // 2), glyph, size=12, fill="#94a3b8", anchor="center", weight="bold")
        if is_open and h > header_h:
            self.draw_rect(x, y + header_h, w, h - header_h, fill="#0f172a", outline="#334155", corner_radius=8)

    def draw_dropdown(self, x: int, y: int, w: int, h: int, items: List[str], selected_idx: int = 0, placeholder: str = "Select...", is_open: bool = False):
        self.draw_commands.append({"type": "dropdown", "x": x, "y": y, "w": w, "h": h, "items": items, "selected": selected_idx, "open": is_open})
        sel_text = items[selected_idx] if 0 <= selected_idx < len(items) else placeholder
        self.draw_rect(x, y, w, h, fill="#1e293b", outline="#00f0ff" if is_open else "#334155", corner_radius=8)
        self.draw_text(x + 14, y + (h // 2), sel_text, size=13, fill="#f8fafc", anchor="w")
        self.draw_text(x + w - 18, y + (h // 2), "▾", size=12, fill="#94a3b8", anchor="center")

    def draw_tooltip(self, x: int, y: int, text: str, position: str = "top"):
        self.draw_commands.append({"type": "tooltip", "x": x, "y": y, "text": text, "position": position})
        tip_w = len(text) * 7 + 16
        tip_h = 24
        tip_x = x - (tip_w // 2)
        tip_y = y - tip_h - 6 if position == "top" else y + 10
        self.draw_rect(tip_x, tip_y, tip_w, tip_h, fill="#0f172a", outline="#00f0ff", corner_radius=6)
        self.draw_text(tip_x + (tip_w // 2), tip_y + (tip_h // 2), text, size=11, fill="#ffffff", anchor="center")

    def draw_breadcrumbs(self, x: int, y: int, items: List[str]):
        self.draw_commands.append({"type": "breadcrumbs", "x": x, "y": y, "items": items})
        curr_x = x
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            fg = "#f8fafc" if is_last else "#94a3b8"
            self.draw_text(curr_x, y, item, size=12, fill=fg, anchor="nw", weight="bold" if is_last else "normal")
            curr_x += len(item) * 8 + 6
            if not is_last:
                self.draw_text(curr_x, y, "/", size=12, fill="#64748b", anchor="nw")
                curr_x += 14

    def draw_segmented_control(self, x: int, y: int, w: int, h: int, items: List[str], selected_idx: int = 0):
        self.draw_commands.append({"type": "segmented_control", "x": x, "y": y, "w": w, "h": h, "items": items, "selected": selected_idx})
        self.draw_rect(x, y, w, h, fill="#0f172a", outline="#334155", corner_radius=8)
        if not items:
            return
        seg_w = (w - 4) // len(items)
        for i, label in enumerate(items):
            sx = x + 2 + (i * seg_w)
            if i == selected_idx:
                self.draw_rect(sx, y + 2, seg_w, h - 4, fill="#6366f1", corner_radius=6)
                self.draw_text(sx + (seg_w // 2), y + (h // 2), label, size=12, fill="#ffffff", anchor="center", weight="bold")
            else:
                self.draw_text(sx + (seg_w // 2), y + (h // 2), label, size=12, fill="#94a3b8", anchor="center")

    def draw_stepper(self, x: int, y: int, w: int, steps: List[str], current_step: int = 0):
        self.draw_commands.append({"type": "stepper", "x": x, "y": y, "w": w, "steps": steps, "current": current_step})
        if not steps:
            return
        step_gap = w // max(1, len(steps) - 1) if len(steps) > 1 else w
        for i, step_name in enumerate(steps):
            cx = x + (i * step_gap) if len(steps) > 1 else x + (w // 2)
            cy = y + 14
            is_done = i < current_step
            is_active = i == current_step
            bg = "#10b981" if is_done else ("#6366f1" if is_active else "#334155")
            fg = "#ffffff" if (is_done or is_active) else "#94a3b8"
            self.draw_rect(cx - 12, cy - 12, 24, 24, fill=bg, corner_radius=12)
            glyph = "✓" if is_done else str(i + 1)
            self.draw_text(cx, cy, glyph, size=11, fill=fg, anchor="center", weight="bold")
            self.draw_text(cx, cy + 20, step_name, size=10, fill=fg, anchor="center")
            if i < len(steps) - 1:
                next_cx = x + ((i + 1) * step_gap)
                line_col = "#10b981" if is_done else "#334155"
                self.draw_divider(cx + 14, cy, next_cx - cx - 28, color=line_col)

    def draw_rating(self, x: int, y: int, score: float = 0.0, max_stars: int = 5):
        self.draw_commands.append({"type": "rating", "x": x, "y": y, "score": score, "max": max_stars})
        curr_x = x
        for i in range(max_stars):
            is_filled = (i + 1) <= score
            fill_col = "#f59e0b" if is_filled else "#334155"
            self.draw_icon(curr_x + 10, y + 10, "star", size=18, fill=fill_col)
            curr_x += 24

    def draw_code_block(self, x: int, y: int, w: int, h: int, code: str, lang: str = "star"):
        self.draw_commands.append({"type": "code_block", "x": x, "y": y, "w": w, "h": h, "code": code, "language": lang})
        self.draw_rect(x, y, w, h, fill="#050811", outline="#1e293b", corner_radius=8)
        # Top banner with lang badge
        self.draw_rect(x, y, w, 28, fill="#0a1020", corner_radius=8)
        self.draw_text(x + 12, y + 14, lang.upper(), size=10, fill="#38bdf8", anchor="w", weight="bold")
        # Code text lines
        lines = code.split("\n")[:max(1, (h - 36) // 18)]
        line_y = y + 36
        for l in lines:
            self.draw_text(x + 14, line_y, l, font="Courier", size=11, fill="#e2e8f0", anchor="w")
            line_y += 18

    def draw_table(self, x: int, y: int, w: int, h: int, headers: List[str], rows: List[List[str]]):
        self.draw_commands.append({"type": "table", "x": x, "y": y, "w": w, "h": h, "headers": headers, "rows": rows})
        self.draw_rect(x, y, w, h, fill="#0f172a", outline="#334155", corner_radius=8)
        if not headers:
            return
        col_w = w // max(1, len(headers))
        # Header row
        self.draw_rect(x, y, w, 32, fill="#1e293b", corner_radius=8)
        for i, header in enumerate(headers):
            hx = x + (i * col_w) + 12
            self.draw_text(hx, y + 16, header, size=11, fill="#94a3b8", anchor="w", weight="bold")
        self.draw_divider(x, y + 32, w, color="#334155")
        # Data rows
        row_y = y + 36
        for r_idx, row in enumerate(rows):
            if row_y + 26 > y + h:
                break
            bg_row = "#141e33" if r_idx % 2 == 1 else "#0f172a"
            self.draw_rect(x + 2, row_y - 2, w - 4, 26, fill=bg_row, corner_radius=4)
            for c_idx, cell in enumerate(row):
                if c_idx < len(headers):
                    cx = x + (c_idx * col_w) + 12
                    self.draw_text(cx, row_y + 11, str(cell), size=12, fill="#f8fafc", anchor="w")
            row_y += 28

    def start_ticker(self, fps: int = 60, callback: Optional[Callable[[float], None]] = None):
        """Starts 60/120 FPS frame ticker for smooth hardware-accelerated animations."""
        interval_ms = max(8, int(1000.0 / fps))
        self._ticker_active = True
        last_time = time.monotonic()

        def _tick():
            nonlocal last_time
            if not getattr(self, "_ticker_active", False):
                return
            now = time.monotonic()
            dt_sec = now - last_time
            last_time = now
            if callback:
                try:
                    callback(dt_sec)
                except Exception:
                    pass
            self.update()
            if self._tk_root and self._ticker_active:
                self._tk_root.after(interval_ms, _tick)

        if self._tk_root:
            self._tk_root.after(interval_ms, _tick)

    def stop_ticker(self):
        self._ticker_active = False

    def update(self):
        if self._tk_root:
            self._tk_root.update()

    def run(self):
        self.is_running = True
        if self._tk_root:
            self._tk_root.mainloop()

    def close(self):
        self.is_running = False
        self.stop_ticker()
        if self._tk_root:
            try:
                self._tk_root.destroy()
            except Exception:
                pass
            self._tk_root = None
            self._tk_canvas = None

