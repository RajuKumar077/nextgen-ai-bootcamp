# Class 7 slides · "Agents in Action: Tools, MCP & Guardrails" · light theme, orange -> pink -> violet
# Every value labelled "exact" below comes from d4_slides_core, which RUNS the notebook's own code against the real MCP server.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d4_slides_core import *          # noqa: F401,F403,E402

D = new_deck("Class 7", "Day 4 · Morning", THEME7, "d4Class7Theme", "light")


# ------------------------------------------------------------------------------------------ small computed pieces
def short(desc, n=56):
    s = re.split(r"[.:]", desc)[0].strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


def badge(name): return '<span class="ro">read-only</span>' if READONLY[name] else '<span class="rw">changes data</span>'


def last3(po): return "…" + po[-3:]


def reason(o): return (o["block_reason"] or o["status"]).lower()


CHANGING = [n for n, v in READONLY.items() if not v]
AGENTS, SYSTEMS = 4, 5
assert (AGENTS * SYSTEMS, AGENTS + SYSTEMS) == (20, 9)
assert "Stopped: step limit reached" in C.LOOP_SRC and "Approved by a person" in C.APPROVAL_SRC and "Declined. Nothing was changed" in C.APPROVAL_SRC
BLOCKED_LINE = " · ".join(last3(o["po_number"]) + " " + o["block_reason"] for o in BLOCKED_1000)
BLOCKED_ANS = ", ".join(o["po_number"] + " (" + reason(o) + ", " + inr(o["value_inr"]) + ")" for o in BLOCKED_1000)
ASK_ARGS = repr(REQ["args"]).replace("'", '"')

# ------------------------------------------------------------------------------------------ key terms
D.terms = {
 "Part A": [("Key terms: the plug", [
    ("MCP", "Model Context Protocol: one standard way for AI apps to connect to systems and data. \"USB-C for AI\": any agent, any system.", "Standard interfaces: IDoc, OData, RFC.", "1"),
    ("MCP server", "A small program in front of a system. It offers the system's data and actions in the standard MCP shape.", "An OData service on top of a system.", "S"),
    ("MCP client", "The part of an AI app that connects to servers: our notebook, Antigravity, VS Code.", "The system that consumes the service.", "S"),
    ("Discovery", "The client asks the server what it offers (tools/list). Nobody types the menu by hand.", "Reading the service metadata.", "1")])],
 "Part B": [("Key terms: the 3 things a server offers", [
    ("Tool", "An action the AI may request, such as check an order or create a ticket. The program runs it.", "A BAPI or function module.", "2"),
    ("Resource", "Data to read: an order list, a report, a policy text. It is read, not run.", "A report or a table view.", "3"),
    ("Prompt", "A ready-made request the server offers, with blanks to fill in, such as the blocked-orders report for a plant.", "A saved variant.", "3")]),
  ("Key terms: under the bonnet", [
    ("JSON message", "What really travels between client and server: a plain-text request and a plain-text result. No magic.", "An IDoc: a structured message.", "4"),
    ("Read-only label", "Every tool says whether it only reads or can change data. A program can use the label to decide when to ask a person.", "Display or change authorisation.", "2")])],
 "Part C": [("Key terms: the agent over MCP", [
    ("Plug and play", "Add a tool to the server and every connected agent can use it. No agent code changes.", "A new service in the gateway.", "7"),
    ("Gate", "The check between \"the AI asked\" and \"the program runs it\". It is plain code, so the AI cannot talk its way past it.", "An authority check.", "6")])],
 "Part D": [("Key terms: guardrails (1 of 2)", [
    ("Guardrail", "A limit built into the program, not into the prompt. It keeps an agent safe whatever the model decides.", "The authorisation concept.", "8"),
    ("Read-only first", "Start with tools that cannot change anything. Add a tool that changes data only when it is needed.", "Display before change.", "8"),
    ("Human approval", "A person says yes before any change. The agent waits.", "A release strategy.", "9")]),
  ("Key terms: guardrails (2 of 2)", [
    ("Allow-list", "The agent gets only the tools it needs. Anything else is refused.", "A role with only the needed transactions.", "8"),
    ("Step limit", "A maximum number of passes through the loop, so an agent cannot run forever.", "A timeout on a background job.", "8"),
    ("Plain automation", "A fixed, rule-based process written as ordinary code. No model, so it is cheaper, faster and easier to audit.", "A scheduled job or a workflow rule.", "10")])],
 "Part E": [("Key terms: using agents well", [
    ("Multi-agent", "Several specialist agents that each do one part of a job and hand over to each other. An overview today, not something we build.", "A team of consultants.", None),
    ("Tool choice", "Which tool the agent picks for a question. You note it in the hands-on, because it tells you why the answer is right or wrong.", "The transaction you opened first.", "11")])],
}
D.tags = [("mcp in one picture", "MCP"), ("typed by hand", "Discovery"), ("how does the agent know", "Discovery"), ("cell 1:", "Discovery"), ("neo runs on", "MCP server"),
  ("every tool has a label", "Read-only label"), ("message, not a crash", "Tool"), ("three things", "Tool"), ("tool, resource or prompt", "Resource"), ("cell 3: resources", "Resource"), ("cell 3: prompts", "Prompt"),
  ("on the wire", "JSON message"), ("cell 5:", "Discovery"), ("request, check", "Gate"), ("cell 6:", "Gate"), ("plug and play", "Plug and play"), ("the new tool answers", "Plug and play"),
  ("four guardrails", "Guardrail"), ("sit between", "Guardrail"), ("cell 8:", "Allow-list"), ("cell 9:", "Human approval"), ("release strategy", "Human approval"), ("make it ask first", "Human approval"),
  ("when not to use", "Plain automation"), ("cell 10:", "Plain automation"), ("multi-agent", "Multi-agent"), ("cell 11:", "Tool choice"), ("worksheet", "Tool choice")]

