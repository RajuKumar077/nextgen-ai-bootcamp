"""A tiny stand-in for Ollama, used ONLY to test that the Day 4 notebooks' plumbing runs. It is NOT a language model.

It answers the same HTTP calls bootcamp_llm makes (/api/chat, /api/embed, /api/show, /api/tags, /api/version), but with fixed rules:
  * the agent: picks MCP / knowledge tools from keywords in the question, then writes an answer from the LAST tool result
  * the router (Class 8): prompt / rag / agent from keywords
  * embeddings: hashed word counts with a few synonyms (so 'signs off on really big orders' lands near 'Director approval')
So a passing test proves the code path works (tools, gates, loops, checks). It says nothing about how a real model will word things.
"""
import hashlib
import json
import math
import re

SYN = {"sign": "approv", "signs": "approv", "big": "lakh", "really": "lakh", "large": "lakh", "off": "approv", "variances": "variance"}


def vec(t):
    v = [0.0] * 64
    for w in re.findall(r"[a-z0-9]+", t.lower()):
        w = SYN.get(w, w)
        v[int(hashlib.md5(w.encode()).hexdigest(), 16) % 64] += 1
    n = math.sqrt(sum(x * x for x in v)) or 1
    return [x / n for x in v]


def _tools_used(msgs):
    out = []
    for m in msgs:
        if m["role"] == "assistant" and m["content"].startswith("{") and '"tool"' in m["content"]:
            out.append(json.loads(m["content"])["tool"])
    return out


def _results(msgs):
    out = []
    for m in msgs:
        if m["role"] == "user" and m["content"].startswith("Tool result: "):
            out.append(json.loads(m["content"][len("Tool result: "):]))
    return out


def agent(msgs):
    sysm = msgs[0]["content"]
    q = next(m["content"] for m in msgs if m["role"] == "user")
    ql = q.lower()
    used, res = _tools_used(msgs), _results(msgs)
    last = res[-1] if res else None
    po = (re.search(r"45000\d{5}", q) or [None])[0] if re.search(r"45000\d{5}", q) else None

    def tool(name, args, why): return {"thought": why, "tool": name, "args": args}
    def done(text): return {"thought": "I have what I need", "answer": text}

    if isinstance(last, dict) and "error" in last:
        return done("I could not finish: " + str(last["error"]))
    if "loop forever" in ql:
        return tool("get_order", {"po_number": "4500012345"}, "check again")
    if "ticket" in ql and po:
        if "create_ticket" not in used:
            return tool("create_ticket", {"po_number": po, "note": "Follow up on the credit check"}, "a ticket was requested")
        return done(f"Ticket {last.get('ticket_id')} was created for PO {po}.")
    if "plant" in ql and ("blocked" in ql or "delayed" in ql):
        plant = re.search(r"plant (\d{4})", ql).group(1)
        status = "Blocked" if "blocked" in ql else "Delayed"
        if not used:
            return tool("list_orders", {"plant": plant, "status": status}, f"list {status.lower()} orders for plant {plant}")
        rows = last["orders"]
        if not rows:
            return done(f"No {status.lower()} orders for plant {plant}.")
        return done("; ".join(f"{o['po_number']} ({o['block_reason'] or status.lower()}, ₹{o['value_inr']:,})" for o in rows))
    if "multi-step" in sysm and "price variance" in ql and po:                      # Class 8 capstone question
        steps = ["get_order", "check_approval", "search_policy", "get_vendor"]
        if len(used) < 4:
            nxt = steps[len(used)]
            args = {"get_order": {"po_number": po}, "check_approval": {"value_inr": str(res[0]["value_inr"]) if res else "0"},
                    "search_policy": {"query": "price variance invoice blocked"}, "get_vendor": {"vendor_id": res[0]["vendor_id"] if res else "V300"}}[nxt]
            return tool(nxt, args, f"step {len(used) + 1}")
        order, appr, hits, ven = res[0], res[1], res[2], res[3]
        hit = next((h for h in hits if "price variance" in h["text"].lower()), hits[0])
        return done(f"PO {po} (₹{order['value_inr']:,}) is {order['status'].lower()} for {str(order['block_reason']).lower()}. The {appr['approver']} must approve it (policy {appr['policy']}). "
                    f"Our rule: {hit['text'].split('] ', 1)[-1]} [{hit['id']}]. Vendor contact: {ven['contact']}, {ven['email']}.")
    if ("policy" in ql or "idoc" in ql or "payment" in ql or "bank details" in ql or "quotations" in ql or "3-way" in ql or "basis" in ql) and not po:
        if not used:
            return tool("search_policy", {"query": q}, "this is in our documents")
        return done(f"{last[0]['text'].split('] ', 1)[-1]} [{last[0]['id']}]")
    if "contact" in ql and po:
        if not used: return tool("get_order", {"po_number": po}, "find the vendor id")
        if used == ["get_order"]: return tool("get_vendor", {"vendor_id": last["vendor_id"]}, "get the contact")
        return done(f"{last['vendor']}: {last['contact']}, {last['email']}.")
    if "approve" in ql and not po and re.search(r"inr (\d+)", ql):
        if not used: return tool("check_approval", {"value_inr": re.search(r"inr (\d+)", ql).group(1)}, "who approves this value?")
        return done(f"The {last['approver']} must approve it (policy {last['policy']}).")
    if ("approve" in ql or "sign off" in ql) and po:
        if not used: return tool("get_order", {"po_number": po}, "I need the value")
        if used == ["get_order"]: return tool("check_approval", {"value_inr": str(last["value_inr"])}, "who approves this value?")
        return done(f"The {last['approver']} must approve it (policy {last['policy']}).")
    if "delayed order value" in ql:
        if not used: return tool("delayed_summary", {}, "summarise delayed orders")
        top = max(last, key=lambda v: last[v]["total_value_inr"])
        return done(f"{top} has the most delayed value: {last[top]['total_value_inr']} INR.")
    if "highest total order value" in ql:
        if "vendor_scorecard" not in sysm:
            return done("I cannot tell: I have no tool for vendor totals.")
        if not used: return tool("vendor_scorecard", {}, "per-vendor totals")
        top = max(last, key=lambda v: last[v]["total_value_inr"])
        return done(f"{top}: total {last[top]['total_value_inr']} INR, {last[top]['delayed']} delayed and {last[top]['blocked']} blocked.")
    if po and ("status" in ql or "blocked" in ql):
        if not used: return tool("get_order", {"po_number": po}, "get the status")
        return done(f"PO {po} is {last['status']} ({last['block_reason']}).")
    if "orders" in ql or "po" in ql:
        if not used: return tool("list_orders", {}, "list all orders")
        return done(f"There are {last['count']} orders.")
    return done("I do not know.")


