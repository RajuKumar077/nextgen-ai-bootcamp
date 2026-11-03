#!/usr/bin/env python3
"""
sap_orders_server.py · a mock "SAP Orders" MCP server for the bootcamp (Class 7).

What it is
    A small program that sits in front of two CSV files (orders.csv, vendors.csv = our mock SAP) and offers them
    to any MCP client (the Class 7 notebook, Antigravity, VS Code) in the standard way.
    It uses ONLY the Python standard library: nothing to install.

The 3 things an MCP server can offer
    TOOLS      actions the AI may request    list_orders · get_order · get_vendor · check_approval · delayed_summary · create_ticket
    RESOURCES  data the app can read          orders://all · orders://summary · policy://approval-limits
    PROMPTS    ready-made prompt templates    blocked_orders_report · vendor_followup

Safety (guardrails built into the server)
    * READ-ONLY by default. The one tool that changes data (create_ticket) is refused unless you start the server
      with  --allow-write.
    * Every tool says whether it is read-only (annotation readOnlyHint), so a client can ask a person before
      running anything that is not.
    * Mock data only. Nothing here talks to a real SAP system.

How it talks (MCP over stdio): one JSON-RPC 2.0 message per line on stdin/stdout. Logs go to stderr, never stdout.

Run by hand:   python sap_orders_server.py            (read-only)
               python sap_orders_server.py --allow-write
               python sap_orders_server.py --with-scorecard      (adds a 7th tool: used in Class 7, CELL 7)
"""
import argparse
import csv
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SERVER_NAME = "nova-sap-orders"
SERVER_VERSION = "1.0.0"
PROTOCOLS = ["2025-06-18", "2025-03-26", "2024-11-05"]       # newest first; we agree on the client's version if we know it
STATUSES = ["Open", "Delayed", "Blocked", "Delivered"]
CFG = {"data": os.path.join(HERE, "..", "data"), "allow_write": False, "with_scorecard": False,
       "tickets": os.environ.get("NOVA_TICKETS") or os.path.join(HERE, "tickets.jsonl")}


class ToolError(Exception):
    """A problem the AI can read and recover from (wrong argument, PO not found, server is read-only…)."""