# ------------------------------------------------------------------------------------------ START
A = "Start"
D.add(A, """<div class="body"><div class="label" style="color:var(--accent)">Day 4 · Class 7 · Tools, MCP &amp; guardrails</div>
<h1><span class="mono">Neo</span><br>plugs in</h1>
<p class="lead" style="margin-top:0">Yesterday Neo used three tools that <b>we</b> wired in by hand. Today we meet the <b>standard plug</b> that connects agents to any system, and the <b>guardrails</b> that keep them safe.</p>
<div><span class="pill">MCP: USB-C for AI</span><span class="pill">Guardrails</span><span class="pill">Live demo: Antigravity + MCP</span><span class="pill">Runs on your laptop</span></div></div>""" + HINT,
 "Before class: open Day_4/Class_7_MCP_Guardrails/notebooks/Class_7_Agents_In_Action.ipynb, choose the .venv kernel and run CELL S. Optional: run setup/make_mcp_config.py once so Antigravity and VS Code can see the MCP server for the live demo.", "title")
D.add(A, slide("Yesterday in 30 seconds", grid(3, card("4 parts of an agent", "Brain · Tools · Memory · Instructions.", "🧩"), card("The loop", "Think → Act → Observe → Repeat.", "🔁"),
  card("AI decides, system executes", "Only the tools we allow.", "🔒")), lead("Neo can <b>act</b>. But those three tools were <b>hand-built for one agent</b>. A real company has dozens of systems.")), "Quick recap of Class 6.")
D.add(A, slide("The scaling problem", grid(3,
  '<div class="card bad f" style="text-align:center"><div class="num">' + str(AGENTS * SYSTEMS) + '</div><h3>custom connections</h3><p>' + str(AGENTS) + " agents × " + str(SYSTEMS) + " systems, each wired by hand</p></div>",
  '<div class="card ok f" style="text-align:center"><div class="num">' + str(AGENTS + SYSTEMS) + '</div><h3>with one standard plug</h3><p>' + str(AGENTS) + " + " + str(SYSTEMS) + ": each side plugs in once</p></div>",
  '<div class="card acc f" style="text-align:center"><div class="emoji">🔌</div><h3>SAP solved this before</h3><p>IDoc · OData · RFC: standard shapes</p></div>'),
  lead("If every new system needs its own custom connection, <b>it does not scale</b>.")),
 "Count it on the board: 4 agents and 5 systems means 20 pieces of custom work. With a standard plug each side connects once: 9. SAP people already know this idea from IDoc, OData and RFC.")
D.add(A, """<div class="hero"><div class="orb">Neo</div><div><div class="label" style="color:var(--accent)">Neo, plugged in</div><h2 style="margin-bottom:18px">One plug. Safe hands.</h2>
<p class="f">🔌 <b>One standard plug</b> to any system</p><p class="f">🔎 Tools <b>discovered</b>, not typed</p><p class="f">🛡️ <b>Guardrails</b> around every change</p><p class="f">🙋 A <b>person approves</b> changes</p></div></div>""",
 "Neo is still the same character. What changes is how Neo connects to systems, and how we keep that safe.")
