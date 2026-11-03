# Class 8 slides · "Putting It All Together: an AI Agent for SAP" · dark theme, green -> blue -> gold
# Every value labelled "exact" comes from d4_slides_core (the notebook's own code, run on the real MCP server and the real documents).
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d4_slides_core import *          # noqa: F401,F403,E402

D = new_deck("Class 8", "Day 4 · Afternoon", THEME8, "d4Class8Theme", "dark")

# ------------------------------------------------------------------------------------------ computed pieces
_chk = C.run_src(C.CHECK_SRC, {"json": json, "re": re})["check_answer"]
EVID = [{"tool": "get_order", "args": {"po_number": "4500012348"}, "result": ORD48},
        {"tool": "check_approval", "args": {"value_inr": "1200000"}, "result": APPR[1200000]},
        {"tool": "search_policy", "args": {"query": "price variance"}, "result": [{"id": "Procurement_Policy §6.2", "text": C62["text"]}]},
        {"tool": "get_vendor", "args": {"vendor_id": "V300"}, "result": VENDOR["V300"]}]
GOOD = ("PO 4500012348 (" + inr(ORD48["value_inr"]) + ") is blocked for price variance. The " + APPR[1200000]["approver"] + " must approve it (policy " + APPR[1200000]["policy"] +
        "). Our rule: a price variance above 1% blocks the invoice [Procurement_Policy §6.2]. Contact " + VENDOR["V300"]["contact"] + ".")
FAKE = "The Director approved it for ₹15,00,000 [Procurement_Policy §9.9]."
assert _chk("q", {"answer": GOOD, "evidence": EVID}) == []
PROBLEMS = _chk("q", {"answer": FAKE, "evidence": EVID})
assert PROBLEMS == ["number 15,00,000 is not in any tool result", "citation Procurement_Policy §9.9 was never retrieved"], PROBLEMS

# the use cases offered in CELL 10: which sources each one needs (every clause named here must exist in the documents)
for cid in ("Procurement_Policy §4.1", "Procurement_Policy §6.2", "IDoc_Error_Guide §1.1", "IDoc_Error_Guide §2.3", "SAP_P2P_Process_Guide §2.1"):
    assert cid in CLAUSE, cid
FIRST_DELAYED_2000 = DELAYED_2000[0]
assert FIRST_DELAYED_2000["po_number"] == "4500012349" and VENDOR[FIRST_DELAYED_2000["vendor_id"]]["contact"] == "Rahul Verma"
UC = [("Invoice exception", "PO 4500012348: price variance", "Orders + approver + <b>policy</b> + vendor", "MCP + RAG"),
      ("PO delay analysis", "Delayed orders on plant 2000", "Orders + vendor contact", "MCP"),
      ("IDoc error triage", "IDoc stuck at status 51", "IDoc handbook (§1.1, §2.3)", "RAG"),
      ("Vendor query", "Contact for PO 4500012346", "Order + vendor", "MCP"),
      ("Month-end close", "Blocked orders + 3-way match", "Orders + <b>policy</b> (§4.1)", "MCP + RAG")]
NEEDS = [("Summarise this supplier email in one line.", "prompt"), ("What does our policy say about changing vendor bank details?", "rag"),
         ("What does IDoc status 51 mean?", "rag"), ("Why is PO 4500012348 blocked, who must approve it and who is the vendor contact?", "agent"), ("Which orders for plant 1000 are blocked?", "agent")]
TESTS = [("direct", "What is the status of PO 4500012345?", "get_order", "blocked"), ("direct", "What does IDoc status 51 mean?", "search_policy", "not posted"),
         ("direct", "Who is the vendor contact for PO 4500012346?", "get_order + get_vendor", "rahul"), ("reworded", "Which senior person has to sign off on PO 4500012348 because it is so large?", "get_order + check_approval", "director"),
         ("missing", "What is the notice period for ending a vendor contract?", "none", "says it is missing")]
assert ORDER["4500012345"]["status"] == "Blocked" and "not posted" in CLAUSE["IDoc_Error_Guide §1.1"]["text"]
assert VENDOR[ORDER["4500012346"]["vendor_id"]]["contact"] == "Rahul Verma"
assert not any(k in " ".join(c["text"].lower() for c in CHUNKS) for k in ("notice period", "terminate", "termination"))      # the 'missing' test really is missing
MAXSTEPS = int(re.search(r"MAX_STEPS = (\d+)", C.MENU_SRC).group(1))
assert MAXSTEPS == 6

