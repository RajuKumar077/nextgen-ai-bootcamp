"""Builds the two Day 4 notebooks (no outputs saved). Run:  python build_notebooks.py   (needs nbformat)"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nbformat
from d4_common import AGENT_DEFAULTS_SRC, MENU_SRC, LOOP_SRC, APPROVAL_SRC, CHECK_SRC, CUT_SRC, C7, C8

nbf = nbformat.v4


def md(t): return nbf.new_markdown_cell(t.strip("\n"))
def code(t): return nbf.new_code_cell(t.strip("\n"))


def save(cells, path, title):
    nb = nbf.new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"display_name": "Python 3 (.venv)", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python"}
    nb.metadata["title"] = title
    nbformat.write(nb, path)
    tagged = [l for c in cells if c.cell_type == "code" for l in c.source.splitlines()[:1] if "▶ CELL" in l]
    print(os.path.basename(path), "| cells:", len(cells), "| code cells tagged:", len(tagged))


TROUBLE = """
---
## 🛠️ Trainer troubleshooting
| Message | Cause | Fix |
|---|---|---|
| `Cannot reach Ollama at http://localhost:11434` | Ollama isn't running | Windows: Start menu → **Ollama**. Mac: open the Ollama app. Or in a terminal: `ollama serve` |
| `Model '…' is not downloaded` | The model in `bootcamp_config.json` isn't pulled | `ollama pull <name>` (see `ollama list`) |
| `ModuleNotFoundError: bootcamp_llm` or `mcp_client` | The notebook is not running from its own folder | Open the **Day_4** folder as the workspace, then pick the **`.venv`** kernel |
| `The MCP server stopped before answering` | The server file crashed or the path is wrong | Run it by hand to see the error: `python Class_7_MCP_Guardrails/mcp_server/sap_orders_server.py` (press Ctrl+C to stop) |
| `Blocked by a guardrail: 'create_ticket' …` | The read-only gate did its job | Expected in CELL 8. CELL 9 swaps in human approval |
| `This server is READ-ONLY` | The server was started without `--allow-write` | Expected until CELL 9, which restarts it with writes enabled |
| `The model did not return valid JSON` | Small models sometimes break the format | Run the cell again. This is a real lesson: agents need validation |
| The agent picks the wrong tool | Normal with small models | Try a larger `model` in the config (7B or 8B follows tool menus better) |
| Antigravity / VS Code do not list the server | The config has no absolute path for this laptop | Run `python setup/make_mcp_config.py`, then restart the editor |
"""

# =====================================================================================================
#                                             CLASS 7
# =====================================================================================================
c7 = []
c7.append(md("""
# 🔌 Class 7: Agents in Action: Tools, MCP & Guardrails
### One standard plug, and how we keep agents safe · Day 4 · Morning · 2 hours

**Same story.** Yesterday Neo learned to use three tools that *we* wired in by hand. A real company has dozens of systems, and every new one would need its own custom connection.

**Today's question:** *If every new system needs its own custom connection, it doesn't scale. How does the industry connect agents to systems in a standard way, and how do we keep them safe?*

| Part | Topic | Cells |
|---|---|---|
| A | The problem and the plug (MCP) | S, 1 |
| B | The 3 things a server offers | 2–4 |
| C | The agent over MCP | 5–7 |
| D | Guardrails | 8–10 |
| E | Your turn | 11–12 |

> 💡 **Key terms come first.** Each part starts with a key-terms slide. Then you run the cells.
> 🔒 All data is **mock** (fictional company *Nova Industries*). The "SAP" here is two CSV files behind a small **MCP server**: a Python file the trainer prepared (`mcp_server/sap_orders_server.py`).
"""))

c7.append(md("## ⚙️ ▶ CELL S: Setup\nChecks that Ollama is running, then **starts the mock SAP Orders MCP server** and shakes hands with it. Run once."))
c7.append(code(r'''
# ▶ CELL S · SETUP: check Ollama, then start the mock SAP Orders MCP server. Run once.
import sys, os, re, json
sys.path.insert(0, "../../shared")            # where bootcamp_llm.py and mcp_client.py live
from bootcamp_llm import *
from mcp_client import *

SERVER = [sys.executable, "../mcp_server/sap_orders_server.py"]      # the MCP server: a Python file the trainer prepared

def connect(*flags):
    """Start the MCP server as a child process and shake hands with it."""
    return McpClient(SERVER + list(flags))

check_setup()
print("🤖 Neo says:", ask_ai("Reply with exactly these words: Connection OK", temperature=0, max_tokens=10))
client = connect()                            # read-only by default
print(f"🔌 Connected to MCP server: {client.server_info['title']} (v{client.server_info['version']})")
'''))

c7.append(md("""
---
# A · The problem and the plug
**In real life:** SAP does not have a custom cable to every other system. It uses **standard interfaces** (IDoc, OData, RFC), so a new system plugs into a known shape.

