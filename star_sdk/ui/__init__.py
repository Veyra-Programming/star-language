"""
Star SDK Declarative UI Module — Upgraded Professional Release
Authoritative Reference: STAR_UI.md
Integrates 60+ UI Widgets, Hardware-Accelerated Animation & Motion Suite
"""

from typing import Dict, List, Any, Optional
from star_engine.types import (
    StarValue, StarNull, StarText, StarInteger, StarDecimal, StarBoolean,
    StarList, StarMap, StarFunction, StarBuiltinFunction, StarModule,
    StarVirtualNode
)
from star_sdk.animation import (
    Curves, SpringSimulation, AnimationController, AnimationStatus,
    Tween, ColorTween, OffsetTween, resolve_curve,
    make_animated_opacity, make_animated_scale, make_animated_slide,
    make_animated_rotation, make_animated_container, make_shimmer,
    make_skeleton, make_pulse, make_bounce, make_shake, make_glow,
    make_marquee, make_confetti, make_ripple, create_animation_module
)


def _star_val_to_py(val: StarValue) -> Any:
    if isinstance(val, (StarInteger, StarDecimal)):
        return val.value
    elif isinstance(val, StarBoolean):
        return val.value
    elif isinstance(val, StarText):
        return val.value
    elif isinstance(val, StarList):
        return [_star_val_to_py(x) for x in val.elements]
    elif isinstance(val, StarMap):
        return {k: _star_val_to_py(v) for k, v in val.entries.items()}
    elif isinstance(val, StarNull):
        return None
    return val


def _to_bool(val: Any) -> bool:
    if isinstance(val, StarBoolean):
        return val.value
    elif isinstance(val, (StarInteger, StarDecimal)):
        return val.value != 0
    elif isinstance(val, StarNull):
        return False
    elif isinstance(val, StarValue):
        return val.is_truthy()
    return bool(val)


def _flatten_children(args: List[Any]) -> List[StarValue]:
    """Safely flattens nested lists or StarList items, filtering out null/empty values."""
    flattened = []
    for arg in args:
        if arg is None or isinstance(arg, StarNull):
            continue
        if isinstance(arg, StarList):
            flattened.extend(_flatten_children(arg.elements))
        elif isinstance(arg, (list, tuple)):
            flattened.extend(_flatten_children(arg))
        else:
            flattened.append(arg)
    return flattened


