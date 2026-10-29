# 🦙 Day 3 · From Answers to Agents: Ollama bundle

**GenAI & Agentic AI for SAP Professionals** · Class 5 *Neo Reads the Policy Binder* (RAG) + Class 6 *Neo Opens SAP* (AI agents)

Same story as Day 2: **Neo**, an AI chatbot, covers your inbox while you're on leave.
This morning Neo learns to **look up the right page** of your documents. This afternoon Neo gets **tools** and learns to **think, act and check its own work**.

Runs **100% locally** with [Ollama](https://ollama.com). No cloud account, no API key, and data stays on the laptop.

---

## ⚡ Quick start (Windows)
1. Install **Ollama** (https://ollama.com/download) and **Python 3.10+** (https://python.org, tick *Add to PATH*).
2. Open **PowerShell** in this folder and run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File setup\setup_windows.ps1
   ```
3. Open this folder in **VS Code** or **Antigravity** → open `Class_5_RAG\notebooks\Class_5_Neo_Policy_Binder.ipynb` → choose the **`.venv`** kernel → run **▶ CELL S**.
4. Open `Class_5_RAG\slides\Class_5_Neo_Policy_Binder_Slides.html` in **Edge** or **Chrome** → press **F** for fullscreen and **P** for presenter view.

*Mac/Linux:* `bash setup/setup_mac_linux.sh`

### 🤖 Using Antigravity (or any AI coding agent)
Open the **Day_3** folder and type:
> *"Read AGENTS.md and set up this bundle with Ollama model `llama3.2:3b`."*

The agent will install and pull everything, create the venv, and run the health check.

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
| 8 GB RAM | `llama3.2:3b` (default) | ~2 GB |
| 16 GB RAM | `llama3.1:8b` or `qwen2.5:7b` (**better at following a tool menu**) | ~5 GB |
| GPU / 32 GB | `gemma3:12b` or `qwen2.5:14b` | ~8–9 GB |

`embed_model` turns text into "meaning fingerprints" for RAG. If you can't download `nomic-embed-text`, set `embed_model` to the same value as `model`; it still works, only more slowly.

> ⚠️ **Class 6 note:** small models sometimes pick the wrong tool or break the JSON format. The notebook retries and prints a ⚠️. That is part of the lesson (*agents are tested*), but a 7B/8B model gives a smoother demo.

---

## 📁 What's inside
```
Day_3/
├── README.md                 ← you are here
├── AGENTS.md                 ← instructions for Antigravity / AI agents (+ GEMINI.md, .agents/rules.md)
├── bootcamp_config.json      ← MODEL PLACEHOLDERS (edit me)
├── requirements.txt
├── shared/bootcamp_llm.py    ← Ollama helper (stdlib only): chat, chat_json, embed, cosine …
├── setup/                    ← setup_windows.ps1 · setup_mac_linux.sh · check_setup.py
├── Class_5_RAG/              ← MORNING · Neo Reads the Policy Binder
│   ├── notebooks/Class_5_Neo_Policy_Binder.ipynb   ← ▶ CELL S, 1–15
│   ├── slides/Class_5_Neo_Policy_Binder_Slides.html ← 69 slides · light theme
│   └── data/docs/ (4 mock documents) · data/old/ (an outdated policy, for CELL 12)
├── Class_6_Agents/           ← AFTERNOON · Neo Opens SAP
│   ├── notebooks/Class_6_Neo_Opens_SAP.ipynb        ← ▶ CELL S, 1–11
│   ├── slides/Class_6_Neo_Opens_SAP_Slides.html     ← 59 slides · dark theme
│   ├── data/orders.csv · vendors.csv                ← mock SAP data
│   └── antigravity/TASK.md · expected_delayed_report.md  ← live demo + answer key
└── _build/                   ← generators (not needed to run the course)
```

## 🎓 How each class runs
Each part of a class starts with a **key-terms slide**: say the names and plain meanings first, then run the demos. Each demo slide carries a **term tag** (top-left) and a **▶ CELL n** tag (top-right) that matches a `# ▶ CELL n ·` header in the notebook.

| Class | Parts | Cells |
|---|---|---|
| **5 · RAG** | 1 Neo doesn't know the binder → 2 The open-book exam (cut, store, find, answer) → 3 Trust but verify (refuse, test, outdated, chunk size) → 4 Your turn | S, 1–15 |
| **6 · Agents** | A Chatbot vs agent → B The 4 parts → C How tools work → D The loop → E Your turn | S, 1–11 |

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
- **Exact** (labelled *"exact"*): values computed from the data files by the same code as the notebook: chunk counts, tool results, the delayed-order report, the safety-check errors. They match your screen.
- **Target** (labelled *"your model will word it differently"*): what the document says the answer should be. Your model's wording will differ.

## 🛠️ Troubleshooting
See the last cell of each notebook, or `AGENTS.md` → *Troubleshooting*.

## ☁️ Optional cloud tools (check before class)
- **NotebookLM** (Class 5 bonus) and **Antigravity** (Class 6 demo) send data to a cloud model. Get IT/security approval and use **mock documents only**. Everything else here runs locally.

🔒 **Mock data only.** All companies, people, POs and bank details are fictional.
