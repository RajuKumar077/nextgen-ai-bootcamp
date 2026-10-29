# Class 6 slides · "Neo Opens SAP" (AI agents) · dark theme, violet -> cyan
BASE += """
.tbl3{width:100%}
.diag{display:grid;grid-template-columns:1fr 1.2fr 1fr;grid-template-rows:auto auto;gap:18px;align-items:stretch}
.diag .top{grid-column:1/4}
.diag .core{background:var(--grad);color:#fff;border:0}
.diag .core h3,.diag .core p{color:#fff}
.menu{background:var(--codebg);color:var(--code);border-radius:22px;padding:22px 28px;font:19px/1.65 @MONO@;box-shadow:var(--winsh)}
.menu .t{color:#5dd8ff;font-weight:600} .menu .d{color:#b9bcc4}
.req{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.step4{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.step4 .s{background:var(--card);border:1px solid var(--hair);border-radius:26px;padding:24px;box-shadow:inset 0 1px 0 var(--gloss),0 18px 40px var(--cardsh)}
.step4 .s .n{font:700 44px @DISP@;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;line-height:1}
.step4 .s h3{font-size:22px;margin-top:8px} .step4 .s p{font-size:18px;color:var(--muted);margin:6px 0 0}
.who2{display:inline-block;font:700 12px @UI@;letter-spacing:.1em;text-transform:uppercase;border-radius:999px;padding:5px 11px;margin-bottom:8px}
.who2.ai{background:var(--acc-s);color:var(--accent)} .who2.prog{background:var(--ok-s);color:var(--ok)}
.loopring{display:flex;align-items:center;justify-content:center;gap:0}
.loopring .node{width:210px;height:210px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;background:var(--card);border:1px solid var(--hair);box-shadow:inset 0 1px 0 var(--gloss),0 22px 50px var(--cardsh)}
.loopring .node b{font:700 30px @DISP@;letter-spacing:-.02em;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.loopring .node span{font-size:17px;color:var(--muted);margin-top:4px;padding:0 18px}
.loopring .arw{font-size:34px;color:var(--muted2);padding:0 8px}
""".replace("@UI@", UI).replace("@MONO@", MONO).replace("@DISP@", DISP)

TERMS["Class 6"] = [
 ("Part A", [("Key terms: chatbot or agent?", [
    ("Chatbot", "Replies to one message using only what it was given. One step, no fetching.", "A helpdesk FAQ.", "1"),
    ("AI agent", "An AI that works towards a goal: it picks tools, takes several steps and checks each result before the next.", "A junior consultant investigating an issue.", "5"),
    ("Goal", "What the agent is trying to achieve. A goal needs many steps; a question needs one.", "The task assignment.", "5")])]),
 ("Part B", [("Key terms: the 4 parts (1 of 2)", [
    ("Brain (LLM)", "The language model. It decides what to do next. It does not run anything itself.", "The consultant's judgement.", "5"),
    ("Tool", "An ordinary function the agent may ask for: look up a PO, find a vendor, check a policy. No AI inside.", "A BAPI or function module.", "2"),
    ("Tool menu", "The list of tools and what each one does, written into the agent's instructions. The agent only knows tools from this menu.", "The list of authorised transactions.", "3")]),
  ("Key terms: the 4 parts (2 of 2)", [
    ("Instructions", "The goal and the rules, sent to the model before every step (the system prompt).", "Task assignment plus authorisations.", "3"),
    ("Memory", "What the agent has done and found so far. It is the conversation list the program keeps adding to.", "Your investigation notes.", "5"),
    ("Hallucination", "A confident answer that is invented. A tool result is a fact; a guess is not.", "\"I'm sure it's blocked.\" Check SAP.", "1")])]),
 ("Part C", [("Key terms: how tools really work", [
    ("Tool call", "A request written by the AI in a fixed format, such as {\"tool\": \"check_policy\", \"args\": {...}}. It is only text.", "Filling in a request form.", "4"),
    ("Executor", "The program that reads the request, runs the real function and returns the result. It is the control point.", "The system processing the form.", "4"),
    ("Allow-list", "Only tools on the menu can run. An unknown tool is refused by the program.", "Authorisation objects: no access, no run.", "7")])]),
 ("Part D", [("Key terms: the loop", [
    ("Think–Act–Observe loop", "Think: decide the next step. Act: request a tool. Observe: read the result. Repeat until the goal is reached. (Also called ReAct.)", "Check, read the result, decide the next check.", "5"),
    ("Observation", "The result a tool returns to the agent. It becomes the next input to think about.", "The answer in SE16.", "5"),
    ("Step limit", "A maximum number of passes through the loop, so an agent cannot run forever.", "A timeout on a background job.", "7"),
    ("Trace", "The printed record of every think, act and observe line. It lets you check the agent's work.", "A debugger log.", "5")])]),
 ("Part E", [("Key terms: using agents safely", [
    ("Human approval", "A person confirms before any risky step: payments, postings, master-data changes, external emails.", "Release strategy.", None),
    ("Tool description", "The one-line text that tells the agent when to use a tool. Clear descriptions give better tool choices.", "A good transaction short text.", "10"),
    ("Multi-agent", "Several agents that each do one part of a job and hand over to each other.", "A team of consultants.", None)])]),
]
TAGS["Class 6"] = [("a chatbot with no tools", "Chatbot"), ("chatbot or agent", "AI agent"), ("the 4 parts", "AI agent"), ("tools are ordinary", "Tool"), ("the tools in action", "Tool"),
  ("tool menu", "Tool menu"), ("instructions", "Instructions"), ("memory", "Memory"), ("request form", "Tool call"), ("one request, by hand", "Tool call"),
  ("who does what", "Executor"), ("think. act. observe", "Think–Act–Observe loop"), ("the agent loop", "Think–Act–Observe loop"), ("the full agent", "Think–Act–Observe loop"),
  ("a real trace", "Trace"), ("read the trace", "Trace"), ("different questions", "Tool"), ("only tools on the menu", "Allow-list"), ("step limit", "Step limit"),
  ("remove a tool", "Tool description"), ("add a tool", "Tool description"), ("never without approval", "Human approval"), ("antigravity", "AI agent"), ("four steps, two actors", "Executor"), ("who decided", "AI agent"), ("whole loop fits", "Think–Act–Observe loop"), ("three questions", "Tool"), ("worksheet", "Trace"), ("safety checks", "Allow-list"), ("guardrails already", "Allow-list"), ("ask your own", "AI agent"), ("take a tool away", "Tool description"), ("fourth tool", "Tool description"), ("the scoreboard", "Trace"), ("control point", "Allow-list"), ("memory is just", "Memory"), ("tool menu", "Tool menu"), ("neo runs on", "Brain (LLM)")]
