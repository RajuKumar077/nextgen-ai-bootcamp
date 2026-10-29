"""A tiny stand-in for Ollama, used ONLY to test that the notebooks' plumbing runs. It is not a language model."""
import http.server, json, re, sys, hashlib, math
SYN = {"sign": "approv", "signs": "approv", "big": "lakh", "really": "lakh", "large": "lakh", "off": "approv"}
def vec(t):
    v = [0.0] * 64
    for w in re.findall(r"[a-z0-9]+", t.lower()):
        w = SYN.get(w, w)
        v[int(hashlib.md5(w.encode()).hexdigest(), 16) % 64] += 1
    n = math.sqrt(sum(x * x for x in v)) or 1
    return [x / n for x in v]
def tools_used(msgs): return [json.loads(m["content"])["tool"] for m in msgs if m["role"] == "assistant" and m["content"].startswith("{") and '"tool"' in m["content"]]
def results(msgs): return [m["content"] for m in msgs if m["role"] == "user" and m["content"].startswith("Tool result:")]
def agent(msgs):
    q = [m for m in msgs if m["role"] == "user"][0]["content"]
    po = (re.search(r"45000\d{5}", q) or [None])[0] if re.search(r"45000\d{5}", q) else None
    used, res = tools_used(msgs), results(msgs)
    if "delayed order value" in q:
        return {"thought": "use summary", "answer": "Chennai Components has the most delayed value: 1500000 INR."} if used else {"thought": "need summary", "tool": "delayed_summary", "args": {}}
    if not po: return {"thought": "no PO", "answer": "Please give a PO number."}
    want_vendor = "vendor" in q.lower() or "contact" in q.lower()
    want_policy = "approve" in q.lower() or "approv" in q.lower()
    if "check_order_status" not in used and not (want_vendor and not want_policy and "status" not in q.lower() and "blocked" not in q.lower() and "delayed" not in q.lower()):
        return {"thought": "need status", "tool": "check_order_status", "args": {"po_number": po}}
    if want_vendor and "get_vendor_details" not in used: return {"thought": "need vendor", "tool": "get_vendor_details", "args": {"po_number": po}}
    if want_policy and "check_policy" not in used:
        val = re.search(r'"value_inr": (\d+)', " ".join(res))
        return {"thought": "need approver", "tool": "check_policy", "args": {"value_inr": val.group(1) if val else "100000"}}
    last = " ".join(res)
    if "Director" in last: return {"thought": "done", "answer": "The Director must approve it (Policy 3.3)."}
    if "Line Manager" in last: return {"thought": "done", "answer": "Yes, a Line Manager can approve (3.1)."}
    if "Rahul" in last: return {"thought": "done", "answer": "Bharat Logistics, contact Rahul Verma, rahul@bharat.example."}
    if "Blocked" in last: return {"thought": "done", "answer": "PO is Blocked: Credit check."}
    return {"thought": "done", "answer": "See tool results."}
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, o, code=200):
        b = json.dumps(o).encode(); self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path == "/api/version": return self.send({"version": "mock"})
        if self.path == "/api/tags": return self.send({"models": [{"name": n} for n in ("llama3.2:3b", "llama3.2:1b", "nomic-embed-text:latest")]})
        self.send({}, 404)
    def do_POST(self):
        b = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if self.path == "/api/show": return self.send({"capabilities": ["completion"]})
        if self.path == "/api/embed": return self.send({"embeddings": [vec(t) for t in b["input"]]})
        if self.path == "/api/chat":
            msgs = b["messages"]; sysm = msgs[0]["content"] if msgs[0]["role"] == "system" else ""
            if b.get("format") == "json": text = json.dumps(agent(msgs))
            else:
                last = msgs[-1]["content"]
                if "Connection OK" in last: text = "Connection OK"
                elif "CONTEXT:" in last:
                    ids = re.findall(r"^\[([^\]]+§[\d.]+)\]", last, re.M)
                    qq = last.split("Question:")[-1].lower()
                    if "singapore" in qq or "allowance" in qq and "Travel" not in last: text = "Not in the documents."
                    else: text = f"Answer from context. [{ids[0] if ids else '?'}]"
                elif "My PO number is" in last: text = "OK"
                elif "What was my PO number" in last: text = "4500012345" if any("4500012345" in m["content"] for m in msgs) else "I don't know."
                else: text = "A generic answer."
            return self.send({"message": {"role": "assistant", "content": text}, "prompt_eval_count": 50, "eval_count": 10})
        self.send({}, 404)
http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
