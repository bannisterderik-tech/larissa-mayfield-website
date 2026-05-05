#!/usr/bin/env python3
"""Generate favicon and OG social share image."""
from PIL import Image, ImageDraw, ImageFont
import os

SITE = "/Users/derikbannister9/larissa-mayfield-website"

# ── Favicon (32x32 and 16x16 ICO) ──────────────────────────────────────────

def gen_favicon():
    sizes = [16, 32, 48]
    images = []
    for sz in sizes:
        img = Image.new("RGBA", (sz, sz), (59, 31, 59, 255))
        draw = ImageDraw.Draw(img)
        # Draw "L" in cream color
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", int(sz * 0.65))
        except:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), "L", font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (sz - tw) // 2 - bbox[0]
        y = (sz - th) // 2 - bbox[1] - int(sz * 0.02)
        draw.text((x, y), "L", fill=(244, 239, 230, 255), font=font)
        images.append(img)

    # Save as ICO
    images[0].save(
        f"{SITE}/favicon.ico",
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    # Also save 180x180 apple-touch-icon
    apple = Image.new("RGBA", (180, 180), (59, 31, 59, 255))
    draw = ImageDraw.Draw(apple)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 110)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), "L", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (180 - tw) // 2 - bbox[0]
    y = (180 - th) // 2 - bbox[1] - 4
    draw.text((x, y), "L", fill=(244, 239, 230, 255), font=font)
    apple.save(f"{SITE}/apple-touch-icon.png")
    print("  ✓ favicon.ico")
    print("  ✓ apple-touch-icon.png")

# ── OG Social Share Image (1200x630) ───────────────────────────────────────

def gen_og_image():
    width, height = 1200, 630
    img = Image.new("RGB", (width, height), (59, 31, 59))
    draw = ImageDraw.Draw(img)

    # Load Larissa headshot and composite on right side
    headshot_path = f"{SITE}/images/larissa-headshot.jpg"
    if os.path.exists(headshot_path):
        hs = Image.open(headshot_path)
        # Resize to fill right panel
        panel_w = 380
        ratio = panel_w / hs.width
        hs = hs.resize((panel_w, int(hs.height * ratio)), Image.LANCZOS)
        # Crop to height
        if hs.height > height:
            top = int((hs.height - height) * 0.2)
            hs = hs.crop((0, top, panel_w, top + height))
        # Create gradient overlay
        gradient = Image.new("RGBA", (80, height), (0, 0, 0, 0))
        for x in range(80):
            alpha = int(255 * (1 - x / 80))
            for y in range(height):
                gradient.putpixel((x, y), (59, 31, 59, alpha))
        img.paste(hs, (width - panel_w, 0))
        img.paste(gradient, (width - panel_w, 0), gradient)

    # Text
    try:
        font_tag = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New.ttf", 14)
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 68)
        font_title_italic = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 68)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
        font_name = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 24)
        font_license = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New.ttf", 12)
    except:
        font_tag = font_title = font_title_italic = font_sub = font_name = font_license = ImageFont.load_default()

    cream = (244, 239, 230)
    cream_muted = (244, 239, 230, 128)
    x_start = 70
    y = 100

    # Tag
    draw.text((x_start, y), "REAL BROKER  ·  OREGON", fill=(180, 160, 170), font=font_tag)
    y += 50

    # Title lines
    draw.text((x_start, y), "Every home", fill=cream, font=font_title)
    y += 75
    draw.text((x_start, y), "tells a", fill=cream, font=font_title)
    y += 75
    draw.text((x_start, y), "story.", fill=cream, font=font_title_italic)
    y += 100

    # Subtitle
    draw.text((x_start, y), "Rural & acreage specialist serving Lane, Linn,", fill=(200, 190, 180), font=font_sub)
    y += 30
    draw.text((x_start, y), "Benton, and Douglas counties.", fill=(200, 190, 180), font=font_sub)

    # Bottom bar
    y_bottom = height - 70
    draw.text((x_start, y_bottom), "Larissa Mayfield", fill=cream, font=font_name)
    draw.text((x_start + 260, y_bottom + 8), "LIC. 201231874", fill=(140, 120, 130), font=font_license)
    draw.text((width - 380 - 70, y_bottom + 4), "541.784.7745", fill=(180, 160, 170), font=font_tag)

    img.save(f"{SITE}/images/og-share.jpg", "JPEG", quality=90)
    print("  ✓ images/og-share.jpg")

if __name__ == "__main__":
    print("Generating assets...")
    gen_favicon()
    gen_og_image()
    print("✅ Done.")