for _tc, _t in {"Part A": "Chatbot vs agent", "Part B": "The 4 parts", "Part C": "How tools work", "Part D": "The loop", "Part E": "Your turn"}.items(): PART_TITLES[("Class 6", _tc)] = _t

# ---- trace rows computed from the tool functions on the data files
def _k(po): return tool_status(po)
S1 = tool_status("4500012345"); V1 = tool_vendor("4500012345"); P1 = policy(int(PO["4500012345"]["value_inr"]))
OBS1 = "{'status': '%s', 'block_reason': '%s', 'value': '%s', 'vendor_id': '%s'}" % (S1["status"], S1["block_reason"], S1["value"], S1["vendor_id"])
OBS2 = "{'vendor': '%s', 'contact': '%s', 'email': '%s'}" % (V1["vendor_name"], V1["contact"], V1["email"])
ANS1 = "PO 4500012345 is <b>%s</b> (%s). Contact <b>%s</b> at %s, %s." % (S1["status"].lower(), S1["block_reason"].lower(), V1["contact"], V1["vendor_name"], V1["email"])
S47 = tool_status("4500012347"); P47 = policy(int(PO["4500012347"]["value_inr"]))
S48 = tool_status("4500012348"); P48 = policy(int(PO["4500012348"]["value_inr"]))
assert (S1["status"], S1["block_reason"], V1["contact"], P1[0]) == ("Blocked", "Credit check", "Priya Sharma", "Line Manager")
assert (P47[0], P48[0]) == ("Line Manager", "Director") and S48["value"] == "₹12,00,000"
TOP_DELAY = max(DELAYED, key=lambda v: DELAYED[v][1]); assert TOP_DELAY == "Chennai Components"

E = Deck("Class 6", "Neo", "Day 3 · Afternoon")
A = "Start"
E.add(A, """<div class="body"><div class="label" style="color:var(--accent)">Day 3 · Class 6 · What is an AI agent?</div>
<h1><span class="mono">Neo</span><br>opens SAP</h1>
<p class="lead" style="margin-top:0">A chatbot <b>answers</b>. An agent <b>acts</b>. Today Neo gets a few tools and learns to <b>think, act and check its own work</b>.</p>
<div><span class="pill">Chatbot vs agent</span><span class="pill">The 4 parts</span><span class="pill">The loop</span><span class="pill">Runs on your laptop</span></div></div>""" + HINT,
 "Before class: open Day_3/Class_6_Agents/notebooks/Class_6_Neo_Opens_SAP.ipynb, choose the .venv kernel and run CELL S. Optional: have Antigravity open on the Class_6_Agents/data folder for the live demo.", "title")
