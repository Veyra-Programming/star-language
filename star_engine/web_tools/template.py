"""
Star Web Tools — Embedded HTML Template Engine (Blade / PHP / Jinja style)
Authoritative Reference: STAR_WEB_TOOLS_SPEC.md
"""

import re
import html
import os
from typing import Dict, Any, List, Optional, Callable


class TemplateEngine:
    """
    Lightweight, high-speed, secure server-side template engine for Star.
    Supports variables, control flow, loops, partial includes, and automatic HTML escaping.
    """

    def __init__(self, templates_dir: Optional[str] = None):
        self.templates_dir = templates_dir or os.getcwd()
        self.filters: Dict[str, Callable[[Any], str]] = {
            "uppercase": lambda v: str(v).upper(),
            "lowercase": lambda v: str(v).lower(),
            "trim": lambda v: str(v).strip(),
            "length": lambda v: str(len(v) if hasattr(v, "__len__") else 0),
            "escape": lambda v: html.escape(str(v)),
            "json": lambda v: self._to_json(v),
        }

    def _to_json(self, v: Any) -> str:
        import json
        return json.dumps(v, ensure_ascii=False)

    def register_filter(self, name: str, fn: Callable[[Any], str]):
        self.filters[name] = fn

    def render(self, template_str: str, context: Optional[Dict[str, Any]] = None) -> str:
        ctx = context or {}

        # 1. Handle partial includes: {% include "header.html" %}
        def _include_repl(m):
            inc_file = m.group(1).strip().strip("'\"")
            inc_path = os.path.join(self.templates_dir, inc_file)
            if os.path.isfile(inc_path):
                with open(inc_path, "r", encoding="utf-8") as f:
                    return self.render(f.read(), ctx)
            return f"<!-- Include Not Found: {inc_file} -->"

        template_str = re.sub(r'\{%\s*include\s+([^%]+)\s*%\}', _include_repl, template_str)

        # 2. Handle Loops: {% for each item in list %} ... {% end %}
        loop_pattern = re.compile(r'\{%\s*for\s+each\s+([a-zA-Z0-9_]+)\s+in\s+([a-zA-Z0-9_\.]+)\s*%\}(.*?)\{%\s*end\s*%\}', re.DOTALL)
        def _loop_repl(m):
            item_var = m.group(1)
            list_key = m.group(2)
            body = m.group(3)

            collection = self._resolve_var(list_key, ctx) or []
            if not isinstance(collection, (list, tuple)):
                return ""

            out_parts = []
            for item in collection:
                sub_ctx = dict(ctx)
                sub_ctx[item_var] = item
                out_parts.append(self.render(body, sub_ctx))
            return "".join(out_parts)

        template_str = loop_pattern.sub(_loop_repl, template_str)

        # 3. Handle Conditionals: {% whenever condition %} ... {% otherwise %} ... {% end %}
        if_pattern = re.compile(r'\{%\s*whenever\s+([^%]+)\s*%\}(.*?)(?:\{%\s*otherwise\s*%\}(.*?))?\{%\s*end\s*%\}', re.DOTALL)
        def _if_repl(m):
            cond_expr = m.group(1).strip()
            true_body = m.group(2)
            false_body = m.group(3) if m.group(3) is not None else ""

            cond_val = self._eval_condition(cond_expr, ctx)
            if cond_val:
                return self.render(true_body, ctx)
            else:
                return self.render(false_body, ctx)

        template_str = if_pattern.sub(_if_repl, template_str)

        # 4. Handle Raw Unescaped Output: {!! expr !!} or {{! expr !}}
        raw_pattern = re.compile(r'(?:\{!!\s*([^!]+)\s*!!\}|\{\{!\s*([^!]+)\s*!\}\})')
        def _raw_repl(m):
            expr = (m.group(1) or m.group(2)).strip()
            return str(self._resolve_expr(expr, ctx))

        template_str = raw_pattern.sub(_raw_repl, template_str)

        # 5. Handle Standard Escaped Variables & Filters: {{ expr }} or {{ expr | filter }}
        var_pattern = re.compile(r'\{\{\s*([^}]+)\s*\}\}')
        def _var_repl(m):
            expr = m.group(1).strip()
            if "|" in expr:
                parts = [p.strip() for p in expr.split("|")]
                val = self._resolve_expr(parts[0], ctx)
                for f_name in parts[1:]:
                    if f_name in self.filters:
                        val = self.filters[f_name](val)
                return html.escape(str(val))
            val = self._resolve_expr(expr, ctx)
            return html.escape(str(val))

        template_str = var_pattern.sub(_var_repl, template_str)
        return template_str

    def render_file(self, filename: str, context: Optional[Dict[str, Any]] = None) -> str:
        filepath = os.path.join(self.templates_dir, filename) if not os.path.isabs(filename) else filename
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Template file not found: '{filepath}'")
        with open(filepath, "r", encoding="utf-8") as f:
            return self.render(f.read(), context)

    def _resolve_expr(self, expr: str, ctx: Dict[str, Any]) -> Any:
        expr = expr.strip()
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        if expr.startswith("'") and expr.endswith("'"):
            return expr[1:-1]
        if expr.isdigit():
            return int(expr)
        if expr.lower() == "true":
            return True
        if expr.lower() == "false":
            return False
        if expr.lower() in ("null", "none"):
            return ""
        return self._resolve_var(expr, ctx)

    def _resolve_var(self, key: str, ctx: Dict[str, Any]) -> Any:
        parts = key.split(".")
        val: Any = ctx
        for p in parts:
            if isinstance(val, dict):
                val = val.get(p, "")
            elif hasattr(val, p):
                val = getattr(val, p)
            else:
                return ""
        return val if val is not None else ""

    def _eval_condition(self, cond: str, ctx: Dict[str, Any]) -> bool:
        cond = cond.strip()
        # Equality: a == b or a is b
        if "==" in cond:
            l, r = cond.split("==", 1)
            return self._resolve_expr(l, ctx) == self._resolve_expr(r, ctx)
        if "!=" in cond:
            l, r = cond.split("!=", 1)
            return self._resolve_expr(l, ctx) != self._resolve_expr(r, ctx)
        if ">=" in cond:
            l, r = cond.split(">=", 1)
            return float(self._resolve_expr(l, ctx)) >= float(self._resolve_expr(r, ctx))
        if "<=" in cond:
            l, r = cond.split("<=", 1)
            return float(self._resolve_expr(l, ctx)) <= float(self._resolve_expr(r, ctx))
        if ">" in cond:
            l, r = cond.split(">", 1)
            return float(self._resolve_expr(l, ctx)) > float(self._resolve_expr(r, ctx))
        if "<" in cond:
            l, r = cond.split("<", 1)
            return float(self._resolve_expr(l, ctx)) < float(self._resolve_expr(r, ctx))

        val = self._resolve_expr(cond, ctx)
        return bool(val)
