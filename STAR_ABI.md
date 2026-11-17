# 🔒 STAR RUNTIME ABI & MOBILE ABI SPECIFICATION
**Specification Version: 0.9.0 Release Candidate**  
**Status: Locked & Frozen Standard (Core ABI v1 · Mobile ABI v1)**

---

## 1. ABI Freezing & Compatibility Contract

As of **Star 0.9.0 RC**, the Star Runtime ABI and Mobile ABI are formally frozen under semantic versioning guarantees:
- **Core Runtime ABI Version**: `1`
- **Mobile Runtime ABI Version**: `1`
- **Tagged Value Layout**: Fixed 64-bit tagged word representation.
- **Backward Compatibility**: All compiled `.starb` and `.starmobile` artifacts produced with ABI v1 are guaranteed forward-compatible across future Star 1.x runtimes. Breaking changes will not occur prior to Star 2.0.

---

## 2. Core VM ABI Layout (v1)

### 2.1 Value Tagging Representation
```text
┌────────────────────────────────────────────────────────┬───────────────┐
│                    Payload (56 bits)                   │  Tag (8 bits) │
└────────────────────────────────────────────────────────┴───────────────┘
```
- `0x00`: `None` / Nil
- `0x01`: `Boolean` (0 = false, 1 = true)
- `0x02`: `Integer` (Signed 64-bit integer payload)
- `0x03`: `Decimal` (IEEE 754 double precision float)
- `0x04`: `Text` (Heap pointer to UTF-8 length-prefixed string)
- `0x05`: `List` (Heap pointer to dynamic array structure)
- `0x06`: `Map` (Heap pointer to hash table structure)
- `0x07`: `Function` (Function index and capture environment pointer)
- `0x08`: `NativePointer` (Foreign Function Interface raw pointer)

---

## 3. Mobile Runtime ABI Layout (v1)

### 3.1 Mobile Render Operations (`MobileRenderOp`)
The binary draw command stream is encoded as 32-bit aligned operation descriptors:
- `0x70`: `DRAW_SAFE_AREA`
- `0x71`: `DRAW_SCROLL_VIEW`
- `0x72`: `DRAW_APP_BAR`
- `0x73`: `DRAW_BOTTOM_NAV`
- `0x74`: `DRAW_CARD`
- `0x75`: `DRAW_BUTTON`
- `0x76`: `DRAW_TEXT`
- `0x77`: `DRAW_SWITCH`
- `0x78`: `DRAW_SLIDER`
- `0x79`: `DRAW_ACTION_SHEET`
- `0x7A`: `CLIP_RECT`

### 3.2 Mobile Event Protocol
Host platforms (Android `StarActivity`, iOS `StarViewController`, Desktop `DesktopWindow`, Web `DOMDriver`) communicate with Star via standardized event records:
- `TouchDown(pointer_id, x_dp, y_dp, timestamp_ms)`
- `TouchMove(pointer_id, x_dp, y_dp, timestamp_ms)`
- `TouchUp(pointer_id, x_dp, y_dp, timestamp_ms)`
- `TouchCancel(pointer_id, timestamp_ms)`
- `LifecycleTransition(state)`: `mounted` $\to$ `resumed` $\to$ `paused` $\to$ `detached`
- `MemoryWarning(severity)`: `low` | `critical`
- `SafeAreaChanged(top_dp, bottom_dp, left_dp, right_dp)`
- `OrientationChanged(orientation)`: `portrait` | `landscape`

---

## 4. Universal `Mobile.*` Public Contract Freeze

All public modules under `use Mobile` are frozen with strict parameter schemas:
- `Mobile.Storage`: `get(key: Text) -> Text`, `set(key: Text, val: Text)`, `remove(key: Text)`, `clear()`
- `Mobile.Battery`: `level() -> Integer`, `is_charging() -> Boolean`
- `Mobile.Haptics`: `impact(style: Text)`, `notification(type: Text)`, `selection()`
- `Mobile.Vibrate`: `start(duration_ms: Integer)`, `cancel()`
- `Mobile.Clipboard`: `get() -> Text`, `set(content: Text)`
- `Mobile.Screen`: `width_dp() -> Decimal`, `height_dp() -> Decimal`, `scale_factor() -> Decimal`, `orientation() -> Text`
- `Mobile.Orientation`: `current() -> Text`, `lock(mode: Text)`, `unlock()`
- `Mobile.Share`: `share_text(text: Text, title: Text)`
- `Mobile.Network`: `status() -> Text`, `is_connected() -> Boolean`
- `Mobile.Geolocation`: `is_available() -> Boolean`, `current_position() -> Map`
- `Mobile.Camera`: `is_available() -> Boolean`