# ------------------------------------------------------------------------------------------ key terms
D.terms = {
 "Part 1": [("Key terms: start simple", [
    ("Simplest approach", "The cheapest tool that solves the problem: a prompt first, then documents (RAG), then an agent. Add the next one only when the problem needs it.", "A standard report before a custom program.", "2"),
    ("Prompt-only", "Summarise, draft or classify text you already have. No documents, no tools. Fast, cheap and often enough.", "A mail template.", "1"),
    ("Router", "The step that chooses prompt, RAG or agent for a request. It is a decision to test, like any other.", "Routing a ticket to the right team.", "2")])],
 "Part 2": [("Key terms: the parts", [
    ("Knowledge tool", "A function that searches the company documents and returns clauses with their ids. RAG becomes one tool on the menu.", "A lookup in the knowledge base.", "3"),
    ("Tool hub", "One menu that mixes MCP tools from the server with our own functions. The agent cannot tell which is which.", "A gateway in front of several services.", "4"),
    ("System prompt", "The assistant's role, rules and answer format, sent before every step. The identity is data you can edit.", "Task assignment plus authorisations.", "5")])],
 "Part 3": [("Key terms: business concerns (1 of 2)", [
    ("Structured response", "An answer returned as fields (answer, tools used, checked, needs a human), not just free text, so an app can act on it.", "An IDoc instead of a free-text email.", "7"),
    ("Answer check", "Code that tests the answer: every number and every citation must appear in the tool results.", "A validation rule on entry.", "7"),
    ("Token", "A piece of text the model reads or writes. More tokens means more cost and more waiting.", "A metered usage unit.", "8")]),
  ("Key terms: business concerns (2 of 2)", [
    ("Local model", "A model that runs on your own laptop or server, so the data does not leave your control.", "The binder never leaves the building.", "9"),
    ("Human oversight", "A person reviews or approves what matters, such as any change. The response says when a human is needed.", "A release strategy.", "9")])],
 "Part 4": [("Key terms: the capstone", [
    ("Capstone", "One assistant that uses everything from the four days: prompt, knowledge, agent, tools, checks and guardrails.", "An end-to-end solution design.", "10"),
    ("Test plan", "Direct, reworded and missing questions, scored by code, re-run after every change.", "A UAT script.", "11"),
    ("Pitch", "Five minutes: one SAP process, the prompt you used, a live demo, and the guardrails you would require.", "A solution walkthrough for the sponsor.", "12")])],
}
D.tags = [("neo runs on", "Local model"), ("cell 1:", "Prompt-only"), ("cell 2:", "Router"), ("which approach fits", "Simplest approach"), ("cell 3:", "Knowledge tool"), ("what a chunk looks like", "Knowledge tool"),
  ("cell 4:", "Tool hub"), ("cell 5:", "System prompt"), ("five questions every sponsor", "Human oversight"), ("cell 7: a checked", "Structured response"), ("cell 7: the check", "Answer check"),
  ("cell 8:", "Token"), ("cell 9:", "Local model"), ("capstone: your", "Capstone"), ("cell 10:", "Capstone"), ("cell 11:", "Test plan"), ("cell 12:", "Pitch")]

# ------------------------------------------------------------------------------------------ START
A = "Start"
D.add(A, """<div class="body"><div class="label" style="color:var(--accent)">Day 4 · Class 8 · Putting it all together</div>
<h1>One <span class="mono">assistant</span><br>for SAP</h1>
<p class="lead" style="margin-top:0">We have every piece: prompts, knowledge, agents, tools and guardrails. Today we <b>assemble them</b>, check the result, and learn <b>where to start</b>.</p>
<div><span class="pill">Start simple</span><span class="pill">Assemble the parts</span><span class="pill">Business concerns</span><span class="pill">Capstone</span></div></div>""" + HINT,
 "Before class: open Day_4/Class_8_Capstone/notebooks/Class_8_Putting_It_All_Together.ipynb, choose the .venv kernel and run CELL S. Check that NotebookLM and Antigravity are approved for mock data, or use the notebook alternatives.", "title")
