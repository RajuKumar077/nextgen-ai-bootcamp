# Day 3 slide builder · CORE: engine + helpers + facts computed from the real data files.
# The engine (Apple-style look, presenter view, term tags, key-term slides) is reused from the Day 2 v6 builder.
import os, re, sys, csv, html as _html

DAY3 = os.path.expanduser("~/Desktop/Day_3")
V6 = "/Users/ra20586957wipro.com/Documents/Enchanté/Conversations/DC7FB73D-48DB-4ECB-884F-FD8CEBF33240/_build/day2_slides_v6_terms.py"
os.environ["OUT_DIR"] = DAY3 + "/Class_5_RAG/slides/"
_v6 = open(V6, encoding="utf-8").read()
exec(_v6[:_v6.index("# 4. BUILD both decks")])          # engine, BASE, TAIL, Deck hooks, TERMS/TAGS/EXTRA dicts, helpers

sys.path.insert(0, DAY3 + "/_build")
import day3_common as C

# ------------------------------------------------------------------------------------------ facts (computed, never typed)
ORD = list(csv.DictReader(open(DAY3 + "/Class_6_Agents/data/orders.csv", encoding="utf-8")))
VEN = {r["vendor_id"]: r for r in csv.DictReader(open(DAY3 + "/Class_6_Agents/data/vendors.csv", encoding="utf-8"))}
PO = {r["po_number"]: r for r in ORD}
def inr(n):                     # Indian digit grouping: 1200000 -> 12,00,000
    s = str(int(n)); head, tail = s[:-3], s[-3:]
    head = re.sub(r"(\d)(?=(\d\d)+$)", r"\1,", head)
    return "₹" + (head + "," + tail if head else tail)
assert inr(1200000) == "₹12,00,000" and inr(85000) == "₹85,000" and inr(3420000) == "₹34,20,000"

CH = {p: C.pack_chunks(p) for p in "ABC"}
DOCW = {n: C.words(C.DOCS + "/" + n) for n in os.listdir(C.DOCS)}
TOTAL_WORDS = sum(DOCW.values())
POLICY_WORDS = DOCW["Procurement_Policy.txt"]
C33 = next(c for c in CH["A"] if c["id"].endswith("Procurement_Policy §3.3"))
C33_WORDS = len(C33["text"].split())

STOP = set("a an the of to is are who what which and or in on for do does it be by at as from that this with must".split())
def _w(t): return set(re.findall(r"[a-z0-9]+", t.lower())) - STOP
def kw(question, top=3):
    q = _w(question); sc = sorted(((len(q & _w(c["text"])), c) for c in CH["A"]), key=lambda s: -s[0])
    return [(s, c["id"]) for s, c in sc[:top] if s > 0]
KW1 = kw("Who approves a PO above 10 lakh?"); KW2 = kw("Who signs off on really big orders?")
assert KW1[:2] == [(3, "Procurement_Policy §3.2"), (3, "Procurement_Policy §3.3")] and KW2 == [(1, "Procurement_Policy §2.1")], (KW1, KW2)

DELAYED = {}
for r in ORD:
    if r["status"] == "Delayed":
        d = DELAYED.setdefault(r["vendor_name"], [0, 0]); d[0] += 1; d[1] += int(r["value_inr"])
PLANT = {}
for r in ORD:
    d = PLANT.setdefault(r["plant"], [0, 0]); d[0] += 1; d[1] += int(r["value_inr"])
VTOTAL = {}
for r in ORD: VTOTAL[r["vendor_name"]] = VTOTAL.get(r["vendor_name"], 0) + int(r["value_inr"])
TOP_VENDOR = max(VTOTAL, key=VTOTAL.get)
BLOCKED = [(r["po_number"], r["vendor_name"], r["block_reason"]) for r in ORD if r["status"] == "Blocked"]
assert DELAYED == {"Bharat Logistics": [2, 1200000], "Chennai Components": [2, 1500000]} and PLANT == {"1000": [7, 3420000], "2000": [5, 1295000]}

def tool_status(po):
    r = PO[po]; return {"status": r["status"], "block_reason": r["block_reason"] or None, "value": inr(r["value_inr"]), "vendor_id": r["vendor_id"]}
def tool_vendor(po):
    v = VEN[PO[po]["vendor_id"]]; return v
def policy(v): return ("Line Manager", "3.1") if v <= 100000 else (("Department Head", "3.2") if v <= 1000000 else ("Director", "3.3"))

# ------------------------------------------------------------------------------------------ html helpers
def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def lead(t, extra=""): return '<p class="lead f"' + (' style="' + extra + '"' if extra else "") + ">" + t + "</p>"
def body(*parts): return '<div class="body">' + "".join(parts) + "</div>"
def slide(title, *parts, center=False): return "<h2>" + title + "</h2>" + body(*parts)
def card(title, text="", emoji=None, cls="", center=False, num=None):
    st = ' style="text-align:center"' if center else ""
    return ('<div class="card ' + cls + ' f"' + st + ">" + ('<div class="num">' + num + "</div>" if num else "") +
            ('<div class="emoji">' + emoji + "</div>" if emoji else "") + "<h3>" + title + "</h3>" + ("<p>" + text + "</p>" if text else "") + "</div>")
