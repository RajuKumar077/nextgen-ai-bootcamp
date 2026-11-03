"""
deck.py · the slide engine for the bootcamp decks (same look, presenter view and keys as Day 3), as a clean module.
The CSS and JavaScript live next to this file (base_vars.css, components.css, tail.tpl): they were taken from the finished Day 3 deck.

    deck = Deck("Class 7", "Neo", "Day 4 · Morning", theme_css, "d4Class7Theme", "light")
    deck.add(section, html, notes, kind=None, cell=None)      # one slide
    deck.divider("Part A", "Name", "Headline", "Lead", section, notes)   # divider + the key-terms slide(s) for that part
    deck.write("File.html", "Title", outdir)
"""
import html as _html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
UI = '-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI Variable Text","Segoe UI",system-ui,"Helvetica Neue",Arial,"Segoe UI Emoji","Apple Color Emoji",sans-serif'
DISP = '-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI Variable Display","Segoe UI",system-ui,"Helvetica Neue",Arial,sans-serif'
MONO = '"SF Mono",ui-monospace,"Cascadia Mono","Cascadia Code",Consolas,Menlo,monospace'


def _read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


def fonts(css):
    return css.replace("@UI@", UI).replace("@DISP@", DISP).replace("@MONO@", MONO)


# ───────────────────────────── small html pieces used by the slides ─────────────────────────────
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def me(t):
    return '<div class="bub me f"><div class="av">You</div><div class="tx">' + t + "</div></div>"


def neo(t, kind=""):
    return '<div class="bub neo ' + kind + ' f"><div class="av">N</div><div class="tx">' + t + "</div></div>"


def chat(*bubbles):
    return '<div class="chat">' + "".join(bubbles) + "</div>"


def msg(kind, t):
    glyph = {"s": "✓", "e": "✕", "w": "!", "n": "i"}[kind]
    return '<div class="msg ' + kind + '"><span class="i">' + glyph + "</span><span>" + t + "</span></div>"


def life_ai(left, right, k1="In real life", k2="With Neo"):
    return ('<div class="vs"><div class="side life f"><div class="k">' + k1 + "</div>" + left + '</div><div class="side ai f"><div class="k">' + k2 + "</div>" + right + "</div></div>")


def theme_vars(accent_l, grad_l, accent_d, grad_d, glow1, glow2, mesh_l, mesh_d, rgb_l, rgb_d, orb, orbsh, shadow_l):
    """CSS variables for one deck. The light block also targets html[data-theme="light"] so it beats the neutral defaults."""
    def glows(a, b, base):
        return ("radial-gradient(1000px 560px at 100% 0%,rgba(" + a + ",.20),transparent 62%),"
                "radial-gradient(900px 520px at 0% 100%,rgba(" + b + ",.14),transparent 60%)," + base)
    light = glows(glow1, glow2, mesh_l)
    dark = glows(glow1, glow2, mesh_d)
    return (':root,html[data-theme="light"]{--accent:' + accent_l + ";--acc-s:rgba(" + rgb_l + ",.10);--grad:" + grad_l + ";--live:" + accent_l + ";--live-s:rgba(" + rgb_l + ",.2);"
            "--divbg:radial-gradient(900px 600px at 82% 18%,rgba(" + glow1 + ",.32),transparent 62%),radial-gradient(800px 520px at 8% 100%,rgba(" + glow2 + ",.22),transparent 60%),#000;"
            "--titlebg:" + light.replace(".20)", ".12)").replace(".14)", ".09)") + ";--mesh:" + light.replace(".20)", ".13)").replace(".14)", ".10)") + ";"
            "--tile:linear-gradient(135deg,rgba(" + glow1 + ",.18),rgba(" + glow2 + ",.16));--acc-line:rgba(" + rgb_l + ",.34);--orb:" + orb + ";--orbsh:" + orbsh + ";--gloss:rgba(255,255,255,.85);--cardsh:" + shadow_l + "}\n"
            'html[data-theme="dark"]{--accent:' + accent_d + ";--acc-s:rgba(" + rgb_d + ",.15);--grad:" + grad_d + ";--live:" + accent_d + ";--live-s:rgba(" + rgb_d + ",.25);"
            "--titlebg:" + dark + ";--mesh:" + dark.replace(".20)", ".26)").replace(".14)", ".17)") + ";"
            "--tile:linear-gradient(135deg,rgba(" + rgb_d + ",.24),rgba(" + glow2 + ",.20));--acc-line:rgba(" + rgb_d + ",.42);--orb:" + orb + ";--orbsh:" + orbsh + ";--gloss:rgba(255,255,255,.07);--cardsh:rgba(0,0,0,.55)}\n")


