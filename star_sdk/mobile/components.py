"""
Star SDK Mobile Declarative Component Builders
Authoritative Reference: STAR_MOBILE.md (Section 6)
"""

from typing import Dict, List, Any, Optional
from star_engine.types import (
    StarValue, StarNull, StarText, StarInteger, StarDecimal, StarBoolean,
    StarList, StarMap, StarFunction, StarBuiltinFunction, StarVirtualNode
)


def make_safe_area(*args: StarValue) -> StarVirtualNode:
    children = list(args)
    return StarVirtualNode("safe_area", children=children)


def make_scroll_view(*args: StarValue) -> StarVirtualNode:
    children = []
    props: Dict[str, Any] = {"orientation": "vertical"}
    for arg in args:
        if isinstance(arg, StarVirtualNode):
            children.append(arg)
        elif isinstance(arg, StarText):
            props["orientation"] = arg.value
    return StarVirtualNode("scroll_view", props, children=children)


def make_app_bar(*args: StarValue) -> StarVirtualNode:
    title = args[0].to_string() if args else "App"
    leading = args[1] if len(args) > 1 and not isinstance(args[1], StarNull) else None
    actions = args[2] if len(args) > 2 and not isinstance(args[2], StarNull) else None
    props: Dict[str, Any] = {"title": title}
    children = []
    if leading and isinstance(leading, StarVirtualNode):
        children.append(leading)
    if actions:
        if isinstance(actions, StarList):
            for it in actions.elements:
                if isinstance(it, StarVirtualNode):
                    children.append(it)
        elif isinstance(actions, StarVirtualNode):
            children.append(actions)
    return StarVirtualNode("mobile_app_bar", props, children=children)


def make_bottom_navigation(*args: StarValue) -> StarVirtualNode:
    items_val = args[0] if len(args) > 0 else StarList([])
    selected_idx = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 0
    on_select = args[2] if len(args) > 2 else None
    items_list = [it.to_string() for it in items_val.elements] if isinstance(items_val, StarList) else []
    listeners = {"select": on_select} if on_select else {}
    return StarVirtualNode(
        "bottom_navigation",
        {"items": items_list, "selected": selected_idx},
        listeners=listeners
    )


def make_switch(*args: StarValue) -> StarVirtualNode:
    val = args[0].is_truthy() if args else False
    on_change = args[1] if len(args) > 1 else None
    listeners = {"change": on_change} if on_change else {}
    return StarVirtualNode("mobile_switch", {"value": val}, listeners=listeners)


def make_slider(*args: StarValue) -> StarVirtualNode:
    # Args can be: (value, min, max, onChange) OR (min, max, value, onChange) OR (value, onChange)
    if len(args) >= 4:
        a0 = float(args[0].value) if hasattr(args[0], "value") else 0.0
        a1 = float(args[1].value) if hasattr(args[1], "value") else 0.0
        a2 = float(args[2].value) if hasattr(args[2], "value") else 100.0
        on_change = args[3] if not isinstance(args[3], StarNull) else None
        # Disambiguate (value, min, max) vs (min, max, value):
        # In UI.slider(50.0, 0.0, 100.0, None), a0=50.0, a1=0.0, a2=100.0 -> value=50, min=0, max=100
        if a1 <= a0 <= a2 or a1 <= a2:
            val, min_v, max_v = a0, a1, a2
        else:
            min_v, max_v, val = a0, a1, a2
    elif len(args) == 3:
        min_v = float(args[0].value) if hasattr(args[0], "value") else 0.0
        max_v = float(args[1].value) if hasattr(args[1], "value") else 100.0
        val = float(args[2].value) if hasattr(args[2], "value") else min_v
        on_change = None
    elif len(args) == 2:
        val = float(args[0].value) if hasattr(args[0], "value") else 50.0
        min_v = 0.0
        max_v = 100.0
        on_change = args[1] if not isinstance(args[1], StarNull) else None
    else:
        min_v = 0.0
        max_v = 100.0
        val = float(args[0].value) if args and hasattr(args[0], "value") else 50.0
        on_change = None
    listeners = {"change": on_change} if on_change else {}
    return StarVirtualNode(
        "mobile_slider",
        {"min": min_v, "max": max_v, "value": val},
        listeners=listeners
    )


def make_action_sheet(*args: StarValue) -> StarVirtualNode:
    title = args[0].to_string() if args else ""
    actions_val = args[1] if len(args) > 1 else StarList([])
    actions_list = [it.to_string() for it in actions_val.elements] if isinstance(actions_val, StarList) else []
    on_select = args[2] if len(args) > 2 else None
    listeners = {"select": on_select} if on_select else {}
    return StarVirtualNode(
        "action_sheet",
        {"title": title, "actions": actions_list},
        listeners=listeners
    )
