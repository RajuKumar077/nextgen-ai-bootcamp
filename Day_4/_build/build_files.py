"""Writes the Day 4 support files: READMEs, agent instructions, Antigravity tasks + answer keys, setup scripts, roadmap, pitch card.
Every number in them is computed from the real MCP server and the built decks. Run after build_notebooks.py and the two slide builders:   python build_files.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d4_slides_core import *          # noqa: F401,F403,E402

NB = lambda p: len(re.findall(r'<section class="slide', open(p, encoding="utf-8").read()))
S7 = NB(C7 + "/slides/Class_7_Agents_In_Action_Slides.html")
S8 = NB(C8 + "/slides/Class_8_Putting_It_All_Together_Slides.html")


def write(path, text, mode=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.strip("\n") + "\n")
    if mode:
        os.chmod(path, mode)
    print("wrote", os.path.relpath(path, DAY4))


def table_md(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(r) + " |" for r in rows])


# ───────────────────────────── answer keys (computed) ─────────────────────────────
blocked_tbl = table_md(["PO number", "Vendor", "Value (INR)", "Block reason"], [[o["po_number"], o["vendor_name"], inr(o["value_inr"]), o["block_reason"]] for o in BLOCKED_1000])
write(C7 + "/antigravity/expected_blocked_plant_1000.md", f"""
# Blocked purchase orders · plant 1000

{blocked_tbl}

_Answer key for the live demo. {len(BLOCKED_1000)} blocked orders on plant 1000. Compare it with what the agent says after calling `list_orders`._
""")

delayed_tbl = table_md(["Vendor", "Delayed POs", "Total value (INR)"], [[v, str(d["delayed_pos"]), inr(d["total_value_inr"])] for v, d in sorted(DELAYED.items())])
write(C7 + "/antigravity/expected_answers.md", f"""
# Answer key · the five hands-on questions (Class 7, CELL 11)

| # | Question | Tools we expect | Approval? | The answer has |
|---|---|---|---|---|
| 1 | Which orders for Plant 1000 are blocked and why? | `list_orders` | no | {len(BLOCKED_1000)} orders (see `expected_blocked_plant_1000.md`) |
| 2 | Who is the vendor contact for PO 4500012346? | `get_order` → `get_vendor` | no | {VENDOR['V200']['contact']}, {VENDOR['V200']['email']} ({VENDOR['V200']['vendor']}) |
| 3 | Who must approve PO 4500012348? | `get_order` → `check_approval` | no | {APPR[1200000]['approver']} ({inr(1200000)}, policy {APPR[1200000]['policy']}) |
| 4 | Which vendor has the most delayed order value? | `delayed_summary` | no | {TOP_DELAY}, {inr(DELAYED[TOP_DELAY]['total_value_inr'])} |
| 5 | Create a ticket for PO 4500012345 about the credit check. | `create_ticket` | **YES** | a ticket id such as `TCK-0001` |

## Delayed orders by vendor (question 4)

{delayed_tbl}

## With the scorecard tool (CELL 7)

Question: *Which vendor has the highest total order value?* → **{TOP_VENDOR}**, {inr(SCORE[TOP_VENDOR]['total_value_inr'])}, {SCORE[TOP_VENDOR]['delayed']} delayed and {SCORE[TOP_VENDOR]['blocked']} blocked.

_A different tool order is a discussion point, not an error. Tool results are exact; the agent's wording will differ._
""")

write(C7 + "/antigravity/TASK.md", f"""
# Antigravity demo tasks (Class 7)

Two live demos, about 10 minutes each: **(1) Antigravity + MCP** and **(2) the guardrail: approval before a change**.

## Before class (once)

1. From the `Day_4` folder run: `python setup/make_mcp_config.py` (use the `.venv` Python). It writes `.vscode/mcp.json` for VS Code and
   `Class_7_MCP_Guardrails/antigravity/mcp_config.json` for Antigravity, both with the absolute path for **this** laptop, and test-starts each server.
2. **VS Code:** open the `Day_4` folder. The servers appear in the MCP / Tools list of the chat view. Start them there.
3. **Antigravity:** open the MCP settings (Agent panel → MCP servers → manage → raw config) and paste the contents of `antigravity/mcp_config.json`. Restart the agent.
4. Run both demos once. **Use the names you actually see** on screen: Antigravity and VS Code change their menus often. Keep a backup recording.

The two servers are the **same Python file** (`mcp_server/sap_orders_server.py`) started with different flags:

| Server name | Flags | What it can do |
|---|---|---|
| `nova-sap-orders` | none | **Read-only.** {len(TOOLS) - 1} read tools. `create_ticket` is refused. |
| `nova-sap-orders-write` | `--allow-write --with-scorecard` | Adds `vendor_scorecard`; `create_ticket` really writes to `mcp_server/tickets.jsonl`. |

