# 🧪 STAR CROSS-PLATFORM CONFORMANCE SPECIFICATION
**Specification Version: 0.8.5**  
**Status: Authoritative Standard for Cross-Platform Contract Verification across Web, Desktop, Android & iOS**

---

## 1. Conformance Principle

A platform provider is defined as **Conformant** when 100% of the defined Star Portable Contracts execute with identical observable semantics and return types without requiring target-specific branching in Star user code.

```text
                  Conformance Test Suite
                            │
       ┌────────────┬───────┴────────┬────────────┐
       ↓            ↓                ↓            ↓
  Web Provider  Desktop Prov   Android Prov   iOS Provider
       │            │                │            │
       └────────────┴───────┬────────┴────────────┘
                            ↓
               Identical Assertions Evaluated
```

---

## 2. Tested Contract Matrix

| Contract Name | Module | Verification Rules |
| :--- | :--- | :--- |
| **Storage Contract** | `Mobile.Storage` | `set()`, `get()`, `remove()` roundtripping and `CapabilitySecurityError` enforcement. |
| **Battery Contract** | `Mobile.Battery` | `level()` returns float in `[0.0, 1.0]`, `is_charging()` returns boolean. |
| **Haptics Contract** | `Mobile.Haptics`, `Mobile.Vibrate` | `impact()` styles ("light", "medium", "heavy"), `notification()` ("success", "warning", "error"). |
| **Clipboard Contract** | `Mobile.Clipboard` | `set()` and `get()` text synchronization and capability gating. |
| **Orientation Contract** | `Mobile.Orientation` | `current()`, `lock()`, `unlock()` state handling. |
| **Screen Metrics** | `Mobile.Screen` | `width_dp()`, `height_dp()`, `scale_factor()`, `orientation()`. |
| **Lifecycle Contract** | `MobileLifecycle` | State transitions (`Mounted` $\to$ `Resumed` $\to$ `Paused` $\to$ `Detached`). |
| **Gesture Contract** | `GestureEngine` | `Tap`, `Swipe`, `Pan`, `Pinch`, `Rotate` velocity & pointer recognition. |
| **Safe Area Insets** | `SafeAreaInsets` | Dynamic Island, notch, and navigation bar rectangle padding. |
| **UI Components** | `UI.*` | `app_bar`, `scroll_view`, `switch`, `slider`, `button` VNode hierarchy. |

---

## 3. Conformance Execution Tooling

```bash
# Execute Cross-Platform Conformance Matrix
star test --target all

# Or alias
star test --conformance
```