E.add(A, slide("This morning in 30 seconds", grid(3, card("RAG = open-book exam", "Find the right page, then answer from it.", "📖"), card("Citations", "Every answer names its clause.", "📎"), card("Refuse when missing", "\"Not in the documents\" is a correct answer.", "🚫")),
  lead("Neo can now <b>answer from documents</b>. Documents don't change by the minute, though. <b>SAP does.</b>")), "Quick recap of Class 5.")
E.add(A, slide("The manager's question", chat(me("Why is PO 4500012345 delayed, and who should I contact?"), neo("…", "bad")) +
  lead("The answer is <b>not in any document</b>. It is in SAP, right now.")), "Set the scene. The same question appears in the notebook (CELL 1).")
E.add(A, slide("What would YOU do?", '<div class="g2" style="align-items:center"><div>' + "".join(
  '<div class="do f"><div class="n">' + str(i) + '</div><div><h3>' + t + "</h3><p>" + p + "</p></div></div>" for i, (t, p) in enumerate([
   ("Check the PO status", "In SAP"), ("Find the block reason", "Why is it stuck?"), ("Look up the vendor", "Name, contact, email"), ("Check the policy", "What happens next?"), ("Write the answer", "For the manager")], 1)) + "</div>" +
  card("Five steps", "Different information at <b>each</b> step, and each step depends on the one before.<br><br>A chatbot can't do that. <b>An agent can.</b>", "🧭", "acc") + "</div>"),
 "Collect the steps on the board before revealing this list. Ask the room for the order.")
E.add(A, """<div class="hero"><div class="orb">Neo</div><div><div class="label" style="color:var(--accent)">Neo, upgraded</div><h2 style="margin-bottom:18px">Now with hands</h2>
<p class="f">🧠 Same brain, same careful notes</p><p class="f">🛠️ Plus <b>three tools</b> it may ask for</p><p class="f">🔁 Plus a <b>loop</b> to check its own work</p><p class="f">🔒 And <b>only</b> the tools we allow</p></div></div>""",
 "Neo is still the same character. What changes is that Neo can now request tools.")
E.add(A, """<div class="body center"><div class="big">The AI <em>decides</em>.<br>The system <em>executes</em>.</div>
<p class="lead f">And only the tools <b>we</b> allow. Keep this sentence for tomorrow's guardrails.</p></div>""", "The one idea for the afternoon. Pause here.")
E.add(A, """<h2>Today's plan · 2 hours</h2><div class="body"><table class="agenda">
<tr><th>Time</th><th>Topic</th><th>Question</th><th>Cells</th></tr>
<tr><td class="t">0:00</td><td>A · Chatbot vs agent</td><td>What is the difference?</td><td class="m">S, 1</td></tr>
<tr><td class="t">0:15</td><td>B · The 4 parts of an agent</td><td>What is inside one?</td><td class="m">2–3</td></tr>
<tr><td class="t">0:30</td><td>C · How tools really work</td><td>Who runs the tool?</td><td class="m">4</td></tr>
<tr><td class="t">0:40</td><td>D · The loop</td><td>How does it decide?</td><td class="m">5–7</td></tr>
<tr><td class="t">1:20</td><td>E · Your turn</td><td>Ask, break and extend it</td><td class="m">8–11</td></tr></table></div>""", "Part D is the heart of the class.")
E.add(A, slide("Neo runs on this laptop", '<div class="g2" style="align-items:center">' + card("Same set-up as this morning", "The agent uses the <b>chat model</b> only. The tools are plain Python reading two CSV files: <span class=\"mono\">orders.csv</span> and <span class=\"mono\">vendors.csv</span>.", "💻") +
  '<div class="f">' + msg("s", "Ollama is running · main model found") + '<div style="height:12px"></div>' + msg("s", "Neo replies <b>Connection OK</b>") + "</div></div>"), "Run CELL S.", cell="S")

BA = "A · Chatbot vs agent"
E.divider("Part A", "Chatbot vs agent", "Answers or acts?", "Same brain. A very different job.", BA, divnote("Part A has one demo: a chatbot with no tools."))
E.add(BA, slide("A chatbot answers. An agent acts.", table(["", "Chatbot", "Agent"], [
  ["Goal", "Answer a message", "Achieve a goal"], ["Steps", "One", "Many"], ["Information", "Only what you give it", "<b>Fetches</b> it with tools"], ["Who decides the steps", "You", "<b>The agent</b>"],
  ["SAP comparison", "A helpdesk FAQ", "A junior consultant investigating an issue"]], cls="sheet f")), "Walk the table row by row.")
E.add(BA, slide("Cell 1: a chatbot with no tools", qa("Why is PO 4500012345 delayed, and who should I contact?",
  "Either <i>\"I don't have access to your purchasing system…\"</i> (honest), or a plausible <b>invention</b> such as <i>\"It is probably a customs delay. Contact the vendor's logistics team.\"</i>", "bad"), exp("Typical answer pattern · your model's wording will differ")),
 "Run CELL 1. A chatbot cannot fetch the status. A small model may invent something: that is a hallucination.", cell=1)