D.add(A, slide("This morning in 30 seconds", grid(3, card("MCP = USB-C for AI", "Tools, resources, prompts. One standard plug.", "🔌"), card("Guardrails", "Read-only first · limits · a person approves changes.", "🛡️"), card("Fixed rules", "Normal automation, not an agent.", "⚙️")),
  lead("Neo can now <b>plug into systems safely</b>. But each piece so far was a separate demo.")), "Quick recap of Class 7.")
D.add(A, slide("The request", chat(me("Can we have one assistant for the SAP operations team? It should answer from our policies and from live SAP data, and never change anything on its own."), neo("…", "bad")) +
  lead("A real request is <b>not one demo</b>. It needs several pieces working together, and a way to <b>trust</b> the result.")), "Set the scene: a sponsor asks for something that needs all four days.")
D.add(A, """<div class="hero"><div class="orb">Neo</div><div><div class="label" style="color:var(--accent)">Neo, today</div><h2 style="margin-bottom:18px">All the parts, one assistant</h2>
<p class="f">✍️ <b>Prompt</b> and rules (Classes 3–4)</p><p class="f">📖 <b>Knowledge</b> from documents (Class 5)</p><p class="f">🧠 An <b>agent</b> that decides the steps (Class 6)</p><p class="f">🔌 <b>Tools</b> through MCP (Class 7)</p></div></div>""",
 "Neo is the same character, now with everything.")
D.add(A, """<div class="body center"><div class="big">Start <em>simple</em>.<br>Add only what the problem <em>needs</em>.</div>
<p class="lead f">Prompt first. Then knowledge. Then an agent. That order saves money, time and risk.</p></div>""", "The one idea for the afternoon. Pause here.")
D.add(A, """<h2>Today's plan · 2 hours</h2><div class="body"><table class="agenda">
<tr><th>Time</th><th>Topic</th><th>Question</th><th>Cells</th></tr>
<tr><td class="t">0:00</td><td>1 · Start simple</td><td>Which approach does the job?</td><td class="m">S, 1–2</td></tr>
<tr><td class="t">0:20</td><td>2 · Assemble the parts</td><td>How do the pieces fit?</td><td class="m">3–6</td></tr>
<tr><td class="t">0:55</td><td>3 · Business concerns</td><td>Can we trust it, afford it, and keep it private?</td><td class="m">7–9</td></tr>
<tr><td class="t">1:20</td><td>4 · Capstone</td><td>Build, test and pitch</td><td class="m">10–12</td></tr></table></div>""", "Part 4 is 40 minutes of team work, then the 5-minute pitches.")
D.add(A, slide("Neo runs on this laptop", '<div class="g2" style="align-items:center">' + card("Two models and a server", "A <b>chat model</b>, an <b>embedding model</b> for the documents, and the <b>MCP server</b> from this morning. Nothing leaves the laptop.", "💻") +
  '<div class="f">' + msg("s", "Ollama is running at localhost:11434") + '<div style="height:12px"></div>' + msg("s", "Main model · Small model · <b>Embed model</b> found") + '<div style="height:12px"></div>' + msg("s", "Neo replies <b>Connection OK</b>") + '<div style="height:12px"></div>' +
  msg("s", "MCP server: <b>" + INFO["title"] + "</b> · " + str(len(TOOLS)) + " tools") + "</div></div>"), "Run CELL S. The same server file as Class 7, started with writes enabled; a person-approval gate protects it later.", cell="S")

# ------------------------------------------------------------------------------------------ PART 1
B1 = "1 · Start simple"
D.divider("Part 1", "Start simple", "Which approach does the job?", "The simplest one that works.", B1, divnote("Two demos: a prompt on its own, and letting the model choose."))
D.add(B1, life_ai("<div class='emoji'>🧰</div><p>You do not write a custom ABAP program when a <b>standard report</b> already answers the question.</p><p>You pick the <b>simplest tool that works</b>.</p>",
                  "<div class='emoji'>🧭</div><p>Do the same for AI: a <b>prompt</b> if the text is in front of you, <b>RAG</b> if the answer is in documents, an <b>agent</b> only for multi-step work with systems.</p>", "In your SAP world", "With AI"), "Set the rule before any demo.")
