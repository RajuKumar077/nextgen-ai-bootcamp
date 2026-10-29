"""Quick health check: is Ollama running, are the models downloaded, do chat and embeddings work?
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

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shared"))
from bootcamp_llm import ask_ai, check_setup, cosine, embed, last_usage  # noqa: E402

if check_setup(need_embed=True):
    reply = ask_ai("Reply with exactly these words: Connection OK", temperature=0, max_tokens=10)
    print(f"🤖 Model says: {reply}   ({last_usage.get('seconds')} s)")
    a, b, c = embed(["Director approval above 10 lakh", "Who signs off on really big orders?", "Payment runs happen on Tuesday"])
    print(f"🧭 Embeddings work: {len(a)} numbers per text · related pair {cosine(a, b):.2f} · unrelated pair {cosine(a, c):.2f}")
    print("\n🎉 All good. You are ready for Day 3.")
else:
    print("\n⚠️  Fix the items marked ❌ above, then run this check again.")
    sys.exit(1)
