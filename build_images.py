#!/usr/bin/env python3
"""
Generate responsive WebP derivatives for every photo on the site.

Why: a listing page was shipping 46.6 MB of images. Gallery tiles render at
~318x212 but were downloading 2048px JPEGs — roughly 40x more pixels than any
visitor sees. This produces narrow WebP variants and a manifest that
generate.py uses to emit <picture> with srcset, so a phone fetches a 400px
file instead of a 2048px one.

Idempotent: a derivative is only rebuilt when it is missing or older than its
source. Safe to run on every build.

Outputs:
  images/<path>/<name>-400.webp, -800.webp, -1600.webp   (skipping upscales)
  images/derivatives.json   { "images/...jpg": {"w":..,"h":..,"widths":[..]} }
"""
import json
import os
from concurrent.futures import ProcessPoolExecutor

from PIL import Image

SITE = os.path.dirname(os.path.abspath(__file__))
IMG_ROOT = os.path.join(SITE, "images")
WIDTHS = (400, 800, 1600)
QUALITY = 80
MANIFEST = os.path.join(IMG_ROOT, "derivatives.json")


def sources():
    for root, _dirs, files in os.walk(IMG_ROOT):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg")) and "-400.webp" not in f:
                yield os.path.join(root, f)


def build_one(src):
    """Return (relpath, {w,h,widths}) for one source image."""
    rel = os.path.relpath(src, SITE)
    try:
        with Image.open(src) as im:
            im = im.convert("RGB")
            ow, oh = im.size
            made = []
            for w in WIDTHS:
                if w >= ow:           # never upscale — it only wastes bytes
                    continue
                out = f"{os.path.splitext(src)[0]}-{w}.webp"
                made.append(w)
                if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src):
                    continue
                h = round(oh * w / ow)
                im.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=QUALITY, method=4)
            # Always give the largest tier a WebP too, so even full-size views
            # avoid the JPEG. Capped at the original's own width.
            top = min(2048, ow)
            if top not in made:
                out = f"{os.path.splitext(src)[0]}-{top}.webp"
                made.append(top)
                if not (os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src)):
                    h = round(oh * top / ow)
                    im.resize((top, h), Image.LANCZOS).save(out, "WEBP", quality=QUALITY, method=4)
            return rel, {"w": ow, "h": oh, "widths": sorted(made)}
    except Exception as e:                                    # corrupt/unreadable
        print(f"  ! skipped {rel}: {e}")
        return rel, None


def main():
    srcs = sorted(sources())
    print(f"Building WebP derivatives for {len(srcs)} source images...")
    manifest = {}
    with ProcessPoolExecutor() as pool:
        for rel, data in pool.map(build_one, srcs):
            if data:
                manifest[rel] = data
    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=0, sort_keys=True)

    webps = sum(len(v["widths"]) for v in manifest.values())
    jpg_bytes = sum(os.path.getsize(os.path.join(SITE, k)) for k in manifest)
    webp_bytes = sum(
        os.path.getsize(f"{os.path.splitext(os.path.join(SITE, k))[0]}-{w}.webp")
        for k, v in manifest.items() for w in v["widths"]
        if os.path.exists(f"{os.path.splitext(os.path.join(SITE, k))[0]}-{w}.webp"))
    print(f"  ✓ {len(manifest)} images -> {webps} webp derivatives")
    print(f"  ✓ sources {jpg_bytes/1_000_000:.0f} MB | all derivatives {webp_bytes/1_000_000:.0f} MB")
    print(f"  ✓ manifest: images/derivatives.json")


if __name__ == "__main__":
    main()