D.add(B1, slide("Which approach fits?", table(["The need", "Use", "Example"], [["Summarise, draft, classify text", "<b>A good prompt</b>", "One-line summary of a supplier email"], ["Answer from company documents", "<b>RAG</b>", "Who approves a PO above ₹10 lakh?"],
  ["Multi-step task using systems", "<b>An agent</b>", "Why is PO 4500012348 blocked and who is the contact?"]]), lead("Move right <b>only when the problem needs it</b>. Each step adds cost, time and risk.")), "Walk the table row by row.")
D.add(B1, slide("Cell 1: prompt only", '<div class="g2" style="align-items:start"><div class="out f"><div class="who">The input</div>“Hello, the truck for PO 4500012346 was held up by heavy rain near Pune. We can deliver on Monday instead of Friday. Regards, Rahul”</div>' +
  "<div>" + qa("Summarise in one sentence.", "The truck was held up by rain; delivery moves from Friday to Monday.", "good") + "</div></div>", exp("Target behaviour · your model's wording will differ")),
 "Run CELL 1. Three jobs (summarise, classify, draft), no documents and no tools. Cheapest and fastest.", cell=1)
D.add(B1, slide("Cell 2: can the model choose?", table(["The need", "We expect"], [[esc(n), "<b>" + a + "</b>"] for n, a in NEEDS]), exp("Expected values are exact · the notebook prints ✅ or ⚠️ for what your model chose")),
 "Run CELL 2. A ⚠️ is the lesson: choosing the approach is itself a decision to test. In a real project a person usually makes this choice once, per use case.", cell=2)
D.add(B1, slide("SAP use cases for the assistant", table(["Use case", "A question we can ask", "What it needs", "Sources"], [[a, b, c, "<b>" + d + "</b>"] for a, b, c, d in UC]), lead("Notice which need <b>only documents</b>, which need <b>only live data</b>, and which need <b>both</b>.")),
 "These are the five use cases in Cell 10. The Sources column says whether the answer comes from MCP tools, RAG documents, or both.")

# ------------------------------------------------------------------------------------------ PART 2
B2 = "2 · Assemble"
D.divider("Part 2", "Assemble", "From four pieces to one", "Knowledge + tools + rules + an agent.", B2, divnote("Four demos: knowledge as a function, one tool menu, the rules, and the agent."))
D.add(B2, slide("The full picture", '<div class="pipe"><div class="pr"><span class="pc">User</span><span>A question in plain words</span></div>' +
  '<div class="pr"><span class="pc">Prompt &amp; rules</span><span>Role, rules, answer format <b>(Classes 3–4)</b></span></div>' +
  '<div class="pr"><span class="pc">Agent</span><span>Decides the steps, one at a time <b>(Class 6)</b></span></div>' +
  '<div class="pr two"><span class="pc">Sources</span><span class="sub">📖 Company knowledge via <b>RAG</b> (Class 5)</span><span class="sub">🔌 System tools via <b>MCP</b> (Class 7)</span></div>' +
  '<div class="pr"><span class="pc">LLM</span><span>Writes the answer <b>(Class 2)</b></span></div>' +
  '<div class="pr end"><span class="pc">Response</span><span><b>Checked, structured</b> response back to the user</span></div></div>'),
 "This is the whole afternoon on one slide. Each row is a class they already did. Cells 3 to 7 build it, in this order.")
D.add(B2, slide("Which tool for which part?", table(["Part", "Tool", "What teams do"], [["🧠 Brain", "Ollama", "Use the local model"], ["📖 Knowledge", "NotebookLM", "Load the team's policy and process documents"],
  ["✍️ Prompts", "Ollama / VS Code", "Write the role, rules and output format"], ["🔌 Agent + tools", "Antigravity + MCP", "Answer multi-step questions on the mock SAP data"]]),
  lead("The notebook has a local alternative for each: " + mono("Cell 3") + " for knowledge, " + mono("Cells 5–6") + " for prompts and agent.")), "NotebookLM and Antigravity are cloud tools: approval first, mock data only. The notebook cells work without them.")
