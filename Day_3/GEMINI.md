# AGENTS.md: Instructions for AI coding agents (Antigravity, Claude Code, Copilot, Cursor…)

You are helping a trainer set up and run **Day 3** of the bootcamp *"GenAI & Agentic AI for SAP Professionals"*:
**Class 5 (RAG)** and **Class 6 (AI agents)**. The audience is SAP consultants, not developers.
Keep everything simple and **never print secrets**. All data is mock (fictional company "Nova Industries").

## What this bundle is
| Path | Purpose |
|---|---|
| `bootcamp_config.json` | **The only file to edit to switch models.** `model` (chat), `small_model`, and `embed_model` (text → meaning fingerprints for RAG). All three are placeholders. |
| `shared/bootcamp_llm.py` | Helper used by every notebook. Talks to Ollama over HTTP using the **Python standard library only**. |
| `Class_5_RAG/notebooks/Class_5_Neo_Policy_Binder.ipynb` | Class 5 (morning). RAG in 4 steps: cut, store, find, answer, plus refusal, testing, outdated documents, chunk size. Cells `▶ CELL S, 1–15`. |
| `Class_5_RAG/data/docs/*.txt` | Mock documents: procurement policy, SAP process guide, travel policy, IDoc error handbook. `data/old/` holds an outdated policy used in CELL 12. |
| `Class_6_Agents/notebooks/Class_6_Neo_Opens_SAP.ipynb` | Class 6 (afternoon). Chatbot vs agent, tools, tool menu, the Think → Act → Observe loop, safety checks. Cells `▶ CELL S, 1–11`. |
| `Class_6_Agents/data/orders.csv` · `vendors.csv` | Mock SAP data read by the agent's tools. |
| `Class_6_Agents/antigravity/` | `TASK.md` (the live demo task) and `expected_delayed_report.md` (answer key). |
| `Class_*/slides/*.html` | Self-contained slide decks (open in Edge or Chrome). Each demo slide shows the cell number to run. |
| `setup/setup_windows.ps1` · `setup_mac_linux.sh` · `check_setup.py` | One-time setup and health check. |
| `_build/` | Generators for the notebooks and slides. Not needed to run the course. |

## Setup task (do this when asked to "set up" or "get this running")
1. Check that Ollama is installed: `ollama --version`. If not: Windows `winget install Ollama.Ollama`; Mac/Linux https://ollama.com/download.
2. Make sure the Ollama server is running (`ollama list` should work). If not: start the Ollama app, or run `ollama serve`.
3. Read `bootcamp_config.json`. If the user named a model, put it in `model`. Use a smaller one in `small_model`. Keep `embed_model` as `nomic-embed-text` unless the user cannot download it; in that case set it to the same value as `model`.
4. Pull the models: `ollama pull <model>`, `ollama pull <small_model>` and `ollama pull <embed_model>`.
5. Create a virtual environment in the bundle root and install `requirements.txt`:
   - Windows: `py -3 -m venv .venv` then `.\.venv\Scripts\python -m pip install -r requirements.txt`
   - Mac/Linux: `python3 -m venv .venv` then `./.venv/bin/pip install -r requirements.txt`
6. Run `python setup/check_setup.py` using the venv's Python. Success = ✅ lines, "Connection OK", and an embeddings line.
7. Tell the user to open a notebook, select the **`.venv`** kernel, and run **CELL S** first.

## Rules for editing
- **Don't hard-code model names in notebooks.** Use `MODEL`, `SMALL_MODEL`, `EMBED_MODEL` from `bootcamp_llm`.
- Keep the `# ▶ CELL n ·` first-line comments. The slides reference these numbers.
- Participants should only edit lines marked `# ← change me`.
- Approval limits and other business rules live in **Python tools**, not in prompts (Class 6, `check_policy`).
- The agent may only run tools that are in the `TOOLS` menu (allow-list). Never add tools that post, pay, delete or email.
- After any change, run the notebook top to bottom and confirm there are **no errors**.
- Mock data only. Never add real vendor, customer or bank data.

## Useful helper functions (from `bootcamp_llm`)
`ask_ai(q, system=None, temperature=None, max_tokens=None)` · `chat(messages, …)` · `chat_json(messages)` (a JSON dict back; used by the agent) ·
`embed(text_or_list)` · `cosine(a, b)` · `ask_json(q, …)` · `parse_json(text)` · `show(markdown)` · `check_setup(need_embed=True)` · `last_usage`.

## Troubleshooting
| Symptom | Fix |
|---|---|
| `Cannot reach Ollama at http://localhost:11434` | Start the Ollama app / `ollama serve`. If Ollama runs on another machine, set `ollama_url` in the config. |
| `Model '…' is not downloaded` | `ollama pull <name>` |
| Embedding step fails or every score looks the same | `ollama pull nomic-embed-text`, or set `embed_model` to your chat model. |
| `ModuleNotFoundError: bootcamp_llm` | The notebook must run from its own `notebooks/` folder. Open the **Day_3** folder as the workspace. |
| `The model did not return valid JSON` (Class 6) | A small model broke the format. Run the cell again. The agent retries on its own. |
| The agent picks the wrong tool | Normal with small models. Try a larger `model` (7B or 8B tends to follow tool menus better) or improve the tool descriptions in CELL 3. |
| Very slow answers | Choose a smaller model in the config, then **Restart kernel**. |
