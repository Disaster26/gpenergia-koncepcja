# -*- coding: utf-8 -*-
"""Blog loader. Articles are Markdown files with YAML front matter
(the same structure is used for WordPress posts: title, meta_title, description, slug, lang,
hreflang_pl / hreflang_en, date, category, sources). FAQ = '## FAQ' section with **Q:** / A: pairs.
Sources: _src/seo_0511/BLOG/ (SEO agent), fallback _src/content/blog/."""
import re, yaml, markdown, html
from pathlib import Path

SRC = Path(__file__).parent
DIRS = [SRC / "seo_0511" / "BLOG", SRC / "content" / "blog"]
SOURCE = None
_CACHE = None

IMG_BY_KEY = [("obsolete", "gauges"), ("wycofan", "gauges"), ("bom", "cabinet"), ("lead", "breakers"), ("czasy", "breakers"),
              ("export", "export"), ("eksport", "export"), ("ship", "export")]

def _img(slug):
    for k, v in IMG_BY_KEY:
        if k in slug:
            return v
    return "cabinet"

def _norm(p):
    return p.strip().strip("/") + "/"

def _parse(f):
    raw = f.read_text(encoding="utf-8").replace("\r\n", "\n").replace("sales@gpenergia.com.pl", "info@gpenergia.com.pl")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        return None
    fm = yaml.safe_load(m.group(1)) or {}
    body = m.group(2).strip()
    body = body.replace("—", "-").replace("–", "-")
    h1 = fm.get("title", "")
    mh = re.match(r"^#\s+(.+)\n", body)
    if mh:
        h1 = mh.group(1).strip(); body = body[mh.end():].strip()
    # FAQ
    faq = []
    mf = re.search(r"^##\s+(FAQ|Frequently asked questions|Najczęstsze pytania|Pytania i odpowiedzi|FAQ.*)\s*$", body, re.M | re.I)
    if mf:
        faq_txt = body[mf.end():]
        nxt = re.search(r"^##\s+", faq_txt, re.M)
        rest = ""
        if nxt:
            rest = faq_txt[nxt.start():]; faq_txt = faq_txt[:nxt.start()]
        body = body[:mf.start()].rstrip() + ("\n\n" + rest if rest else "")
        for q, a in re.findall(r"\*\*(?:Q|P|Pytanie):\s*(.+?)\*\*\s*\n+(?:A|O|Odpowiedź):\s*(.+?)(?=\n\s*\n|\Z)", faq_txt, re.S):
            faq.append((q.strip(), " ".join(a.split())))
        if not faq:  # ### question / paragraph answer
            for q, a in re.findall(r"^###\s+(.+?)\n+(.+?)(?=\n###|\Z)", faq_txt, re.S | re.M):
                faq.append((q.strip(), " ".join(a.split())))
    # lead = first paragraph
    paras = body.split("\n\n")
    lead = ""
    if paras and not paras[0].lstrip().startswith(("#", "-", "|", "1.")):
        lead = " ".join(paras[0].split()); body = "\n\n".join(paras[1:])
    lang = fm.get("lang", "en")
    path = _norm(fm.get("slug", ""))
    alt = fm.get("hreflang_pl") if lang == "en" else fm.get("hreflang_en")
    words = len(re.findall(r"\w+", raw))
    return {"lang": lang, "path": path, "alt_path": _norm(alt) if alt else None, "slug": path.rstrip("/").split("/")[-1],
            "title": (fm.get("meta_title") or fm.get("title") or h1).strip(), "title_h": (fm.get("title") or h1).strip(),
            "h1": h1, "desc": (fm.get("description") or "").strip(), "excerpt": (fm.get("description") or lead)[:220],
            "date": str(fm.get("date", "2026-11-05")), "modified": str(fm.get("updated", fm.get("date", "2026-11-05"))),
            "category": fm.get("category", ""),
            "sources": [x for x in (fm.get("sources") or []) if not re.search(r"himtek|client|klient|own data|dane własne|concept", str(x), re.I)],
            "md": body, "lead": lead, "faq": faq, "mins": max(2, round(words / 200)), "img": _img(path)}

def _to_html(md_text, rel):
    md_text = re.sub(r"\]\((/[^)]*)\)", lambda m: "](" + rel(m.group(1).lstrip("/")) + ")", md_text)
    h = markdown.markdown(md_text, extensions=["tables", "sane_lists"])
    toc = []
    def add_id(m):
        txt = re.sub("<[^>]+>", "", m.group(1))
        slug = re.sub(r"[^a-z0-9]+", "-", txt.lower().translate(str.maketrans("ąćęłńóśźż", "acelnoszz"))).strip("-")[:60]
        toc.append((slug, html.unescape(txt)))
        return f'<h2 id="{slug}">{m.group(1)}</h2>'
    h = re.sub(r"<h2>(.*?)</h2>", add_id, h)
    h = h.replace("<table>", '<div class="tbl-scroll" tabindex="0"><table>').replace("</table>", "</table></div>")
    return h, toc

def load():
    """returns list of {'en': post, 'pl': post} complete pairs"""
    global SOURCE, _CACHE
    for d in DIRS:
        files = sorted(d.glob("*.md")) if d.exists() else []
        if files:
            SOURCE = str(d.relative_to(SRC)); break
    else:
        _CACHE = []; return []
    posts = [p for p in (_parse(f) for f in files) if p]
    by_path = {p["path"]: p for p in posts}
    pairs = []
    for p in posts:
        if p["lang"] != "en":
            continue
        q = by_path.get(p["alt_path"] or "")
        if q:
            q["alt_path"] = p["path"]
            pairs.append({"en": p, "pl": q})
    pairs.sort(key=lambda x: x["en"]["date"], reverse=True)
    _CACHE = pairs
    return pairs

def render_html(post, rel):
    h, toc = _to_html(post["md"], rel)
    if post["sources"]:
        lab = "Sources" if post["lang"] == "en" else "Źródła"
        items = "".join(f"<li>{html.escape(str(s))}</li>" for s in post["sources"])
        h += f'<section class="art-sources"><h2 id="sources">{lab}</h2><ul>{items}</ul></section>'
        toc.append(("sources", lab))
    return h, toc

def posts(lang):
    global _CACHE
    if _CACHE is None:
        load()
    return [p[lang] for p in _CACHE]
