#!/usr/bin/env bash
# Day 2 Prompt Engineering · one-time setup for macOS / Linux
# Run from this folder:   bash setup/setup_mac_linux.sh
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"

echo "=== 1/5 Checking Ollama ==="
command -v ollama >/dev/null || { echo "Install Ollama first: https://ollama.com/download"; exit 1; }
ollama --version

echo "=== 2/5 Reading model names ==="
MODEL=$(python3 -c "import json;print(json.load(open('bootcamp_config.json'))['model'])")
SMALL=$(python3 -c "import json;print(json.load(open('bootcamp_config.json'))['small_model'])")
echo "Main: $MODEL   Small: $SMALL"

echo "=== 3/5 Pulling models ==="
ollama pull "$MODEL"; [ "$SMALL" != "$MODEL" ] && ollama pull "$SMALL"

echo "=== 4/5 Python venv ==="
python3 -m venv .venv && ./.venv/bin/pip install -q --upgrade pip && ./.venv/bin/pip install -q -r requirements.txt

echo "=== 5/5 Connection test ==="
./.venv/bin/python setup/check_setup.py
echo "Done. Open notebooks/Class_3_*.ipynb and choose the '.venv' kernel."
