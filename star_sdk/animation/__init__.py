"""
🌟 Star UI Animation & Motion Engine
Authoritative Reference: STAR_UI.md
Architected for Hardware-Accelerated 60/120 FPS Native & Web Motion
"""

import math
import time
from typing import Dict, List, Any, Optional, Callable, Tuple, Union
from star_engine.types import (
    StarValue, StarNull, StarText, StarInteger, StarDecimal, StarBoolean,
    StarList, StarMap, StarFunction, StarBuiltinFunction, StarModule,
    StarVirtualNode
)


# ============================================================================
# 1. EASING CURVES & MATHEMATICAL INTERPOLATORS
# ============================================================================

def _bezier_solve(x1: float, y1: float, x2: float, y2: float) -> Callable[[float], float]:
    """Cubic Bezier curve solver using Newton-Raphson approximation."""
    def _sample_curve_x(t: float) -> float:
        return ((1.0 - 3.0 * x2 + 3.0 * x1) * t + (3.0 * x2 - 6.0 * x1)) * t * t + 3.0 * x1 * t

    def _sample_curve_y(t: float) -> float:
        return ((1.0 - 3.0 * y2 + 3.0 * y1) * t + (3.0 * y2 - 6.0 * y1)) * t * t + 3.0 * y1 * t

    def _sample_curve_derivative_x(t: float) -> float:
        return (3.0 * (1.0 - 3.0 * x2 + 3.0 * x1) * t + 2.0 * (3.0 * x2 - 6.0 * x1)) * t + 3.0 * x1

    def _curve(x: float) -> float:
        if x <= 0.0:
            return 0.0
        if x >= 1.0:
            return 1.0
        t2 = x
        for _ in range(8):
            x2_val = _sample_curve_x(t2) - x
            if abs(x2_val) < 1e-6:
                return _sample_curve_y(t2)
            d2 = _sample_curve_derivative_x(t2)
            if abs(d2) < 1e-6:
                break
            t2 = t2 - x2_val / d2
        t0 = 0.0
        t1 = 1.0
        t2 = x
        while t0 < t1:
            x2_val = _sample_curve_x(t2)
            if abs(x2_val - x) < 1e-6:
                return _sample_curve_y(t2)
            if x > x2_val:
                t0 = t2
            else:
                t1 = t2
            t2 = (t1 - t0) * 0.5 + t0
        return _sample_curve_y(t2)

    return _curve


class Curves:
    @staticmethod
    def linear(t: float) -> float:
        return max(0.0, min(1.0, t))

    @staticmethod
    def ease_in(t: float) -> float:
        t = max(0.0, min(1.0, t))
        return t * t

    @staticmethod
    def ease_out(t: float) -> float:
        t = max(0.0, min(1.0, t))
        return t * (2.0 - t)

    @staticmethod
    def ease_in_out(t: float) -> float:
        t = max(0.0, min(1.0, t))
        if t < 0.5:
            return 2.0 * t * t
        return -1.0 + (4.0 - 2.0 * t) * t

    @staticmethod
    def bounce_out(t: float) -> float:
        t = max(0.0, min(1.0, t))
        n1 = 7.5625
        d1 = 2.75
        if t < 1.0 / d1:
            return n1 * t * t
        elif t < 2.0 / d1:
            t -= 1.5 / d1
            return n1 * t * t + 0.75
        elif t < 2.5 / d1:
            t -= 2.25 / d1
            return n1 * t * t + 0.9375
        else:
            t -= 2.625 / d1
            return n1 * t * t + 0.984375

    @staticmethod
    def bounce_in(t: float) -> float:
        return 1.0 - Curves.bounce_out(1.0 - t)

    @staticmethod
    def bounce_in_out(t: float) -> float:
        if t < 0.5:
            return Curves.bounce_in(t * 2.0) * 0.5
        return Curves.bounce_out(t * 2.0 - 1.0) * 0.5 + 0.5

    @staticmethod
    def elastic_out(t: float) -> float:
        t = max(0.0, min(1.0, t))
        if t == 0.0 or t == 1.0:
            return t
        p = 0.3
        s = p / 4.0
        return math.pow(2.0, -10.0 * t) * math.sin((t - s) * (2.0 * math.pi) / p) + 1.0

    @staticmethod
    def elastic_in(t: float) -> float:
        return 1.0 - Curves.elastic_out(1.0 - t)

    @staticmethod
    def spring(t: float) -> float:
        # High-performance fluid spring approximation
        return 1.0 - math.exp(-6.0 * t) * math.cos(7.0 * t)

    @staticmethod
    def cubic_bezier(x1: float, y1: float, x2: float, y2: float) -> Callable[[float], float]:
        return _bezier_solve(x1, y1, x2, y2)

    # Pre-calculated standard Material/Fluent/Apple design curves
    fast_out_slow_in = _bezier_solve(0.4, 0.0, 0.2, 1.0)
    smooth_spring = _bezier_solve(0.16, 1.0, 0.3, 1.0)
    overshoot = _bezier_solve(0.34, 1.56, 0.64, 1.0)