D.add(B2, slide("Cell 3: knowledge as a function", '<div class="g2" style="align-items:start">' + pycode('''def search_policy(query, top=3):
    q = embed(query)
    ranked = sorted(store,
        key=lambda s: cosine(q, s[1]),
        reverse=True)[:top]
    return [{"id": c["id"], "text": c["text"]}
            for c, v in ranked]''', (0,)) +
  '<div class="out f"><div class="who">Notebook output · exact</div><b>' + str(len(CHUNKS)) + "</b> chunks from <b>" + str(len(DOCW)) + "</b> documents stored.<br>RAG sends only <b>3</b> of them to the model, not all " + str(len(CHUNKS)) + ".</div></div>", exp("exact counts · the scores printed under it depend on your embedding model")),
 "Run CELL 3. Same four steps as Class 5. The new idea: the search is a function that returns clauses with ids, so it can sit on a tool menu.", cell=3)
D.add(B2, slide("What a chunk looks like", '<div class="chunk f"><div class="ch">id <b>' + esc(C62["id"]) + '</b></div><div class="cb"><span class="tg">[Procurement_Policy · 6. INVOICE DISPUTES]</span> 6.2 A price variance above 1% between the PO and the invoice blocks the invoice for review.</div></div>' +
  lead("The <b>id</b> becomes the citation. Only " + str(len(C62["text"].split())) + " words, against " + str(TOTAL_WORDS) + " for all " + str(len(DOCW)) + " documents.")), "This is the clause the capstone question needs.", cell=3)
tool_rows = [(t["name"], "MCP server") for t in TOOLS] + [("search_policy", "Knowledge (RAG)")]
D.add(B2, slide("Cell 4: one menu, two sources", '<div class="g2" style="align-items:start"><div class="out f"><div class="who">Notebook output · exact</div>' +
  "<br>".join("• " + mono(n) + " ← " + ("<b>" + s + "</b>" if "RAG" in s else s) for n, s in tool_rows) + "</div>" +
  card("To the agent, both are just tools", "Live SAP data comes through <b>MCP</b>. Company documents come through <b>RAG</b>. One menu, one loop.", "🧩", "acc") + "</div>", exp("exact")),
 "Run CELL 4. The ToolHub class puts the MCP tools and our own function on one menu.", cell=4)
D.add(B2, slide("Cell 5: the assistant's identity is data", '<div class="g2" style="align-items:start">' + pycode('''ROLE = "You are the SAP Operations Assistant…"
RULES = [
  "Use ONLY facts returned by your tools.",
  "Cite the clause id, e.g. [Procurement_Policy §6.2].",
  "You may only READ. Ask a person to approve a ticket.",
  "If it is missing, say what is missing.",
]
FORMAT = "At most four short sentences."''', (1, 2, 3)) +
  "<div>" + card("Role", "Who the assistant is.", None, "acc", num="1") + '<div style="height:12px"></div>' + card("Rules", "What it must and must not do.", None, "acc", num="2") + '<div style="height:12px"></div>' + card("Format", "How the answer looks.", None, "acc", num="3") + "</div></div>"),
 "Run CELL 5. Edit a rule, run it again, and the behaviour changes. This is Class 3 and 4 in one place.", cell=5)
D.add(B2, slide("Cell 6: one question, four tools", table(["Step", "The agent asks for", "Comes from", "What comes back"], [
  ["1", mono("get_order"), "MCP", ORD48["status"] + ", " + ORD48["block_reason"].lower() + ", " + inr(ORD48["value_inr"])], ["2", mono("check_approval"), "MCP", APPR[1200000]["approver"] + " (policy " + APPR[1200000]["policy"] + ")"],
  ["3", mono("search_policy"), "RAG", "<b>target:</b> Procurement_Policy §6.2"], ["4", mono("get_vendor"), "MCP", VENDOR["V300"]["contact"] + ", " + VENDOR["V300"]["email"]]], mono=()),
  exp("Rows 1, 2 and 4 are exact (from the server) · row 3 is a target, because it depends on your embedding model · the order may differ")),
 "Run CELL 6. The question: PO 4500012348 is blocked. Why, who must approve it, what does our policy say about price variance, and who is the vendor contact? Nobody wrote this sequence.", cell=6)
D.add(B2, slide("Who provided each fact?", grid(3, card("From the prompt", "The role, the rules and the answer format.", "✍️", "acc"), card("From MCP tools", "The order, the approver and the vendor: live SAP data.", "🔌", "ok"),
  card("From RAG", "The policy clause on price variance, with its id.", "📖", "ok")), lead("The LLM <b>writes</b>. It does not <b>know</b>. Every fact has a source we can point to.")), "This is why the answer can be checked in Part 3.", cell=6)