# ───────────────────────────── the deck ─────────────────────────────
class Deck:
    def __init__(self, label, obj, sub, theme_css, theme_key, default_theme, extra_css=""):
        self.label, self.obj, self.sub = label, obj, sub
        self.theme_css, self.theme_key, self.default_theme, self.extra_css = theme_css, theme_key, default_theme, extra_css
        self.items, self.terms, self.tags, self.part_titles = [], {}, [], {}
        self.term_total = 0

    # one ordinary slide. kind: None | "title" (title slide) ; cell: notebook cell tag shown top-right
    def add(self, section, html, notes="", kind=None, cell=None):
        self.items.append({"section": section, "html": html, "notes": notes, "kind": kind, "cell": cell})

    def divider(self, code, kname, headline, lead, section, notes):
        self.items.append({"section": section, "kind": "div", "cell": None, "notes": notes,
                           "html": '<div class="divgrid"><div class="divtc">' + code + '</div><div><div class="divk">' + kname + "</div><h1>" + headline +
                                   '</h1><p class="lead" style="margin-top:0">' + lead + "</p></div></div>"})
        for title, terms in self.terms.get(code, []):
            cards = ""
            for name, definition, sap, cell in terms:
                self.term_total += 1
                cards += ('<div class="term f"><div class="tmeta"><span class="tno">Term ' + str(self.term_total).zfill(2) + '</span><span class="tcell">' +
                          (("Notebook · Cell " + str(cell)) if cell else "Concept") + '</span></div><div class="tname">' + name + '</div><p class="tdef">' + definition +
                          '</p><div class="tsap"><span class="tlab">In your world</span>' + sap + "</div></div>")
            n = min(len(terms), 4)
            cols = "c" + str(max(n, 2) if n != 3 else 3)
            names = ", ".join(t[0] for t in terms)
            self.items.append({"section": section, "kind": "terms", "cell": None,
                               "html": '<h2 style="margin-bottom:28px">' + title + '</h2><div class="body"><div class="terms ' + cols + '">' + cards + "</div></div>",
                               "notes": "<b>Teach the names first (about 2 minutes).</b> Say each term aloud and ask the room to repeat it. Give the plain meaning, then the example from the card. "
                                        "Don't go deeper yet: the demos come next and each one carries a term tag in the top-left corner. Terms on this slide: " + names + "."})

    # ── assembling the page ──
    @staticmethod
    def _title(h):
        m = re.search(r"<h2[^>]*>(.*?)</h2>", h, re.S)
        return _html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip().lower() if m else ""

    def _apply_tags(self):
        used = set()
        for it in self.items:
            if it["kind"] in ("div", "terms", "title"):
                continue
            title = self._title(it["html"])
            for frag, term in self.tags:
                if frag in title:
                    it["html"] = '<div class="termtag"><b>Key term</b>' + term + "</div>" + it["html"]
                    used.add(frag)
                    break
        unused = [f for f, _ in self.tags if f not in used]
        if unused:
            raise ValueError("Term tags that matched no slide title: " + str(unused))

    def write(self, fname, title, outdir):
        self._apply_tags()
        if self.items:                                                     # "N key terms" pill on the cover
            first = self.items[0]
            first["html"] = first["html"].replace('<span class="pill">', '<span class="pill hl">' + str(self.term_total) + ' key terms</span><span class="pill">', 1)
        sections = []
        for i, it in enumerate(self.items):
            cls = "slide title cover" if i == 0 else ("slide div" if it["kind"] == "div" else ("slide title" if it["kind"] == "title" else "slide "))
            cmd = ('<span class="box" data-cell="' + str(it["cell"]) + '"><small>Notebook</small>Cell ' + str(it["cell"]) + "</span>") if it["cell"] else '<span class="tc">' + self.sub + "</span>"
            notes = it["notes"]
            if it["cell"]:
                notes = "<b>▶ Run CELL " + str(it["cell"]) + "</b> · " + notes
            sections.append('<section class="' + cls + '" data-section="' + it["section"] + '"><div class="shell"><span class="obj">' + self.obj + '</span><span class="sep">›</span><span class="sec">' +
                            self.label + " · " + it["section"] + '</span><span class="cmd">' + cmd + "</span></div>\n" + it["html"] + '\n<aside class="notes">' + notes + "</aside>\n</section>")
        tail = _read("tail.tpl").replace("{{THEME_KEY}}", self.theme_key).replace("{{DEFAULT_THEME}}", self.default_theme).replace("{{LABEL}}", self.label)
        css = _read("base_vars.css") + self.theme_css + _read("components.css") + fonts(self.extra_css)
        page = ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>' + title + "</title><style>" + css +
                "</style></head><body>\n<div id=\"deck\">\n<div id=\"progress\"></div>\n" + "\n".join(sections) + '\n<div class="foot"><span id="sec"></span><span id="num"></span></div>\n</div>\n\n' + tail)
        assert "{{" not in page, "unfilled placeholder"
        os.makedirs(outdir, exist_ok=True)
        path = os.path.join(outdir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        return path, len(self.items)
