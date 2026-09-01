import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_master_icon(size=1024):
    # 1. Create smooth radial & linear gradient background
    img = Image.new("RGBA", (size, size), (8, 18, 32, 255)) # Dark navy base #081220
    draw = ImageDraw.Draw(img)

    # Draw gradient circles from center-top
    cx, cy = size / 2, size * 0.45
    max_r = size * 0.75
    for r in range(int(max_r), 0, -2):
        factor = 1.0 - (r / max_r)
        if factor > 0.5:
            t = (factor - 0.5) * 2.0
            red = int(0 * (1 - t) + 0 * t)
            green = int(102 * (1 - t) + 163 * t)
            blue = int(153 * (1 - t) + 224 * t)
            alpha = int(255 * factor * 0.9)
        else:
            t = factor * 2.0
            red = int(8 * (1 - t) + 0 * t)
            green = int(18 * (1 - t) + 102 * t)
            blue = int(32 * (1 - t) + 153 * t)
            alpha = int(255 * factor * 0.7)
        
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(red, green, blue, alpha))

    # Add soft outer ambient glow for droplet
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([size * 0.25, size * 0.25, size * 0.75, size * 0.85], fill=(0, 220, 255, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=60))
    img = Image.alpha_composite(img, glow)

    # Draw Water Drop + Pulse Wave Vector Motif
    drop_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(drop_layer)

    drop_cx, drop_cy = 512, 590
    drop_r = 205
    tip_x, tip_y = 512, 235

    points = []
    tangent_angle = math.acos(drop_r / (drop_cy - tip_y))
    for a in range(int(math.degrees(tangent_angle)), 180 - int(math.degrees(tangent_angle)) + 180):
        rad = math.radians(a)
        x = drop_cx + drop_r * math.cos(rad)
        y = drop_cy + drop_r * math.sin(rad)
        points.append((x, y))
    
    points.append((tip_x, tip_y))

    # Fill water droplet in pure crisp white
    d_draw.polygon(points, fill=(255, 255, 255, 255))
    d_draw.ellipse([drop_cx - drop_r, drop_cy - drop_r, drop_cx + drop_r, drop_cy + drop_r], fill=(255, 255, 255, 255))

    # Draw pulse wave cutout inside droplet in deep cyan/blue
    wave_path = [
        (325, 590),
        (430, 590),
        (465, 520),
        (495, 680),
        (525, 470),
        (555, 650),
        (585, 560),
        (610, 590),
        (699, 590)
    ]
    d_draw.line(wave_path, fill=(0, 102, 153, 255), width=28, joint="round")

    # Top accent ripple dot
    d_draw.ellipse([512 - 18, 175 - 18, 512 + 18, 175 + 18], fill=(0, 220, 255, 240))

    img = Image.alpha_composite(img, drop_layer)
    return img

def create_round_icon(size=1024):
    master = create_master_icon(size)
    # Mask to circle
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0, size, size], fill=255)
    
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    output.paste(master, (0, 0), mask=mask)
    return output

def create_foreground_icon(size=1024):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    
    # Scale drop to fit Android safe zone (diameter ~ 420px)
    drop_cx, drop_cy = 512, 530
    drop_r = 135
    tip_x, tip_y = 512, 300

    d_draw = ImageDraw.Draw(img)

    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([drop_cx - drop_r - 40, drop_cy - drop_r - 40, drop_cx + drop_r + 40, drop_cy + drop_r + 40], fill=(0, 190, 240, 160))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=30))
    img = Image.alpha_composite(img, glow)
    d_draw = ImageDraw.Draw(img)

    d_draw.ellipse([drop_cx - drop_r, drop_cy - drop_r, drop_cx + drop_r, drop_cy + drop_r], fill=(255, 255, 255, 255))
    
    tangent_angle = math.acos(drop_r / (drop_cy - tip_y))
    left_tx = drop_cx - drop_r * math.sin(tangent_angle)
    left_ty = drop_cy - drop_r * math.cos(tangent_angle)
    right_tx = drop_cx + drop_r * math.sin(tangent_angle)
    right_ty = drop_cy - drop_r * math.cos(tangent_angle)
    d_draw.polygon([(tip_x, tip_y), (left_tx, left_ty), (drop_cx, drop_cy), (right_tx, right_ty)], fill=(255, 255, 255, 255))

    scale_factor = drop_r / 205.0
    base_cx, base_cy = 512, 590
    orig_wave = [
        (325, 590), (430, 590), (465, 520), (495, 680),
        (525, 470), (555, 650), (585, 560), (610, 590), (699, 590)
    ]
    scaled_wave = [
        (drop_cx + (x - base_cx) * scale_factor, drop_cy + (y - base_cy) * scale_factor)
        for x, y in orig_wave
    ]
    d_draw.line(scaled_wave, fill=(0, 102, 153, 255), width=18, joint="round")
    d_draw.ellipse([512 - 12, 260 - 12, 512 + 12, 260 + 12], fill=(0, 220, 255, 240))

    return img

