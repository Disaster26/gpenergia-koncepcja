# -*- coding: utf-8 -*-
"""Static generator for gpenergia.com.pl (preview on GitHub Pages).
python _src/build.py            -> preview build (noindex, robots Disallow)
python _src/build.py --prod     -> production build (indexable) into _dist/
Content lives in content.py and (when present) _src/seo_0511/ (META.json, BLOG/, JSONLD/)."""
import json, re, sys, shutil, html, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from content import *  # noqa
import blog as BLOGMOD

PROD = "--prod" in sys.argv
CANON = "https://gpenergia.com.pl"          # the ONE canonical origin
PREVIEW_BASE = "/gpenergia-koncepcja/"      # absolute base only used by 404.html on GitHub Pages
FORM_ENDPOINT = ""                          # empty = preview mock; set to WP endpoint on launch
ROOT = Path(__file__).resolve().parents[1]
OUT = (ROOT / "_dist") if PROD else ROOT
SRC = ROOT / "_src"
MAN = json.loads((SRC / "tools" / "images.json").read_text())
SEO = SRC / "seo_0511"
VER = datetime.datetime.now().strftime("%Y%m%d%H%M")

def esc(s): return html.escape(str(s), quote=True)

# ---------------------------------------------------------------- SEO agent overrides
def load_seo_meta():
    f = SEO / "META.json"
    if not f.exists():
        return False
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        print("META.json unreadable:", e); return False
    n = 0
    pages = data.get("pages")
    if isinstance(pages, list):
        data = {pg.get("id"): {"en": pg.get("en", {}), "pl": pg.get("pl", {})} for pg in pages if pg.get("id")}
    elif "en" in data and isinstance(data["en"], dict) and "home" in data["en"]:
        data = {p: {l: data[l].get(p, {}) for l in ("en", "pl")} for p in data["en"]}
    for page, langs in data.items():
        if page not in META or not isinstance(langs, dict):
            continue
        for l in ("en", "pl"):
            d = langs.get(l) or {}
            for k_src, k_dst in (("title", "title"), ("description", "desc"), ("h1", "h1")):
                v = d.get(k_src)
                if isinstance(v, str) and v.strip():
                    META[page][l][k_dst] = v.strip().replace("—", "-").replace("–", "-").replace("sales@gpenergia.com.pl", "info@gpenergia.com.pl"); n += 1
    print("SEO META applied:", n, "fields")
    return True

SEO_META = load_seo_meta()

def load_seo_faq():
    f = SEO / "TEXTS.md"
    out = {}
    if not f.exists():
        return out
    t = f.read_text(encoding="utf-8")
    for m in re.finditer(r"^###\s+FAQ\s+\(faq:(\w+):(en|pl)\)\s*\n(.*?)(?=^#{1,3}\s|^---|\Z)", t, re.M | re.S):
        page, lang, block = m.group(1), m.group(2), m.group(3)
        items = []
        for q, a in re.findall(r"\*\*Q:\s*(.+?)\*\*\s*\n+A:\s*(.+?)(?=\n\s*\n|\Z)", block, re.S):
            if "CONFIRM" in q + a:
                continue
            a = " ".join(a.split()).replace("sales@gpenergia.com.pl", EMAIL)
            a = re.sub(r"\s*\[[A-Z0-9, ]+\]", "", a)
            items.append((q.strip(), a))
        if items:
            out[(page, lang)] = items
    print("SEO FAQ blocks:", list(out))
    return out

SEO_FAQ = load_seo_faq()

# ---------------------------------------------------------------- paths / links
class Ctx: path = ""; lang = "en"; pid = "home"; alt = {}
C = Ctx()

def rel(to):
    """relative link from current page dir to site path `to` ('' = root)."""
    depth = C.path.count("/")
    pre = "../" * depth
    return (pre + to) or "./"

def P(pid, lang=None):
    lang = lang or C.lang
    return PATHS[pid][0 if lang == "en" else 1]

def asset(p): return rel(p)

def tr(): return T[C.lang]

def logo_file(white=False):
    new = ROOT / "img" / ("logo-gpenergia-white.svg" if white else "logo-gpenergia.svg")
    if new.exists():
        return "img/" + new.name
    return "img/logo/gpenergia-1-ciemne.svg" if white else "img/logo/gpenergia-1-jasne.svg"

def svg_size(p):
    try:
        t = (ROOT / p).read_text(encoding="utf-8")
        m = re.search(r'viewBox="([\d.\-]+)[ ,]+([\d.\-]+)[ ,]+([\d.]+)[ ,]+([\d.]+)"', t)
        if m:
            return float(m.group(3)), float(m.group(4))
    except Exception:
        pass
    return 761.2, 100

# ---------------------------------------------------------------- images
def pic(key, alt, sizes, cls="", eager=False, high=False):
    m = MAN[key]; ws = m["w"]; r = m["ratio"]
    big = ws[-1]
    av = ", ".join(f"{asset(f'img/p/{key}-{w}.avif')} {w}w" for w in ws)
    wb = ", ".join(f"{asset(f'img/p/{key}-{w}.webp')} {w}w" for w in ws)
    fallback = asset(f"img/p/{key}-{ws[min(1, len(ws)-1)]}.webp")
    load = 'fetchpriority="high"' if high else ('' if eager else 'loading="lazy"')
    return (f'<picture{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>'
            f'<source type="image/avif" srcset="{av}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{wb}" sizes="{sizes}">'
            f'<img src="{fallback}" width="{big}" height="{round(big*r)}" alt="{esc(alt)}" {load} decoding="async"></picture>')

def brand_img(slug, name, cls=""):
    m = MAN["_logos"][slug]
    if m["w"] / m["h"] < 2.3:
        cls = (cls + " sq").strip()
    return f'<img src="{asset("img/brands/" + slug + ".webp")}" width="{m["w"]}" height="{m["h"]}" alt="{esc(name)}" loading="lazy" decoding="async"{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>'

# ---------------------------------------------------------------- icons (inline, aria-hidden)
I_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm1.6 2 7.4 5.6L19.4 7H4.6ZM20 8.6l-7.4 5.6a1 1 0 0 1-1.2 0L4 8.6V17h16V8.6Z"/></svg>'
I_ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M13.3 5.3a1 1 0 0 1 1.4 0l6 6a1 1 0 0 1 0 1.4l-6 6a1 1 0 0 1-1.4-1.4l4.3-4.3H4a1 1 0 1 1 0-2h13.6l-4.3-4.3a1 1 0 0 1 0-1.4Z"/></svg>'
I_PIN = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2a7 7 0 0 1 7 7c0 5-6 12-6.3 12.3a1 1 0 0 1-1.4 0C11 21 5 14 5 9a7 7 0 0 1 7-7Zm0 4.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5Z"/></svg>'
I_FILE = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 2h8l6 6v13a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1Zm7 1.5V9h5.5L13 3.5ZM8 13h8v1.6H8V13Zm0 3.4h8V18H8v-1.6Z"/></svg>'

WYLINKA = ('<a class="wylinka-badge" href="https://wylinka.pl/?utm_source=gpenergia.com.pl&amp;utm_medium=stopka&amp;utm_campaign=wykonanie" rel="noopener" title="Strona wykonana przez Wylinka">'
           '<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false" fill="currentColor"><path d="M9.8 22.8l-1.2-7.9 2.2-3.7 15.5 4.6-.5 1.5-7.2 5.5 4.7 15.6 5-15.6 7 0 4.1 12.7-4.2-.9-2.6 1.8-.8-2.2-5.3 15.6-4.3 0 .4 .2-2.1 2.8-1.3-1.1 1.1-1.4-3.1 .2-.1-1.7 2.2-.1-5.7-16.5-4.8 .6-.8 3.1 0 .5-.3 .5 .8 2.2-1.6 .5-.4-1.3-.8 1.6-1.5-.8 .8-1.6-1.4 .6-.6-1.6 2.3-.8 .2-.4 1.3-4.8 5.9-.8-2.4-6.9zM15.2 13.7l-.1-.4-.4 .8-.1 .8 .1 1 .1 .4 .3 .7 .3-.9 .1-.7 0-.8z"/><path class="wy-pod" d="M37.1 49.8l-4.5-13.3 2.6-1.8 4.2 .9 .9 2.8 3-9.7 0-.5 .1-.8 3.2-8.4 .5-1 .6-1 .9-1.1 1.3-1 1.1-.7 1.4-.5 1.4-.3 .7 0 .9 0 1.2 .3 1.4 .6 .8 .5 .7 .7 .6 .7 .5 .9 .3 .9 .1 .9 0 .8-.2 .9-.5 .9-.5 .6-.7 .5-.7 .3-.1-.1 0-.1 .5-.5 .3-.7 .2-.5 0-.6-.1-.6-.3-.7-.4-.5-.4-.4-.5-.3-.6-.3-.7 0-.7 .1-.6 .1-.5 .4-.5 .5-.3 .5-.2 .7-.1 1.5-1.4 5.1-.8 3.3-.3 .7-.5 .7-6 17.5 1.9 .1-.1 1.7-3.1-.2 1.1 1.4-1.3 1.1-2.1-2.8 .4-.2z"/><path class="wy-old" d="M40.8 50l.4-.2-4.1 0-4.2-12.5 2.5-1.7 4.3 .9 .6 1.9 .6-1.6 0-.3 2.4-7.8 0-.5 .1-.8 3.2-8.4 .4-.8 .6-.9 .9-1.2 .9-.9 1.3-.8 1.4-.6 1.2-.3 1.4-.1 1.3 .1 .6 .2 .8 .3 1.1 .6 .9 .7 .7 .9 .5 .9 .3 .9 .1 1.1-.1 .9-.3 .9-.4 .7-.6 .7-.6 .4-.6 .2-.1-.1 0-.1 .5-.5 .3-.7 .2-.5 0-.5-.1-.6-.2-.6-.3-.5-.4-.5-.5-.3-.6-.3-.7-.1-.6 0-.6 .1-.6 .3-.6 .5-.3 .4-.2 .5-.1 .5-.1 1.5-1.4 5.1-.8 3.3-.3 .7-.5 .7-6 17.5 1.9 .1-.1 1.7-3.1-.2 1.1 1.4-1.3 1.1zM49.6 17.1l.6 1.7-1.5 1.9 .4 .4 1.8-2.1-.7-2.1zM48.1 28.3l.5 1.8-1.7 1.8 .4 .4 1.9-2-.6-2.2zM37.9 41.7l1.7-1.5-.4-.4-1.7 1.4zM42.6 38.7l-1.5 2.8 1.1 2-1.3 2.6 .5 .2 1.5-2.8-1.1-2 1.4-2.5z"/></svg>'
           '<span>wykonanie: <b>Wylinka</b></span></a>')

SLOGAN = {"en": "Every line of your BOM, answered.", "pl": "Każda pozycja listy z odpowiedzią."}

# ---------------------------------------------------------------- JSON-LD
def org_ld():
    return {
        "@type": "Organization", "@id": CANON + "/#org",
        "name": "GP ENERGIA", "legalName": COMPANY["legal"], "url": CANON + "/",
        "logo": CANON + "/" + ("img/logo-gpenergia.png" if (ROOT / "img/logo-gpenergia.png").exists() else logo_file()),
        "email": EMAIL, "foundingDate": "2009",
        "taxID": COMPANY["nip_raw"], "vatID": "PL" + COMPANY["nip_raw"],
        "identifier": [{"@type": "PropertyValue", "propertyID": "KRS", "value": COMPANY["krs"]},
                       {"@type": "PropertyValue", "propertyID": "REGON", "value": COMPANY["regon"]}],
        "address": {"@type": "PostalAddress", "streetAddress": COMPANY["street"], "postalCode": COMPANY["postcode"],
                    "addressLocality": COMPANY["city"], "addressRegion": "dolnośląskie", "addressCountry": "PL"},
        "location": {"@type": "Place", "name": "GP ENERGIA warehouse",
                     "geo": {"@type": "GeoCoordinates", "latitude": COMPANY["lat"], "longitude": COMPANY["lon"]}},
        "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "email": EMAIL,
                         "availableLanguage": ["English", "Polish", "Russian"]},
        "areaServed": ["Europe", "United States", "Asia", "Middle East", "Africa"],
        "knowsAbout": ["BOM sourcing", "industrial automation components", "electrical components", "obsolete parts sourcing", "export logistics"],
    }

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": CANON + "/" + p} for i, (n, p) in enumerate(items)]}

def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faq]}

# ---------------------------------------------------------------- layout
_CSS = None
def inline_css():
    """whole stylesheet inlined (no render-blocking request); font urls rewritten per page depth"""
    global _CSS
    if _CSS is None:
        css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8") + chr(10) + (SRC / "brand.css").read_text(encoding="utf-8")
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        css = re.sub(r"\s*\n\s*", "", css)
        css = re.sub(r"\s*([{};>])\s*", r"\1", css).replace(";}", "}")
        _CSS = css
    return _CSS.replace("url(fonts/", "url(" + asset("assets/fonts/"))