## Demo 1 · Antigravity + MCP

Enable **only** `nova-sap-orders`. Paste this into the agent:

```
Use the nova-sap-orders MCP tools to answer: Which orders for Plant 1000 are blocked and why?
Show a table with PO number, vendor, value in INR and block reason. Use only facts from the tools.
```

| What you see | Say |
|---|---|
| The agent lists the available tools | **DISCOVERY.** It asked the server what it offers. |
| It calls `list_orders` with `plant: "1000"` and `status: "Blocked"` | **ACT.** It chose the tool and the arguments itself. |
| The result appears | **OBSERVE.** The facts come from the server, not from the model. |
| It writes the table | **FINISH.** Compare with `expected_blocked_plant_1000.md`. |

Then try the MCP **prompt**: in VS Code, type `/` and pick `blocked_orders_report` (plant: `1000`). That is the "ready-made prompt" the server offers.

## Demo 2 · Guardrail: approval before a change

Enable `nova-sap-orders-write`. In Antigravity's settings choose the mode that **asks before running commands or tools**. Paste:

```
Create a follow-up ticket for PO 4500012345 about the credit check, using the nova-sap-orders-write tools.
```

Expected: the agent **pauses** and shows the `create_ticket` call with its arguments. **Do not click yet.** Say: *"That pause is the guardrail. Nothing has changed."*
Click **approve** once, then show `mcp_server/tickets.jsonl`. Run it again and **decline**; the file does not grow.

Contrast: with only `nova-sap-orders` enabled, the same request is refused by the server (`This server is READ-ONLY`). Two layers: the **server** can refuse, and the **client** can ask.

## Hands-on questions

See `expected_answers.md`. Teams note, for each question, **which tool** the agent chose and **whether it needed approval**.

> Antigravity and VS Code send your prompts to a cloud model. Get IT/security approval first. The data here is **mock only**.
""")

# ───────────────────────────── Class 8 capstone files ─────────────────────────────
uc_rows = [[a, b, c, d] for a, b, c, d in [("Invoice exception", "PO 4500012348: price variance", "Orders + approver + policy + vendor", "MCP + RAG"), ("PO delay analysis", "Delayed orders on plant 2000", "Orders + vendor contact", "MCP"),
                                           ("IDoc error triage", "IDoc stuck at status 51", "IDoc handbook (§1.1, §2.3)", "RAG"), ("Vendor query", "Contact for PO 4500012346", "Order + vendor", "MCP"), ("Month-end close", "Blocked orders + 3-way match", "Orders + policy (§4.1)", "MCP + RAG")]]
write(C8 + "/capstone/CAPSTONE_GUIDE.md", f"""
# Capstone guide · the SAP Operations Assistant (Class 8)

**Goal:** one assistant that answers a multi-step SAP question using **a prompt, knowledge (RAG), an agent and MCP tools**, with a checked answer and guardrails.
Teams of 3 or 4 · 40 minutes to build and test · then a 5-minute pitch each.

## The four parts

| Part | Tool | What teams do | Notebook alternative (no cloud) |
|---|---|---|---|
| Brain | Ollama | Use the local model | CELL S |
| Knowledge | NotebookLM | Load the team's policy and process documents | CELL 3 (`data/docs/`) |
| Prompts | Ollama / VS Code | Write the assistant's role, rules and output format | CELL 5 (`ROLE`, `RULES`, `FORMAT`) |
| Agent + tools | Antigravity + MCP | Answer multi-step questions on the mock SAP data | CELLs 4 and 6 |

NotebookLM and Antigravity are **cloud** tools: get approval, use **mock documents only**. The notebook does the same thing locally.

## Five use cases to choose from

{table_md(["Use case", "A question to start with", "What it needs", "Sources"], uc_rows)}

## Steps

1. Pick **one** process (CELL 10: `MY_USE_CASE`) or write your own question.
2. Run the agent. Look at the tools it chose and the facts it observed.
3. Change one rule or the format (CELL 5, `# ← change me`) and run again. What changed?
4. Test it (CELL 11): direct, reworded and missing questions, scored by code.
5. Fill in the pitch card (CELL 12). It prints from what you built.

## Capstone check (Antigravity + MCP, optional)

Enable `nova-sap-orders` and ask:

```
PO 4500012348 is blocked. Why, who must approve it, and who is the vendor contact?
Use only facts from the tools.
```

