"""
Star Flutter Base Widgets Library
Authoritative Reference: STAR_FLUTTER.md
Provides Flutter-style fundamental widget trees and layout containers for Star.
"""

from typing import Dict, List, Any, Optional
from star_engine.types import (
    StarValue, StarNull, StarText, StarInteger, StarDecimal, StarBoolean,
    StarList, StarMap, StarFunction, StarBuiltinFunction, StarModule,
    StarVirtualNode
)
from star_sdk.flutter.core import _val_to_py


def _extract_children(props: Dict[str, Any], children: List[Any]):
    if "child" in props and props["child"]:
        c = props["child"]
        if isinstance(c, (list, tuple)):
            children.extend(c)
        else:
            children.append(c)
    if "children" in props and props["children"]:
        c = props["children"]
        if isinstance(c, (list, tuple)):
            children.extend(c)
        elif isinstance(c, StarList):
            children.extend(c.elements)
        else:
            children.append(c)


def create_widgets_module() -> StarModule:
    exports: Dict[str, StarValue] = {}

    def _widget_container(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props.update(_val_to_py(arg))
            elif isinstance(arg, (StarVirtualNode, StarText, StarInteger, StarDecimal)):
                children.append(arg)
        _extract_children(props, children)
        return StarVirtualNode("container", props=props, children=children)

    def _widget_padding(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        if args and isinstance(args[0], (StarMap, StarInteger, StarDecimal)):
            props["padding"] = _val_to_py(args[0])
            children = list(args[1:])
        else:
            children = list(args)
        _extract_children(props, children)
        return StarVirtualNode("padding", props=props, children=children)

    def _widget_center(*args: StarValue) -> StarValue:
        children = [a for a in args if not isinstance(a, StarMap)]
        props = _val_to_py(args[0]) if args and isinstance(args[0], StarMap) else {}
        _extract_children(props, children)
        return StarVirtualNode("center", props=props, children=children)

    def _widget_align(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        if args and isinstance(args[0], (StarText, StarMap)):
            props["alignment"] = _val_to_py(args[0])
            children = list(args[1:])
        else:
            children = list(args)
        _extract_children(props, children)
        return StarVirtualNode("align", props=props, children=children)

    def _widget_sized_box(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        # Support SizedBox(width: 10, height: 20, child: ...) or SizedBox(w, h, child)
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        elif len(args) >= 2 and isinstance(args[0], (StarInteger, StarDecimal)):
            props["width"] = _val_to_py(args[0])
            props["height"] = _val_to_py(args[1])
            children = list(args[2:])
        else:
            children = list(args)
        _extract_children(props, children)
        return StarVirtualNode("sized_box", props=props, children=children)

    def _widget_expanded(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"flex": 1}
        children = []
        if args and isinstance(args[0], (StarInteger, StarDecimal)):
            props["flex"] = int(_val_to_py(args[0]))
            children = list(args[1:])
        elif args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        _extract_children(props, children)
        return StarVirtualNode("expanded", props=props, children=children)

    def _widget_spacer(*args: StarValue) -> StarValue:
        flex = 1
        if args and isinstance(args[0], (StarInteger, StarDecimal)):
            flex = int(_val_to_py(args[0]))
        return StarVirtualNode("spacer", props={"flex": flex})

    def _widget_row(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props.update(_val_to_py(arg))
            else:
                children.append(arg)
        _extract_children(props, children)
        return StarVirtualNode("row", props=props, children=children)

    def _widget_column(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props.update(_val_to_py(arg))
            else:
                children.append(arg)
        _extract_children(props, children)
        return StarVirtualNode("column", props=props, children=children)

    def _widget_stack(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props.update(_val_to_py(arg))
            else:
                children.append(arg)
        _extract_children(props, children)
        return StarVirtualNode("stack", props=props, children=children)

    def _widget_positioned(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        _extract_children(props, children)
        return StarVirtualNode("positioned", props=props, children=children)

    def _widget_wrap(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props.update(_val_to_py(arg))
            else:
                children.append(arg)
        _extract_children(props, children)
        return StarVirtualNode("wrap", props=props, children=children)

    def _widget_list_view(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props.update(_val_to_py(arg))
            elif isinstance(arg, StarList):
                children.extend(arg.elements)
            else:
                children.append(arg)
        _extract_children(props, children)
        return StarVirtualNode("list_view", props=props, children=children)

    def _widget_grid_view(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"crossAxisCount": 2}
        children = []
        start_idx = 0
        if args and isinstance(args[0], (StarInteger, StarDecimal)):
            props["crossAxisCount"] = int(_val_to_py(args[0]))
            start_idx = 1
        elif args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            start_idx = 1
        for arg in args[start_idx:]:
            if isinstance(arg, StarList):
                children.extend(arg.elements)
            else:
                children.append(arg)
        return StarVirtualNode("grid_view", props=props, children=children)

    def _widget_single_child_scroll_view(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props.update(_val_to_py(arg))
            else:
                children.append(arg)
        return StarVirtualNode("single_child_scroll_view", props=props, children=children)

    def _widget_text(*args: StarValue) -> StarValue:
        content = ""
        props: Dict[str, Any] = {}
        if args and isinstance(args[0], StarMap):
            m = _val_to_py(args[0])
            content = str(m.get("content", m.get("text", "")))
            if "style" in m:
                props["style"] = m["style"]
            if len(args) > 1:
                content = args[1].to_string()
        elif args:
            content = args[0].to_string()
            if len(args) > 1 and isinstance(args[1], StarMap):
                props["style"] = _val_to_py(args[1])
        props["content"] = content
        return StarVirtualNode("text", props=props)

    def _widget_icon(*args: StarValue) -> StarValue:
        name = args[0].to_string() if args else "star"
        size = int(_val_to_py(args[1])) if len(args) > 1 and isinstance(args[1], (StarInteger, StarDecimal)) else 24
        color = args[2].to_string() if len(args) > 2 and isinstance(args[2], StarText) else ""
        props = {"name": name, "size": size, "color": color}
        if len(args) > 1 and isinstance(args[1], StarMap):
            props.update(_val_to_py(args[1]))
        return StarVirtualNode("icon", props=props)

    def _widget_image(*args: StarValue) -> StarValue:
        src = args[0].to_string() if args else ""
        w = int(_val_to_py(args[1])) if len(args) > 1 and isinstance(args[1], (StarInteger, StarDecimal)) else 100
        h = int(_val_to_py(args[2])) if len(args) > 2 and isinstance(args[2], (StarInteger, StarDecimal)) else 100
        props = {"src": src, "width": w, "height": h}
        if len(args) > 3 and isinstance(args[3], StarMap):
            props.update(_val_to_py(args[3]))
        return StarVirtualNode("image", props=props)

    def _widget_divider(*args: StarValue) -> StarValue:
        props = _val_to_py(args[0]) if args and isinstance(args[0], StarMap) else {}
        return StarVirtualNode("divider", props=props)

    def _widget_gesture_detector(*args: StarValue) -> StarValue:
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
        elif len(args) >= 2 and isinstance(args[0], (StarFunction, StarBuiltinFunction)):
            listeners["click"] = args[0]
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("gesture_detector", props=props, children=children, listeners=listeners)

    def _widget_custom_paint(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("custom_paint", props=props, children=children)

    def _widget_animated_container(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {"duration": 300}
        children = []
        if args and isinstance(args[0], StarMap):
            props.update(_val_to_py(args[0]))
            children = list(args[1:])
        else:
            children = list(args)
        return StarVirtualNode("animated_container", props=props, children=children)

    def _widget_hero(*args: StarValue) -> StarValue:
        tag = args[0].to_string() if args else ""
        children = list(args[1:])
        return StarVirtualNode("hero", props={"tag": tag}, children=children)

    def _widget_when(*args: StarValue) -> StarValue:
        """
        Declarative conditional widget:
        When(condition, true_widget, false_widget=None)
        """
        if not args:
            return StarVirtualNode("sized_box", props={"width": 0, "height": 0})
        cond_val = args[0]
        # Truthiness evaluation
        is_true = False
        if isinstance(cond_val, StarBoolean):
            is_true = cond_val.value
        elif isinstance(cond_val, StarInteger):
            is_true = cond_val.value != 0
        elif isinstance(cond_val, StarText):
            is_true = len(cond_val.value) > 0 and cond_val.value.lower() not in ("false", "0", "")
        elif not isinstance(cond_val, StarNull):
            is_true = bool(getattr(cond_val, "value", True))

        if is_true:
            return args[1] if len(args) > 1 else StarVirtualNode("sized_box", props={"width": 0, "height": 0})
        else:
            return args[2] if len(args) > 2 else StarVirtualNode("sized_box", props={"width": 0, "height": 0})

    def _widget_switch_case(*args: StarValue) -> StarValue:
        """
        Declarative pattern matching widget:
        SwitchCase(key, cases_map, default_widget=None)
        """
        if len(args) < 2:
            return StarVirtualNode("sized_box", props={"width": 0, "height": 0})
        key_str = args[0].to_string() if hasattr(args[0], "to_string") else str(getattr(args[0], "value", args[0]))
        cases = args[1]
        default_child = args[2] if len(args) > 2 else StarVirtualNode("sized_box", props={"width": 0, "height": 0})
        if isinstance(cases, StarMap):
            if key_str in cases.entries:
                return cases.entries[key_str]
        return default_child

    def _widget_visibility(*args: StarValue) -> StarValue:
        """
        Visibility(visible, child)
        """
        if not args:
            return StarVirtualNode("sized_box", props={"width": 0, "height": 0})
        visible = bool(getattr(args[0], "value", True)) if not isinstance(args[0], StarNull) else False
        child = args[1] if len(args) > 1 else StarVirtualNode("sized_box", props={"width": 0, "height": 0})
        if visible:
            return child
        return StarVirtualNode("sized_box", props={"width": 0, "height": 0})

    def _widget_opacity(*args: StarValue) -> StarValue:
        """
        Opacity(opacity, child)
        """
        val = 1.0
        if args and isinstance(args[0], (StarDecimal, StarInteger)):
            val = float(args[0].value)
        children = list(args[1:])
        return StarVirtualNode("opacity", props={"opacity": val}, children=children)

    # Register all widget constructors
    exports["Container"] = StarBuiltinFunction("Container", _widget_container)
    exports["Padding"] = StarBuiltinFunction("Padding", _widget_padding)
    exports["Center"] = StarBuiltinFunction("Center", _widget_center)
    exports["Align"] = StarBuiltinFunction("Align", _widget_align)
    exports["SizedBox"] = StarBuiltinFunction("SizedBox", _widget_sized_box)
    exports["Expanded"] = StarBuiltinFunction("Expanded", _widget_expanded)
    exports["Spacer"] = StarBuiltinFunction("Spacer", _widget_spacer)
    exports["Row"] = StarBuiltinFunction("Row", _widget_row)
    exports["Column"] = StarBuiltinFunction("Column", _widget_column)
    exports["Stack"] = StarBuiltinFunction("Stack", _widget_stack)
    exports["Positioned"] = StarBuiltinFunction("Positioned", _widget_positioned)
    exports["Wrap"] = StarBuiltinFunction("Wrap", _widget_wrap)
    exports["ListView"] = StarBuiltinFunction("ListView", _widget_list_view)
    exports["GridView"] = StarBuiltinFunction("GridView", _widget_grid_view)
    exports["SingleChildScrollView"] = StarBuiltinFunction("SingleChildScrollView", _widget_single_child_scroll_view)
    exports["Text"] = StarBuiltinFunction("Text", _widget_text)
    exports["Icon"] = StarBuiltinFunction("Icon", _widget_icon)
    exports["Image"] = StarBuiltinFunction("Image", _widget_image)
    exports["Divider"] = StarBuiltinFunction("Divider", _widget_divider)
    exports["GestureDetector"] = StarBuiltinFunction("GestureDetector", _widget_gesture_detector)
    exports["InkWell"] = StarBuiltinFunction("InkWell", _widget_gesture_detector)
    exports["CustomPaint"] = StarBuiltinFunction("CustomPaint", _widget_custom_paint)
    exports["AnimatedContainer"] = StarBuiltinFunction("AnimatedContainer", _widget_animated_container)
    exports["Hero"] = StarBuiltinFunction("Hero", _widget_hero)
    exports["When"] = StarBuiltinFunction("When", _widget_when)
    exports["SwitchCase"] = StarBuiltinFunction("SwitchCase", _widget_switch_case)
    exports["Visibility"] = StarBuiltinFunction("Visibility", _widget_visibility)
    exports["Opacity"] = StarBuiltinFunction("Opacity", _widget_opacity)

    # Geometry & Styling Utilities
    def _edge_insets_all(*args):
        val = _val_to_py(args[0]) if args else 0.0
        return StarMap({
            "top": StarDecimal(float(val)),
            "right": StarDecimal(float(val)),
            "bottom": StarDecimal(float(val)),
            "left": StarDecimal(float(val))
        })

    def _edge_insets_symmetric(*args):
        props = _val_to_py(args[0]) if args and isinstance(args[0], StarMap) else {}
        vert = float(props.get("vertical", 0.0))
        horiz = float(props.get("horizontal", 0.0))
        return StarMap({
            "top": StarDecimal(vert),
            "right": StarDecimal(horiz),
            "bottom": StarDecimal(vert),
            "left": StarDecimal(horiz)
        })

    def _edge_insets_only(*args):
        props = _val_to_py(args[0]) if args and isinstance(args[0], StarMap) else {}
        return StarMap({
            "top": StarDecimal(float(props.get("top", 0.0))),
            "right": StarDecimal(float(props.get("right", 0.0))),
            "bottom": StarDecimal(float(props.get("bottom", 0.0))),
            "left": StarDecimal(float(props.get("left", 0.0)))
        })

    exports["EdgeInsets"] = StarModule("EdgeInsets", {
        "all": StarBuiltinFunction("all", _edge_insets_all),
        "symmetric": StarBuiltinFunction("symmetric", _edge_insets_symmetric),
        "only": StarBuiltinFunction("only", _edge_insets_only),
    })

    def _border_radius_circular(*args):
        r = _val_to_py(args[0]) if args else 0.0
        return StarMap({
            "topLeft": StarDecimal(float(r)),
            "topRight": StarDecimal(float(r)),
            "bottomRight": StarDecimal(float(r)),
            "bottomLeft": StarDecimal(float(r))
        })

    exports["BorderRadius"] = StarModule("BorderRadius", {
        "circular": StarBuiltinFunction("circular", _border_radius_circular),
    })

    def _text_style(*args):
        props = _val_to_py(args[0]) if args and isinstance(args[0], StarMap) else {}
        return StarMap({
            "fontSize": StarDecimal(float(props.get("fontSize", 14.0))),
            "fontWeight": StarText(str(props.get("fontWeight", "normal"))),
            "color": StarText(str(props.get("color", "#ffffff"))),
            "fontStyle": StarText(str(props.get("fontStyle", "normal"))),
        })
    exports["TextStyle"] = StarBuiltinFunction("TextStyle", _text_style)

    def _box_decoration(*args):
        props = _val_to_py(args[0]) if args and isinstance(args[0], StarMap) else {}
        return StarMap({
            "color": StarText(str(props.get("color", ""))),
            "borderRadius": args[0].entries.get("borderRadius", StarNull()) if args and isinstance(args[0], StarMap) else StarNull(),
        })
    exports["BoxDecoration"] = StarBuiltinFunction("BoxDecoration", _box_decoration)

    return StarModule("Widgets", exports)
