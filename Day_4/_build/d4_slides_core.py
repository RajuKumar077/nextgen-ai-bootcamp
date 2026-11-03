# Day 4 slide builder · CORE: helpers + facts computed from the REAL MCP server and the real data files.
# Nothing a slide calls "exact" is typed by hand: it is produced here by the same code the notebooks run.
import json
import os
import re
import sys
import tempfile

BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
sys.path.insert(0, BUILD + "/engine")
import d4_common as C                                                                    # noqa: E402
from deck import Deck, theme_vars, esc, me, neo, chat, msg, life_ai, UI, DISP, MONO      # noqa: E402,F401
from mcp_client import McpClient                                                         # noqa: E402

DAY4, C7, C8 = C.DAY4, C.C7, C.C8

# ------------------------------------------------------------------------------------------ facts (computed, never typed)
_tmp = tempfile.mkdtemp()


def _server(*flags):
    return McpClient([sys.executable, C.SERVER, "--tickets", os.path.join(_tmp, "tickets.jsonl")] + list(flags))


P = _server()                                              # the default server (read-only, 6 tools): what the notebook starts in CELL S
W = _server("--allow-write", "--with-scorecard")           # all tools, writes enabled (for the scorecard and the approval demo)


def inr(n):                                                # Indian digit grouping: 1200000 -> ₹12,00,000
    s = str(int(n)); head, tail = s[:-3], s[-3:]
    head = re.sub(r"(\d)(?=(\d\d)+$)", r"\1,", head)
    return "₹" + (head + "," + tail if head else tail)


assert inr(1200000) == "₹12,00,000" and inr(85000) == "₹85,000" and inr(125000) == "₹1,25,000" and inr(2700000) == "₹27,00,000"

INFO, PROTOCOL, CAPS = P.server_info, P.protocol, list(P.capabilities)
TOOLS = P.list_tools()
TOOLS_W = W.list_tools()
T_NAMES = [t["name"] for t in TOOLS]
assert T_NAMES == ["list_orders", "get_order", "get_vendor", "check_approval", "delayed_summary", "create_ticket"]
assert len(TOOLS_W) == 7 and [t["name"] for t in TOOLS_W if t["name"] not in T_NAMES] == ["vendor_scorecard"]
READONLY = {t["name"]: t["annotations"]["readOnlyHint"] for t in TOOLS}
assert [n for n, v in READONLY.items() if not v] == ["create_ticket"]


def args_of(t): return ", ".join(t["inputSchema"]["properties"])


BLOCKED_1000 = P.call_tool("list_orders", {"plant": "1000", "status": "Blocked"})["data"]["orders"]
assert [o["po_number"] for o in BLOCKED_1000] == ["4500012345", "4500012348", "4500012352", "4500012355"]
DELAYED_2000 = P.call_tool("list_orders", {"plant": "2000", "status": "Delayed"})["data"]["orders"]
assert [o["po_number"] for o in DELAYED_2000] == ["4500012349", "4500012351"]
ORDER = {po: P.call_tool("get_order", {"po_number": po})["data"] for po in ("4500012345", "4500012346", "4500012347", "4500012348", "4500012350", "4500012355")}
VENDOR = {v: P.call_tool("get_vendor", {"vendor_id": v})["data"] for v in ("V100", "V200", "V300", "V400")}
APPR = {v: P.call_tool("check_approval", {"value_inr": v})["data"] for v in (85000, 750000, 1200000)}
assert [APPR[v]["approver"] for v in (85000, 750000, 1200000)] == ["Line Manager", "Department Head", "Director"]
NOT_FOUND = P.call_tool("get_order", {"po_number": "4500099999"})
assert not NOT_FOUND["ok"] and NOT_FOUND["data"] == "PO 4500099999 not found."
DELAYED = P.call_tool("delayed_summary")["data"]
assert DELAYED == {"Bharat Logistics": {"delayed_pos": 2, "total_value_inr": 1200000}, "Chennai Components": {"delayed_pos": 2, "total_value_inr": 1500000}}
TOP_DELAY = max(DELAYED, key=lambda v: DELAYED[v]["total_value_inr"])
SCORE = W.call_tool("vendor_scorecard")["data"]
TOP_VENDOR = max(SCORE, key=lambda v: SCORE[v]["total_value_inr"])
assert (TOP_VENDOR, SCORE[TOP_VENDOR]["total_value_inr"], SCORE[TOP_VENDOR]["delayed"], SCORE[TOP_VENDOR]["blocked"]) == ("Chennai Components", 2700000, 2, 1)
SUMMARY = json.loads(P.read_resource("orders://summary"))
RESOURCES, PROMPTS = P.list_resources(), P.list_prompts()
PROMPT_TXT = P.get_prompt("blocked_orders_report", {"plant": "1000"})
POLICY_RES = P.read_resource("policy://approval-limits")
assert SUMMARY["by_status"] == {"Blocked": 4, "Delayed": 4, "Open": 2, "Delivered": 2} and len(RESOURCES) == 3 and len(PROMPTS) == 2