D.add(A, """<div class="body center"><div class="big">One standard <em>plug</em>.<br>A few simple <em>guardrails</em>.</div>
<p class="lead f">That is MCP. By the end of the class you will connect an agent, watch it use tools, and make it stop and ask.</p></div>""", "The one idea for the morning. Pause here.")
D.add(A, """<h2>Today's plan · 2 hours</h2><div class="body"><table class="agenda">
<tr><th>Time</th><th>Topic</th><th>Question</th><th>Cells</th></tr>
<tr><td class="t">0:00</td><td>A · The problem and the plug</td><td>What is MCP?</td><td class="m">S, 1</td></tr>
<tr><td class="t">0:15</td><td>B · The 3 things a server offers</td><td>What can a system give an agent?</td><td class="m">2–4</td></tr>
<tr><td class="t">0:35</td><td>C · The agent over MCP</td><td>What changes in the agent?</td><td class="m">5–7</td></tr>
<tr><td class="t">0:55</td><td>D · Guardrails</td><td>How do we keep it safe?</td><td class="m">8–10</td></tr>
<tr><td class="t">1:20</td><td>E · Your turn</td><td>Five business questions</td><td class="m">11–12</td></tr></table></div>""", "Part D has the guardrail demo. Part E is 40 minutes of hands-on.")
D.add(A, slide("Neo runs on this laptop", '<div class="g2" style="align-items:center">' + card("Same set-up as yesterday, plus a server", "The agent uses the <b>chat model</b>. This time the tools sit behind a small <b>MCP server</b>: " + mono("sap_orders_server.py") + ", a Python file the trainer prepared. It reads " + mono("orders.csv") + " and " + mono("vendors.csv") + ".", "💻") +
  '<div class="f">' + msg("s", "Ollama is running · main model found") + '<div style="height:12px"></div>' + msg("s", "Neo replies <b>Connection OK</b>") + '<div style="height:12px"></div>' +
  msg("s", "Connected to MCP server: <b>" + INFO["title"] + "</b> (v" + INFO["version"] + ")") + "</div></div>"), "The cell starts the server as a child process and shakes hands with it.", cell="S")

# ------------------------------------------------------------------------------------------ PART A
BA = "A · The plug"
D.divider("Part A", "The plug", "One plug for everything", "MCP: USB-C for AI.", BA, divnote("Part A has one demo: connect and discover."))
D.add(BA, life_ai("<div class='emoji'>🔌</div><p>SAP has no custom cable to every other system. It uses <b>standard interfaces</b> (IDoc, OData, RFC).</p><p>A new system plugs into a <b>known shape</b>.</p>",
                  "<div class='emoji'>🤖</div><p>Agents had the same problem: a custom connection for every system.</p><p><b>MCP</b> is the standard shape for AI: one plug, any system.</p>", "In your SAP world", "For agents"), "Use the SAP comparison first. People already trust standard interfaces.")
D.add(BA, slide("MCP in one picture", '<div class="agentbox"><div class="card f"><h3>AI apps</h3><p>MCP <b>clients</b><br>Our notebook<br>Antigravity<br>VS Code</p></div>' +
  '<div class="card mid f" style="text-align:center"><div class="emoji">🔌</div><h3>MCP</h3><p>One standard plug.<br>Tools · Resources · Prompts</p></div>' +
  '<div class="card f"><h3>Systems</h3><p>MCP <b>servers</b><br>Mock SAP orders<br>Documents<br>Tickets</p></div></div>', lead("Any client can use any server that speaks the standard. <b>Nobody builds the pair twice.</b>")),
 "Walk left to right. The notebook, Antigravity and VS Code are all MCP clients. Our mock SAP is one MCP server.")
D.add(BA, slide("Cell 1: connect, then discover", '<div class="g2" style="align-items:start">' + pycode('''print(client.server_info["title"])
print(client.protocol)
tools = client.list_tools()
for t in tools:
    print(" •", t["name"])''', (2,)) +
  '<div class="out f"><div class="who">Notebook output · exact</div>Server: <b>' + esc(INFO["title"]) + "</b> · version " + INFO["version"] + "<br>Protocol: " + PROTOCOL + "<br>Offers: " + mono(esc(str(CAPS))) +
  "<br><br><b>" + str(len(TOOLS)) + " tools discovered:</b><br>" + "<br>".join("• " + mono(n) for n in T_NAMES) + "</div></div>", exp("exact")),
 "Run CELL 1. The server tells us its name, its protocol version and what it offers. Then tools/list: nobody typed these six names.", cell=1)
D.add(BA, slide("Yesterday typed by hand, today discovered", table(["", "Class 6 (yesterday)", "Class 7 (today)"], [
  ["The tool menu", "Typed in the notebook: " + mono("TOOLS = {…}"), "Asked from the server: " + mono("list_tools()")],
  ["Add a tool", "Edit the notebook", "<b>Edit the server only</b>"], ["Who can use it", "This one agent", "<b>Any MCP client</b>"], ["Change data?", "Not labelled", "Every tool says: <b>read-only</b> or not"]]),
  lead("Same loop, same idea. <b>The plumbing is now standard.</b>")), "Contrast Cell 3 of Class 6 with Cell 5 of today.")
D.add(BA, slide("How does the agent know what exists?", '<div class="flow"><div class="st f"><h3>1 · Client asks</h3><p>' + mono("tools/list") + "<br>\"What do you offer?\"</p></div><div class=\"ar f\">→</div>" +
  '<div class="st f"><h3>2 · Server answers</h3><p>For each tool: <b>name</b>, <b>description</b>, <b>inputs</b>, <b>read-only label</b></p></div><div class="ar f">→</div>' +
  '<div class="st f"><h3>3 · Menu is built</h3><p>The agent\'s instructions list exactly these tools</p></div></div>', lead("This is <b>discovery</b>. Add a tool to the server and it appears on the menu by itself.")), "The descriptions matter: they are what the model reads to choose a tool.", cell=1)

