"""Quick health check: is Ollama running, are the models downloaded, do chat, embeddings and the MCP server work?
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "shared"))
from bootcamp_llm import ask_ai, check_setup, cosine, embed, last_usage  # noqa: E402
from mcp_client import McpClient, McpError                               # noqa: E402

SERVER = os.path.join(ROOT, "Class_7_MCP_Guardrails", "mcp_server", "sap_orders_server.py")


def check_mcp():
    """Start the mock SAP Orders MCP server, list its tools and call one."""
    try:
        with McpClient([sys.executable, SERVER]) as c:
            tools = [t["name"] for t in c.list_tools()]
            blocked = c.call_tool("list_orders", {"plant": "1000", "status": "Blocked"})["data"]["count"]
            refused = not c.call_tool("create_ticket", {"po_number": "4500012345", "note": "health check"})["ok"]
        print(f"🔌 MCP server works: {len(tools)} tools ({', '.join(tools[:3])}, …) · plant 1000 has {blocked} blocked orders · read-only: {'yes' if refused else 'NO!'}")
        return refused
    except McpError as e:
        print("❌ MCP server:", e)
        return False


if __name__ == "__main__":
    ok = check_setup(need_embed=True)
    if ok:
        reply = ask_ai("Reply with exactly these words: Connection OK", temperature=0, max_tokens=10)
        print(f"🤖 Model says: {reply}   ({last_usage.get('seconds')} s)")
        a, b, c = embed(["Director approval above 10 lakh", "Who signs off on really big orders?", "Payment runs happen on Tuesday"])
        print(f"🧭 Embeddings work: {len(a)} numbers per text · related pair {cosine(a, b):.2f} · unrelated pair {cosine(a, c):.2f}")
    mcp_ok = check_mcp()                      # the MCP server does not need Ollama, so it is checked either way
    if ok and mcp_ok:
        print("\n🎉 All good. You are ready for Day 4.")
    else:
        print("\n⚠️  Fix the items marked ❌ above, then run this check again.")
        sys.exit(1)