E.add(BA, slide("What the chatbot is missing", grid(3, card("The status", "Blocked? Delayed? Delivered?", "📦", "bad"), card("The vendor", "Who is the contact?", "📇", "bad"), card("The policy", "Who must act next?", "📖", "bad")),
  lead("Three facts, three different places. <b>It needs to go and get them.</b>")), "Set up Part B.")
E.add(BA, """<div class="body center"><div class="big">A chatbot talks about work.<br>An agent <em>does the steps</em>.</div></div>""", "Pause.")

BB = "B · The 4 parts"
E.divider("Part B", "The 4 parts", "Inside an agent", "Brain · Tools · Memory · Instructions.", BB, divnote("Two demos: the tools, and the tool menu."))
E.add(BB, slide("An agent has four parts", '<div class="diag"><div class="card acc top f"><h3>📋 Instructions</h3><p>The goal and the rules. "Answer using only facts returned by your tools."</p></div>' +
  '<div class="card f"><h3>📝 Memory</h3><p>What it has done and found so far.</p></div><div class="card core f"><h3>🧠 Brain (the LLM)</h3><p>Decides what to do next.</p></div><div class="card f"><h3>🛠️ Tools</h3><p>Actions and data it may ask for.</p></div></div>'),
 "Draw the diagram. Ask for the SAP comparison: Brain = judgement, Tools = BAPIs, Memory = investigation notes, Instructions = task assignment plus authorisations.")
E.add(BB, slide("The SAP comparison", table(["Part", "Say this", "SAP comparison"], [
  ["🧠 Brain", "The LLM decides what to do next.", "The consultant's judgement"], ["🛠️ Tools", "Actions or data it can use.", "BAPIs · function modules · transactions"],
  ["📝 Memory", "What it has done and found so far.", "Your investigation notes"], ["📋 Instructions", "Its goal and its rules.", "Task assignment + authorisations"]], cls="sheet f")), "Each row links an agent part to something SAP people already know.")
E.add(BB, slide("Tools are ordinary functions", grid(3, card("check_order_status", "Status, block reason, value, delivery date, vendor id", "📦", "acc"), card("get_vendor_details", "Vendor name, contact, email, rating", "📇", "acc"), card("check_policy", "Who must approve a PO of this value", "📖", "acc")),
  lead("They read our mock data. <b>There is no AI inside a tool</b>: same input, same output.")), "Name the three tools. The 4th arrives in Cell 10.", cell=2)
E.add(BB, slide("Cell 2: the tools in action", '<div class="out f"><div class="who">Notebook output · exact</div>' +
  "<span class=\"mono\">check_order_status('4500012345')</span><br>→ " + esc(OBS1) + "<br><br>" +
  "<span class=\"mono\">get_vendor_details('4500012345')</span><br>→ " + esc(OBS2) + "<br><br>" +
  "<span class=\"mono\">check_policy(85000)</span> → " + esc(policy(85000)[0]) + " (policy " + policy(85000)[1] + ") &nbsp;·&nbsp; <span class=\"mono\">check_policy(1200000)</span> → " + esc(policy(1200000)[0]) + " (policy " + policy(1200000)[1] + ")</div>", exp("exact")),
 "Run CELL 2. These lines are computed from orders.csv and vendors.csv by the same logic as the notebook, so they match your screen.", cell=2)
E.add(BB, slide("The tool menu", '<div class="g2" style="align-items:start"><div class="menu f"><span class="t">check_order_status</span>(po_number)<br><span class="d">Status, block reason, value, delivery date, vendor id.</span><br><br><span class="t">get_vendor_details</span>(po_number)<br><span class="d">Vendor, contact, email, rating.</span><br><br><span class="t">check_policy</span>(value_inr)<br><span class="d">Who must approve a PO of this value.</span></div>' +
  card("The agent only knows its tools from this menu", "Clear names and one-line descriptions matter, just like a good prompt. A vague description means the wrong tool gets chosen.", "📋", "warn") + "</div>"),
 "Run CELL 3 and read the printed instructions aloud.", cell=3)
E.add(BB, slide("The instructions (system prompt)", '<div class="g2" style="align-items:start">' + pycode('''You are Neo, an SAP procurement assistant.
GOAL: answer using ONLY facts returned by
your tools. Never guess a status, a contact
or an approver.

TOOLS (the only ones you may use):
- check_order_status(po_number): ...
- get_vendor_details(po_number): ...
- check_policy(value_inr): ...

Reply with ONE JSON object and nothing else.
To use a tool: {"thought":..,"tool":..,"args":{..}}
To finish:     {"thought":..,"answer":".."}''') +
  "<div>" + card("Goal", "What to achieve.", None, "acc", num="1") + '<div style="height:12px"></div>' + card("Rule", "Facts from tools only. No guessing.", None, "acc", num="2") + '<div style="height:12px"></div>' + card("Reply format", "Two shapes: use a tool, or finish.", None, "acc", num="3") + "</div></div>"),
 "These instructions are the same R-T-C-F-R idea from Day 2: a role, a task, context (the tools), a format and rules.", cell=3)