CURVE_LOOKUP = {
    "linear": Curves.linear,
    "ease_in": Curves.ease_in,
    "ease_out": Curves.ease_out,
    "ease_in_out": Curves.ease_in_out,
    "bounce_in": Curves.bounce_in,
    "bounce_out": Curves.bounce_out,
    "bounce_in_out": Curves.bounce_in_out,
    "elastic_in": Curves.elastic_in,
    "elastic_out": Curves.elastic_out,
    "spring": Curves.spring,
    "fast_out_slow_in": Curves.fast_out_slow_in,
    "smooth_spring": Curves.smooth_spring,
    "overshoot": Curves.overshoot
}


def resolve_curve(curve_name_or_fn: Any) -> Callable[[float], float]:
    if callable(curve_name_or_fn):
        return curve_name_or_fn
    if isinstance(curve_name_or_fn, str):
        key = curve_name_or_fn.lower().replace("-", "_")
        return CURVE_LOOKUP.get(key, Curves.smooth_spring)
    return Curves.smooth_spring


# ============================================================================
# 2. SPRING HARMONIC PHYSICS SIMULATOR
# ============================================================================

class SpringSimulation:
    def __init__(self, mass: float = 1.0, stiffness: float = 180.0, damping: float = 18.0, initial_velocity: float = 0.0):
        self.mass = max(0.001, mass)
        self.stiffness = max(0.001, stiffness)
        self.damping = max(0.0, damping)
        self.velocity = initial_velocity
        self.target = 1.0
        self.position = 0.0

        # Characteristic equation roots: m*r^2 + c*r + k = 0
        self.omega0 = math.sqrt(self.stiffness / self.mass)
        self.zeta = self.damping / (2.0 * math.sqrt(self.stiffness * self.mass))

    def evaluate(self, t: float) -> Tuple[float, float]:
        """Returns (position, velocity) at elapsed seconds t."""
        if t <= 0.0:
            return 0.0, self.velocity

        if self.zeta < 1.0:
            # Under-damped (oscillates and settles)
            omega_d = self.omega0 * math.sqrt(1.0 - self.zeta * self.zeta)
            c1 = -self.target
            c2 = (self.velocity + self.zeta * self.omega0 * c1) / omega_d
            decay = math.exp(-self.zeta * self.omega0 * t)
            pos = self.target + decay * (c1 * math.cos(omega_d * t) + c2 * math.sin(omega_d * t))
            vel = decay * (
                (-self.zeta * self.omega0 * (c1 * math.cos(omega_d * t) + c2 * math.sin(omega_d * t))) +
                (-c1 * omega_d * math.sin(omega_d * t) + c2 * omega_d * math.cos(omega_d * t))
            )
            return pos, vel
        elif abs(self.zeta - 1.0) < 1e-5:
            # Critically damped (fastest settle without oscillation)
            c1 = -self.target
            c2 = self.velocity + self.omega0 * c1
            decay = math.exp(-self.omega0 * t)
            pos = self.target + decay * (c1 + c2 * t)
            vel = decay * (c2 - self.omega0 * (c1 + c2 * t))
            return pos, vel
        else:
            # Over-damped
            r1 = -self.omega0 * (self.zeta - math.sqrt(self.zeta * self.zeta - 1.0))
            r2 = -self.omega0 * (self.zeta + math.sqrt(self.zeta * self.zeta - 1.0))
            c2 = (self.velocity - r1 * (-self.target)) / (r2 - r1)
            c1 = -self.target - c2
            pos = self.target + c1 * math.exp(r1 * t) + c2 * math.exp(r2 * t)
            vel = c1 * r1 * math.exp(r1 * t) + c2 * r2 * math.exp(r2 * t)
            return pos, vel

    def is_done(self, t: float, eps: float = 1e-3) -> bool:
        pos, vel = self.evaluate(t)
        return abs(pos - self.target) < eps and abs(vel) < eps


