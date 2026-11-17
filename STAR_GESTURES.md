# 👆 STAR GESTURE RECOGNITION SPECIFICATION & GUIDE
**Specification Version: 0.8.0**  
**Status: Authoritative Standard for Universal Multi-Touch & Gesture Architecture**

---

## 1. Vision & Architecture

Star standardizes touch inputs across Android (MotionEvents) and iOS (UITouch/UIGestureRecognizer) into a single, unified gesture stream:

```text
  Android MotionEvents ────┐
                           ├──► Star Gesture Engine ──► Universal Star Gestures
  iOS UITouch Stream   ────┘       (Heuristics Pass)       (Tap, Swipe, Pinch, ...)
```

---

## 2. Supported Universal Gestures

| Gesture | Parameters | Recognition Heuristics |
| :--- | :--- | :--- |
| **`Tap`** | `x: Integer, y: Integer` | Single contact released in $< 250\text{ ms}$ with displacement $< 12\text{ dp}$. |
| **`DoubleTap`** | `x: Integer, y: Integer` | Two successive Taps within $300\text{ ms}$ and $< 20\text{ dp}$ distance. |
| **`LongPress`** | `x: Integer, y: Integer, duration_ms: Integer` | Stationary contact held for $\ge 500\text{ ms}$. |
| **`Pan`** | `dx: Integer, dy: Integer, x: Integer, y: Integer` | Continuous single-finger movement tracking instantaneous displacement deltas. |
| **`Swipe`** | `direction: Text, velocity: Decimal, distance: Decimal` | Fast ballistic motion ($> 30\text{ dp}$, velocity $\ge 0.2\text{ dp/ms}$) emitting `"left"`, `"right"`, `"up"`, or `"down"`. |
| **`Pinch`** | `scale: Decimal, focal_x: Integer, focal_y: Integer` | Two-finger distance scaling relative to initial contact baseline. |
| **`Rotate`** | `angle: Decimal, center_x: Integer, center_y: Integer` | Two-finger rotational angular displacement relative to initial contact vector. |

---

## 3. Gesture Lifecycle & Raw Event Stream

For custom component creation or physics engines, low-level touch events are also available:
- `TouchStart`: Contact initiated.
- `TouchMove`: Touch point moved.
- `TouchEnd`: Touch released.
- `TouchCancel`: Interrupted by OS (e.g. system notification).

---

## 4. Headless Gesture Simulation

Developers can test touch and gesture sequences in CI without physical hardware:

```bash
# Run headless mobile test suite
star test mobile

# Inspect mobile application layout & safe area in headless runtime
star simulate mobile examples/mobile/gestures.star
```
