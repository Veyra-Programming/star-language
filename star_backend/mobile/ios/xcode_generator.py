"""
Star Apple Xcode Project Generator
Authoritative Reference: STAR_IOS.md (Section 7)
"""

import os
import shutil
from typing import Dict, Any, Optional
from star_backend.mobile.packaging import MobileBundle
from star_backend.mobile.ios.swift_bridge import SwiftNativeBridge
from star_backend.mobile.ios.view_controller import StarViewController
from star_backend.mobile.ios.metal_renderer import iOSMetalRenderer


class XcodeProjectGenerator:
    """
    Generates standard Xcode project structures (.xcodeproj) incorporating
    Swift bridges, MetalKit views, and embedded .starmobile application bundles.
    """
    def __init__(self):
        pass

    def generate_project(
        self,
        bundle: MobileBundle,
        bundle_path: str,
        output_dir: str
    ) -> str:
        os.makedirs(output_dir, exist_ok=True)
        manifest = bundle.manifest
        app_name = "".join(c for c in manifest.name.rstrip(":").strip() if c.isalnum() or c == "_") or "StarApp"
        bundle_id = manifest.package_id

        src_dir = os.path.join(output_dir, app_name)
        res_dir = os.path.join(src_dir, "Resources")
        proj_dir = os.path.join(output_dir, f"{app_name}.xcodeproj")

        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(res_dir, exist_ok=True)
        os.makedirs(proj_dir, exist_ok=True)

        # 1. Info.plist
        with open(os.path.join(src_dir, "Info.plist"), "w", encoding="utf-8") as f:
            f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>{app_name}</string>
    <key>CFBundleIdentifier</key>
    <string>{bundle_id}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>{manifest.version}</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>arm64</string>
        <string>metal</string>
    </array>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
</dict>
</plist>
""")

        # 2. Swift & C Sources
        with open(os.path.join(src_dir, "AppDelegate.swift"), "w", encoding="utf-8") as f:
            f.write(StarViewController.generate_app_delegate_swift(app_name))

        with open(os.path.join(src_dir, "StarViewController.swift"), "w", encoding="utf-8") as f:
            f.write(StarViewController.generate_view_controller_swift(app_name))

        with open(os.path.join(src_dir, "StarMetalView.swift"), "w", encoding="utf-8") as f:
            f.write(iOSMetalRenderer.generate_metal_view_swift())

        with open(os.path.join(src_dir, "StarNativeBridge.swift"), "w", encoding="utf-8") as f:
            f.write(SwiftNativeBridge.generate_swift_bridge_source())

        with open(os.path.join(src_dir, "StarRuntime.h"), "w", encoding="utf-8") as f:
            f.write(SwiftNativeBridge.generate_c_header())

        # 3. Xcode Project PBXProj Descriptor
        with open(os.path.join(proj_dir, "project.pbxproj"), "w", encoding="utf-8") as f:
            f.write(f"""// !$*UTF8*$!
{{
    archiveVersion = 1;
    classes = {{}};
    objectVersion = 56;
    objects = {{
        /* Star Application Xcode Project Scaffold */
        ROOT_OBJ = {{
            isa = PBXProject;
            buildConfigurationList = 1DEB928908733DD80010E9CD;
            compatibilityVersion = "Xcode 14.0";
            developmentRegion = en;
            hasScannedForEncodings = 0;
            knownRegions = (en, Base);
            mainGroup = 1DEB928408733DD80010E9CD;
            productRefGroup = 1DEB928808733DD80010E9CD;
            projectDirPath = "";
            projectRoot = "";
            targets = (
                APP_TARGET /* {app_name} */,
            );
        }};
    }};
    rootObject = ROOT_OBJ;
}}
""")

        # 4. Embed .starmobile bundle into Resources
        shutil.copyfile(bundle_path, os.path.join(res_dir, "app.starmobile"))

        return output_dir
