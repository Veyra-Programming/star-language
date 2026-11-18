"""
Star HyperFlow Engine — Sovereign Actor Mesh & Ring-Buffer Mailboxes
Authoritative Reference: STAR_ACTOR_SPEC.md

Concept:
Lightweight server actors running concurrently with isolated state,
bounded message mailboxes, request-reply semantics (`ask`), and
self-healing supervision trees.
"""

import time
import queue
import threading
from typing import Dict, Any, List, Optional, Callable
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarBuiltinFunction, to_star_value
)


class ActorMessage:
    def __init__(self, payload: Any, reply_queue: Optional[queue.Queue] = None):
        self.payload = payload
        self.reply_queue = reply_queue
        self.timestamp = time.time()


class Actor:
    def __init__(self, name: str, handler: Callable[[Any], Any], max_mailbox_size: int = 10000, supervision: str = "restart"):
        self.name = name
        self.handler = handler
        self.supervision = supervision
        self.mailbox: queue.Queue = queue.Queue(maxsize=max_mailbox_size)
        self.is_running = True
        self.processed_count = 0
        self.error_count = 0
        self.thread = threading.Thread(target=self._run_loop, name=f"StarActor-{name}", daemon=True)
        self.thread.start()

    def _run_loop(self):
        while self.is_running:
            try:
                msg = self.mailbox.get(timeout=0.1)
                if msg is None:  # Stop poison pill
                    break
                try:
                    res = self.handler(msg.payload)
                    self.processed_count += 1
                    if msg.reply_queue:
                        msg.reply_queue.put({"success": True, "value": res})
                except Exception as e:
                    self.error_count += 1
                    if msg.reply_queue:
                        msg.reply_queue.put({"success": False, "error": str(e)})
                    if self.supervision == "restart":
                        # Continue processing subsequent messages
                        pass
                    elif self.supervision == "escalate":
                        self.is_running = False
                        break
                finally:
                    self.mailbox.task_done()
            except queue.Empty:
                continue

    def send(self, payload: Any):
        if not self.is_running:
            raise RuntimeError(f"Actor '{self.name}' is stopped.")
        self.mailbox.put_nowait(ActorMessage(payload=payload))

    def ask(self, payload: Any, timeout: float = 2.0) -> Any:
        if not self.is_running:
            raise RuntimeError(f"Actor '{self.name}' is stopped.")
        rq = queue.Queue(maxsize=1)
        self.mailbox.put(ActorMessage(payload=payload, reply_queue=rq), timeout=timeout)
        try:
            res = rq.get(timeout=timeout)
            if res.get("success"):
                return res.get("value")
            else:
                raise RuntimeError(f"Actor '{self.name}' error: {res.get('error')}")
        except queue.Empty:
            raise TimeoutError(f"Actor '{self.name}' timed out after {timeout}s.")

    def stop(self):
        self.is_running = False
        try:
            self.mailbox.put_nowait(None)
        except Exception:
            pass


class ActorMesh:
    def __init__(self):
        self.actors: Dict[str, Actor] = {}
        self._lock = threading.Lock()

    def spawn(self, name: str, handler: Callable[[Any], Any], supervision: str = "restart") -> Actor:
        with self._lock:
            if name in self.actors and self.actors[name].is_running:
                return self.actors[name]
            actor = Actor(name=name, handler=handler, supervision=supervision)
            self.actors[name] = actor
            return actor

    def get(self, name: str) -> Optional[Actor]:
        return self.actors.get(name)

    def stop_all(self):
        with self._lock:
            for a in self.actors.values():
                a.stop()
            self.actors.clear()


class StarActorRef(StarValue):
    def __init__(self, actor: Actor):
        self.actor = actor

    @property
    def type_name(self) -> str:
        return "Actor"

    def get(self, name: str) -> StarValue:
        if name == "send":
            def _send(*args):
                if not args:
                    return StarNull()
                self.actor.send(args[0])
                return StarBoolean(True)
            return StarBuiltinFunction("send", _send)

        if name == "ask":
            def _ask(*args):
                if not args:
                    return StarNull()
                timeout = 2.0
                if len(args) > 1 and hasattr(args[1], "value"):
                    timeout = float(args[1].value)
                try:
                    res = self.actor.ask(args[0], timeout=timeout)
                    return to_star_value(res)
                except Exception as e:
                    from star_engine.errors import StarRuntimeError
                    raise StarRuntimeError(str(e))
            return StarBuiltinFunction("ask", _ask)

        if name == "stop":
            def _stop(*args):
                self.actor.stop()
                return StarBoolean(True)
            return StarBuiltinFunction("stop", _stop)

        if name == "processed_count":
            return StarInteger(self.actor.processed_count)

        if name == "error_count":
            return StarInteger(self.actor.error_count)

        if name == "is_running":
            return StarBoolean(self.actor.is_running)

        from star_engine.errors import StarNameError
        raise StarNameError(f"Actor '{self.actor.name}' has no member '{name}'.")

    def to_string(self) -> str:
        return f"<Actor '{self.actor.name}' processed={self.actor.processed_count}>"

    def __repr__(self) -> str:
        return self.to_string()