def head(title, desc, alt_paths, extra_ld, ogimg="cabinet"):
    t = tr()
    en_p, pl_p = alt_paths
    canon = CANON + "/" + C.path
    ld = {"@context": "https://schema.org", "@graph": [org_ld(),
          {"@type": "WebSite", "@id": CANON + "/#web", "url": CANON + "/", "name": "GP ENERGIA",
           "inLanguage": ["en", "pl"], "publisher": {"@id": CANON + "/#org"}},
          {"@type": "WebPage", "@id": canon + "#page", "url": canon, "name": title, "description": desc,
           "inLanguage": C.lang, "isPartOf": {"@id": CANON + "/#web"}}] + extra_ld}
    fav = []
    if (ROOT / "img/favicon.ico").exists():
        fav.append(f'<link rel="icon" href="{asset("img/favicon.ico")}" sizes="32x32">')
    favsvg = "img/favicon-gp.svg" if (ROOT / "img/favicon-gp.svg").exists() else "img/favicon.svg"
    fav.append(f'<link rel="icon" href="{asset(favsvg)}" type="image/svg+xml">')
    if (ROOT / "img/apple-touch-icon.png").exists():
        fav.append(f'<link rel="apple-touch-icon" href="{asset("img/apple-touch-icon.png")}">')
    if (ROOT / "site.webmanifest").exists():
        fav.append(f'<link rel="manifest" href="{asset("site.webmanifest")}">')
    ogw = MAN[ogimg]["w"][-1]
    return f'''<!doctype html>
<html lang="{C.lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{'<meta name="robots" content="index, follow">' if PROD else '<meta name="robots" content="noindex, nofollow">'}
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{CANON}/{en_p}">
<link rel="alternate" hreflang="pl" href="{CANON}/{pl_p}">
<link rel="alternate" hreflang="x-default" href="{CANON}/{en_p}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="GP ENERGIA">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
{('<meta property="og:image" content="' + CANON + '/img/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">') if (ROOT / "img/og-image.png").exists() else ('<meta property="og:image" content="' + CANON + '/img/p/' + ogimg + '-' + str(ogw) + '.webp">')}
<meta property="og:locale" content="{'en_GB' if C.lang == 'en' else 'pl_PL'}">
<meta name="theme-color" content="#232826">
<script>document.documentElement.classList.add('js')</script>
{chr(10).join(fav)}
<link rel="preload" href="{asset('assets/fonts/plex-latin.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{asset('assets/fonts/archivo-latin.woff2')}" as="font" type="font/woff2" crossorigin>
<style>{inline_css()}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
'''

def header():
    t = tr(); L = C.lang
    nav = "".join(
        f'<a href="{rel(P(pid))}"{" aria-current=" + chr(34) + "page" + chr(34) if (C.pid == pid or (pid == "blog" and C.pid == "article")) else ""}>{esc(lbl)}</a>'
        for pid, lbl in t["nav"])
    en_p, pl_p = C.alt
    lang = (f'<a href="{rel(en_p)}" hreflang="en" lang="en"{" aria-current=" + chr(34) + "true" + chr(34) if L == "en" else ""}>EN</a>'
            f'<a href="{rel(pl_p)}" hreflang="pl" lang="pl"{" aria-current=" + chr(34) + "true" + chr(34) if L == "pl" else ""}>PL</a>')
    lw, lh = svg_size(logo_file(True))
    return f'''<body class="p-{C.pid}">
<a class="skip" href="#main">{t["skip"]}</a>
<div class="util">
  <div class="wrap util-in">
    <p>{I_PIN}{esc(t["util_addr"])}</p>
    <p class="util-r"><a href="mailto:{EMAIL}">{I_MAIL}{EMAIL}</a><span class="lang" role="group" aria-label="{t["lang_label"]}">{lang}</span></p>
  </div>
</div>
<header class="top" id="top">
  <div class="wrap top-in">
    <a class="logo" href="{rel(P("home"))}" aria-label="GP ENERGIA - {esc(t["home"])}"><img src="{asset(logo_file(True))}" width="{round(lw)}" height="{round(lh)}" alt="GP ENERGIA"></a>
    <nav class="menu" id="menu" aria-label="{"Main" if L == "en" else "Menu główne"}">
      {nav}
      <div class="menu-extra">
        <a class="menu-mail" href="mailto:{EMAIL}">{I_MAIL}{EMAIL}</a>
        <span class="lang" role="group" aria-label="{t["lang_label"]}">{lang}</span>
      </div>
    </nav>
    <a class="btn btn-top" href="{rel(P("contact"))}#rfq"><span class="l-long">{t["cta"]}</span><span class="l-short">{t["cta_short"]}</span></a>
    <button class="burger" id="burger" type="button" aria-label="{t["menu_open"]}" aria-expanded="false" aria-controls="menu" data-open="{t["menu_open"]}" data-close="{t["menu_close"]}"><span></span><span></span><span></span></button>
  </div>
</header>
'''

def footer():
    t = tr(); L = C.lang
    c1, c2, c3 = t["foot_cols"]
    off = "".join(f'<li><a href="{rel(P("products"))}#{c["id"]}">{esc(c[L]["t"])}</a></li>' for c in CATEGORIES[:4])
    serv = ([("services", "BOM sourcing" if L == "en" else "Wycena list BOM", "#bom"),
             ("services", "Obsolete parts" if L == "en" else "Części wycofane", "#obsolete"),
             ("services", "Logistics and export" if L == "en" else "Logistyka i eksport", "#export")])
    off += "".join(f'<li><a href="{rel(P(p))}{h}">{esc(n)}</a></li>' for p, n, h in serv)
    comp = "".join(f'<li><a href="{rel(P(p))}">{esc(n)}</a></li>' for p, n in t["nav"] if p in ("about", "references", "products", "blog")) + \
        f'<li><a href="{rel(P("privacy"))}">{t["foot_privacy"]}</a></li>'
    en_p, pl_p = C.alt
    other = rel(pl_p if L == "en" else en_p)
    wl, hl = svg_size(logo_file(True))
    return f'''<footer class="foot">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <a class="logo" href="{rel(P("home"))}"><img src="{asset(logo_file(True))}" width="{round(wl)}" height="{round(hl)}" alt="GP ENERGIA" loading="lazy"></a>
      <p class="foot-slogan">{SLOGAN[L]}</p>
      <p>{esc(t["foot_desc"])}</p>
    </div>
    <nav aria-label="{esc(c1)}"><h2>{esc(c1)}</h2><ul>{off}</ul></nav>
    <nav aria-label="{esc(c2)}"><h2>{esc(c2)}</h2><ul>{comp}</ul></nav>
    <div><h2>{esc(c3)}</h2>
      <p><a class="foot-mail" href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>{COMPANY["legal"]}<br>{"Warehouse" if L == "en" else "Magazyn"}: {COMPANY["street"]}<br>{COMPANY["postcode"]} {COMPANY["city"]}, {"Poland" if L == "en" else "Polska"}</p>
      <p><a href="{rel(P("contact"))}#rfq">{t["cta"]}</a></p>
    </div>
  </div>
  <div class="wrap foot-legal">
    <p>{COMPANY["legal"]} · KRS {COMPANY["krs"]} · NIP {COMPANY["nip"]} · REGON {COMPANY["regon"]}</p>
    <p>{esc(t["foot_note"])}</p>
    <p class="foot-last"><span>© 2026 {COMPANY["legal"]}</span><a href="{other}" hreflang="{"pl" if L == "en" else "en"}" lang="{"pl" if L == "en" else "en"}">{t["foot_switch"]}</a><button type="button" class="ck-open" data-ck-open>{CK[L]["link"]}</button>{WYLINKA}</p>
  </div>
</footer>
<div class="mob" id="mob" aria-hidden="true">
  <a class="mob-mail" href="mailto:{EMAIL}" tabindex="-1">{I_MAIL}{t["mob_mail"]}</a>
  <a class="mob-cta" href="{rel(P("contact"))}#rfq" tabindex="-1">{t["mob_cta"]}</a>
</div>
{cookie_banner()}
<script src="{asset('assets/site.js')}?v={VER}" defer></script>
</body>
</html>
'''

CK = {
 "en": {"link": "Cookie settings", "h": "Cookies on this website",
        "p": "We use only the cookies needed for the site to work and, if you agree, Google Maps on the contact page. We do not use analytics or advertising cookies.",
        "all": "Accept all", "nec": "Necessary only", "set": "Settings", "save": "Save choice",
        "c1": "Necessary", "c1d": "Remember your cookie choice. Always on.",
        "c2": "External media", "c2d": "Google Maps on the contact page (Google may set its own cookies).",
        "more": "Privacy policy"},
 "pl": {"link": "Ustawienia cookies", "h": "Pliki cookies na tej stronie",
        "p": "Używamy tylko plików cookies niezbędnych do działania strony, a za Twoją zgodą także Map Google na stronie kontaktu. Nie używamy cookies analitycznych ani reklamowych.",
        "all": "Akceptuję wszystkie", "nec": "Tylko niezbędne", "set": "Ustawienia", "save": "Zapisz wybór",
        "c1": "Niezbędne", "c1d": "Zapamiętanie Twojego wyboru cookies. Zawsze włączone.",
        "c2": "Media zewnętrzne", "c2d": "Mapa Google na stronie kontaktu (Google może zapisać własne cookies).",
        "more": "Polityka prywatności"},
}

def cookie_banner():
    L = C.lang; k = CK[L]
    return f"""<div class="ck" id="ck" role="dialog" aria-modal="false" aria-labelledby="ck-h" hidden>
  <p class="ck-h" id="ck-h">{k["h"]}</p>
  <p class="ck-p">{k["p"]} <a href="{rel(P("privacy"))}#cookies">{k["more"]}</a></p>
  <div class="ck-set" id="ck-set" hidden>
    <label class="ck-row"><input type="checkbox" checked disabled><span><b>{k["c1"]}</b> {k["c1d"]}</span></label>
    <label class="ck-row"><input type="checkbox" id="ck-media"><span><b>{k["c2"]}</b> {k["c2d"]}</span></label>
  </div>
  <div class="ck-act">
    <button type="button" class="btn ck-all" data-ck="all">{k["all"]}</button>
    <button type="button" class="ck-btn" data-ck="nec">{k["nec"]}</button>
    <button type="button" class="ck-btn ck-more" data-ck="set" data-save="{k["save"]}">{k["set"]}</button>
  </div>
</div>"""

def crumbs(items):
    t = tr()
    lis = []
    for i, (n, p) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li aria-current="page">{esc(n)}</li>')
        else:
            lis.append(f'<li><a href="{rel(p)}">{esc(n)}</a></li>')
    return f'<nav class="crumbs" aria-label="{t["breadcrumb"]}"><ol>{"".join(lis)}</ol></nav>'

def page_head(h1, lead, crumb_items, aside=""):
    return f'''<section class="phead">
  <div class="wrap phead-in{" has-aside" if aside else ""}">
    <div class="phead-txt">
      {crumbs(crumb_items)}
      <h1>{esc(h1)}</h1>
      <p class="lead">{lead}</p>
    </div>
    {aside}
  </div>
</section>'''

def write(path, html_text):
    f = OUT / path / "index.html" if (path == "" or path.endswith("/")) else OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html_text, encoding="utf-8")

PAGES_OUT = []  # (pid, en_path, pl_path, lastmod)

def render(pid, lang, body, extra_ld=None, path=None, alt=None, title=None, desc=None, ogimg="cabinet"):
    C.lang = lang; C.pid = pid
    C.alt = alt or PATHS[pid]
    C.path = path if path is not None else P(pid, lang)
    m = META.get(pid, {}).get(lang, {})
    title = title or m["title"]; desc = desc or m["desc"]
    out = head(title, desc, C.alt, extra_ld or [], ogimg) + header() + '<main id="main">\n' + body + '\n</main>\n' + footer()
    out = out.replace("—", "-").replace("–", "-")
    write(C.path, out)

# ---------------------------------------------------------------- shared blocks
def cta_band():
    L = C.lang
    if L == "en":
        h, p, b = SLOGAN["en"], "Send part numbers or attach your BOM file. We reply with prices, lead times and any alternatives, often within 1-6 hours.", "Send your BOM"
    else:
        h, p, b = SLOGAN["pl"], "Wyślij kody produktów albo dołącz plik BOM. Odpowiemy z cenami, terminami dostaw i ewentualnymi zamiennikami, często w ciągu 1-6 godzin.", "Wyślij listę BOM"
    return f'''<section class="ctaband" aria-labelledby="h-cta">
  <div class="wrap ctaband-in">
    <div><h2 id="h-cta">{h}</h2><p>{p}</p></div>
    <div class="ctaband-act"><a class="btn" href="{rel(P("contact"))}#rfq">{b}</a><a class="mail-link" href="mailto:{EMAIL}">{I_MAIL}{EMAIL}</a></div>
  </div>
</section>'''

