"""
Star HyperFlow Engine — Ultra-Fast Trie Router
Authoritative Reference: STAR_SERVER_SPEC.md

Features:
- Sub-microsecond Radix Trie route lookup
- Dynamic parameter extraction (:param) and wildcards (*wildcard)
- Route-specific and global middleware pipelines
- HTTP method multiplexing (GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD, WS)
- Route introspection and table reflection
"""

import re
from typing import Dict, List, Optional, Tuple, Any, Callable


class RouteMatch:
    def __init__(self, handler: Any, params: Dict[str, str], middleware: List[Any], pattern: str):
        self.handler = handler
        self.params = params
        self.middleware = middleware
        self.pattern = pattern


class TrieNode:
    def __init__(self, part: str = "", is_param: bool = False, param_name: str = "", is_wildcard: bool = False):
        self.part = part
        self.is_param = is_param
        self.param_name = param_name
        self.is_wildcard = is_wildcard
        self.children: Dict[str, "TrieNode"] = {}
        self.param_child: Optional["TrieNode"] = None
        self.wildcard_child: Optional["TrieNode"] = None
        # method -> (handler, middleware, pattern)
        self.handlers: Dict[str, Tuple[Any, List[Any], str]] = {}


class HyperRouter:
    def __init__(self):
        self.root = TrieNode()
        self.global_middleware: List[Any] = []
        self.routes_registry: List[Dict[str, Any]] = []

    def use(self, middleware: Any):
        """Register global middleware."""
        self.global_middleware.append(middleware)

    def add_route(self, method: str, path: str, handler: Any, middleware: Optional[List[Any]] = None):
        """
        Registers a route handler for an HTTP method and path pattern.
        Example: /api/v1/users/:id
        """
        method = method.upper()
        clean_path = "/" + path.strip("/") if path.strip("/") else "/"
        parts = [p for p in clean_path.split("/") if p]
        
        curr = self.root
        for part in parts:
            if part.startswith(":"):
                param_name = part[1:]
                if not curr.param_child:
                    curr.param_child = TrieNode(part=part, is_param=True, param_name=param_name)
                curr = curr.param_child
            elif part.startswith("*"):
                wildcard_name = part[1:] if len(part) > 1 else "path"
                if not curr.wildcard_child:
                    curr.wildcard_child = TrieNode(part=part, is_wildcard=True, param_name=wildcard_name)
                curr = curr.wildcard_child
                break
            else:
                if part not in curr.children:
                    curr.children[part] = TrieNode(part=part)
                curr = curr.children[part]

        mw = list(middleware) if middleware else []
        curr.handlers[method] = (handler, mw, clean_path)
        self.routes_registry.append({
            "method": method,
            "path": clean_path,
            "handler": handler,
            "middleware_count": len(self.global_middleware) + len(mw)
        })

    def match(self, method: str, path: str) -> Optional[RouteMatch]:
        """
        Matches an incoming HTTP method and path against the Trie.
        Returns RouteMatch with handler, captured params, and full middleware chain.
        """
        method = method.upper()
        clean_path = "/" + path.strip("/") if path.strip("/") else "/"
        parts = [p for p in clean_path.split("/") if p]
        params: Dict[str, str] = {}

        def _search(node: TrieNode, idx: int) -> Optional[Tuple[Any, List[Any], str]]:
            # Wildcard match captures everything remaining
            if node.wildcard_child and node.wildcard_child.is_wildcard:
                wc_node = node.wildcard_child
                remaining = "/".join(parts[idx:])
                params[wc_node.param_name] = remaining
                if method in wc_node.handlers:
                    return wc_node.handlers[method]
                if "ALL" in wc_node.handlers:
                    return wc_node.handlers["ALL"]

            if idx == len(parts):
                if method in node.handlers:
                    return node.handlers[method]
                if "ALL" in node.handlers:
                    return node.handlers["ALL"]
                return None

            curr_part = parts[idx]

            # 1. Exact static segment match
            if curr_part in node.children:
                res = _search(node.children[curr_part], idx + 1)
                if res is not None:
                    return res

            # 2. Parameterized segment match (:param)
            if node.param_child:
                params[node.param_child.param_name] = curr_part
                res = _search(node.param_child, idx + 1)
                if res is not None:
                    return res
                # Backtrack param
                params.pop(node.param_child.param_name, None)

            return None

        match_res = _search(self.root, 0)
        if match_res:
            handler, route_mw, pattern = match_res
            combined_mw = list(self.global_middleware) + list(route_mw)
            return RouteMatch(handler=handler, params=params, middleware=combined_mw, pattern=pattern)

        return None

    def get_all_routes(self) -> List[Dict[str, Any]]:
        """Returns metadata list of all registered routes."""
        return list(self.routes_registry)
