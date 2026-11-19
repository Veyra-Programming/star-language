"""
Star Web Tools — Security, Cryptographic Hashing & Input Validation Suite
Authoritative Reference: STAR_WEB_TOOLS_SPEC.md
"""

import hashlib
import hmac
import os
import re
import html
import secrets
from typing import Dict, Any, List, Optional, Tuple


class Hash:
    """Cryptographic Password & Secret Hashing (PBKDF2-HMAC-SHA256)."""

    @classmethod
    def make(cls, password: str, salt: Optional[str] = None, iterations: int = 100000) -> str:
        s = salt or secrets.token_hex(16)
        pwd_bytes = password.encode("utf-8")
        salt_bytes = s.encode("utf-8")
        derived = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt_bytes, iterations)
        return f"pbkdf2:sha256:{iterations}${s}${derived.hex()}"

    @classmethod
    def verify(cls, password: str, hashed_string: str) -> bool:
        try:
            parts = hashed_string.split("$")
            if len(parts) != 3:
                return False
            meta, salt, expected_hex = parts[0], parts[1], parts[2]
            iterations = int(meta.split(":")[2])
            derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations)
            return hmac.compare_digest(derived.hex(), expected_hex)
        except Exception:
            return False


class Sanitizer:
    """XSS prevention & HTML text sanitizer."""

    @classmethod
    def escape(cls, text: str) -> str:
        return html.escape(str(text))

    @classmethod
    def strip_tags(cls, text: str) -> str:
        return re.sub(r'<[^>]*?>', '', str(text))

    @classmethod
    def slugify(cls, text: str) -> str:
        text = str(text).lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        return re.sub(r'[\s_-]+', '-', text).strip('-')


class Validator:
    """Declarative schema and web input validation engine."""

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    @classmethod
    def validate(cls, data: Dict[str, Any], rules: Dict[str, str]) -> Dict[str, Any]:
        errors: Dict[str, List[str]] = {}

        for field, rule_str in rules.items():
            rule_list = rule_str.split("|")
            val = data.get(field)

            for r in rule_list:
                r = r.strip()
                if r == "required":
                    if val is None or (isinstance(val, str) and not val.strip()):
                        errors.setdefault(field, []).append(f"Field '{field}' is required.")
                elif r == "email":
                    if val and not cls.EMAIL_REGEX.match(str(val)):
                        errors.setdefault(field, []).append(f"Field '{field}' must be a valid email.")
                elif r == "numeric":
                    if val is not None and not (isinstance(val, (int, float)) or (isinstance(val, str) and val.replace(".", "", 1).isdigit())):
                        errors.setdefault(field, []).append(f"Field '{field}' must be numeric.")
                elif r.startswith("min:"):
                    min_len = int(r.split(":")[1])
                    if val is not None:
                        length = len(val) if hasattr(val, "__len__") else float(val)
                        if length < min_len:
                            errors.setdefault(field, []).append(f"Field '{field}' must have minimum length/value of {min_len}.")
                elif r.startswith("max:"):
                    max_len = int(r.split(":")[1])
                    if val is not None:
                        length = len(val) if hasattr(val, "__len__") else float(val)
                        if length > max_len:
                            errors.setdefault(field, []).append(f"Field '{field}' cannot exceed length/value of {max_len}.")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "data": data,
        }


class CSRF:
    """Cross-Site Request Forgery (CSRF) Protection."""

    @classmethod
    def generate_token(cls, secret_key: str, session_id: str) -> str:
        random_bytes = secrets.token_hex(16)
        sig = hmac.new(secret_key.encode("utf-8"), f"{session_id}:{random_bytes}".encode("utf-8"), hashlib.sha256).hexdigest()
        return f"{random_bytes}.{sig}"

    @classmethod
    def verify_token(cls, token: str, secret_key: str, session_id: str) -> bool:
        try:
            random_bytes, sig = token.split(".")
            expected_sig = hmac.new(secret_key.encode("utf-8"), f"{session_id}:{random_bytes}".encode("utf-8"), hashlib.sha256).hexdigest()
            return hmac.compare_digest(sig, expected_sig)
        except Exception:
            return False