def bom_table(caption_extra=True):
    L = C.lang
    if L == "en":
        cap, sub, cols = "Sample BOM", "Excerpt from an industrial project. Every line comes back with price, lead time and alternative.", ("No.", "Item", "Manufacturer", "Part number", "Qty", "Quote")
    else:
        cap, sub, cols = "Przykładowy BOM", "Fragment listy z projektu przemysłowego. Każda pozycja wraca z ceną, terminem i zamiennikiem.", ("Lp.", "Pozycja", "Producent", "Kod produktu", "Ilość", "Oferta")
    qt_lbl = "price, lead time, alternative" if L == "en" else "cena, termin, zamiennik"
    rows = "".join(
        f'<tr><td class="n">{i+1}</td><td><b>{esc(r[0] if L=="en" else r[2])}</b><span>{esc(r[1] if L=="en" else r[3])}</span></td><td>{esc(r[4])}</td><td class="pn">{esc(r[5])}</td><td class="q">{r[6]}</td><td class="qt"><span class="dash3" role="img" aria-label="{qt_lbl}"><i></i><i></i><i></i></span></td></tr>'
        for i, r in enumerate(BOM))
    return f'''<figure class="bomsheet">
  <div class="bomsheet-scroll" tabindex="0" role="region" aria-label="{cap}">
  <table>
    <caption><b>{cap}</b> <span>{sub}</span></caption>
    <thead><tr>{"".join(f'<th scope="col"{" class=" + chr(34) + c + chr(34) if c else ""}>{h}</th>' for h, c in zip(cols, ("n", "", "", "", "q", "qt")))}</tr></thead>
    <tbody>{rows}</tbody>
  </table>
  </div>
</figure>'''

def compare_table():
    L = C.lang
    if L == "en":
        h = ("", "Direct from the manufacturer", "Through GP ENERGIA")
        rows = [("Availability", "often 6-12 weeks", "1-5 days from European warehouses"),
                ("Price", "list price or project discount", "market price, often below wholesalers"),
                ("Brands", "one manufacturer only", "many brands and alternatives in one order"),
                ("Handling", "separate contacts and invoices per brand", "one quote, one delivery, simpler invoicing")]
        cap = "Buying direct versus through a project distributor"
    else:
        h = ("", "Zakup u producenta", "Zakup przez GP ENERGIA")
        rows = [("Dostępność", "często 6-12 tygodni", "1-5 dni z magazynów europejskich"),
                ("Cena", "katalogowa lub rabat projektowy", "rynkowa, często niższa niż w hurtowniach"),
                ("Marki", "tylko jednego producenta", "wiele marek i zamienniki w jednym zamówieniu"),
                ("Obsługa", "osobne kontakty i faktury dla każdej marki", "jedna oferta, jedna dostawa, prostsze rozliczenie")]
        cap = "Zakup u producenta a zakup przez dystrybutora projektowego"
    body = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    return f'''<div class="cmp-scroll" tabindex="0" role="region" aria-label="{cap}"><table class="cmp"><caption class="sr">{cap}</caption>
<thead><tr><td></td><th scope="col">{h[1]}</th><th scope="col">{h[2]}</th></tr></thead><tbody>{body}</tbody></table></div>'''

def facts_dl(rows, cls="facts"):
    return f'<dl class="{cls}">' + "".join(f'<div><dt>{esc(a)}</dt><dd>{b}</dd></div>' for a, b in rows) + '</dl>'

def export_rows():
    if C.lang == "en":
        return [("Markets", "Europe, the United States, Asia, the Middle East and Africa"),
                ("Incoterms", "EXW, FCA or DAP, whatever suits your project"),
                ("Shipping", "DHL, FedEx or UPS courier, or pallet freight"),
                ("Consolidation", "multi-source orders combined at our warehouse near Wrocław"),
                ("Languages", "English, Polish, Russian")]
    return [("Kierunki", "Europa, Stany Zjednoczone, Azja, Bliski Wschód i Afryka"),
            ("Incoterms", "EXW, FCA albo DAP, według potrzeb projektu"),
            ("Transport", "kurier DHL, FedEx, UPS albo spedycja paletowa"),
            ("Konsolidacja", "zamówienia z wielu źródeł łączone w naszym magazynie pod Wrocławiem"),
            ("Języki", "polski, angielski, rosyjski")]

def countries():
    if C.lang == "en":
        return "Recent destinations include Germany, France, Spain, Italy, Romania, Turkey, India, Saudi Arabia, Vietnam, the UAE, Qatar, the Philippines and Thailand."
    return "Wysyłamy m.in. do Niemiec, Francji, Hiszpanii, Włoch, Rumunii, Turcji, Indii, Arabii Saudyjskiej, Wietnamu, ZEA, Kataru, na Filipiny i do Tajlandii."

def company_rows():
    L = C.lang
    return [("Company" if L == "en" else "Firma", COMPANY["legal"]),
            ("In business since" if L == "en" else "Działalność od", "2009"),
            ("Warehouse" if L == "en" else "Magazyn", f'{COMPANY["street"]}, {COMPANY["postcode"]} {COMPANY["city"]}'),
            ("E-mail", f'<a href="mailto:{EMAIL}">{EMAIL}</a>'),
            ("KRS", COMPANY["krs"]), ("NIP" if L == "pl" else "NIP (tax ID)", COMPANY["nip"]),
            ("REGON", COMPANY["regon"]),
            ("Share capital" if L == "en" else "Kapitał zakładowy", COMPANY["capital_en"] if L == "en" else COMPANY["capital_pl"])]

def faq_block(faq, hid="h-faq"):
    items = "".join(f'<details><summary><h3>{esc(q)}</h3></summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faq)
    return f'<div class="faq">{items}</div>'

def default_faq(lang):
    if lang == "en":
        return [
            ("In what format can I send my BOM?", "Send an xlsx, xls, csv or pdf file through the form on the contact page or by e-mail to info@gpenergia.com.pl. A list of part numbers with quantities pasted into the message works too."),
            ("How quickly do you reply?", "We often send a quote within 1-6 hours. Long lists with many brands or parts that need an alternative can take longer, and we tell you when to expect the answer."),
            ("What order size do you handle?", "From orders of about EUR 100 up to BOMs worth several hundred thousand euros."),
            ("Can you find discontinued or hard-to-find parts?", "Yes. We check availability with distributors, manufacturers and independent suppliers across Europe, and where the original is no longer available we propose a technically compliant alternative for your approval."),
            ("Do you ship outside the EU?", "Yes. We deliver across Europe, to the United States, Asia, the Middle East and Africa on EXW, FCA or DAP terms, by DHL, FedEx, UPS or pallet freight."),
            ("Are the products genuine?", "We supply genuine products from established manufacturers only, such as Siemens, Schneider Electric, ABB, Phoenix Contact and Rittal."),
        ]
    return [
        ("W jakim formacie wysłać listę BOM?", "Plik xlsx, xls, csv albo pdf przez formularz na stronie kontaktu lub e-mailem na info@gpenergia.com.pl. Wystarczy też lista kodów produktów z ilościami wklejona w treść wiadomości."),
        ("Jak szybko odpowiadacie?", "Ofertę często wysyłamy w ciągu 1-6 godzin. Długie listy z wieloma markami albo pozycjami wymagającymi zamiennika mogą potrwać dłużej i wtedy podajemy, kiedy spodziewać się odpowiedzi."),
        ("Jakiej wielkości zamówienia obsługujecie?", "Od zamówień za około 100 EUR po listy BOM o wartości kilkuset tysięcy euro."),
        ("Czy znajdziecie części wycofane z produkcji?", "Tak. Sprawdzamy dostępność u dystrybutorów, producentów i niezależnych dostawców w całej Europie, a gdy oryginał nie jest już dostępny, proponujemy zgodny technicznie zamiennik do akceptacji."),
        ("Czy wysyłacie poza Unię Europejską?", "Tak. Dostarczamy w Europie, do Stanów Zjednoczonych, Azji, na Bliski Wschód i do Afryki na warunkach EXW, FCA albo DAP, kurierem DHL, FedEx, UPS lub spedycją paletową."),
        ("Czy produkty są oryginalne?", "Dostarczamy wyłącznie oryginalne produkty uznanych producentów, takich jak Siemens, Schneider Electric, ABB, Phoenix Contact i Rittal."),
    ]

FAQ = {"en": default_faq("en"), "pl": default_faq("pl")}

# ---------------------------------------------------------------- pages
def page_home(L):
    m = META["home"][L]
    if L == "en":
        loc = "B2B supplier of industrial automation and electrical components · Długołęka near Wrocław, Poland"
        lead = "PLCs, HMIs, sensors, contactors, power supplies and switchgear from the original manufacturers. Send the whole bill of materials and get one quote with prices, lead times and alternatives, shipped from European stock."
        cta, strip_t = "Send your BOM", "Genuine products from more than 40 manufacturers, including"
        three = ("For every line of your list", [("Price", "from European stock"), ("Lead time", "stated per line"), ("Alternative", "only if you allow it")])
    else:
        loc = "Hurtowy dostawca komponentów automatyki i elektrotechniki · Długołęka k. Wrocławia"
        lead = "PLC, HMI, czujniki, styczniki, zasilacze i aparatura rozdzielcza od oryginalnych producentów. Wyślij całą listę materiałową, a dostaniesz jedną ofertę z cenami, terminami i zamiennikami, z dostawą z magazynów w Europie."
        cta, strip_t = "Wyślij listę BOM", "Oryginalne produkty ponad 40 producentów, m.in."
        three = ("Dla każdej pozycji listy", [("Cena", "z magazynów w Europie"), ("Termin", "podany przy pozycji"), ("Zamiennik", "tylko gdy go dopuszczasz")])
    strip = "".join(f'<li>{brand_img(s, n)}</li>' for s, n in LOGOS if s in STRIP)
    hero = f'''<section class="hero" aria-labelledby="h1">
  <div class="hero-main wrap">
    <figure class="hero-img">{pic("cabinet", CATEGORIES[0][L]["alt"], "(max-width: 860px) 100vw, 50vw", eager=True, high=True)}</figure>
    <div class="hero-txt">
      <p class="hero-loc">{esc(loc)}</p>
      <h1 id="h1">{esc(m["h1"])}</h1>
      <p class="lead">{esc(lead)}</p>
      <div class="hero-cta" id="heroCta"><a class="btn btn-lg" href="{rel(P("contact"))}#rfq">{cta}{I_ARROW}</a><a class="mail-link" href="mailto:{EMAIL}">{I_MAIL}{EMAIL}</a></div>
      <div class="hero-three"><p>{esc(three[0])}:</p><ul>{"".join(f'<li><i aria-hidden="true"></i><b>{esc(a)}</b> <span>{esc(b)}</span></li>' for a, b in three[1])}</ul></div>
    </div>
  </div>
  <div class="strip">
    <div class="wrap strip-in">
      <p>{strip_t}</p>
      <ul class="strip-logos">{strip}</ul>
      <a class="more" href="{rel(P("products"))}#brands">{tr()["see_brands"]}{I_ARROW}</a>
    </div>
  </div>
</section>'''

    # categories
    if L == "en":
        h_cat, p_cat = "What we supply", "Electrical and electronic components for automation, switchboard building, construction and industry, from a single part number to the complete material list of a project."
    else:
        h_cat, p_cat = "Co dostarczamy", "Komponenty elektryczne i elektroniczne dla automatyki, prefabrykacji rozdzielnic, budownictwa i przemysłu, od pojedynczej pozycji po kompletną listę materiałową projektu."
    tiles = "".join(f'''<li class="cat"><a href="{rel(P("products"))}#{c["id"]}">
  <span class="cat-img">{pic(c["img"], c[L]["alt"], "(max-width: 560px) 34vw, (max-width: 1000px) 45vw, 400px")}</span>
  <span class="cat-txt"><span class="cat-t">{esc(c[L]["t"])}</span><span class="cat-s">{esc(", ".join(c[L]["s"][:4]))}</span></span></a></li>''' for c in CATEGORIES)
    cats = f'''<section class="sec" aria-labelledby="h-cat">
  <div class="wrap">
    <div class="sec-head"><h2 id="h-cat">{h_cat}</h2><p>{p_cat}</p></div>
    <ul class="cats">{tiles}</ul>
  </div>
</section>'''

    # BOM
    if L == "en":
        bom_h = "Send your BOM, get one quote for the whole list"
        bom_p = ["A BOM (bill of materials) lists every component needed to build a control cabinet, a machine or an installation. In switchboard prefabrication, retrofits and export projects what matters is getting the whole list from one source, on time and at a sensible price.",
                 "A list we can quote quickly includes:"]
        bom_li = ["the part number, e.g. 6ES7212-1BE40-0XB0,", "a short technical description and the quantity,", "the preferred manufacturer, if one is required,", "whether alternatives are acceptable and which certificates you need."]
        bom_end = "We handle orders from EUR 100 up to BOMs worth several hundred thousand euros."
        bom_b = "How BOM sourcing works"
    else:
        bom_h = "Wyślij listę BOM, dostaniesz jedną ofertę na całość"
        bom_p = ["BOM (bill of materials) to lista wszystkich komponentów potrzebnych do wykonania szafy sterowniczej, maszyny albo instalacji. Przy prefabrykacji rozdzielnic, retrofitach i projektach eksportowych liczy się, żeby cała lista przyszła z jednego źródła, na czas i w rozsądnej cenie.",
                 "Listę wycenimy najszybciej, gdy zawiera:"]
        bom_li = ["kod produktu, np. 6ES7212-1BE40-0XB0,", "krótki opis techniczny i ilość,", "preferowanego producenta, jeśli jest wymagany,", "informację, czy dopuszczasz zamienniki i jakie certyfikaty są potrzebne."]
        bom_end = "Obsługujemy zamówienia od 100 EUR po listy BOM o wartości kilkuset tysięcy euro."
        bom_b = "Jak wyceniamy listy BOM"
    bom = f'''<section class="sec sec-panel" aria-labelledby="h-bom">
  <div class="wrap split">
    <div class="split-txt">
      <h2 id="h-bom">{bom_h}</h2>
      {"".join(f"<p>{x}</p>" for x in bom_p)}
      <ul class="ticks">{"".join(f"<li>{x}</li>" for x in bom_li)}</ul>
      <p>{bom_end}</p>
      <p class="actions"><a class="btn" href="{rel(P("contact"))}#rfq">{cta}</a><a class="txt-link" href="{rel(P("services"))}#bom">{bom_b}{I_ARROW}</a></p>
    </div>
    {bom_table()}
  </div>
</section>'''

    # services overview
    if L == "en":
        sv_h = "How we work with buyers and engineers"
        sv = [("bom", "BOM sourcing", "One quote for the complete list, with lead times per line and alternatives where you allow them."),
              ("obsolete", "Obsolete and hard-to-find parts", "We search distributors, manufacturers and independent suppliers across Europe and propose compliant replacements."),
              ("project", "Project supply", "For prefabricators, integrators, OEMs and general contractors: 50-300 line lists consolidated into one delivery."),
              ("export", "Logistics and export", "EXW, FCA or DAP. Courier or pallet freight to Europe, the US, Asia, the Middle East and Africa.")]
    else:
        sv_h = "Jak pracujemy z zaopatrzeniem i inżynierami"
        sv = [("bom", "Wycena list BOM", "Jedna oferta na całą listę, z terminem dla każdej pozycji i zamiennikami tam, gdzie je dopuszczasz."),
              ("obsolete", "Części wycofane i trudno dostępne", "Szukamy u dystrybutorów, producentów i niezależnych dostawców w całej Europie i proponujemy zgodne zamienniki."),
              ("project", "Dostawy projektowe", "Dla prefabrykatorów, integratorów, OEM i generalnych wykonawców: listy na 50-300 pozycji w jednej dostawie."),
              ("export", "Logistyka i eksport", "EXW, FCA albo DAP. Kurier lub spedycja paletowa do Europy, USA, Azji, na Bliski Wschód i do Afryki.")]
    svc = "".join(f'<li><h3><a href="{rel(P("services"))}#{a}">{esc(t)}</a></h3><p>{esc(d)}</p></li>' for a, t, d in sv)
    services = f'''<section class="sec sec-dark" aria-labelledby="h-sv">
  <div class="wrap">
    <div class="sec-head"><h2 id="h-sv">{sv_h}</h2></div>
    <ul class="svc">{svc}</ul>
  </div>
</section>'''

    # references
    if L == "en":
        rf_h, rf_p = "Examples from our work", "We review lists, find alternatives, shorten lead times and combine orders from many sources."
    else:
        rf_h, rf_p = "Przykłady z naszej pracy", "Analizujemy listy, dobieramy zamienniki, skracamy terminy i łączymy zamówienia z wielu źródeł."
    rows = "".join(f'''<li class="case-row">
  <div class="case-who"><h3><a href="{rel(P("references"))}#{c["id"]}">{esc(c[L]["t"])}</a></h3><p>{esc(c[L]["brands"])}</p></div>
  <p class="case-sit">{esc(c[L]["did"])}</p>
  <p class="case-res">{esc(c[L]["res"])}</p>
</li>''' for c in CASES)
    refs = f'''<section class="sec sec-line" aria-labelledby="h-rf">
  <div class="wrap">
    <div class="sec-head sec-head-row"><div><h2 id="h-rf">{rf_h}</h2><p>{rf_p}</p></div><a class="txt-link" href="{rel(P("references"))}">{tr()["case_more"]}{I_ARROW}</a></div>
    <ol class="cases">{rows}</ol>
  </div>
</section>'''

    # export
    if L == "en":
        ex_h = "Deliveries in Poland and worldwide"
        ex_p = "We check availability with distributors, manufacturers and independent suppliers across Europe. When a list has 50-300 lines and the project was due yesterday, we consolidate the order at our warehouse in Długołęka near Wrocław and ship it as one delivery."
        ex_alt = "Container port with a world map overlay"
    else:
        ex_h = "Dostawy w Polsce i na eksport"
        ex_p = "Sprawdzamy dostępność u dystrybutorów, producentów i niezależnych dostawców w całej Europie. Gdy lista ma 50-300 pozycji, a projekt jest na wczoraj, konsolidujemy zamówienie w naszym magazynie w Długołęce pod Wrocławiem i wysyłamy je jedną dostawą."
        ex_alt = "Port kontenerowy z nałożoną mapą świata"
    export = f'''<section class="export" aria-labelledby="h-ex">
  <figure class="export-img">{pic("export", ex_alt, "(max-width: 900px) 100vw, 50vw")}</figure>
  <div class="export-txt">
    <h2 id="h-ex">{ex_h}</h2>
    <p>{ex_p}</p>
    {facts_dl(export_rows(), "facts facts-tight")}
    <p class="small">{countries()}</p>
  </div>
</section>'''

    # company
    if L == "en":
        co_h = "In the electrical trade since 2009"
        co_p = ["GP ENERGIA sp. z o.o. started with electrical installation work, took part in gas sector projects and spent five years prefabricating control cabinets and switchboards. Since 2022 we have focused on wholesale and sourcing of automation and electrical components, and since 2025 on export.",
                "That background matters when you send a list: we know what the parts do in a cabinet, which substitutes are safe to propose and which are not."]
        co_b = "Company history"
    else:
        co_h = "W branży elektrotechnicznej od 2009 roku"
        co_p = ["GP ENERGIA sp. z o.o. zaczynała od usług elektroinstalacyjnych, uczestniczyła w projektach dla sektora gazowego i przez pięć lat prefabrykowała szafy sterownicze i rozdzielnice. Od 2022 roku zajmujemy się handlem hurtowym i sourcingiem komponentów automatyki i elektrotechniki, a od 2025 roku także eksportem.",
                "To doświadczenie ma znaczenie przy każdej liście: wiemy, jaką rolę pełni dana część w szafie i który zamiennik można bezpiecznie zaproponować, a którego nie."]
        co_b = "Historia firmy"
    company = f'''<section class="sec" aria-labelledby="h-co">
  <div class="wrap split split-co">
    <div class="split-txt">
      <h2 id="h-co">{co_h}</h2>
      {"".join(f"<p>{x}</p>" for x in co_p)}
      <p><a class="txt-link" href="{rel(P("about"))}">{co_b}{I_ARROW}</a></p>
    </div>
    {facts_dl(company_rows())}
  </div>
</section>'''

    # blog
    posts = BLOGMOD.posts(L)[:3]
    blog_html = ""
    if posts:
        h_b = "Guides for buyers and engineers" if L == "en" else "Poradniki dla zaopatrzenia i inżynierów"
        items = "".join(post_card(p) for p in posts)
        blog_html = f'''<section class="sec sec-line" aria-labelledby="h-bl">
  <div class="wrap">
    <div class="sec-head sec-head-row"><h2 id="h-bl">{h_b}</h2><a class="txt-link" href="{rel(P("blog"))}">{"All articles" if L == "en" else "Wszystkie artykuły"}{I_ARROW}</a></div>
    <ul class="posts">{items}</ul>
  </div>
</section>'''

    hfaq = SEO_FAQ.get(("home", L)) or FAQ[L]
    faq_html = f'''<section class="sec sec-line" aria-labelledby="h-hfaq"><div class="wrap narrow"><h2 id="h-hfaq">{tr()["faq"]}</h2>{faq_block(hfaq)}</div></section>'''
    body = hero + cats + bom + services + refs + export + company + blog_html + faq_html + cta_band()
    render("home", L, body, [faq_ld(hfaq)])

def post_card(p):
    L = C.lang
    return f'''<li class="post"><a href="{rel(p["path"])}">
  <span class="post-img">{pic(p["img"], "", "(max-width: 700px) 100vw, 400px")}</span>
  <span class="post-meta">{fmt_date(p["date"], L)} · {p["mins"]} {tr()["min"]}</span>
  <span class="post-t">{esc(p["title_h"])}</span>
  <span class="post-x">{esc(p["excerpt"])}</span></a></li>'''

def fmt_date(d, L):
    y, m, dd = d.split("-")
    if L == "en":
        mon = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][int(m)-1]
        return f"{int(dd)} {mon} {y}"
    mon = ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca", "sierpnia", "września", "października", "listopada", "grudnia"][int(m)-1]
    return f"{int(dd)} {mon} {y}"