BC = "C · How tools work"
E.divider("Part C", "How tools work", "Who runs the tool?", "The AI asks. The program runs.", BC, divnote("One demo, one idea: the request form."))
E.add(BC, life_ai("<div class='emoji'>📝</div><p>A consultant fills in a <b>request form</b>.</p><p>The system processes it and returns the result.</p>",
                  "<div class='emoji'>🤖</div><p>Neo writes a <b>tool request</b> as text.</p><p>The program runs the function and returns the result.</p>"), "The AI itself can only produce text.")
E.add(BC, slide("Four steps, two actors", '<div class="step4"><div class="s f"><span class="who2 ai">AI</span><div class="n">1</div><h3>Writes a request</h3><p>{"tool": "check_order_status", "args": {…}}</p></div>' +
  '<div class="s f"><span class="who2 prog">Program</span><div class="n">2</div><h3>Runs the function</h3><p>Only if it is on the menu</p></div>' +
  '<div class="s f"><span class="who2 prog">Program</span><div class="n">3</div><h3>Returns the result</h3><p>Added to the conversation</p></div>' +
  '<div class="s f"><span class="who2 ai">AI</span><div class="n">4</div><h3>Carries on thinking</h3><p>Next step, or the final answer</p></div></div>'), "This is the most important slide of the class.", cell=4)
E.add(BC, slide("Cell 4: one request, by hand", '<div class="req"><div class="out f"><div class="who">1 · The AI wrote a request</div><span class="mono">{"thought": "I need the PO status", "tool": "check_order_status", "args": {"po_number": "4500012345"}}</span></div>' +
  '<div class="out ok f"><div class="who">2 · The program ran it</div><span class="mono">' + esc(OBS1) + "</span></div></div>" +
  lead("The AI wrote <b>text</b>. The program did the <b>work</b>. The thought wording will differ; the tool result is exact."), exp("Request wording varies · the tool result is exact")),
 "Run CELL 4. If the model answers without a tool, run it again and say that is exactly why we test.", cell=4)
E.add(BC, slide("This is our control point", grid(3, card("Only the menu runs", "An unknown tool name is refused.", "🔒", "ok"), card("The program checks arguments", "Wrong or missing arguments become an error, not an action.", "🧪", "ok"), card("We decide what is on the menu", "No tool for payments? Then it cannot pay.", "🎛️", "ok")),
  lead("This is where <b>guardrails</b> live. We use it heavily tomorrow.")), "Link to Day 4.")

BD = "D · The loop"
E.divider("Part D", "The loop", "How does it decide?", "Think. Act. Observe. Repeat.", BD, divnote("Three demos: the full agent, three questions, the safety checks."))
E.add(BD, '<h2>Think. Act. Observe. Repeat.</h2><div class="body"><div class="loopring f"><div class="node"><b>Think</b><span>What do I need next?</span></div><div class="arw">→</div>' +
  '<div class="node"><b>Act</b><span>Ask for a tool</span></div><div class="arw">→</div><div class="node"><b>Observe</b><span>Read the result</span></div><div class="arw">→</div><div class="node"><b>Repeat</b><span>Or give the answer</span></div></div>' +
  '<p class="lead f" style="text-align:center;max-width:none">Just how you investigate an issue: check something, read the result, decide the next check.</p></div>', "Also called ReAct (reason plus act) in the literature.")
E.add(BD, slide("A real trace", trace([("think", "I need the PO status."), ("act", "<span class=\"mono\">check_order_status({'po_number': '4500012345'})</span>"), ("obs", "<span class=\"mono\">" + esc(OBS1) + "</span>"),
  ("think", "Now I need the vendor contact."), ("act", "<span class=\"mono\">get_vendor_details({'po_number': '4500012345'})</span>"), ("obs", "<span class=\"mono\">" + esc(OBS2) + "</span>"), ("fin", ANS1)]) +
  exp("Observe lines are exact (from the data) · Think lines and the final wording will differ")), "Target trace for the manager's question. The OBSERVE lines are computed from the data files.", cell=5)
E.add(BD, slide("Who decided the order?", grid(3, card("Tools used", "<b>2</b> of the 3", None, "acc", num="2"), card("Order chosen by", "<b>The agent</b>, not us", None, "acc", num="🧠"), card("Steps", "<b>3</b> passes through the loop", None, "acc", num="3")),
  lead("Nobody told Neo the order. Neo read the question and chose.")), "Ask the room: how many tools did it use, and who decided the order?", cell=5)
