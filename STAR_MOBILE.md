# 🌟 STAR MOBILE SPECIFICATION
**Specification Version: 0.8.0**  
**Status: Authoritative Standard for Mobile Platforms (Android & iOS) & Native SDK Architecture**

---

## 1. Vision & Architecture Philosophy

Star Mobile provides a **lightweight, native, high-performance execution platform** for mobile devices (Android and iOS) using a single, unified Star codebase.

### 1.1 Core Principles
1. **One Star Codebase**: Write identical declarative UI, business logic, and reactive state across Web, Desktop, and Mobile.
2. **Strict Runtime Decoupling**: Language syntax and UI component APIs remain 100% platform-independent. All platform-specific details (Android NDK/JNI/SurfaceView vs iOS Metal/UIKit/Swift) remain encapsulated behind portable runtime abstractions.
3. **Standardized Gesture & Touch Model**: Input events are normalized into universal gestures (`Tap`, `DoubleTap`, `LongPress`, `Pan`, `Swipe`, `Pinch`, `Rotate`) rather than exposing fragmented native OS event APIs.
4. **Adaptive & Safe-Area Aware**: Built-in support for density-independent pixels (`dp`), scale-independent text (`sp`), device notches, dynamic islands, and system navigation bars.
5. **Headless Verification First**: Complete headless execution mode allowing full automated testing, gesture simulation, and lifecycle verification in CI pipelines without requiring a physical device or emulator.

---

## 2. Platform Architecture & Compilation Flow

```text
                  🌟 Star Source Code (.star)
                              │
                    Lexer & Pratt Parser
                              │
                     Semantic Analyzer
                              │
                    AST → Star IR Compiler
                              │
                  Star Bytecode (.starb / IR)
                              │
              ┌───────────────┴───────────────┐
              │   Star Mobile Runtime ABI     │
              │  (Layout, Gestures, Lifecycle)│
              └───────────────┬───────────────┘
                              │
             ┌────────────────┴────────────────┐
             ↓                                 ↓
   ┌────────────────────┐            ┌────────────────────┐
   │  Android Backend   │            │    iOS Backend     │
   │  (NDK / JNI Bridge)│            │(Swift/C ABI Bridge)│
   ├────────────────────┤            ├────────────────────┤
   │ Android SurfaceView│            │ Metal / Quartz Core│
   │ Skia/Vulkan Canvas │            │ Render Pipeline    │
   └─────────┬──────────┘            └─────────┬──────────┘
             ↓                                 ↓
     🤖 Android APK / AAB              🍎 iOS IPA / App
```

---

## 3. Touch & Gesture Model

Star standardizes touch interactions into a deterministic gesture recognition hierarchy.

### 3.1 Gesture Event Categories

| Event Name | Parameters | Description |
| :--- | :--- | :--- |
| `Tap` | `x: Integer, y: Integer` | Single instantaneous contact release within touch slop threshold (< 250ms). |
| `DoubleTap` | `x: Integer, y: Integer` | Two successive taps within 300ms window. |
| `LongPress` | `x: Integer, y: Integer, duration_ms: Integer` | Continuous contact exceeding 500ms without significant displacement. |
| `Pan` | `dx: Integer, dy: Integer, x: Integer, y: Integer` | Continuous movement tracking delta displacement. |
| `Swipe` | `direction: Text, velocity: Decimal` | Fast ballistic motion (`"left"`, `"right"`, `"up"`, `"down"`). |
| `Pinch` | `scale: Decimal, focal_x: Integer, focal_y: Integer` | Multi-touch pinch-to-zoom / scale interaction. |
| `Rotate` | `angle: Decimal, center_x: Integer, center_y: Integer` | Two-finger rotational gesture. |
| `TouchStart` | `touches: List[TouchPoint]` | Raw low-level touch contact initiated. |
| `TouchMove` | `touches: List[TouchPoint]` | Raw low-level touch contact coordinates updated. |
| `TouchEnd` | `touches: List[TouchPoint]` | Raw low-level touch contact terminated. |
| `TouchCancel`| `reason: Text` | System-interrupted touch sequence (e.g. incoming phone call). |

### 3.2 Declarative Event Binding

Events can be bound directly to components or listened to via the gesture subsystem:

```text
use UI
use Mobile

app GestureDemo

    variable message = "Interact with me"

    render
        UI.card(
            UI.text(message)
        )
        on Swipe(direction, velocity)
            message = "Swiped: " + direction + " (velocity: " + velocity + ")"
        end
        on DoubleTap(x, y)
            message = "Double tapped at (" + x + ", " + y + ")"
        end
    end

end
```

