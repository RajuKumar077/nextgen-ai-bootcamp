"""Builds one instructor script page per class (self-contained HTML), from the finished decks + instructor_scripts.py.
Titles, parts, cell numbers and the key-term cards are read FROM THE DECK, so the page cannot drift from the slides.
Run after the decks are built:   python build_instructor.py
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DAY4 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from instructor_scripts import C7, C8  # noqa: E402

CLASSES = [
    dict(n=7, folder="Class_7_MCP_Guardrails", deck="Class_7_Agents_In_Action_Slides.html", out="Class_7_Instructor_Script.html", scripts=C7,
         title="Class 7 · Tools, MCP & Guardrails", sub="Instructor script · Day 4 morning · about 2 hours", accent="#0a84ff", accent2="#30b0c7",
         prep=["Ollama running; open the Class 7 notebook, pick the <b>.venv</b> kernel, run <b>CELL S</b>.",
               "Run <code>python setup/make_mcp_config.py</code> once, so Antigravity and VS Code can see the MCP server.",
               "Rehearse both live demos once (<code>antigravity/TASK.md</code>). Use the menu names you actually see. Keep a backup recording.",
               "Antigravity sends prompts to a cloud model: get approval first. Mock data only."]),
    dict(n=8, folder="Class_8_Capstone", deck="Class_8_Putting_It_All_Together_Slides.html", out="Class_8_Instructor_Script.html", scripts=C8,
         title="Class 8 · Putting It All Together", sub="Instructor script · Day 4 afternoon · about 2 hours", accent="#bf5af2", accent2="#ff6482",
         prep=["Ollama running; open the Class 8 notebook, pick the <b>.venv</b> kernel, run <b>CELL S</b>.",
               "Check NotebookLM and Antigravity are approved for mock data, or tell teams to use the notebook cells instead.",
               "Prepare 5 minutes per team for the pitches, plus a timer. Share <code>capstone/CAPSTONE_GUIDE.md</code> and <code>pitch_card.md</code>.",
               "Have <code>ROADMAP.md</code> ready for the close."]),
]


def clean(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()


def parse_deck(path):
    text = open(path, encoding="utf-8").read()
    secs = re.findall(r'<section class="([^"]*)" data-section="([^"]*)">(.*?)</section>', text, re.S)
    out = []
    for i, (cls, sec, body) in enumerate(secs, 1):
        body = re.sub(r'<aside class="notes">.*?</aside>', "", body, flags=re.S)
        cell = re.search(r'data-cell="([^"]+)"', body)
        h = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S) if ("div" in cls.split() or "title" in cls.split()) else None
        h = h or re.search(r"<h2[^>]*>(.*?)</h2>", body, re.S) or re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S) or re.search(r'class="(?:big|bigq)[^"]*"[^>]*>(.*?)</', body, re.S)
        kind = "terms" if 'class="terms' in body else ("div" if "div" in cls.split() else "title" if "title" in cls.split() else "slide")
        title = clean(h.group(1)) if h else ""
        if not title:                                                      # comparison slides have no heading, only a side label
            k = re.search(r'<div class="k">(.*?)</div>', body, re.S)
            title = clean(k.group(1)) + " (SAP comparison)" if k else ""
        lead = re.search(r'<p class="lead"[^>]*>(.*?)</p>', body, re.S)
        terms = []
        for t in re.findall(r'<div class="term f">(.*?)</div></div>|<div class="term f">(.*?)</div>\s*(?=<div class="term f">|</div>)', body, re.S):
            pass
        for m in re.finditer(r'<div class="tname">(.*?)</div><p class="tdef">(.*?)</p><div class="tsap"><span class="tlab">.*?</span>(.*?)</div>', body, re.S):
            terms.append((clean(m.group(1)), clean(m.group(2)), clean(m.group(3))))
        code = re.search(r'class="divtc">(.*?)</div>', body, re.S)
        out.append(dict(i=i, sec=sec, kind=kind, title=title, cell=cell.group(1) if cell else None, lead=clean(lead.group(1)) if lead else "",
                        terms=terms, code=clean(code.group(1)) if code else ""))
    return out


CSS = """
:root{--bg:#f5f5f7;--card:#fff;--ink:#1d1d1f;--mut:#6e6e73;--line:#e5e5ea;--acc:@A@;--acc2:@A2@;--say:#f0f7ff;--do:#fff6e5;--dobar:#ff9f0a;--code:#f2f2f7;--shadow:0 1px 3px rgba(0,0,0,.06)}
html[data-theme=dark]{--bg:#000;--card:#1c1c1e;--ink:#f5f5f7;--mut:#a1a1a6;--line:#38383a;--say:#0f2236;--do:#2b2210;--code:#2c2c2e;--shadow:none}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:70px}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 -apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",system-ui,Helvetica,Arial,sans-serif}
header.top{position:sticky;top:0;z-index:20;display:flex;gap:12px;align-items:center;padding:10px 20px;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
header.top b{font-size:15px}header.top .sp{flex:1}
button{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;padding:5px 11px;cursor:pointer}
button:hover{border-color:var(--acc)}
.wrap{display:grid;grid-template-columns:260px 1fr;gap:28px;max-width:1220px;margin:0 auto;padding:24px 20px 80px}
nav.side{position:sticky;top:64px;align-self:start;max-height:calc(100vh - 80px);overflow:auto;font-size:14px;padding-right:6px}
nav.side h4{margin:16px 0 4px;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
nav.side a{display:flex;gap:8px;color:var(--ink);text-decoration:none;padding:3px 8px;border-radius:6px;line-height:1.35}
nav.side a:hover{background:var(--card)}nav.side a .n{color:var(--mut);min-width:24px;font-variant-numeric:tabular-nums}
nav.side a.done{opacity:.45}
.hero{background:linear-gradient(135deg,var(--acc),var(--acc2));color:#fff;border-radius:20px;padding:30px 32px;margin-bottom:22px}
.hero h1{margin:0 0 4px;font-size:30px;letter-spacing:-.02em}.hero p{margin:0;opacity:.92}
.box{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 22px;margin-bottom:22px;box-shadow:var(--shadow)}
.box h3{margin:0 0 8px;font-size:16px}.box ul{margin:0;padding-left:20px}.box li{margin:4px 0}
code{background:var(--code);padding:1px 6px;border-radius:5px;font:14px ui-monospace,"SF Mono",Menlo,Consolas,monospace}
h2.part{margin:36px 0 12px;font-size:13px;letter-spacing:.09em;text-transform:uppercase;color:var(--acc)}
article.s{background:var(--card);border:1px solid var(--line);border-radius:16px;margin-bottom:14px;box-shadow:var(--shadow);overflow:hidden}
article.s>summary,article.s .hd{display:flex;gap:12px;align-items:center;padding:12px 18px;cursor:pointer;list-style:none}
article.s summary::-webkit-details-marker{display:none}
.num{flex:none;width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,var(--acc),var(--acc2));color:#fff;font-weight:700;font-size:14px;display:grid;place-items:center}
.ttl{font-weight:650;font-size:18px;flex:1;line-height:1.3}
.pill{font-size:12px;font-weight:600;padding:3px 10px;border-radius:99px;background:var(--code);color:var(--mut);white-space:nowrap}
.pill.cell{background:var(--acc);color:#fff}
.body{padding:2px 20px 18px}
.say{background:var(--say);border-left:4px solid var(--acc);border-radius:10px;padding:10px 16px;margin:6px 0 10px}
.say .k,.do .k{display:block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--acc);margin-bottom:2px}
.say p{margin:6px 0}
.do{background:var(--do);border-left:4px solid var(--dobar);border-radius:10px;padding:8px 16px;font-size:15px}
.do .k{color:var(--dobar)}
.terms{width:100%;border-collapse:collapse;margin:6px 0 10px;font-size:15px}
.terms th{text-align:left;font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--mut);padding:4px 8px;border-bottom:1px solid var(--line)}
.terms td{padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}.terms td:first-child{font-weight:650;white-space:nowrap}
.divr{border-left:5px solid var(--acc)}
label.chk{display:flex;gap:6px;align-items:center;font-size:12px;color:var(--mut);cursor:pointer;margin-left:6px}
footer{color:var(--mut);font-size:13px;text-align:center;margin-top:40px}
@media(max-width:900px){.wrap{grid-template-columns:1fr}nav.side{display:none}}
@media print{header.top,nav.side,label.chk,button{display:none!important}.wrap{display:block;padding:0}body{background:#fff;color:#000;font-size:12px}
 article.s{break-inside:avoid;box-shadow:none}.hero{color:#000;background:#eee}details>*{display:block!important}}
"""

JS = """
const KEY='d4Instr@N@';const root=document.documentElement;
const th=localStorage.getItem(KEY+'Theme');if(th)root.dataset.theme=th;else if(matchMedia('(prefers-color-scheme: dark)').matches)root.dataset.theme='dark';
document.getElementById('tg').onclick=()=>{const d=root.dataset.theme==='dark'?'light':'dark';root.dataset.theme=d;localStorage.setItem(KEY+'Theme',d)};
document.getElementById('pr').onclick=()=>{document.querySelectorAll('details').forEach(d=>d.open=true);window.print()};
const all=document.querySelectorAll('details.s');
document.getElementById('ex').onclick=()=>{const o=[...all].some(d=>!d.open);all.forEach(d=>d.open=o);document.getElementById('ex').textContent=o?'Collapse all':'Expand all'};
const done=JSON.parse(localStorage.getItem(KEY+'Done')||'{}');
function paint(){document.querySelectorAll('nav.side a').forEach(a=>a.classList.toggle('done',!!done[a.dataset.n]));
 const c=Object.values(done).filter(Boolean).length;document.getElementById('prog').textContent=c+' / '+all.length+' covered'}
document.querySelectorAll('input.dn').forEach(i=>{i.checked=!!done[i.dataset.n];i.onclick=e=>{e.stopPropagation();done[i.dataset.n]=i.checked;localStorage.setItem(KEY+'Done',JSON.stringify(done));paint()}});
document.querySelectorAll('label.chk').forEach(l=>l.onclick=e=>e.stopPropagation());
paint();
"""


def render(c):
    deck = parse_deck(os.path.join(DAY4, c["folder"], "slides", c["deck"]))
    S = c["scripts"]
    missing = [d["i"] for d in deck if d["kind"] != "terms" and d["i"] not in S]
    # dividers can be covered by the generic line; anything else missing is an error
    for d in deck:
        if d["kind"] == "div" and d["i"] not in S:
            S[d["i"]] = ([f"{d['code']}: {d['title']}. {d['lead']}"], "")
    missing = [d["i"] for d in deck if d["kind"] != "terms" and d["i"] not in S]
    extra = [k for k in S if k > len(deck) or deck[k - 1]["kind"] == "terms"]
    assert not missing, f"Class {c['n']}: no script for slides {missing}"
    assert not extra, f"Class {c['n']}: script written for non-existent or key-terms slides {extra}"

    sections, order = [], []
    for d in deck:
        if d["sec"] not in order:
            order.append(d["sec"])
    nav, body = [], []
    for sec in order:
        nav.append(f"<h4>{html.escape(sec)}</h4>")
        body.append(f'<h2 class="part" id="p-{abs(hash(sec)) % 99999}">{html.escape(sec)}</h2>')
        for d in [x for x in deck if x["sec"] == sec]:
            title = d["title"] or ("Key terms" if d["kind"] == "terms" else "Slide")
            nav.append(f'<a href="#s{d["i"]}" data-n="{d["i"]}"><span class="n">{d["i"]}</span><span>{html.escape(title)}</span></a>')
            pills = (f'<span class="pill cell">Run CELL {html.escape(d["cell"])}</span>' if d["cell"] else "")
            if d["kind"] == "div":
                pills += '<span class="pill">Part opener</span>'
            if d["kind"] == "terms":
                rows = "".join(f"<tr><td>{html.escape(n)}</td><td>{html.escape(df)}</td><td>{html.escape(sp)}</td></tr>" for n, df, sp in d["terms"])
                say = ('<p>Teach the names first, about two minutes. Say each term aloud and ask the room to repeat it. Then give the plain meaning and the example from the card. '
                       "Do not go deeper yet: the demos come next, and each demo slide carries a term tag in the top-left corner.</p>")
                inner = (f'<div class="say"><span class="k">Say</span>{say}</div><table class="terms"><tr><th>Term</th><th>Plain meaning (read from the slide)</th><th>In your SAP world</th></tr>{rows}</table>'
                         '<div class="do"><span class="k">Do</span>Say each name, pause, let the room repeat it. Move on after about two minutes.</div>')
            else:
                say, do = S[d["i"]]
                inner = '<div class="say"><span class="k">Say</span>' + "".join(f"<p>{p}</p>" for p in say) + "</div>"
                if do:
                    inner += f'<div class="do"><span class="k">Do</span>{do}</div>'
            cls = "s divr" if d["kind"] == "div" else "s"
            body.append(f'<details class="{cls}" id="s{d["i"]}" open><summary class="hd"><span class="num">{d["i"]}</span><span class="ttl">{html.escape(title)}</span>{pills}'
                        f'<label class="chk"><input type="checkbox" class="dn" data-n="{d["i"]}"> covered</label></summary><div class="body">{inner}</div></details>')
    prep = "".join(f"<li>{p}</li>" for p in c["prep"])
    page = (f'<!DOCTYPE html>\n<html lang="en" data-theme="light"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{c["title"]}: instructor script</title>'
            f'<style>{CSS.replace("@A@", c["accent"]).replace("@A2@", c["accent2"])}</style></head><body>'
            f'<header class="top"><b>{c["title"]}</b><span class="sp"></span><span id="prog" class="pill"></span><button id="ex">Collapse all</button><button id="tg">Light / dark</button><button id="pr">Print</button></header>'
            f'<div class="wrap"><nav class="side">{"".join(nav)}</nav><main>'
            f'<div class="hero"><h1>{c["title"]}</h1><p>{c["sub"]} · {len(deck)} slides</p></div>'
            f'<div class="box"><h3>Before you start</h3><ul>{prep}</ul></div>'
            f'<div class="box"><h3>How to use this page</h3><ul><li><b>Say</b> is what you can read or paraphrase. <b>Do</b> is an action, a question for the room, or a cell to run.</li>'
            f'<li>Slide numbers match the deck. A blue <b>Run CELL</b> pill matches the pill on the slide and the <code># ▶ CELL n</code> header in the notebook.</li>'
            f'<li>Numbers marked <i>exact</i> on the slides come from the data and the real server. For model answers, say: <i>"your model will word it differently."</i></li>'
            f'<li>Tick <b>covered</b> as you go (saved in this browser). <b>Print</b> gives a paper copy.</li></ul></div>'
            f'{"".join(body)}<footer>Mock data only · Nova Industries is fictional · generated from the deck, so the titles and cell numbers always match</footer></main></div>'
            f'<script>{JS.replace("@N@", str(c["n"]))}</script></body></html>')
    assert page.count("<details") == page.count("</details>")
    path = os.path.join(DAY4, c["folder"], "slides", c["out"])
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
    return path, len(deck), len(S), sum(1 for d in deck if d["kind"] == "terms")


if __name__ == "__main__":
    for c in CLASSES:
        p, n, s, t = render(c)
        print(f"Class {c['n']}: {n} slides ({s} scripted + {t} key-terms generated) → {os.path.relpath(p, DAY4)}")