# ------------------------------------------------------------------------------------------ PART B
BB = "B · Three things"
D.divider("Part B", "Three things", "What does a server offer?", "Tools · Resources · Prompts.", BB, divnote("Three demos: tools, resources and prompts, and one call on the wire."))
D.add(BB, slide("A server offers three things", grid(3, card("Tools", "Actions the AI may request: check a status, create a ticket.", "🛠️", "acc"), card("Resources", "Data to read: order lists, reports, policy text.", "📚", "acc"),
  card("Prompts", "Ready-made requests the server offers, with blanks to fill.", "💬", "acc")), lead("Read, do, or ask in a saved way. <b>Three shapes, one standard.</b>")), "Say the three words and give one example each from the order system.")
D.add(BB, slide("The SAP comparison", table(["MCP word", "Say this", "SAP comparison"], [
  ["🛠️ Tool", "An action the AI may request.", "A BAPI or function module"], ["📚 Resource", "Data to read.", "A report or a table view"], ["💬 Prompt", "A saved, ready-made request.", "A transaction variant"],
  ["🖥️ Server", "Offers the three things.", "An OData service"], ["🤖 Client", "Uses what the server offers.", "The consuming system"]]), ), "Each row links an MCP word to something SAP people already know.")
D.add(BB, slide("Cell 2: every tool has a label", '<div class="out f"><div class="who">Notebook output · exact</div>' +
  "<br>".join(badge(t["name"]) + " " + mono(t["name"] + "(" + args_of(t) + ")") for t in TOOLS) + "</div>" +
  lead("Only <b>one</b> tool can change anything: " + mono(CHANGING[0]) + ". The label is what lets a program <b>ask a person first</b>."), exp("exact")), "Run CELL 2. Point at the one amber label. Part D uses it.", cell=2)
D.add(BB, slide("Cell 2: a problem is a message, not a crash", '<div class="req"><div class="out ok f"><div class="who">get_order("4500012345")</div>' + mono(esc(str({k: ORDER["4500012345"][k] for k in ("status", "block_reason", "value_inr", "vendor_id")}))) + "</div>" +
  '<div class="out bad f"><div class="who">get_order("4500099999")</div>' + mono(esc(str({"ok": NOT_FOUND["ok"], "data": NOT_FOUND["data"]}))) + "</div></div>" +
  lead("A readable error lets the agent <b>try again or say what is missing</b>. A crash would stop it."), exp("exact · the first result is shortened to four fields")),
 "Run CELL 2 again and read the output aloud. A tool problem comes back as text the model can read.", cell=2)
D.add(BB, slide("Tool, resource or prompt?", table(["Example", "It is a…", "Why"], [
  ["Check the status of PO 4500012345", "<b>Tool</b>", "An action the AI requests: " + mono("get_order")], ["The full order list as a report", "<b>Resource</b>", "Data to read: " + mono("orders://all")],
  ["The blocked-orders report for plant 1000", "<b>Prompt</b>", "A saved request: " + mono("blocked_orders_report")], ["Create a follow-up ticket", "<b>Tool</b>", "It <b>changes data</b>, so a person approves"],
  ["PO approval limits as plain text", "<b>Resource</b>", mono("policy://approval-limits")]]), ), "Ask the room before revealing the middle column. Create a ticket is a tool, not a resource, because it does something.")
D.add(BB, slide("Cell 3: resources", '<div class="out f"><div class="who">Notebook output · exact</div>' + "<br>".join("• " + mono(r["uri"]) + " " + esc(r["name"]) for r in RESOURCES) +
  "<br><br>" + mono("orders://summary") + " →<br>" + mono(esc(json.dumps(SUMMARY, ensure_ascii=False))) + "</div>", exp("exact")), "Run CELL 3. Resources are things to read, each with an address.", cell=3)
D.add(BB, slide("Cell 3: prompts", '<div class="g2" style="align-items:start"><div class="out f"><div class="who">Notebook output · exact</div>' + "<br>".join("• " + mono(p["name"]) + "<br>&nbsp;&nbsp;" + esc(p["description"]) for p in PROMPTS) + "</div>" +
  '<div class="out ok f"><div class="who">blocked_orders_report, plant 1000</div>' + esc(PROMPT_TXT) + "</div></div>", exp("exact")), "A prompt is a saved request. The server fills in the blank (plant 1000) and hands back the text.", cell=3)
D.add(BB, slide("Cell 4: one call on the wire", '<div class="req"><div class="out f"><div class="who">→ Request</div><span class="wire">' + esc(json.dumps(WIRE[0][1], ensure_ascii=False)) + "</span></div>" +
  '<div class="out ok f"><div class="who">← Result</div><span class="wire">' + esc(json.dumps(WIRE[1][1], ensure_ascii=False)) + "</span></div></div>" +
  lead("JSON in, JSON out. <b>Any agent that speaks this can use any server that speaks it.</b>"), exp("Exact, except the id number, which counts up with every call")),
 "Run CELL 4. The id on your screen will differ. This is the whole protocol for one call.", cell=4)

