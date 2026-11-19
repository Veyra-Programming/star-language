"""
Star Standard Library — Web Tools & PHP-style Scripting Suite (use Web / use DB / use Template)
Authoritative Reference: STAR_WEB_TOOLS_SPEC.md
"""

from typing import Dict, Any, List, Optional
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarBuiltinFunction, StarModule, to_star_value, from_star_value
)
from star_engine.web_tools.template import TemplateEngine
from star_engine.web_tools.database import Database, QueryBuilder
from star_engine.web_tools.security import Hash, Sanitizer, Validator, CSRF
from star_engine.web_tools.session import SessionManager, Session, Cookie

_default_template_engine = TemplateEngine()
_default_database = Database(":memory:")
_default_session_manager = SessionManager()


class StarQueryBuilder(StarValue):
    def __init__(self, qb: QueryBuilder):
        self.qb = qb

    @property
    def type_name(self) -> str:
        return "QueryBuilder"

    def to_string(self) -> str:
        return f"<QueryBuilder table='{self.qb.table_name}'>"

    def is_truthy(self) -> bool:
        return True

    def get(self, prop: str) -> StarValue:
        if prop == "select":
            def _select(*args):
                cols = [a.to_string() for a in args]
                new_qb = self.qb.select(*cols)
                return StarQueryBuilder(new_qb)
            return StarBuiltinFunction("select", _select)

        if prop == "where":
            def _where(*args):
                if len(args) == 2:
                    col = args[0].to_string()
                    val = from_star_value(args[1])
                    new_qb = self.qb.where(col, val)
                elif len(args) >= 3:
                    col = args[0].to_string()
                    op = args[1].to_string()
                    val = from_star_value(args[2])
                    new_qb = self.qb.where(col, op, val)
                else:
                    new_qb = self.qb
                return StarQueryBuilder(new_qb)
            return StarBuiltinFunction("where", _where)

        if prop == "order_by":
            def _order_by(*args):
                col = args[0].to_string() if args else "id"
                direction = args[1].to_string() if len(args) > 1 else "asc"
                new_qb = self.qb.order_by(col, direction)
                return StarQueryBuilder(new_qb)
            return StarBuiltinFunction("order_by", _order_by)

        if prop == "limit":
            def _limit(*args):
                n = int(args[0].value) if args else 10
                new_qb = self.qb.limit(n)
                return StarQueryBuilder(new_qb)
            return StarBuiltinFunction("limit", _limit)

        if prop == "offset":
            def _offset(*args):
                n = int(args[0].value) if args else 0
                new_qb = self.qb.offset(n)
                return StarQueryBuilder(new_qb)
            return StarBuiltinFunction("offset", _offset)

        if prop == "get":
            def _get(*args):
                records = self.qb.get()
                return to_star_value(records)
            return StarBuiltinFunction("get", _get)

        if prop == "first":
            def _first(*args):
                record = self.qb.first()
                return to_star_value(record) if record is not None else StarNull()
            return StarBuiltinFunction("first", _first)

        if prop == "count":
            def _count(*args):
                return StarInteger(self.qb.count())
            return StarBuiltinFunction("count", _count)

        if prop == "insert":
            def _insert(*args):
                if not args:
                    return StarInteger(0)
                data = from_star_value(args[0])
                if isinstance(data, dict):
                    row_id = self.qb.insert(data)
                    return StarInteger(row_id)
                return StarInteger(0)
            return StarBuiltinFunction("insert", _insert)

        if prop == "update":
            def _update(*args):
                if not args:
                    return StarInteger(0)
                data = from_star_value(args[0])
                if isinstance(data, dict):
                    rows = self.qb.update(data)
                    return StarInteger(rows)
                return StarInteger(0)
            return StarBuiltinFunction("update", _update)

        if prop == "delete":
            def _delete(*args):
                rows = self.qb.delete()
                return StarInteger(rows)
            return StarBuiltinFunction("delete", _delete)

        return StarNull()


class StarSessionRef(StarValue):
    def __init__(self, session: Session):
        self.session = session

    @property
    def type_name(self) -> str:
        return "Session"

    def to_string(self) -> str:
        return f"<Session id='{self.session.session_id}'>"

    def is_truthy(self) -> bool:
        return True

    def get(self, prop: str) -> StarValue:
        if prop == "id":
            return StarText(self.session.session_id)
        if prop == "get":
            def _get(*args):
                k = args[0].to_string() if args else ""
                default = from_star_value(args[1]) if len(args) > 1 else None
                return to_star_value(self.session.get(k, default))
            return StarBuiltinFunction("get", _get)
        if prop == "set":
            def _set(*args):
                if len(args) >= 2:
                    k = args[0].to_string()
                    v = from_star_value(args[1])
                    self.session.set(k, v)
                return StarNull()
            return StarBuiltinFunction("set", _set)
        if prop == "has":
            def _has(*args):
                k = args[0].to_string() if args else ""
                return StarBoolean(self.session.has(k))
            return StarBuiltinFunction("has", _has)
        if prop == "remove":
            def _remove(*args):
                if args:
                    self.session.remove(args[0].to_string())
                return StarNull()
            return StarBuiltinFunction("remove", _remove)
        if prop == "flash":
            def _flash(*args):
                if len(args) >= 2:
                    self.session.flash(args[0].to_string(), from_star_value(args[1]))
                return StarNull()
            return StarBuiltinFunction("flash", _flash)
        return StarNull()


