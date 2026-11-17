# 🌟 STAR UI SPECIFICATION
**Specification Version: 1.0.0**  
**Status: Authoritative Standard for Declarative UI**

---

## 1. Vision & Design Philosophy

Star UI provides a **declarative, reactive, cross-platform component model**.

Developers construct modern UI layouts using clean, pure Star functions. State updates automatically trigger runtime reconciliation and surgical window, surface, canvas, and ANSI terminal updates without manual synchronization calls.

Supported Render Targets:
- **Native Desktop**: Tkinter-backed hardware 2D canvas with anti-aliased rounded rectangles, gradients, shadows, and hover tracking.
- **Terminal UI (TUI)**: TrueColor 24-bit ANSI box-drawing renderer (`star preview <file.star>` or `star run tui`).
- **Mobile Hardware**: Android SurfaceView & iOS Metal command stream pipelines.
- **Web Platform**: WebGPU shaders & CSS3 glassmorphic design system.

---

## 2. Core Component Hierarchy

All components are accessed via `use UI`:

### 2.1 Content & Typography Components
- `UI.title(text: Text, level: Integer = 1, style: Map = {})`: Top-level bold heading (h1 to h6).
- `UI.text(content: Text, style: Map = {})`: Paragraph or label element.
- `UI.badge(label: Text, variant: Text = "primary", style: Map = {})`: Pill status indicator (`primary`, `success`, `warning`, `danger`, `accent`, `info`).
- `UI.divider(style: Map = {})`: Horizontal separation line.
- `UI.icon(name: Text, size: Integer = 20, color: Text = "")`: Vector glyph icon (e.g. `star`, `heart`, `check`, `close`, `search`, `settings`, `user`, `bell`, `arrow_right`, `chevron_right`, `plus`, `refresh`, `shield`, `zap`, `chart`, `sparkles`).
- `UI.avatar(name: Text, size: Integer = 40, style: Map = {})`: Circular user avatar with initials.
- `UI.image(src: Text, width: Integer, height: Integer, fit: Text = "cover")`: Image surface element.
- `UI.toast(message: Text, variant: Text = "info")`: Floating alert banner with accent stripe.
- `UI.spinner(size: Integer = 24, color: Text = "")`: Circular loading spinner.

### 2.2 Layout Containers
- `UI.column(...children)`: Vertical stack container with flex gap and alignment.
- `UI.row(...children)`: Horizontal flex container with automatic distribution and spacer expansion.
- `UI.stack(...children)`: Overlaid Z-index container (children layered on top of each other).
- `UI.grid(columns: Integer, ...children)`: Multi-column responsive grid layout.
- `UI.card(...children)`: Elevated surface container with subtle border, corner radius, and drop shadow.
- `UI.container(...children)` / `UI.box(...children)`: Universal styled wrapper.
- `UI.spacer(size: Integer = null)`: Flex grow space expander or fixed size gap.
- `UI.scroll(...children)`: Scrollable viewport.

### 2.3 Interactive Controls & Forms
- `UI.button(label: Text, onClick: Function, style: Map = {})`: Interactive button with hover/pressed states.
- `UI.input(placeholder: Text, onChange: Function, style: Map = {})`: Text entry field.
- `UI.checkbox(label: Text, checked: Boolean, onChange: Function)`: Toggleable checkbox.
- `UI.switch(checked: Boolean, onChange: Function)`: iOS/Material-style sliding toggle switch.
- `UI.slider(value: Decimal, min: Decimal, max: Decimal, onChange: Function)`: Range slider track with draggable knob.
- `UI.progress(value: Integer, max: Integer = 100, style: Map = {})`: Rounded progress bar with gradient fill.
- `UI.tabs(items: List, active_idx: Integer, onSelect: Function)`: Horizontal tab bar switcher.
- `UI.modal(title: Text, is_open: Boolean, on_close: Function, on_confirm: Function, ...children)`: Centered modal dialog with backdrop blur.
- `UI.dialog(title: Text, message: Text, on_confirm: Function, on_cancel: Function, is_open: Boolean)`: Quick confirmation/alert dialog.
- `UI.drawer(is_open: Boolean, side: Text = "right", on_close: Function, ...children)`: Slide-out drawer panel.
- `UI.accordion(title: Text, is_expanded: Boolean, on_toggle: Function, ...children)`: Collapsible accordion disclosure card.
- `UI.dropdown(items: List, selected_idx: Integer, on_select: Function, placeholder: Text = "Select...", is_open: Boolean = false)`: Select menu.
- `UI.tooltip(text: Text, position: Text = "top", child: VirtualNode)`: Hover-triggered contextual tooltip.
- `UI.breadcrumbs(items: List, on_select: Function)`: Hierarchical navigational breadcrumb trail.
- `UI.pagination(total_pages: Integer, current_page: Integer, on_change: Function)`: Multi-page navigation bar.
- `UI.table(headers: List, rows: List[List], options: Map = {})`: Responsive data table with striped rows.
- `UI.code_block(code: Text, language: Text = "star")`: Formatted code viewer with language badge.
- `UI.segmented_control(items: List, selected_idx: Integer, on_select: Function)`: Apple/Fluent-style pill switch.
- `UI.stepper(steps: List, current_step: Integer)`: Multi-step checkout/onboarding progress indicators.
- `UI.rating(value: Decimal, max_rating: Integer = 5, on_change: Function)`: Interactive gold star rating widget.
- `UI.fab(label: Text, onClick: Function, icon: Text = "plus", style: Map = {})`: Elevated floating action button.
- `UI.bottom_sheet(is_open: Boolean, on_close: Function, ...children)`: Mobile-first sliding bottom action sheet.

