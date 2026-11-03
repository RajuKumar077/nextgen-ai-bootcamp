"""Shared pieces for the Day 4 builders (notebooks + slides). Not needed to run the course.

Everything the notebooks and the slides must agree on lives here ONCE:
  * the code that goes into the notebook cells (CUT_SRC, AGENT_SRC, ...). The slide builder RUNS the same text, so numbers on slides are real.
  * the paths (relative to this file, so the bundle can live in any folder).
"""
import os
import re
import sys

BUILD = os.path.dirname(os.path.abspath(__file__))
DAY4 = os.path.dirname(BUILD)
C7 = DAY4 + "/Class_7_MCP_Guardrails"
C8 = DAY4 + "/Class_8_Capstone"
SERVER = C7 + "/mcp_server/sap_orders_server.py"
DOCS = C8 + "/data/docs"
sys.path.insert(0, DAY4 + "/shared")

# ------------------------------------------------------------------ the chunker (same text as Day 3 / Class 5, CELL 4)
CUT_SRC = r'''def cut(path):
    """Split one document into chunks: one chunk per numbered clause, labelled with its source and section."""
    name = os.path.basename(path).replace(".txt", "")
    heading, chunks = "", []
    for block in open(path, encoding="utf-8").read().split("\n\n"):
        for line in block.strip().splitlines():
            m = re.match(r"^(\d+\.\d+)\s+(.*)", line)
            if m:                                    # a numbered clause, e.g. "3.3 POs above ..."
                chunks.append({"id": f"{name} §{m.group(1)}", "text": f"[{name} · {heading}] {line}"})
            elif re.match(r"^\d+\.\s", line):        # a section heading, e.g. "3. PO APPROVAL LIMITS"
                heading = line
    return chunks
'''

# ------------------------------------------------------------------ the agent over MCP (Class 7 CELL 5; reused in Class 8 CELL 4)
AGENT_DEFAULTS_SRC = r'''ROLE = "You are Neo, an SAP procurement assistant for Nova Industries."
RULES = ["Answer using ONLY facts returned by your tools. Never guess a status, a contact, a value or an approver.",
         "If a tool returns an error, read it and try again, or say what is missing."]
FORMAT = ""               # optional: how the final answer should look (the Class 8 capstone sets this)
'''

MENU_SRC = r'''ALLOWED = None            # None = every tool the server offers. Or a set of names: an allow-list.
MAX_STEPS = 6             # the step limit: an agent must never loop forever

def offered():
    """The tools the server offers RIGHT NOW (name -> description, arguments, read-only label). Nobody types this list."""
    return {t["name"]: t for t in client.list_tools() if ALLOWED is None or t["name"] in ALLOWED}

def system_prompt():
    menu = "\n".join(f"- {n}({', '.join(t['inputSchema']['properties'])}): {t['description']}" for n, t in offered().items())
    rules = "\n".join(f"- {r}" for r in RULES)
    return f"""{ROLE}
RULES:
{rules}

TOOLS (the only ones you may use):
{menu}

Reply with ONE JSON object and nothing else.
To use a tool:  {{"thought": "why I need it", "tool": "<tool name>", "args": {{"<argument>": "<value>"}}}}
To finish:      {{"thought": "why I can finish", "answer": "<final answer for the user>"}}
{FORMAT}""".strip()
'''

