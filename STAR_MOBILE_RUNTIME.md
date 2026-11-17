# 📱 STAR MOBILE RUNTIME SPECIFICATION
**Specification Version: 0.8.0**  
**Status: Authoritative Standard for Mobile Runtime ABI, Render Commands & `.starmobile` Application Packaging**

---

## 1. Overview & Architecture Boundary

The Star Mobile Runtime provides a **portable, high-performance execution boundary** between Star application bytecode and platform-specific native UI layers (Android SurfaceView / iOS Metal).

```text
                  🌟 Star Source Code (.star)
                              │
                    AST → Star IR Compiler
                              │
                    Compiled Bytecode (.starb)
                              │
              ┌───────────────┴───────────────┐
              │     Mobile Packager           │
              └───────────────┬───────────────┘
                              │
              📦 Portable Bundle (.starmobile)
                              │
              ┌───────────────┴───────────────┐
              │      Star Mobile Runtime      │
              │  ┌─────────────────────────┐  │
              │  │ Mobile Runtime ABI (v1) │  │
              │  │ Capability Manager      │  │
              │  │ 2D Layout Engine        │  │
              │  │ Gesture & Touch Bridge  │  │
              │  │ Lifecycle Bridge        │  │
              │  │ Device Hardware Bridge  │  │
              │  │ Command Stream Renderer │  │
              │  └─────────────────────────┘  │
              └───────────────┬───────────────┘
                              │
             ┌────────────────┴────────────────┐
             ↓                                 ↓
   ┌────────────────────┐            ┌────────────────────┐
   │  Android Backend   │            │    iOS Backend     │
   │  (NDK / JNI Bridge)│            │(Swift/C ABI Bridge)│
   └────────────────────┘            └────────────────────┘
```

---

## 2. Portable Application Container (`.starmobile`)

A `.starmobile` bundle is a self-contained, reproducible zip archive packaging the compiled Star bytecode, manifest, security permissions, and runtime metadata:

```text
MyApp.starmobile (Zip Archive)
├── manifest.json       (Application metadata, package ID, permissions)
├── app.starb           (Compiled Star IR Bytecode binary)
├── src/main.star       (Embedded source code reference)
└── metadata.json       (ABI version, magic bytes, SHA-256 integrity checksum)
```

### 2.1 Manifest Schema (`manifest.json`)
```json
{
  "name": "Counter",
  "version": "0.8.0",
  "package_id": "org.starlang.counter",
  "entry": "counter.star",
  "orientation": "portrait",
  "permissions": [
    "vibrate",
    "storage"
  ],
  "abi_version": 1,
  "min_sdk_version": 1,
  "created_at": 1725000000.0
}
```

---

## 3. Render Command Stream (`MobileDrawCommand`)

Rather than binding to Android Canvas or iOS CoreGraphics directly in user space, the Star Mobile Runtime emits a normalized, serializable **Render Command Stream**:

| Render Opcode | Parameters | Description |
| :--- | :--- | :--- |
| `DRAW_APP_BAR` | `x, y, w, h, {title, bg, fg}` | Top mobile application header bar. |
| `DRAW_CARD` | `x, y, w, h, {bg, border, corner_radius}` | Elevated surface container with rounded corners. |
| `DRAW_BUTTON` | `x, y, w, h, {label, bg, fg, corner_radius}` | Interactive button surface. |
| `DRAW_TEXT` | `x, y, w, h, {content, font_size, weight, fg}` | Typography render command with scale-independent resolution. |
| `DRAW_SWITCH` | `x, y, w, h, {value, active_color}` | Mobile toggle switch. |
| `DRAW_SLIDER` | `x, y, w, h, {min, max, value}` | Continuous value slider. |
| `DRAW_BOTTOM_NAV` | `x, y, w, h, {items, selected, bg}` | Bottom tab bar. |
| `CLIP_RECT` | `x, y, w, h` | Clipping boundary for scrollable viewports. |

---

## 4. Capability Security & Permission Boundaries

Star Mobile uses a capability-gated security system. Hardware APIs will raise a `CapabilitySecurityError` if an undeclared capability is accessed:

```text
MobileCapability:
  - VIBRATE       ("vibrate")
  - STORAGE       ("storage")
  - BATTERY       ("battery")
  - CAMERA        ("camera")
  - GEOLOCATION   ("geolocation")
  - NETWORK       ("network")
  - CLIPBOARD     ("clipboard")
  - NOTIFICATIONS ("notifications")
```

---

## 5. Host Bridges

1. **Event Bridge (`MobileEventBridge`)**: Maps raw host OS touch events (`down`, `move`, `up`, `cancel`) to Star `TouchEvent` streams and dispatches recognized gestures to targeted layout nodes.
2. **Lifecycle Bridge (`MobileLifecycleBridge`)**: Translates host lifecycle state changes (`on_native_resume`, `on_native_pause`, `on_native_back_press`, `on_native_memory_warning`).
3. **Device Bridge (`MobileDeviceBridge`)**: Coordinates storage, battery, vibration, and clipboard access.

---

## 6. CLI Commands

```bash
# Build portable .starmobile bundle
star build mobile [entry.star]

# Run mobile application in portable runtime
star run mobile [app.starmobile | entry.star]

# Inspect runtime & backend health
star doctor
```
