"""
Star Standard Library — OmniEngine 2.0 GN Subsystem (use Omni)
Authoritative Reference: STAR_OMNI_SPEC.md

Exports the Omni, Fiber, Grid, JIT, and Memory modules into Star Language programs.
"""

from typing import Dict, Any, List, Optional, Callable
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarBuiltinFunction, StarModule, to_star_value, from_star_value
)
from star_engine.omni.jit import TieredJITEngine
from star_engine.omni.fiber import FiberScheduler, OmniFiber, OmniChannel, FiberState
from star_engine.omni.memory import ArenaAllocator, BorrowedBuffer
from star_engine.omni.grid import OmniCluster, OmniNode
from star_engine.omni.ffi import PolyglotFFIEngine

_global_scheduler = FiberScheduler(num_workers=4)
_global_jit = TieredJITEngine(hotspot_threshold=20)
_global_ffi = PolyglotFFIEngine()
_global_cluster = OmniCluster(cluster_name="star-global-grid")


class StarFiber(StarValue):
    def __init__(self, fiber: OmniFiber):
        self.fiber = fiber

    @property
    def type_name(self) -> str:
        return "Fiber"

    def to_string(self) -> str:
        return f"<Fiber id={self.fiber.id} state={self.fiber.state.name} duration={self.fiber.duration_ms}ms>"

    def is_truthy(self) -> bool:
        return True

    def get(self, prop: str) -> StarValue:
        if prop == "id":
            return StarInteger(self.fiber.id)
        if prop == "state":
            return StarText(self.fiber.state.name)
        if prop == "duration_ms":
            return StarDecimal(self.fiber.duration_ms)
        if prop == "join":
            def _join(*args):
                timeout = None
                if args and isinstance(args[0], (StarInteger, StarDecimal)):
                    timeout = args[0].value
                res = self.fiber.join(timeout=timeout)
                return to_star_value(res)
            return StarBuiltinFunction(f"join_{self.fiber.id}", _join)
        return StarNull()


class StarChannel(StarValue):
    def __init__(self, channel: OmniChannel):
        self.channel = channel

    @property
    def type_name(self) -> str:
        return "Channel"

    def to_string(self) -> str:
        return f"<Channel size={self.channel.size} capacity={self.channel.capacity}>"

    def is_truthy(self) -> bool:
        return not self.channel.is_closed

    def get(self, prop: str) -> StarValue:
        if prop == "size":
            return StarInteger(self.channel.size)
        if prop == "is_closed":
            return StarBoolean(self.channel.is_closed)
        if prop == "send":
            def _send(*args):
                if not args:
                    return StarBoolean(False)
                val = from_star_value(args[0])
                timeout = args[1].value if len(args) > 1 and isinstance(args[1], (StarInteger, StarDecimal)) else None
                ok = self.channel.send(val, timeout=timeout)
                return StarBoolean(ok)
            return StarBuiltinFunction("send", _send)
        if prop == "recv":
            def _recv(*args):
                timeout = args[0].value if args and isinstance(args[0], (StarInteger, StarDecimal)) else None
                val = self.channel.recv(timeout=timeout)
                return to_star_value(val)
            return StarBuiltinFunction("recv", _recv)
        if prop == "close":
            def _close(*args):
                self.channel.close()
                return StarNull()
            return StarBuiltinFunction("close", _close)
        return StarNull()


class StarBorrowedBuffer(StarValue):
    def __init__(self, buffer: BorrowedBuffer):
        self.buffer = buffer

    @property
    def type_name(self) -> str:
        return "BorrowedBuffer"

    def to_string(self) -> str:
        return self.buffer.to_text()

    def is_truthy(self) -> bool:
        return self.buffer.length > 0

    def get(self, prop: str) -> StarValue:
        if prop in ("length", "size"):
            return StarInteger(self.buffer.length)
        if prop == "to_text":
            return StarBuiltinFunction("to_text", lambda *a: StarText(self.buffer.to_text()))
        if prop == "slice":
            def _slice(*args):
                start = int(args[0].value) if args else 0
                end = int(args[1].value) if len(args) > 1 else None
                sub = self.buffer.slice(start, end)
                return StarBorrowedBuffer(sub)
            return StarBuiltinFunction("slice", _slice)
        return StarNull()


