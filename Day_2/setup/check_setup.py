"""Quick health check: is Ollama running, are the models downloaded, does a chat call work?
Run:  python setup/check_setup.py
"""
import os
import sys

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notebooks"))
from bootcamp_llm import ask_ai, check_setup, last_usage  # noqa: E402

if check_setup():
    reply = ask_ai("Reply with exactly these words: Connection OK", temperature=0, max_tokens=10)
    print(f"🤖 Model says: {reply}   ({last_usage.get('seconds')} s)")
    print("\n🎉 All good. You are ready for Day 2.")
else:
    print("\n⚠️  Fix the items marked ❌ above, then run this check again.")
    sys.exit(1)
