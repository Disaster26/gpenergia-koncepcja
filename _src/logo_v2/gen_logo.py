# -*- coding: utf-8 -*-
"""GP ENERGIA logo v2 (09.11.2026) - built on the client's own design.
ENERGIA: redrawn as clean polygons from the client's file (same letterforms, open R/G/A counters,
slant 22.5 deg, sharp corners instead of soft roundings, tighter spacing).
GP: new sharp letters in the spirit of WAGO (heavy, angular, chamfered corners), same slant.
Line + three dashes under ENERGIA as on the client's file.
No fonts used - every letter is our own path.  python _src/logo_v2/gen_logo.py"""
import math, os, sys
import pathops

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'img', 'logo')
SL = math.tan(math.radians(22.5))
GRAPHITE = '#232826'
G1, G2 = '#0b7a33', '#46b82c'          # GP gradient (client's file: dark green -> light green)
G1D, G2D = '#22a043', '#5fcb3c'        # same on dark backgrounds
H = 180                                 # ENERGIA cap height

# ---------------------------------------------------------------- ENERGIA (upright, y up, x from 0)
def E():
    return [(0, 0), (186, 0), (186, 46), (72, 46), (72, 67), (166, 67), (166, 113), (72, 113),
            (72, 134), (186, 134), (186, 180), (0, 180)]
def N():
    return [(0, 0), (72, 0), (72, 92), (150, 0), (210, 0), (210, 180), (138, 180), (138, 88), (60, 180), (0, 180)]
def R():
    c = 18
    return [(0, 0), (70, 0), (70, 64.6), (148, 0), (216, 0),
            (150, 58), (198 - c, 58), (198, 58 + c), (198, 180 - c), (198 - c, 180), (0, 180)]
R_COUNTER = [(70, 104), (128, 104), (128, 134), (70, 134)]
def G():
    c = 18
    return [(c, 0), (196, 0), (196, 106), (98, 106), (98, 68), (130, 68), (130, 48), (68, 48), (68, 134),
            (196, 134), (196, 180), (c, 180), (0, 180 - c), (0, c)]
def I():
    return [(0, 0), (70, 0), (70, 180), (0, 180)]
def A():
    li = lambda y: 78 + 0.38 * y          # left leg inner edge
    ri = lambda y: 215 - 0.74 * y         # right leg inner edge
    ye = (215 - 78) / (0.38 + 0.74)
    cl = lambda y: 106 + 0.38 * y         # free left end of the crossbar
    return [(0, 0), (78, 0), (li(ye), ye), (ri(66), 66), (cl(66), 66), (cl(26), 26), (ri(26), 26),
            (215, 0), (282, 0), (282 - 0.74 * 180, 180), (0.38 * 180, 180)]

# ---------------------------------------------------------------- GP (new, sharp)
GH = 232                                  # GP cap height (client's file: GP clearly taller than ENERGIA)
def GPg(cut=False):
    c, st, bar = 32, 90, 58
    W = 252
    return [(c, 0), (W, 0), (W, 138), (128, 138), (128, 90), (W - st + 4, 90), (W - st + 4, bar),
            (st, bar), (st, GH - bar), (W, GH - bar), (W, GH), (c, GH), (0, GH - c), (0, c)]
def GPp():
    c, st, bar = 32, 90, 58
    W = 236
    return [(0, 0), (st, 0), (st, 82), (W - c, 82), (W, 82 + c), (W, GH - c), (W - c, GH), (0, GH)]
def GPp_counter():
    st, bar = 90, 58
    return [(st, 82 + 52), (236 - 88, 82 + 52), (236 - 88, GH - bar), (st, GH - bar)]

# ---------------------------------------------------------------- helpers
def path_of(polys, holes=()):
    p = pathops.Path()
    for poly in polys:
        pen = p.getPen(); pen.moveTo(poly[0])
        for pt in poly[1:]: pen.lineTo(pt)
        pen.closePath()
    out = pathops.op(p, pathops.Path(), pathops.PathOp.UNION)
    for h in holes:
        q = pathops.Path(); pen = q.getPen(); pen.moveTo(h[0])
        for pt in h[1:]: pen.lineTo(pt)
        pen.closePath()
        out = pathops.op(out, q, pathops.PathOp.DIFFERENCE)
    return out

def shift(poly, dx, dy=0): return [(x + dx, y + dy) for x, y in poly]

def raster_profile(poly, ymax):
    """left/right ink x per integer row (upright coords) for optical spacing."""
    rows = {}
    n = len(poly)
    for y in range(0, int(ymax) + 1, 2):
        xs = []
        for i in range(n):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
            if (y1 <= y < y2) or (y2 <= y < y1):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
        if xs: rows[y] = (min(xs), max(xs))
    return rows