Agents had the same problem. With 4 agents and 5 systems, custom connections mean **4 × 5 = 20** pieces to build and maintain. With one standard plug it is **4 + 5 = 9**.

> 🔌 **MCP (Model Context Protocol) = "USB-C for AI".** One standard plug, so any AI agent can connect to any system that speaks it.

### ▶ CELL 1: Connect, and ask the server what it offers
"""))
c7.append(code(r'''
# ▶ CELL 1 · CONNECT: the handshake, then DISCOVER what the server offers (nobody typed this list)
print("Server   :", client.server_info["title"], "· version", client.server_info["version"])
print("Protocol :", client.protocol)
print("Offers   :", list(client.capabilities))

tools = client.list_tools()
print(f"\n{len(tools)} tools discovered:")
for t in tools:
    print(" •", t["name"])
'''))
c7.append(md("> 🤝 **initialize** is the handshake: client and server agree on the protocol and on what each side can do. Then **tools/list** is *discovery*. Yesterday we typed the tool menu by hand (Class 6, Cell 3). Today **the server tells us**."))

c7.append(md("""
---
# B · The 3 things a server offers
**Tools** (actions the AI may request) · **Resources** (data to read) · **Prompts** (ready-made requests).

### ▶ CELL 2: Tools: what they do, and whether they only read
"""))
c7.append(code(r'''
# ▶ CELL 2 · TOOLS: each one says what it needs and whether it only READS
for t in tools:
    label = "🔍 read-only" if t["annotations"]["readOnlyHint"] else "✏️  changes data"
    print(f"{label:<15} {t['name']}({', '.join(t['inputSchema']['properties'])})")

print("\nCalling a tool by hand:")
print(client.call_tool("get_order", {"po_number": "4500012345"}))
print("\nA tool problem comes back as a readable message, not a crash:")
print(client.call_tool("get_order", {"po_number": "4500099999"}))
'''))
c7.append(md("> 🏷️ Every tool carries a **read-only label**. That label is what lets a program decide *when to ask a person* (Part D). Notice the one tool that **changes data**.\n\n### ▶ CELL 3: Resources and prompts"))
c7.append(code(r'''
# ▶ CELL 3 · RESOURCES (data to read) and PROMPTS (ready-made requests)
print("RESOURCES:")
for r in client.list_resources():
    print(f" • {r['uri']:<26} {r['name']}")
print("\norders://summary →", client.read_resource("orders://summary"))

print("\nPROMPTS:")
for p in client.list_prompts():
    print(f" • {p['name']:<22} {p['description']}")
print("\nThe 'blocked_orders_report' prompt for plant 1000 turns into this request:\n")
print(client.get_prompt("blocked_orders_report", {"plant": "1000"}))
'''))
c7.append(md("> 📚 A **resource** is something to *read* (like a report). A **tool** is something to *do* (like a BAPI). A **prompt** is a *saved request* the server offers.\n\n### ▶ CELL 4: What one tool call looks like on the wire"))
c7.append(code(r'''
# ▶ CELL 4 · ON THE WIRE: one tool call is two plain JSON messages (the "id" number will differ on your screen)
client.wire.clear()
client.call_tool("check_approval", {"value_inr": 1200000})
for direction, message in client.wire:
    print(direction, json.dumps(message, ensure_ascii=False), "\n")
'''))
c7.append(md("> 🔎 **→** is the request, **←** is the result. No magic: JSON in, JSON out. Any agent that speaks this can use any server that speaks it. *That is the whole idea.*"))

c7.append(md("""
---
# C · The agent over MCP
Same agent as Class 6, with two changes: the **menu comes from the server**, and a **gate** sits between "the AI asked" and "the program runs it".