def create_template_module() -> StarModule:
    exports: Dict[str, StarValue] = {}

    def _render(*args: StarValue) -> StarValue:
        if not args:
            return StarText("")
        tmpl = args[0].to_string()
        ctx = from_star_value(args[1]) if len(args) > 1 else {}
        res = _default_template_engine.render(tmpl, ctx if isinstance(ctx, dict) else {})
        return StarText(res)
    exports["render"] = StarBuiltinFunction("render", _render)

    def _render_file(*args: StarValue) -> StarValue:
        if not args:
            return StarText("")
        filepath = args[0].to_string()
        ctx = from_star_value(args[1]) if len(args) > 1 else {}
        res = _default_template_engine.render_file(filepath, ctx if isinstance(ctx, dict) else {})
        return StarText(res)
    exports["render_file"] = StarBuiltinFunction("render_file", _render_file)

    return StarModule("Template", exports)


def create_db_module() -> StarModule:
    exports: Dict[str, StarValue] = {}

    def _table(*args: StarValue) -> StarValue:
        t_name = args[0].to_string() if args else "default"
        qb = _default_database.table(t_name)
        return StarQueryBuilder(qb)
    exports["table"] = StarBuiltinFunction("table", _table)

    def _raw(*args: StarValue) -> StarValue:
        if not args:
            return StarList([])
        sql = args[0].to_string()
        params = from_star_value(args[1]) if len(args) > 1 else []
        res = _default_database.raw(sql, params if isinstance(params, list) else [])
        return to_star_value(res)
    exports["raw"] = StarBuiltinFunction("raw", _raw)

    return StarModule("DB", exports)


def create_security_module() -> StarModule:
    exports: Dict[str, StarValue] = {}

    # Hash
    exports["hash_make"] = StarBuiltinFunction("hash_make", lambda *a: StarText(Hash.make(a[0].to_string()) if a else ""))
    exports["hash_verify"] = StarBuiltinFunction("hash_verify", lambda *a: StarBoolean(Hash.verify(a[0].to_string(), a[1].to_string()) if len(a) >= 2 else False))

    # Sanitizer
    exports["escape"] = StarBuiltinFunction("escape", lambda *a: StarText(Sanitizer.escape(a[0].to_string()) if a else ""))
    exports["strip_tags"] = StarBuiltinFunction("strip_tags", lambda *a: StarText(Sanitizer.strip_tags(a[0].to_string()) if a else ""))
    exports["slugify"] = StarBuiltinFunction("slugify", lambda *a: StarText(Sanitizer.slugify(a[0].to_string()) if a else ""))

    # Validator
    def _validate(*args: StarValue) -> StarValue:
        data = from_star_value(args[0]) if args else {}
        rules = from_star_value(args[1]) if len(args) > 1 else {}
        res = Validator.validate(data if isinstance(data, dict) else {}, rules if isinstance(rules, dict) else {})
        return to_star_value(res)
    exports["validate"] = StarBuiltinFunction("validate", _validate)

    # CSRF
    exports["csrf_token"] = StarBuiltinFunction("csrf_token", lambda *a: StarText(CSRF.generate_token(a[0].to_string(), a[1].to_string()) if len(a) >= 2 else ""))
    exports["csrf_verify"] = StarBuiltinFunction("csrf_verify", lambda *a: StarBoolean(CSRF.verify_token(a[0].to_string(), a[1].to_string(), a[2].to_string()) if len(a) >= 3 else False))

    return StarModule("Security", exports)


def create_session_module() -> StarModule:
    exports: Dict[str, StarValue] = {}

    def _start(*args: StarValue) -> StarValue:
        sid = args[0].to_string() if args else None
        sess = _default_session_manager.start(sid)
        return StarSessionRef(sess)
    exports["start"] = StarBuiltinFunction("start", _start)

    exports["cookie_serialize"] = StarBuiltinFunction("cookie_serialize", lambda *a: StarText(Cookie.serialize(a[0].to_string(), a[1].to_string()) if len(a) >= 2 else ""))
    exports["cookie_parse"] = StarBuiltinFunction("cookie_parse", lambda *a: to_star_value(Cookie.parse(a[0].to_string()) if a else {}))

    return StarModule("Session", exports)


def create_web_module() -> StarModule:
    tmpl = create_template_module()
    db = create_db_module()
    sec = create_security_module()
    sess = create_session_module()

    exports: Dict[str, StarValue] = {
        "Template": tmpl,
        "DB": db,
        "Security": sec,
        "Session": sess,
        "render": tmpl.get("render"),
        "render_file": tmpl.get("render_file"),
        "table": db.get("table"),
        "hash_make": sec.get("hash_make"),
        "hash_verify": sec.get("hash_verify"),
        "escape": sec.get("escape"),
        "strip_tags": sec.get("strip_tags"),
        "validate": sec.get("validate"),
        "session_start": sess.get("start"),
    }
    return StarModule("Web", exports)
