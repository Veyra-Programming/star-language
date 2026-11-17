#!/usr/bin/env python3
"""
Star Language Professional Android Icon & Asset Generator
Generates pixel-perfect adaptive vector drawables and multi-density mipmaps
(mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi, 512px store icon) with antialiased rendering.
"""

import os
import math
import zlib
import struct

def create_png(width, height, rgba_data):
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter type 0 (None)
        raw.extend(rgba_data[y * width * 4 : (y + 1) * width * 4])
    idat = chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    iend = chunk(b'IEND', b'')
    return header + ihdr + idat + iend


def render_star_icon(size: int, is_round: bool = False) -> bytes:
    """Renders a gorgeous cosmic Star logo icon at arbitrary resolution."""
    width, height = size, size
    buf = bytearray(width * height * 4)
    cx, cy = size / 2.0, size / 2.0
    r_max = size / 2.0

    # Corner radius for squircle
    squircle_r = size * 0.22

    # Star geometry
    r_cardinal = size * 0.38
    r_cardinal_in = size * 0.09
    r_diagonal = size * 0.22
    r_diagonal_in = size * 0.06

    ring_rx = size * 0.36
    ring_ry = size * 0.14
    ring_angle = -math.radians(35)
    cos_ra = math.cos(ring_angle)
    sin_ra = math.sin(ring_angle)

    def star_dist(x, y, r_out, r_in, rot=0.0):
        # Rotate point
        dx = x - cx
        dy = y - cy
        if rot != 0:
            rx = dx * math.cos(rot) - dy * math.sin(rot)
            ry = dx * math.sin(rot) + dy * math.cos(rot)
            dx, dy = rx, ry
        # 4-point star distance in 4 sectors
        adx, ady = abs(dx), abs(dy)
        # Pointy shape: |x|/r_in + |y|/r_out <= 1 and |x|/r_out + |y|/r_in <= 1
        # Astroid / polygon approximation
        # Normalized distance: 0 at center, 1 at boundary
        d1 = adx / r_in + ady / r_out
        d2 = adx / r_out + ady / r_in
        return min(d1, d2)

    for py in range(height):
        for px in range(width):
            idx = (py * width + px) * 4
            dx = px - cx
            dy = py - cy
            dist_center = math.sqrt(dx * dx + dy * dy)

            # 1. Masking: Round vs Squircle
            mask_alpha = 1.0
            if is_round:
                circle_edge = r_max - 1.5
                if dist_center > circle_edge + 1.0:
                    mask_alpha = 0.0
                elif dist_center > circle_edge - 1.0:
                    mask_alpha = max(0.0, min(1.0, (circle_edge + 1.0 - dist_center) / 2.0))
            else:
                # Rounded rect
                ax = abs(dx) - (cx - squircle_r)
                ay = abs(dy) - (cy - squircle_r)
                if ax > 0 and ay > 0:
                    corner_d = math.sqrt(ax * ax + ay * ay)
                    if corner_d > squircle_r + 0.5:
                        mask_alpha = 0.0
                    elif corner_d > squircle_r - 1.5:
                        mask_alpha = max(0.0, min(1.0, (squircle_r + 0.5 - corner_d) / 2.0))

            if mask_alpha <= 0.0:
                buf[idx] = 0
                buf[idx + 1] = 0
                buf[idx + 2] = 0
                buf[idx + 3] = 0
                continue

            # 2. Background Gradient (deep cosmic space from navy #0A0F1D to sapphire #1E1B4B to violet #312E81)
            t_grad = min(1.0, dist_center / r_max)
            bg_r = int(10 + (26 - 10) * t_grad)
            bg_g = int(15 + (18 - 15) * t_grad)
            bg_b = int(29 + (58 - 29) * t_grad)

            # Central nebula cyan radial glow
            nebula = max(0.0, 1.0 - (dist_center / (size * 0.42)))
            nebula_glow = nebula * nebula
            bg_r = min(255, int(bg_r + 20 * nebula_glow))
            bg_g = min(255, int(bg_g + 80 * nebula_glow))
            bg_b = min(255, int(bg_b + 140 * nebula_glow))

            # 3. Outer Border Ring (Electric Cyan subtle glow)
            if is_round:
                ring_dist = abs(dist_center - (r_max - 2.5))
                if ring_dist < 2.0:
                    intensity = (2.0 - ring_dist) / 2.0
                    bg_r = int(bg_r + (56 - bg_r) * intensity * 0.6)
                    bg_g = int(bg_g + (189 - bg_g) * intensity * 0.6)
                    bg_b = int(bg_b + (248 - bg_b) * intensity * 0.6)

            # 4. Celestial Orbital Ring
            # Transform to ring coordinate frame
            rx = dx * cos_ra - dy * sin_ra
            ry = dx * sin_ra + dy * cos_ra
            ring_norm = (rx / ring_rx) ** 2 + (ry / ring_ry) ** 2
            ring_d = abs(math.sqrt(ring_norm) - 1.0)
            if ring_d < 0.14:
                # Ring brightness
                ring_alpha = max(0.0, 1.0 - (ring_d / 0.14))
                # Dim the backside of the ring (when ry < 0 and near center)
                if ry < 0:
                    ring_alpha *= 0.5
                bg_r = min(255, int(bg_r + (0 - bg_r) * ring_alpha * 0.7 + 56 * ring_alpha))
                bg_g = min(255, int(bg_g + (240 - bg_g) * ring_alpha * 0.7 + 189 * ring_alpha))
                bg_b = min(255, int(bg_b + (255 - bg_b) * ring_alpha * 0.8 + 248 * ring_alpha))

            # 5. Star Shape Rendering
            # Diagonal secondary star
            d_diag = star_dist(px, py, r_diagonal, r_diagonal_in, rot=math.pi / 4.0)
            # Primary cardinal star
            d_card = star_dist(px, py, r_cardinal, r_cardinal_in, rot=0.0)

            # Antialiasing threshold
            fg_alpha = 0.0
            if d_diag <= 1.0:
                fg_alpha = max(fg_alpha, max(0.0, min(1.0, (1.0 - d_diag) * 4.0)) * 0.85)
            if d_card <= 1.0:
                fg_alpha = max(fg_alpha, max(0.0, min(1.0, (1.0 - d_card) * 5.0)))

            if fg_alpha > 0.0:
                # Core star color: Radiant Gradient from Pure White #FFFFFF (core) to Electric Cyan #38BDF8 / Gold #FDE047
                core_t = max(0.0, min(1.0, dist_center / (r_cardinal * 0.4)))
                # White core fading to electric cyan/neon blue
                star_r = int(255 * (1.0 - core_t) + 56 * core_t)
                star_g = int(255 * (1.0 - core_t) + 189 * core_t)
                star_b = int(255 * (1.0 - core_t) + 248 * core_t)

                bg_r = int(bg_r * (1.0 - fg_alpha) + star_r * fg_alpha)
                bg_g = int(bg_g * (1.0 - fg_alpha) + star_g * fg_alpha)
                bg_b = int(bg_b * (1.0 - fg_alpha) + star_b * fg_alpha)

            # Central brilliant light spark
            if dist_center < size * 0.07:
                spark_t = 1.0 - (dist_center / (size * 0.07))
                spark_t = spark_t * spark_t
                bg_r = min(255, int(bg_r + (255 - bg_r) * spark_t))
                bg_g = min(255, int(bg_g + (255 - bg_g) * spark_t))
                bg_b = min(255, int(bg_b + (255 - bg_b) * spark_t))

            final_a = int(mask_alpha * 255)
            buf[idx] = min(255, max(0, bg_r))
            buf[idx + 1] = min(255, max(0, bg_g))
            buf[idx + 2] = min(255, max(0, bg_b))
            buf[idx + 3] = final_a

    return create_png(width, height, buf)