# ------------------------------------------------------------------------------------------ PART C
BC = "C · The agent over MCP"
D.divider("Part C", "The agent over MCP", "Same loop. New plug.", "The menu comes from the server.", BC, divnote("Three demos: the menu, the loop, and plug and play. Then the Antigravity live demo."))
D.add(BC, slide("Request, check, run, observe", '<div class="step4"><div class="s f"><span class="who2 ai">AI</span><div class="n">1</div><h3>Writes a request</h3><p>' + esc('{"tool": "list_orders", "args": {…}}') + '</p></div>' +
  '<div class="s f"><span class="who2 prog">Program</span><div class="n">2</div><h3>Checks the gate</h3><p>Allowed? Read-only? Within the limit?</p></div>' +
  '<div class="s f"><span class="who2 prog">Server</span><div class="n">3</div><h3>Runs the function</h3><p>Over MCP, on the real data</p></div>' +
  '<div class="s f"><span class="who2 ai">AI</span><div class="n">4</div><h3>Observes</h3><p>Reads the result, then the next step</p></div></div>'),
 "Compare with the four steps from Class 6. The only new actor is the gate between 1 and 3. Cell 6 runs this.", cell=6)
menu_html = "".join('<span class="t">' + t["name"] + "</span>(" + args_of(t) + ')<br><span class="d">' + esc(short(t["description"])) + ".</span><br>" for t in TOOLS)
D.add(BC, slide("Cell 5: the menu comes from the server", '<div class="g2" style="align-items:start"><div class="menu f">' + menu_html + "</div>" +
  card("Class 6 versus today", "Then: " + mono("TOOLS = {…}") + " typed by hand.<br>Now: " + mono("offered()") + " <b>asks the server</b>, every time.<br><br>Add a tool to the server and it shows up here.", "📋", "acc") + "</div>"),
 "Run CELL 5 and read the printed instructions. Same structure as Class 6, but nobody typed the tool list.", cell=5)
D.add(BC, slide("Cell 6: the loop over MCP", trace([("think", "I need the blocked orders for plant 1000."), ("act", mono("list_orders({'plant': '1000', 'status': 'Blocked'})")),
  ("obs", mono(str(len(BLOCKED_1000)) + " orders: " + esc(BLOCKED_LINE))), ("fin", "Four blocked orders on plant 1000: " + esc(BLOCKED_ANS) + ".")]) +
  exp("The server's result is exact (shortened) · Think lines and the final wording will differ")), "Run CELL 6. The question is the one from the live demo: Which orders for Plant 1000 are blocked and why?", cell=6)
D.add(BC, slide("Live demo: Antigravity + MCP", '<div class="g2" style="align-items:start"><div>' + steps([("Open the Day_4 folder", "Antigravity reads the MCP config made by " + mono("make_mcp_config.py")),
  ("Check the server is connected", "Use the names you actually see for its MCP settings"), ("Ask the question", "Which orders for Plant 1000 are blocked and why?"),
  ("Narrate the tool calls", "Which tool? Which arguments? What came back?")]) + "</div>" +
  card("Check before class", "Antigravity changes quickly. Run this once beforehand and use the <b>names you see</b> on screen. Have a backup recording. The server shows mock data only.", "🎬", "warn") + "</div>"),
 "Live demo, about 10 minutes. See Class_7_MCP_Guardrails/antigravity/TASK.md for the exact prompts and a narration table. The agent should call list_orders with plant 1000 and status Blocked.")
D.add(BC, slide("Check the Antigravity result", table(["PO", "Vendor", "Value", "Block reason"], [[o["po_number"], o["vendor_name"], inr(o["value_inr"]), o["block_reason"]] for o in BLOCKED_1000], mono=(0, 2)) +
  lead("Four orders. We gave it only the <b>question</b>. It chose the tool, and we can check every row."), exp("exact · computed from orders.csv by the MCP server")), "The same answer key is saved as antigravity/expected_blocked_plant_1000.md.")
D.add(BC, slide("Cell 7: plug and play", '<div class="g2" style="align-items:start">' + pycode('''client.close()
client = connect("--with-scorecard")
print(len(client.list_tools()))
_ = run_agent("Which vendor has the highest total order value…")''', (1,)) +
  '<div class="out f"><div class="who">Notebook output · exact</div>Tools before: <b>' + str(len(TOOLS)) + "</b><br>Tools after: <b>" + str(len(TOOLS_W)) + "</b> → new: " + mono("vendor_scorecard") +
  "<br><br><b>We changed no agent code.</b> The trainer added one tool to the server.</div></div>", exp("exact")),
 "Run CELL 7. The point: yesterday we edited the notebook to add a tool (Class 6, Cell 10). Today the notebook is untouched.", cell=7)
