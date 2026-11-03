"""
mcp_client.py · a tiny MCP client for the bootcamp (Class 7 and Class 8). Python standard library only.

It starts an MCP server as a child process and talks to it the standard way: JSON-RPC messages, one per line, over stdin/stdout.
Participants never need to read this file. Notebooks just do:   from mcp_client import *

    client = McpClient([sys.executable, "server.py"])     # start the server and shake hands
    client.list_tools()                                    # DISCOVER what it offers (nobody typed this menu by hand)
    client.call_tool("get_order", {"po_number": "4500012345"})
    client.close()
"""
import json
import os
import queue
import subprocess
import sys
import threading

__all__ = ["McpClient", "McpError", "tool_result_data"]

CLIENT_INFO = {"name": "bootcamp-notebook", "version": "1.0.0"}
PROTOCOL = "2025-06-18"


class McpError(RuntimeError):
    """A friendly error with a clear 'how to fix' message."""


def tool_result_data(result):
    """The text of a tools/call result, as a Python object when it is JSON (otherwise the plain text)."""
    text = "\n".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text")
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return text


class McpClient:
    def __init__(self, command, timeout=20, env=None):
        self.command, self.timeout, self._id, self._lines, self.server_info = list(command), timeout, 0, queue.Queue(), {}
        self.stderr_lines = []
        self.wire = []                 # every message in order: ("→" sent | "←" received, message). Used by Class 7, CELL 4.
        try:
            self._proc = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          text=True, encoding="utf-8", bufsize=1, env={**os.environ, **(env or {})})
        except OSError as e:
            raise McpError(f"Could not start the MCP server: {e}\n👉 Fix: check the path to the server file and that Python can run it.") from None
        threading.Thread(target=self._pump, args=(self._proc.stdout, self._lines), daemon=True).start()
        threading.Thread(target=lambda: [self.stderr_lines.append(l.rstrip()) for l in self._proc.stderr], daemon=True).start()
        info = self._request("initialize", {"protocolVersion": PROTOCOL, "capabilities": {}, "clientInfo": CLIENT_INFO})
        self.server_info, self.capabilities, self.protocol = info.get("serverInfo", {}), info.get("capabilities", {}), info.get("protocolVersion")
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    # ── plumbing ──
    @staticmethod
    def _pump(stream, q):
        for line in stream:
            q.put(line)
        q.put(None)

    def _send(self, msg):
        self.wire.append(("→", msg))
        try:
            self._proc.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
            self._proc.stdin.flush()
        except (BrokenPipeError, OSError):
            raise McpError("The MCP server stopped.\n👉 Fix: run the server file by hand to see its error: " + " ".join(self.command)) from None

    def _request(self, method, params=None):
        self._id += 1
        mid = self._id
        self._send({"jsonrpc": "2.0", "id": mid, "method": method, "params": params or {}})
        while True:
            try:
                line = self._lines.get(timeout=self.timeout)
            except queue.Empty:
                raise McpError(f"The MCP server did not answer '{method}' within {self.timeout} s.") from None
            if line is None:
                tail = " | ".join(self.stderr_lines[-3:])
                raise McpError("The MCP server stopped before answering." + (f"\n   server said: {tail}" if tail else "")) from None
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if msg.get("id") == mid:
                self.wire.append(("←", msg))
                if "error" in msg:
                    raise McpError(f"{method}: {msg['error'].get('message')} (code {msg['error'].get('code')})")
                return msg.get("result", {})

    # ── the three things a server offers ──
    def list_tools(self):
        return self._request("tools/list").get("tools", [])

    def call_tool(self, name, arguments=None):
        """Returns {'ok': bool, 'data': <parsed JSON or text>}. A tool problem (isError) is NOT an exception: the AI should read it."""
        r = self._request("tools/call", {"name": name, "arguments": arguments or {}})
        return {"ok": not r.get("isError", False), "data": tool_result_data(r)}

    def list_resources(self):
        return self._request("resources/list").get("resources", [])

    def read_resource(self, uri):
        return self._request("resources/read", {"uri": uri}).get("contents", [{}])[0].get("text", "")

    def list_prompts(self):
        return self._request("prompts/list").get("prompts", [])

    def get_prompt(self, name, arguments=None):
        r = self._request("prompts/get", {"name": name, "arguments": arguments or {}})
        return "\n".join(m["content"]["text"] for m in r.get("messages", []))

    def ping(self):
        self._request("ping")
        return True

    def close(self):
        try:
            self._proc.stdin.close()
            self._proc.wait(timeout=3)
        except Exception:
            self._proc.kill()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