### ▶ CELL 5: The tool menu, built from discovery
"""))
c7.append(code("# ▶ CELL 5 · THE MENU: built from what the server told us, plus the instructions\n" + AGENT_DEFAULTS_SRC + "\n" + MENU_SRC + "\nprint(system_prompt())\n"))
c7.append(md("> 📋 Compare with Class 6, Cell 3: there we typed `TOOLS = {...}`. Now `offered()` **asks the server**. Add a tool to the server and it appears on this menu by itself.\n\n### ▶ CELL 6: The loop: think → act → observe, over MCP"))
c7.append(code("# ▶ CELL 6 · THE AGENT LOOP over MCP: think → act → observe → repeat\n" + LOOP_SRC + r'''
QUESTION = "Which orders for Plant 1000 are blocked and why?"      # ← change me
_ = run_agent(QUESTION)
'''))
c7.append(md("> 🔁 The loop is the one from Class 6. Look for the **tool the agent chose** and the **facts in the OBSERVE line**. Expected: four orders on plant 1000 (`…345` credit check, `…348` price variance, `…352` missing goods receipt, `…355` credit check). The wording of the THINK lines will differ on your model.\n\n### ▶ CELL 7: Plug and play: the server gets a new tool"))
c7.append(code(r'''
# ▶ CELL 7 · PLUG AND PLAY: the trainer adds a tool to the SERVER. We change NO agent code.
print("Tools before:", len(client.list_tools()))
client.close()
client = connect("--with-scorecard")                  # the same server file, now offering one more tool
print("Tools after :", len(client.list_tools()), "→ new:", [t["name"] for t in client.list_tools() if t["name"] == "vendor_scorecard"])

_ = run_agent("Which vendor has the highest total order value, and how many of its orders are delayed or blocked?")
'''))
c7.append(md("> ✅ Expected: **Chennai Components**, ₹27,00,000 in total, 2 delayed and 1 blocked. Yesterday (Class 6, Cell 10) we edited the notebook to add a fourth tool. **Today we edited nothing here.** That is plug and play."))

c7.append(md("""
---
# D · Guardrails
An agent that can act needs limits. Four to know:
1. **Read-only first**: start with tools that cannot change anything.
2. **Allow-list**: the agent only gets the tools it needs.
3. **Step limit**: no endless loops.
4. **Human approval** before any change, like an SAP **release strategy**.

### ▶ CELL 8: Guardrails 1–3 in action
"""))
c7.append(code(r'''
# ▶ CELL 8 · GUARDRAILS 1-3: read-only first · allow-list · step limit
print("1) READ-ONLY FIRST: the agent asks for a change, the gate says no")
print("  ", execute({"tool": "create_ticket", "args": {"po_number": "4500012345", "note": "Chase the credit check"}}))

print("\n2) ALLOW-LIST: this agent gets only two tools")
ALLOWED = {"get_order", "check_approval"}
try:
    print("   menu :", list(offered()))
    print("  ", execute({"tool": "list_orders", "args": {}}))
finally:
    ALLOWED = None                                   # back to the full menu

print("\n3) STEP LIMIT: a limit of 1 for a question that needs two steps")
_ = run_agent("Who must approve PO 4500012348?", max_steps=1)
'''))
c7.append(md("> 🛡️ The **program**, not the AI, decides what runs. Each guardrail is a few lines of ordinary code *between* the AI and the system.\n\n### ▶ CELL 9: Guardrail 4: human approval\nNow we let the server write (`--allow-write`), but **only a person can say yes**. Run the cell and answer the prompt. Then run it again and answer **no**."))
c7.append(code("# ▶ CELL 9 · GUARDRAIL 4: HUMAN APPROVAL: the agent pauses until a person says yes\n" + r'''client.close()
client = connect("--allow-write", "--with-scorecard")   # the server CAN create tickets now, but only after a person approves

''' + APPROVAL_SRC + r'''
r = run_agent("Create a ticket for PO 4500012345 so someone chases the credit check.")
print("\nTools that needed approval:", r["approval_tools"])
'''))
c7.append(md("> 🛑 The agent **paused** and waited. The `gate()` function is the only thing we changed; the loop is untouched. If you typed **no**, nothing was created. In SAP terms: a **release strategy** for AI.\n\n### ▶ CELL 10: When NOT to use an agent"))
c7.append(code(r'''
# ▶ CELL 10 · AGENT OR PLAIN AUTOMATION? The same job, two ways
reset_usage()
plain = client.call_tool("check_approval", {"value_inr": 85000})["data"]
print("Plain automation:", plain, f"→ model calls: {usage_total['calls']}")

reset_usage()
r = run_agent("Who must approve a purchase order of INR 85000?", verbose=False)
print("Agent           :", r["answer"], f"→ model calls: {usage_total['calls']}, steps: {r['steps']}, {usage_total['seconds']} s")
'''))
c7.append(md("> ⚖️ Same answer. The fixed rule needed **no model at all**. Use an agent when *the next step depends on what is found*. For a fixed, rule-based process, normal automation is faster, cheaper and easier to audit."))

c7.append(md("""
---
# E · Your turn (40 min)
Ask **five business questions** through the MCP-connected agent. For each one, note **which tool it chose** and **whether it needed approval**.