# ============================================================================
# 3. ANIMATION CONTROLLER & TWEENS
# ============================================================================

class AnimationStatus:
    DISMISSED = "dismissed"
    FORWARD = "forward"
    REVERSE = "reverse"
    COMPLETED = "completed"


class AnimationController:
    def __init__(self, duration_ms: float = 300.0, lower_bound: float = 0.0, upper_bound: float = 1.0, curve: Any = None, loop: bool = False, autoreverse: bool = False):
        self.duration_ms = max(1.0, duration_ms)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.curve = resolve_curve(curve) if curve else Curves.smooth_spring
        self.loop = loop
        self.autoreverse = autoreverse

        self._value = lower_bound
        self.status = AnimationStatus.DISMISSED
        self._elapsed_ms = 0.0
        self._listeners: List[Callable[[float], None]] = []
        self._status_listeners: List[Callable[[str], None]] = []

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, v: float):
        self._value = max(self.lower_bound, min(self.upper_bound, v))
        self._notify_listeners()

    @property
    def is_animating(self) -> bool:
        return self.status in (AnimationStatus.FORWARD, AnimationStatus.REVERSE)

    def forward(self, from_val: Optional[float] = None):
        if from_val is not None:
            self._value = from_val
            span = self.upper_bound - self.lower_bound
            self._elapsed_ms = ((from_val - self.lower_bound) / (span if span > 0 else 1.0)) * self.duration_ms
        self.status = AnimationStatus.FORWARD
        self._notify_status()

    def reverse(self, from_val: Optional[float] = None):
        if from_val is not None:
            self._value = from_val
            span = self.upper_bound - self.lower_bound
            self._elapsed_ms = (1.0 - (from_val - self.lower_bound) / (span if span > 0 else 1.0)) * self.duration_ms
        self.status = AnimationStatus.REVERSE
        self._notify_status()

    def repeat(self, reverse: bool = False):
        self.loop = True
        self.autoreverse = reverse
        self.forward(from_val=self.lower_bound)

    def stop(self):
        self.status = AnimationStatus.DISMISSED if self._value == self.lower_bound else AnimationStatus.COMPLETED
        self._notify_status()

    def reset(self):
        self._value = self.lower_bound
        self._elapsed_ms = 0.0
        self.status = AnimationStatus.DISMISSED
        self._notify_listeners()
        self._notify_status()

    def tick(self, dt_ms: float) -> bool:
        """Advance time by dt_ms. Returns True if frame was dirty and updated."""
        if not self.is_animating:
            return False

        if self.status == AnimationStatus.FORWARD:
            self._elapsed_ms += dt_ms
            t = min(1.0, self._elapsed_ms / self.duration_ms)
            curved_t = self.curve(t)
            self._value = self.lower_bound + (self.upper_bound - self.lower_bound) * curved_t
            self._notify_listeners()

            if t >= 1.0:
                if self.loop:
                    if self.autoreverse:
                        self.reverse(from_val=self.upper_bound)
                    else:
                        self.forward(from_val=self.lower_bound)
                else:
                    self.status = AnimationStatus.COMPLETED
                    self._notify_status()
            return True

        elif self.status == AnimationStatus.REVERSE:
            self._elapsed_ms += dt_ms
            t = min(1.0, self._elapsed_ms / self.duration_ms)
            curved_t = self.curve(t)
            self._value = self.upper_bound - (self.upper_bound - self.lower_bound) * curved_t
            self._notify_listeners()

            if t >= 1.0:
                if self.loop:
                    if self.autoreverse:
                        self.forward(from_val=self.lower_bound)
                    else:
                        self.reverse(from_val=self.upper_bound)
                else:
                    self.status = AnimationStatus.DISMISSED
                    self._notify_status()
            return True

        return False

    def add_listener(self, cb: Callable[[float], None]):
        self._listeners.append(cb)

    def remove_listener(self, cb: Callable[[float], None]):
        if cb in self._listeners:
            self._listeners.remove(cb)

    def add_status_listener(self, cb: Callable[[str], None]):
        self._status_listeners.append(cb)

    def _notify_listeners(self):
        for cb in self._listeners:
            try:
                cb(self._value)
            except Exception:
                pass

    def _notify_status(self):
        for cb in self._status_listeners:
            try:
                cb(self.status)
            except Exception:
                pass


