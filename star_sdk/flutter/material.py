"""
Star Flutter Material 3 (M3) Component Library
Authoritative Reference: STAR_FLUTTER.md
Provides complete Google Material Design 3 widgets for Star.
"""

from typing import Dict, List, Any, Optional
from star_engine.types import (
    StarValue, StarNull, StarText, StarInteger, StarDecimal, StarBoolean,
    StarList, StarMap, StarFunction, StarBuiltinFunction, StarModule,
    StarVirtualNode
)
from star_sdk.flutter.core import _val_to_py
from star_sdk.flutter.widgets import _extract_children


def create_material_module() -> StarModule:
    exports: Dict[str, StarValue] = {}

    def _mat_app(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"title": "Star Flutter App"}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("material_app", props=props, children=children)

    def _mat_scaffold(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        if args and isinstance(args[0], StarMap):
            m = _val_to_py(args[0])
            props.update(m)
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("scaffold", props=props, children=children)

    def _mat_app_bar(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"title": "AppBar"}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        elif args and isinstance(args[0], (StarText, StarVirtualNode)):
            props["title"] = _val_to_py(args[0])
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("app_bar", props=props, children=children)

    def _mat_elevated_button(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"variant": "elevated"}
        listeners: Dict[str, Any] = {}
        children = []
        # Support ElevatedButton(label, onClick) or ElevatedButton(onPressed: ..., child: ...)
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
            if len(args) > 2 and isinstance(args[2], StarMap):
                props["style"] = _val_to_py(args[2])
        return StarVirtualNode("button", props=props, children=children, listeners=listeners)

    def _mat_filled_button(*args: StarValue) -> StarValue:
        res = _mat_elevated_button(*args)
        res.props["variant"] = "filled"
        return res

    def _mat_tonal_button(*args: StarValue) -> StarValue:
        res = _mat_elevated_button(*args)
        res.props["variant"] = "tonal"
        return res

    def _mat_outlined_button(*args: StarValue) -> StarValue:
        res = _mat_elevated_button(*args)
        res.props["variant"] = "outlined"
        return res

    def _mat_text_button(*args: StarValue) -> StarValue:
        res = _mat_elevated_button(*args)
        res.props["variant"] = "text"
        return res

    def _mat_icon_button(*args: StarValue) -> StarValue:
        icon_name = "star"
        listeners: Dict[str, Any] = {}
        props: Dict[str, Any] = {"variant": "icon"}
        if args and isinstance(args[0], (StarText, StarVirtualNode)):
            if isinstance(args[0], StarText):
                icon_name = args[0].value
            props["icon"] = icon_name
            if len(args) > 1 and not isinstance(args[1], StarNull):
                listeners["click"] = args[1]
        elif args and isinstance(args[0], StarMap):
            m = _val_to_py(args[0])
            props.update(m)
            if "onPressed" in m:
                listeners["click"] = m["onPressed"]
        return StarVirtualNode("button", props=props, listeners=listeners)

    def _mat_fab(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"variant": "fab"}
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
        elif args and not isinstance(args[0], StarNull):
            listeners["click"] = args[0]
            children = list(args[1:])
        return StarVirtualNode("fab", props=props, children=children, listeners=listeners)

    def _mat_card(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"elevation": 2}
        children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props.update(_val_to_py(arg))
            else:
                children.append(arg)
        _extract_children(props, children)
        if "subtitle" in props and props["subtitle"]:
            children.insert(0, StarVirtualNode("text", props={"content": str(props["subtitle"])}))
        if "title" in props and props["title"]:
            children.insert(0, StarVirtualNode("title", props={"content": str(props["title"]), "level": 2}))
        return StarVirtualNode("card", props=props, children=children)

    def _mat_list_tile(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        listeners: Dict[str, Any] = {}
        children = []
        if args and isinstance(args[0], StarMap):
            m = _val_to_py(args[0])
            for k, v in m.items():
                if k in ("onTap", "onClick"):
                    listeners["click"] = v
                else:
                    props[k] = v
            children = list(args[1:])
        elif args and isinstance(args[0], (StarText, StarVirtualNode)):
            props["title"] = _val_to_py(args[0])
            if len(args) > 1:
                props["subtitle"] = _val_to_py(args[1])
            children = list(args[2:])
        return StarVirtualNode("list_tile", props=props, children=children, listeners=listeners)

    def _mat_text_field(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"placeholder": "Enter text..."}
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

    def _mat_checkbox(*args: StarValue) -> StarValue:
        checked = False
        listeners: Dict[str, Any] = {}
        props: Dict[str, Any] = {}
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
        return StarVirtualNode("checkbox", props=props, listeners=listeners)

    def _mat_switch(*args: StarValue) -> StarValue:
        checked = False
        listeners: Dict[str, Any] = {}
        props: Dict[str, Any] = {}
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

    def _mat_slider(*args: StarValue) -> StarValue:
        val = 0.0
        min_v = 0.0
        max_v = 100.0
        listeners: Dict[str, Any] = {}
        props: Dict[str, Any] = {}
        if args and isinstance(args[0], StarMap):
            m = _val_to_py(args[0])
            val = float(m.get("value", 0.0))
            min_v = float(m.get("min", 0.0))
            max_v = float(m.get("max", 100.0))
            if "onChanged" in m:
                listeners["change"] = m["onChanged"]
        elif args and isinstance(args[0], (StarInteger, StarDecimal)):
            val = float(args[0].value)
            if len(args) > 1:
                min_v = float(args[1].value)
            if len(args) > 2:
                max_v = float(args[2].value)
            if len(args) > 3:
                listeners["change"] = args[3]
        props["value"] = val
        props["min"] = min_v
        props["max"] = max_v
        return StarVirtualNode("slider", props=props, listeners=listeners)

    def _mat_badge(*args: StarValue) -> StarValue:
        label = args[0].to_string() if args else ""
        variant = args[1].to_string() if len(args) > 1 and isinstance(args[1], StarText) else "primary"
        children = list(args[2:])
        return StarVirtualNode("badge", props={"label": label, "variant": variant}, children=children)

    def _mat_chip(*args: StarValue) -> StarValue:
        label = args[0].to_string() if args else ""
        props: Dict[str, Any] = {"label": label}
        if len(args) > 1 and isinstance(args[1], StarMap):
            props.update(_val_to_py(args[1]))
        return StarVirtualNode("badge", props=props)

    def _mat_progress_indicator(*args: StarValue) -> StarValue:
        val = 50
        max_val = 100
        props: Dict[str, Any] = {}
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
        elif args and isinstance(args[0], (StarInteger, StarDecimal)):
            val = int(args[0].value)
            if len(args) > 1 and isinstance(args[1], (StarInteger, StarDecimal)):
                max_val = int(args[1].value)
        props["value"] = val
        props["max"] = max_val
        return StarVirtualNode("progress", props=props)

    def _mat_snack_bar(*args: StarValue) -> StarValue:
        msg = args[0].to_string() if args else ""
        variant = args[1].to_string() if len(args) > 1 and isinstance(args[1], StarText) else "info"
        return StarVirtualNode("toast", props={"message": msg, "variant": variant})

    def _mat_dialog(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("dialog", props=props, children=children)

    def _mat_nav_bar(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("navigation_bar", props=props, children=children)

    def _mat_tabs(*args: StarValue) -> StarValue:
        items = ["Tab 1", "Tab 2"]
        active = 0
        listeners: Dict[str, Any] = {}
        if args and isinstance(args[0], StarList):
            items = [_val_to_py(x) for x in args[0].elements]
            if len(args) > 1 and isinstance(args[1], (StarInteger, StarDecimal)):
                active = int(args[1].value)
            if len(args) > 2 and not isinstance(args[2], StarNull):
                listeners["select"] = args[2]
        return StarVirtualNode("tabs", props={"items": items, "active_idx": active}, listeners=listeners)

    # Register all Material 3 widgets
    exports["MaterialApp"] = StarBuiltinFunction("MaterialApp", _mat_app)
    exports["Scaffold"] = StarBuiltinFunction("Scaffold", _mat_scaffold)
    exports["AppBar"] = StarBuiltinFunction("AppBar", _mat_app_bar)
    exports["ElevatedButton"] = StarBuiltinFunction("ElevatedButton", _mat_elevated_button)
    exports["FilledButton"] = StarBuiltinFunction("FilledButton", _mat_filled_button)
    exports["FilledTonalButton"] = StarBuiltinFunction("FilledTonalButton", _mat_tonal_button)
    exports["OutlinedButton"] = StarBuiltinFunction("OutlinedButton", _mat_outlined_button)
    exports["TextButton"] = StarBuiltinFunction("TextButton", _mat_text_button)
    exports["IconButton"] = StarBuiltinFunction("IconButton", _mat_icon_button)
    exports["FloatingActionButton"] = StarBuiltinFunction("FloatingActionButton", _mat_fab)
    exports["Card"] = StarBuiltinFunction("Card", _mat_card)
    exports["ListTile"] = StarBuiltinFunction("ListTile", _mat_list_tile)
    exports["TextField"] = StarBuiltinFunction("TextField", _mat_text_field)
    exports["Checkbox"] = StarBuiltinFunction("Checkbox", _mat_checkbox)
    exports["Switch"] = StarBuiltinFunction("Switch", _mat_switch)
    exports["Slider"] = StarBuiltinFunction("Slider", _mat_slider)
    exports["Badge"] = StarBuiltinFunction("Badge", _mat_badge)
    exports["Chip"] = StarBuiltinFunction("Chip", _mat_chip)
    exports["CircularProgressIndicator"] = StarBuiltinFunction("CircularProgressIndicator", _mat_progress_indicator)
    exports["LinearProgressIndicator"] = StarBuiltinFunction("LinearProgressIndicator", _mat_progress_indicator)
    exports["SnackBar"] = StarBuiltinFunction("SnackBar", _mat_snack_bar)
    exports["AlertDialog"] = StarBuiltinFunction("AlertDialog", _mat_dialog)
    exports["BottomNavigationBar"] = StarBuiltinFunction("BottomNavigationBar", _mat_nav_bar)
    exports["NavigationBar"] = StarBuiltinFunction("NavigationBar", _mat_nav_bar)
    exports["NavigationRail"] = StarBuiltinFunction("NavigationRail", _mat_nav_bar)
    exports["TabBar"] = StarBuiltinFunction("TabBar", _mat_tabs)

    return StarModule("Material", exports)
