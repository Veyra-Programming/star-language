# 📱 STAR NATIVE DEVICE HARDWARE SDK SPECIFICATION
**Specification Version: 0.8.5**  
**Status: Authoritative Standard for Universal Hardware APIs across Web, Desktop, Android & iOS**

---

## 1. Vision & Architecture

The Star Native Device SDK provides a universal, cross-platform hardware interface (`use Mobile`). The observable semantics, method signatures, return structures, and permission behaviors are **100% identical** across all supported targets:

```text
                    ⭐ Star Application Code
                              │
                      use Mobile / use UI
                              │
                    CapabilityManager (Security)
                              │
                    IDeviceProvider Interface
                              │
        ┌──────────────┬──────┴──────┬──────────────┐
        ↓              ↓             ↓              ↓
   Web Provider   Desktop Prov   Android Prov   iOS Provider
     (WASM/DOM)     (Native OS)   (JVM / JNI)   (Swift / C ABI)
        │              │             │              │
   localStorage   OS Keyring     EncryptedPrefs  Keychain
   Clipboard      OS Clipboard   ClipboardMgr    UIPasteboard
   Navigator      Power APIs     BatteryMgr      UIDevice
   Vibration      Haptic Stub    Vibrator        UIFeedback
```

---

## 2. Capability Security Layer

Every hardware API invocation passes through `CapabilityManager.require(MobileCapability.<CAP>)`.
If a capability is undeclared or revoked, Star throws a `CapabilitySecurityError` with remediation instructions:

| Capability | Module API | Default Status |
| :--- | :--- | :--- |
| `STORAGE` | `Mobile.Storage` | Granted |
| `BATTERY` | `Mobile.Battery` | Granted |
| `VIBRATE` | `Mobile.Haptics`, `Mobile.Vibrate` | Granted |
| `CLIPBOARD` | `Mobile.Clipboard` | Granted |
| `NETWORK` | `Mobile.Network` | Granted |
| `GEOLOCATION` | `Mobile.Geolocation` | Gated (Requires User Permission) |
| `CAMERA` | `Mobile.Camera` | Gated (Requires User Permission) |

---

## 3. Core Device APIs

### 3.1 Storage (`Mobile.Storage`)
```star
use Mobile

// Set secure persistent key-value pair
Mobile.Storage.set("session_token", "abc123xyz")

// Retrieve stored value
variable token = Mobile.Storage.get("session_token")

// Remove key
Mobile.Storage.remove("session_token")
```

### 3.2 Battery (`Mobile.Battery`)
```star
use Mobile

variable level = Mobile.Battery.level()        // Float: 0.0 to 1.0
variable charging = Mobile.Battery.is_charging() // Boolean: true/false
```

### 3.3 Haptics & Vibration (`Mobile.Haptics` & `Mobile.Vibrate`)
```star
use Mobile

// Light / Medium / Heavy impact feedback
Mobile.Haptics.impact("medium")

// Notification feedback: "success", "warning", "error"
Mobile.Haptics.notification("success")

// Raw vibration duration (ms)
Mobile.Vibrate(100)
```

### 3.4 Clipboard (`Mobile.Clipboard`)
```star
use Mobile

Mobile.Clipboard.set("Copied text from Star app")
variable text = Mobile.Clipboard.get()
```

### 3.5 Screen & Viewport (`Mobile.Screen`)
```star
use Mobile

variable w = Mobile.Screen.width_dp()
variable h = Mobile.Screen.height_dp()
variable scale = Mobile.Screen.scale_factor()
variable orientation = Mobile.Screen.orientation() // "portrait" / "landscape"
```

### 3.6 Orientation Control (`Mobile.Orientation`)
```star
use Mobile

variable current = Mobile.Orientation.current()
Mobile.Orientation.lock("landscape")
Mobile.Orientation.unlock()
```

### 3.7 Share (`Mobile.Share`)
```star
use Mobile

Mobile.Share.text("Check out Star 0.8.5!", "Star Language")
```

### 3.8 Network Status (`Mobile.Network`)
```star
use Mobile

variable status = Mobile.Network.status()       // "wifi", "cellular", "none"
variable connected = Mobile.Network.is_connected() // true / false
```
