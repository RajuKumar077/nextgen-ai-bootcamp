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
| `Class_7_MCP_Guardrails/mcp_server/sap_orders_server.py` | The mock **SAP Orders MCP server** (standard library only). 6 tools, 3 resources, 2 prompts. **Read-only by default.** `--allow-write` enables `create_ticket`; `--with-scorecard` adds `vendor_scorecard`. |
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
   - Windows: `py -3 -m venv .venv` then `.\.venv\Scripts\python -m pip install -r requirements.txt`
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
From `mcp_client`: `McpClient([python, server.py, flags…])` with `.list_tools()` · `.call_tool(name, args)` → `{"ok", "data"}` · `.list_resources()` · `.read_resource(uri)` · `.list_prompts()` · `.get_prompt(name, args)` · `.wire` (the raw messages) · `.close()`.

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