D.add(BC, slide("Cell 7: the new tool answers", table(["Vendor", "Rating", "Orders", "Delayed", "Blocked", "Total value"], [[v, SCORE[v]["rating"], str(SCORE[v]["orders"]), str(SCORE[v]["delayed"]), str(SCORE[v]["blocked"]), inr(SCORE[v]["total_value_inr"])] for v in sorted(SCORE)], mono=(2, 3, 4, 5)) +
  lead("Question: <i>which vendor has the highest total order value?</i> Target: <b>" + TOP_VENDOR + "</b>, " + inr(SCORE[TOP_VENDOR]["total_value_inr"]) + ", " + str(SCORE[TOP_VENDOR]["delayed"]) + " delayed and " + str(SCORE[TOP_VENDOR]["blocked"]) + " blocked."), exp("exact data · the agent's wording will differ")),
 "The tool does the adding. The agent only chooses to use it.", cell=7)

# ------------------------------------------------------------------------------------------ PART D
BD = "D · Guardrails"
D.divider("Part D", "Guardrails", "Safe by design", "Limits that live in code, not in hope.", BD, divnote("Three demos: guardrails 1 to 3, human approval, and agent versus plain automation."))
D.add(BD, life_ai("<div class='emoji'>📜</div><p>In SAP a PO above a limit <b>waits for release</b>. Users get <b>display</b> or <b>change</b> authorisation, never everything.</p>",
                  "<div class='emoji'>🛑</div><p>An agent that can act needs the same: limits the <b>program</b> enforces, not limits we ask the model to remember.</p>", "In your SAP world", "For agents"), "Guardrails are the authorisation concept for agents.")
D.add(BD, slide("Four guardrails", grid(4, card("Read-only first", "Start with tools that cannot change anything.", None, "ok", num="1"), card("Allow-list", "The agent gets only the tools it needs.", None, "ok", num="2"),
  card("Step limit", "No endless loops.", None, "ok", num="3"), card("Human approval", "A person says yes before any change.", None, "ok", num="4")),
  lead("SAP comparison: display authorisation · a role · a job timeout · a <b>release strategy</b>.")), "Name the four, then give the SAP comparison in the lead line.")
D.add(BD, slide("Guardrails sit between the AI and the system", '<div class="flow"><div class="st f"><h3>The AI asks</h3><p>A request. <b>Only text.</b></p></div><div class="ar f">→</div>' +
  '<div class="st f" style="border-color:var(--ok)"><h3>The program checks</h3><p>Read-only? On the menu? Under the step limit? Approved?</p></div><div class="ar f">→</div><div class="st f"><h3>The server runs</h3><p>Only what passed the checks</p></div></div>',
  lead("Each guardrail is a few lines of ordinary code. <b>The AI cannot talk its way past them.</b>")), "This is the gate from Part C, with its four checks.")
D.add(BD, slide("Cell 8: guardrails 1 to 3", '<div class="out f"><div class="who">Notebook output</div>' +
  "1) Read-only first → " + mono(esc(str(G1))) + "<br>2) Allow-list of two tools → menu " + mono(esc(str(G2_MENU))) + "<br>&nbsp;&nbsp;&nbsp;&nbsp;list_orders → " + mono(esc(str(G2))) +
  "<br>3) Step limit of 1 → " + mono("⛔ Stopped: step limit reached") + "</div>", exp("Lines 1 and 2 are exact · in line 3 the Think and Act lines above it will differ by model; the last line is exact")),
 "Run CELL 8. Errors go back to the agent as observations, so it can recover or say what is missing.", cell=8)
D.add(BD, slide("Cell 9: human approval", '<div class="g2" style="align-items:start">' + pycode('''def gate(tool, args):
    if tool["annotations"].get("readOnlyHint"):
        return True            # reading is safe
    return ask_person(tool["name"], args)''', (3,)) +
  "<div>" + '<div class="out ok f"><div class="who">A person types yes</div>🛑 APPROVAL NEEDED: create_ticket(' + mono(esc(ASK_ARGS)) + ")<br>✅ Approved by a person.<br>→ " + mono(APPROVED["ticket_id"] + " created") + "</div>" +
  '<div style="height:14px"></div><div class="out bad f"><div class="who">A person types no</div>⛔ Declined. Nothing was changed.<br>→ ' + mono(esc(str(DECLINED))) + "</div></div></div>", exp("exact · the ticket number is the first one the server hands out")),
 "Run CELL 9 twice: answer yes once and no once. Only gate() changed. The loop is untouched. This is a simplified excerpt of the notebook cell.", cell=9)
D.add(BD, slide("A release strategy for AI", table(["In SAP", "For the agent"], [["A PO above the limit waits for release", "A tool that changes data waits for a person"], ["The approver sees the PO first", "The person sees the tool <b>and its arguments</b>"],
  ["Not released: nothing is posted", "Declined: <b>nothing is changed</b>"], ["Display or change authorisation", "A read-only label on every tool"]]), lead("Reading runs alone. <b>Changing waits for a person.</b>")), "The SAP people in the room already believe in this.", cell=9)