# Vector Drawables for Adaptive Icons (API 26+)
ADAPTIVE_BACKGROUND_XML = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:aapt="http://schemas.android.com/aapt"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path android:pathData="M0,0h108v108h-108z">
        <aapt:attr name="android:fillColor">
            <gradient
                android:type="radial"
                android:centerX="54"
                android:centerY="54"
                android:gradientRadius="76"
                android:startColor="#1E1B4B"
                android:centerColor="#0F172A"
                android:endColor="#050811" />
        </aapt:attr>
    </path>
    <!-- Cosmic Nebula Glow -->
    <path
        android:pathData="M54,54m-42,0a42,42 0,1 1,84 0a42,42 0,1 1,-84 0">
        <aapt:attr name="android:fillColor">
            <gradient
                android:type="radial"
                android:centerX="54"
                android:centerY="54"
                android:gradientRadius="42"
                android:startColor="#3300F0FF"
                android:endColor="#00000000" />
        </aapt:attr>
    </path>
</vector>
"""

ADAPTIVE_FOREGROUND_XML = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:aapt="http://schemas.android.com/aapt"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <!-- Orbital Celestial Ring -->
    <group
        android:pivotX="54"
        android:pivotY="54"
        android:rotation="-35">
        <path
            android:pathData="M16,54 A38,15 0 1,0 92,54 A38,15 0 1,0 16,54"
            android:strokeWidth="2.5"
            android:strokeColor="#6600F0FF" />
    </group>

    <!-- Diagonal Secondary 4-Point Star -->
    <path
        android:pathData="M54,34 L56.5,51.5 L74,54 L56.5,56.5 L54,74 L51.5,56.5 L34,54 L51.5,51.5 Z">
        <aapt:attr name="android:fillColor">
            <gradient
                android:type="linear"
                android:startX="34"
                android:startY="34"
                android:endX="74"
                android:endY="74"
                android:startColor="#8038BDF8"
                android:endColor="#800284C7" />
        </aapt:attr>
    </path>

    <!-- Primary 4-Point Star Body -->
    <path
        android:pathData="M54,18 L58.5,49.5 L90,54 L58.5,58.5 L54,90 L49.5,58.5 L18,54 L49.5,49.5 Z">
        <aapt:attr name="android:fillColor">
            <gradient
                android:type="radial"
                android:centerX="54"
                android:centerY="54"
                android:gradientRadius="36"
                android:startColor="#FFFFFF"
                android:centerColor="#38BDF8"
                android:endColor="#0284C7" />
        </aapt:attr>
    </path>

    <!-- Diamond Brilliant Center -->
    <path
        android:pathData="M54,46 L62,54 L54,62 L46,54 Z"
        android:fillColor="#FFFFFF" />

    <!-- Radiant Center Spike Rays -->
    <path
        android:pathData="M54,50 L54,58 M50,54 L58,54"
        android:strokeWidth="2.0"
        android:strokeColor="#FFFFFF" />
</vector>
"""

