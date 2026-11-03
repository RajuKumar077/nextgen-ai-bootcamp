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
   powershell -ExecutionPolicy Bypass -File setup\setup_windows.ps1
   ```
3. Open this folder in **VS Code** or **Antigravity** → open `Class_7_MCP_Guardrails\notebooks\Class_7_Agents_In_Action.ipynb` → choose the **`.venv`** kernel → run **▶ CELL S**.
4. Open `Class_7_MCP_Guardrails\slides\Class_7_Agents_In_Action_Slides.html` in **Edge** or **Chrome** → press **F** for fullscreen and **P** for presenter view.

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
│   ├── slides/Class_7_Instructor_Script.html           ← what to SAY, slide by slide (instructor only)
│   ├── slides/Class_7_Agents_In_Action_Slides.html     ← 59 slides · light theme
│   ├── mcp_server/sap_orders_server.py                 ← the mock SAP Orders MCP server
│   ├── data/orders.csv · vendors.csv                   ← mock SAP data
│   └── antigravity/TASK.md · expected_*.md             ← live demos + answer keys
├── Class_8_Capstone/         ← AFTERNOON · the SAP Operations Assistant
│   ├── notebooks/Class_8_Putting_It_All_Together.ipynb ← ▶ CELL S, 1–12
│   ├── slides/Class_8_Instructor_Script.html           ← what to SAY, slide by slide (instructor only)
│   ├── slides/Class_8_Putting_It_All_Together_Slides.html ← 48 slides · dark theme
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
| **Tools** (actions) | `list_orders`, `get_order`, `get_vendor`, `check_approval`, `delayed_summary`, `create_ticket` (+ `vendor_scorecard` with `--with-scorecard`) |
| **Resources** (data to read) | `orders://all`, `orders://summary`, `policy://approval-limits` |
| **Prompts** (ready-made requests) | `blocked_orders_report`, `vendor_followup` |

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