SVC = {
 "service_bom": {
  "img": "cabinet",
  "en": {"lead": "A BOM (bill of materials) is the complete list of components needed to build an electrical panel, a control system or an automation solution. Send it as it is, from ERP, EPLAN, a spreadsheet or a PDF, and get one quote for every line, with price, lead time and alternatives where they help.",
         "nav": "BOM sourcing",
         "sec": [("What a good BOM includes", "<ul class=ticks><li>manufacturer or brand,</li><li>full part number, e.g. 6ES7212-1BE40-0XB0,</li><li>a short technical description and quantity,</li><li>whether alternatives are allowed and which certificates are required,</li><li>delivery address and date, or Incoterms.</li></ul><p>The full checklist is in our guide <a href='{blog_bom}'>what to include in a BOM request</a>.</p>"),
                 ("What we do with your list", "<ul class=ticks><li>review and check every line,</li><li>propose direct or equivalent alternatives where the original is slow, expensive or discontinued, always marked next to the original,</li><li>handle mixed-brand requests (PLC, HMI, sensors, wiring) in one order,</li><li>source from suppliers in the EU with short lead times,</li><li>consolidate the delivery and invoice it once.</li></ul>"),
                 ("Numbers worth knowing", "<p>Quotes often within 1-6 hours. Orders from EUR 100 up to BOMs worth several hundred thousand euros. Lists of 50-300 lines are routine.</p>")],
         "aside": "bom"},
  "pl": {"lead": "BOM (bill of materials, lista materiałowa) to pełna lista komponentów potrzebnych do zbudowania rozdzielnicy, układu sterowania albo instalacji automatyki. Wyślij ją w takiej postaci, w jakiej ją masz, z ERP, EPLAN, arkusza albo PDF, a dostaniesz jedną ofertę na wszystkie pozycje, z ceną, terminem i zamiennikami tam, gdzie się przydadzą.",
         "nav": "Wycena list BOM",
         "sec": [("Co powinna zawierać dobra lista BOM", "<ul class=ticks><li>producenta lub markę,</li><li>pełny numer katalogowy, np. 6ES7212-1BE40-0XB0,</li><li>krótki opis techniczny i ilość,</li><li>informację, czy dopuszczasz zamienniki i jakie certyfikaty są wymagane,</li><li>adres i termin dostawy albo warunki Incoterms.</li></ul><p>Pełna lista kontrolna jest w poradniku <a href='{blog_bom}'>co zawrzeć w zapytaniu z listą BOM</a>.</p>"),
                 ("Co robimy z Twoją listą", "<ul class=ticks><li>sprawdzamy każdą pozycję,</li><li>proponujemy zamienniki bezpośrednie lub równoważne, gdy oryginał ma długi termin, jest drogi albo wycofany, zawsze oznaczone obok oryginału,</li><li>łączymy wiele marek (PLC, HMI, czujniki, osprzęt) w jednym zamówieniu,</li><li>kupujemy u dostawców w UE z krótkim terminem,</li><li>konsolidujemy dostawę i wystawiamy jedną fakturę.</li></ul>"),
                 ("Liczby", "<p>Wycena często w 1-6 godzin. Zamówienia od 100 EUR po listy BOM o wartości kilkuset tysięcy euro. Listy po 50-300 pozycji to dla nas codzienność.</p>")],
         "aside": "bom"}},
 "service_obsolete": {
  "img": "gauges",
  "en": {"lead": "When a manufacturer discontinues a PLC module, a relay or a fire panel, the installed base does not disappear. Plants and buildings still run on it, and a single missing part can stop a line or hold up a handover.",
         "nav": "Obsolete parts",
         "sec": [("Two ways we solve it", "<h3>Find the original</h3><p>We search remaining stock at distributors, manufacturers and independent suppliers across Europe, and tell you the condition and origin of every item.</p><h3>Replace it properly</h3><p>If the original is gone or too risky, we propose a compatible alternative and send the documentation, so your engineer can check fit, function and wiring before ordering.</p>"),
                 ("Typical requests", "<p>Discontinued PLC CPUs and I/O modules, HMI panels, safety relays, communication modules, detectors and control units from alarm, BMS and fire systems.</p>"),
                 ("Example", "<p>A general contractor upgrading BMS and fire alarm systems from 2005-2010 found that the design relied on relays, detectors and control panels no longer made. Working with a systems integrator in a consortium, we proposed a new system concept that was technically compliant, ready to install and cheaper than planned. <a href='{ref3}'>Read the case</a>.</p><p>Guide: <a href='{blog_obs}'>how to source obsolete automation components safely</a>.</p>")]},
  "pl": {"lead": "Gdy producent wycofuje moduł PLC, przekaźnik albo centralę ppoż., zainstalowane urządzenia nadal pracują. Zakłady i budynki dalej na nich działają, a brak jednej części potrafi zatrzymać linię albo opóźnić odbiór obiektu.",
         "nav": "Części wycofane",
         "sec": [("Dwa sposoby", "<h3>Znaleźć oryginał</h3><p>Szukamy pozostałych zapasów u dystrybutorów, producentów i niezależnych dostawców w Europie i podajemy stan oraz pochodzenie każdej pozycji.</p><h3>Dobrać zamiennik</h3><p>Jeśli oryginału nie ma albo ryzyko jest zbyt duże, proponujemy zgodny zamiennik i przesyłamy dokumentację, żeby projektant sprawdził wymiary, funkcje i podłączenie przed zamówieniem.</p>"),
                 ("Najczęstsze zapytania", "<p>Wycofane jednostki centralne PLC i moduły wejść/wyjść, panele HMI, przekaźniki bezpieczeństwa, moduły komunikacyjne, czujki i moduły kontrolno-sterujące systemów alarmowych, BMS i ppoż.</p>"),
                 ("Przykład", "<p>Generalny wykonawca modernizował systemy BMS i sygnalizacji pożaru z lat 2005-2010. Projekt opierał się na przekaźnikach, czujkach i centralach, których już nie produkowano. W konsorcjum z integratorem zaproponowaliśmy nową koncepcję systemu: zgodną technicznie, gotową do montażu i tańszą od założeń. <a href='{ref3}'>Zobacz realizację</a>.</p><p>Poradnik: <a href='{blog_obs}'>części automatyki wycofane z produkcji - jak kupić bezpiecznie</a>.</p>")]}},
 "service_project": {
  "img": "breakers",
  "en": {"lead": "Switchboard prefabrication, plant retrofits and building system upgrades all depend on one thing: having every part on site when the schedule says so. We built switchboards and control cabinets ourselves for years, so we know which lines in a BOM usually cause delays.",
         "nav": "Project supply",
         "sec": [("What we take on", "<ul class=ticks><li>review of the project BOM and flagging of long-lead and discontinued items,</li><li>alternatives that keep the design compliant,</li><li>price optimisation across brands,</li><li>deliveries split into stages to match your schedule,</li><li>cooperation with your integrator when a system needs redesign.</li></ul>"),
                 ("Who it is for", "<p>Switchboard prefabricators, automation integrators, OEMs, general contractors and plant owners, as well as distributors, resellers and procurement teams. Industries: industrial automation, switchboard prefabrication, machine building, food processing, marine, oil and gas, power generation and rail.</p>"),
                 ("Two results", "<ul class=ticks><li>Plant modernisation for an integrator: the cost of the list cut by 9.5% on average and by up to 30% on single items, complete set delivered in 4 weeks. <a href='{ref2}'>Read the case</a>.</li><li>Switchboard prefabricator, Czech Republic: Siemens S7-1200 and Phoenix Contact QUINT quoted by the makers at 6 and 8 weeks, delivered from EU stock in 48-72 hours. <a href='{ref1}'>Read the case</a>.</li></ul>")]},
  "pl": {"lead": "Prefabrykacja rozdzielnic, modernizacja zakładu czy wymiana systemów w budynku zależą od jednego: żeby każda część była na miejscu wtedy, kiedy wymaga tego harmonogram. Przez lata sami budowaliśmy rozdzielnice i szafy sterownicze, więc wiemy, które pozycje BOM najczęściej powodują opóźnienia.",
         "nav": "Dostawy projektowe",
         "sec": [("Czym się zajmujemy", "<ul class=ticks><li>analiza projektowej listy BOM i wskazanie pozycji z długim terminem lub wycofanych,</li><li>zamienniki, przy których projekt pozostaje zgodny z wymaganiami,</li><li>optymalizacja cen między markami,</li><li>dostawy etapami, zgodnie z harmonogramem,</li><li>współpraca z integratorem, gdy system wymaga przeprojektowania.</li></ul>"),
                 ("Dla kogo", "<p>Prefabrykatorzy rozdzielnic, integratorzy automatyki, producenci maszyn (OEM), generalni wykonawcy i właściciele zakładów, a także dystrybutorzy, resellerzy i działy zaopatrzenia. Branże: automatyka przemysłowa, prefabrykacja rozdzielnic, budowa maszyn, przemysł spożywczy, przemysł morski, ropa i gaz, energetyka i kolej.</p>"),
                 ("Dwa wyniki", "<ul class=ticks><li>Modernizacja zakładu dla integratora: koszt listy niższy średnio o 9,5%, na pojedynczych pozycjach do 30%, komplet w 4 tygodnie. <a href='{ref2}'>Zobacz realizację</a>.</li><li>Prefabrykator rozdzielnic z Czech: Siemens S7-1200 i Phoenix Contact QUINT u producentów 6 i 8 tygodni, od nas z magazynów w UE w 48-72 godziny. <a href='{ref1}'>Zobacz realizację</a>.</li></ul>")]}},
 "service_export": {
  "img": "export",
  "en": {"lead": "When a list has 50-300 lines and the project was due yesterday, splitting it across a dozen suppliers costs time. We check availability across Europe, consolidate the order at our warehouse in Długołęka near Wrocław and ship it as one delivery.",
         "nav": "Logistics and export",
         "sec": [("How we ship", "{export_dl}"),
                 ("Recent destinations", "<p>Germany, France, Spain, Italy, Romania, Turkey, India, Saudi Arabia, Vietnam, the UAE, Qatar, the Philippines and Thailand.</p>"),
                 ("For buyers in the Middle East and Asia", "<p>If you are looking for a European supplier of Siemens, Schneider Electric, ABB or Phoenix Contact parts with a better lead time than you get locally, send us the list. A late delivery on an export project can mean penalties, so we tell you the real lead time per line up front.</p>"),
                 ("Commonly shipped", "<p>PLCs, HMIs, safety relays, digital and analogue I/O modules, sensors, transmitters, power supplies, contactors, soft starters, interfaces, communication modules, connectors, and discontinued parts or their replacements.</p>")]},
  "pl": {"lead": "Gdy lista ma 50-300 pozycji, a projekt był na wczoraj, rozbijanie zamówienia na kilkunastu dostawców kosztuje czas. Sprawdzamy dostępność w całej Europie, konsolidujemy zamówienie w magazynie w Długołęce pod Wrocławiem i wysyłamy jedną dostawą.",
         "nav": "Logistyka i eksport",
         "sec": [("Jak wysyłamy", "{export_dl}"),
                 ("Dokąd ostatnio wysyłaliśmy", "<p>Niemcy, Francja, Hiszpania, Włochy, Rumunia, Turcja, Indie, Arabia Saudyjska, Wietnam, ZEA, Katar, Filipiny i Tajlandia.</p>"),
                 ("Najczęściej wysyłane", "<p>Sterowniki PLC, panele HMI, przekaźniki bezpieczeństwa, moduły wejść/wyjść cyfrowych i analogowych, czujniki, przetworniki, zasilacze, styczniki, softstarty, interfejsy, moduły komunikacyjne, konektory oraz części wycofane z produkcji i ich zamienniki.</p>")]}},
}
SVC_ORDER = ["service_bom", "service_obsolete", "service_project", "service_export"]