def grid(n, *items, style=""): return '<div class="g' + str(n) + '"' + (' style="' + style + '"' if style else "") + ">" + "".join(items) + "</div>"
def exp(kind="model"):
    """Honest labels: the Day 3 slides never claim a recorded model run. Exact = code output; target = what the document says."""
    if kind == "exact":
        return '<p class="expect f">Exact output of the notebook cell · no AI involved</p>'
    if kind == "model":
        return '<p class="expect warn f">Target answer, taken from the document · your model\'s wording will differ</p>'
    return '<p class="expect warn f">' + kind + "</p>"
def table(head, rows, cls="sheet f", mono=()):
    th = "".join("<th>" + h + "</th>" for h in head)
    tr = "".join("<tr>" + "".join(('<td class="mono">' if i in mono else "<td>") + c + "</td>" for i, c in enumerate(r)) + "</tr>" for r in rows)
    return '<table class="' + cls + '"><tr>' + th + "</tr>" + tr + "</table>"
def blank(t=""): return '<td class="blank">' + (t or "&nbsp;") + "</td>"
def trace(rows):
    lab = {"think": "Think", "act": "Act", "obs": "Observe", "fin": "Answer"}
    return '<div class="trace">' + "".join('<div class="tr2 f"><span class="lab2 ' + k + '">' + lab[k] + "</span><span>" + t + "</span></div>" for k, t in rows) + "</div>"

_KW = r"\b(def|return|for|in|if|else|import|from|not|and|or|try|except|with|as|print)\b"
def pycode(src, hl=()):
    out = []
    for i, line in enumerate(src.strip("\n").split("\n")):
        e = esc(line); m = re.search(r"(^|\s)#", e)
        code, com = (e[:m.start() + len(m.group(1))], e[m.start() + len(m.group(1)):]) if m else (e, "")
        code = re.sub(r'("[^"]*")|' + _KW, lambda g: '<span class="st">' + g.group(1) + "</span>" if g.group(1) else '<span class="kw">' + g.group(2) + "</span>", code)
        s = code + ('<span class="cm">' + com + "</span>" if com else "")
        out.append('<span class="hl">' + s + "</span>" if i in hl else s)
    return '<pre class="abap f">' + "\n".join(out) + "</pre>"
def qa(q, a, kind=""): return chat(me(q), neo(a, kind))

# ------------------------------------------------------------------------------------------ extra CSS (Day 3 components)
BASE += """
.expect{display:flex;align-items:center;gap:9px;font:600 16px @UI@;color:var(--muted);margin-top:14px}
.expect::before{content:"";width:9px;height:9px;border-radius:50%;background:var(--ok);box-shadow:0 0 0 4px var(--ok-s)}
.expect.warn::before{background:var(--warn);box-shadow:0 0 0 4px var(--warn-s)}
.trace{display:flex;flex-direction:column;gap:10px}
.trace .tr2{display:grid;grid-template-columns:128px 1fr;gap:18px;align-items:center;background:var(--card);border:1px solid var(--hair);border-radius:20px;padding:12px 20px;font-size:21px;line-height:1.38;box-shadow:inset 0 1px 0 var(--gloss),0 12px 30px var(--cardsh)}
.lab2{font:700 13px @UI@;letter-spacing:.1em;text-transform:uppercase;border-radius:999px;padding:7px 12px;text-align:center}
.lab2.think{background:var(--acc-s);color:var(--accent)} .lab2.act{background:var(--warn-s);color:var(--warn)}
.lab2.obs{background:var(--ok-s);color:var(--ok)} .lab2.fin{background:var(--grad);color:#fff}
.trace .mono{font-size:18px}
.pairs{display:grid;grid-template-columns:1fr 1fr;gap:26px}
.say{background:var(--seg);border-radius:20px;padding:20px 26px;font-size:22px;line-height:1.45}
.say b{color:var(--accent)}
.do{display:flex;gap:16px;align-items:flex-start;margin:0 0 14px}
.do .n{flex:0 0 46px;height:46px;border-radius:50%;background:var(--grad);color:#fff;font:700 21px @DISP@;display:flex;align-items:center;justify-content:center}
.do h3{font-size:24px;margin:0 0 2px} .do p{font-size:19px;color:var(--muted);margin:0}
.no li,.yes li{font-size:22px;margin:0 0 9px;list-style:none;padding-left:34px;position:relative} .no,.yes{padding:0;margin:0}
.yes li::before{content:"✓";position:absolute;left:0;color:var(--ok);font-weight:700} .no li::before{content:"✕";position:absolute;left:0;color:var(--bad);font-weight:700}
""".replace("@UI@", UI).replace("@DISP@", DISP)

