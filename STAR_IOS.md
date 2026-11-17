# 🍎 STAR IOS NATIVE BACKEND SPECIFICATION
**Specification Version: 0.8.0**  
**Status: Authoritative Standard for Apple iOS / Swift C ABI, Metal GPU Rendering, UIKit Lifecycle & Xcode Toolchain**

---

## 1. Vision & Architecture

The Star iOS Native Backend provides native Apple platform execution for Star mobile applications using the high-performance StarVM bytecode engine, a Swift / C ABI bridge, hardware-accelerated Apple Metal rendering via MetalKit, and direct iOS platform framework integrations.

```text
                  🌟 Star Source Code (.star)
                              │
                    AST → Star IR Compiler
                              │
                  Star Bytecode (.starb / IR)
                              │
                  📦 .starmobile Bundle
                              │
              ┌───────────────┴───────────────┐
              │       iOS Builder             │
              │  (Xcode Project Generator)    │
              └───────────────┬───────────────┘
                              │
             ┌────────────────┴────────────────┐
             ↓                                 ↓
   ┌────────────────────┐            ┌────────────────────┐
   │ UIKit / Swift Host │ ◄── C ABI ─►│   Star Native C    │
   │(StarViewController)│            │ (StarVM / Runtime) │
   ├────────────────────┤            ├────────────────────┤
   │ StarMetalView      │            │ Layout Engine      │
   │ iOSTouchBridge     │            │ Gesture Recognizer │
   │ iOSDeviceBridge    │            │ Command Stream Gen │
   └─────────┬──────────┘            └─────────┬──────────┘
             ↓                                 ↓
     🍎 iOS IPA / App Distribution Package
```

---

## 2. Swift / C ABI Native Interface

The iOS runtime communicates with StarVM through high-speed, zero-overhead C ABI native interfaces defined in `StarRuntime.h` and accessed via `StarNativeBridge.swift`:

```c
#ifndef STAR_IOS_RUNTIME_H
#define STAR_IOS_RUNTIME_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

bool star_ios_init_runtime(const char* app_name, float width, float height, float scale);
bool star_ios_load_bytecode(const uint8_t* bytes, size_t length);
void star_ios_dispatch_touch(int phase, int touch_id, float x, float y, float force);
const char* star_ios_render_frame(void);
void star_ios_dispatch_lifecycle(const char* state);
bool star_ios_dispatch_back_press(void);
void star_ios_set_safe_area(float top, float bottom, float left, float right);

#ifdef __cplusplus
}
#endif

#endif
```

---

## 3. UIKit View Controller & Lifecycle Mapping

Host iOS Application / View Controller lifecycle callbacks map directly into Star lifecycle states:

| UIKit / UIApplication Callback | Star Lifecycle State | Action |
| :--- | :--- | :--- |
| `viewDidLoad()` | `Mounted` | Viewport initialized, Swift runtime bound. |
| `viewDidAppear()` / `applicationDidBecomeActive` | `Resumed` | Metal render loop active, touch inputs accepted. `Mobile.on_resume()` executed. |
| `viewDidDisappear()` / `applicationDidEnterBackground` | `Paused` | Rendering paused, power consumption throttled. `Mobile.on_pause()` executed. |
| `applicationWillTerminate()` | `Detached` | Resources released, VM teardown. |
| `viewSafeAreaInsetsDidChange()` | Safe Area Update | Notifies Star Layout of Dynamic Island, notch, and home bar insets. |
| `didReceiveMemoryWarning()` | Warning Hook | `Mobile.on_memory_warning()` executed to purge cached assets. |

---

## 4. Input & UITouch Bridge

Apple `UITouch` event phases are converted into normalized Star touch streams:

| UITouch Event Phase | Star TouchPhase | Recognition Result |
| :--- | :--- | :--- |
| `touchesBegan` | `TouchStart` | Contact initiated, touch hash registered with pressure force. |
| `touchesMoved` | `TouchMove` | Coordinates tracked for `Pan`, `Pinch`, `Rotate`. |
| `touchesEnded` | `TouchEnd` | Contact released, evaluated for `Tap`, `DoubleTap`, `LongPress`, `Swipe`. |
| `touchesCancelled` | `TouchCancel` | Active touch sequence cleared. |

---

## 5. Apple Platform Frameworks Bridge

Star Mobile APIs seamlessly map to native iOS frameworks:

- **Haptics**: Maps to `UIImpactFeedbackGenerator` and `UINotificationFeedbackGenerator`.
- **Storage**: Backed by Apple Keychain Services (`kSecClassGenericPassword`).
- **Battery**: Queries `UIDevice.current.batteryLevel` and `batteryState`.
- **Clipboard**: Reads/writes `UIPasteboard.general`.
- **Share**: Invokes `UIActivityViewController`.

---

## 6. Star Inbuild System & Star SDK IPA Packaging

iOS compilation in Star is powered by the **Star Inbuild System & Star SDKs**. Unlike traditional workflows that mandate macOS hardware and full Xcode installations, Star's Inbuild System compiles and packages complete, compliant iOS IPAs directly on Windows, Linux, and macOS.

### Key Inbuild Capabilities:
* **Zero-Mac Cross-Platform Compilation**: Assembles `Payload/<AppName>.app` containers directly with ARM64 Mach-O headers and standard `_CodeSignature/CodeResources`.
* **Built-in Apple MetalKit Shaders**: Translates Star declarative layouts to hardware-accelerated Metal pipelines.
* **Xcode Project Scaffolding**: Automatically outputs a clean Xcode project for developers who wish to open it on a Mac:

```text
build/ios/project/
├── <AppName>.xcodeproj/
│   └── project.pbxproj
└── <AppName>/
    ├── Info.plist
    ├── AppDelegate.swift
    ├── StarViewController.swift
    ├── StarMetalView.swift
    ├── StarNativeBridge.swift
    ├── StarRuntime.h
    └── Resources/
        └── app.starmobile
```

---

## 7. CLI Commands & Artifact Targets

```bash
# Build standalone Xcode project
star build ios [entry.star]

# Build iOS IPA package (Payload/<App>.app container)
star build ipa [--release] [entry.star]

# Run on booted iOS Simulator or simulated Metal host
star run ios [entry.star | app.ipa | app.starmobile]

# Inspect toolchain readiness
star doctor
```