def blog_link(key):
    for p in BLOGMOD.posts(C.lang):
        if key in p["slug"]:
            return rel(p["path"])
    return rel(P("blog"))

def svc_crumbs(pid=None):
    t = tr()
    it = [(t["home"], P("home")), (t["nav"][1][1], P("services"))]
    if pid:
        it.append((SVC[pid][C.lang]["nav"], P(pid)))
    return it

def svc_subnav(cur=None):
    L = C.lang
    lis = "".join(f'<li><a href="{rel(P(k))}"{" aria-current=" + chr(34) + "page" + chr(34) if k == cur else ""}>{esc(SVC[k][L]["nav"])}</a></li>' for k in SVC_ORDER)
    return f'<nav class="subnav" aria-label="{"Services" if L == "en" else "Usługi"}"><div class="wrap"><ul>{lis}</ul></div></nav>'

def page_services(L):
    m = META["services"][L]; t = tr()
    C.lang = L; C.path = P("services", L); C.pid = "services"
    if L == "en":
        lead = "We do more than buy single parts. We review lists, find alternatives, shorten lead times and combine orders from many sources into one delivery. One contact, one quote, one invoice."
        how_h = "How it works"
        how = ["<b>Send</b> part numbers or a BOM file (xlsx, csv, pdf) to info@gpenergia.com.pl or through the form.",
               "<b>We check</b> availability with distributors, manufacturers and independent suppliers across Europe.",
               "<b>You get one quote</b>: price, lead time, alternatives and delivery terms for every line.",
               "<b>We consolidate</b> everything at our warehouse and ship it as one delivery."]
        more = "Read more"
        cmp_h = "Manufacturer or distributor?"
        cmp_p = "Buying direct from the manufacturer makes sense when a project needs the maker's full technical support, for example drive systems, SCADA or certified OEM applications. For prefabrication, switchboards, retrofits and export, a project distributor usually gives you more."
        blurbs = {"service_bom": "Send your bill of materials as it is. You get one quote for every line, with price, lead time and alternatives where they help.",
                  "service_obsolete": "Discontinued PLC modules, relays, detectors or control panels. We search European stock and, where needed, propose a compatible replacement with documentation.",
                  "service_project": "Complete component packages for panel prefabrication, plant retrofits and BMS or fire system upgrades, delivered in stages if your schedule needs it.",
                  "service_export": "Consolidation at our warehouse near Wrocław, courier or pallet freight, EXW, FCA or DAP, to Europe, the US, Asia, the Middle East and Africa."}
    else:
        lead = "Nie ograniczamy się do zakupu pojedynczych części. Sprawdzamy listy, szukamy zamienników, skracamy terminy i łączymy zamówienia z wielu źródeł w jedną dostawę. Jeden kontakt, jedna oferta, jedna faktura."
        how_h = "Jak to działa"
        how = ["<b>Wysyłasz</b> numery katalogowe albo plik BOM (xlsx, csv, pdf) na info@gpenergia.com.pl lub przez formularz.",
               "<b>Sprawdzamy</b> dostępność u dystrybutorów, producentów i niezależnych dostawców w Europie.",
               "<b>Dostajesz jedną ofertę</b>: cena, termin, zamienniki i warunki dostawy dla każdej pozycji.",
               "<b>Konsolidujemy</b> towar w magazynie i wysyłamy jedną dostawą."]
        more = "Więcej"
        cmp_h = "Producent czy dystrybutor?"
        cmp_p = "Zakup bezpośrednio u producenta sprawdza się, gdy projekt wymaga pełnego wsparcia technicznego producenta, np. przy systemach napędowych, SCADA czy certyfikowanych aplikacjach OEM. Przy prefabrykacji, rozdzielnicach, retrofitach i eksporcie więcej daje zwykle dystrybutor projektowy."
        blurbs = {"service_bom": "Wyślij listę BOM w takiej postaci, w jakiej ją masz. Dostaniesz jedną ofertę na wszystkie pozycje, z ceną, terminem i zamiennikami tam, gdzie się przydadzą.",
                  "service_obsolete": "Wycofane moduły PLC, przekaźniki, czujki czy centrale. Szukamy w magazynach w Europie, a w razie potrzeby proponujemy zgodny zamiennik z dokumentacją.",
                  "service_project": "Kompletne dostawy do prefabrykacji rozdzielnic, modernizacji zakładów oraz systemów BMS i ppoż., także etapami, jeśli tego wymaga harmonogram.",
                  "service_export": "Konsolidacja w magazynie pod Wrocławiem, kurier lub spedycja paletowa, EXW, FCA albo DAP, do Europy, USA, Azji, na Bliski Wschód i do Afryki."}
    ph = page_head(m["h1"], esc(lead), svc_crumbs())
    rows = "".join(f'''<li class="svc-row"><a href="{rel(P(k))}">
  <span class="svc-row-img">{pic(SVC[k]["img"], "", "(max-width: 760px) 30vw, 220px")}</span>
  <span class="svc-row-txt"><span class="svc-row-t">{esc(META[k][L]["h1"])}</span><span class="svc-row-d">{esc(blurbs[k])}</span></span>
  <span class="svc-row-more">{more}{I_ARROW}</span></a></li>''' for k in SVC_ORDER)
    faq = SEO_FAQ.get(("services", L)) or FAQ[L]
    body = ph + f'''<section class="sec"><div class="wrap"><ul class="svc-rows">{rows}</ul></div></section>
<section class="sec sec-dark" aria-labelledby="h-how"><div class="wrap split">
  <div class="split-txt"><h2 id="h-how">{how_h}</h2><ol class="steps">{"".join(f"<li>{x}</li>" for x in how)}</ol></div>
  {bom_table()}
</div></section>
<section class="sec" id="compare" aria-labelledby="h-compare"><div class="wrap narrow"><h2 id="h-compare">{cmp_h}</h2><p>{cmp_p}</p>{compare_table()}</div></section>
<section class="sec sec-line" id="faq" aria-labelledby="h-faq"><div class="wrap narrow"><h2 id="h-faq">{t["faq"]}</h2>{faq_block(faq)}</div></section>''' + cta_band()
    svc_ld = {"@type": "Service", "name": m["h1"], "provider": {"@id": CANON + "/#org"}, "areaServed": "Worldwide",
              "hasOfferCatalog": {"@type": "OfferCatalog", "name": m["h1"], "itemListElement": [
                  {"@type": "Offer", "itemOffered": {"@type": "Service", "name": META[k][L]["h1"], "url": CANON + "/" + P(k, L)}} for k in SVC_ORDER]}}
    render("services", L, body, [crumbs_ld(svc_crumbs()), svc_ld, faq_ld(faq)], ogimg="breakers")

