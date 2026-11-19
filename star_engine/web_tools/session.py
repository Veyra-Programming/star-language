"""
Star Web Tools — Session & Cookie State Management (PHP $_SESSION & $_COOKIE style)
Authoritative Reference: STAR_WEB_TOOLS_SPEC.md
"""

import time
import secrets
from typing import Dict, Any, Optional, List


class Session:
    """Represents an active client web session."""

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or secrets.token_hex(24)
        self.data: Dict[str, Any] = {}
        self.flash_data: Dict[str, Any] = {}
        self.created_at = time.time()
        self.last_accessed = time.time()

    def get(self, key: str, default: Any = None) -> Any:
        self.last_accessed = time.time()
        if key in self.flash_data:
            return self.flash_data.pop(key)
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        self.last_accessed = time.time()
        self.data[key] = value

    def has(self, key: str) -> bool:
        return key in self.data or key in self.flash_data

    def remove(self, key: str):
        self.data.pop(key, None)
        self.flash_data.pop(key, None)

    def flash(self, key: str, value: Any):
        """Stores flash data available for only the next request."""
        self.flash_data[key] = value

    def clear(self):
        self.data.clear()
        self.flash_data.clear()


class SessionManager:
    """Manages multi-tenant in-memory web sessions."""

    def __init__(self, session_ttl_seconds: int = 7200):
        self.sessions: Dict[str, Session] = {}
        self.ttl = session_ttl_seconds

    def start(self, session_id: Optional[str] = None) -> Session:
        if session_id and session_id in self.sessions:
            sess = self.sessions[session_id]
            if time.time() - sess.last_accessed < self.ttl:
                sess.last_accessed = time.time()
                return sess

        new_sess = Session()
        self.sessions[new_sess.session_id] = new_sess
        return new_sess

    def destroy(self, session_id: str):
        self.sessions.pop(session_id, None)

    def prune_expired(self):
        now = time.time()
        expired = [sid for sid, s in self.sessions.items() if now - s.last_accessed >= self.ttl]
        for sid in expired:
            del self.sessions[sid]


class Cookie:
    """HTTP Cookie builder and parser."""

    @classmethod
    def serialize(
        cls,
        name: str,
        value: str,
        max_age: int = 86400,
        path: str = "/",
        domain: Optional[str] = None,
        secure: bool = False,
        http_only: bool = True,
        same_site: str = "Lax"
    ) -> str:
        parts = [f"{name}={value}", f"Path={path}", f"Max-Age={max_age}"]
        if domain:
            parts.append(f"Domain={domain}")
        if secure:
            parts.append("Secure")
        if http_only:
            parts.append("HttpOnly")
        if same_site:
            parts.append(f"SameSite={same_site}")
        return "; ".join(parts)

    @classmethod
    def parse(cls, cookie_header: str) -> Dict[str, str]:
        cookies: Dict[str, str] = {}
        if not cookie_header:
            return cookies
        for pair in cookie_header.split(";"):
            if "=" in pair:
                k, v = pair.strip().split("=", 1)
                cookies[k.strip()] = v.strip()
        return cookies