def place(letters, gap):
    """letters: list of polys (x from 0). returns shifted list with min horizontal gap 'gap' at every row."""
    out = []; prev = None
    for poly in letters:
        if prev is None:
            out.append(poly); prev = raster_profile(poly, 240); continue
        prof = raster_profile(poly, 240)
        need = max(prev[y][1] - prof[y][0] + gap for y in prof if y in prev)
        moved = shift(poly, need); out.append(moved)
        prof2 = {y: (a + need, b + need) for y, (a, b) in prof.items()}
        # keep the union profile (rightmost ink so far)
        merged = dict(prev)
        for y, v in prof2.items():
            merged[y] = (min(merged[y][0], v[0]), max(merged[y][1], v[1])) if y in merged else v
        prev = merged
    return out

def skew(path_d_polys):
    return [[(x + y * SL, -y) for x, y in poly] for poly in path_d_polys]

def to_d(path):
    """pathops path (upright) -> skewed svg d with y down."""
    d = []
    for verb, pts in path:
        if verb == pathops.PathVerb.MOVE:
            x, y = pts[0]; d.append(f'M{x + y * SL:.1f} {-y:.1f}')
        elif verb == pathops.PathVerb.LINE:
            x, y = pts[0]; d.append(f'L{x + y * SL:.1f} {-y:.1f}')
        elif verb == pathops.PathVerb.CLOSE:
            d.append('Z')
    return ''.join(d).replace('.0 ', ' ').replace('.0L', 'L').replace('.0Z', 'Z').replace('.0M', 'M')

def bounds_of(path):
    xs, ys = [], []
    for verb, pts in path:
        for x, y in pts:
            xs.append(x + y * SL); ys.append(-y)
    return min(xs), min(ys), max(xs), max(ys)

# ---------------------------------------------------------------- build
def build(variant='a'):
    gp_gap, en_gap, gp_en_gap = 14, 7, 20
    g = GPg(); p = GPp()
    gpl = place([g, p], gp_gap)
    ppath = path_of([gpl[1]], holes=[shift(GPp_counter(), gpl[1][0][0])])
    gpath = path_of([gpl[0]])
    if variant == 'b':
        # speed cut from the client's file ("//" marks): one diagonal slit through G and P
        x0 = 0
        slit = [(150, -10), (166, -10), (300, 250), (284, 250)]
        slit2 = [(316, -10), (332, -10), (466, 250), (450, 250)]
        for s in (slit, slit2):
            sp = path_of([s])
            gpath = pathops.op(gpath, sp, pathops.PathOp.DIFFERENCE)
            ppath = pathops.op(ppath, sp, pathops.PathOp.DIFFERENCE)
    gp_union = pathops.op(gpath, ppath, pathops.PathOp.UNION)
    gp_prof = {}
    for poly in gpl:
        for y, v in raster_profile(poly, 240).items():
            gp_prof[y] = (min(gp_prof[y][0], v[0]), max(gp_prof[y][1], v[1])) if y in gp_prof else v
    letters = place([E(), N(), E(), R(), G(), I(), A()], en_gap)
    # move ENERGIA so its first letter sits gp_en_gap right of GP at the closest row
    e_prof = raster_profile(letters[0], 240)
    dx = max(gp_prof[y][1] - e_prof[y][0] + gp_en_gap for y in e_prof if y in gp_prof)
    letters = [shift(l, dx) for l in letters]
    r = letters[3]
    en_path = path_of(letters, holes=[shift(R_COUNTER, r[0][0])])
    a_right = letters[-1][8][0]           # A right foot
    return gp_union, gpath, ppath, en_path, letters, a_right

