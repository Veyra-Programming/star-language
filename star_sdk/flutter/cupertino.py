"""
Star Flutter Cupertino (iOS) Component Library
Authoritative Reference: STAR_FLUTTER.md
Provides Apple Human Interface Design Cupertino widgets for Star.
"""

from typing import Dict, List, Any, Optional
from star_engine.types import (
    StarValue, StarNull, StarText, StarInteger, StarDecimal, StarBoolean,
    StarList, StarMap, StarFunction, StarBuiltinFunction, StarModule,
    StarVirtualNode
)
from star_sdk.flutter.core import _val_to_py


def create_cupertino_module() -> StarModule:
    exports: Dict[str, StarValue] = {}

    def _cup_app(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"title": "Star Cupertino iOS App", "style_preset": "cupertino"}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("cupertino_app", props=props, children=children)

    def _cup_scaffold(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"style_preset": "cupertino"}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("scaffold", props=props, children=children)

    def _cup_nav_bar(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"style_preset": "cupertino"}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        elif args and isinstance(args[0], (StarText, StarVirtualNode)):
            props["title"] = _val_to_py(args[0])
            children = list(args[1:])
        return StarVirtualNode("app_bar", props=props, children=children)

    def _cup_button(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"variant": "cupertino", "radius": 10}
        listeners: Dict[str, Any] = {}
        children = []
        if args and isinstance(args[0], StarMap):
            m = _val_to_py(args[0])
            for k, v in m.items():
                if k in ("onPressed", "onClick"):
                    listeners["click"] = v
                else:
                    props[k] = v
            children = list(args[1:])
        elif args and isinstance(args[0], (StarText, StarVirtualNode)):
            if isinstance(args[0], StarText):
                props["label"] = args[0].value
            else:
                children.append(args[0])
            if len(args) > 1 and not isinstance(args[1], StarNull):
                listeners["click"] = args[1]
        return StarVirtualNode("button", props=props, children=children, listeners=listeners)

    def _cup_text_field(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"variant": "cupertino", "placeholder": "Search or enter text..."}
        listeners: Dict[str, Any] = {}
        if args and isinstance(args[0], StarMap):
            m = _val_to_py(args[0])
            for k, v in m.items():
                if k in ("onChanged", "onChange"):
                    listeners["change"] = v
                else:
                    props[k] = v
        elif args and isinstance(args[0], StarText):
            props["placeholder"] = args[0].value
            if len(args) > 1 and not isinstance(args[1], StarNull):
                listeners["change"] = args[1]
        return StarVirtualNode("input", props=props, listeners=listeners)

    def _cup_switch(*args: StarValue) -> StarValue:
        checked = False
        listeners: Dict[str, Any] = {}
        props: Dict[str, Any] = {"variant": "cupertino"}
        if args and isinstance(args[0], StarMap):
            m = _val_to_py(args[0])
            checked = m.get("value", False)
            if "onChanged" in m:
                listeners["change"] = m["onChanged"]
        elif args and isinstance(args[0], StarBoolean):
            checked = args[0].value
            if len(args) > 1:
                listeners["change"] = args[1]
        props["checked"] = checked
        return StarVirtualNode("switch", props=props, listeners=listeners)

    def _cup_activity_indicator(*args: StarValue) -> StarValue:
        radius = 12
        if args and isinstance(args[0], (StarInteger, StarDecimal)):
            radius = int(args[0].value)
        return StarVirtualNode("spinner", props={"size": radius * 2, "variant": "cupertino"})

    def _cup_segmented_control(*args: StarValue) -> StarValue:
        items = []
        active = 0
        listeners: Dict[str, Any] = {}
        if args and isinstance(args[0], StarList):
            items = [_val_to_py(x) for x in args[0].elements]
            if len(args) > 1 and isinstance(args[1], (StarInteger, StarDecimal)):
                active = int(args[1].value)
            if len(args) > 2 and not isinstance(args[2], StarNull):
                listeners["select"] = args[2]
        return StarVirtualNode("tabs", props={"items": items, "active_idx": active, "variant": "cupertino"}, listeners=listeners)

    # Register all Cupertino widgets
    exports["CupertinoApp"] = StarBuiltinFunction("CupertinoApp", _cup_app)
    exports["CupertinoPageScaffold"] = StarBuiltinFunction("CupertinoPageScaffold", _cup_scaffold)
    exports["CupertinoNavigationBar"] = StarBuiltinFunction("CupertinoNavigationBar", _cup_nav_bar)
    exports["CupertinoButton"] = StarBuiltinFunction("CupertinoButton", _cup_button)
    exports["CupertinoTextField"] = StarBuiltinFunction("CupertinoTextField", _cup_text_field)
    exports["CupertinoSwitch"] = StarBuiltinFunction("CupertinoSwitch", _cup_switch)
    exports["CupertinoActivityIndicator"] = StarBuiltinFunction("CupertinoActivityIndicator", _cup_activity_indicator)
    exports["CupertinoSegmentedControl"] = StarBuiltinFunction("CupertinoSegmentedControl", _cup_segmented_control)

    return StarModule("Cupertino", exports)