Expected facts: blocked for **{ORD48['block_reason'].lower()}**, value **{inr(ORD48['value_inr'])}**, approver **{APPR[1200000]['approver']}** (policy {APPR[1200000]['policy']}), contact **{VENDOR['V300']['contact']}** ({VENDOR['V300']['email']}).
The policy clause on price variance is **Procurement_Policy §6.2**: *{C62['text'].split('] ', 1)[1]}* (this part needs the documents, so it comes from NotebookLM or CELL 3).

## Team presentation (5 minutes)

1. **One SAP process.** What is the question and who asks it?
2. **The prompt used.** Role, rules, format.
3. **A live demo.** Which tools did it call? Was the answer checked?
4. **The guardrails you would require** before this touches real data.

## Judging: one question

*Would I trust this answer?* Listen for: sources named, a step limit, read-only by default, a person approving changes, and mock data in cloud tools.
""")

write(C8 + "/capstone/pitch_card.md", """
# Pitch card · SAP Operations Assistant

**Team:** ______________________

| | |
|---|---|
| **1. The SAP process** | |
| **2. The prompt** (role · rules · format) | |
| **3. The live demo question** | |
| **   Tools it called** | |
| **   Answer checked? (numbers and citations from the tools)** | |
| **4. Guardrails we would require** | |
| **   Business concerns** (accuracy · cost · speed · privacy · oversight) | |

_CELL 12 prints this card from your notebook. Copy it here or present from the notebook._
""")

write(C8 + "/ROADMAP.md", """
# Roadmap · keep learning with the same free tools

You finished the course with five free tools: **Ollama**, **VS Code**, **NotebookLM**, **Antigravity** and **MCP**. Here is how to keep going. Always in this order.

## Step 1 · Prompts (week 1)
- Pick one repeated text job: summarise a supplier email, draft a reminder, classify tickets.
- Save your best prompt as **Role · Task · Context · Format · Rules**. Test it on five real examples (with data you are allowed to use).
- Tools: Ollama + VS Code. *Exit test: the same prompt gives a usable answer 5 times out of 5.*

## Step 2 · Knowledge (weeks 2-3)
- Pick **one** small, approved, current document set (a process guide, an error handbook). Remove old versions.
- Build a RAG on it (Class 5, or NotebookLM). Write a **test plan**: direct, reworded and missing questions.
- *Exit test: every answer cites its source, and "Not in the documents" is returned when it should be.*

## Step 3 · Tools (weeks 4-6)
- Pick **one** read-only data source (an export, a report). Write a small MCP server over it (copy `sap_orders_server.py`).
- Connect it to Antigravity or VS Code. Start with **read-only tools only**.
- *Exit test: the agent picks the right tool for ten different questions.*

## Step 4 · Guardrails and pilot (weeks 7-8)
- Add the four guardrails: **read-only first**, **allow-list**, **step limit**, **human approval**. Check answers in code (Class 8, CELL 7).
- Get IT and security approval. Agree an **owner** for the documents and the tools.
- Run a pilot on **one** process with a small group. Count the time saved and the mistakes caught.

## Rules of thumb
1. **Start simple.** Prompt, then knowledge, then an agent. Only when the problem needs it.
2. **A fixed rule is not an agent.** Use normal automation for rule-based work.
3. **Business rules live in code**, not in the prompt.
4. **A person approves any change.**
5. **Mock or approved data only** in cloud tools.

## Where to look
- Ollama models: https://ollama.com/library
- MCP: https://modelcontextprotocol.io
- This bundle: `Class_7_MCP_Guardrails/mcp_server/sap_orders_server.py` is a complete, small, readable example server.
""")

# ───────────────────────────── root documents ─────────────────────────────
AGENTS = f"""
# AGENTS.md: Instructions for AI coding agents (Antigravity, Claude Code, Copilot, Cursor…)

You are helping a trainer set up and run **Day 4** of the bootcamp *"GenAI & Agentic AI for SAP Professionals"*:
**Class 7 (Tools, MCP & guardrails)** and **Class 8 (Putting it all together: the SAP Operations Assistant)**. The audience is SAP consultants, not developers.
Keep everything simple and **never print secrets**. All data is mock (fictional company "Nova Industries").