### 2.4 Hardware-Accelerated Animation & Motion Suite (`use Animation` / `use Motion`)
Star UI includes a state-of-the-art 60/120 FPS animation and physics engine:
- `UI.animated_opacity(opacity: Decimal, duration_ms: Integer = 300, curve: Text = "smooth_spring", child)`
- `UI.animated_scale(scale: Decimal, duration_ms: Integer = 300, curve: Text = "overshoot", child)`
- `UI.animated_slide(offset_x: Decimal, offset_y: Decimal, duration_ms: Integer = 300, curve: Text = "smooth_spring", child)`
- `UI.animated_rotation(angle_deg: Decimal, duration_ms: Integer = 300, curve: Text = "smooth_spring", child)`
- `UI.animated_container(width, height, bg, radius, duration_ms = 300, curve = "smooth_spring", child)`
- `UI.shimmer(width: Integer, height: Integer, radius: Integer = 8, child = null)`: Shimmer loading effect.
- `UI.skeleton(width: Integer = 200, height: Integer = 24, radius: Integer = 6)`: Placeholder skeleton bone.
- `UI.pulse(min_scale: Decimal = 0.95, max_scale: Decimal = 1.05, duration_ms: Integer = 1200, child)`
- `UI.bounce(intensity: Decimal = 10.0, duration_ms: Integer = 800, child)`
- `UI.shake(intensity: Decimal = 8.0, duration_ms: Integer = 500, child)`
- `UI.glow(color: Text = "#00f0ff", blur: Integer = 16, duration_ms: Integer = 1500, child)`
- `UI.marquee(text: Text, speed: Integer = 50)`: Smooth scrolling ticker.
- `UI.confetti(count: Integer = 50, active: Boolean = true)`: Particle celebration burst.
- `UI.ripple(color: Text = "rgba(255,255,255,0.35)", duration_ms: Integer = 600)`: Material click wave.

Supported Motion Curves:
- `linear`, `ease_in`, `ease_out`, `ease_in_out`
- `bounce_in`, `bounce_out`, `bounce_in_out`
- `elastic_in`, `elastic_out`
- `spring`, `smooth_spring`, `fast_out_slow_in`, `overshoot`
- `cubic_bezier(x1, y1, x2, y2)`

Spring Physics Simulator:
- `SpringSimulation(mass, stiffness, damping, initial_velocity)`: Solves under-damped, critically damped, and over-damped second-order differential equations in real-time.

### 2.4 Styling Utility Engine
- `UI.style(node: VirtualNode, styles: Map)`: Attaches a style dictionary to any node.
- `UI.styled(tag: Text, styles: Map, ...children)`: Constructs a styled node in a single call.

Supported Style Properties:
- `bg` / `background`: Solid hex color (`#1e293b`) or gradient tuple (`["#6366f1", "#a855f7"]`).
- `fg` / `color`: Foreground text or icon color.
- `padding`: Interior spacing (px).
- `margin`: Exterior margin (px).
- `gap`: Spacing between children.
- `radius` / `corner_radius`: Corner rounding radius.
- `border` / `border_color`: Border outline color.
- `elevation`: Shadow depth level (1, 2, 3).
- `flex`: Flex expansion factor.
- `width`, `height`: Explicit dimension overrides.

---

## 3. Design System Themes (`use Theme`)

Presets available:
- `dark`: Default slate, indigo, and sky palette.
- `light`: Clean snow, royal blue, and azure palette.
- `midnight`: OLED deep navy, electric violet, and cyan.
- `aurora`: Dark emerald, violet, and mint.
- `sunset`: Deep plum, coral, and amber.
- `cyberpunk`: Neon magenta, cyan, and electric yellow.
- `nord`: Polar arctic frost and slate.

Methods:
- `Theme.set_mode("dark" | "light")`
- `Theme.set_preset("midnight" | "aurora" | "sunset" | "cyberpunk" | "nord")`

---

## 4. Example Application (Pure Star Language)

```star
use UI
use Theme

component Dashboard
    state count = 0

    render
        UI.column(
            UI.row(
                UI.title("🌟 Star Studio"),
                UI.spacer(),
                UI.avatar("ST", 36)
            ),
            UI.card(
                UI.text("Real-time Counter: " + count),
                UI.progress(count * 10, 100),
                UI.row(
                    UI.button("- Decrement", function()
                        count = count - 1
                    end),
                    UI.button("+ Increment", function()
                        count = count + 1
                    end)
                )
            ),
            UI.toast("All platform contracts active", "success")
        )
    end
end

app DashboardApp
    Dashboard()
end
```

---

## 5. CLI Developer Workflow

- Preview UI instantly in Terminal (TUI TrueColor ANSI):
  ```bash
  star preview app.star
  ```
- Run on Native Desktop window:
  ```bash
  star run desktop app.star
  ```
- Run on Web (WebGPU & WASM):
  ```bash
  star run web app.star
  ```
- Run Mobile simulation:
  ```bash
  star simulate mobile app.star
  ```