def svg_logo(kind='jasne', variant='a'):
    gp, gpath, ppath, en, letters, a_right = build(variant)
    dark = kind == 'ciemne'
    x0, y0, x1, y1 = bounds_of(gp)
    ex0, ey0, ex1, ey1 = bounds_of(en)
    # line + three dashes under ENERGIA (client's file): line from below P to before the dashes
    ly0, ly1 = 18, 38                     # below baseline (svg y down)
    dash_w, dash_gap, sh = 46, 22, 18
    d_end = ex1 - 4                        # last dash ends at the A
    dashes = []
    for i in range(3):
        r = d_end - i * (dash_w + dash_gap)
        dashes.insert(0, (r - dash_w, r))
    line_end = dashes[0][0] - 30
    line_start = x0 + 380
    vb_x0, vb_y0 = min(x0, ex0) - 2, min(y0, ey0) - 2
    vb_x1, vb_y1 = max(ex1, d_end + sh) + 2, ly1 + 2
    W, Hh = vb_x1 - vb_x0, vb_y1 - vb_y0
    g1, g2 = (G1D, G2D) if dark else (G1, G2)
    en_fill = '#ffffff' if dark else GRAPHITE
    line_c = '#ffffff' if dark else GRAPHITE
    gid = f'gp{kind[0]}{variant}'
    dsh = ''.join(f'<path d="M{a + sh:.1f} {ly0}H{b + sh:.1f}L{b:.1f} {ly1}H{a:.1f}Z"/>' for a, b in dashes)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_x0:.1f} {vb_y0:.1f} {W:.1f} {Hh:.1f}" '
           f'width="{W:.0f}" height="{Hh:.0f}" role="img" aria-label="GP ENERGIA"><title>GP ENERGIA</title>'
           f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0:.0f}" y1="0" x2="{x1:.0f}" y2="0">'
           f'<stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient>'
           f'<linearGradient id="{gid}l" gradientUnits="userSpaceOnUse" x1="{line_start:.0f}" y1="0" x2="{line_end:.0f}" y2="0">'
           f'<stop offset="0" stop-color="{line_c}" stop-opacity="0"/><stop offset=".55" stop-color="{line_c}" stop-opacity=".55"/>'
           f'<stop offset="1" stop-color="{line_c}"/></linearGradient></defs>'
           f'<path fill="url(#{gid})" d="{to_d(gp)}"/>'
           f'<path fill="{en_fill}" d="{to_d(en)}"/>'
           f'<path fill="url(#{gid}l)" d="M{line_start:.1f} {ly0}H{line_end + sh:.1f}L{line_end:.1f} {ly1}H{line_start:.1f}Z"/>'
           f'<g fill="url(#{gid})">{dsh}</g></svg>')
    return svg

def svg_mark(kind='jasne', variant='a', pad=0.0, bg=None, size=None):
    gp, *_ = build(variant)
    x0, y0, x1, y1 = bounds_of(gp)
    w, h = x1 - x0, y1 - y0
    s = max(w, h) * (1 + 2 * pad)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    vb = (cx - s / 2, cy - s / 2, s, s) if bg else (x0 - 2, y0 - 2, w + 4, h + 4)
    dark = kind == 'ciemne'
    g1, g2 = (G1D, G2D) if dark else (G1, G2)
    gid = f'm{kind[0]}{variant}{"b" if bg else ""}'
    rect = f'<rect x="{vb[0]:.1f}" y="{vb[1]:.1f}" width="{vb[2]:.1f}" height="{vb[3]:.1f}" rx="{vb[2] * .18:.1f}" fill="{bg}"/>' if bg else ''
    wh = f' width="{size}" height="{size}"' if size else f' width="{vb[2]:.0f}" height="{vb[3]:.0f}"'
    fill = f'url(#{gid})'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]:.1f} {vb[1]:.1f} {vb[2]:.1f} {vb[3]:.1f}"{wh} role="img" aria-label="GP ENERGIA">'
            f'<title>GP ENERGIA</title><defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0:.0f}" y1="0" x2="{x1:.0f}" y2="0">'
            f'<stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient></defs>'
            f'{rect}<path fill="{fill}" d="{to_d(gp)}"/></svg>')

def svg_favicon(size=100):
    gp, *_ = build('a')
    x0, y0, x1, y1 = bounds_of(gp)
    w, h = x1 - x0, y1 - y0
    s = w * 1.2
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    vb = (cx - s / 2, cy - s / 2, s, s)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]:.1f} {vb[1]:.1f} {s:.1f} {s:.1f}" width="{size}" height="{size}">'
            f'<title>GP ENERGIA</title><defs><linearGradient id="fv" gradientUnits="userSpaceOnUse" x1="{vb[0]:.0f}" y1="0" x2="{vb[0] + s:.0f}" y2="0">'
            f'<stop offset="0" stop-color="{G1}"/><stop offset="1" stop-color="#2f9f35"/></linearGradient></defs>'
            f'<rect x="{vb[0]:.1f}" y="{vb[1]:.1f}" width="{s:.1f}" height="{s:.1f}" rx="{s * .18:.1f}" fill="url(#fv)"/>'
            f'<path fill="#ffffff" d="{to_d(gp)}"/></svg>')

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    w = lambda name, s: open(os.path.join(ROOT, name), 'w', encoding='utf-8').write(s)
    w('img/logo/gpenergia-jasne.svg', svg_logo('jasne'))
    w('img/logo/gpenergia-ciemne.svg', svg_logo('ciemne'))
    w('img/logo/znak-gp.svg', svg_mark('jasne'))
    w('img/logo/znak-gp-ciemne.svg', svg_mark('ciemne'))
    w('img/logo-gpenergia.svg', svg_logo('jasne'))
    w('img/logo-gpenergia-white.svg', svg_logo('ciemne'))
    w('img/logo-mark.svg', svg_mark('jasne'))
    w('img/favicon.svg', svg_favicon())
    print('ok')