P.wire.clear()                                             # the two real messages behind one tool call (CELL 4)
P.call_tool("check_approval", {"value_inr": 1200000})
WIRE = list(P.wire)
assert [d for d, _ in WIRE] == ["→", "←"]

# the guardrails: run the NOTEBOOK's own agent code (menu + gate + executor) against the real server, with no model involved
_ns = {"json": json, "re": re, "os": os, "client": P}
C.run_src(C.AGENT_DEFAULTS_SRC + "\n" + C.MENU_SRC + "\n" + C.LOOP_SRC, _ns)
G1 = _ns["execute"]({"tool": "create_ticket", "args": {"po_number": "4500012345", "note": "Chase the credit check"}})
assert "Blocked by a guardrail" in G1["error"]
_ns["ALLOWED"] = {"get_order", "check_approval"}
G2_MENU = list(_ns["offered"]())
G2 = _ns["execute"]({"tool": "list_orders", "args": {}})
assert G2_MENU == ["get_order", "check_approval"] and "Unknown tool 'list_orders'" in G2["error"]
_ns["ALLOWED"] = None
G3 = _ns["execute"]({"tool": "delete_purchase_order", "args": {"po_number": "4500012345"}})
G4 = _ns["execute"]({"tool": "get_order", "args": {"order": "4500012345"}})
assert "Unknown tool" in G3["error"] and "Unexpected argument" in G4["error"]
SYSTEM_PROMPT = _ns["system_prompt"]()
assert all(f"- {n}(" in SYSTEM_PROMPT for n in T_NAMES)

# human approval: the notebook's APPROVAL_SRC, once with "yes" and once with "no", against the server with writes enabled
_ns2 = {"json": json, "re": re, "os": os, "client": W}
C.run_src(C.AGENT_DEFAULTS_SRC + "\n" + C.MENU_SRC + "\n" + C.LOOP_SRC + "\n" + C.APPROVAL_SRC, _ns2)
import contextlib, io                                      # noqa: E402,E401
REQ = {"tool": "create_ticket", "args": {"po_number": "4500012345", "note": "Chase the credit check"}}
os.environ["BOOTCAMP_AUTO_APPROVE"] = "yes"
with contextlib.redirect_stdout(io.StringIO()):
    APPROVED = _ns2["execute"](REQ)
os.environ["BOOTCAMP_AUTO_APPROVE"] = "no"
with contextlib.redirect_stdout(io.StringIO()):
    DECLINED = _ns2["execute"](REQ)
del os.environ["BOOTCAMP_AUTO_APPROVE"]
assert APPROVED["ticket_id"] == "TCK-0001" and "Blocked by a guardrail" in DECLINED["error"]
assert not os.path.exists(os.path.join(_tmp, "tickets.jsonl")) or len(open(os.path.join(_tmp, "tickets.jsonl")).read().strip().splitlines()) == 1   # "no" created nothing

