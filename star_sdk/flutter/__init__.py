"""
Star Flutter Ecosystem & Universal UI Suite
Authoritative Reference: STAR_FLUTTER.md
Provides Flutter-style widget hierarchy, Material 3, Cupertino, Fluent,
Vector Icons, Color Palettes, and 60,000+ UI Components for Star.
"""

from typing import Dict, Any
from star_engine.types import StarModule, StarValue, StarBuiltinFunction, StarInteger
from star_sdk.flutter.core import (
    BuildContext, EdgeInsets, BorderRadius, TextStyle, BoxDecoration
)
from star_sdk.flutter.widgets import create_widgets_module
from star_sdk.flutter.material import create_material_module
from star_sdk.flutter.cupertino import create_cupertino_module
from star_sdk.flutter.fluent import create_fluent_module
from star_sdk.flutter.icons import create_icons_module
from star_sdk.flutter.colors import create_colors_module
from star_sdk.flutter.catalog import create_catalog_module, CATALOG


def create_flutter_module() -> StarModule:
    """
    Unified Flutter root module for Star:
    Combines Widgets, Material, Cupertino, Icons, Colors, and Catalog.
    """
    exports: Dict[str, StarValue] = {}

    # Merge Widgets
    widgets_mod = create_widgets_module()
    exports.update(widgets_mod.exports)

    # Merge Material 3
    mat_mod = create_material_module()
    exports.update(mat_mod.exports)

    # Merge Cupertino
    cup_mod = create_cupertino_module()
    exports.update(cup_mod.exports)

    # Merge Fluent
    fl_mod = create_fluent_module()
    exports.update(fl_mod.exports)

    # Sub-modules
    exports["Icons"] = create_icons_module()
    exports["Colors"] = create_colors_module()
    exports["Catalog"] = create_catalog_module()
    exports["Widgets"] = widgets_mod
    exports["Material"] = mat_mod
    exports["Cupertino"] = cup_mod
    exports["Fluent"] = fl_mod

    # Metrics
    exports["component_count"] = StarInteger(CATALOG.total_count)

    return StarModule("Flutter", exports)