D.add(BD, slide("Antigravity: make it ask first", '<div class="g2" style="align-items:start"><div>' + steps([("Turn on approval", "In its settings, choose the mode that asks before running commands or tools"), ("Start the write server", "Enable " + mono("nova-sap-orders-write") + " in the MCP settings"),
  ("Ask for a change", "Create a follow-up ticket for PO 4500012345 about the credit check"), ("Watch it pause", "It waits until a person approves")]) + "</div>" +
  card("Check before class", "Setting names change between versions. Run it once, note the names you see, and keep a backup recording. If it asks for approval, say: <b>\"That pause is the guardrail.\"</b>", "🎬", "warn") + "</div>"),
 "Live guardrail demo, about 10 minutes. The read-only server cannot create tickets at all; the write server can, but only after approval. Exact steps are in antigravity/TASK.md.")
D.add(BD, slide("When NOT to use an agent", grid(2, card("Fixed rules → normal automation", "Approval limit lookup · the Tuesday and Friday payment run · posting an invoice that passed the 3-way match.", "⚙️", "ok"),
  card("Next step depends on what is found → agent", "PO delay investigation · IDoc error triage · invoice exceptions.", "🧭", "acc")), lead("If you can write the steps down in advance, <b>you probably do not need an agent</b>.")), "Ask the room for one process of each kind from their own projects.")
D.add(BD, slide("Cell 10: the same job, two ways", grid(2, '<div class="out ok f"><div class="who">Plain automation · exact</div>' + mono("check_approval(85000)") + "<br>→ " + mono(esc(str(PLAIN85))) + "<br><br><b>0</b> model calls.</div>",
  '<div class="out f"><div class="who">Agent · pattern</div>The same question typically needs <b>2</b> model calls and <b>2</b> steps (think, then answer).<br><br>Same answer. Slower, and it can slip.</div>') +
  lead("A fixed rule needs <b>no model</b>. It is faster, cheaper and easier to audit."), exp("Left side exact · the notebook prints your real call counts on the right")), "Run CELL 10.", cell=10)
D.add(BD, '<h2>Multi-agent: the idea (overview only)</h2><div class="body"><div class="diag"><div class="card acc top f"><h3>🧑‍✈️ Lead agent</h3><p>Splits the job, hands each part to a specialist, and puts the answer together.</p></div>' +
  '<div class="card f"><h3>📦 Procurement</h3><p>Orders · vendors · approval limits</p></div><div class="card f"><h3>💶 Finance</h3><p>Invoices · payments · disputes</p></div><div class="card f"><h3>🚚 Logistics</h3><p>Deliveries · delays · carriers</p></div></div>' +
  '<p class="lead f">Each specialist is the pattern you already know: <b>instructions + tools + loop</b>. We do not build this today.</p></div>', "Overview only. Keep it to two minutes. The point is that multi-agent is just several of what we built, with a coordinator.")

# ------------------------------------------------------------------------------------------ PART E
BE = "E · Your turn"
D.divider("Part E", "Your turn", "Ask five questions", "Note the tool it chose and whether it needed approval.", BE, divnote("40 minutes. Cells 11 and 12."))
D.add(BE, slide("Four tasks · 40 min", '<div class="g2"><div>' + steps([("Ask five business questions", "Cell 11: through the MCP-connected agent"), ("Note the tool it chose", "Was it the one you expected?")]) + "</div><div>" +
  steps([("Note if it needed approval", "Which question made the agent stop?"), ("Score it", "Cell 12: four questions checked in code")]) + "</div></div>"), "Pairs or teams. Remind them to change only the lines marked ← change me. Cell 9 must have been run so the write server and approval gate are active.", cell="11–12")
EXPECT = [("Which orders for Plant 1000 are blocked and why?", mono("list_orders"), "no", str(len(BLOCKED_1000)) + " orders"), ("Who is the vendor contact for PO 4500012346?", mono("get_order → get_vendor"), "no", VENDOR[ORDER["4500012346"]["vendor_id"]]["contact"]),
  ("Who must approve PO 4500012348?", mono("get_order → check_approval"), "no", APPR[1200000]["approver"]), ("Which vendor has the most delayed order value?", mono("delayed_summary"), "no", TOP_DELAY),
  ("Create a ticket for PO 4500012345 about the credit check.", mono("create_ticket"), "<b>YES</b>", "a ticket id")]
assert ORDER["4500012346"]["vendor_id"] == "V200" and VENDOR["V200"]["contact"] == "Rahul Verma"
D.add(BE, slide("Cell 11: five business questions", table(["Question", "Tools we expect", "Approval?", "Answer has"], [[q, t, a, esc(h)] for q, t, a, h in EXPECT], mono=()), exp("Expected values are exact (from the server) · the notebook prints what your model actually chose")),
 "Run CELL 11. The table prints the tools chosen, the steps and whether approval was needed. A different tool choice is a discussion point, not an error.", cell=11)