---

## 4. Mobile Lifecycle Model

Mobile applications must respond deterministically to operating system lifecycle transitions.

```text
    [App Launched]
          │
          ↓
     ┌─────────┐      resume()
     │ Mounted ├──────────────────┐
     └────┬────┘                  │
          │                       ↓
          │                  ┌─────────┐
          │                  │ Resumed │ ◄── (Active / Foreground)
          │                  └────┬────┘
          │                       │
          │                       │ pause()
          │                       ↓
          │                  ┌─────────┐
          │                  │ Paused  │ ◄── (Backgrounded)
          │                  └────┬────┘
          │                       │
          │                       │ detach()
          ↓                       ↓
     ┌─────────────────────────────────┐
     │            Detached             │ ◄── (Terminated)
     └─────────────────────────────────┘
```

### 4.1 Lifecycle States
- **`Mounted`**: App instance created and virtual component tree mounted.
- **`Resumed` (`Foreground`)**: Application is active, visible, and receiving touch/sensor inputs.
- **`Paused` (`Background`)**: Application is in background, rendering paused, battery consumption minimized.
- **`Detached`**: Application is being destroyed by the operating system.

### 4.2 Lifecycle Event Hooks

```text
use Mobile

app LifecycleDemo

    Mobile.on_resume(function()
        IO.println("App returned to foreground")
    end)

    Mobile.on_pause(function()
        IO.println("App moved to background - saving state")
        Mobile.Storage.set("last_active", Time.now())
    end)

    Mobile.on_back_press(function()
        // Return true to prevent default system back navigation
        IO.println("Hardware back button pressed")
        return false
    end)

    Mobile.on_memory_warning(function()
        IO.println("Low memory warning received - clearing cache")
    end)

end
```

---

## 5. Adaptive Layout & Safe-Area Sizing

Mobile devices feature diverse screen geometries, pixel densities, notches, and navigation bars.

### 5.1 Unit System
- **`dp` (Density-independent Pixels)**: Scaled by device screen density ($1\text{ dp} = 1\text{ px}$ at 160 DPI).
- **`sp` (Scale-independent Pixels)**: Scaled by both device pixel density and user accessibility font scale preferences.
- **`%` (Percentage Units)**: Relative fraction of parent container dimensions.

### 5.2 Safe-Area Inset Model

The `SafeArea` container queries native display insets and pads content away from hardware cutouts, dynamic islands, status bars, and home indicators:

```text
┌─────────────────────────────────────────┐
│ ▲ Top Inset (Status Bar / Notch)        │
├─────────────────────────────────────────┤
│ ◄ Left Inset     SAFE AREA    Right Inset ►│
│                  VIEWPORT               │
├─────────────────────────────────────────┤
│ ▼ Bottom Inset (Home Indicator Bar)     │
└─────────────────────────────────────────┘
```

### 5.3 Sizing & Adaptive Example

```text
use UI

app AdaptiveView

    render
        UI.safe_area(
            UI.column(
                UI.title("Responsive Mobile View"),
                UI.card(
                    UI.text("Padded cleanly away from all notches and home bars.")
                )
            )
        )
    end

end
```

---

## 6. Portable Mobile UI Component Contracts

Star 0.8 introduces dedicated mobile-optimized declarative UI components extending the unified `UI` subsystem:

| Component | Signature | Description |
| :--- | :--- | :--- |
| `UI.safe_area` | `UI.safe_area(...children)` | Container applying automatic padding for device cutouts and navigation bars. |
| `UI.scroll_view` | `UI.scroll_view(...children, orientation = "vertical")` | Scrollable container with momentum physics and overscroll bounce. |
| `UI.app_bar` | `UI.app_bar(title: Text, leading = nil, actions = [])` | Standard mobile header bar with optional back navigation and action icons. |
| `UI.bottom_navigation` | `UI.bottom_navigation(items: List, selected: Integer, onSelect: Function)` | Bottom tab bar for top-level application navigation. |
| `UI.switch` | `UI.switch(value: Boolean, onChange: Function)` | Mobile toggle switch with native haptic feedback. |
| `UI.slider` | `UI.slider(min: Decimal, max: Decimal, value: Decimal, onChange: Function)` | Continuous value slider. |
| `UI.action_sheet` | `UI.action_sheet(title: Text, actions: List[Action])` | Bottom modal action picker. |

---

## 7. Star Mobile Device SDK (`use Mobile`)

The `Mobile` module provides capability-gated access to native hardware and platform services:

### 7.1 Haptics & Vibration
```text
Mobile.Vibrate()                     // Standard 100ms vibration
Mobile.Vibrate(pattern = [0, 100, 50, 200]) // Custom pattern
Mobile.Haptics.impact("light")       // "light" | "medium" | "heavy"
Mobile.Haptics.notification("success")// "success" | "warning" | "error"
```

### 7.2 Secure Key-Value Storage
Backed by Android EncryptedSharedPreferences and iOS Keychain:
```text
Mobile.Storage.set("auth_token", "sec_token_98765")
variable token = Mobile.Storage.get("auth_token")
Mobile.Storage.remove("auth_token")
Mobile.Storage.clear()
```

### 7.3 Battery & Power Management
```text
variable level = Mobile.Battery.level()           // Decimal (0.0 to 1.0)
variable isCharging = Mobile.Battery.is_charging() // Boolean
variable powerMode = Mobile.Battery.power_save()  // Boolean
```

### 7.4 Orientation & Display Metrics
```text
variable current = Mobile.Orientation.current()   // "portrait" | "landscape"
Mobile.Orientation.lock("portrait")               // "portrait" | "landscape" | "unlock"

variable width = Mobile.Screen.width_dp()
variable height = Mobile.Screen.height_dp()
variable scale = Mobile.Screen.scale_factor()
```

### 7.5 Clipboard & Share
```text
Mobile.Clipboard.set("https://starlang.org")
variable text = Mobile.Clipboard.get()

Mobile.Share.text("Check out Star Language!", title = "Share Star")
```

---

## 8. Mobile Runtime ABI & Headless Test Harness

### 8.1 Runtime Interface Contracts

```python
class IMobileWindow:
    def get_safe_area_insets(self) -> Tuple[int, int, int, int]: ...
    def get_screen_metrics(self) -> Tuple[int, int, float]: ...
    def set_orientation(self, mode: str) -> None: ...

class IMobileTouchDispatcher:
    def inject_touch_start(self, touch_id: int, x: int, y: int) -> None: ...
    def inject_touch_move(self, touch_id: int, x: int, y: int) -> None: ...
    def inject_touch_end(self, touch_id: int, x: int, y: int) -> None: ...
    def inject_gesture(self, gesture_name: str, payload: dict) -> None: ...

class IMobileLifecycleManager:
    def transition_to(self, state: str) -> None: ...
    def dispatch_back_press(self) -> bool: ...
```

### 8.2 Headless Test Engine
The `MobileHeadlessRuntime` allows writing automated unit and integration tests for touch gestures, device rotation, and lifecycle state changes without physical devices:

```python
runtime = MobileHeadlessRuntime(app_bytecode)
runtime.mount()

# Simulate device rotation
runtime.set_orientation("landscape")

# Simulate touch gesture
runtime.inject_tap(x=150, y=200)

# Simulate lifecycle transition
runtime.transition_lifecycle("paused")
runtime.transition_lifecycle("resumed")

assert runtime.get_state("count") == 1
```

---

## 9. Mobile Packaging & Project Configuration

### 9.1 Project Manifest (`star.toml`)

```toml
[project]
name = "star_counter_app"
version = "0.8.0"

[mobile]
package_id = "org.starlang.counter"
app_name = "Star Counter"
orientation = "portrait"
version_code = 1
permissions = [
    "vibrate",
    "storage",
    "network"
]

[mobile.android]
min_sdk = 24
target_sdk = 34

[mobile.ios]
min_ios = "15.0"
bundle_identifier = "org.starlang.counter"
```

### 9.2 Mobile Distribution Container (`.starmobile`)
A structured bundle packaging IR bytecode, asset manifests, mobile display metadata, and capability declarations:

```json
{
  "target": "mobile",
  "version": "0.8.0",
  "package_id": "org.starlang.counter",
  "entry": "src/main.star",
  "bytecode_hex": "<compiled_bytecode_hex>",
  "manifest": {
    "orientation": "portrait",
    "permissions": ["vibrate", "storage"],
    "safe_area_mode": "adaptive"
  }
}
```

### 9.3 CLI Integration

```bash
# Build mobile package bundle (.starmobile)
star build mobile [entry.star]

# Build native packages
star build apk [--release]
star build ipa [--release]

# Execute in simulator / connected device
star run android [--device <id>]
star run ios [--simulator <name>]
```

---

## 10. Conformance & Parity Guarantees

All Star declarative UI components, reactive state semantics, standard libraries, and developer productivity tools (LSP, DevTools, Debugger, Doctor) maintain **100% semantic parity across Web, Desktop, and Mobile**.