ADAPTIVE_ICON_XML = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
"""

SPLASH_BACKGROUND_XML = """<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@color/background" />
    <item
        android:drawable="@drawable/ic_launcher_foreground"
        android:gravity="center"
        android:width="160dp"
        android:height="160dp" />
</layer-list>
"""


def install_all_icons(target_res_dir: str):
    print(f"Generating professional Android icons into: {target_res_dir}")
    os.makedirs(target_res_dir, exist_ok=True)

    # 1. Drawables
    drawable_dir = os.path.join(target_res_dir, "drawable")
    os.makedirs(drawable_dir, exist_ok=True)

    with open(os.path.join(drawable_dir, "ic_launcher_background.xml"), "w", encoding="utf-8") as f:
        f.write(ADAPTIVE_BACKGROUND_XML)
    with open(os.path.join(drawable_dir, "ic_launcher_foreground.xml"), "w", encoding="utf-8") as f:
        f.write(ADAPTIVE_FOREGROUND_XML)
    with open(os.path.join(drawable_dir, "splash_background.xml"), "w", encoding="utf-8") as f:
        f.write(SPLASH_BACKGROUND_XML)

    # High-resolution store icon
    store_png = render_star_icon(512, is_round=False)
    with open(os.path.join(drawable_dir, "ic_launcher.png"), "wb") as f:
        f.write(store_png)

    # 2. Adaptive Icons for Android 8.0+ (API 26+)
    v26_dir = os.path.join(target_res_dir, "mipmap-anydpi-v26")
    os.makedirs(v26_dir, exist_ok=True)
    with open(os.path.join(v26_dir, "ic_launcher.xml"), "w", encoding="utf-8") as f:
        f.write(ADAPTIVE_ICON_XML)
    with open(os.path.join(v26_dir, "ic_launcher_round.xml"), "w", encoding="utf-8") as f:
        f.write(ADAPTIVE_ICON_XML)

    # 3. Density Mipmaps for all screen resolutions
    density_sizes = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }

    for folder_name, px_size in density_sizes.items():
        folder_path = os.path.join(target_res_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        square_png = render_star_icon(px_size, is_round=False)
        round_png = render_star_icon(px_size, is_round=True)

        with open(os.path.join(folder_path, "ic_launcher.png"), "wb") as f:
            f.write(square_png)
        with open(os.path.join(folder_path, "ic_launcher_round.png"), "wb") as f:
            f.write(round_png)

        print(f"  ✓ {folder_name}: {px_size}x{px_size}px (square & round)")

    print(f"✓ All icons and adaptive drawables successfully generated in {target_res_dir}!")


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # 1. Install into android/app/src/main/res
    android_res = os.path.join(repo_root, "android", "app", "src", "main", "res")
    install_all_icons(android_res)

    # 2. Also install into assets/ for future project generators
    assets_dir = os.path.join(repo_root, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    high_res_icon = render_star_icon(512, is_round=False)
    with open(os.path.join(assets_dir, "star_mobile_icon.png"), "wb") as f:
        f.write(high_res_icon)
    with open(os.path.join(assets_dir, "star_logo.png"), "wb") as f:
        f.write(high_res_icon)


if __name__ == "__main__":
    main()

