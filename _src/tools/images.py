"""Responsive images for the GP ENERGIA site (AVIF + WebP srcset).
Packshots (white background) are auto-cropped to the product, padded to a fixed
aspect ratio and tinted so that white becomes the site's panel colour.
Brand logos are converted to single-colour graphite PNG/WebP on transparency.
Run: python _src/tools/images.py   (from repo root or anywhere)"""
from pathlib import Path
from PIL import Image, ImageChops, ImageOps
import json

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "_src"
OUT = ROOT / "img" / "p"
OUT.mkdir(parents=True, exist_ok=True)
PANEL = (243, 244, 242)  # --panel

PACKSHOTS = {
    # key: (source file, aspect w/h, padding fraction, widths)
    "cabinet": ("1_SWITCHBOARDS_CABINETS__ENDCLOSURES_AdobeStock_919539470.jpeg", 1.25, 0.10, [480, 720, 960, 1280]),
    "breakers": ("2_LOW_VOLTAGE_EQUIPMENT__SYSTEMS_AdobeStock_277174967.jpeg", 4/3, 0.12, [400, 640, 960]),
    "gauges": ("3_ELECTRICAL_INSTALLATION_EQUIPMENT_AdobeStock_111924937.jpeg", 4/3, 0.0, [400, 640, 960]),
    "sprinklers": ("4_FIRE-PROTECTION-SYSTEMS_AdobeStock_786927686.jpeg", 4/3, 0.04, [400, 640, 960]),
    "lamps": ("5_LIGHTING_AdobeStock_13179320.jpeg", 4/3, 0.12, [400, 640, 960]),
    "marking": ("6_ACCESSORIES_from_Phoenix_Contact.jpg", 4/3, 0.10, [400, 640]),
}
PHOTOS = {
    "export": ("header-home.webp", None, [480, 800, 1200, 1600]),
}

def bbox_nonwhite(im, thr=242):
    g = im.convert("L")
    mask = g.point(lambda v: 255 if v < thr else 0)
    return mask.getbbox() or (0, 0, im.width, im.height)

def pad_to_aspect(im, box, aspect, pad):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    w2, h2 = w * (1 + 2 * pad), h * (1 + 2 * pad)
    if w2 / h2 < aspect:
        w2 = h2 * aspect
    else:
        h2 = w2 / aspect
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    canvas = Image.new("RGB", (int(w2), int(h2)), (255, 255, 255))
    canvas.paste(im, (int(w2 / 2 - cx), int(h2 / 2 - cy)))
    return canvas

def tint(im):
    layer = Image.new("RGB", im.size, PANEL)
    return ImageChops.multiply(im, layer)

def save_set(im, key, widths, q_avif=52, q_webp=76):
    out = []
    for w in widths:
        if w > im.width * 1.02:
            continue
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(OUT / f"{key}-{w}.avif", quality=q_avif, speed=4)
        r.save(OUT / f"{key}-{w}.webp", quality=q_webp, method=6)
        out.append(w)
    if not out:
        w = im.width
        im.save(OUT / f"{key}-{w}.avif", quality=q_avif); im.save(OUT / f"{key}-{w}.webp", quality=q_webp, method=6); out=[w]
    return out

manifest = {}
for key, (fn, aspect, pad, widths) in PACKSHOTS.items():
    im = Image.open(SRC / fn).convert("RGB")
    if pad > 0:
        im = pad_to_aspect(im, bbox_nonwhite(im), aspect, pad)
    else:
        im = ImageOps.fit(im, (im.width, int(im.width / aspect)))
    im = tint(im)
    done = save_set(im, key, widths)
    manifest[key] = {"w": done, "ratio": round(im.height / im.width, 4)}
for key, (fn, aspect, widths) in PHOTOS.items():
    im = Image.open(SRC / fn).convert("RGB")
    done = save_set(im, key, widths)
    manifest[key] = {"w": done, "ratio": round(im.height / im.width, 4)}

# brand logos -> graphite on transparency
LOGO_OUT = ROOT / "img" / "brands"; LOGO_OUT.mkdir(exist_ok=True)
INK = (37, 42, 41)
logos = {}
for f in sorted((SRC / "logos").glob("*")):
    if f.suffix.lower() not in (".png", ".jpg", ".jpeg") or f.name[0] in "_":
        continue
    if f.stem.startswith(("akcesoria", "aparatura", "logistyka", "mierniki", "ppoz", "sygnalizacja", "szafa", "favicon")):
        continue
    im = Image.open(f).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    flat = Image.alpha_composite(bg, im).convert("L")
    a_orig = im.split()[3]
    # darkness -> opacity, boosted so mid-tones (coloured logos) become solid
    dark = flat.point(lambda v: max(0, min(255, int((255 - v) * 1.9))))
    alpha = ImageChops.multiply(dark, a_orig)
    box = alpha.point(lambda v: 255 if v > 18 else 0).getbbox()
    mono = Image.new("RGBA", im.size, INK + (0,))
    mono.putalpha(alpha)
    if box:
        mono = mono.crop(box)
    h = 96
    mono = mono.resize((max(1, round(mono.width * h / mono.height)), h), Image.LANCZOS)
    slug = f.stem.split("-768")[0].split("_Transparent")[0].split(".1")[0].split("-1")[0].lower().replace("_", "-")
    mono.save(LOGO_OUT / f"{slug}.webp", lossless=False, quality=88, method=6)
    mono.save(LOGO_OUT / f"{slug}.png", optimize=True)
    logos[slug] = {"w": mono.width, "h": mono.height}
manifest["_logos"] = logos
(SRC / "tools" / "images.json").write_text(json.dumps(manifest, indent=1))
print(json.dumps(manifest, indent=1))