E.add(BD, slide("Cell 5: the whole loop fits on one screen", '<div class="g2" style="align-items:start">' + pycode('''for step in range(1, max_steps + 1):
    reply = chat_json(messages)              # THINK
    if "answer" in reply:
        return reply["answer"]               # FINISH
    result = execute(reply)                  # ACT
    messages += [                            # OBSERVE
      {"role": "assistant", "content": reply},
      {"role": "user", "content": "Tool result: " + result}]
# step limit reached → stop''', (1, 4, 5)) +
  '<div class="card f"><h3>Read it in four lines</h3><p><b>Think:</b> the model replies with a tool request or an answer.<br><b>Act:</b> the program runs the tool.<br><b>Observe:</b> the result is added to the conversation.<br><b>Repeat</b> until it can answer, or the step limit hits.</p></div></div>'),
 "Do not explain the Python. Point at the three comments: THINK, ACT, OBSERVE. This code is a simplified excerpt of the notebook cell.", cell=5)
E.add(BD, slide("Memory is just the growing list", chat(me("Why is PO 4500012345 delayed…"), neo("<span class=\"mono\">{tool: check_order_status…}</span>"), me("<span class=\"mono\">Tool result: {status: Blocked…}</span>"), neo("<span class=\"mono\">{tool: get_vendor_details…}</span>")) +
  lead("Each pass, the program <b>re-sends the whole list</b>. Same trick as chat memory this morning.")), "Link back to Cell 3 of Class 5: the app re-sends the history.", cell=5)
E.add(BD, slide("Cell 6: three questions, three tool choices", table(["Question", "Tools we expect", "Answer should contain"], [
  ["What is the status of PO 4500012345?", "<span class=\"mono\">check_order_status</span>", "Blocked · " + S1["block_reason"]],
  ["Who is the vendor for PO 4500012346 and how do I contact them?", "<span class=\"mono\">get_vendor_details</span>", tool_vendor("4500012346")["contact"] + " · " + tool_vendor("4500012346")["email"]],
  ["Can PO 4500012347 be approved by a line manager?", "<span class=\"mono\">check_order_status</span> + <span class=\"mono\">check_policy</span>", "Yes · " + S47["value"] + " ≤ ₹1,00,000 → " + P47[0]]], cls="sheet f", ), exp("Expected values are exact (from the data) · the notebook prints ✅ or ⚠️ for each")),
 "Run CELL 6. The notebook checks both the tools used and a keyword in the answer. A ⚠️ is part of the lesson.", cell=6)
E.add(BD, slide("Worksheet: tools and steps", table(["Question", "Tools used (in order)", "Steps", "Correct?"], [["1", "", "", ""], ["2", "", "", ""], ["3", "", "", ""]]).replace("<td></td>", blank()),
  lead("Fill it in while the notebook runs. <b>Compare answers</b> with your neighbour.")), "Hand out or copy. They write the tools in the order the trace shows.", cell=6)
E.add(BD, slide("A ⚠️ is a lesson, not a failure", grid(2, card("It can choose the wrong tool", "Or call the right tool with the wrong argument.", "🔧", "warn"), card("It can misread a result", "Or stop too early, or loop.", "👀", "warn")),
  lead("Agents are <b>tested</b>, and risky steps get a <b>person's approval</b>.")), "If a small model produces bad JSON live, say: that is why production agents need validation and step limits.")
E.add(BD, slide("Cell 7: the safety checks", '<div class="out f"><div class="who">Notebook output · exact</div>' +
  "1) Tool not on the menu → <span class=\"mono\">{'error': \"Unknown tool 'delete_purchase_order'. Allowed tools: ['check_order_status', 'get_vendor_details', 'check_policy']\"}</span><br>" +
  "2) Wrong arguments → <span class=\"mono\">{'error': \"Bad arguments for check_order_status: … unexpected keyword argument 'order'\"}</span><br>" +
  "3) PO that doesn't exist → <span class=\"mono\">{'error': 'PO 4500099999 not found'}</span><br>" +
  "4) Step limit of 1 → <span class=\"mono\">⛔ Stopped: step limit reached</span></div>", exp("exact")),
 "Run CELL 7. Errors are returned to the agent as observations, so it can recover. The step limit is a guardrail.", cell=7)
E.add(BD, slide("Four guardrails already built in", grid(4, card("Allow-list", "Unknown tool → refused", None, "ok", num="1"), card("Argument check", "Bad arguments → error", None, "ok", num="2"), card("Not found", "Missing PO → clear error", None, "ok", num="3"), card("Step limit", "Cannot loop forever", None, "ok", num="4")),
  lead("Tomorrow: more guardrails, and a <b>standard way</b> to connect tools (MCP).")), "Forward reference to Day 4.", cell=7)
