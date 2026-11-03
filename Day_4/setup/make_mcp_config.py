"""Writes the MCP config that lets VS Code and Antigravity find the mock SAP Orders server on THIS laptop (absolute paths), then test-starts each server.

    python setup/make_mcp_config.py            (use the .venv Python)

Writes:
    .vscode/mcp.json                                          VS Code (open the Day_4 folder; the servers show up in the chat tools list)
    Class_7_MCP_Guardrails/antigravity/mcp_config.json        Antigravity (paste into its MCP settings → raw config)

Two servers, the SAME Python file with different flags:
    nova-sap-orders          read-only
    nova-sap-orders-write    --allow-write --with-scorecard  (create_ticket really writes; the CLIENT should ask a person first)
"""
import json
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
from mcp_client import McpClient, McpError  # noqa: E402

SERVER = os.path.join(ROOT, "Class_7_MCP_Guardrails", "mcp_server", "sap_orders_server.py")
VENV_PY = [os.path.join(ROOT, ".venv", "bin", "python"), os.path.join(ROOT, ".venv", "Scripts", "python.exe")]
PY = next((p for p in VENV_PY if os.path.exists(p)), sys.executable)

SERVERS = {
    "nova-sap-orders": [SERVER],
    "nova-sap-orders-write": [SERVER, "--allow-write", "--with-scorecard"],
}


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print("✅ wrote", os.path.relpath(path, ROOT))


vscode = {"servers": {name: {"type": "stdio", "command": PY, "args": args} for name, args in SERVERS.items()}}
antigravity = {"mcpServers": {name: {"command": PY, "args": args} for name, args in SERVERS.items()}}
write(os.path.join(ROOT, ".vscode", "mcp.json"), vscode)
write(os.path.join(ROOT, "Class_7_MCP_Guardrails", "antigravity", "mcp_config.json"), antigravity)

print(f"\nPython used in the config: {PY}")
if PY == sys.executable and not any(os.path.exists(p) for p in VENV_PY):
    print("ℹ️  No .venv found, so the config uses the Python you ran this with. Create the .venv first if you want it to use that.")
bad = 0
for name, args in SERVERS.items():
    try:
        with McpClient([PY] + args, timeout=15) as c:
            print(f"✅ {name}: starts, {len(c.list_tools())} tools")
    except McpError as e:
        bad += 1
        print(f"❌ {name}: {e}")
print("""
Next steps
  VS Code     : open the Day_4 folder → open the chat's tools list → start the servers (names as above). Restart VS Code if they do not appear.
  Antigravity : MCP settings → manage servers → raw config → paste Class_7_MCP_Guardrails/antigravity/mcp_config.json → restart the agent.
  Menus change often between versions: use the names you actually see on screen. Mock data only.""")
sys.exit(1 if bad else 0)