class Tween:
    def __init__(self, begin: float = 0.0, end: float = 1.0):
        self.begin = float(begin)
        self.end = float(end)

    def lerp(self, t: float) -> float:
        return self.begin + (self.end - self.begin) * t

    def transform(self, t: float) -> float:
        return self.lerp(t)

    def evaluate(self, controller: AnimationController) -> float:
        return self.lerp(controller.value)


class ColorTween:
    def __init__(self, begin_hex: str = "#000000", end_hex: str = "#ffffff"):
        self.begin_hex = begin_hex
        self.end_hex = end_hex

    @staticmethod
    def _parse(hex_str: str) -> Tuple[int, int, int]:
        h = hex_str.lstrip('#')
        if len(h) == 3:
            h = ''.join([c * 2 for c in h])
        if len(h) < 6:
            return 0, 0, 0
        try:
            return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        except Exception:
            return 0, 0, 0

    def lerp(self, t: float) -> str:
        t = max(0.0, min(1.0, t))
        r1, g1, b1 = self._parse(self.begin_hex)
        r2, g2, b2 = self._parse(self.end_hex)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{max(0, min(255, r)):02x}{max(0, min(255, g)):02x}{max(0, min(255, b)):02x}"


class OffsetTween:
    def __init__(self, begin: Tuple[float, float] = (0.0, 0.0), end: Tuple[float, float] = (0.0, 0.0)):
        self.begin = begin
        self.end = end

    def lerp(self, t: float) -> Tuple[float, float]:
        t = max(0.0, min(1.0, t))
        x = self.begin[0] + (self.end[0] - self.begin[0]) * t
        y = self.begin[1] + (self.end[1] - self.begin[1]) * t
        return x, y


# ============================================================================
# 4. STAR UI DECLARATIVE ANIMATION VIRTUAL NODES
# ============================================================================

def make_animated_opacity(opacity: float = 1.0, duration_ms: int = 300, curve: str = "smooth_spring", child: Any = None) -> StarVirtualNode:
    props = {
        "opacity": float(opacity),
        "duration_ms": int(duration_ms),
        "curve": str(curve)
    }
    children = [child] if child and not isinstance(child, StarNull) else []
    return StarVirtualNode("animated_opacity", props=props, children=children)


def make_animated_scale(scale: float = 1.0, duration_ms: int = 300, curve: str = "overshoot", child: Any = None) -> StarVirtualNode:
    props = {
        "scale": float(scale),
        "duration_ms": int(duration_ms),
        "curve": str(curve)
    }
    children = [child] if child and not isinstance(child, StarNull) else []
    return StarVirtualNode("animated_scale", props=props, children=children)


def make_animated_slide(offset_x: float = 0.0, offset_y: float = 0.0, duration_ms: int = 300, curve: str = "smooth_spring", child: Any = None) -> StarVirtualNode:
    props = {
        "offset_x": float(offset_x),
        "offset_y": float(offset_y),
        "duration_ms": int(duration_ms),
        "curve": str(curve)
    }
    children = [child] if child and not isinstance(child, StarNull) else []
    return StarVirtualNode("animated_slide", props=props, children=children)


def make_animated_rotation(angle_deg: float = 0.0, duration_ms: int = 300, curve: str = "smooth_spring", child: Any = None) -> StarVirtualNode:
    props = {
        "angle_deg": float(angle_deg),
        "duration_ms": int(duration_ms),
        "curve": str(curve)
    }
    children = [child] if child and not isinstance(child, StarNull) else []
    return StarVirtualNode("animated_rotation", props=props, children=children)


def make_animated_container(width: Optional[int] = None, height: Optional[int] = None, bg: Optional[str] = None, radius: int = 12, duration_ms: int = 300, curve: str = "smooth_spring", child: Any = None) -> StarVirtualNode:
    props = {
        "width": width,
        "height": height,
        "bg": bg,
        "radius": radius,
        "duration_ms": int(duration_ms),
        "curve": str(curve)
    }
    children = [child] if child and not isinstance(child, StarNull) else []
    return StarVirtualNode("animated_container", props=props, children=children)


def make_shimmer(width: Optional[int] = None, height: Optional[int] = None, radius: int = 8, child: Any = None) -> StarVirtualNode:
    props = {
        "width": width,
        "height": height,
        "radius": radius
    }
    children = [child] if child and not isinstance(child, StarNull) else []
    return StarVirtualNode("shimmer", props=props, children=children)