def page_service_sub(pid, L):
    C.lang = L; C.pid = pid; C.path = P(pid, L)
    m = META[pid][L]; d = SVC[pid][L]; t = tr()
    refs = {f"ref{i+1}": rel(P("references")) + "#" + c["id"] for i, c in enumerate(CASES)}
    fill = dict(refs, blog_bom=blog_link("bom" if L == "en" else "bom"), blog_obs=blog_link("obsolete" if L == "en" else "wycofane"), export_dl=facts_dl(export_rows()))
    secs = "".join(f'<section class="subsec" aria-labelledby="h-s{i}"><h2 id="h-s{i}">{esc(h)}</h2>{c.format(**fill)}</section>' for i, (h, c) in enumerate(d["sec"]))
    side = bom_table() if d.get("aside") == "bom" else f'<figure class="svc-img">{pic(SVC[pid]["img"], "", "(max-width: 900px) 100vw, 40vw")}</figure>'
    cta_t = "Send your list" if L == "en" else "Wyślij listę"
    body = page_head(m["h1"], esc(d["lead"]), svc_crumbs(pid)) + svc_subnav(pid) + f'''<section class="sec sec-sub"><div class="wrap split split-sub">
  <div class="split-txt">{secs}<p class="actions"><a class="btn" href="{rel(P("contact"))}#rfq">{cta_t}</a><a class="mail-link" href="mailto:{EMAIL}">{I_MAIL}{EMAIL}</a></p></div>
  <div class="sub-side">{side}</div>
</div></section>''' + cta_band()
    ld = [crumbs_ld(svc_crumbs(pid)), {"@type": "Service", "name": m["h1"], "description": m["desc"], "provider": {"@id": CANON + "/#org"},
          "areaServed": "Worldwide", "url": CANON + "/" + P(pid, L)}]
    render(pid, L, body, ld, ogimg=SVC[pid]["img"])

def page_brands(L):
    C.lang = L; C.path = P("brands", L); C.pid = "brands"
    m = META["brands"][L]; t = tr()
    if L == "en":
        lead = "Genuine products from established manufacturers only. We can combine brands in one order and propose alternatives for discontinued models."
        look_h = "Looking for a specific brand?"
        look_p = "We are an independent B2B supplier. We source genuine products of these brands from European distribution and ship them worldwide, including to buyers in the Middle East and Asia. Send the part numbers and we will confirm availability and origin."
        note = "Brand names and logos belong to their owners and show the products we supply; they do not mean a partnership with the manufacturer."
    else:
        lead = "Tylko oryginalne produkty uznanych producentów. Łączymy marki w jednym zamówieniu i proponujemy zamienniki dla wycofanych modeli."
        look_h = "Szukasz konkretnej marki?"
        look_p = "Jesteśmy niezależnym dostawcą B2B. Oryginalne produkty tych marek kupujemy w europejskiej dystrybucji i wysyłamy na cały świat. Wyślij numery katalogowe, a potwierdzimy dostępność i pochodzenie towaru."
        note = "Nazwy i logotypy marek należą do ich właścicieli i pokazują produkty, które dostarczamy; nie oznaczają partnerstwa z producentem."
    ph = page_head(m["h1"], esc(lead), [(t["home"], P("home")), (t["nav"][0][1], P("products")), (m["h1"], P("brands"))])
    logos = "".join(f'<li>{brand_img(s, n)}</li>' for s, n in LOGOS)
    groups = "".join(f'<div class="bgroup"><h3>{esc(g)}</h3><p>{esc(", ".join(b))}</p></div>' for g, b in BRAND_GROUPS[L])
    body = ph + f'''<section class="sec"><div class="wrap"><ul class="logowall">{logos}</ul><p class="small">{esc(note)}</p></div></section>
<section class="sec sec-panel" aria-labelledby="h-groups"><div class="wrap"><h2 id="h-groups">{"All brands by product group" if L == "en" else "Wszystkie marki według grup produktów"}</h2><div class="bgroups">{groups}</div></div></section>
<section class="sec" aria-labelledby="h-look"><div class="wrap narrow"><h2 id="h-look">{look_h}</h2><p>{look_p}</p><p class="actions"><a class="btn" href="{rel(P("contact"))}#rfq">{t["cta"]}</a></p></div></section>''' + cta_band()
    render("brands", L, body, [crumbs_ld([(t["home"], P("home")), (t["nav"][0][1], P("products")), (m["h1"], P("brands"))])])

def page_products(L):
    m = META["products"][L]; t = tr()
    lead = ("Six product groups for automation, switchboard building and installations. Below each group you will find the typical items we quote. If your part is not listed, send the part number anyway."
            if L == "en" else
            "Sześć grup produktów dla automatyki, prefabrykacji rozdzielnic i instalacji. Przy każdej grupie wymieniamy typowe pozycje, które wyceniamy. Jeśli Twojej części nie ma na liście, i tak wyślij jej kod.")
    aside = f'<nav class="phead-toc" aria-label="{"On this page" if L=="en" else "Na tej stronie"}"><ul>' + "".join(f'<li><a href="#{c["id"]}">{esc(c[L]["t"])}</a></li>' for c in CATEGORIES) + f'<li><a href="#brands">{"Brands" if L=="en" else "Marki"}</a></li></ul></nav>'
    ph = page_head(m["h1"], esc(lead), [(t["home"], P("home")), (t["nav"][0][1], P("products"))], aside)
    groups = "".join(f'''<article class="pgroup" id="{c["id"]}" aria-labelledby="h-{c["id"]}">
  <div class="pgroup-img">{pic(c["img"], c[L]["alt"], "(max-width: 760px) 100vw, 360px")}</div>
  <div class="pgroup-txt">
    <h2 id="h-{c["id"]}">{esc(c[L]["t"])}</h2>
    <p>{esc(c[L]["d"])}</p>
    <ul class="sublist">{"".join(f"<li>{esc(s)}</li>" for s in c[L]["s"])}</ul>
    <p><a class="txt-link" href="{rel(P("contact"))}#rfq">{"Ask for a price" if L=="en" else "Zapytaj o cenę"}{I_ARROW}</a></p>
  </div>
</article>''' for c in CATEGORIES)
    logos = "".join(f'<li>{brand_img(s, n)}</li>' for s, n in LOGOS)
    shown = {n for _, n in LOGOS}
    rest = [b for b in BRANDS if b not in shown] + [b for b in BRANDS_EXTRA if b not in shown]
    if L == "en":
        br_h, br_p, br_r = "Brands we supply", "Genuine products from established manufacturers. We combine brands in one order and propose alternatives for discontinued models.", "Also: "
    else:
        br_h, br_p, br_r = "Marki, które dostarczamy", "Oryginalne produkty uznanych producentów. Łączymy marki w jednym zamówieniu i proponujemy zamienniki dla modeli wycofanych z produkcji.", "A także: "
    brands = f'''<section class="sec sec-panel" id="brands" aria-labelledby="h-brands">
  <div class="wrap">
    <div class="sec-head"><h2 id="h-brands">{br_h}</h2><p>{br_p}</p></div>
    <ul class="logowall">{logos}</ul>
    <p class="brands-rest">{br_r}{esc(", ".join(rest))}.</p>
    <p class="small">{esc(t["foot_note"].split(". ", 1)[1])}</p>
  </div>
</section>'''
    body = ph + f'<section class="sec"><div class="wrap pgroups">{groups}</div></section>' + brands + cta_band()
    itemlist = {"@type": "ItemList", "name": m["h1"], "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": c[L]["t"], "url": CANON + "/" + P("products") + "#" + c["id"]} for i, c in enumerate(CATEGORIES)]}
    render("products", L, body, [crumbs_ld([(t["home"], P("home")), (t["nav"][0][1], P("products"))]), itemlist])

def page_references(L):
    m = META["references"][L]; t = tr()
    lead = ("Three supplies that show how we work: a shorter lead time for a prefabricator, a lower BOM cost for an integrator and a new concept where parts were no longer made. Client names are not published."
            if L == "en" else
            "Trzy dostawy, które pokazują, jak pracujemy: krótszy termin dla prefabrykatora, niższy koszt listy dla integratora i nowa koncepcja tam, gdzie części nie były już produkowane. Nie publikujemy nazw klientów.")
    ph = page_head(m["h1"], esc(lead), [(t["home"], P("home")), (t["nav"][2][1], P("references"))])
    lab = {"en": ("Client", "Project", "Scope", "Brands", "Part numbers", "The situation", "What we did", "Result"),
           "pl": ("Klient", "Projekt", "Zakres", "Marki", "Kody produktów", "Sytuacja", "Co zrobiliśmy", "Efekt")}[L]
    cases = "".join(f'''<article class="case" id="{c["id"]}" aria-labelledby="h-{c["id"]}">
  <header class="case-head"><p class="case-n">{i+1} / {len(CASES)}</p><h2 id="h-{c["id"]}">{esc(c[L]["t"])}</h2><p class="case-result">{esc(c[L]["res"])}</p></header>
  <div class="case-body">
    {facts_dl([(lab[0], esc(c[L]["client"])), (lab[1], esc(c[L]["where"])), (lab[2], esc(c[L]["scope"])), (lab[3], esc(c[L]["brands"])), (lab[4], esc(c[L]["parts"]))], "facts facts-case")}
    <div class="case-txt"><h3>{lab[5]}</h3><p>{esc(c[L]["sit"])}</p><h3>{lab[6]}</h3><p>{esc(c[L]["did"])}</p></div>
  </div>
</article>''' for i, c in enumerate(CASES))
    body = ph + f'<section class="sec"><div class="wrap cases-full">{cases}</div></section>' + cta_band()
    render("references", L, body, [crumbs_ld([(t["home"], P("home")), (t["nav"][2][1], P("references"))])])

def page_about(L):
    m = META["about"][L]; t = tr()
    if L == "en":
        lead = "GP ENERGIA sp. z o.o. is a Polish company with many years of experience in the electrical trade. Since 2009 we have kept developing our skills and adapting what we do to the needs of the market: from installation work and switchboard prefabrication to international sourcing of automation components."
        h_hist, h_who, h_co, h_how = "Our history", "Who we work with", "Company details", "How we work"
        who = "Distributors, trading companies and resellers, industrial procurement teams, automation system integrators, switchboard prefabricators, OEMs, general contractors and plant owners."
        ind = "Industries: industrial automation, switchboard prefabrication, machine building, food processing, marine, oil and gas, power generation and rail."
        how = ["We build long-term business relationships on competitive commercial terms, clear communication and reliable delivery.", "Technical experience, global sourcing and international cooperation: that is what GP ENERGIA, Industrial Automation and Electrical Supply, stands for."]
    else:
        lead = "GP ENERGIA sp. z o.o. to polska firma z wieloletnim doświadczeniem w branży elektrotechnicznej. Od 2009 roku konsekwentnie rozwijamy kompetencje i dopasowujemy zakres działalności do potrzeb rynku: od instalacji i prefabrykacji rozdzielnic po międzynarodowy sourcing komponentów automatyki."
        h_hist, h_who, h_co, h_how = "Historia firmy", "Z kim pracujemy", "Dane firmy", "Jak pracujemy"
        who = "Dystrybutorzy, firmy handlowe i resellerzy, działy zaopatrzenia przemysłowego, integratorzy systemów automatyki, prefabrykatorzy rozdzielnic, producenci OEM, generalni wykonawcy i właściciele zakładów."
        ind = "Branże: automatyka przemysłowa, prefabrykacja rozdzielnic, budowa maszyn, przemysł spożywczy, przemysł morski, ropa i gaz, energetyka i kolej."
        how = ["Budujemy długoterminowe relacje biznesowe oparte na konkurencyjnych warunkach handlowych, sprawnej komunikacji i niezawodności dostaw.", "Doświadczenie techniczne, globalny sourcing i międzynarodowa współpraca: to oznacza GP ENERGIA, Industrial Automation and Electrical Supply."]
    ph = page_head(m["h1"], esc(lead), [(t["home"], P("home")), (t["nav"][3][1], P("about"))])
    hist = "".join(f'<li><p class="yr">{esc(y)}</p><div><h3>{esc(h)}</h3><p>{esc(d)}</p></div></li>' for y, h, d in HISTORY[L])
    body = ph + f'''<section class="sec" aria-labelledby="h-hist">
  <div class="wrap split split-about">
    <div class="split-txt"><h2 id="h-hist">{h_hist}</h2><ol class="timeline">{hist}</ol></div>
    <aside class="about-side">
      <h2 id="h-co">{h_co}</h2>
      {facts_dl(company_rows())}
    </aside>
  </div>
</section>
<section class="sec sec-panel" aria-labelledby="h-who">
  <div class="wrap split">
    <div class="split-txt"><h2 id="h-who">{h_who}</h2><p>{who}</p><p>{ind}</p></div>
    <div class="split-txt"><h2>{h_how}</h2>{"".join(f"<p>{x}</p>" for x in how)}</div>
  </div>
</section>''' + cta_band()
    render("about", L, body, [crumbs_ld([(t["home"], P("home")), (t["nav"][3][1], P("about"))])], ogimg="export")