class StarArena(StarValue):
    def __init__(self, arena: ArenaAllocator):
        self.arena = arena

    @property
    def type_name(self) -> str:
        return "Arena"

    def to_string(self) -> str:
        return f"<Arena capacity={self.arena.capacity // 1024}KB used={self.arena.cursor}B>"

    def is_truthy(self) -> bool:
        return True

    def get(self, prop: str) -> StarValue:
        if prop == "alloc_text":
            def _alloc_text(*args):
                txt = args[0].to_string() if args else ""
                buf = self.arena.alloc_text(txt)
                return StarBorrowedBuffer(buf)
            return StarBuiltinFunction("alloc_text", _alloc_text)
        if prop == "alloc":
            def _alloc(*args):
                size = int(args[0].value) if args else 64
                buf = self.arena.alloc(size)
                return StarBorrowedBuffer(buf)
            return StarBuiltinFunction("alloc", _alloc)
        if prop == "reset":
            def _reset(*args):
                self.arena.reset()
                return StarNull()
            return StarBuiltinFunction("reset", _reset)
        if prop == "stats":
            def _stats(*args):
                s = self.arena.stats()
                return to_star_value(s)
            return StarBuiltinFunction("stats", _stats)
        return StarNull()


class StarClusterRef(StarValue):
    def __init__(self, cluster: OmniCluster):
        self.cluster = cluster

    @property
    def type_name(self) -> str:
        return "OmniCluster"

    def to_string(self) -> str:
        return f"<OmniCluster '{self.cluster.cluster_name}' nodes={len(self.cluster.nodes)}>"

    def is_truthy(self) -> bool:
        return True

    def get(self, prop: str) -> StarValue:
        if prop == "status":
            return StarBuiltinFunction("status", lambda *a: to_star_value(self.cluster.cluster_status()))
        if prop == "register_node":
            def _reg(*args):
                node_id = args[0].to_string() if args else "peer"
                addr = args[1].to_string() if len(args) > 1 else "127.0.0.1"
                port = int(args[2].value) if len(args) > 2 else 7001
                node = OmniNode(node_id=node_id, address=addr, port=port)
                self.cluster.register_node(node)
                return StarBoolean(True)
            return StarBuiltinFunction("register_node", _reg)
        if prop == "dispatch":
            def _dispatch(*args):
                task_name = args[0].to_string() if args else "task"
                payload = from_star_value(args[1]) if len(args) > 1 else None
                handler = args[2] if len(args) > 2 else None
                def _invoke(p):
                    if hasattr(handler, "call"):
                        return from_star_value(handler.call([to_star_value(p)]))
                    elif callable(handler):
                        return handler(p)
                    return p
                res = self.cluster.dispatch(task_name, payload, _invoke)
                return to_star_value(res)
            return StarBuiltinFunction("dispatch", _dispatch)
        if prop == "scatter_gather":
            def _sg(*args):
                items = from_star_value(args[0]) if args else []
                handler = args[1] if len(args) > 1 else None
                def _invoke(p):
                    if hasattr(handler, "call"):
                        return from_star_value(handler.call([to_star_value(p)]))
                    elif callable(handler):
                        return handler(p)
                    return p
                res = self.cluster.scatter_gather(items, _invoke)
                return to_star_value(res)
            return StarBuiltinFunction("scatter_gather", _sg)
        return StarNull()