PLAIN85 = P.call_tool("check_approval", {"value_inr": 85000})["data"]

# the knowledge side (Class 8)
CHUNKS = C.chunk_all()
DOCW = {n: C.word_count(C.DOCS + "/" + n) for n in sorted(os.listdir(C.DOCS)) if n.endswith(".txt")}
TOTAL_WORDS = sum(DOCW.values())
CLAUSE = {c["id"]: c for c in CHUNKS}
C62 = CLAUSE["Procurement_Policy §6.2"]
C33 = CLAUSE["Procurement_Policy §3.3"]
assert len(CHUNKS) == 39 and len(DOCW) == 4 and "price variance above 1%" in C62["text"]
ORD48 = ORDER["4500012348"]
assert (ORD48["status"], ORD48["block_reason"], ORD48["value_inr"], ORD48["vendor_id"]) == ("Blocked", "Price variance", 1200000, "V300")
assert (APPR[1200000]["approver"], VENDOR["V300"]["contact"]) == ("Director", "Lakshmi Iyer")


# ------------------------------------------------------------------------------------------ html helpers (same as Day 3)
def lead(t, extra=""): return '<p class="lead f"' + (' style="' + extra + '"' if extra else "") + ">" + t + "</p>"
def body(*parts): return '<div class="body">' + "".join(parts) + "</div>"
def slide(title, *parts): return "<h2>" + title + "</h2>" + body(*parts)


def card(title, text="", emoji=None, cls="", center=False, num=None):
    st = ' style="text-align:center"' if center else ""
    return ('<div class="card ' + cls + ' f"' + st + ">" + ('<div class="num">' + num + "</div>" if num else "") +
            ('<div class="emoji">' + emoji + "</div>" if emoji else "") + "<h3>" + title + "</h3>" + ("<p>" + text + "</p>" if text else "") + "</div>")


def grid(n, *items, style=""): return '<div class="g' + str(n) + '"' + (' style="' + style + '"' if style else "") + ">" + "".join(items) + "</div>"


def exp(kind="model"):
    """Honest labels. Exact = produced by running the notebook's own code on the data / the real MCP server. Target = what we expect; your model's wording will differ."""
    if kind == "exact":
        return '<p class="expect f">Exact output of the notebook cell · no AI involved</p>'
    if kind == "model":
        return '<p class="expect warn f">Target answer · your model\'s wording will differ</p>'
    return '<p class="expect warn f">' + kind + "</p>"


def exact(kind): return '<p class="expect f">' + kind + "</p>"


def table(head, rows, cls="sheet f", mono=()):
    th = "".join("<th>" + h + "</th>" for h in head)
    tr = "".join("<tr>" + "".join(('<td class="mono">' if i in mono else "<td>") + c + "</td>" for i, c in enumerate(r)) + "</tr>" for r in rows)
    return '<table class="' + cls + '"><tr>' + th + "</tr>" + tr + "</table>"


def blank(t=""): return '<td class="blank">' + (t or "&nbsp;") + "</td>"


def trace(rows):
    lab = {"think": "Think", "act": "Act", "obs": "Observe", "fin": "Answer"}
    return '<div class="trace">' + "".join('<div class="tr2 f"><span class="lab2 ' + k + '">' + lab[k] + "</span><span>" + t + "</span></div>" for k, t in rows) + "</div>"


def mono(t): return '<span class="mono">' + t + "</span>"


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
def steps(items):
    """The numbered 'do' list used on the Your-turn slides: items = [(title, text), ...]."""
    return "".join('<div class="do f"><div class="n">' + str(i) + '</div><div><h3>' + t + "</h3><p>" + p + "</p></div></div>" for i, (t, p) in enumerate(items, 1))


