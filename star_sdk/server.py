"""
Star Standard Library — Server Subsystem (use Server)
Authoritative Reference: STAR_SERVER_SPEC.md

Exports the Server & HTTP module into Star Language programs.
"""

import os
import time
import json
import uuid
import hmac
import hashlib
import base64
from typing import Dict, Any, List, Optional, Callable

from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarBuiltinFunction, StarModule, to_star_value
)
from star_engine.hyperflow.server import ServerApp, StarServerApp
from star_engine.hyperflow.chrono import ChronoStore, StarChronoStore
from star_engine.hyperflow.reactive_mesh import ReactiveStore, StarReactiveStore
from star_engine.hyperflow.actor import ActorMesh, StarActorRef


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def _base64url_decode(s: str) -> bytes:
    rem = len(s) % 4
    if rem > 0:
        s += '=' * (4 - rem)
    return base64.urlsafe_b64decode(s.encode('ascii'))


def create_server_module() -> StarModule:
    exports: Dict[str, StarValue] = {}

    # 1. Server.app()
    def _server_app(*args: StarValue) -> StarValue:
        name = args[0].to_string() if args else "StarApp"
        app = ServerApp(name=name)
        return StarServerApp(app)
    exports["app"] = StarBuiltinFunction("app", _server_app)

    # 2. Server.chrono_store()
    def _chrono_store(*args: StarValue) -> StarValue:
        name = args[0].to_string() if args else "default"
        init_val = {}
        if len(args) > 1 and isinstance(args[1], StarMap):
            from star_engine.hyperflow.server import StarMap, StarInteger, StarDecimal, StarBoolean, StarText, StarList
            def _to_native(v):
                if isinstance(v, (StarInteger, StarDecimal, StarBoolean, StarText)):
                    return v.value
                if isinstance(v, StarList):
                    return [_to_native(x) for x in v.elements]
                if isinstance(v, StarMap):
                    return {k: _to_native(val) for k, val in v.entries.items()}
                return v
            init_val = _to_native(args[1])
        store = ChronoStore(name=name, initial_data=init_val)
        return StarChronoStore(store)
    exports["chrono_store"] = StarBuiltinFunction("chrono_store", _chrono_store)

    # 3. Server.reactive_store()
    def _reactive_store(*args: StarValue) -> StarValue:
        name = args[0].to_string() if args else "default"
        init_val = {}
        if len(args) > 1 and isinstance(args[1], StarMap):
            from star_engine.hyperflow.server import StarMap, StarInteger, StarDecimal, StarBoolean, StarText, StarList
            def _to_native(v):
                if isinstance(v, (StarInteger, StarDecimal, StarBoolean, StarText)):
                    return v.value
                if isinstance(v, StarList):
                    return [_to_native(x) for x in v.elements]
                if isinstance(v, StarMap):
                    return {k: _to_native(val) for k, val in v.entries.items()}
                return v
            init_val = _to_native(args[1])
        store = ReactiveStore(name=name, initial_data=init_val)
        return StarReactiveStore(store)
    exports["reactive_store"] = StarBuiltinFunction("reactive_store", _reactive_store)

    # 4. Server.spawn_actor()
    _global_actor_mesh = ActorMesh()
    def _spawn_actor(*args: StarValue) -> StarValue:
        if len(args) < 2:
            return StarNull()
        name = args[0].to_string()
        handler = args[1]
        def _cb(payload):
            if hasattr(handler, "call"):
                return handler.call([to_star_value(payload)])
            elif callable(handler):
                return handler(payload)
            return None
        actor = _global_actor_mesh.spawn(name, _cb)
        return StarActorRef(actor)
    exports["spawn_actor"] = StarBuiltinFunction("spawn_actor", _spawn_actor)

    # 5. Cryptography & Security Helpers:
    # JWT Sign
    def _jwt_sign(*args: StarValue) -> StarValue:
        if len(args) < 2:
            return StarNull()
        from star_engine.hyperflow.server import StarMap, StarInteger, StarDecimal, StarBoolean, StarText, StarList
        def _to_native(v):
            if isinstance(v, (StarInteger, StarDecimal, StarBoolean, StarText)):
                return v.value
            if isinstance(v, StarList):
                return [_to_native(x) for x in v.elements]
            if isinstance(v, StarMap):
                return {k: _to_native(val) for k, val in v.entries.items()}
            return str(v)
        payload = _to_native(args[0])
        secret = args[1].to_string().encode("utf-8")
        header = {"alg": "HS256", "typ": "JWT"}
        h_b64 = _base64url_encode(json.dumps(header).encode("utf-8"))
        p_b64 = _base64url_encode(json.dumps(payload).encode("utf-8"))
        msg = f"{h_b64}.{p_b64}".encode("utf-8")
        sig = hmac.new(secret, msg, hashlib.sha256).digest()
        s_b64 = _base64url_encode(sig)
        return StarText(f"{h_b64}.{p_b64}.{s_b64}")
    exports["jwt_sign"] = StarBuiltinFunction("jwt_sign", _jwt_sign)

    # JWT Verify
    def _jwt_verify(*args: StarValue) -> StarValue:
        if len(args) < 2:
            return StarNull()
        token = args[0].to_string()
        secret = args[1].to_string().encode("utf-8")
        parts = token.split(".")
        if len(parts) != 3:
            return StarNull()
        h_b64, p_b64, s_b64 = parts
        msg = f"{h_b64}.{p_b64}".encode("utf-8")
        expected_sig = _base64url_encode(hmac.new(secret, msg, hashlib.sha256).digest())
        if not hmac.compare_digest(s_b64, expected_sig):
            return StarNull()
        try:
            payload_json = json.loads(_base64url_decode(p_b64).decode("utf-8"))
            return to_star_value(payload_json)
        except Exception:
            return StarNull()
    exports["jwt_verify"] = StarBuiltinFunction("jwt_verify", _jwt_verify)

    # Password Hash & Verify (Salted PBKDF2-HMAC-SHA256)
    def _hash_password(*args: StarValue) -> StarValue:
        if not args:
            return StarNull()
        pwd = args[0].to_string().encode("utf-8")
        salt = os.urandom(16)
        h = hashlib.pbkdf2_hmac("sha256", pwd, salt, 100000)
        encoded = base64.b64encode(salt + h).decode("ascii")
        return StarText(encoded)
    exports["hash_password"] = StarBuiltinFunction("hash_password", _hash_password)

    def _verify_password(*args: StarValue) -> StarValue:
        if len(args) < 2:
            return StarBoolean(False)
        pwd = args[0].to_string().encode("utf-8")
        raw = base64.b64decode(args[1].to_string().encode("ascii"))
        salt = raw[:16]
        expected_h = raw[16:]
        actual_h = hashlib.pbkdf2_hmac("sha256", pwd, salt, 100000)
        return StarBoolean(hmac.compare_digest(expected_h, actual_h))
    exports["verify_password"] = StarBuiltinFunction("verify_password", _verify_password)

    # Monotonic Time & UUID
    exports["now_ms"] = StarBuiltinFunction("now_ms", lambda *args: StarDecimal(time.time() * 1000.0))
    exports["uuid"] = StarBuiltinFunction("uuid", lambda *args: StarText(str(uuid.uuid4())))

    # Rate Limiting Token Bucket Middleware
    def _rate_limit(*args: StarValue) -> StarValue:
        max_req = int(args[0].value) if args and hasattr(args[0], "value") else 60
        window = float(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 60.0
        buckets: Dict[str, List[float]] = {}
        
        def _mw(req, res):
            ip = req.req.client_ip if hasattr(req, "req") else "unknown"
            now = time.time()
            if ip not in buckets:
                buckets[ip] = []
            # Purge expired timestamps
            buckets[ip] = [ts for ts in buckets[ip] if now - ts < window]
            if len(buckets[ip]) >= max_req:
                res.status(429).json({"error": "Too Many Requests", "retry_after": int(window)})
                return StarBoolean(False)
            buckets[ip].append(now)
            return StarBoolean(True)
        return StarBuiltinFunction("rate_limit_middleware", _mw)
    exports["rate_limit"] = StarBuiltinFunction("rate_limit", _rate_limit)

    return StarModule("Server", exports)