## What this bundle is
| Path | Purpose |
|---|---|
| `bootcamp_config.json` | **The only file to edit to switch models.** `model` (chat), `small_model`, and `embed_model` (text → meaning fingerprints for RAG). All three are placeholders. |
| `shared/bootcamp_llm.py` | Helper used by every notebook. Talks to Ollama over HTTP using the **Python standard library only**. |
| `shared/mcp_client.py` | A tiny MCP client (standard library only): starts an MCP server and calls `list_tools`, `call_tool`, resources and prompts. |
| `Class_7_MCP_Guardrails/mcp_server/sap_orders_server.py` | The mock **SAP Orders MCP server** (standard library only). {len(TOOLS)} tools, 3 resources, 2 prompts. **Read-only by default.** `--allow-write` enables `create_ticket`; `--with-scorecard` adds `vendor_scorecard`. |
| `Class_7_MCP_Guardrails/notebooks/Class_7_Agents_In_Action.ipynb` | Class 7 (morning). MCP, the 3 things a server offers, the agent over MCP, guardrails, human approval. Cells `▶ CELL S, 1–12`. |
| `Class_7_MCP_Guardrails/data/orders.csv` · `vendors.csv` | Mock SAP data behind the MCP server. |
| `Class_7_MCP_Guardrails/antigravity/` | `TASK.md` (both live demos), `expected_answers.md`, `expected_blocked_plant_1000.md` (answer keys). |
| `Class_8_Capstone/notebooks/Class_8_Putting_It_All_Together.ipynb` | Class 8 (afternoon). Start simple, assemble prompt + RAG + MCP + agent, checks, cost, privacy, capstone. Cells `▶ CELL S, 1–12`. |
| `Class_8_Capstone/data/docs/*.txt` | Mock documents: procurement policy, SAP process guide, travel policy, IDoc handbook. |
| `Class_8_Capstone/capstone/` · `ROADMAP.md` | Capstone guide, pitch card, and the "keep learning" roadmap. |
| `Class_*/slides/*.html` | Self-contained slide decks (open in Edge or Chrome). Each demo slide shows the cell number to run. |
| `setup/setup_windows.ps1` · `setup_mac_linux.sh` · `check_setup.py` · `make_mcp_config.py` | One-time setup, health check, and the config that lets VS Code / Antigravity find the MCP server. |
| `_build/` | Generators and tests for the notebooks and slides. Not needed to run the course. |

## Setup task (do this when asked to "set up" or "get this running")
1. Check that Ollama is installed: `ollama --version`. If not: Windows `winget install Ollama.Ollama`; Mac/Linux https://ollama.com/download.
2. Make sure the Ollama server is running (`ollama list` should work). If not: start the Ollama app, or run `ollama serve`.
3. Read `bootcamp_config.json`. If the user named a model, put it in `model`. Use a smaller one in `small_model`. Keep `embed_model` as `nomic-embed-text` unless the user cannot download it; in that case set it to the same value as `model`.
4. Pull the models: `ollama pull <model>`, `ollama pull <small_model>` and `ollama pull <embed_model>`.
5. Create a virtual environment in the bundle root and install `requirements.txt`:
   - Windows: `py -3 -m venv .venv` then `.\\.venv\\Scripts\\python -m pip install -r requirements.txt`
   - Mac/Linux: `python3 -m venv .venv` then `./.venv/bin/pip install -r requirements.txt`
6. Run `python setup/check_setup.py` using the venv's Python. Success = ✅ lines, "Connection OK", an embeddings line, and an **MCP line** listing the tools.
7. Run `python setup/make_mcp_config.py` using the venv's Python. It writes `.vscode/mcp.json` and `Class_7_MCP_Guardrails/antigravity/mcp_config.json` with absolute paths for this laptop and test-starts each server.
8. Tell the user to open a notebook, select the **`.venv`** kernel, and run **CELL S** first.

