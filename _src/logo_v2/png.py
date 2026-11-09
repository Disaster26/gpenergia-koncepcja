# -*- coding: utf-8 -*-
"""PNG / ICO / og-image from the v2 SVG files (headless Chromium).  python _src/logo_v2/png.py"""
import os, io
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
EXE = os.path.expanduser(r'~\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe')

def render(pg, svg, w, h, bg='transparent', pad=0, inner=None):
    data = (ROOT / svg).read_text(encoding='utf-8')
    iw = inner or (w - 2 * pad)
    html = (f'<html><body style="margin:0;background:{bg};width:{w}px;height:{h}px;display:grid;place-items:center">'
            f'<div style="width:{iw}px">{data.replace("<svg ", "<svg style=\"width:100%;height:auto;display:block\" ", 1)}</div></body></html>')
    pg.set_viewport_size({'width': w, 'height': h})
    pg.set_content(html); pg.wait_for_timeout(100)
    return Image.open(io.BytesIO(pg.screenshot(omit_background=(bg == 'transparent'))))

def trim(im):
    bb = im.getbbox(); return im.crop(bb) if bb else im

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)
    pg = b.new_page(accept_downloads=False)
    L = ROOT / 'img' / 'logo'
    for k in ('jasne', 'ciemne'):
        im = trim(render(pg, f'img/logo/gpenergia-{k}.svg', 2100, 400, inner=2048))
        im.save(L / f'gpenergia-{k}.png', optimize=True)
    trim(render(pg, 'img/logo/znak-gp.svg', 1100, 700, inner=1024)).save(L / 'znak-gp.png', optimize=True)
    # favicons
    fav = render(pg, 'img/favicon.svg', 512, 512, inner=512)
    for s in (16, 32, 48):
        fav.resize((s, s), Image.LANCZOS).save(ROOT / 'img' / f'favicon-{s}.png')
    fav.save(ROOT / 'img' / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
    fav.resize((192, 192), Image.LANCZOS).save(ROOT / 'img' / 'android-chrome-192.png')
    fav.save(ROOT / 'img' / 'android-chrome-512.png')
    # apple touch: white GP on green, no transparency, iOS rounds itself
    ap = render(pg, 'img/favicon.svg', 180, 180, bg='#0f7c34', inner=180).convert('RGB')
    ap.save(ROOT / 'img' / 'apple-touch-icon.png')
    # og image 1200x630: logo on white, green band at the bottom
    og = render(pg, 'img/logo/gpenergia-jasne.svg', 1200, 520, bg='#ffffff', inner=860).convert('RGB')
    canvas = Image.new('RGB', (1200, 630), '#ffffff'); canvas.paste(og, (0, 0))
    band = Image.new('RGB', (1200, 110), '#0f7c34'); canvas.paste(band, (0, 520))
    canvas.save(ROOT / 'img' / 'og-image.png', optimize=True)
    # presentation board for the client
    html = (ROOT / 'wizualizacja' / 'logo.html').as_uri()
    b.close()
print('ok')
