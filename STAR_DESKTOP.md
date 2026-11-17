# 🌟 STAR DESKTOP SPECIFICATION
**Specification Version: 0.6.0**  
**Status: Authoritative Standard for Native Desktop Backend & Windowing Architecture**

---

## 1. Vision & Architecture

Star Desktop provides a **native, lightweight, declarative desktop execution platform** across Windows, macOS, and Linux.

The Star Desktop platform pairs the high-performance Star Bytecode Engine with a native windowing abstraction, deterministic 2D layout calculation pass, and reactive event dispatching.

```
┌─────────────────────────────────────────────────────────────┐
│                   Star Desktop Application                  │
│                     (Declarative UI DSL)                    │
├─────────────────────────────────────────────────────────────┤
│         Star SDK Component Model & Reactive State Graph     │
├──────────────────────────────┬──────────────────────────────┤
│    Desktop Layout Engine     │   Desktop Event Subsystem    │
│  (Column / Row / Card / Flex)│ (Click, KeyPress, Resize)    │
├──────────────────────────────┴──────────────────────────────┤
│                 Desktop Window Abstraction                  │
│    (Native Window Canvas / Headless Test Surface Engine)    │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Desktop Windowing Model

The `DesktopWindow` interface specifies the cross-platform native viewport:

- **Window Lifecycle**: Configuration (`title`, `width`, `height`, `bg_color`), initialization, event loop (`run`), update frame commit (`update`), and teardown (`close`).
- **Unified 2D Canvas Primitives**:
  - `draw_rect(x, y, w, h, fill, outline, corner_radius)`
  - `draw_text(x, y, text, font, size, fill, anchor)`
  - `draw_button(x, y, w, h, label, bg, fg, corner_radius)`
  - `draw_card(x, y, w, h, bg, border)`
  - `draw_badge(x, y, label, bg, fg)`
  - `draw_divider(x, y, w, color)`
  - `draw_input(x, y, w, h, placeholder, text, bg, border)`
- **Headless Execution Mode**: Guaranteed full headless support for continuous integration (CI) and automated conformance testing without requiring an active display server or X11/Wayland/Quartz instance.

---

## 3. Layout Engine

The `DesktopRuntime` executes a dual-pass rendering pipeline:

1. **Layout Pass (`_compute_layout`)**:
   - Recursively measures bounding boxes for components (`column`, `row`, `card`, `title`, `text`, `button`, `badge`, `input`, `progress`).
   - Resolves responsive container widths, item heights, padding, and inter-element spacing.
   - Computes absolute screen coordinates for interactive hit testing.
2. **Paint Pass (`_paint_node`)**:
   - Traverses the computed `LayoutNode` hierarchy.
   - Issues optimized draw commands to the underlying `DesktopWindow` surface.
   - Registers interactive hit regions for automatic click and event dispatching.

---

## 4. Desktop Packaging & Distribution

Star applications target desktop via standard packaging pipelines:

### 4.1 Desktop Bundle Format (`.stardesktop`)
A structured JSON container packaging the compiled Star IR bytecode and native window configuration:
```json
{
  "target": "desktop",
  "version": "0.6.0",
  "entry": "src/main.star",
  "bytecode_hex": "<compiled_bytecode_hex>",
  "window": {
    "title": "Star Application",
    "width": 800,
    "height": 600,
    "resizable": true
  }
}
```

### 4.2 CLI Integration
- `star build desktop [entry.star]`: Compiles Star source code into `build/desktop/app.stardesktop`.
- `star run desktop [entry.star]`: Executes the desktop application in the native windowing environment.
- `star doctor`: Verifies desktop backend and runtime readiness.

---

## 5. Conformance & Parity

All Star declarative UI components (`UI.title`, `UI.button`, `UI.input`, `UI.card`, etc.) and reactive state workflows (`state`, `computed`, `watch`) exhibit 100% semantic parity across Desktop and Web platforms.