# ------------------------------------------------------------------------------------------ PART 3
B3 = "3 · Business concerns"
D.divider("Part 3", "Business concerns", "A demo is not a solution", "Accuracy · cost · speed · privacy · oversight.", B3, divnote("Three demos: a checked response, cost and speed, and privacy with oversight."))
D.add(B3, slide("Five questions every sponsor asks", table(["Concern", "What we did", "Cell"], [["Accuracy", "Code checks every number and citation against the tool results", "7"], ["Cost", "Count model calls and tokens for each approach", "8"],
  ["Speed", "Time each approach, then start with the simplest", "8"], ["Data privacy", "Local model; only 3 chunks sent; mock data in cloud tools", "9"], ["Human oversight", "A person approves any change", "9"]], mono=(2,))), "Each row is answered by a cell in this part.")
D.add(B3, slide("Cell 7: a checked, structured response", '<div class="g2" style="align-items:start">' + pycode('''{
  "question": "PO 4500012348 is blocked…",
  "answer": "PO 4500012348 (₹12,00,000)…",
  "tools_used": ["get_order", "check_approval",
                 "search_policy", "get_vendor"],
  "steps": 5,
  "checked": true,
  "problems": [],
  "needs_human": false
}''', (5, 7)) + card("Fields, not free text", "An app can read " + mono("checked") + " and " + mono("needs_human") + " and decide what to do next.", "🧾", "acc") + "</div>", exp("Shape is exact · the values come from your live run")),
 "Run CELL 7. The response shape is fixed. The answer text and tools used come from the live run.", cell=7)
D.add(B3, slide("Cell 7: the check catches a made-up answer", '<div class="g2" style="align-items:start"><div class="out ok f"><div class="who">A grounded answer</div>' + esc(GOOD) + "<br><br>→ problems: " + mono("[]") + "</div>" +
  '<div class="out bad f"><div class="who">A made-up answer</div>' + esc(FAKE) + "<br><br>→ " + mono(esc(PROBLEMS[0])) + "<br>→ " + mono(esc(PROBLEMS[1])) + "</div></div>", exp("exact · the checker is the notebook's own code, run on the real tool results")),
 "Run CELL 7. The checker is plain code: every number and citation must appear in the tool results. A flagged answer sets needs_human.", cell=7)
D.add(B3, slide("Cell 8: cost and speed", table(["Approach", "Model calls", "Tokens", "Waiting"], [["Prompt only", "1", "few", "seconds"], ["RAG", "1 (plus the embedding)", "more: 3 clauses added", "seconds"], ["Agent + tools", "<b>5</b> for the capstone question (4 tools + the answer)", "<b>many</b>: the whole conversation is re-sent each step", "<b>longest</b>"]]) +
  lead("The notebook prints your real numbers. With a paid cloud model, <b>tokens are money</b>."), exp("Pattern · the call count for the agent follows from four tool requests plus one answer · the notebook prints your real tokens and seconds")),
 "Run CELL 8. Exact numbers depend on your model and laptop. The shape is the lesson: more steps, more tokens, more waiting.", cell=8)
D.add(B3, slide("Cell 9: privacy and oversight", grid(2, card("Privacy", "Local model: nothing leaves this laptop. RAG sends <b>3 of " + str(len(CHUNKS)) + " chunks</b>. Cloud tools (NotebookLM, Antigravity): <b>mock data only</b>, after approval.", "🔒", "ok"),
  card("Oversight", "Reading runs alone. <b>Changing waits for a person.</b> The response carries " + mono("needs_human") + ".", "🙋", "ok")), lead("The same approval gate as this morning. <b>Nothing new to learn, only to apply.</b>")), "Run CELL 9. It prints where the model runs, then triggers the approval prompt for a ticket request.", cell=9)
D.add(B3, slide("What would you require?", '<div class="pairs"><div><div class="label">Before a pilot</div><ul class="yes f"><li>Read-only tools first</li><li>Answers checked in code</li><li>A step limit</li><li>A test plan that re-runs</li></ul></div>' +
  '<div><div class="label">Before it touches live data</div><ul class="no f"><li>IT and security approval</li><li>A person approves every change</li><li>No real vendor or bank data in cloud tools</li><li>An owner for the document library</li></ul></div></div>' + lead("Keep this list for your pitch.")), "Collect the room's list before showing it. They reuse it in Cell 12.")

