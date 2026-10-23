# AGENTS.md: Instructions for AI coding agents (Antigravity, Claude Code, Copilot, Cursor…)

You are helping a trainer set up and run **Day 2 (Prompt Engineering)** of the bootcamp *"GenAI & Agentic AI for SAP Professionals"*.
The audience is SAP consultants, not developers. Keep everything simple and **never print secrets**.

## What this bundle is
| Path | Purpose |
|---|---|
| `bootcamp_config.json` | **The only file to edit to switch models.** `model` (main) and `small_model` are placeholders. |
| `notebooks/bootcamp_llm.py` | Helper used by every notebook. Talks to Ollama over HTTP using the **Python standard library only**. |
| `notebooks/Class_3_Neo_Handover_Note.ipynb` | Class 3 (morning), "Writing Neo's Handover Note": the 5 parts of a prompt (R-T-C-F-R), exact rules, which part matters most, few-shot examples, writing for different readers. Cells `▶ CELL S, 1–14`. |
| `notebooks/Class_4_Neo_Goes_Live.ipynb` | Class 4 (afternoon), "Neo Goes Live": fixed tracker columns (JSON), show your working + a calculator for money, read → check → draft, scam emails (prompt injection), 3 layers of protection, and testing prompts (normal / edge / bad). Cells `▶ CELL S, 1–17`. |
| `slides/Class_3_Neo_Handover_Note_Slides.html` · `slides/Class_4_Neo_Goes_Live_Slides.html` | Self-contained slide decks (open in Edge or Chrome). Each demo slide shows the cell number to run. |
| `data/emails.json` · `data/three_way_match.csv` | Mock data (fictional company "Nova Industries"). |
| `setup/setup_windows.ps1` · `setup/setup_mac_linux.sh` · `setup/check_setup.py` | One-time setup and health check. |

## Setup task (do this when asked to "set up" or "get this running")
1. Check that Ollama is installed: `ollama --version`. If not: Windows `winget install Ollama.Ollama`; Mac/Linux https://ollama.com/download.
2. Make sure the Ollama server is running (`ollama list` should work). If not: start the Ollama app, or run `ollama serve`.
3. Read `bootcamp_config.json`. If the user named a model, put it in `model`. Use a smaller one in `small_model` (it can be the same).
4. Pull the models: `ollama pull <model>` and `ollama pull <small_model>`.
5. Create a virtual environment in the bundle root and install `requirements.txt`:
   - Windows: `py -3 -m venv .venv` then `.\.venv\Scripts\python -m pip install -r requirements.txt`
   - Mac/Linux: `python3 -m venv .venv` then `./.venv/bin/pip install -r requirements.txt`
6. Run `python setup/check_setup.py` using the venv's Python. Success = three ✅ lines and "Connection OK".
7. Tell the user to open a notebook, select the **`.venv`** kernel, and run **CELL S** first.

## Rules for editing
- **Don't hard-code model names in notebooks.** Use `MODEL` / `SMALL_MODEL` from `bootcamp_llm`, which reads the config.
- Keep the `# ▶ CELL n ·` first-line comments. The slides reference these numbers.
- Participants should only edit lines marked `# ← change me`.
- Money and threshold logic belongs in **Python**, not in prompts (see Class 4, CELL 7 and 11).
- After any change, run the notebook top to bottom and confirm there are **no errors**.
- Mock data only. Never add real vendor, customer or bank data.

## Useful helper functions (from `bootcamp_llm`)
`ask_ai(q, system=None, temperature=None, max_tokens=None)` · `chat(messages, …)` · `ask_small(…)` (small model) ·
`ask_json(q, system=None, schema=None)` (uses Ollama's JSON mode if the model supports it, otherwise prompts and parses) · `parse_json(text)` ·
`stream_ai(q)` · `show(markdown)` · `check_setup()` · `last_usage` (tokens and seconds of the last call).

## Troubleshooting
| Symptom | Fix |
|---|---|
| `Cannot reach Ollama at http://localhost:11434` | Start the Ollama app / `ollama serve`. If Ollama runs on another machine, set `ollama_url` in the config. |
| `Model '…' is not downloaded` | `ollama pull <name>` |
| `ModuleNotFoundError: bootcamp_llm` | The notebook's working directory must be `notebooks/` (open the bundle folder as the workspace). |
| Very slow answers | Choose a smaller model in the config (e.g. `llama3.2:1b`), then restart the kernel. |
| `structured output is unavailable` | Harmless: `ask_json` falls back to prompt + parse automatically. |