E.add(BD, slide("Antigravity: an agent you can watch", '<div class="g2" style="align-items:start"><div>' +
  '<div class="do f"><div class="n">1</div><div><h3>Open the folder</h3><p><span class="mono">Class_6_Agents/data</span> in Antigravity</p></div></div>' +
  '<div class="do f"><div class="n">2</div><div><h3>Give it the task</h3><p>Copy it from <span class="mono">antigravity/TASK.md</span></p></div></div>' +
  '<div class="do f"><div class="n">3</div><div><h3>Narrate each step</h3><p>Plan → Think · reads file → Act · checks → Observe</p></div></div></div>' +
  card("Check before class", "Antigravity changes quickly. Run the task once beforehand and use the <b>names you actually see</b> on screen for its plan, task list and steps. Have a backup recording.", "🎬", "warn") + "</div>"),
 "Live demo, about 15 minutes. If Antigravity asks for approval to run a command, point it out: that is a guardrail.")
E.add(BD, slide("Check the Antigravity result", table(["Vendor", "Delayed POs", "Total value"], [[v, str(d[0]), inr(d[1])] for v, d in sorted(DELAYED.items())], cls="sheet f", mono=(1, 2)) +
  lead("Expected report grouped by vendor. We gave it only the <b>goal</b>. It worked out the steps, and we can check every one."), exp("exact · computed from orders.csv")), "The expected report is also saved as antigravity/expected_delayed_report.md.")

BE = "E · Your turn"
E.divider("Part E", "Your turn", "Ask, break, extend", "Change only the lines marked ← change me.", BE, divnote("40 minutes. Cells 8 to 11."))
E.add(BE, slide("Four tasks · 40 min", '<div class="g2"><div>' +
  '<div class="do f"><div class="n">1</div><div><h3>Ask your own question</h3><p>Cell 8</p></div></div><div class="do f"><div class="n">2</div><div><h3>Remove a tool</h3><p>Cell 9: what happens without <span class="mono">check_policy</span>?</p></div></div></div><div>' +
  '<div class="do f"><div class="n">3</div><div><h3>Add a tool</h3><p>Cell 10: a fourth tool, one summary function</p></div></div><div class="do f"><div class="n">4</div><div><h3>Score the agent</h3><p>Cell 11: four questions checked in code</p></div></div></div></div>'), "Pairs. Remind them to change only the lines marked ← change me.", cell="8–11")
E.add(BE, slide("Cell 8: ask your own question", '<div class="g2" style="align-items:start">' + pycode('''MY_QUESTION = "Who must approve PO 4500012348,
               and why is it blocked?"      # ← change me
run_agent(MY_QUESTION)''', (0, 1, 2)) +
  '<div class="card f"><h3>Try these</h3><p>• Who is the vendor for PO 4500012350?<br>• What is the delivery date of PO 4500012354?<br>• Is PO 4500012355 blocked, and who is the contact?</p></div></div>'
  + lead("Target for the first: <b>" + P48[0] + "</b> (" + S48["value"] + " &gt; ₹10,00,000, policy " + P48[1] + "), blocked for <b>" + S48["block_reason"].lower() + "</b>."), exp()),
 "Run CELL 8. The target answer comes from the data and the policy limits.", cell=8)
E.add(BE, slide("Cell 9: take a tool away", '<div class="g2" style="align-items:center">' + pycode('''removed = TOOLS.pop("check_policy")
run_agent("Who must approve PO 4500012348?")
TOOLS["check_policy"] = removed''', (0,)) +
  card("What do you expect?", "Without the policy tool the agent either says it <b>cannot tell</b>, or it <b>guesses</b>.<br><br>Correct answer: <b>" + P48[0] + "</b>.", "🧪", "warn") + "</div>" + lead("Tools are what make an agent <b>reliable</b>."), exp("Behaviour varies by model")),
 "Run CELL 9. The tool is put back automatically afterwards.", cell=9)
E.add(BE, slide("Cell 10: add a fourth tool", '<div class="g2" style="align-items:start">' + pycode('''def delayed_summary():
    """Delayed POs per vendor: count and total value."""
    ...

TOOLS["delayed_summary"] = {
    "fn": delayed_summary, "args": "(none)",
    "does": "Number and total value (INR) of Delayed
             purchase orders for every vendor."}''', (6,)) +
  "<div>" + table(["Vendor", "Delayed", "Value"], [[v, str(d[0]), inr(d[1])] for v, d in sorted(DELAYED.items())], mono=(1, 2)) + lead("Question: <i>which vendor has the most delayed value?</i> Target: <b>" + TOP_DELAY + "</b>, " + inr(DELAYED[TOP_DELAY][1]) + ".") + "</div></div>", exp("exact data · the agent's wording will differ")),
 "Run CELL 10. We add one function and one menu entry, and the agent can use it straight away.", cell=10)
