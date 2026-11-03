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