def generate_all():
    os.makedirs("assets/icon", exist_ok=True)
    
    # 1. Master Icon
    master = create_master_icon(1024)
    master.save("assets/icon/icon.png", "PNG")
    print("Generated assets/icon/icon.png (1024x1024)")

    # 2. Foreground Adaptive Icon
    fg = create_foreground_icon(1024)
    fg.save("assets/icon/icon_foreground.png", "PNG")
    print("Generated assets/icon/icon_foreground.png (1024x1024)")

    # 3. Round Icon
    round_icon = create_round_icon(1024)
    round_icon.save("assets/icon/icon_round.png", "PNG")

    # 4. Android Mipmaps
    android_sizes = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192
    }
    
    res_targets = [
        "android/app/src/main/res",
        "android_build/res"
    ]

    for base_res in res_targets:
        for folder, px in android_sizes.items():
            out_dir = f"{base_res}/{folder}"
            os.makedirs(out_dir, exist_ok=True)
            
            # Standard square/squircle icon
            resized = master.resize((px, px), Image.Resampling.LANCZOS)
            resized.save(f"{out_dir}/ic_launcher.png", "PNG")

            # Round icon
            resized_round = round_icon.resize((px, px), Image.Resampling.LANCZOS)
            resized_round.save(f"{out_dir}/ic_launcher_round.png", "PNG")
            
            # Foreground for adaptive
            fg_px = int(px * 108 / 48)
            fg_resized = fg.resize((fg_px, fg_px), Image.Resampling.LANCZOS)
            fg_resized.save(f"{out_dir}/ic_launcher_foreground.png", "PNG")

        # Android anydpi-v26 adaptive icon XML
        v26_dir = f"{base_res}/mipmap-anydpi-v26"
        os.makedirs(v26_dir, exist_ok=True)
        with open(f"{v26_dir}/ic_launcher.xml", "w") as f:
            f.write('''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
''')
        with open(f"{v26_dir}/ic_launcher_round.xml", "w") as f:
            f.write('''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
''')
        
        # Colors XML
        val_dir = f"{base_res}/values"
        os.makedirs(val_dir, exist_ok=True)
        with open(f"{val_dir}/colors.xml", "w") as f:
            f.write('''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#081220</color>
</resources>
''')

    # 5. iOS AppIcon.appiconset
    ios_sizes = [
        (20, 1, "Icon-App-20x20@1x.png"),
        (20, 2, "Icon-App-20x20@2x.png"),
        (20, 3, "Icon-App-20x20@3x.png"),
        (29, 1, "Icon-App-29x29@1x.png"),
        (29, 2, "Icon-App-29x29@2x.png"),
        (29, 3, "Icon-App-29x29@3x.png"),
        (40, 1, "Icon-App-40x40@1x.png"),
        (40, 2, "Icon-App-40x40@2x.png"),
        (40, 3, "Icon-App-40x40@3x.png"),
        (60, 2, "Icon-App-60x60@2x.png"),
        (60, 3, "Icon-App-60x60@3x.png"),
        (76, 1, "Icon-App-76x76@1x.png"),
        (76, 2, "Icon-App-76x76@2x.png"),
        (83.5, 2, "Icon-App-83.5x83.5@2x.png"),
        (1024, 1, "Icon-App-1024x1024@1x.png")
    ]
    ios_dir = "ios/Runner/Assets.xcassets/AppIcon.appiconset"
    os.makedirs(ios_dir, exist_ok=True)
    
    images_json = []
    for pt, scale, filename in ios_sizes:
        px = int(pt * scale)
        resized = master.resize((px, px), Image.Resampling.LANCZOS)
        resized.save(f"{ios_dir}/{filename}", "PNG")
        
        idiom = "ios-marketing" if pt == 1024 else ("ipad" if pt in [76, 83.5] or (pt == 40 and scale == 1) else "iphone")
        images_json.append({
            "size": f"{pt}x{pt}" if pt != 83.5 else "83.5x83.5",
            "idiom": idiom,
            "filename": filename,
            "scale": f"{scale}x"
        })

    import json
    with open(f"{ios_dir}/Contents.json", "w") as f:
        json.dump({
            "images": images_json,
            "info": {
                "version": 1,
                "author": "xcode"
            }
        }, f, indent=2)

    print("=== All Android & iOS App Icons & Round Variants Generated Successfully ===")

if __name__ == "__main__":
    generate_all()