LOOP_SRC = r'''def gate(tool, args):
    """GUARDRAIL between 'the AI asked' and 'the program runs it'. First version: read-only tools only."""
    return bool(tool["annotations"].get("readOnlyHint"))

def execute(reply):
    """The PROGRAM's side: check the request, then ask the MCP server to run it."""
    name, args = reply.get("tool"), reply.get("args")
    tools = offered()
    if name not in tools:
        return {"error": f"Unknown tool '{name}'. Allowed tools: {list(tools)}"}
    if not isinstance(args, dict):
        return {"error": 'args must be an object, for example {"po_number": "4500012345"}'}
    if not gate(tools[name], args):
        return {"error": f"Blocked by a guardrail: '{name}' is not allowed to run."}
    result = client.call_tool(name, args)
    return result["data"] if result["ok"] else {"error": result["data"]}

def run_agent(question, max_steps=None, verbose=True):
    max_steps = max_steps or MAX_STEPS
    messages = [{"role": "system", "content": system_prompt()}, {"role": "user", "content": question}]
    used, evidence = [], []
    for step in range(1, max_steps + 1):
        try:
            reply = chat_json(messages)                                  # THINK
        except ValueError as e:                                          # the model broke the JSON format
            if verbose: print(f"⚠️  step {step}: {e}")
            messages.append({"role": "user", "content": "Reply with ONE valid JSON object only."})
            continue
        if not isinstance(reply, dict):
            messages.append({"role": "user", "content": "Reply with ONE JSON object only."})
            continue
        if verbose: print(f"🧠 THINK   (step {step}): {reply.get('thought', '')}")
        if "answer" in reply:
            if verbose: print(f"✅ ANSWER : {reply['answer']}")
            return {"answer": str(reply["answer"]), "tools": used, "steps": step, "stopped": False, "evidence": evidence, "approval_tools": needs_approval(used)}
        observation = execute(reply)                                     # ACT
        used.append(reply.get("tool"))
        evidence.append({"tool": reply.get("tool"), "args": reply.get("args"), "result": observation})
        if verbose:
            print(f"🛠️  ACT     : {reply.get('tool')}({reply.get('args')})")
            print(f"👀 OBSERVE: {json.dumps(observation, ensure_ascii=False)[:300]}")
        messages += [{"role": "assistant", "content": json.dumps(reply, ensure_ascii=False)},          # OBSERVE
                     {"role": "user", "content": "Tool result: " + json.dumps(observation, ensure_ascii=False)}]
    if verbose: print("⛔ Stopped: step limit reached")                   # a guardrail
    return {"answer": None, "tools": used, "steps": max_steps, "stopped": True, "evidence": evidence, "approval_tools": needs_approval(used)}

def needs_approval(tool_names):
    """Which of these tools change data (so a person must approve them)? The server labels every tool."""
    tools = {t["name"]: t for t in client.list_tools()}
    return [n for n in tool_names if n in tools and not tools[n]["annotations"].get("readOnlyHint", False)]
'''

AGENT_SRC = MENU_SRC + "\n" + LOOP_SRC       # both halves in ONE cell (Class 8)


# ------------------------------------------------------------------ human approval (Class 7 CELL 8; the gate is swapped, the loop is untouched)
APPROVAL_SRC = r'''def ask_person(name, args):
    """Pause the agent until a human decides. (Set BOOTCAMP_AUTO_APPROVE=yes|no only for automated tests.)"""
    print(f"\n🛑 APPROVAL NEEDED: the agent wants to run  {name}({args})")
    answer = os.environ.get("BOOTCAMP_AUTO_APPROVE") or input("   Approve? Type yes or no: ")
    ok = answer.strip().lower() in ("y", "yes")
    print("   ✅ Approved by a person." if ok else "   ⛔ Declined. Nothing was changed.")
    return ok

def gate(tool, args):
    if tool["annotations"].get("readOnlyHint"):
        return True                                       # reading is safe: let it run
    return ask_person(tool["name"], args)                 # changing data: a person decides
'''


CHECK_SRC = r'''def check_answer(question, result):
    """Code, not hope: every number and every citation in the answer must come from the evidence."""
    evidence = json.dumps(result["evidence"], ensure_ascii=False)
    haystack = re.sub(r"(?<=\d),(?=\d)", "", evidence + " " + question)             # 12,00,000 -> 1200000
    answer, problems = result["answer"] or "", []
    for n in sorted(set(re.findall(r"\d[\d,]{3,}\d", answer))):                      # numbers with 4+ digits
        if n.replace(",", "") not in haystack:
            problems.append(f"number {n} is not in any tool result")
    for cite in sorted(set(re.findall(r"[A-Za-z0-9_]+ §\d+(?:\.\d+)*", answer))):          # citations such as Procurement_Policy §6.2
        if cite not in evidence:
            problems.append(f"citation {cite} was never retrieved")
    return problems
'''


def run_src(src, ns):
    exec(compile(src, "<cell>", "exec"), ns)
    return ns


def word_count(path):
    return len(open(path, encoding="utf-8").read().split())


def chunk_all():
    """Chunks of all four mock documents, using the exact chunker that goes into the notebook."""
    ns = run_src(CUT_SRC, {"os": os, "re": re})
    out = []
    for n in sorted(os.listdir(DOCS)):
        if n.endswith(".txt"):
            out += ns["cut"](f"{DOCS}/{n}")
    return out
