# 📱 STAR DUAL-DEVICE HARDWARE VERIFICATION SPECIFICATION
**Specification Version: 0.8.7**  
**Status: Authoritative Standard for Real-Device Conformance, Probes & Stability**

---

## 1. Vision & Architecture

Star 0.8.7 establishes the formal **Dual-Device Hardware Verification Layer**, confirming that Star applications behave identically and performantly across real Android and Apple hardware:

```text
                           ⭐ Star Application
                                    │
                         Star Mobile Runtime ABI
                                    │
         ┌──────────────────────────┴──────────────────────────┐
         ▼                                                     ▼
  Android Backend                                         iOS Backend
         │                                                     │
   ADB / Native HW                                       Apple Metal / HW
         │                                                     │
         └──────────────────────────┬──────────────────────────┘
                                    ▼
                     Hardware Verification Framework
                                    │
           ┌────────────────────────┼────────────────────────┐
           ▼                        ▼                        ▼
    Capability Probes        Touch & Gestures         60 FPS Profiler
           │                        │                        │
           └────────────────────────┼────────────────────────┘
                                    ▼
                         ⭐ Release Candidate
```

---

## 2. Supported Baseline Hardware Matrix

### 2.1 Android Baselines
- **Architecture**: `ARM64-v8a`, `x86_64` (Emulator).
- **Minimum OS**: Android 8.0 (API Level 26).
- **Target OS**: Android 14.0 / 15.0 (API Level 34/35).
- **Display**: High density (320dpi - 560dpi, `xhdpi`, `xxhdpi`, `xxxhdpi`), adaptive safe area insets.

### 2.2 iOS Baselines
- **Architecture**: `ARM64` (Apple Silicon iPhone/iPad).
- **Minimum OS**: iOS 15.0 / iPadOS 15.0.
- **Target OS**: iOS 17.x / 18.x.
- **Display**: Retina (`@2x`, `@3x`), Dynamic Island insets, rounded corners, home indicators.

---

## 3. Hardware Capability Probing Standards

Probes return standardized result status descriptors:
- `SUPPORTED`: Hardware feature is present, active, and accessible.
- `UNSUPPORTED`: Physical hardware does not possess this sensor (e.g. tablet without vibration motor). Not treated as test failure.
- `PERMISSION_DENIED`: Application capability was not declared or user rejected permission request.
- `UNAVAILABLE`: Hardware sensor is temporarily disabled (e.g. location service turned off in system settings).
- `FAILED`: Bridge error occurred during operation.

---

## 4. Hardware Verification Commands

```bash
# Discover connected devices and simulators
star devices

# Run hardware verification on all targets
star test hardware

# Run hardware verification on specific platform
star test hardware --platform android
star test hardware --platform ios

# Run and record hardware telemetry session
star test hardware --record

# Check hardware toolchain diagnostics
star doctor --hardware
```