### ▶ CELL 11: Five business questions
"""))
c7.append(code(r'''
# ▶ CELL 11 · Your turn: five business questions through the MCP-connected agent
MY_QUESTIONS = [   # ← change me: replace any of these
    "Which orders for Plant 1000 are blocked and why?",
    "Who is the vendor contact for PO 4500012346?",
    "Who must approve PO 4500012348?",
    "Which vendor has the most delayed order value?",
    "Create a ticket for PO 4500012345 about the credit check.",
]
print(f"{'#':<3}{'Tools the agent chose':<44}{'Steps':<7}Approval needed?")
for i, q in enumerate(MY_QUESTIONS, 1):
    r = run_agent(q, verbose=False)
    print(f"{i:<3}{' → '.join(r['tools']) or '—':<44}{r['steps']:<7}{'YES: ' + ', '.join(r['approval_tools']) if r['approval_tools'] else 'no'}")
    print(f"   {q}\n   ↳ {(r['answer'] or 'no answer: step limit reached')[:150]}\n")
'''))
c7.append(md("> 💡 Try your own: *Which orders for Plant 2000 are delayed?* · *What does the approval policy say?* (use the resource) · *Delete PO 4500012345.* (what happens?)\n\n### ▶ CELL 12: Scoreboard: check it in code\nQuestion 4 must produce a real ticket id (`TCK-…`). If you type **no** at the approval prompt, nothing is created and that row shows ❌: the guardrail worked, the test just wanted a ticket."))
c7.append(code(r'''
# ▶ CELL 12 · Final check: four questions scored in code (tools used · a word in the answer · approval)
FINAL = [  # (question, tools that must be used, a word the answer must contain, should a person be asked?)
    ("Which orders for Plant 1000 are blocked and why?",           {"list_orders"},                "credit check", False),
    ("Who must approve PO 4500012348?",                            {"get_order", "check_approval"}, "director",    False),
    ("Which vendor has the highest total order value?",            {"vendor_scorecard"},           "chennai",      False),
    ("Create a ticket for PO 4500012345 about the credit check.",  {"create_ticket"},              "tck-",         True),   # a real ticket id: a declined request must NOT score
]
points = 0
for question, need, word, approval in FINAL:
    r = run_agent(question, verbose=False)
    ok = need <= set(r["tools"]) and bool(r["answer"]) and word in r["answer"].lower() and bool(r["approval_tools"]) == approval
    points += ok
    print(f"{'✅' if ok else '❌'} {question}   tools: {r['tools']}   approval: {bool(r['approval_tools'])}")
print(f"\nScore: {points} / {len(FINAL)}")
client.close()
'''))
c7.append(md("""
---
## ✅ Remember three things
1. **MCP = USB-C for AI.** A server offers **tools, resources and prompts** in one standard shape, so any agent can use any system.
2. **Guardrails keep agents safe:** step limits · read-only first · human approval before any change.
3. **Not every job needs an agent.** Fixed, rule-based processes are better left to normal automation.

> 🌉 **Bridge to Class 8:** We have seen every piece: prompts, knowledge, agents, tools and guardrails. *How do they come together into one real solution?*
""" + TROUBLE))
save(c7, C7 + "/notebooks/Class_7_Agents_In_Action.ipynb", "Class 7 · Agents in Action: Tools, MCP & Guardrails")

# =====================================================================================================
#                                             CLASS 8
# =====================================================================================================
c8 = []
c8.append(md("""
# 🧩 Class 8: Putting It All Together: an AI Agent for SAP
### From pieces to a real solution · Day 4 · Afternoon · 2 hours

**Same story.** Neo can write (Class 3–4), read our documents (Class 5), use tools (Class 6) and plug into systems safely (Class 7). Today we assemble **one assistant**: the **SAP Operations Assistant**.

**Today's question:** *How do LLMs, prompts, knowledge and agents combine into a real business solution, and where do we start?*

```
 User question
   → Prompt & rules                      (Classes 3–4)
   → Agent decides the steps             (Class 6)
   → Company knowledge via RAG           (Class 5)
     + System tools via MCP              (Class 7)
   → LLM writes the answer               (Class 2)
   → Checked, structured response back to the user
```

| Part | Topic | Cells |
|---|---|---|
| 1 | Start simple: choose the simplest approach that works | S, 1–2 |
| 2 | Assemble the parts: knowledge + tools + rules + agent | 3–6 |
| 3 | Business concerns: checks, cost, speed, privacy, oversight | 7–9 |
| 4 | Capstone: your assistant | 10–12 |