def page_contact(L):
    m = META["contact"][L]; t = tr()
    if L == "en":
        lead = f'Enter part numbers or attach your BOM file, or e-mail <a href="mailto:{EMAIL}">{EMAIL}</a>. We reply with prices, lead times and any alternatives.'
        F = dict(subj="Subject", subj_o=["Price and availability", "BOM quote", "Obsolete or hard-to-find part", "Export delivery", "Other"],
                 company="Company", name="Name", email="E-mail", phone="Phone", country="Country", msg="Part numbers or message",
                 msg_ph="e.g. 6ES7212-1BE40-0XB0 - 2 pcs, LC1D09P7 - 10 pcs", file="BOM file", file_hint="xlsx, xls, csv or pdf, up to 10 MB",
                 file_btn="Choose file", file_none="No file selected",
                 consent=f'I agree to {COMPANY["legal"]} processing my data to answer this enquiry, as described in the <a href="{rel(P("privacy"))}">privacy policy</a>.',
                 req="required", send="Send enquiry", hp="Leave this field empty",
                 ok_h="Thank you, your enquiry is ready", ok_p="Preview version: the form is not connected yet. On the live site it is sent straight to info@gpenergia.com.pl. Until then please e-mail your list to",
                 side_h="Contact details", addr_h="Warehouse and dispatch", map_t="Map: ul. Polna 29, Długołęka", map_l="Open in Google Maps", reg_h="Company")
    else:
        lead = f'Wpisz kody produktów albo dołącz plik BOM lub napisz na <a href="mailto:{EMAIL}">{EMAIL}</a>. Odpowiemy z cenami, terminami dostaw i ewentualnymi zamiennikami.'
        F = dict(subj="Temat", subj_o=["Cena i dostępność", "Wycena listy BOM", "Część wycofana lub trudno dostępna", "Dostawa eksportowa", "Inne"],
                 company="Firma", name="Imię i nazwisko", email="E-mail", phone="Telefon", country="Kraj", msg="Kody produktów lub wiadomość",
                 msg_ph="np. 6ES7212-1BE40-0XB0 - 2 szt., LC1D09P7 - 10 szt.", file="Plik BOM", file_hint="xlsx, xls, csv lub pdf, do 10 MB",
                 file_btn="Wybierz plik", file_none="Nie wybrano pliku",
                 consent=f'Zgadzam się na przetwarzanie moich danych przez {COMPANY["legal"]} w celu odpowiedzi na zapytanie, zgodnie z <a href="{rel(P("privacy"))}">polityką prywatności</a>.',
                 req="wymagane", send="Wyślij zapytanie", hp="Zostaw to pole puste",
                 ok_h="Dziękujemy, zapytanie jest gotowe", ok_p="Wersja podglądowa: formularz nie jest jeszcze podłączony. Na docelowej stronie trafi prosto na info@gpenergia.com.pl. Do tego czasu prosimy o wysłanie listy na adres",
                 side_h="Dane kontaktowe", addr_h="Magazyn i wysyłka", map_t="Mapa: ul. Polna 29, Długołęka", map_l="Otwórz w Mapach Google", reg_h="Firma")
    ph = page_head(m["h1"], lead, [(t["home"], P("home")), (t["nav"][5][1], P("contact"))])
    star = f'<span class="req" aria-hidden="true">*</span>'
    opts = "".join(f"<option>{esc(o)}</option>" for o in F["subj_o"])
    form = f'''<form class="rfq" id="rfqForm" action="{FORM_ENDPOINT}" method="post" enctype="multipart/form-data" novalidate data-endpoint="{FORM_ENDPOINT}" data-lang="{L}">
  <div class="f f-full"><label for="f-subj">{F["subj"]}</label><select id="f-subj" name="subject">{opts}</select></div>
  <div class="f"><label for="f-company">{F["company"]} {star}</label><input id="f-company" name="company" autocomplete="organization" required aria-required="true"></div>
  <div class="f"><label for="f-name">{F["name"]}</label><input id="f-name" name="name" autocomplete="name"></div>
  <div class="f"><label for="f-email">{F["email"]} {star}</label><input id="f-email" name="email" type="email" autocomplete="email" required aria-required="true" inputmode="email"></div>
  <div class="f"><label for="f-phone">{F["phone"]}</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
  <div class="f f-full"><label for="f-country">{F["country"]}</label><input id="f-country" name="country" autocomplete="country-name"></div>
  <div class="f f-full"><label for="f-msg">{F["msg"]} {star}</label><textarea id="f-msg" name="message" rows="6" required aria-required="true" placeholder="{esc(F["msg_ph"])}"></textarea></div>
  <div class="f f-full f-file">
    <span class="lbl" id="f-file-l">{F["file"]}</span>
    <label class="filebox" for="f-file">{I_FILE}<span class="filebox-btn">{F["file_btn"]}</span><span class="filebox-name" id="f-file-name" data-none="{F["file_none"]}">{F["file_none"]}</span></label>
    <input id="f-file" class="sr-file" name="bom" type="file" accept=".xlsx,.xls,.csv,.pdf,application/pdf,text/csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" aria-describedby="f-file-h" aria-labelledby="f-file-l">
    <p class="hint" id="f-file-h">{F["file_hint"]}</p>
  </div>
  <div class="hp" aria-hidden="true"><label for="f-web">{F["hp"]}</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
  <input type="hidden" name="t" id="f-t" value="">
  <div class="f f-full f-check"><input id="f-consent" name="consent" type="checkbox" required aria-required="true"><label for="f-consent">{F["consent"]} {star}</label></div>
  <div class="f f-full f-submit"><button class="btn btn-lg" type="submit">{F["send"]}</button><p class="f-err" id="f-err" role="alert" aria-live="assertive"></p></div>
</form>
<div class="rfq-ok" id="rfqOk" hidden tabindex="-1">
  <h2>{F["ok_h"]}</h2>
  <p id="rfqSum"></p>
  <p>{F["ok_p"]} <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div>'''
    c = COMPANY
    gembed = "https://maps.google.com/maps?q=Polna+29%2C+55-095+D%C5%82ugo%C5%82%C4%99ka&amp;z=15&amp;hl=" + L + "&amp;output=embed"
    groute = "https://www.google.com/maps/dir/?api=1&amp;destination=Polna+29%2C+55-095+D%C5%82ugo%C5%82%C4%99ka"
    gmap = "https://www.google.com/maps/search/?api=1&amp;query=Polna+29%2C+55-095+D%C5%82ugo%C5%82%C4%99ka"
    side = f'''<aside class="contact-side" aria-labelledby="h-side">
  <h2 id="h-side">{F["side_h"]}</h2>
  <p class="big-mail"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <h3>{F["addr_h"]}</h3>
  <p>{c["legal"]}<br>{c["street"]}<br>{c["postcode"]} {c["city"]}, {"Poland" if L=="en" else "Polska"}</p>
  <div class="map" data-map><iframe title="{F["map_t"]}" src="{gembed}" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    <div class="map-off"><p><b>{c["street"]}</b><br>{c["postcode"]} {c["city"]}</p><p><a class="btn" href="{groute}" target="_blank" rel="noopener">{"Get directions" if L=="en" else "Wyznacz trasę"}</a></p><p class="small">{"The map is off because external media are disabled in" if L=="en" else "Mapa jest wyłączona, bo media zewnętrzne są wyłączone w"} <button type="button" class="ck-open" data-ck-open>{CK[L]["link"].lower()}</button>.</p></div></div>
  <p><a class="txt-link" href="{gmap}" target="_blank" rel="noopener">{F["map_l"]}{I_ARROW}</a></p>
  <h3>{F["reg_h"]}</h3>
  <p class="small">KRS {c["krs"]} · NIP {c["nip"]} · REGON {c["regon"]}</p>
</aside>'''
    body = ph + f'<section class="sec sec-contact" id="rfq" aria-label="{F["send"]}"><div class="wrap contact-grid"><div class="rfq-wrap">{form}</div>{side}</div></section>'
    cfaq = SEO_FAQ.get(("contact", L))
    if cfaq:
        body += f'''<section class="sec sec-line" aria-labelledby="h-cfaq"><div class="wrap narrow"><h2 id="h-cfaq">{t["faq"]}</h2>{faq_block(cfaq)}</div></section>'''
    cp = {"@type": "ContactPage", "url": CANON + "/" + P("contact"), "about": {"@id": CANON + "/#org"}}
    render("contact", L, body, [crumbs_ld([(t["home"], P("home")), (t["nav"][5][1], P("contact"))]), cp] + ([faq_ld(cfaq)] if cfaq else []))

def page_privacy(L):
    m = META["privacy"][L]; t = tr(); c = COMPANY
    if L == "en":
        lead = "This policy explains how we process personal data that you send us through the enquiry form or by e-mail."
        txt = f'''<h2>Data controller</h2>
<p>The controller of your personal data is {c["legal"]}, entered in the National Court Register (KRS) under number {c["krs"]}, NIP {c["nip"]}, REGON {c["regon"]}. You can contact us about personal data at <a href="mailto:{EMAIL}">{EMAIL}</a> or by post to our warehouse: {c["street"]}, {c["postcode"]} {c["city"]}, Poland.</p>
<h2>What data we process and why</h2>
<p>When you send an enquiry we process the data you enter: company name, name, e-mail address, phone number, country, the content of your message and any attached file. We use it to answer your enquiry, prepare a quote and, if you place an order, to carry out the contract (Article 6(1)(b) GDPR). We may also keep correspondence to defend against claims, which is our legitimate interest (Article 6(1)(f) GDPR).</p>
<p>Providing data is voluntary, but without an e-mail address we cannot reply to you.</p>
<h2>How long we keep it</h2>
<p>We keep enquiry data for as long as needed to handle the enquiry and any order that follows, and then for the period required by tax and accounting law or until claims become time-barred.</p>
<h2>Who receives the data</h2>
<p>Your data may be processed on our behalf by providers of hosting and e-mail services and by IT service providers, only to the extent necessary. If you order goods for delivery, we pass the necessary data to the carrier. We do not sell personal data.</p>
<h2>Transfers outside the EEA</h2>
<p>If an order is shipped outside the European Economic Area, the delivery data needed for shipping and customs is passed to the carrier and the recipient's customs authorities.</p>
<h2>Your rights</h2>
<p>You have the right to access your data, to have it corrected or deleted, to restrict processing, to data portability and to object to processing based on our legitimate interest. You can also lodge a complaint with the President of the Personal Data Protection Office (UODO), ul. Stawki 2, 00-193 Warsaw.</p>
<h2 id="cookies">Cookies and external services</h2>
<p>Cookies are small files saved by your browser. This website does not use analytics or advertising cookies. We use:</p>
<ul><li><strong>necessary storage</strong>: your cookie choice is saved in your browser for 12 months, so the banner does not appear on every page (legal basis: our legitimate interest, Article 6(1)(f) GDPR);</li>
<li><strong>external media</strong>: the map on the contact page is provided by Google Maps (Google Ireland Ltd.). When it loads, your browser connects to Google servers, which receive your IP address and may set their own cookies, as described in the Google privacy policy. If you choose "Necessary only", the map is not loaded and you see the address and a directions link instead.</li></ul>
<p>You can change or withdraw your choice at any time using the "Cookie settings" link in the footer, and you can also delete cookies in your browser settings.</p>
<h2>Changes</h2>
<p>We may update this policy, for example when we add new features to the website. The current version is always published on this page.</p>
<p class="small">Last updated: 6 November 2026.</p>'''
    else:
        lead = "Polityka wyjaśnia, jak przetwarzamy dane osobowe przesłane przez formularz zapytania lub pocztą elektroniczną."
        txt = f'''<h2>Administrator danych</h2>
<p>Administratorem Twoich danych osobowych jest {c["legal"]}, wpisana do Krajowego Rejestru Sądowego pod numerem KRS {c["krs"]}, NIP {c["nip"]}, REGON {c["regon"]}. W sprawach danych osobowych możesz kontaktować się z nami pod adresem <a href="mailto:{EMAIL}">{EMAIL}</a> albo listownie na adres magazynu: {c["street"]}, {c["postcode"]} {c["city"]}.</p>
<h2>Jakie dane przetwarzamy i w jakim celu</h2>
<p>Gdy wysyłasz zapytanie, przetwarzamy dane wpisane w formularzu: nazwę firmy, imię i nazwisko, adres e-mail, numer telefonu, kraj, treść wiadomości i załączony plik. Wykorzystujemy je, aby odpowiedzieć na zapytanie, przygotować ofertę, a jeśli złożysz zamówienie, aby wykonać umowę (art. 6 ust. 1 lit. b RODO). Korespondencję możemy także przechowywać w celu obrony przed roszczeniami, co jest naszym prawnie uzasadnionym interesem (art. 6 ust. 1 lit. f RODO).</p>
<p>Podanie danych jest dobrowolne, ale bez adresu e-mail nie możemy odpowiedzieć.</p>
<h2>Jak długo przechowujemy dane</h2>
<p>Dane z zapytania przechowujemy przez czas potrzebny do jego obsługi i realizacji ewentualnego zamówienia, a następnie przez okres wymagany przepisami podatkowymi i rachunkowymi lub do przedawnienia roszczeń.</p>
<h2>Komu przekazujemy dane</h2>
<p>Dane mogą przetwarzać w naszym imieniu dostawcy usług hostingu i poczty elektronicznej oraz usług informatycznych, wyłącznie w niezbędnym zakresie. Przy dostawie towaru przekazujemy niezbędne dane przewoźnikowi. Nie sprzedajemy danych osobowych.</p>
<h2>Przekazywanie poza EOG</h2>
<p>Jeśli zamówienie jest wysyłane poza Europejski Obszar Gospodarczy, dane potrzebne do wysyłki i odprawy celnej otrzymują przewoźnik i organy celne kraju odbiorcy.</p>
<h2>Twoje prawa</h2>
<p>Masz prawo dostępu do danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przenoszenia danych oraz sprzeciwu wobec przetwarzania opartego na naszym prawnie uzasadnionym interesie. Możesz też wnieść skargę do Prezesa Urzędu Ochrony Danych Osobowych, ul. Stawki 2, 00-193 Warszawa.</p>
<h2 id="cookies">Pliki cookies i usługi zewnętrzne</h2>
<p>Pliki cookies to niewielkie pliki zapisywane przez przeglądarkę. Strona nie używa analitycznych ani reklamowych plików cookies. Korzystamy z:</p>
<ul><li><strong>niezbędnego zapisu w przeglądarce</strong>: Twój wybór dotyczący cookies przechowujemy przez 12 miesięcy, żeby baner nie pojawiał się na każdej stronie (podstawa: nasz prawnie uzasadniony interes, art. 6 ust. 1 lit. f RODO);</li>
<li><strong>mediów zewnętrznych</strong>: mapę na stronie kontaktu dostarczają Mapy Google (Google Ireland Ltd.). Po jej wczytaniu przeglądarka łączy się z serwerami Google, które otrzymują Twój adres IP i mogą zapisać własne pliki cookies zgodnie z polityką prywatności Google. Po wybraniu „Tylko niezbędne” mapa nie jest wczytywana, a w jej miejscu widać adres i link do wyznaczenia trasy.</li></ul>
<p>Wybór możesz w każdej chwili zmienić lub wycofać przez link „Ustawienia cookies” w stopce strony, a pliki cookies możesz też usunąć w ustawieniach przeglądarki.</p>
<h2>Zmiany</h2>
<p>Możemy aktualizować politykę, np. gdy dodamy nowe funkcje strony. Aktualna wersja jest zawsze publikowana na tej stronie.</p>
<p class="small">Ostatnia aktualizacja: 6 listopada 2026 r.</p>'''
    ph = page_head(m["h1"], esc(lead), [(t["home"], P("home")), (t["foot_privacy"], P("privacy"))])
    body = ph + f'<section class="sec"><div class="wrap narrow prose">{txt}</div></section>'
    render("privacy", L, body, [crumbs_ld([(t["home"], P("home")), (t["foot_privacy"], P("privacy"))])])

