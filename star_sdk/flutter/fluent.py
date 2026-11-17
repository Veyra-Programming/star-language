"""
Star Flutter Fluent (Desktop Windows) Component Library
Authoritative Reference: STAR_FLUTTER.md
Provides Microsoft Windows Fluent Design System widgets for Star.
"""

from typing import Dict, List, Any, Optional
from star_engine.types import (
    StarValue, StarNull, StarText, StarInteger, StarDecimal, StarBoolean,
    StarList, StarMap, StarFunction, StarBuiltinFunction, StarModule,
    StarVirtualNode
)
from star_sdk.flutter.core import _val_to_py


def create_fluent_module() -> StarModule:
    exports: Dict[str, StarValue] = {}

    def _fl_app(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"title": "Star Fluent Desktop App", "style_preset": "fluent"}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("fluent_app", props=props, children=children)

    def _fl_nav_view(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"style_preset": "fluent"}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("scaffold", props=props, children=children)

    def _fl_acrylic(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"material": "acrylic", "bg": "#1e293b", "opacity": 0.85}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("container", props=props, children=children)

    def _fl_infobar(*args: StarValue) -> StarValue:
        title = args[0].to_string() if args else ""
        msg = args[1].to_string() if len(args) > 1 else ""
        severity = args[2].to_string() if len(args) > 2 else "info"
        return StarVirtualNode("toast", props={"message": f"{title}: {msg}", "variant": severity})

    def _fl_expander(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"expanded": False}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("card", props=props, children=children)

    exports["FluentApp"] = StarBuiltinFunction("FluentApp", _fl_app)
    exports["NavigationView"] = StarBuiltinFunction("NavigationView", _fl_nav_view)
    exports["Acrylic"] = StarBuiltinFunction("Acrylic", _fl_acrylic)
    exports["InfoBar"] = StarBuiltinFunction("InfoBar", _fl_infobar)
    exports["Expander"] = StarBuiltinFunction("Expander", _fl_expander)

    return StarModule("Fluent", exports)