> 🔒 All data is **mock** (*Nova Industries*). Everything runs on this laptop with Ollama.
"""))
c8.append(md("## ⚙️ ▶ CELL S: Setup\nChecks Ollama (chat + embedding model) and starts the SAP Orders MCP server from Class 7. Run once."))
c8.append(code(r'''
# ▶ CELL S · SETUP: check Ollama, then start the SAP Orders MCP server (from Class 7). Run once.
import sys, os, re, json, glob
sys.path.insert(0, "../../shared")            # where bootcamp_llm.py and mcp_client.py live
from bootcamp_llm import *
from mcp_client import *

DOCS_DIR = "../data/docs"                     # the mock company documents (Nova Industries)
SERVER = [sys.executable, "../../Class_7_MCP_Guardrails/mcp_server/sap_orders_server.py"]

check_setup(need_embed=True)
print("🤖 Neo says:", ask_ai("Reply with exactly these words: Connection OK", temperature=0, max_tokens=10))
mcp = McpClient(SERVER + ["--allow-write"])   # the server CAN write; a person-approval gate protects it (CELL 9)
print(f"🔌 MCP server: {mcp.server_info['title']} · {len(mcp.list_tools())} tools")
'''))

c8.append(md("""
---
# 1️⃣ Start simple
**In real life:** you do not call a consultant to add two numbers. Pick the **simplest approach that works**.

| Need | Use |
|---|---|
| Summarise, draft, classify text | **A good prompt** |
| Answer from company documents | **RAG** |
| Multi-step tasks using systems | **An agent** |

### ▶ CELL 1: Prompt only
"""))
c8.append(code(r'''
# ▶ CELL 1 · PROMPT ONLY: summarise, classify, draft. No documents, no tools.
EMAIL = "Hello, the truck for PO 4500012346 was held up by heavy rain near Pune. We can deliver on Monday instead of Friday. Regards, Rahul"
print("SUMMARISE:", ask_ai(f"Summarise in one sentence:\n{EMAIL}", temperature=0))
print("CLASSIFY :", ask_ai(f"Classify this email as one word: delay, invoice, complaint or thanks.\n{EMAIL}", temperature=0))
print("DRAFT    :", ask_ai("Draft a two-line polite reply asking Rahul to confirm the new delivery date in writing.", temperature=0))
'''))
c8.append(md("> ✍️ Three useful jobs, **no documents and no tools**. A good prompt is the cheapest and fastest option. Start here.\n\n### ▶ CELL 2: Can the model choose the approach?"))
c8.append(code(r'''
# ▶ CELL 2 · THE SIMPLEST APPROACH THAT WORKS: let the model choose, then check it in code
ROUTER_RULES = """You choose the simplest approach that works. Reply with ONE JSON object: {"approach": "prompt" | "rag" | "agent", "why": "<one short reason>"}
prompt = summarise, draft or classify text that is already given
rag    = answer from company documents (policies, process guides, handbooks)
agent  = multi-step work that needs live system data and several tools"""

NEEDS = [  # (the need, the approach we expect)
    ("Summarise this supplier email in one line.",                                        "prompt"),
    ("What does our policy say about changing vendor bank details?",                      "rag"),
    ("What does IDoc status 51 mean?",                                                    "rag"),
    ("Why is PO 4500012348 blocked, who must approve it and who is the vendor contact?",  "agent"),
    ("Which orders for plant 1000 are blocked?",                                          "agent"),
]
score = 0
for need, expected in NEEDS:
    pick = chat_json([{"role": "system", "content": ROUTER_RULES}, {"role": "user", "content": need}])
    ok = pick.get("approach") == expected
    score += ok
    print(f"{'✅' if ok else '⚠️'} {pick.get('approach'):<7} (expected {expected:<6}) {need}")
print(f"\n{score} / {len(NEEDS)}")
'''))
c8.append(md("> 🧭 A ⚠️ is the lesson: **choosing the approach is itself a decision to test.** In a real project a person (or a simple rule) usually makes this choice once, per use case."))

c8.append(md("""
---
# 2️⃣ Assemble the parts
Knowledge from Class 5 + tools from Class 7 + rules from Classes 3–4 + the agent from Class 6.