def create_ui_module() -> StarModule:
    exports: Dict[str, StarValue] = {}

    # ------------------------------------------------------------------------
    # 1. CORE CONTENT & TYPOGRAPHY
    # ------------------------------------------------------------------------
    def _ui_title(*args: StarValue) -> StarValue:
        text = args[0].to_string() if args else ""
        level = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 1
        props: Dict[str, Any] = {"content": text, "level": level}
        if len(args) > 2 and isinstance(args[2], StarMap):
            props["style"] = _star_val_to_py(args[2])
        return StarVirtualNode("title", props)

    def _ui_text(*args: StarValue) -> StarValue:
        text = args[0].to_string() if args else ""
        props: Dict[str, Any] = {"content": text}
        if len(args) > 1 and isinstance(args[1], StarMap):
            props["style"] = _star_val_to_py(args[1])
        return StarVirtualNode("text", props)

    def _ui_button(*args: StarValue) -> StarValue:
        label = args[0].to_string() if args else "Button"
        handler = args[1] if len(args) > 1 and not isinstance(args[1], StarNull) else None
        props: Dict[str, Any] = {"label": label}
        if len(args) > 2 and isinstance(args[2], StarMap):
            props["style"] = _star_val_to_py(args[2])
        listeners = {"click": handler} if handler else {}
        return StarVirtualNode("button", props, listeners=listeners)

    # ------------------------------------------------------------------------
    # 2. LAYOUT CONTAINERS
    # ------------------------------------------------------------------------
    def _ui_column(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        raw_children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props["style"] = _star_val_to_py(arg)
            else:
                raw_children.append(arg)
        children = _flatten_children(raw_children)
        return StarVirtualNode("column", props=props, children=children)

    def _ui_row(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        raw_children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props["style"] = _star_val_to_py(arg)
            else:
                raw_children.append(arg)
        children = _flatten_children(raw_children)
        return StarVirtualNode("row", props=props, children=children)

    def _ui_stack(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        raw_children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props["style"] = _star_val_to_py(arg)
            else:
                raw_children.append(arg)
        children = _flatten_children(raw_children)
        return StarVirtualNode("stack", props=props, children=children)

    def _ui_grid(*args: StarValue) -> StarValue:
        cols = 2
        raw_children = []
        props: Dict[str, Any] = {}
        start_idx = 0
        if args and isinstance(args[0], (StarInteger, StarDecimal)):
            cols = int(args[0].value)
            start_idx = 1
        elif args and isinstance(args[0], StarMap):
            props["style"] = _star_val_to_py(args[0])
            start_idx = 1
        props["columns"] = cols
        for arg in args[start_idx:]:
            raw_children.append(arg)
        children = _flatten_children(raw_children)
        return StarVirtualNode("grid", props=props, children=children)

    def _ui_card(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        raw_children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props["style"] = _star_val_to_py(arg)
            else:
                raw_children.append(arg)
        children = _flatten_children(raw_children)
        return StarVirtualNode("card", props=props, children=children)

    def _ui_container(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        raw_children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props["style"] = _star_val_to_py(arg)
            else:
                raw_children.append(arg)
        children = _flatten_children(raw_children)
        return StarVirtualNode("container", props=props, children=children)

    def _ui_spacer(*args: StarValue) -> StarValue:
        size = int(args[0].value) if args and hasattr(args[0], "value") else None
        return StarVirtualNode("spacer", {"size": size})

    def _ui_badge(*args: StarValue) -> StarValue:
        label = args[0].to_string() if args else ""
        variant = args[1].to_string() if len(args) > 1 and not isinstance(args[1], StarNull) else "primary"
        props: Dict[str, Any] = {"label": label, "variant": variant}
        if len(args) > 2 and isinstance(args[2], StarMap):
            props["style"] = _star_val_to_py(args[2])
        return StarVirtualNode("badge", props)

    def _ui_divider(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        if args and isinstance(args[0], StarMap):
            props["style"] = _star_val_to_py(args[0])
        return StarVirtualNode("divider", props)

    def _ui_input(*args: StarValue) -> StarValue:
        placeholder = args[0].to_string() if args else ""
        on_change = args[1] if len(args) > 1 and not isinstance(args[1], StarNull) else None
        props: Dict[str, Any] = {"placeholder": placeholder}
        if len(args) > 2 and isinstance(args[2], StarMap):
            props["style"] = _star_val_to_py(args[2])
        listeners = {"change": on_change} if on_change else {}
        return StarVirtualNode("input", props, listeners=listeners)

    def _ui_checkbox(*args: StarValue) -> StarValue:
        label = args[0].to_string() if args else ""
        checked = _to_bool(args[1]) if len(args) > 1 else False
        on_change = args[2] if len(args) > 2 and not isinstance(args[2], StarNull) else None
        listeners = {"change": on_change} if on_change else {}
        return StarVirtualNode("checkbox", {"label": label, "checked": checked}, listeners=listeners)

    def _ui_progress(*args: StarValue) -> StarValue:
        val = int(args[0].value) if args and hasattr(args[0], "value") else 0
        max_v = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 100
        props: Dict[str, Any] = {"value": val, "max": max_v}
        if len(args) > 2 and isinstance(args[2], StarMap):
            props["style"] = _star_val_to_py(args[2])
        return StarVirtualNode("progress", props)

    def _ui_scroll(*args: StarValue) -> StarValue:
        props: Dict[str, Any] = {}
        raw_children = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, StarMap):
                props["style"] = _star_val_to_py(arg)
            else:
                raw_children.append(arg)
        children = _flatten_children(raw_children)
        return StarVirtualNode("scroll", props=props, children=children)

    def _ui_icon(*args: StarValue) -> StarValue:
        name = args[0].to_string() if args else "star"
        size = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 20
        color = args[2].to_string() if len(args) > 2 and not isinstance(args[2], StarNull) else ""
        props: Dict[str, Any] = {"name": name, "size": size, "color": color}
        return StarVirtualNode("icon", props)

    def _ui_image(*args: StarValue) -> StarValue:
        src = args[0].to_string() if args else ""
        w = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 0
        h = int(args[2].value) if len(args) > 2 and hasattr(args[2], "value") else 0
        fit = args[3].to_string() if len(args) > 3 else "cover"
        props: Dict[str, Any] = {"src": src, "width": w, "height": h, "fit": fit}
        return StarVirtualNode("image", props)

    def _ui_avatar(*args: StarValue) -> StarValue:
        label = args[0].to_string() if args else ""
        size = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 40
        props: Dict[str, Any] = {"label": label, "size": size}
        if len(args) > 2 and isinstance(args[2], StarMap):
            props["style"] = _star_val_to_py(args[2])
        return StarVirtualNode("avatar", props)

    def _ui_tabs(*args: StarValue) -> StarValue:
        items_val = args[0] if args else StarList([])
        items = [it.to_string() for it in items_val.elements] if isinstance(items_val, StarList) else []
        active_idx = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 0
        on_select = args[2] if len(args) > 2 and not isinstance(args[2], StarNull) else None
        listeners = {"select": on_select} if on_select else {}
        return StarVirtualNode("tabs", {"items": items, "active": active_idx}, listeners=listeners)

    def _ui_toast(*args: StarValue) -> StarValue:
        message = args[0].to_string() if args else ""
        variant = args[1].to_string() if len(args) > 1 else "info"
        return StarVirtualNode("toast", {"message": message, "variant": variant})

    def _ui_spinner(*args: StarValue) -> StarValue:
        size = int(args[0].value) if args and hasattr(args[0], "value") else 24
        color = args[1].to_string() if len(args) > 1 else ""
        return StarVirtualNode("spinner", {"size": size, "color": color})

    def _ui_style(*args: StarValue) -> StarValue:
        if not args:
            return StarNull()
        target = args[0]
        if not isinstance(target, StarVirtualNode):
            return target
        if len(args) > 1 and isinstance(args[1], StarMap):
            style_data = _star_val_to_py(args[1])
            existing_style = target.props.get("style", {})
            if isinstance(existing_style, dict):
                merged = dict(existing_style)
                merged.update(style_data)
                target.props["style"] = merged
            else:
                target.props["style"] = style_data
        return target

    def _ui_styled(*args: StarValue) -> StarValue:
        tag = args[0].to_string() if args else "container"
        style_map = _star_val_to_py(args[1]) if len(args) > 1 and isinstance(args[1], StarMap) else {}
        raw_children = list(args[2:])
        children = _flatten_children(raw_children)
        return StarVirtualNode(tag, props={"style": style_map}, children=children)

    # ------------------------------------------------------------------------
    # 3. EXTRA ADDED PROFESSIONAL WIDGETS
    # ------------------------------------------------------------------------
    def _ui_modal(*args: StarValue) -> StarValue:
        title = args[0].to_string() if args else ""
        is_open = _to_bool(args[1]) if len(args) > 1 else True
        on_close = args[2] if len(args) > 2 and not isinstance(args[2], StarNull) else None
        on_confirm = args[3] if len(args) > 3 and not isinstance(args[3], StarNull) else None
        raw_children = list(args[4:])
        children = _flatten_children(raw_children)
        listeners = {}
        if on_close:
            listeners["close"] = on_close
        if on_confirm:
            listeners["confirm"] = on_confirm
        return StarVirtualNode("modal", {"title": title, "open": is_open}, children=children, listeners=listeners)

    def _ui_dialog(*args: StarValue) -> StarValue:
        title = args[0].to_string() if args else "Alert"
        message = args[1].to_string() if len(args) > 1 else ""
        on_confirm = args[2] if len(args) > 2 and not isinstance(args[2], StarNull) else None
        on_cancel = args[3] if len(args) > 3 and not isinstance(args[3], StarNull) else None
        is_open = _to_bool(args[4]) if len(args) > 4 else True
        listeners = {}
        if on_confirm:
            listeners["confirm"] = on_confirm
        if on_cancel:
            listeners["cancel"] = on_cancel
        return StarVirtualNode("dialog", {"title": title, "message": message, "open": is_open}, listeners=listeners)

    def _ui_drawer(*args: StarValue) -> StarValue:
        is_open = _to_bool(args[0]) if args else False
        side = args[1].to_string() if len(args) > 1 and not isinstance(args[1], StarNull) else "right"
        on_close = args[2] if len(args) > 2 and not isinstance(args[2], StarNull) else None
        raw_children = list(args[3:])
        children = _flatten_children(raw_children)
        listeners = {"close": on_close} if on_close else {}
        return StarVirtualNode("drawer", {"open": is_open, "side": side}, children=children, listeners=listeners)

    def _ui_accordion(*args: StarValue) -> StarValue:
        title = args[0].to_string() if args else ""
        is_expanded = _to_bool(args[1]) if len(args) > 1 else False
        on_toggle = args[2] if len(args) > 2 and not isinstance(args[2], StarNull) else None
        raw_children = list(args[3:])
        children = _flatten_children(raw_children)
        listeners = {"toggle": on_toggle} if on_toggle else {}
        return StarVirtualNode("accordion", {"title": title, "expanded": is_expanded}, children=children, listeners=listeners)

    def _ui_dropdown(*args: StarValue) -> StarValue:
        items_val = args[0] if args else StarList([])
        items = [it.to_string() for it in items_val.elements] if isinstance(items_val, StarList) else []
        selected_idx = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 0
        on_select = args[2] if len(args) > 2 and not isinstance(args[2], StarNull) else None
        placeholder = args[3].to_string() if len(args) > 3 and not isinstance(args[3], StarNull) else "Select option..."
        is_open = _to_bool(args[4]) if len(args) > 4 else False
        listeners = {"select": on_select} if on_select else {}
        return StarVirtualNode("dropdown", {
            "items": items,
            "selected": selected_idx,
            "placeholder": placeholder,
            "open": is_open
        }, listeners=listeners)

    def _ui_tooltip(*args: StarValue) -> StarValue:
        text = args[0].to_string() if args else ""
        position = args[1].to_string() if len(args) > 1 and not isinstance(args[1], StarNull) else "top"
        child = args[2] if len(args) > 2 else None
        children = [child] if child and not isinstance(child, StarNull) else []
        return StarVirtualNode("tooltip", {"text": text, "position": position}, children=children)

    def _ui_breadcrumbs(*args: StarValue) -> StarValue:
        items_val = args[0] if args else StarList([])
        items = [it.to_string() for it in items_val.elements] if isinstance(items_val, StarList) else []
        on_select = args[1] if len(args) > 1 and not isinstance(args[1], StarNull) else None
        listeners = {"select": on_select} if on_select else {}
        return StarVirtualNode("breadcrumbs", {"items": items}, listeners=listeners)

    def _ui_pagination(*args: StarValue) -> StarValue:
        total_pages = int(args[0].value) if args and hasattr(args[0], "value") else 1
        current_page = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 1
        on_change = args[2] if len(args) > 2 and not isinstance(args[2], StarNull) else None
        listeners = {"change": on_change} if on_change else {}
        return StarVirtualNode("pagination", {"total": total_pages, "current": current_page}, listeners=listeners)

    def _ui_table(*args: StarValue) -> StarValue:
        headers_val = args[0] if args else StarList([])
        headers = [h.to_string() for h in headers_val.elements] if isinstance(headers_val, StarList) else []
        rows_val = args[1] if len(args) > 1 else StarList([])
        rows = []
        if isinstance(rows_val, StarList):
            for r in rows_val.elements:
                if isinstance(r, StarList):
                    rows.append([c.to_string() for c in r.elements])
                else:
                    rows.append([r.to_string()])
        return StarVirtualNode("table", {"headers": headers, "rows": rows})

    def _ui_code_block(*args: StarValue) -> StarValue:
        code = args[0].to_string() if args else ""
        lang = args[1].to_string() if len(args) > 1 and not isinstance(args[1], StarNull) else "star"
        return StarVirtualNode("code_block", {"code": code, "language": lang})

    def _ui_segmented_control(*args: StarValue) -> StarValue:
        items_val = args[0] if args else StarList([])
        items = [it.to_string() for it in items_val.elements] if isinstance(items_val, StarList) else []
        selected_idx = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 0
        on_select = args[2] if len(args) > 2 and not isinstance(args[2], StarNull) else None
        listeners = {"select": on_select} if on_select else {}
        return StarVirtualNode("segmented_control", {"items": items, "selected": selected_idx}, listeners=listeners)

    def _ui_stepper(*args: StarValue) -> StarValue:
        steps_val = args[0] if args else StarList([])
        steps = [s.to_string() for s in steps_val.elements] if isinstance(steps_val, StarList) else []
        current_step = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 0
        return StarVirtualNode("stepper", {"steps": steps, "current": current_step})

    def _ui_rating(*args: StarValue) -> StarValue:
        value = float(args[0].value) if args and hasattr(args[0], "value") else 0.0
        max_rating = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 5
        on_change = args[2] if len(args) > 2 and not isinstance(args[2], StarNull) else None
        listeners = {"change": on_change} if on_change else {}
        return StarVirtualNode("rating", {"value": value, "max": max_rating}, listeners=listeners)

    def _ui_fab(*args: StarValue) -> StarValue:
        label = args[0].to_string() if args else "＋"
        on_click = args[1] if len(args) > 1 and not isinstance(args[1], StarNull) else None
        icon = args[2].to_string() if len(args) > 2 and not isinstance(args[2], StarNull) else "plus"
        props: Dict[str, Any] = {"label": label, "icon": icon}
        if len(args) > 3 and isinstance(args[3], StarMap):
            props["style"] = _star_val_to_py(args[3])
        listeners = {"click": on_click} if on_click else {}
        return StarVirtualNode("fab", props, listeners=listeners)

    def _ui_bottom_sheet(*args: StarValue) -> StarValue:
        is_open = args[0].is_truthy() if args else False
        on_close = args[1] if len(args) > 1 and not isinstance(args[1], StarNull) else None
        raw_children = list(args[2:])
        children = _flatten_children(raw_children)
        listeners = {"close": on_close} if on_close else {}
        return StarVirtualNode("bottom_sheet", {"open": is_open}, children=children, listeners=listeners)

    # ------------------------------------------------------------------------
    # 4. ANIMATION VIRTUAL NODES INTEGRATION
    # ------------------------------------------------------------------------
    anim_mod = create_animation_module()
    for anim_name, anim_fn in anim_mod.exports.items():
        exports[anim_name] = anim_fn

    # Base UI Component Registry
    exports["title"] = StarBuiltinFunction("title", _ui_title)
    exports["text"] = StarBuiltinFunction("text", _ui_text)
    exports["button"] = StarBuiltinFunction("button", _ui_button)
    exports["column"] = StarBuiltinFunction("column", _ui_column)
    exports["row"] = StarBuiltinFunction("row", _ui_row)
    exports["stack"] = StarBuiltinFunction("stack", _ui_stack)
    exports["grid"] = StarBuiltinFunction("grid", _ui_grid)
    exports["card"] = StarBuiltinFunction("card", _ui_card)
    exports["container"] = StarBuiltinFunction("container", _ui_container)
    exports["box"] = StarBuiltinFunction("box", _ui_container)
    exports["spacer"] = StarBuiltinFunction("spacer", _ui_spacer)
    exports["badge"] = StarBuiltinFunction("badge", _ui_badge)
    exports["divider"] = StarBuiltinFunction("divider", _ui_divider)
    exports["input"] = StarBuiltinFunction("input", _ui_input)
    exports["checkbox"] = StarBuiltinFunction("checkbox", _ui_checkbox)
    exports["progress"] = StarBuiltinFunction("progress", _ui_progress)
    exports["scroll"] = StarBuiltinFunction("scroll", _ui_scroll)
    exports["icon"] = StarBuiltinFunction("icon", _ui_icon)
    exports["image"] = StarBuiltinFunction("image", _ui_image)
    exports["avatar"] = StarBuiltinFunction("avatar", _ui_avatar)
    exports["tabs"] = StarBuiltinFunction("tabs", _ui_tabs)
    exports["toast"] = StarBuiltinFunction("toast", _ui_toast)
    exports["spinner"] = StarBuiltinFunction("spinner", _ui_spinner)
    exports["style"] = StarBuiltinFunction("style", _ui_style)
    exports["styled"] = StarBuiltinFunction("styled", _ui_styled)

    # New Extended Widgets
    exports["modal"] = StarBuiltinFunction("modal", _ui_modal)
    exports["dialog"] = StarBuiltinFunction("dialog", _ui_dialog)
    exports["drawer"] = StarBuiltinFunction("drawer", _ui_drawer)
    exports["accordion"] = StarBuiltinFunction("accordion", _ui_accordion)
    exports["dropdown"] = StarBuiltinFunction("dropdown", _ui_dropdown)
    exports["tooltip"] = StarBuiltinFunction("tooltip", _ui_tooltip)
    exports["breadcrumbs"] = StarBuiltinFunction("breadcrumbs", _ui_breadcrumbs)
    exports["pagination"] = StarBuiltinFunction("pagination", _ui_pagination)
    exports["table"] = StarBuiltinFunction("table", _ui_table)
    exports["code_block"] = StarBuiltinFunction("code_block", _ui_code_block)
    exports["segmented_control"] = StarBuiltinFunction("segmented_control", _ui_segmented_control)
    exports["stepper"] = StarBuiltinFunction("stepper", _ui_stepper)
    exports["rating"] = StarBuiltinFunction("rating", _ui_rating)
    exports["fab"] = StarBuiltinFunction("fab", _ui_fab)
    exports["bottom_sheet"] = StarBuiltinFunction("bottom_sheet", _ui_bottom_sheet)

    # Mobile components integration
    from star_sdk.mobile.components import (
        make_safe_area, make_scroll_view, make_app_bar,
        make_bottom_navigation, make_switch, make_action_sheet,
        make_slider
    )
    exports["slider"] = StarBuiltinFunction("slider", make_slider)
    exports["safe_area"] = StarBuiltinFunction("safe_area", make_safe_area)
    exports["scroll_view"] = StarBuiltinFunction("scroll_view", make_scroll_view)
    exports["app_bar"] = StarBuiltinFunction("app_bar", make_app_bar)
    exports["bottom_navigation"] = StarBuiltinFunction("bottom_navigation", make_bottom_navigation)
    exports["switch"] = StarBuiltinFunction("switch", make_switch)
    exports["action_sheet"] = StarBuiltinFunction("action_sheet", make_action_sheet)

    # Sub-modules
    exports["Animation"] = anim_mod
    exports["Motion"] = anim_mod

    # Flutter & 60,000+ UI Component Suite Integration
    from star_sdk.flutter import (
        create_flutter_module, create_material_module, create_cupertino_module,
        create_fluent_module, create_widgets_module, create_icons_module,
        create_colors_module, create_catalog_module
    )
    fl_mod = create_flutter_module()
    exports["Flutter"] = fl_mod
    exports["Material"] = create_material_module()
    exports["Cupertino"] = create_cupertino_module()
    exports["Fluent"] = create_fluent_module()
    exports["Widgets"] = create_widgets_module()
    exports["Catalog"] = create_catalog_module()
    exports["Icons"] = create_icons_module()
    exports["Colors"] = create_colors_module()

    # Direct Flutter widget constructors available via UI.*
    for k, v in fl_mod.exports.items():
        if k not in exports:
            exports[k] = v

    return StarModule("UI", exports)


UI = create_ui_module()