# ------------------------------------------------------------------------------------------ PART 4
B4 = "4 · Capstone"
D.divider("Part 4", "Capstone", "Your SAP Operations Assistant", "Pick a process. Build it. Test it. Pitch it.", B4, divnote("40 minutes of team work (Cells 10 to 12), then 5-minute team presentations."))
D.add(B4, slide("Capstone: your SAP Operations Assistant", table(["Part", "Tool", "What teams do"], [["Brain", "Ollama", "Use the local model"], ["Knowledge", "NotebookLM", "Load the team's policy and process documents"], ["Prompts", "Ollama / VS Code", "Write the assistant's role, rules and output format"],
  ["Agent + tools", "Antigravity + MCP", "Answer multi-step questions using the mock SAP data"]]), lead("The notebook (Cells 10–12) lets every team do all four <b>without any cloud tool</b>.")), "Teams of 3 or 4. Cloud tools only if approved; the notebook covers the same ground locally.")
D.add(B4, slide("Four tasks · 40 min", '<div class="g2"><div>' + steps([("Pick one SAP process", "Cell 10: five to choose from")]) + steps([("Ask a multi-step question", "Check the tools, the answer and the response")]) + "</div><div>" +
  steps([("Test it", "Cell 11: five questions scored in code")]) + steps([("Fill in your pitch card", "Cell 12: the process, prompt, demo and guardrails")]) + "</div></div>"), "Remind them to change only the lines marked ← change me.", cell="10–12")
D.add(B4, slide("Cell 10: pick a process", '<div class="g2" style="align-items:start">' + pycode('''USE_CASES = {
  "invoice exception": "PO 4500012348 has a price variance…",
  "PO delay analysis": "Which orders for plant 2000 are delayed…",
  "IDoc error triage": "An IDoc is stuck at status 51…",
  "vendor query":      "Who is the vendor contact for PO…",
  "month-end close":   "Which orders for plant 1000 are blocked…",
}
MY_USE_CASE = "invoice exception"    # ← change me''', (7,)) +
  "<div>" + table(["Use case", "Sources"], [[a, "<b>" + d + "</b>"] for a, _, _, d in UC]) + "</div></div>", exp("Sources are exact (from the data and documents) · the answer wording will differ")),
 "Run CELL 10. Let teams try more than one. Which need only documents, which only MCP, which both?", cell=10)
D.add(B4, slide("Cell 11: test your assistant", table(["Type", "Question", "Must use", "Answer has"], [[k, esc(q), mono(t) if t != "none" else "no tool", w] for k, q, t, w in TESTS]), exp("Expected values are exact · the notebook prints ✅ or ❌ and a score out of 5")),
 "Run CELL 11. Three kinds of test, as in Class 5. A ❌ is a good lesson: wrong tool, wrong clause retrieved, or the model ignored the result.", cell=11)
D.add(B4, slide("Worksheet: reading a ❌", grid(3, card("Wrong tool", "The agent chose a tool that cannot answer. Fix: the tool descriptions.", "🔧", "warn"), card("Wrong clause", "Retrieval did not return the right id. Fix: chunking or the embedding model.", "🔎", "warn"),
  card("Ignored the result", "The right facts were there. Fix: the rules, or a stronger model.", "👀", "warn")), lead("The printed " + mono("tools") + " tell you <b>where to look</b>.")), "Celebrate a wrong answer: it tells you where to look.", cell=11)
D.add(B4, slide("Cell 12: the five-minute pitch", table(["#", "Say", "Where it comes from"], [["1", "<b>The process</b>", mono("MY_USE_CASE")], ["2", "<b>The prompt</b> you used", mono("ROLE") + " and " + mono("FORMAT")], ["3", "<b>A live demo</b>", mono("MY_QUESTION") + " and its tools"],
  ["4", "<b>The guardrails</b> you would require", mono("GUARDRAILS_I_REQUIRE")]], mono=()) + lead("The notebook prints your card. <b>Five minutes each.</b>")), "Run CELL 12. The card fills itself from what the team built.", cell=12)
D.add(B4, slide("Your turn on stage", grid(2, card("Show", "One SAP process. The prompt. A live demo, with the tools it called.", "🎤", "acc"), card("Say", "The guardrails you would require, and where you would start on Monday.", "🛡️", "acc")),
  lead("Judge each other on one question: <b>would I trust this answer?</b>")), "Five minutes per team. Ask the room to listen for the guardrails.")