### ▶ CELL 3: Knowledge: RAG, wrapped as a tool
"""))
c8.append(code("# ▶ CELL 3 · KNOWLEDGE (Class 5): cut the documents, store fingerprints, and wrap the search as a function\n" + CUT_SRC + r'''
files = sorted(glob.glob(f"{DOCS_DIR}/*.txt"))
chunks = [c for f in files for c in cut(f)]
store = list(zip(chunks, embed([c["text"] for c in chunks])))
print(f"{len(chunks)} chunks from {len(files)} documents stored.")

def search_policy(query, top=3):
    """FIND: the best clauses for a question, with their ids (so answers can cite them)."""
    q = embed(query)
    ranked = sorted(store, key=lambda s: cosine(q, s[1]), reverse=True)[:top]
    return [{"id": c["id"], "text": c["text"], "score": round(cosine(q, v), 2)} for c, v in ranked]

def rag_answer(question):
    """The 4 steps in one go: find the clauses, then answer ONLY from them, with a citation."""
    context = "\n".join(f"[{h['id']}] {h['text']}" for h in search_policy(question))
    rules = "Answer ONLY from the CONTEXT. If the answer is not there, reply exactly: Not in the documents. End with the source in brackets."
    return ask_ai(f"CONTEXT:\n<<<\n{context}\n>>>\n\nQuestion: {question}", system=rules, temperature=0)

for h in search_policy("Who signs off on really big orders?"):
    print(f"  {h['score']}  {h['id']}")
'''))
c8.append(md("> 📖 Same four steps as Class 5. The new part: `search_policy` is just a **function that returns clauses with ids**. Any function can become a tool.\n\n### ▶ CELL 4: Tools: the MCP server and the knowledge tool, on ONE menu"))
c8.append(code(r'''
# ▶ CELL 4 · TOOLS (Class 7): MCP tools from the server + our knowledge tool, on ONE menu
class ToolHub:
    """One menu for the agent. MCP tools come from the server; the knowledge tool is our own function. The agent cannot tell the difference."""
    def __init__(self, mcp, local): self.mcp, self.local = mcp, local
    def list_tools(self): return self.mcp.list_tools() + [spec for spec, _ in self.local.values()]
    def call_tool(self, name, args):
        if name in self.local:
            try: return {"ok": True, "data": self.local[name][1](**args)}
            except TypeError as e: return {"ok": False, "data": f"Bad arguments for {name}: {e}"}
        return self.mcp.call_tool(name, args)

KNOWLEDGE_TOOLS = {"search_policy": ({
    "name": "search_policy",
    "description": "Search the company documents (procurement policy, P2P process guide, travel policy, IDoc handbook). Returns the 3 best clauses with their ids. Use it for rules and procedures.",
    "inputSchema": {"type": "object", "properties": {"query": {"type": "string", "description": "What to look up, in plain words"}}, "required": ["query"]},
    "annotations": {"readOnlyHint": True}}, search_policy)}

client = ToolHub(mcp, KNOWLEDGE_TOOLS)
for t in client.list_tools():
    print(f" • {t['name']:<16} ← {'knowledge (RAG, Class 5)' if t['name'] in KNOWLEDGE_TOOLS else 'MCP server (Class 7)'}")
'''))
c8.append(md("> 🔌 Live SAP data comes **through MCP**. Company documents come **through RAG**. To the agent both are just tools on a menu.\n\n### ▶ CELL 5: Prompt and rules: the assistant's role, rules and format"))
c8.append(code("# ▶ CELL 5 · PROMPT & RULES (Classes 3-4): the assistant's role, rules and output format\n" + r'''ROLE = "You are the SAP Operations Assistant for Nova Industries. You handle multi-step questions about purchase orders, vendors and company policy."
RULES = [   # ← change me: add or edit a rule
    "Use ONLY facts returned by your tools. Never guess a status, a value, a contact, an approver or a policy.",
    "Use search_policy for company rules and cite the clause id in square brackets, for example [Procurement_Policy §6.2].",
    "Use the order, vendor and approval tools for live SAP data.",
    "You may only READ. If someone asks for a change, ask for a ticket and wait for a person to approve it.",
    "If a tool returns an error or the answer is not available, say what is missing. Do not invent it.",
]
FORMAT = "Write the final answer in at most four short sentences. Start with the main finding."      # ← change me

''' + MENU_SRC + "\nprint(system_prompt())\n"))
c8.append(md("> 📝 The assistant's **identity is data**: a role, a list of rules and a format. Change a rule and the behaviour changes. Yesterday's menu and today's rules are assembled into one system prompt.\n\n### ▶ CELL 6: The agent: one multi-step question, end to end"))
c8.append(code("# ▶ CELL 6 · THE AGENT (Class 6) with KNOWLEDGE + TOOLS: one multi-step question, end to end\n" + LOOP_SRC + r'''
CAPSTONE_Q = "PO 4500012348 is blocked. Why, who must approve it, what does our policy say about price variance, and who is the vendor contact?"
r = run_agent(CAPSTONE_Q)
'''))
c8.append(md("> 🧩 Four steps, **three kinds of source**: the order (MCP), the approver (MCP), the policy clause (RAG) and the vendor (MCP). Nobody wrote this sequence; the agent chose it. Expected facts: **blocked for price variance**, **Director** (₹12,00,000), **Procurement_Policy §6.2**, contact **Lakshmi Iyer**."))

c8.append(md("""
---
# 3️⃣ Business concerns
A demo is not a solution. Five questions every sponsor will ask: **accuracy · cost · speed · data privacy · human oversight.**

