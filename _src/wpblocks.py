# -*- coding: utf-8 -*-
"""HTML from the Markdown articles -> WordPress block markup (editable in the block editor)."""
import re, html

TOP = re.compile(r"<(p|h2|h3|h4|ul|ol|div|blockquote|table|hr|figure|section)\b[^>]*?/?>", re.I)

def _split(h):
    out, i = [], 0
    while True:
        m = TOP.search(h, i)
        if not m:
            break
        tag = m.group(1).lower()
        if tag == "hr" or m.group(0).endswith("/>"):
            out.append((tag, m.group(0))); i = m.end(); continue
        depth, j = 0, m.start()
        pat = re.compile(r"<(/?)%s\b[^>]*>" % tag, re.I)
        for t in pat.finditer(h, m.start()):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                j = t.end(); break
        out.append((tag, h[m.start():j])); i = j
    return out

def _inner(el, tag):
    return re.sub(r"^<%s\b[^>]*>|</%s>$" % (tag, tag), "", el.strip(), flags=re.I).strip()

def _list(el, tag):
    items = re.findall(r"<li>(.*?)</li>", el, re.S)
    ordered = tag == "ol"
    lis = "".join(f"<!-- wp:list-item -->\n<li>{x.strip()}</li>\n<!-- /wp:list-item -->\n" for x in items)
    attrs = ' {"ordered":true}' if ordered else ""
    return f'<!-- wp:list{attrs} -->\n<{tag} class="wp-block-list">{lis}</{tag}>\n<!-- /wp:list -->'

def para(t):
    return f"<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->"

def heading(t, level=2):
    a = "" if level == 2 else ' {"level":%d}' % level
    return f'<!-- wp:heading{a} -->\n<h{level} class="wp-block-heading">{t}</h{level}>\n<!-- /wp:heading -->'

def convert(h):
    blocks = []
    for tag, el in _split(h):
        if tag == "p":
            blocks.append(para(_inner(el, "p")))
        elif tag in ("h2", "h3", "h4"):
            blocks.append(heading(_inner(el, tag), int(tag[1])))
        elif tag in ("ul", "ol"):
            blocks.append(_list(el, tag))
        elif tag == "div" and "<table" in el:
            t = re.search(r"<table>.*?</table>", el, re.S).group(0)
            blocks.append(f'<!-- wp:table -->\n<figure class="wp-block-table">{t}</figure>\n<!-- /wp:table -->')
        elif tag == "blockquote":
            inner = "".join(para(_inner(x, "p")) for _, x in _split(_inner(el, "blockquote")))
            blocks.append(f'<!-- wp:quote -->\n<blockquote class="wp-block-quote">{inner}</blockquote>\n<!-- /wp:quote -->')
        elif tag == "hr":
            blocks.append('<!-- wp:separator -->\n<hr class="wp-block-separator has-alpha-channel-opacity"/>\n<!-- /wp:separator -->')
        else:
            blocks.append(f"<!-- wp:html -->\n{el}\n<!-- /wp:html -->")
    return "\n\n".join(blocks)

def faq(items, title):
    if not items:
        return ""
    out = [heading(html.escape(title))]
    for q, a in items:
        out.append(f'<!-- wp:details -->\n<details class="wp-block-details"><summary>{html.escape(q)}</summary>{para(a)}</details>\n<!-- /wp:details -->')
    return "\n\n".join(out)

def sources(items, title):
    if not items:
        return ""
    lis = "".join(f"<!-- wp:list-item -->\n<li>{html.escape(s)}</li>\n<!-- /wp:list-item -->\n" for s in items)
    return heading(html.escape(title)) + "\n\n" + f'<!-- wp:list -->\n<ul class="wp-block-list">{lis}</ul>\n<!-- /wp:list -->'