def theme_vars(accent_l, grad_l, accent_d, grad_d, glow1, glow2, mesh_l, mesh_d, rgb_l, rgb_d, orb, orbsh, shadow_l):
    def glows(a, b, base): return ("radial-gradient(1000px 560px at 100% 0%,rgba(" + a + ",.20),transparent 62%),"
                                   "radial-gradient(900px 520px at 0% 100%,rgba(" + b + ",.14),transparent 60%)," + base)
    return (":root{--accent:" + accent_l + ";--acc-s:rgba(" + rgb_l + ",.10);--grad:" + grad_l + ";--live:" + accent_l + ";--live-s:rgba(" + rgb_l + ",.2);"
            "--divbg:radial-gradient(900px 600px at 82% 18%,rgba(" + glow1 + ",.32),transparent 62%),radial-gradient(800px 520px at 8% 100%,rgba(" + glow2 + ",.22),transparent 60%),#000;"
            "--titlebg:" + glows(glow1, glow2, mesh_l).replace(".20)", ".12)").replace(".14)", ".09)") + ";--mesh:" + glows(glow1, glow2, mesh_l).replace(".20)", ".13)").replace(".14)", ".10)") + ";"
            "--tile:linear-gradient(135deg,rgba(" + glow1 + ",.18),rgba(" + glow2 + ",.16));--acc-line:rgba(" + rgb_l + ",.34);--orb:" + orb + ";--orbsh:" + orbsh + ";--gloss:rgba(255,255,255,.85);--cardsh:" + shadow_l + "}\n"
            'html[data-theme="dark"]{--accent:' + accent_d + ";--acc-s:rgba(" + rgb_d + ",.15);--grad:" + grad_d + ";--live:" + accent_d + ";--live-s:rgba(" + rgb_d + ",.25);"
            "--titlebg:" + glows(glow1, glow2, mesh_d) + ";--mesh:" + glows(glow1, glow2, mesh_d).replace(".20)", ".26)").replace(".14)", ".17)") + ";"
            "--tile:linear-gradient(135deg,rgba(" + rgb_d + ",.24),rgba(" + glow2 + ",.20));--acc-line:rgba(" + rgb_d + ",.42);--orb:" + orb + ";--orbsh:" + orbsh + ";--gloss:rgba(255,255,255,.07);--cardsh:rgba(0,0,0,.55)}\n")

# Class 5 = light, teal → blue.  Class 6 = dark, violet → cyan.
EXTRA["Class 5"] = theme_vars("#00778f", "linear-gradient(90deg,#00b3a4 0%,#0a84ff 52%,#6e5bff 100%)", "#4fd8e6", "linear-gradient(90deg,#3be0cf 0%,#4aa3ff 52%,#9d8cff 100%)",
                              "0,179,164", "10,132,255", "#f4f8fa", "#04080a", "0,150,170", "79,216,230",
                              "linear-gradient(135deg,#3be0cf 0%,#0a84ff 55%,#7a5cff 100%)", "rgba(10,132,255,.36)", "rgba(10,50,80,.085)")
EXTRA["Class 6"] = theme_vars("#5b46e6", "linear-gradient(90deg,#6e56ff 0%,#0a84ff 52%,#00b3a4 100%)", "#a99bff", "linear-gradient(90deg,#8e7bff 0%,#3b9bff 50%,#35e0c4 100%)",
                              "110,86,255", "0,179,164", "#f6f5fc", "#06050c", "91,70,230", "169,155,255",
                              "linear-gradient(135deg,#8e7bff 0%,#3b9bff 55%,#35e0c4 100%)", "rgba(110,86,255,.42)", "rgba(40,20,90,.09)")

HINT = '<div class="hint">Press <kbd>→</kbd> next <kbd>F</kbd> fullscreen <kbd>T</kbd> theme <kbd>P</kbd> presenter <kbd>K</kbd> fit check <kbd>?</kbd> help</div>'
def divnote(nxt): return "Section divider. Next comes a key-terms slide: say the names first, then run the demos. " + nxt

def finish(deck, fname, title, theme, key, outdir):
    global OUT
    OUT = outdir; os.makedirs(outdir, exist_ok=True)
    deck.write(fname, title, theme)
    p = outdir + fname; h = open(p, encoding="utf-8").read()
    h = h.replace("localStorage.getItem('deckTheme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')", "localStorage.getItem('" + key + "')||'" + ("light" if deck.label == "Class 5" else "dark") + "'")
    h = h.replace("localStorage.setItem('deckTheme',", "localStorage.setItem('" + key + "',")
    assert key in h
    open(p, "w", encoding="utf-8").write(h)