### ▶ CELL 7: Accuracy: a checked, structured response
"""))
c8.append(code("# ▶ CELL 7 · CHECKED + STRUCTURED: do not hand the user raw text\n" + CHECK_SRC + r'''
def structured(question, result=None):
    """Run the agent (or reuse a result) and return a CHECKED, STRUCTURED response: fields, not just text."""
    r = result or run_agent(question, verbose=False)
    problems = check_answer(question, r) if r["answer"] else ["no answer (step limit reached)"]
    return {"question": question, "answer": r["answer"], "tools_used": r["tools"], "steps": r["steps"],
            "checked": not problems, "problems": problems, "needs_human": bool(r["approval_tools"]) or bool(problems)}

reply = structured(CAPSTONE_Q, r)
print(json.dumps(reply, indent=2, ensure_ascii=False))

fake = {"answer": "The Director approved it for ₹15,00,000 [Procurement_Policy §9.9].", "evidence": r["evidence"]}
print("\nA made-up answer is caught →", check_answer(CAPSTONE_Q, fake))
'''))
c8.append(md("> ✅ **Code checks the answer**: every number and every citation must appear in the tools' results. A made-up figure or a clause nobody retrieved is flagged, and `needs_human` tells the app to ask a person.\n\n### ▶ CELL 8: Cost and speed"))
c8.append(code(r'''
# ▶ CELL 8 · COST AND SPEED: the three approaches compared
jobs = [("prompt only",   lambda: ask_ai(f"Summarise in one sentence:\n{EMAIL}", temperature=0)),
        ("RAG",           lambda: rag_answer("Who approves a PO above ₹10 lakh?")),
        ("agent + tools", lambda: run_agent(CAPSTONE_Q, verbose=False))]
print(f"{'approach':<15}{'model calls':<13}{'tokens in':<11}{'tokens out':<12}seconds")
for label, job in jobs:
    reset_usage()
    job()
    u = usage_total
    print(f"{label:<15}{u['calls']:<13}{u['input_tokens']:<11}{u['output_tokens']:<12}{u['seconds']}")
'''))
c8.append(md("> ⏱️ More steps means more model calls, more tokens and more waiting. With a paid cloud model, **tokens are money**. This is why we start simple and add an agent *only when the problem needs it*.\n\n### ▶ CELL 9: Privacy and human oversight"))
c8.append(code("# ▶ CELL 9 · PRIVACY AND OVERSIGHT: where does the data go, and who approves a change?\n" + r'''from urllib.parse import urlparse
host = urlparse(OLLAMA_URL).hostname
print(f"Model runs at {host} →", "🔒 this laptop: nothing leaves it" if host in ("localhost", "127.0.0.1") else "⚠️ another machine: check that it is approved")
print(f"RAG sends only 3 of {len(chunks)} chunks to the model, not the whole library.\n")

''' + APPROVAL_SRC + r'''
r = run_agent("Create a ticket for PO 4500012348 asking the buyer to resolve the price variance.")
print("\nTools that needed approval:", r["approval_tools"])
'''))
c8.append(md("> 🔒 **Privacy:** a local model keeps data on the laptop. Cloud tools (NotebookLM, Antigravity) need approval and **mock data only**. **Oversight:** reads run alone; any change waits for a person."))

c8.append(md("""
---
# 4️⃣ Capstone: your SAP Operations Assistant (40 min)
Pick **one SAP process**, ask it a multi-step question, test it, and fill in your pitch card. Change only the lines marked **← change me**.

