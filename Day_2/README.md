# 🦙 Day 2 · Prompt Engineering: Ollama bundle

**GenAI & Agentic AI for SAP Professionals** · Class 3 *Writing Neo's Handover Note* + Class 4 *Neo Goes Live* (one everyday example throughout: Neo, an AI chatbot, covers your inbox while you're on leave; the prompt is your handover note)
Runs **100% locally** with [Ollama](https://ollama.com). No cloud account, no API key, and data stays on the laptop.

---

## ⚡ Quick start (Windows)
1. Install **Ollama** (https://ollama.com/download) and **Python 3.10+** (https://python.org, tick *Add to PATH*).
2. Open **PowerShell** in this folder and run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File setup\setup_windows.ps1
   ```
3. Open this folder in **VS Code** or **Antigravity** → open `notebooks\Class_3_Neo_Handover_Note.ipynb` → choose the **`.venv`** kernel → run **▶ CELL S**.
4. Open `slides\Class_3_Neo_Handover_Note_Slides.html` in **Edge** or **Chrome** → press **F** for fullscreen and **P** for presenter view.

*Mac/Linux:* `bash setup/setup_mac_linux.sh`

### 🤖 Using Antigravity (or any AI coding agent)
Open this folder and type:
> *"Read AGENTS.md and set up this bundle with Ollama model `llama3.2:3b`."*

The agent will install and pull everything, create the venv, and run the health check.

---

## 🔁 Changing the model (placeholder)
Edit **`bootcamp_config.json`** (it's the only file you need to touch):
```json
"model": "llama3.2:3b",
"small_model": "llama3.2:1b"
```
Then `ollama pull <name>` and **Restart kernel** in the notebook.

| Laptop | Suggested `model` | Download |
|---|---|---|
| 8 GB RAM | `llama3.2:3b` (default) · small: `llama3.2:1b` | ~2 GB |
| 16 GB RAM | `llama3.1:8b` or `qwen2.5:7b` | ~5 GB |
| GPU / 32 GB | `gemma3:12b` or `qwen2.5:14b` | ~8–9 GB |

> ⚠️ **Slides quote a real test run on `gemma4:e2b`.** Your model will word things differently, and small models make different mistakes. The speaker notes explain what to say either way.

---

## 📁 What's inside
```
Day2_Prompt_Engineering_Ollama/
├── README.md                ← you are here
├── AGENTS.md                ← instructions for Antigravity / AI agents
├── bootcamp_config.json     ← MODEL PLACEHOLDER (edit me)
├── requirements.txt
├── notebooks/
│   ├── bootcamp_llm.py                     ← Ollama helper (stdlib only)
│   ├── Class_3_Neo_Handover_Note.ipynb  ← ▶ CELL S, 1–14
│   └── Class_4_Neo_Goes_Live.ipynb      ← ▶ CELL S, 1–17
├── slides/
│   ├── Class_3_Neo_Handover_Note_Slides.html     ← 54 slides · light theme
│   └── Class_4_Neo_Goes_Live_Slides.html← 50 slides · dark theme
├── archive_v1… to archive_v4…   ← earlier versions, kept for reference
├── data/
│   ├── emails.json          ← mock vendor emails and attacks (Nova Industries)
│   └── three_way_match.csv  ← 6 PO/GR/invoice cases with answer key
└── setup/
    ├── setup_windows.ps1
    ├── setup_mac_linux.sh
    └── check_setup.py
```

## 🎤 Presenting
| Key | Action |
|---|---|
| → / Space | Next point or slide |
| ← | Back |
| **F** | Fullscreen |
| **P** | Presenter window (notes, next slide, timer). Allow pop-ups. |
| **T** | Light / dark theme |
| N · B · ? | Notes on screen · black screen · help |

Each demo slide has a **▶ CELL n** tag (shown in the command field at the top right as **▶ CELL n**). Switch to the notebook and run that cell.

## 🛠️ Troubleshooting
See the last cell of each notebook, or `AGENTS.md` → *Troubleshooting*.

🔒 **Mock data only.** All companies, people, POs and bank details are fictional.