def router(msgs):
    q = msgs[-1]["content"].lower()
    if q.startswith(("summarise", "classify", "draft")): a = "prompt"
    elif "po " in q or "orders" in q: a = "agent"
    else: a = "rag"
    return {"approach": a, "why": "mock rule"}


def chat_text(msgs):
    last = msgs[-1]["content"]
    if "Connection OK" in last: return "Connection OK"
    if "CONTEXT:" in last:
        ids = re.findall(r"^\[([^\]]+§[\d.]+)\]", last, re.M)
        return f"Answer from context. [{ids[0] if ids else '?'}]"
    if last.lower().startswith("summarise"): return "The truck was delayed by rain; delivery moves to Monday."
    if last.lower().startswith("classify"): return "thanks"
    if last.lower().startswith("draft"): return "Dear Rahul, could you please confirm the new delivery date? Regards, Neo"
    if "My PO number is" in last: return "OK"
    return "A generic answer."


def get(path):
    if path == "/api/version": return {"version": "mock"}
    if path == "/api/tags": return {"models": [{"name": n} for n in ("qwen3:8b", "llama3.2:1b", "nomic-embed-text:latest")]}
    raise AssertionError(path)


def post(path, body, stream=False):
    if path == "/api/show": return {"capabilities": ["completion"]}
    if path == "/api/embed": return {"embeddings": [vec(t) for t in body["input"]]}
    if path == "/api/chat":
        msgs = body["messages"]
        words = sum(len(m["content"].split()) for m in msgs)
        if body.get("format") == "json":
            out = router(msgs) if "simplest approach" in msgs[0]["content"] else agent(msgs)
            text = json.dumps(out)
        else:
            text = chat_text(msgs)
        return {"message": {"role": "assistant", "content": text}, "prompt_eval_count": words, "eval_count": max(1, len(text.split()))}
    raise AssertionError(path)