## Rules for editing
- **Don't hard-code model names in notebooks.** Use `MODEL`, `SMALL_MODEL`, `EMBED_MODEL` from `bootcamp_llm`.
- Keep the `# ▶ CELL n ·` first-line comments. The slides reference these numbers.
- Participants should only edit lines marked `# ← change me`.
- **Business rules live in Python tools** (the MCP server's `check_approval`), not in prompts.
- **Guardrails live in code between the AI and the system** (`gate()`, `ALLOWED`, `MAX_STEPS`), never only in the prompt.
- The server is **read-only by default**. The only tool that changes data is `create_ticket`: it is refused unless the server is started with `--allow-write`, and the notebooks add a **human-approval gate** in front of it.
- **Never add a tool that posts, pays, deletes or emails.** Any new tool that changes data must carry `readOnlyHint: false` so the gate asks a person.
- Servers use **stdout only for protocol messages**. Log to stderr.
- After any change, run the notebook top to bottom and confirm there are **no errors**. Without Ollama you can run `python _build/test_notebooks.py <notebook.ipynb>`, which uses a mock model to prove the plumbing.
- Mock data only. Never add real vendor, customer or bank data.

## Useful helper functions
From `bootcamp_llm`: `ask_ai(q, system=None, temperature=None, max_tokens=None)` · `chat(messages, …)` · `chat_json(messages)` (a JSON dict back; used by the agent) · `embed(text_or_list)` · `cosine(a, b)` · `show(markdown)` · `check_setup(need_embed=True)` · `last_usage` · `usage_total` / `reset_usage()` (calls, tokens, seconds).
From `mcp_client`: `McpClient([python, server.py, flags…])` with `.list_tools()` · `.call_tool(name, args)` → `{{"ok", "data"}}` · `.list_resources()` · `.read_resource(uri)` · `.list_prompts()` · `.get_prompt(name, args)` · `.wire` (the raw messages) · `.close()`.

## Troubleshooting
| Symptom | Fix |
|---|---|
| `Cannot reach Ollama at http://localhost:11434` | Start the Ollama app / `ollama serve`. If Ollama runs on another machine, set `ollama_url` in the config. |
| `Model '…' is not downloaded` | `ollama pull <name>` |
| Embedding step fails or every score looks the same | `ollama pull nomic-embed-text`, or set `embed_model` to your chat model. |
| `ModuleNotFoundError: bootcamp_llm` or `mcp_client` | The notebook must run from its own `notebooks/` folder. Open the **Day_4** folder as the workspace. |
| `The MCP server stopped before answering` | Run the server by hand to see its error: `python Class_7_MCP_Guardrails/mcp_server/sap_orders_server.py`, then press Ctrl+C. |
| `This server is READ-ONLY` | Expected. CELL 9 restarts the server with `--allow-write`. |
| `Blocked by a guardrail` | Expected. The gate refused a tool that changes data. CELL 9 swaps in human approval. |
| `The model did not return valid JSON` | A small model broke the format. Run the cell again. The agent retries on its own. |
| The agent picks the wrong tool | Normal with small models. Try a larger `model` (7B or 8B follows tool menus better) or improve the tool descriptions in the server. |
| VS Code / Antigravity do not list the servers | Run `python setup/make_mcp_config.py` again (the paths are for this laptop), restart the editor, and use the names you see on screen. |
| Very slow answers | Choose a smaller model in the config, then **Restart kernel**. |
"""
write(DAY4 + "/AGENTS.md", AGENTS)
write(DAY4 + "/GEMINI.md", AGENTS)
write(DAY4 + "/.agents/rules.md", AGENTS)

write(DAY4 + "/README.md", f"""
# 🔌 Day 4 · Tools, MCP & the full assistant: Ollama bundle

**GenAI & Agentic AI for SAP Professionals** · Class 7 *Agents in Action: Tools, MCP & Guardrails* + Class 8 *Putting It All Together: an AI Agent for SAP*

Same story as Day 3: **Neo**, an AI chatbot, covers your inbox while you're on leave.
This morning Neo meets the **standard plug (MCP)** and the **guardrails** that keep agents safe. This afternoon the whole course comes together in **one SAP Operations Assistant**.

Runs **100% locally** with [Ollama](https://ollama.com). No cloud account, no API key, and data stays on the laptop. (Antigravity, VS Code agents and NotebookLM are optional cloud extras: mock data only.)

---

## ⚡ Quick start (Windows)
1. Install **Ollama** (https://ollama.com/download) and **Python 3.10+** (https://python.org, tick *Add to PATH*).
2. Open **PowerShell** in this folder and run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File setup\\setup_windows.ps1
   ```
3. Open this folder in **VS Code** or **Antigravity** → open `Class_7_MCP_Guardrails\\notebooks\\Class_7_Agents_In_Action.ipynb` → choose the **`.venv`** kernel → run **▶ CELL S**.
4. Open `Class_7_MCP_Guardrails\\slides\\Class_7_Agents_In_Action_Slides.html` in **Edge** or **Chrome** → press **F** for fullscreen and **P** for presenter view.

*Mac/Linux:* `bash setup/setup_mac_linux.sh`

### 🤖 Using Antigravity (or any AI coding agent)
Open the **Day_4** folder and type:
> *"Read AGENTS.md and set up this bundle with Ollama model `llama3.2:3b`."*

The agent will install and pull everything, create the venv, run the health check, and write the MCP config for your editor.

---

## 🔁 Changing the models (placeholders)
Edit **`bootcamp_config.json`** (it's the only file you need to touch):
```json
"model": "llama3.2:3b",
"small_model": "llama3.2:1b",
"embed_model": "nomic-embed-text"
```
Then `ollama pull <name>` and **Restart kernel** in the notebook.

| Laptop | Suggested `model` | Download |
|---|---|---|
| 8 GB RAM | `llama3.2:3b` | ~2 GB |
| 16 GB RAM | `llama3.1:8b` or `qwen2.5:7b` (**better at following a tool menu**) | ~5 GB |
| GPU / 32 GB | `gemma3:12b` or `qwen2.5:14b` | ~8–9 GB |

> ⚠️ **Class 7 and 8 note:** small models sometimes pick the wrong tool or break the JSON format. The notebook retries and prints a ⚠️. That is part of the lesson (*agents are tested*), but a 7B/8B model gives a smoother demo. The Class 8 capstone question uses four tools in a row, so it benefits most from a larger model.

---

## 📁 What's inside
```
Day_4/
├── README.md                 ← you are here
├── AGENTS.md                 ← instructions for Antigravity / AI agents (+ GEMINI.md, .agents/rules.md)
├── bootcamp_config.json      ← MODEL PLACEHOLDERS (edit me)
├── requirements.txt
├── shared/
│   ├── bootcamp_llm.py       ← Ollama helper (stdlib only): chat, chat_json, embed, cosine, usage_total …
│   └── mcp_client.py         ← MCP client (stdlib only): list_tools, call_tool, resources, prompts
├── setup/                    ← setup_windows.ps1 · setup_mac_linux.sh · check_setup.py · make_mcp_config.py
├── Class_7_MCP_Guardrails/   ← MORNING · Neo plugs in
│   ├── notebooks/Class_7_Agents_In_Action.ipynb        ← ▶ CELL S, 1–12
│   ├── slides/Class_7_Agents_In_Action_Slides.html     ← {S7} slides · light theme
│   ├── mcp_server/sap_orders_server.py                 ← the mock SAP Orders MCP server
│   ├── data/orders.csv · vendors.csv                   ← mock SAP data
│   └── antigravity/TASK.md · expected_*.md             ← live demos + answer keys
├── Class_8_Capstone/         ← AFTERNOON · the SAP Operations Assistant
│   ├── notebooks/Class_8_Putting_It_All_Together.ipynb ← ▶ CELL S, 1–12
│   ├── slides/Class_8_Putting_It_All_Together_Slides.html ← {S8} slides · dark theme
│   ├── data/docs/ (4 mock documents)
│   ├── capstone/CAPSTONE_GUIDE.md · pitch_card.md
│   └── ROADMAP.md
└── _build/                   ← generators and tests (not needed to run the course)
```

## 🎓 How each class runs
Each part of a class starts with a **key-terms slide**: say the names and plain meanings first, then run the demos. Each demo slide carries a **term tag** (top-left) and a **▶ CELL n** tag (top-right) that matches a `# ▶ CELL n ·` header in the notebook.

| Class | Parts | Cells |
|---|---|---|
| **7 · MCP & guardrails** | A The plug → B The 3 things a server offers → C The agent over MCP → D Guardrails → E Your turn | S, 1–12 |
| **8 · The full assistant** | 1 Start simple → 2 Assemble the parts → 3 Business concerns → 4 Capstone | S, 1–12 |

## 🔌 The MCP server in one minute
`sap_orders_server.py` sits in front of the two CSV files (our mock SAP) and offers them in the standard way:

| | Offered |
|---|---|
| **Tools** (actions) | {", ".join("`" + n + "`" for n in T_NAMES)} (+ `vendor_scorecard` with `--with-scorecard`) |
| **Resources** (data to read) | {", ".join("`" + r["uri"] + "`" for r in RESOURCES)} |
| **Prompts** (ready-made requests) | {", ".join("`" + p["name"] + "`" for p in PROMPTS)} |

**Read-only by default.** Only `create_ticket` changes anything; it is refused unless the server is started with `--allow-write`, and the notebooks put a **person-approval gate** in front of it.
Run it by hand: `python Class_7_MCP_Guardrails/mcp_server/sap_orders_server.py` (it waits for JSON on stdin; press Ctrl+C to stop).

## 🎤 Presenting
| Key | Action |
|---|---|
| → / Space | Next point or slide |
| ← | Back |
| **F** | Fullscreen |
| **P** | Presenter window (notes, next slide, timer). Allow pop-ups. |
| **T** | Light / dark theme |
| **K** | Check that every slide fits the screen (lists any that overflow) |
| N · B · ? | Notes on screen · black screen · help |

## 🧾 About the numbers on the slides
These slides **do not quote a recorded model run**. Instead:
- **Exact** (labelled *"exact"*): values produced by running the notebook's own code on the data files and the real MCP server: tool lists, tool results, guardrail errors, the approval outcome, the answer-check output. They match your screen.
- **Target** (labelled *"your model will word it differently"*): what we expect the agent to find. Your model's wording and, sometimes, its tool order will differ.

## 🛠️ Troubleshooting
See the last cell of each notebook, or `AGENTS.md` → *Troubleshooting*.

## ☁️ Optional cloud tools (check before class)
- **Antigravity**, **VS Code agent mode** (Class 7 live demos) and **NotebookLM** (Class 8 capstone) send data to a cloud model. Get IT/security approval and use **mock data only**. Everything else here runs locally, and every cloud step has a notebook alternative.

🔒 **Mock data only.** All companies, people, POs and bank details are fictional.
""")

write(DAY4 + "/.gitignore", ".venv/\n__pycache__/\n.ipynb_checkpoints/\n.vscode/mcp.json\nClass_7_MCP_Guardrails/antigravity/mcp_config.json\nClass_7_MCP_Guardrails/mcp_server/tickets.jsonl\n")

# ───────────────────────────── setup scripts ─────────────────────────────
write(DAY4 + "/setup/check_setup.py", '''
"""Quick health check: is Ollama running, are the models downloaded, do chat, embeddings and the MCP server work?
Run:  python setup/check_setup.py
"""
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "shared"))
from bootcamp_llm import ask_ai, check_setup, cosine, embed, last_usage  # noqa: E402
from mcp_client import McpClient, McpError                               # noqa: E402

SERVER = os.path.join(ROOT, "Class_7_MCP_Guardrails", "mcp_server", "sap_orders_server.py")


def check_mcp():
    """Start the mock SAP Orders MCP server, list its tools and call one."""
    try:
        with McpClient([sys.executable, SERVER]) as c:
            tools = [t["name"] for t in c.list_tools()]
            blocked = c.call_tool("list_orders", {"plant": "1000", "status": "Blocked"})["data"]["count"]
            refused = not c.call_tool("create_ticket", {"po_number": "4500012345", "note": "health check"})["ok"]
        print(f"🔌 MCP server works: {len(tools)} tools ({', '.join(tools[:3])}, …) · plant 1000 has {blocked} blocked orders · read-only: {'yes' if refused else 'NO!'}")
        return refused
    except McpError as e:
        print("❌ MCP server:", e)
        return False


if __name__ == "__main__":
    ok = check_setup(need_embed=True)
    if ok:
        reply = ask_ai("Reply with exactly these words: Connection OK", temperature=0, max_tokens=10)
        print(f"🤖 Model says: {reply}   ({last_usage.get('seconds')} s)")
        a, b, c = embed(["Director approval above 10 lakh", "Who signs off on really big orders?", "Payment runs happen on Tuesday"])
        print(f"🧭 Embeddings work: {len(a)} numbers per text · related pair {cosine(a, b):.2f} · unrelated pair {cosine(a, c):.2f}")
    mcp_ok = check_mcp()                      # the MCP server does not need Ollama, so it is checked either way
    if ok and mcp_ok:
        print("\\n🎉 All good. You are ready for Day 4.")
    else:
        print("\\n⚠️  Fix the items marked ❌ above, then run this check again.")
        sys.exit(1)
''')

write(DAY4 + "/setup/make_mcp_config.py", '''
"""Writes the MCP config that lets VS Code and Antigravity find the mock SAP Orders server on THIS laptop (absolute paths), then test-starts each server.

    python setup/make_mcp_config.py            (use the .venv Python)

Writes:
    .vscode/mcp.json                                          VS Code (open the Day_4 folder; the servers show up in the chat tools list)
    Class_7_MCP_Guardrails/antigravity/mcp_config.json        Antigravity (paste into its MCP settings → raw config)

Two servers, the SAME Python file with different flags:
    nova-sap-orders          read-only
    nova-sap-orders-write    --allow-write --with-scorecard  (create_ticket really writes; the CLIENT should ask a person first)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "shared"))
from mcp_client import McpClient, McpError  # noqa: E402

SERVER = os.path.join(ROOT, "Class_7_MCP_Guardrails", "mcp_server", "sap_orders_server.py")
VENV_PY = [os.path.join(ROOT, ".venv", "bin", "python"), os.path.join(ROOT, ".venv", "Scripts", "python.exe")]
PY = next((p for p in VENV_PY if os.path.exists(p)), sys.executable)

SERVERS = {
    "nova-sap-orders": [SERVER],
    "nova-sap-orders-write": [SERVER, "--allow-write", "--with-scorecard"],
}


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\\n")
    print("✅ wrote", os.path.relpath(path, ROOT))


vscode = {"servers": {name: {"type": "stdio", "command": PY, "args": args} for name, args in SERVERS.items()}}
antigravity = {"mcpServers": {name: {"command": PY, "args": args} for name, args in SERVERS.items()}}
write(os.path.join(ROOT, ".vscode", "mcp.json"), vscode)
write(os.path.join(ROOT, "Class_7_MCP_Guardrails", "antigravity", "mcp_config.json"), antigravity)

print(f"\\nPython used in the config: {PY}")
if PY == sys.executable and not any(os.path.exists(p) for p in VENV_PY):
    print("ℹ️  No .venv found, so the config uses the Python you ran this with. Create the .venv first if you want it to use that.")
bad = 0
for name, args in SERVERS.items():
    try:
        with McpClient([PY] + args, timeout=15) as c:
            print(f"✅ {name}: starts, {len(c.list_tools())} tools")
    except McpError as e:
        bad += 1
        print(f"❌ {name}: {e}")
print("""
Next steps
  VS Code     : open the Day_4 folder → open the chat's tools list → start the servers (names as above). Restart VS Code if they do not appear.
  Antigravity : MCP settings → manage servers → raw config → paste Class_7_MCP_Guardrails/antigravity/mcp_config.json → restart the agent.
  Menus change often between versions: use the names you actually see on screen. Mock data only.""")
sys.exit(1 if bad else 0)
''')

write(DAY4 + "/setup/setup_mac_linux.sh", '''
#!/usr/bin/env bash
# Day 4 · MCP + the full assistant · one-time setup for macOS / Linux
# Run from the Day_4 folder:   bash setup/setup_mac_linux.sh
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"

echo "=== 1/6 Checking Ollama ==="
command -v ollama >/dev/null || { echo "Install Ollama first: https://ollama.com/download"; exit 1; }
ollama --version

echo "=== 2/6 Reading model names ==="
MODELS=$(python3 -c "import json;c=json.load(open('bootcamp_config.json'));print(' '.join(dict.fromkeys([c['model'],c['small_model'],c['embed_model']])))")
echo "Models: $MODELS"

echo "=== 3/6 Pulling models ==="
for m in $MODELS; do ollama pull "$m"; done

echo "=== 4/6 Python venv ==="
python3 -m venv .venv && ./.venv/bin/pip install -q --upgrade pip && ./.venv/bin/pip install -q -r requirements.txt

echo "=== 5/6 Connection test (Ollama + MCP server) ==="
./.venv/bin/python setup/check_setup.py

echo "=== 6/6 MCP config for VS Code and Antigravity ==="
./.venv/bin/python setup/make_mcp_config.py
echo "Done. Open Class_7_MCP_Guardrails/notebooks/Class_7_*.ipynb and choose the '.venv' kernel."
''', 0o755)

write(DAY4 + "/setup/setup_windows.ps1", r'''
# ─────────────────────────────────────────────────────────────────────────────
#  Day 4 · MCP + the full assistant · one-time setup for Windows (PowerShell)
#  Run from the Day_4 folder:   powershell -ExecutionPolicy Bypass -File setup\setup_windows.ps1
# ─────────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "`n=== 1/6  Checking Ollama ===" -ForegroundColor Cyan
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "Ollama is not installed. Trying winget..." -ForegroundColor Yellow
    winget install --id Ollama.Ollama -e --accept-source-agreements --accept-package-agreements
    Write-Host "Close and reopen PowerShell, then run this script again." -ForegroundColor Yellow
    exit 1
}
ollama --version