D.add(BE, slide("Worksheet: tool and approval", table(["Question", "Tool it chose", "Approval?", "Right?"], [[str(i), "", "", ""] for i in range(1, 6)]).replace("<td></td>", blank()),
  lead("Fill it in while the notebook runs. <b>Compare with your neighbour.</b>")), "Hand out or copy. They write the tools in the order printed by Cell 11.", cell=11)
FINAL = [("Which orders for Plant 1000 are blocked and why?", "list_orders", "credit check"), ("Who must approve PO 4500012348?", "get_order + check_approval", "director"),
  ("Which vendor has the highest total order value?", "vendor_scorecard", "chennai"), ("Create a ticket for PO 4500012345 about the credit check.", "create_ticket", "tck-")]
D.add(BE, slide("Cell 12: the scoreboard", table(["#", "Question", "Tools that must be used", "Answer must contain"], [[str(i), q, mono(t), w] for i, (q, t, w) in enumerate(FINAL, 1)]), exp("Expected values are exact · the notebook prints ✅ or ❌ and a score out of 4")),
 "Run CELL 12. Question 4 must trigger an approval AND produce a ticket id (TCK-…). If the approver types no, that row is a ❌ by design: nothing was created. Fast finishers can add their own rows.", cell=12)
D.add(BE, slide("What must never run without a person?", '<div class="pairs"><div><div class="label">An agent may do alone</div><ul class="yes f"><li>Look up a status</li><li>Find a vendor contact</li><li>Check an approval limit</li><li>Summarise delayed orders</li></ul></div>' +
  '<div><div class="label">A person approves first</div><ul class="no f"><li>Create a ticket (Cell 9)</li><li>Post documents (MIGO, MIRO)</li><li>Release payments</li><li>Change master data, especially bank details</li><li>Email vendors or customers</li></ul></div></div>' +
  lead("Collect this list from the room. <b>Tomorrow it becomes part of the capstone.</b>")), "This is the list from Class 6, now with a working mechanism behind it.")
D.add(BE, slide("Common myths", table(["They might think…", "Better to say…"], [["MCP is a new SAP product", "It is an <b>open standard</b>. It sits on top of the interfaces you already have."],
  ["If it is on MCP, it is safe", "MCP is the plug. <b>Safety comes from the guardrails we add.</b>"], ["The AI runs the tool on the server", "The AI <b>asks</b>. The program checks. The server runs."],
  ["More tools make a better agent", "Give an agent <b>only the tools it needs</b> (allow-list)."]])), "Use as a quick correction list.")
D.add(BE, slide("MCP and guardrails in one page", '<div class="g2"><div class="card f"><h3>MCP: the plug</h3><p>A server offers <b>tools</b>, <b>resources</b> and <b>prompts</b>.<br>The client <b>discovers</b> them. Add a tool to the server: every agent can use it.</p></div>' +
  '<div class="card f"><h3>Guardrails</h3><p><b>Read-only first</b> · <b>allow-list</b> · <b>step limit</b> · <b>human approval</b>.<br>Not every job needs an agent.</p></div></div>' + lead("The AI <b>asks</b>. The program <b>checks</b>. The server <b>runs</b>.")), "This is the participant handout.")

D.add("Wrap-up", """<h2>Quick quiz</h2><div class="body"><div class="quiz">
<div class="q f">What does MCP stand for, and what is the one-line idea?<span class="a">Model Context Protocol: USB-C for AI. One standard plug.</span></div>
<div class="q f">Name the 3 things an MCP server can offer.<span class="a">Tools, resources and prompts.</span></div>
<div class="q f">How does the agent know which tools exist?<span class="a">It asks the server (discovery). Nobody types the menu.</span></div>
<div class="q f">Name three guardrails.<span class="a">Read-only first, allow-list, step limit, human approval.</span></div>
<div class="q f">When must a person approve?<span class="a">Before any change: tickets, postings, payments, master data.</span></div>
<div class="q f">When is an agent the wrong choice?<span class="a">Fixed, rule-based processes: use normal automation.</span></div></div></div>""", "Ask each question aloud before revealing the answer.")
D.add("Wrap-up", slide("Remember three things", grid(3, card("MCP = USB-C for AI", "Tools, resources, prompts. Any agent, any system.", None, "acc", num="1"), card("Guardrails keep it safe", "Read-only first · limits · a person approves changes.", None, "acc", num="2"),
  card("Not every job needs an agent", "Fixed rules belong to normal automation.", None, "acc", num="3"))), "Three takeaways.")
D.add("Wrap-up", """<div class="body center"><div class="label" style="color:var(--accent)">After lunch · Class 8</div><div class="big">We have seen <em>every piece</em>.<br>How do they fit together?</div>
<p class="lead">Prompts, knowledge, agents, tools and guardrails. This afternoon we assemble them into <b>one real solution</b>, and learn where to start.</p></div>""", "Bridge to the afternoon.", "title")

path, n = D.write("Class_7_Agents_In_Action_Slides.html", "Class 7 · Agents in Action: Tools, MCP & Guardrails", C7 + "/slides")
print("Class 7 deck:", n, "slides,", D.term_total, "key terms ->", path)
close_servers()