def create_omni_module() -> StarModule:
    exports: Dict[str, StarValue] = {
        "version": StarText("2.0-GN"),
    }

    # 1. Omni.spawn(fn, *args)
    def _spawn(*args: StarValue) -> StarValue:
        if not args:
            return StarNull()
        fn = args[0]
        call_args = [from_star_value(a) for a in args[1:]]
        def _target():
            if hasattr(fn, "call"):
                return fn.call([to_star_value(a) for a in call_args])
            elif callable(fn):
                return fn(*call_args)
            return None
        fiber = _global_scheduler.spawn(_target)
        return StarFiber(fiber)
    exports["spawn"] = StarBuiltinFunction("spawn", _spawn)

    # 2. Omni.channel(capacity=0)
    def _channel(*args: StarValue) -> StarValue:
        cap = int(args[0].value) if args and isinstance(args[0], (StarInteger, StarDecimal)) else 0
        return StarChannel(OmniChannel(capacity=cap))
    exports["channel"] = StarBuiltinFunction("channel", _channel)

    # 3. Omni.parallel_map(fn, list)
    def _parallel_map(*args: StarValue) -> StarValue:
        if len(args) < 2:
            return StarList([])
        fn = args[0]
        raw_items = from_star_value(args[1])
        if not isinstance(raw_items, list):
            return StarList([])
        def _mapper(item):
            if hasattr(fn, "call"):
                return from_star_value(fn.call([to_star_value(item)]))
            elif callable(fn):
                return fn(item)
            return item
        res = _global_scheduler.parallel_map(_mapper, raw_items)
        return to_star_value(res)
    exports["parallel_map"] = StarBuiltinFunction("parallel_map", _parallel_map)

    # 4. Omni.arena(capacity_kb=1024)
    def _arena(*args: StarValue) -> StarValue:
        cap_kb = int(args[0].value) if args and isinstance(args[0], (StarInteger, StarDecimal)) else 1024
        return StarArena(ArenaAllocator(capacity_bytes=cap_kb * 1024))
    exports["arena"] = StarBuiltinFunction("arena", _arena)

    # 5. Omni.cluster(name="star-grid")
    def _cluster(*args: StarValue) -> StarValue:
        name = args[0].to_string() if args else "star-global-grid"
        return StarClusterRef(OmniCluster(cluster_name=name))
    exports["cluster"] = StarBuiltinFunction("cluster", _cluster)

    # 6. Omni.info()
    def _info(*args: StarValue) -> StarValue:
        info_dict = {
            "engine": "Star OmniEngine 2.0 GN (Generation Next)",
            "version": "2.0-GN",
            "scheduler": _global_scheduler.stats(),
            "jit": {
                "threshold": _global_jit.hotspot_threshold,
                "compiled_count": len(_global_jit.compiled_cache),
                "optimizations": _global_jit.total_optimizations,
            },
            "ffi": _global_ffi.stats(),
            "cluster": _global_cluster.cluster_status(),
        }
        return to_star_value(info_dict)
    exports["info"] = StarBuiltinFunction("info", _info)

    # 7. Omni.bench_jit(name, fn, iterations)
    def _bench_jit(*args: StarValue) -> StarValue:
        name = args[0].to_string() if args else "workload"
        fn = args[1] if len(args) > 1 else None
        iters = int(args[2].value) if len(args) > 2 and isinstance(args[2], (StarInteger, StarDecimal)) else 50000
        def _workload():
            if hasattr(fn, "call"):
                return fn.call([])
            elif callable(fn):
                return fn()
            return None
        res = _global_jit.benchmark_speedup(name, _workload, iters)
        return to_star_value(res)
    exports["bench_jit"] = StarBuiltinFunction("bench_jit", _bench_jit)

    return StarModule("Omni", exports)


def create_fiber_module() -> StarModule:
    omni = create_omni_module()
    exports: Dict[str, StarValue] = {
        "spawn": omni.get("spawn"),
        "channel": omni.get("channel"),
        "parallel_map": omni.get("parallel_map"),
        "stats": StarBuiltinFunction("stats", lambda *a: to_star_value(_global_scheduler.stats())),
    }
    return StarModule("Fiber", exports)


def create_grid_module() -> StarModule:
    omni = create_omni_module()
    exports: Dict[str, StarValue] = {
        "cluster": omni.get("cluster"),
        "default": StarClusterRef(_global_cluster),
        "status": StarBuiltinFunction("status", lambda *a: to_star_value(_global_cluster.cluster_status())),
    }
    return StarModule("Grid", exports)