E.add(BE, slide("Cell 11: the scoreboard", table(["#", "Question", "Tools that must be used", "Answer must contain"], [
  ["1", "What is the status of PO 4500012345?", "check_order_status", "block"], ["2", "Who is the vendor for PO 4500012346 …?", "get_vendor_details", "rahul"],
  ["3", "Can PO 4500012347 be approved by a line manager?", "check_order_status + check_policy", "yes"], ["4", "Who must approve PO 4500012348?", "check_policy", "director"]], mono=(2, 3)), exp("exact · the notebook prints ✅ or ❌ and a score out of 4")),
 "Run CELL 11. The code scores the tools used and a keyword in each answer. Fast finishers can add their own rows.", cell=11)
E.add(BE, slide("What must never run without a person?", '<div class="pairs"><div><div class="label">An agent may do alone</div><ul class="yes f"><li>Look up a status</li><li>Find a vendor contact</li><li>Check a policy</li><li>Summarise delayed orders</li></ul></div>' +
  '<div><div class="label">Never without approval</div><ul class="no f"><li>Post documents (MIGO, MIRO)</li><li>Release payments</li><li>Change master data, especially bank details</li><li>Email vendors or customers</li><li>Delete anything</li></ul></div></div>' +
  lead("Keep this list. <b>Tomorrow we build it into the system.</b>")), "Collect this list from the room before showing it. Save it for Class 7.")
E.add(BE, slide("Which SAP tasks suit an agent?", grid(3, card("Good fit", "Multi-step investigations where the next step depends on what you find.", "✅", "ok"), card("Good examples", "PO follow-ups · IDoc error investigation · invoice exceptions · month-end checks", "📋", "ok"),
  card("Poor fit", "A simple question with one answer. A prompt or RAG is cheaper and faster.", "⚠️", "warn"))), "Ask the room for their own examples.")
E.add(BE, slide("Common myths", table(["They might think…", "Better to say…"], [
  ["Agents are fully autonomous robots", "They act within the tools and rules we give them."], ["The AI logs into SAP and runs transactions", "The AI <b>requests</b> a tool. The program runs it."],
  ["Agents are always better than chatbots", "For simple Q&amp;A, a prompt or RAG is simpler and cheaper."], ["If it's an agent, it's always right", "It can pick the wrong tool or misread a result. Test it."]])), "Use as a quick correction list.")
E.add(BE, slide("Agents in one page", '<div class="g2"><div class="card f"><h3>Chatbot vs agent</h3><p>Chatbot: answers a message.<br>Agent: achieves a goal, in many steps, using tools.</p></div>' +
  '<div class="card f"><h3>The loop</h3><p><b>Think → Act → Observe → Repeat</b><br>until it can answer, or the step limit is reached.</p></div></div>' +
  lead("The AI <b>asks</b>. The program <b>runs</b>. Only the tools we <b>allow</b>.")), "This is the participant handout.")

E.add("Wrap-up", """<h2>Quick quiz</h2><div class="body"><div class="quiz">
<div class="q f">Describe the agent loop in four words.<span class="a">Think, act, observe, repeat.</span></div>
<div class="q f">What are the 4 parts of an agent?<span class="a">Brain, tools, memory, instructions.</span></div>
<div class="q f">Does the AI run the tool itself?<span class="a">No. It requests it; the program runs it.</span></div>
<div class="q f">When is an agent the right choice?<span class="a">Multi-step tasks where the next step depends on what is found.</span></div>
<div class="q f">Name one thing an agent must never do without approval.<span class="a">Payments, postings, master-data changes, external emails.</span></div>
<div class="q f">What stops an agent looping forever?<span class="a">A step limit.</span></div></div></div>""", "Ask each question aloud before revealing the answer.")
E.add("Wrap-up", slide("Remember three things", grid(3, card("4 parts", "Brain · Tools · Memory · Instructions.", None, "acc", num="1"), card("The loop", "Think → Act → Observe → Repeat.", None, "acc", num="2"), card("AI decides, system executes", "Only the tools we allow.", None, "acc", num="3"))), "Three takeaways.")
E.add("Wrap-up", """<div class="body center"><div class="label" style="color:var(--accent)">Tomorrow · Day 4</div><div class="big">Our tools were <em>hand-built</em>.<br>What about twenty systems?</div>
<p class="lead">Day 4: a <b>standard way</b> to connect agents to systems (MCP), and the <b>guardrails</b> that keep them safe. Tonight, think of <b>one SAP process</b> where an assistant would help you.</p></div>""", "Bridge to Day 4, and the capstone preparation.", "title")

finish(E, "Class_6_Neo_Opens_SAP_Slides.html", "Class 6 · Neo Opens SAP", DARK, "d3Class6Theme", DAY3 + "/Class_6_Agents/slides/")
