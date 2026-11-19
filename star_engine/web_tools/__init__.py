"""
Star Web Tools Subsystem (PHP / Blade / Eloquent / Modern Web Suite)
Authoritative Reference: STAR_WEB_TOOLS_SPEC.md
"""

from star_engine.web_tools.template import TemplateEngine
from star_engine.web_tools.database import Database, QueryBuilder
from star_engine.web_tools.security import Hash, Sanitizer, Validator, CSRF
from star_engine.web_tools.session import Session, SessionManager, Cookie
from star_engine.web_tools.generators import WebGenerators

__all__ = [
    "TemplateEngine",
    "Database",
    "QueryBuilder",
    "Hash",
    "Sanitizer",
    "Validator",
    "CSRF",
    "Session",
    "SessionManager",
    "Cookie",
    "WebGenerators",
]
