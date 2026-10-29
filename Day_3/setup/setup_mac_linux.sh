#!/usr/bin/env bash
# Day 3 · RAG + Agents · one-time setup for macOS / Linux
# Run from the Day_3 folder:   bash setup/setup_mac_linux.sh
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"

echo "=== 1/5 Checking Ollama ==="
command -v ollama >/dev/null || { echo "Install Ollama first: https://ollama.com/download"; exit 1; }
ollama --version

echo "=== 2/5 Reading model names ==="
MODELS=$(python3 -c "import json;c=json.load(open('bootcamp_config.json'));print(' '.join(dict.fromkeys([c['model'],c['small_model'],c['embed_model']])))")
echo "Models: $MODELS"

echo "=== 3/5 Pulling models ==="
for m in $MODELS; do ollama pull "$m"; done

echo "=== 4/5 Python venv ==="
python3 -m venv .venv && ./.venv/bin/pip install -q --upgrade pip && ./.venv/bin/pip install -q -r requirements.txt

echo "=== 5/5 Connection test ==="
./.venv/bin/python setup/check_setup.py
echo "Done. Open Class_5_RAG/notebooks/Class_5_*.ipynb and choose the '.venv' kernel."