Write-Host "`n=== 2/6  Reading model names from bootcamp_config.json ===" -ForegroundColor Cyan
$cfg = Get-Content (Join-Path $Root "bootcamp_config.json") -Raw | ConvertFrom-Json
Write-Host "Main model : $($cfg.model)"
Write-Host "Small model: $($cfg.small_model)"
Write-Host "Embed model: $($cfg.embed_model)"

Write-Host "`n=== 3/6  Downloading models (first time only, may take a few minutes) ===" -ForegroundColor Cyan
$models = @($cfg.model, $cfg.small_model, $cfg.embed_model) | Select-Object -Unique
foreach ($m in $models) { ollama pull $m }

Write-Host "`n=== 4/6  Creating Python virtual environment (.venv) ===" -ForegroundColor Cyan
$py = (Get-Command py -ErrorAction SilentlyContinue)
if ($py) { py -3 -m venv .venv } else { python -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install --upgrade pip -q
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt -q

Write-Host "`n=== 5/6  Connection test (Ollama + MCP server) ===" -ForegroundColor Cyan
& .\.venv\Scripts\python.exe setup\check_setup.py

Write-Host "`n=== 6/6  MCP config for VS Code and Antigravity ===" -ForegroundColor Cyan
& .\.venv\Scripts\python.exe setup\make_mcp_config.py

Write-Host "`nDone. Open the Day_4 folder in VS Code or Antigravity, open Class_7_MCP_Guardrails\notebooks\Class_7_*.ipynb," -ForegroundColor Green
Write-Host "and choose the kernel '.venv' (top right). Then press Shift+Enter on each cell." -ForegroundColor Green
''')

write(DAY4 + "/requirements.txt", """
ipykernel>=6.0
jupyter>=1.0
# bootcamp_llm.py, mcp_client.py and the MCP server use only the Python standard library, so nothing else is required.
""")
print("\nS7", S7, "S8", S8)
close_servers()