def make_skeleton(width: int = 200, height: int = 24, radius: int = 6) -> StarVirtualNode:
    props = {
        "width": int(width),
        "height": int(height),
        "radius": int(radius)
    }
    return StarVirtualNode("skeleton", props=props)


def make_pulse(min_scale: float = 0.95, max_scale: float = 1.05, duration_ms: int = 1200, child: Any = None) -> StarVirtualNode:
    props = {
        "min_scale": float(min_scale),
        "max_scale": float(max_scale),
        "duration_ms": int(duration_ms)
    }
    children = [child] if child and not isinstance(child, StarNull) else []
    return StarVirtualNode("pulse", props=props, children=children)


def make_bounce(intensity: float = 10.0, duration_ms: int = 800, child: Any = None) -> StarVirtualNode:
    props = {
        "intensity": float(intensity),
        "duration_ms": int(duration_ms)
    }
    children = [child] if child and not isinstance(child, StarNull) else []
    return StarVirtualNode("bounce", props=props, children=children)


def make_shake(intensity: float = 8.0, duration_ms: int = 500, child: Any = None) -> StarVirtualNode:
    props = {
        "intensity": float(intensity),
        "duration_ms": int(duration_ms)
    }
    children = [child] if child and not isinstance(child, StarNull) else []
    return StarVirtualNode("shake", props=props, children=children)


def make_glow(color: str = "#00f0ff", blur: int = 16, duration_ms: int = 1500, child: Any = None) -> StarVirtualNode:
    props = {
        "color": str(color),
        "blur": int(blur),
        "duration_ms": int(duration_ms)
    }
    children = [child] if child and not isinstance(child, StarNull) else []
    return StarVirtualNode("glow", props=props, children=children)


def make_marquee(text: str = "", speed: int = 50) -> StarVirtualNode:
    props = {
        "text": str(text),
        "speed": int(speed)
    }
    return StarVirtualNode("marquee", props=props)


def make_confetti(count: int = 50, active: bool = True) -> StarVirtualNode:
    props = {
        "count": int(count),
        "active": bool(active)
    }
    return StarVirtualNode("confetti", props=props)


def make_ripple(color: str = "rgba(255, 255, 255, 0.35)", duration_ms: int = 600) -> StarVirtualNode:
    props = {
        "color": str(color),
        "duration_ms": int(duration_ms)
    }
    return StarVirtualNode("ripple", props=props)


# ============================================================================
# 5. MODULE EXPORTS FOR STAR LANGUAGE
# ============================================================================