# ------------------------------------------------------------------------------------------ extra CSS (Day 4 components)
EXTRA_CSS = """
.pipe{display:flex;flex-direction:column;gap:9px}
.pipe .pr{display:grid;grid-template-columns:210px 1fr;gap:20px;align-items:center;background:var(--card);border:1px solid var(--hair);border-radius:18px;padding:10px 20px;font-size:22px;line-height:1.35;box-shadow:inset 0 1px 0 var(--gloss),0 10px 26px var(--cardsh)}
.pipe .pr.two{grid-template-columns:210px 1fr 1fr}
.pipe .pc{font:700 13px @UI@;letter-spacing:.09em;text-transform:uppercase;color:var(--accent);background:var(--acc-s);border-radius:999px;padding:7px 12px;text-align:center}
.pipe .pr.end{background:var(--grad);color:#fff;border:0}
.pipe .pr.end .pc{background:rgba(255,255,255,.24);color:#fff}
.pipe .sub{background:var(--seg);border-radius:12px;padding:7px 14px;font-size:20px}
.chunk{background:var(--card);border:1px solid var(--hair);border-radius:28px;box-shadow:inset 0 1px 0 var(--gloss),0 22px 50px var(--cardsh);overflow:hidden}
.chunk .ch{display:flex;gap:12px;align-items:center;padding:16px 26px;background:var(--seg);font:600 15px @UI@;color:var(--muted)}
.chunk .ch b{color:var(--accent);font-family:@MONO@}
.chunk .cb{padding:22px 28px;font-size:25px;line-height:1.5}
.chunk .cb .tg{color:var(--accent);font:600 18px @MONO@}
.wire{font:600 17px/1.5 @MONO@;word-break:break-all}
.ro,.rw{display:inline-block;font:700 12px @UI@;letter-spacing:.08em;text-transform:uppercase;border-radius:999px;padding:4px 10px}
.ro{background:var(--ok-s);color:var(--ok)} .rw{background:var(--warn-s);color:var(--warn)}
.agentbox{display:grid;grid-template-columns:1fr 1.15fr 1fr;gap:18px;align-items:stretch}
.agentbox .mid{background:var(--grad);color:#fff;border:0} .agentbox .mid h3,.agentbox .mid p{color:#fff}
"""

HINT = '<div class="hint">Press <kbd>→</kbd> next <kbd>F</kbd> fullscreen <kbd>T</kbd> theme <kbd>P</kbd> presenter <kbd>K</kbd> fit check <kbd>?</kbd> help</div>'


def divnote(nxt): return "Section divider. Next comes a key-terms slide: say the names first, then run the demos. " + nxt


# Class 7 = light, orange -> pink -> violet.  Class 8 = dark, green -> blue -> gold.   (Day 3 was light teal/blue and dark violet/cyan.)
THEME7 = theme_vars("#c2410c", "linear-gradient(90deg,#ff8a00 0%,#ff4d6d 52%,#a855f7 100%)", "#ffb066", "linear-gradient(90deg,#ffb340 0%,#ff6a8a 52%,#c084fc 100%)",
                    "255,138,0", "168,85,247", "#fbf7f4", "#0a0706", "194,65,12", "255,176,102",
                    "linear-gradient(135deg,#ffb340 0%,#ff4d6d 55%,#a855f7 100%)", "rgba(255,77,109,.38)", "rgba(90,40,10,.085)")
THEME8 = theme_vars("#0b7a5a", "linear-gradient(90deg,#10b981 0%,#0a84ff 52%,#f59e0b 100%)", "#5ee0a8", "linear-gradient(90deg,#34d399 0%,#4aa3ff 52%,#fbbf24 100%)",
                    "16,185,129", "245,158,11", "#f3f9f6", "#050a08", "11,122,90", "94,224,168",
                    "linear-gradient(135deg,#34d399 0%,#4aa3ff 55%,#fbbf24 100%)", "rgba(52,211,153,.38)", "rgba(10,60,40,.085)")


def new_deck(label, sub, theme, key, default):
    from deck import fonts
    return Deck(label, "Neo", sub, theme, key, default, EXTRA_CSS)


def close_servers():
    for c in (P, W):
        try:
            c.close()
        except Exception:
            pass