D.add(B4, slide("Common myths", table(["They might think…", "Better to say…"], [["More parts means a better solution", "<b>Start simple.</b> Add a part only when the problem needs it."], ["The agent is always right", "It can pick the wrong tool. <b>Check the answer in code.</b>"],
  ["RAG, MCP and agents are rivals", "They are <b>parts</b> of one assistant, each with a job."], ["A demo means it is ready", "A demo is not a solution. Plan for <b>accuracy, cost, privacy and oversight</b>."]])), "Use as a quick correction list.")
D.add(B4, slide("The assistant in one page", '<div class="g2"><div class="card f"><h3>The parts</h3><p><b>Prompt and rules</b> · <b>RAG</b> for documents · <b>MCP</b> for live data · an <b>agent</b> to decide the steps · an <b>answer check</b>.</p></div>' +
  '<div class="card f"><h3>Where to start</h3><p><b>1</b> A good prompt<br><b>2</b> Add documents (RAG)<br><b>3</b> Add an agent with tools<br>Only when the problem needs it.</p></div></div>' + lead("Business concerns: <b>accuracy · cost · speed · privacy · oversight</b>.")), "This is the participant handout.")

# ------------------------------------------------------------------------------------------ WRAP-UP
D.add("Wrap-up", slide("Keep learning with the same free tools", '<div class="flow"><div class="st f"><h3>1 · Prompts</h3><p>Ollama + VS Code. Save your best role, rules and format.</p></div><div class="ar f">→</div>' +
  '<div class="st f"><h3>2 · Knowledge</h3><p>RAG on <b>approved</b> documents: NotebookLM or this notebook.</p></div><div class="ar f">→</div>' +
  '<div class="st f"><h3>3 · Tools</h3><p>An MCP server over a <b>read-only</b> export. Antigravity or VS Code.</p></div><div class="ar f">→</div>' +
  '<div class="st f"><h3>4 · Pilot</h3><p>Guardrails, tests and approval from IT. Then one real process.</p></div></div>', lead("The step-by-step roadmap is in " + mono("Class_8_Capstone/ROADMAP.md") + ".")), "Roadmap: how to keep learning with the same free tools. Each step reuses something from the course.")
D.add("Wrap-up", """<h2>Quick quiz</h2><div class="body"><div class="quiz">
<div class="q f">When is a prompt enough?<span class="a">When the text is in front of you: summarise, draft, classify.</span></div>
<div class="q f">When do you add RAG?<span class="a">When the answer is in company documents.</span></div>
<div class="q f">When do you add an agent?<span class="a">For multi-step tasks that need systems and several tools.</span></div>
<div class="q f">How do you check an answer in code?<span class="a">Every number and citation must appear in the tool results.</span></div>
<div class="q f">Name three business concerns.<span class="a">Accuracy, cost, speed, data privacy, human oversight.</span></div>
<div class="q f">What did the router and the test plan teach?<span class="a">Choosing the approach is a decision to test.</span></div></div></div>""", "Ask each question aloud before revealing the answer.")
D.add("Wrap-up", slide("Remember three things", grid(3, card("Start simple", "Prompt, then knowledge, then an agent. Only when needed.", None, "acc", num="1"), card("One assistant, known parts", "Prompt + agent + RAG + MCP + a checked answer.", None, "acc", num="2"),
  card("Business concerns decide", "Accuracy, cost, speed, privacy, oversight.", None, "acc", num="3"))), "Three takeaways.")
D.add("Wrap-up", """<div class="body center"><div class="label" style="color:var(--accent)">The end of the course</div><div class="big">You can now <em>build it</em>,<br><em>test it</em> and <em>explain it</em>.</div>
<p class="lead">Take one SAP process back to your team. Start with a prompt. Add only what it needs. <b>Keep a person in the loop.</b></p></div>""", "Close the course. Invite questions and point to ROADMAP.md.", "title")

path, n = D.write("Class_8_Putting_It_All_Together_Slides.html", "Class 8 · Putting It All Together: an AI Agent for SAP", C8 + "/slides")
print("Class 8 deck:", n, "slides,", D.term_total, "key terms ->", path)
close_servers()