def create_animation_module() -> StarModule:
    exports: Dict[str, StarValue] = {}

    def _star_animated_opacity(*args: StarValue) -> StarValue:
        op = float(args[0].value) if args and hasattr(args[0], "value") else 1.0
        dur = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 300
        curve = args[2].to_string() if len(args) > 2 and not isinstance(args[2], StarNull) else "smooth_spring"
        child = args[3] if len(args) > 3 else None
        return make_animated_opacity(op, dur, curve, child)

    def _star_animated_scale(*args: StarValue) -> StarValue:
        sc = float(args[0].value) if args and hasattr(args[0], "value") else 1.0
        dur = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 300
        curve = args[2].to_string() if len(args) > 2 and not isinstance(args[2], StarNull) else "overshoot"
        child = args[3] if len(args) > 3 else None
        return make_animated_scale(sc, dur, curve, child)

    def _star_animated_slide(*args: StarValue) -> StarValue:
        ox = float(args[0].value) if args and hasattr(args[0], "value") else 0.0
        oy = float(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 0.0
        dur = int(args[2].value) if len(args) > 2 and hasattr(args[2], "value") else 300
        curve = args[3].to_string() if len(args) > 3 and not isinstance(args[3], StarNull) else "smooth_spring"
        child = args[4] if len(args) > 4 else None
        return make_animated_slide(ox, oy, dur, curve, child)

    def _star_animated_rotation(*args: StarValue) -> StarValue:
        ang = float(args[0].value) if args and hasattr(args[0], "value") else 0.0
        dur = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 300
        curve = args[2].to_string() if len(args) > 2 and not isinstance(args[2], StarNull) else "smooth_spring"
        child = args[3] if len(args) > 3 else None
        return make_animated_rotation(ang, dur, curve, child)

    def _star_animated_container(*args: StarValue) -> StarValue:
        w = int(args[0].value) if args and hasattr(args[0], "value") else None
        h = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else None
        bg = args[2].to_string() if len(args) > 2 and not isinstance(args[2], StarNull) else None
        radius = int(args[3].value) if len(args) > 3 and hasattr(args[3], "value") else 12
        dur = int(args[4].value) if len(args) > 4 and hasattr(args[4], "value") else 300
        curve = args[5].to_string() if len(args) > 5 and not isinstance(args[5], StarNull) else "smooth_spring"
        child = args[6] if len(args) > 6 else None
        return make_animated_container(w, h, bg, radius, dur, curve, child)

    def _star_shimmer(*args: StarValue) -> StarValue:
        w = int(args[0].value) if args and hasattr(args[0], "value") else None
        h = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else None
        rad = int(args[2].value) if len(args) > 2 and hasattr(args[2], "value") else 8
        child = args[3] if len(args) > 3 else None
        return make_shimmer(w, h, rad, child)

    def _star_skeleton(*args: StarValue) -> StarValue:
        w = int(args[0].value) if args and hasattr(args[0], "value") else 200
        h = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 24
        rad = int(args[2].value) if len(args) > 2 and hasattr(args[2], "value") else 6
        return make_skeleton(w, h, rad)

    def _star_pulse(*args: StarValue) -> StarValue:
        min_s = float(args[0].value) if args and hasattr(args[0], "value") else 0.95
        max_s = float(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 1.05
        dur = int(args[2].value) if len(args) > 2 and hasattr(args[2], "value") else 1200
        child = args[3] if len(args) > 3 else None
        return make_pulse(min_s, max_s, dur, child)

    def _star_bounce(*args: StarValue) -> StarValue:
        inten = float(args[0].value) if args and hasattr(args[0], "value") else 10.0
        dur = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 800
        child = args[2] if len(args) > 2 else None
        return make_bounce(inten, dur, child)

    def _star_shake(*args: StarValue) -> StarValue:
        inten = float(args[0].value) if args and hasattr(args[0], "value") else 8.0
        dur = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 500
        child = args[2] if len(args) > 2 else None
        return make_shake(inten, dur, child)

    def _star_glow(*args: StarValue) -> StarValue:
        color = args[0].to_string() if args and not isinstance(args[0], StarNull) else "#00f0ff"
        blur = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 16
        dur = int(args[2].value) if len(args) > 2 and hasattr(args[2], "value") else 1500
        child = args[3] if len(args) > 3 else None
        return make_glow(color, blur, dur, child)

    def _star_marquee(*args: StarValue) -> StarValue:
        txt = args[0].to_string() if args else ""
        spd = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 50
        return make_marquee(txt, spd)

    def _star_confetti(*args: StarValue) -> StarValue:
        cnt = int(args[0].value) if args and hasattr(args[0], "value") else 50
        act = args[1].is_truthy() if len(args) > 1 else True
        return make_confetti(cnt, act)

    def _star_ripple(*args: StarValue) -> StarValue:
        col = args[0].to_string() if args and not isinstance(args[0], StarNull) else "rgba(255, 255, 255, 0.35)"
        dur = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 600
        return make_ripple(col, dur)

    exports["animated_opacity"] = StarBuiltinFunction("animated_opacity", _star_animated_opacity)
    exports["animated_scale"] = StarBuiltinFunction("animated_scale", _star_animated_scale)
    exports["animated_slide"] = StarBuiltinFunction("animated_slide", _star_animated_slide)
    exports["animated_rotation"] = StarBuiltinFunction("animated_rotation", _star_animated_rotation)
    exports["animated_container"] = StarBuiltinFunction("animated_container", _star_animated_container)
    exports["shimmer"] = StarBuiltinFunction("shimmer", _star_shimmer)
    exports["skeleton"] = StarBuiltinFunction("skeleton", _star_skeleton)
    exports["pulse"] = StarBuiltinFunction("pulse", _star_pulse)
    exports["bounce"] = StarBuiltinFunction("bounce", _star_bounce)
    exports["shake"] = StarBuiltinFunction("shake", _star_shake)
    exports["glow"] = StarBuiltinFunction("glow", _star_glow)
    exports["marquee"] = StarBuiltinFunction("marquee", _star_marquee)
    exports["confetti"] = StarBuiltinFunction("confetti", _star_confetti)
    exports["ripple"] = StarBuiltinFunction("ripple", _star_ripple)

    return StarModule("Animation", exports)