def page_blog_index(L):
    m = META["blog"][L]; t = tr()
    lead = ("Practical guides on BOM sourcing, discontinued automation parts and shipping components abroad, written from our daily work with buyers and engineers."
            if L == "en" else
            "Praktyczne poradniki o wycenie list BOM, wycofanych komponentach automatyki i wysyłce części za granicę, pisane na podstawie codziennej pracy z zaopatrzeniem i inżynierami.")
    ph = page_head(m["h1"], esc(lead), [(t["home"], P("home")), ("Blog", P("blog"))])
    posts = BLOGMOD.posts(L)
    items = "".join(post_card(p) for p in posts)
    body = ph + f'<section class="sec"><div class="wrap"><ul class="posts posts-index">{items}</ul></div></section>' + cta_band()
    bl = {"@type": "Blog", "name": "GP ENERGIA Blog", "url": CANON + "/" + P("blog"), "inLanguage": L, "publisher": {"@id": CANON + "/#org"},
          "blogPost": [{"@type": "BlogPosting", "headline": p["title_h"], "url": CANON + "/" + p["path"], "datePublished": p["date"]} for p in posts]}
    render("blog", L, body, [crumbs_ld([(t["home"], P("home")), ("Blog", P("blog"))]), bl])

def page_article(p, L):
    t = tr()
    other = p["alt_path"]
    alt = (p["path"], other) if L == "en" else (other, p["path"])
    C.lang = L; C.pid = "article"; C.alt = alt; C.path = p["path"]
    p["html"], p["toc"] = BLOGMOD.render_html(p, rel)
    toc = "".join(f'<li><a href="#{a}">{esc(b)}</a></li>' for a, b in p["toc"])
    faq = p.get("faq") or []
    faq_html = f'<section class="art-faq" aria-labelledby="h-afaq"><h2 id="h-afaq">{t["faq"]}</h2>{faq_block(faq)}</section>' if faq else ""
    rel_posts = [q for q in BLOGMOD.posts(L) if q["slug"] != p["slug"]][:2]
    related = "".join(post_card(q) for q in rel_posts)
    if L == "en":
        box_h, box_p, box_b = "Have a BOM to quote?", "Send the list as it is. We reply with prices, lead times and alternatives, often within 1-6 hours.", "Send your BOM"
    else:
        box_h, box_p, box_b = "Masz listę BOM do wyceny?", "Wyślij ją w takiej postaci, w jakiej jest. Odpowiemy z cenami, terminami i zamiennikami, często w ciągu 1-6 godzin.", "Wyślij listę BOM"
    body = f'''<article class="art" aria-labelledby="h1">
  <header class="art-head">
    <div class="wrap art-head-in">
      {crumbs([(t["home"], P("home")), ("Blog", P("blog")), (p["title_h"], p["path"])])}
      <h1 id="h1">{esc(p["h1"])}</h1>
      <p class="art-meta"><time datetime="{p["date"]}">{fmt_date(p["date"], L)}</time> · {p["mins"]} {t["min"]} · GP ENERGIA</p>
      <p class="lead">{esc(p["lead"])}</p>
    </div>
  </header>
  <div class="wrap art-grid">
    <aside class="art-side">
      <nav class="art-toc" aria-label="{t["toc"]}"><p class="art-toc-h">{t["toc"]}</p><ol>{toc}</ol></nav>
      <div class="art-box"><p class="art-box-h">{box_h}</p><p>{box_p}</p><a class="btn" href="{rel(P("contact"))}#rfq">{box_b}</a></div>
    </aside>
    <div class="art-body prose">
      <figure class="art-img">{pic(p["img"], p.get("img_alt", ""), "(max-width: 1000px) 100vw, 760px", eager=True)}</figure>
      {p["html"]}
      {faq_html}
    </div>
  </div>
</article>
<section class="sec sec-line" aria-labelledby="h-rel"><div class="wrap"><div class="sec-head"><h2 id="h-rel">{t["related"]}</h2></div><ul class="posts">{related}</ul></div></section>''' + cta_band()
    ld = [crumbs_ld([(t["home"], P("home")), ("Blog", P("blog")), (p["title_h"], p["path"])]),
          {"@type": "BlogPosting", "headline": p["h1"], "description": p["desc"], "datePublished": p["date"], "dateModified": p.get("modified", p["date"]),
           "inLanguage": L, "mainEntityOfPage": CANON + "/" + p["path"], "author": {"@id": CANON + "/#org"}, "publisher": {"@id": CANON + "/#org"},
           "image": CANON + f"/img/p/{p['img']}-{MAN[p['img']]['w'][-1]}.webp"}]
    if faq:
        ld.append(faq_ld(faq))
    ld += p.get("extra_ld", [])
    m_title, m_desc = p["title"], p["desc"]
    out = head(m_title, m_desc, alt, ld, p["img"]) + header() + '<main id="main">\n' + body + '\n</main>\n' + footer()
    out = out.replace("—", "-").replace("–", "-")
    write(p["path"], out)

def page_404():
    C.lang = "en"; C.pid = "404"; C.alt = ("", "pl/"); C.path = ""
    base = "/" if PROD else PREVIEW_BASE
    # absolute links: page may be served at any depth
    global rel
    _rel = rel
    rel = lambda to: base + to
    body = f'''<section class="phead phead-404"><div class="wrap">
<h1>Page not found</h1>
<p class="lead">The page you are looking for does not exist or has moved. <span lang="pl">Nie znaleziono strony - mogła zostać przeniesiona.</span></p>
<p class="actions"><a class="btn" href="{base}">Go to the home page</a><a class="txt-link" href="{base}pl/" lang="pl">Strona główna po polsku{I_ARROW}</a><a class="txt-link" href="{base}contact/#rfq">Request a quote{I_ARROW}</a></p>
</div></section>'''
    out = head("Page not found | GP ENERGIA", "The page you are looking for does not exist.", C.alt, []).replace('<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="x-canonical"') + header() + '<main id="main">' + body + '</main>' + footer()
    rel = _rel
    (OUT / "404.html").write_text(out.replace("—", "-").replace("–", "-"), encoding="utf-8")

# ---------------------------------------------------------------- sitemap / robots
def sitemap(articles):
    urls = []
    lm = datetime.date.today().isoformat()
    pairs = [PATHS[k] for k in ("home", "products", "brands", "services", "service_bom", "service_obsolete", "service_project", "service_export", "references", "about", "blog", "contact", "privacy")]
    pairs += [(a["en"]["path"], a["pl"]["path"]) for a in articles]
    for en_p, pl_p in pairs:
        for loc in (en_p, pl_p):
            urls.append(f'''<url><loc>{CANON}/{loc}</loc><lastmod>{lm}</lastmod>
<xhtml:link rel="alternate" hreflang="en" href="{CANON}/{en_p}"/><xhtml:link rel="alternate" hreflang="pl" href="{CANON}/{pl_p}"/><xhtml:link rel="alternate" hreflang="x-default" href="{CANON}/{en_p}"/></url>''')
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n"
    (OUT / "sitemap.xml").write_text(xml, encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "ClaudeBot", "Claude-SearchBot", "Google-Extended", "Bingbot", "Googlebot"]
    prod_robots = "User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {CANON}/sitemap.xml\n"
    L_ = "\n".join(f"- [{a['en']['title_h']}]({CANON}/{a['en']['path']})" for a in articles)
    llms = f"""# GP ENERGIA sp. z o.o.

> Polish B2B supplier of industrial automation and electrical components (PLCs, HMIs, sensors, contactors, power supplies, switchgear, cabinets), sourced to customer BOM lists and shipped from a warehouse near Wrocław to Europe, the United States, Asia, the Middle East and Africa. Independent supplier, in the electrical trade since 2009.

- E-mail: {EMAIL}
- Warehouse: {COMPANY["street"]}, {COMPANY["postcode"]} {COMPANY["city"]}, Poland
- KRS {COMPANY["krs"]}, NIP {COMPANY["nip"]}, REGON {COMPANY["regon"]}
- Quotes often within 1-6 hours; orders from about EUR 100 to BOMs worth several hundred thousand euros; Incoterms EXW, FCA, DAP; languages English, Polish, Russian

## Pages
- [Services]({CANON}/services/): BOM sourcing, obsolete parts, project supply, logistics and export
- [BOM sourcing]({CANON}/services/bom-sourcing/)
- [Obsolete and discontinued parts]({CANON}/services/obsolete-parts/)
- [Project supply]({CANON}/services/project-supply/)
- [Logistics and export]({CANON}/services/logistics-export/)
- [Products]({CANON}/products/) and [brands]({CANON}/brands/)
- [References]({CANON}/references/)
- [About and history]({CANON}/about/)
- [Contact and request for quote]({CANON}/contact/)
- Polish version: {CANON}/pl/

## Blog
{L_}
"""
    (OUT / "llms.txt").write_text(llms, encoding="utf-8")
    (SRC / "production").mkdir(exist_ok=True)
    (SRC / "production" / "robots.txt").write_text(prod_robots, encoding="utf-8")
    (OUT / "robots.txt").write_text(prod_robots if PROD else "# preview - do not index\nUser-agent: *\nDisallow: /\n", encoding="utf-8")

# ---------------------------------------------------------------- main
def main():
    if PROD:
        if OUT.exists():
            shutil.rmtree(OUT)
        OUT.mkdir()
        for d in ("assets", "img"):
            shutil.copytree(ROOT / d, OUT / d)
        shutil.copy(ROOT / "site.webmanifest", OUT / "site.webmanifest")
    articles = BLOGMOD.load()
    for L in ("en", "pl"):
        # 05.11: kontekst strony (jezyk + sciezka) ustawiany PRZED skladaniem tresci - inaczej obrazy dostaja sciezki poprzedniej strony
        def _c(pid):
            C.lang = L; C.pid = pid; C.path = P(pid, L); C.alt = PATHS[pid]
        _c("home"); page_home(L); _c("services"); page_services(L); _c("products"); page_products(L)
        _c("references"); page_references(L); _c("about"); page_about(L); _c("brands"); page_brands(L)
        for k in SVC_ORDER:
            page_service_sub(k, L)
        _c("contact"); page_contact(L); _c("privacy"); page_privacy(L); _c("blog"); page_blog_index(L)
        for a in articles:
            page_article(a[L], L)
    page_404()
    sitemap(articles)
    print("built", "PROD" if PROD else "PREVIEW", "->", OUT, "| articles:", len(articles), "| SEO meta:", SEO_META, "| blog source:", BLOGMOD.SOURCE)

if __name__ == "__main__":
    main()