### ▶ CELL 10: Pick a process and ask
"""))
c8.append(code(r'''
# ▶ CELL 10 · YOUR ASSISTANT: pick one SAP process and ask it a multi-step question
USE_CASES = {
    "invoice exception":  "PO 4500012348 has a price variance. Why is it blocked, who must approve it, and what does our policy say?",
    "PO delay analysis":  "Which orders for plant 2000 are delayed, and who is the vendor contact for the first one?",
    "IDoc error triage":  "An IDoc is stuck at status 51. What does it mean, and who do we involve if the cause is the connection?",
    "vendor query":       "Who is the vendor contact for PO 4500012346, and what is the status of that order?",
    "month-end close":    "Which orders for plant 1000 are blocked, and what does our policy say about the 3-way match before payment?",
}
MY_USE_CASE = "invoice exception"                       # ← change me (one of the five above)
MY_QUESTION = USE_CASES[MY_USE_CASE]                    # ← or write your own question here

MY_RESULT = run_agent(MY_QUESTION)
reply = structured(MY_QUESTION, MY_RESULT)
print("\n📋 Checked:", reply["checked"], "| Needs a human:", reply["needs_human"], "| Problems:", reply["problems"])
'''))
c8.append(md("> 🏁 Try the others. Notice which ones need only the **knowledge tool**, which need only **MCP tools**, and which need **both**.\n\n### ▶ CELL 11: Test your assistant: 5 questions, scored in code"))
c8.append(code(r'''
# ▶ CELL 11 · TEST PLAN: direct · reworded · not in the documents. The CODE checks tools and answer.
NOT_FOUND = ("not in the documents", "not found", "no information", "cannot", "do not know", "don't know", "not available", "no tool")
TESTS = [  # (type, question, tools that must be used, a word the answer must contain, or None for "must say it is missing")
    ("direct",   "What is the status of PO 4500012345?",                                  {"get_order"},                  "blocked"),
    ("direct",   "What does IDoc status 51 mean?",                                        {"search_policy"},              "not posted"),
    ("direct",   "Who is the vendor contact for PO 4500012346?",                          {"get_order", "get_vendor"},    "rahul"),
    ("reworded", "Which senior person has to sign off on PO 4500012348 because it is so large?", {"get_order", "check_approval"}, "director"),
    ("missing",  "What is the notice period for ending a vendor contract?",               set(),                          None),
]
points = 0
for kind, question, need, word in TESTS:
    r = run_agent(question, verbose=False)
    answer = (r["answer"] or "").lower()
    ok = need <= set(r["tools"]) and bool(answer) and ((word in answer) if word else any(p in answer for p in NOT_FOUND))
    points += ok
    print(f"{'✅' if ok else '❌'} {kind:<8} {question}")
    print(f"     tools : {r['tools']}   checked: {not check_answer(question, r) if r['answer'] else False}")
    print(f"     answer: {(r['answer'] or '—')[:140]}\n")
print(f"Score: {points} / {len(TESTS)}")
'''))
c8.append(md("> 📋 A ❌ is a good lesson. Was the **wrong tool** chosen? Was the **right clause not retrieved**? Or did the model **ignore** the result? The printed tools tell you where to look.\n\n### ▶ CELL 12: Your 5-minute pitch card"))
c8.append(code(r'''
# ▶ CELL 12 · YOUR 5-MINUTE PITCH: the card fills itself from what you built
TEAM = "Team 1"                                         # ← change me
GUARDRAILS_I_REQUIRE = [                                # ← change me: the guardrails you would insist on
    "Read-only tools by default",
    "A person approves any ticket or change",
    f"A step limit of {MAX_STEPS}",
    "Answers checked in code: numbers and citations must come from the tools",
    "Mock data only; a local model for anything sensitive",
]
print(f"""
╔══════════════════════ {TEAM} · SAP OPERATIONS ASSISTANT ══════════════════════
 1. THE PROCESS   : {MY_USE_CASE}
 2. THE PROMPT    : {ROLE[:110]}…
                    Format: {FORMAT}
 3. LIVE DEMO     : {MY_QUESTION}
                    tools used: {' → '.join(MY_RESULT['tools'])}   (test score: {points} / {len(TESTS)})""")
print(" 4. GUARDRAILS    :")
for g in GUARDRAILS_I_REQUIRE:
    print("      •", g)
print("╚" + "═" * 78)
mcp.close()
'''))
c8.append(md("""
---
## ✅ Remember three things
1. **Start simple.** Prompt first, then add knowledge (RAG), then an agent, and only when the problem needs it.
2. **One assistant = parts you already know:** prompt and rules + agent + RAG + MCP tools + a checked answer.
3. **Business concerns decide success:** accuracy checks, cost, speed, data privacy and human oversight.

> 🌱 **Keep learning with the same free tools.** See `Class_8_Capstone/ROADMAP.md`.
""" + TROUBLE))
save(c8, C8 + "/notebooks/Class_8_Putting_It_All_Together.ipynb", "Class 8 · Putting It All Together: an AI Agent for SAP")