# ───────────────────────────── the mock SAP data ─────────────────────────────
def _rows(name):
    with open(os.path.join(CFG["data"], name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def orders():
    out = []
    for r in _rows("orders.csv"):
        out.append({"po_number": r["po_number"], "vendor_id": r["vendor_id"], "vendor_name": r["vendor_name"], "plant": r["plant"],
                    "material": r["material"], "qty": int(r["qty"]), "value_inr": int(r["value_inr"]),
                    "delivery_date": r["delivery_date"], "status": r["status"], "block_reason": r["block_reason"] or None})
    return out


def vendors():
    return {r["vendor_id"]: r for r in _rows("vendors.csv")}


def approver_for(value):
    """Procurement Policy section 3. The same rule as Day 3, now behind a standard plug."""
    if value <= 100000:
        return {"value_inr": value, "approver": "Line Manager", "policy": "3.1"}
    if value <= 1000000:
        return {"value_inr": value, "approver": "Department Head", "policy": "3.2"}
    return {"value_inr": value, "approver": "Director", "policy": "3.3"}


POLICY_TEXT = ("Procurement Policy section 3 · PO approval limits (mock)\n"
               "3.1 POs up to INR 1,00,000 are approved by the Line Manager.\n"
               "3.2 POs above INR 1,00,000 and up to INR 10,00,000 are approved by the Department Head.\n"
               "3.3 POs above INR 10,00,000 require Director approval.")


# ───────────────────────────── tools ─────────────────────────────
def _text(v, name):
    if v is None or str(v).strip() == "":
        raise ToolError(f"Missing argument '{name}'.")
    return str(v).strip()


def _check_args(args, allowed):
    for k in args:
        if k not in allowed:
            raise ToolError(f"Unexpected argument '{k}'. Allowed arguments: {sorted(allowed) or 'none'}.")


def t_list_orders(a):
    _check_args(a, {"plant", "status", "vendor_id"})
    rows = orders()
    if a.get("plant") not in (None, ""):
        plant = str(a["plant"]).strip()
        if plant not in {r["plant"] for r in rows}:
            raise ToolError(f"Unknown plant '{plant}'. Plants: {sorted({r['plant'] for r in rows})}.")
        rows = [r for r in rows if r["plant"] == plant]
    if a.get("status") not in (None, ""):
        status = str(a["status"]).strip().capitalize()
        if status not in STATUSES:
            raise ToolError(f"Unknown status '{a['status']}'. Statuses: {STATUSES}.")
        rows = [r for r in rows if r["status"] == status]
    if a.get("vendor_id") not in (None, ""):
        rows = [r for r in rows if r["vendor_id"] == str(a["vendor_id"]).strip().upper()]
    return {"count": len(rows), "orders": rows}


def t_get_order(a):
    _check_args(a, {"po_number"})
    po = _text(a.get("po_number"), "po_number")
    for r in orders():
        if r["po_number"] == po:
            return r
    raise ToolError(f"PO {po} not found.")


def t_get_vendor(a):
    _check_args(a, {"vendor_id"})
    vid = _text(a.get("vendor_id"), "vendor_id").upper()
    v = vendors().get(vid)
    if not v:
        raise ToolError(f"Vendor {vid} not found. Known vendors: {sorted(vendors())}.")
    return {"vendor_id": vid, "vendor": v["vendor_name"], "contact": v["contact"], "email": v["email"], "rating": v["rating"]}


def t_check_approval(a):
    _check_args(a, {"value_inr"})
    digits = re.sub(r"[^0-9]", "", str(a.get("value_inr", "")))          # accepts 85000, "85,000" or "₹85,000"
    if not digits:
        raise ToolError("Missing argument 'value_inr' (a number in INR).")
    return approver_for(int(digits))


def t_delayed_summary(a):
    _check_args(a, set())
    out = {}
    for r in orders():
        if r["status"] == "Delayed":
            row = out.setdefault(r["vendor_name"], {"delayed_pos": 0, "total_value_inr": 0})
            row["delayed_pos"] += 1
            row["total_value_inr"] += r["value_inr"]
    return out


def t_vendor_scorecard(a):
    _check_args(a, set())
    vs, out = vendors(), {}
    for r in orders():
        row = out.setdefault(r["vendor_name"], {"rating": vs[r["vendor_id"]]["rating"], "orders": 0, "delayed": 0, "blocked": 0, "total_value_inr": 0})
        row["orders"] += 1
        row["delayed"] += r["status"] == "Delayed"
        row["blocked"] += r["status"] == "Blocked"
        row["total_value_inr"] += r["value_inr"]
    return out


def t_create_ticket(a):
    """The ONLY tool that changes anything. Refused unless the server was started with --allow-write."""
    _check_args(a, {"po_number", "note"})
    if not CFG["allow_write"]:
        raise ToolError("This server is READ-ONLY, so no ticket was created. (Start it with --allow-write to enable changes.)")
    po = _text(a.get("po_number"), "po_number")
    t_get_order({"po_number": po})                                        # the PO must exist
    note = _text(a.get("note"), "note")[:300]
    n = 1
    if os.path.exists(CFG["tickets"]):
        with open(CFG["tickets"], encoding="utf-8") as f:
            n += sum(1 for line in f if line.strip())
    ticket = {"ticket_id": f"TCK-{n:04d}", "po_number": po, "note": note, "status": "Open",
              "created": datetime.datetime.now().isoformat(timespec="seconds")}
    with open(CFG["tickets"], "a", encoding="utf-8") as f:
        f.write(json.dumps(ticket, ensure_ascii=False) + "\n")
    return ticket


def _schema(props=None, required=()):
    return {"type": "object", "properties": props or {}, "required": list(required)}


def tool_specs():
    ro = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}
    specs = [
        ("list_orders", "List purchase orders. Optional filters: plant ('1000' or '2000'), status (Open, Delayed, Blocked, Delivered), vendor_id (V100 to V400). "
                        "Each order has po_number, vendor, plant, material, value_inr, delivery_date, status and block_reason.",
         _schema({"plant": {"type": "string", "description": "Plant, for example 1000"},
                  "status": {"type": "string", "description": "Open, Delayed, Blocked or Delivered"},
                  "vendor_id": {"type": "string", "description": "Vendor id, for example V200"}}), ro, t_list_orders),
        ("get_order", "Full details of ONE purchase order: status, block reason, value (INR), delivery date, plant, vendor id.",
         _schema({"po_number": {"type": "string", "description": "Purchase order number, for example 4500012345"}}, ["po_number"]), ro, t_get_order),
        ("get_vendor", "Vendor name, contact person, email and rating for a vendor_id (for example V200). Get the vendor_id from get_order or list_orders.",
         _schema({"vendor_id": {"type": "string", "description": "Vendor id, for example V200"}}, ["vendor_id"]), ro, t_get_vendor),
        ("check_approval", "Who must approve a purchase order of this value in INR (Procurement Policy section 3).",
         _schema({"value_inr": {"type": "string", "description": "Order value in INR, for example 1200000"}}, ["value_inr"]), ro, t_check_approval),
        ("delayed_summary", "Number and total value (INR) of Delayed purchase orders, for every vendor.", _schema(), ro, t_delayed_summary),
    ]
    if CFG["with_scorecard"]:
        specs.append(("vendor_scorecard", "Per vendor: rating, number of orders, delayed orders, blocked orders and total order value (INR).", _schema(), ro, t_vendor_scorecard))
    specs.append(("create_ticket", "Create a follow-up ticket for a purchase order. THIS CHANGES DATA, so a person must approve it first.",
                  _schema({"po_number": {"type": "string", "description": "Purchase order number"},
                           "note": {"type": "string", "description": "What the ticket should say"}}, ["po_number", "note"]),
                  {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False}, t_create_ticket))
    return specs


# ───────────────────────────── resources and prompts ─────────────────────────────
def resource_list():
    return [
        {"uri": "orders://all", "name": "All purchase orders (CSV)", "description": "The full mock order list as CSV text.", "mimeType": "text/csv"},
        {"uri": "orders://summary", "name": "Order summary", "description": "Counts of orders by status and by plant.", "mimeType": "application/json"},
        {"uri": "policy://approval-limits", "name": "PO approval limits", "description": "Procurement Policy section 3 in plain text.", "mimeType": "text/plain"},
    ]


def resource_read(uri):
    if uri == "orders://all":
        with open(os.path.join(CFG["data"], "orders.csv"), encoding="utf-8") as f:
            return "text/csv", f.read()
    if uri == "orders://summary":
        rows, by_status, by_plant = orders(), {}, {}
        for r in rows:
            by_status[r["status"]] = by_status.get(r["status"], 0) + 1
            p = by_plant.setdefault(r["plant"], {"orders": 0, "value_inr": 0})
            p["orders"] += 1
            p["value_inr"] += r["value_inr"]
        return "application/json", json.dumps({"orders": len(rows), "by_status": by_status, "by_plant": by_plant}, ensure_ascii=False)
    if uri == "policy://approval-limits":
        return "text/plain", POLICY_TEXT
    raise KeyError(uri)


PROMPTS = {
    "blocked_orders_report": {
        "description": "Report of blocked purchase orders for one plant, with the reason for each block.",
        "arguments": [{"name": "plant", "description": "Plant, for example 1000", "required": True}],
        "text": ("Use the nova-sap-orders tools to list the BLOCKED purchase orders for plant {plant}. "
                 "Show a table with PO number, vendor, value in INR and block reason. Use only facts from the tools. Do not change anything.")},
    "vendor_followup": {
        "description": "Draft (do not send) a polite follow-up message to the vendor of a purchase order.",
        "arguments": [{"name": "po_number", "description": "Purchase order number", "required": True}],
        "text": ("Find the status of PO {po_number} and the contact person of its vendor with the nova-sap-orders tools. "
                 "Then draft a short, polite follow-up message to that contact. Do not send or create anything.")},
}


# ───────────────────────────── JSON-RPC plumbing ─────────────────────────────
def log(*a):
    print("[nova-sap-orders]", *a, file=sys.stderr, flush=True)


def reply(mid, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": mid}
    if error:
        msg["error"] = error
    else:
        msg["result"] = result
    return msg


def rpc_error(code, message):
    return {"code": code, "message": message}


def handle(msg):
    if not isinstance(msg, dict):
        return reply(None, error=rpc_error(-32600, "Invalid request"))
    method, mid, params = msg.get("method"), msg.get("id"), msg.get("params") or {}
    if method is None:                                                     # a response from the client: nothing to do
        return None
    is_note = "id" not in msg
    try:
        if method == "initialize":
            asked = params.get("protocolVersion")
            return reply(mid, {"protocolVersion": asked if asked in PROTOCOLS else PROTOCOLS[0],
                               "capabilities": {"tools": {"listChanged": False}, "resources": {}, "prompts": {}},
                               "serverInfo": {"name": SERVER_NAME, "title": "Nova SAP Orders (mock)", "version": SERVER_VERSION},
                               "instructions": "Mock SAP orders for Nova Industries. Use the tools for facts; never guess. "
                                               "Read-only unless the server was started with --allow-write."})
        if method in ("notifications/initialized", "notifications/cancelled"):
            return None
        if method == "ping":
            return reply(mid, {})
        if method == "tools/list":
            return reply(mid, {"tools": [{"name": n, "description": d, "inputSchema": s, "annotations": ann} for n, d, s, ann, _ in tool_specs()]})
        if method == "tools/call":
            name, args = params.get("name"), params.get("arguments") or {}
            spec = next((s for s in tool_specs() if s[0] == name), None)
            if spec is None:
                return reply(mid, error=rpc_error(-32602, f"Unknown tool: {name}"))
            if not isinstance(args, dict):
                return reply(mid, error=rpc_error(-32602, "arguments must be an object"))
            try:
                data = spec[4](args)
                return reply(mid, {"content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False)}], "isError": False})
            except ToolError as e:                                         # the AI can read this and try again
                return reply(mid, {"content": [{"type": "text", "text": str(e)}], "isError": True})
        if method == "resources/list":
            return reply(mid, {"resources": resource_list()})
        if method == "resources/read":
            uri = params.get("uri")
            try:
                mime, text = resource_read(uri)
            except KeyError:
                return reply(mid, error=rpc_error(-32002, f"Resource not found: {uri}"))
            return reply(mid, {"contents": [{"uri": uri, "mimeType": mime, "text": text}]})
        if method == "prompts/list":
            return reply(mid, {"prompts": [{"name": n, "description": p["description"], "arguments": p["arguments"]} for n, p in PROMPTS.items()]})
        if method == "prompts/get":
            p = PROMPTS.get(params.get("name"))
            if not p:
                return reply(mid, error=rpc_error(-32602, f"Unknown prompt: {params.get('name')}"))
            vals = params.get("arguments") or {}
            missing = [a["name"] for a in p["arguments"] if a.get("required") and a["name"] not in vals]
            if missing:
                return reply(mid, error=rpc_error(-32602, f"Missing prompt argument(s): {missing}"))
            return reply(mid, {"description": p["description"],
                               "messages": [{"role": "user", "content": {"type": "text", "text": p["text"].format(**{k: vals[k] for k in vals})}}]})
        if is_note:
            return None
        return reply(mid, error=rpc_error(-32601, f"Method not found: {method}"))
    except Exception as e:                                                 # never crash the server on one bad message
        log("internal error:", repr(e))
        return None if is_note else reply(mid, error=rpc_error(-32603, f"Internal error: {e}"))


def main():
    ap = argparse.ArgumentParser(description="Mock SAP Orders MCP server (stdio)")
    ap.add_argument("--data", default=CFG["data"], help="folder with orders.csv and vendors.csv")
    ap.add_argument("--allow-write", action="store_true", help="enable the create_ticket tool (default: read-only)")
    ap.add_argument("--with-scorecard", action="store_true", help="add the vendor_scorecard tool")
    ap.add_argument("--tickets", default=CFG["tickets"], help="where create_ticket writes (JSON lines)")
    a = ap.parse_args()
    CFG.update({"data": os.path.abspath(a.data), "allow_write": a.allow_write, "with_scorecard": a.with_scorecard, "tickets": os.path.abspath(a.tickets)})
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    log(f"v{SERVER_VERSION} ready · {'WRITE enabled' if CFG['allow_write'] else 'read-only'} · data: {CFG['data']}")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            out = handle(json.loads(line))
        except json.JSONDecodeError:
            out = reply(None, error=rpc_error(-32700, "Parse error"))
        if out is not None:
            sys.stdout.write(json.dumps(out, ensure_ascii=True) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
