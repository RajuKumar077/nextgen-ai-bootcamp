"""Builds the two Day 3 notebooks (no outputs saved). Run:  python3 build_notebooks.py"""
import os, sys, nbformat
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from day3_common import CUT_SRC, DAY3

nbf = nbformat.v4


def md(t): return nbf.new_markdown_cell(t.strip("\n"))
def code(t): return nbf.new_code_cell(t.strip("\n"))


def save(cells, path, title):
    nb = nbf.new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"display_name": "Python 3 (.venv)", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python"}
    nb.metadata["title"] = title
    nbformat.write(nb, path)
    heads = [l for c in cells if c.cell_type == "code" for l in c.source.splitlines()[:1] if "▶ CELL" in l]
    print(os.path.basename(path), "| cells:", len(cells), "| code cells tagged:", len(heads))


TROUBLE = """
---
## 🛠️ Trainer troubleshooting (Ollama)
| Message | Cause | Fix |
|---|---|---|
| `Cannot reach Ollama at http://localhost:11434` | Ollama isn't running | Windows: Start menu → **Ollama**. Mac: open the Ollama app. Or in a terminal: `ollama serve` |
| `Model '…' is not downloaded` | The model in `bootcamp_config.json` isn't pulled | `ollama pull <name>` (see `ollama list`) |
| `ModuleNotFoundError: bootcamp_llm` | The notebook is not running from its own folder | Open the **Day_3** folder as the workspace, then pick the **`.venv`** kernel |
| Very slow answers | The model is too big for this laptop | Choose a smaller `model` in `bootcamp_config.json`, then **Restart kernel** |
| `The model did not return valid JSON` (Class 6) | Small models sometimes break the format | Run the cell again. This is a real lesson: agents need validation |
| `embed` fails or all scores look the same (Class 5) | The embedding model is missing | `ollama pull nomic-embed-text`, or set `embed_model` to your chat model in the config |
"""

# =====================================================================================================
#                                             CLASS 5
# =====================================================================================================
c5 = []
c5.append(md("""
# 📚 Class 5: Neo Reads the Policy Binder
### Giving AI our knowledge (RAG) · Day 3 · Morning · 2 hours

**Same story as Day 2.** Neo, your AI chatbot, covers your inbox while you're on leave. Today a vendor asks a question that is **only answered in your company's policy binder**. Neo has never seen that binder.

**Today's question:** *How do we make Neo answer from our documents, and show where the answer came from?*

| Part | Topic | Cells |
|---|---|---|
| 1 | Neo doesn't know our binder | S, 1–3 |
| 2 | The open-book exam: the 4 steps of RAG | 4–9 |
| 3 | Trust but verify: refusing, testing, outdated documents | 10–13 |
| 4 | Your turn | 14–15 |

> 💡 **Key terms come first.** Each part starts with a key-terms slide. Then you run the cells.
> 🔒 All documents are **mock** (fictional company *Nova Industries*). Everything runs on this laptop with Ollama.
"""))

c5.append(md("## ⚙️ ▶ CELL S: Setup\nChecks that Ollama is running and the models (chat + embedding) are downloaded. Run once."))
c5.append(code('''
# ▶ CELL S · SETUP: check Ollama (chat model + embedding model). Run once.
import sys, os, re, json, glob
sys.path.insert(0, "../../shared")            # where bootcamp_llm.py lives
from bootcamp_llm import *

DOCS_DIR = "../data/docs"                     # the mock company documents (Nova Industries)
check_setup(need_embed=True)
print("🤖 Neo says:", ask_ai("Reply with exactly these words: Connection OK", temperature=0, max_tokens=10))
'''))

c5.append(md("""
---
# 1️⃣ Neo doesn't know our binder
**In real life:** a new colleague on day one is asked *"who approves a PO above ₹10 lakh?"*. They haven't read the policy yet. A careful one says "I'll check". A confident one guesses.

### ▶ CELL 1: Ask Neo, with no documents
"""))
c5.append(code('''
# ▶ CELL 1 · No documents: Neo answers from general knowledge
QUESTION = "In our company, who approves a purchase order above ₹10 lakh?"   # ← change me
show(ask_ai(QUESTION, temperature=0))
print(f"({last_usage['seconds']} s)")
'''))
c5.append(md("""
> 🔎 **What to look for:** a generic answer ("usually a senior manager or the CFO…"). It sounds fine, but **it is not our policy**. Our policy says *Director* (Section 3.3). Better prompts can't fix this: Neo never saw the document.

### ▶ CELL 2: Paste the whole policy into the prompt
This is the simplest fix, and it works for **one short document**.
"""))
c5.append(code('''
# ▶ CELL 2 · Paste the whole policy into the prompt ("context stuffing")
policy = open(f"{DOCS_DIR}/Procurement_Policy.txt", encoding="utf-8").read()
prompt = f"""Answer ONLY from the policy below. If the answer is not in it, say "Not in the documents."

POLICY:
<<<
{policy}
>>>

Question: {QUESTION}"""
show(ask_ai(prompt, temperature=0))

total_words = sum(len(open(f, encoding="utf-8").read().split()) for f in glob.glob(f"{DOCS_DIR}/*.txt"))
print(f"\\nThis prompt: {len(prompt.split())} words.   All 4 mock documents together: {total_words} words.")
print("A real company has hundreds of documents. They will not all fit in the context window, and every question would pay for all of them.")
'''))
c5.append(md("""
> ✅ With the policy in front of it, Neo answers correctly. **But we can't paste 500 documents every time.** We need to paste only the *right page*. That is RAG.

### ▶ CELL 3: Where does "memory" come from?
The model remembers nothing between messages. The **app** re-sends the conversation each time.
"""))
c5.append(code('''
# ▶ CELL 3 · Chat "memory": the APP re-sends the history, the model remembers nothing
q1 = {"role": "user", "content": "My PO number is 4500012345. Please just say OK."}
a1 = chat([q1], temperature=0)
q2 = {"role": "user", "content": "What was my PO number?"}
print("A) Only the new message sent :", chat([q2], temperature=0))
print("B) Whole history re-sent     :", chat([q1, {"role": "assistant", "content": a1}, q2], temperature=0))
'''))
c5.append(md("> 🧠 In **A** the model has no idea. In **B** it knows, because we sent the earlier messages again. *Memory is something the app does, not the model.*"))

c5.append(md("""
---
# 2️⃣ The open-book exam: RAG in 4 steps
**In real life:** closed-book = answer from memory (and guess when unsure). Open-book = **find the right page first, then answer from it**.

```
 1. CUT      →   2. STORE      →   3. FIND       →   4. ANSWER
 split docs      save by           get the best      give pieces +
 into pieces     MEANING           pieces for a      question to Neo
 (chunks)        (embeddings)      question          → cited answer
```

### ▶ CELL 4: Step 1, CUT the documents into chunks
We cut **one chunk per numbered clause** and label each with its source, so every answer can say *where it came from*.
"""))
c5.append(code("# ▶ CELL 4 · STEP 1 · CUT: split the documents into chunks\n" + CUT_SRC + '''
PACKS = {"A": ["Procurement_Policy.txt", "SAP_P2P_Process_Guide.txt"],   # A = Procurement
         "B": ["Travel_Policy.txt"],                                      # B = Travel
         "C": ["IDoc_Error_Guide.txt"]}                                   # C = IDoc errors
DOC_PACK = "A"                                                            # ← change me (A, B or C)

chunks = [c for name in PACKS[DOC_PACK] for c in cut(f"{DOCS_DIR}/{name}")]
print(f"Pack {DOC_PACK}: {len(chunks)} chunks. The first three:\\n")
for c in chunks[:3]:
    print(" •", c["id"], "→", c["text"][:95], "…")
print("\\nThe chunk that holds the Director rule:")
print(" •", next(c["text"] for c in chunks if c["id"].endswith("§3.3")))
'''))
c5.append(md("""
> ✂️ **Chunk** = a small piece of a document. We kept each clause whole so the meaning isn't cut in half.

### ▶ CELL 5: Why not just search for words?
Normal (keyword) search counts matching words. Watch what happens when the question uses **different words** from the policy.
"""))
c5.append(code('''
# ▶ CELL 5 · Keyword search: finds matching WORDS, not matching MEANING
STOP = set("a an the of to is are who what which and or in on for do does it be by at as from that this with must".split())
def words_of(text): return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP

def keyword_search(question, top=3):
    q = words_of(question)
    scored = sorted(((len(q & words_of(c["text"])), c) for c in chunks), key=lambda s: -s[0])
    return [(score, c) for score, c in scored[:top] if score > 0]

for question in ["Who approves a PO above 10 lakh?", "Who signs off on really big orders?"]:
    print("❓", question)
    for score, c in keyword_search(question):
        print(f"   {score} matching words → {c['id']}")
    print()
'''))
c5.append(md("""
> 😕 The reworded question *"Who signs off on really big orders?"* shares almost no words with Section 3.3 (*"POs above ₹10,00,000 require Director approval"*). Keyword search picks the wrong clause. **We need search by meaning.**

### ▶ CELL 6: Step 2, STORE chunks as "meaning fingerprints"
An **embedding** is a list of numbers that captures what a text *means*. Similar meaning → similar numbers.
"""))
c5.append(code('''
# ▶ CELL 6 · STEP 2 · STORE: turn every chunk into an embedding (a "meaning fingerprint")
fingerprints = embed([c["text"] for c in chunks])
store = list(zip(chunks, fingerprints))
print(f"Stored {len(store)} chunks. Each fingerprint is a list of {len(fingerprints[0])} numbers.")
print("First 6 numbers of one fingerprint:", [round(x, 3) for x in fingerprints[0][:6]])

# Similar meaning → similar numbers (1.0 = identical meaning, near 0 = unrelated)
a, b, c_ = embed(["Who approves a big purchase order?",
                  "Director approval is needed above ₹10 lakh",
                  "Payment runs happen on Tuesday and Friday"])
print("\\nbig PO question  ↔  Director approval rule :", round(cosine(a, b), 2))
print("big PO question  ↔  Tuesday payment run    :", round(cosine(a, c_), 2))
'''))
c5.append(md("> 🧭 The first pair scores higher than the second. That is all \"search by meaning\" is: **compare fingerprints**. (Embeddings are *not* encryption; they are only a way to search.)\n\n### ▶ CELL 7: Step 3, FIND the best chunks"))
c5.append(code('''
# ▶ CELL 7 · STEP 3 · FIND: compare the question's fingerprint with every chunk
def find(question, top=3, the_store=None):
    the_store = the_store or store
    q = embed(question)
    ranked = sorted(the_store, key=lambda s: cosine(q, s[1]), reverse=True)[:top]
    return [(round(cosine(q, v), 2), c) for c, v in ranked]

for question in ["Who approves a PO above ₹10 lakh?", "Who signs off on really big orders?"]:
    print("❓", question)
    for score, c in find(question):
        print(f"   {score}  {c['id']:<32} {c['text'][-60:]}")
    print()
'''))
c5.append(md("> 🎯 Now the reworded question should find **Section 3.3** by meaning, with no shared keywords. (A small model may rank it 2nd or 3rd. That is why we pass the **top 3** chunks, not just one.)\n\n### ▶ CELL 8: Step 4, ANSWER from the pieces, with a citation"))
c5.append(code('''
# ▶ CELL 8 · STEP 4 · ANSWER: give the best chunks + the question to Neo
RAG_RULES = """You are Neo, answering questions for Nova Industries staff.
Answer ONLY from the CONTEXT. If the answer is not in the CONTEXT, reply exactly: Not in the documents.
Keep it to one or two sentences and end with the source in brackets, for example [Procurement_Policy §3.3]."""

def rag(question, top=3, the_store=None, rules=RAG_RULES):
    hits = find(question, top, the_store)
    context = "\\n".join(f"[{c['id']}] {c['text']}" for _, c in hits)
    prompt = f"CONTEXT:\\n<<<\\n{context}\\n>>>\\n\\nQuestion: {question}"
    return ask_ai(prompt, system=rules, temperature=0), hits

answer, hits = rag("Who approves a PO above ₹10 lakh?")
print("🤖 Neo:", answer)
print("📎 Sources it was given:", [c["id"] for _, c in hits])
'''))
c5.append(md("> ✅ **Retrieval + Augmented + Generation.** Neo answered from our document and named the source. *Click-to-verify is the whole point.*\n\n### ▶ CELL 9: The reworded question, end to end"))
c5.append(code('''
# ▶ CELL 9 · The reworded question, end to end
for question in ["Who signs off on really big orders?",
                 "What must happen before a vendor's bank details can be changed?"]:
    answer, hits = rag(question)
    print("❓", question)
    print("🤖", answer)
    print("📎", [c["id"] for _, c in hits], "\\n")
'''))
c5.append(md("> 💡 The second question connects to **Email D** from Day 2 (the bank-detail scam). Our policy requires *written confirmation AND a call-back* (Section 5.2). RAG lets Neo apply **our** rule."))

c5.append(md("""
---
# 3️⃣ Trust but verify
### ▶ CELL 10: What if the answer is NOT in the documents?
A grounded assistant should say **"Not in the documents"**, not guess. Compare a strict rule with a weak one.
"""))
c5.append(code('''
# ▶ CELL 10 · The "I don't know" test: not in the documents
NOT_THERE = "What is the daily allowance for a trip to Singapore?"          # ← change me
WEAK_RULES = "You are Neo, a helpful assistant for Nova Industries. Use the CONTEXT if it helps."

strict, hits = rag(NOT_THERE)
weak, _ = rag(NOT_THERE, rules=WEAK_RULES)
print("❓", NOT_THERE, "(pack A has no travel policy)\\n")
print("🔒 With a strict rule :", strict)
print("🔓 With a weak rule   :", weak)
'''))
c5.append(md("> 🛡️ The strict rule should give **\"Not in the documents.\"** The weak rule may produce a confident number from nowhere. *The rule in the note is part of the system, not decoration.*\n\n### ▶ CELL 11: Test five questions and score them"))
c5.append(code('''
# ▶ CELL 11 · Test plan: answerable · reworded · not in the documents. The CODE checks the retrieval.
TESTS = [  # (type, question, the clause that must be retrieved, or None if the answer is not in the documents)
    ("direct",   "Who approves a PO above ₹10 lakh?",                             "Procurement_Policy §3.3"),
    ("direct",   "What must happen before a vendor's bank details can be changed?", "Procurement_Policy §5.2"),
    ("direct",   "Which transaction posts a goods receipt?",                      "SAP_P2P_Process_Guide §1.3"),
    ("reworded", "Who signs off on really big orders?",                           "Procurement_Policy §3.3"),
    ("missing",  "What is the daily allowance for a trip to Singapore?",          None),
]

def score_tests(tests, the_store=None):
    points = 0
    for kind, question, expected in tests:
        answer, hits = rag(question, the_store=the_store)
        ids = [c["id"] for _, c in hits]
        ok = (expected in ids) if expected else ("not in the documents" in answer.lower())
        points += ok
        print(f"{'✅' if ok else '❌'} {kind:<8} {question}")
        print(f"     retrieved: {ids}")
        print(f"     answer   : {answer[:150]}\\n")
    print(f"Score: {points} / {len(tests)}")

score_tests(TESTS)
'''))
c5.append(md("> 📋 Always test **all three kinds**: a direct question, a reworded one, and one that is *not* in the documents. A ❌ is a good lesson: was the chunk not retrieved, or did Neo ignore it?\n\n### ▶ CELL 12: The outdated-document trap"))
c5.append(code('''
# ▶ CELL 12 · Outdated document: RAG quotes whatever you give it
old_chunks = cut("../data/old/Procurement_Policy_2024_OLD.txt")          # the 2024 policy: limits were lower
old_store = store + list(zip(old_chunks, embed([c["text"] for c in old_chunks])))

QUESTION_7L = "Who approves a PO of ₹7,00,000?"
print("Current policy says: above ₹1,00,000 and up to ₹10,00,000 → Department Head (Section 3.2).")
print("2024 policy says   : above ₹5,00,000 → Director.\\n")

answer, hits = rag(QUESTION_7L, the_store=old_store)
print("📚 With BOTH versions stored → retrieved:", [c["id"] for _, c in hits])
print("🤖", answer, "\\n")
answer, hits = rag(QUESTION_7L)
print("📗 Current policy only      → retrieved:", [c["id"] for _, c in hits])
print("🤖", answer)
'''))
c5.append(md("> ⚠️ Two versions = a coin toss, or a confidently wrong answer. **RAG is only as good as the documents.** The fix is not a better prompt: it is keeping the library current (remove old versions or tag them).\n\n### ▶ CELL 13: Chunk size matters"))
c5.append(code('''
# ▶ CELL 13 · Chunk size: one big chunk per document vs one chunk per clause
big_docs = [{"id": n.replace(".txt", ""), "text": open(f"{DOCS_DIR}/{n}", encoding="utf-8").read()} for n in PACKS["A"]]
big_store = list(zip(big_docs, embed([d["text"] for d in big_docs])))

q = "Who approves a PO above ₹10 lakh?"
ans_big, hits_big = rag(q, top=1, the_store=big_store);   tokens_big = last_usage["input_tokens"]
ans_small, hits_small = rag(q, top=3);                    tokens_small = last_usage["input_tokens"]

print(f"BIG chunks   → cites: {[c['id'] for _, c in hits_big]}   prompt size: {tokens_big} tokens")
print(f"SMALL chunks → cites: {[c['id'] for _, c in hits_small]}   prompt size: {tokens_small} tokens")
print("\\nBig chunks can only cite a whole document. Small chunks cite the exact clause and keep the prompt short.")
'''))

c5.append(md("""
---
# 4️⃣ Your turn (40 min)
Change only the lines marked **← change me**, then press **Shift + Enter**.

### ▶ CELL 14: Try another document pack
Pack **B** = Travel policy · Pack **C** = IDoc error handbook.
"""))
c5.append(code('''
# ▶ CELL 14 · Your turn: another document pack
MY_PACK = "C"                                              # ← change me ("B" = Travel, "C" = IDoc errors)
my_chunks = [c for name in PACKS[MY_PACK] for c in cut(f"{DOCS_DIR}/{name}")]
my_store = list(zip(my_chunks, embed([c["text"] for c in my_chunks])))
print(f"Pack {MY_PACK}: {len(my_chunks)} chunks stored.\\n")

MY_QUESTION = "What does IDoc status 51 mean?"            # ← change me (pack B: "What is the daily allowance in Singapore?")
answer, hits = rag(MY_QUESTION, the_store=my_store)
print("🤖", answer)
print("📎", [c["id"] for _, c in hits])
'''))
c5.append(md("### ▶ CELL 15: Write your own five test questions and score them\nUse your pack from Cell 14. For each question write the clause that **must** come back (look in `data/docs/`). Use `None` for a question that is not in the documents."))
c5.append(code('''
# ▶ CELL 15 · Your turn: your own 5 test questions (3 direct · 1 reworded · 1 not in the documents)
MY_TESTS = [   # ← change me: replace these examples (they are for pack C)
    ("direct",   "What does IDoc status 56 mean?",                                  "IDoc_Error_Guide §1.2"),
    ("direct",   "Which transaction is used to reprocess failed IDocs?",            "IDoc_Error_Guide §2.2"),
    ("direct",   "When should the Basis team be involved?",                         "IDoc_Error_Guide §2.3"),
    ("reworded", "A pile of IDocs is stuck waiting to be processed. Where do I look?", "IDoc_Error_Guide §1.4"),
    ("missing",  "What is the approval limit for a purchase order?",                None),
]
score_tests(MY_TESTS, the_store=my_store)
'''))
c5.append(md("""
---
## ✅ Remember three things
1. **RAG = open-book exam:** find the right page first, then answer from it.
2. **Citations** make answers checkable. **"Not in the documents"** is a correct answer.
3. **RAG is only as good as your documents:** current, approved, non-sensitive.

> 🌉 **Bridge to Class 6:** Neo can now *answer* from our documents. But when a manager asks *"Why is PO 4500012345 delayed and who should I contact?"* the answer isn't in a document. Neo has to **check SAP, look up the vendor and apply the policy**. Can Neo **do things**?
""" + TROUBLE))
save(c5, DAY3 + "/Class_5_RAG/notebooks/Class_5_Neo_Policy_Binder.ipynb", "Class 5 · Neo Reads the Policy Binder")

# =====================================================================================================
#                                             CLASS 6
# =====================================================================================================
c6 = []
c6.append(md("""
# 🤖 Class 6: Neo Opens SAP
### What is an AI agent, and how does it think? · Day 3 · Afternoon · 2 hours

**Same story.** This morning Neo learned to answer from the policy binder. Now a manager asks:
*"Why is PO 4500012345 delayed, and who should I contact?"*, and **the answer isn't in any document**. Neo has to check SAP, look up the vendor and apply the policy.

**Today's question:** *A chatbot answers. An agent acts. What's the difference, and how does an agent decide what to do?*

| Part | Topic | Cells |
|---|---|---|
| A | Chatbot vs agent | S, 1 |
| B | The 4 parts of an agent (and its tools) | 2–3 |
| C | How tools really work | 4 |
| D | The loop: think → act → observe | 5–7 |
| E | Your turn | 8–11 |

> 🔒 Mock SAP data only. The "SAP" here is two CSV files. Neo can use **only the tools we give it**.
"""))
c6.append(md("## ⚙️ ▶ CELL S: Setup"))
c6.append(code('''
# ▶ CELL S · SETUP: check Ollama. Run once.
import sys, os, re, json, csv
sys.path.insert(0, "../../shared")            # where bootcamp_llm.py lives
from bootcamp_llm import *

DATA_DIR = "../data"                          # orders.csv and vendors.csv (mock SAP data)
check_setup()
print("🤖 Neo says:", ask_ai("Reply with exactly these words: Connection OK", temperature=0, max_tokens=10))
'''))
c6.append(md("""
---
# A · Chatbot vs agent
**In real life:** to answer the manager properly you would (1) check the PO status, (2) find the block reason, (3) look up the vendor, (4) check the policy, (5) write the answer. **Five steps, different information at each step.**

### ▶ CELL 1: A chatbot with no tools
"""))
c6.append(code('''
# ▶ CELL 1 · A chatbot: it only has what you give it
QUESTION = "Why is PO 4500012345 delayed, and who should I contact?"   # ← change me
show(ask_ai(QUESTION, temperature=0))
'''))
c6.append(md("> 🔎 **What to look for:** it cannot know the status or the vendor, so it either says so, or **invents** something plausible. A chatbot answers from what it was given. For this question we need something that can *fetch* information.\n\n---\n# B · The 4 parts of an agent\n**Brain** (the LLM) + **Tools** (actions it can use) + **Memory** (steps so far) + **Instructions** (goal and rules).\n\n### ▶ CELL 2: The tools: ordinary Python functions\nThese are Neo's \"BAPIs\". They are **not AI**: they read our mock data and always give the same answer."))
c6.append(code('''
# ▶ CELL 2 · TOOLS: ordinary functions that read our mock SAP data (no AI inside)
ORDERS  = {r["po_number"]: r for r in csv.DictReader(open(f"{DATA_DIR}/orders.csv", encoding="utf-8"))}
VENDORS = {r["vendor_id"]: r for r in csv.DictReader(open(f"{DATA_DIR}/vendors.csv", encoding="utf-8"))}

def check_order_status(po_number):
    r = ORDERS.get(str(po_number).strip())
    if not r:
        return {"error": f"PO {po_number} not found"}
    return {"po_number": r["po_number"], "status": r["status"], "block_reason": r["block_reason"] or None,
            "value_inr": int(r["value_inr"]), "delivery_date": r["delivery_date"], "vendor_id": r["vendor_id"]}

def get_vendor_details(po_number):
    r = ORDERS.get(str(po_number).strip())
    if not r:
        return {"error": f"PO {po_number} not found"}
    v = VENDORS[r["vendor_id"]]
    return {"vendor": v["vendor_name"], "contact": v["contact"], "email": v["email"], "rating": v["rating"]}

def check_policy(value_inr):
    value = int(re.sub(r"[^0-9]", "", str(value_inr)) or 0)       # accepts 85000, "85,000" or "₹85,000"
    if value <= 100000:   return {"value_inr": value, "approver": "Line Manager",    "policy": "3.1"}
    if value <= 1000000:  return {"value_inr": value, "approver": "Department Head", "policy": "3.2"}
    return                       {"value_inr": value, "approver": "Director",        "policy": "3.3"}

print(check_order_status("4500012345"))
print(get_vendor_details("4500012345"))
print(check_policy(85000), "\\n", check_policy(1200000))
'''))
c6.append(md("> 🛠️ Same input, same output, every time. **The AI will not do the maths or the lookup. It will ask for a tool to do it.**\n\n### ▶ CELL 3: The tool menu and the instructions\nThe agent knows its tools only from a short **menu** inside its instructions. Clear names and descriptions matter, just like a good prompt."))
c6.append(code('''
# ▶ CELL 3 · TOOL MENU + INSTRUCTIONS: the only things the agent knows about its tools
TOOLS = {
    "check_order_status": {"fn": check_order_status, "args": "po_number",
                           "does": "Status, block reason, value (INR), delivery date and vendor id of a purchase order."},
    "get_vendor_details": {"fn": get_vendor_details, "args": "po_number",
                           "does": "Vendor name, contact person, email and rating for a purchase order."},
    "check_policy":       {"fn": check_policy,       "args": "value_inr",
                           "does": "Who must approve a purchase order of this value (Procurement Policy section 3)."},
}

def system_prompt():
    menu = "\\n".join(f"- {name}({t['args']}): {t['does']}" for name, t in TOOLS.items())
    return f"""You are Neo, an SAP procurement assistant for Nova Industries.
GOAL: answer the user's question using ONLY facts returned by your tools. Never guess a status, a contact or an approver.

TOOLS (the only ones you may use):
{menu}

Reply with ONE JSON object and nothing else.
To use a tool:  {{"thought": "why I need it", "tool": "<tool name>", "args": {{"<argument>": "<value>"}}}}
To finish:      {{"thought": "why I can finish", "answer": "<final answer for the user>"}}"""

print(system_prompt())
'''))
c6.append(md("""
---
# C · How tools really work
**The AI itself runs nothing.** It can only write text. So it writes a *request*, our program runs the tool, and hands back the result.

```
1. AI writes a REQUEST     {"tool": "check_order_status", "args": {"po_number": "4500012345"}}
2. The PROGRAM runs the real function
3. The PROGRAM gives the RESULT back to the AI
4. The AI carries on thinking
```
### ▶ CELL 4: One request, by hand
"""))
c6.append(code('''
# ▶ CELL 4 · ONE tool request: the AI asks, the PROGRAM runs it
messages = [{"role": "system", "content": system_prompt()},
            {"role": "user", "content": QUESTION}]
request = chat_json(messages)
print("1️⃣ The AI wrote a REQUEST :", request)

if "tool" in request:
    result = TOOLS[request["tool"]]["fn"](**request["args"])
    print("2️⃣ The PROGRAM ran it     :", result)
    print("3️⃣ The result goes back to the AI, which then decides the next step.")
else:
    print("The model answered without using a tool. Run the cell again to see a tool request.")
'''))
c6.append(md("""
> 🔑 **This is the control point.** The AI can only request tools on the menu. Unknown tool? Our program refuses (see Cell 7).

---
# D · The loop: Think → Act → Observe → Repeat
### ▶ CELL 5: The full agent
It fits on one screen. Each pass: the AI **thinks** and asks for a tool, the program **acts**, the AI **observes** the result, then repeats until it can answer.
"""))
c6.append(code('''
# ▶ CELL 5 · THE AGENT LOOP: think → act → observe → repeat
def execute(reply):
    """The PROGRAM's side: run the requested tool, but only if it is on the allowed list."""
    name, args = reply.get("tool"), reply.get("args") or {}
    if name not in TOOLS:
        return {"error": f"Unknown tool '{name}'. Allowed tools: {list(TOOLS)}"}
    try:
        return TOOLS[name]["fn"](**args)
    except (TypeError, ValueError, KeyError) as e:
        return {"error": f"Bad arguments for {name}: {e}"}

def run_agent(question, max_steps=5, verbose=True):
    messages = [{"role": "system", "content": system_prompt()}, {"role": "user", "content": question}]
    used = []
    for step in range(1, max_steps + 1):
        try:
            reply = chat_json(messages)
        except ValueError as e:                                   # the model broke the JSON format
            if verbose: print(f"⚠️  step {step}: {e}")
            messages.append({"role": "user", "content": "Reply with ONE valid JSON object only."})
            continue
        if not isinstance(reply, dict):                           # e.g. the model sent a list
            messages.append({"role": "user", "content": "Reply with ONE JSON object only."})
            continue
        if verbose: print(f"🧠 THINK   (step {step}): {reply.get('thought', '')}")
        if "answer" in reply:
            if verbose: print(f"✅ ANSWER : {reply['answer']}")
            return {"answer": str(reply["answer"]), "tools": used, "steps": step, "stopped": False}
        observation = execute(reply)                              # ACT
        used.append(reply.get("tool"))
        if verbose:
            print(f"🛠️  ACT     : {reply.get('tool')}({reply.get('args')})")
            print(f"👀 OBSERVE: {observation}")
        messages += [{"role": "assistant", "content": json.dumps(reply, ensure_ascii=False)},
                     {"role": "user", "content": "Tool result: " + json.dumps(observation, ensure_ascii=False)}]
    if verbose: print("⛔ Stopped: step limit reached")            # a guardrail (more in Class 7)
    return {"answer": None, "tools": used, "steps": max_steps, "stopped": True}

_ = run_agent(QUESTION)
'''))
c6.append(md("> 🔁 Read it aloud as **THINK → ACT → OBSERVE**. Two or three passes, then the answer. *Nobody told it the order of the tools; it decided.* The wording of the THINK lines will differ on your model.\n\n### ▶ CELL 6: Different questions, different tools"))
c6.append(code('''
# ▶ CELL 6 · Three questions: does the agent pick different tools?
EXERCISES = [  # (question, tools we expect, a word the answer should contain)
    ("What is the status of PO 4500012345?",                                  {"check_order_status"},                     "block"),
    ("Who is the vendor for PO 4500012346 and how do I contact them?",        {"get_vendor_details"},                     "rahul"),
    ("Can PO 4500012347 be approved by a line manager?",                      {"check_order_status", "check_policy"},     "yes"),
]
for question, expected_tools, keyword in EXERCISES:
    r = run_agent(question, verbose=False)
    ok_tools = expected_tools <= set(r["tools"])
    ok_answer = bool(r["answer"]) and keyword in r["answer"].lower()
    print(f"{'✅' if ok_tools and ok_answer else '⚠️'} {question}")
    print(f"     tools used: {r['tools']}   steps: {r['steps']}   stopped: {r['stopped']}")
    print(f"     answer    : {(r['answer'] or '—')[:140]}\\n")
'''))
c6.append(md("> ⚠️ A ⚠️ is not a failure of the class. It is the lesson: **agents can pick the wrong tool or misread a result**, so we test them.\n\n### ▶ CELL 7: Safety on the menu: unknown tools, bad arguments, step limit"))
c6.append(code('''
# ▶ CELL 7 · The control point: only tools on the menu run, and the loop has a step limit
print("1) A tool that is NOT on the menu:")
print("  ", execute({"tool": "delete_purchase_order", "args": {"po_number": "4500012345"}}))
print("2) Wrong arguments:")
print("  ", execute({"tool": "check_order_status", "args": {"order": "4500012345"}}))
print("3) A PO that does not exist:")
print("  ", execute({"tool": "check_order_status", "args": {"po_number": "4500099999"}}))

print("\\n4) A step limit of 1 for a question that needs two or more steps:")
_ = run_agent("Why is PO 4500012345 delayed, and who should I contact?", max_steps=1)
'''))
c6.append(md("""
> 🛡️ The program, not the AI, decides what runs. **The AI decides; the system executes, and only the tools we allow.** That is the idea we expand tomorrow (MCP and guardrails).

---
# E · Your turn (40 min)
Change only the lines marked **← change me**.

### ▶ CELL 8: Ask your own question
"""))
c6.append(code('''
# ▶ CELL 8 · Your turn: ask the agent your own question
MY_QUESTION = "Who must approve PO 4500012348, and why is it blocked?"      # ← change me
_ = run_agent(MY_QUESTION)
'''))
c6.append(md("> 💡 Try: *Who is the vendor for PO 4500012350?* · *What is the delivery date of PO 4500012354?* · *Is PO 4500012355 blocked, and who is the contact?*\n\n### ▶ CELL 9: What if we remove a tool?\nTake away `check_policy` and ask an approval question."))
c6.append(code('''
# ▶ CELL 9 · Your turn: remove a tool. What does the agent do without check_policy?
removed = TOOLS.pop("check_policy")                       # the tool leaves the menu
try:
    _ = run_agent("Who must approve PO 4500012348?", max_steps=4)
finally:
    TOOLS["check_policy"] = removed                       # put it back for the next cells
print("\\n(check_policy is back on the menu:", "check_policy" in TOOLS, ")")
'''))
c6.append(md("> 🧪 Without the policy tool the agent either says it **cannot tell**, or **guesses**. (Correct answer: *Director*, ₹12,00,000.) *Tools are what make an agent reliable.*\n\n### ▶ CELL 10: Add a new tool\nA fourth tool that summarises delayed orders per vendor. We add it to the menu, and the agent can use it straight away."))
c6.append(code('''
# ▶ CELL 10 · Your turn: add a 4th tool to the menu
def delayed_summary():
    """Number and total value of Delayed purchase orders, per vendor."""
    out = {}
    for r in ORDERS.values():
        if r["status"] == "Delayed":
            row = out.setdefault(r["vendor_name"], {"delayed_pos": 0, "total_value_inr": 0})
            row["delayed_pos"] += 1
            row["total_value_inr"] += int(r["value_inr"])
    return out

TOOLS["delayed_summary"] = {"fn": delayed_summary, "args": "(none)",
                            "does": "Number and total value (INR) of Delayed purchase orders for every vendor."}
print("Tool check →", delayed_summary())

MY_QUESTION_2 = "Which vendor has the most delayed order value, and how much is it?"   # ← change me
_ = run_agent(MY_QUESTION_2)
'''))
c6.append(md("> ✅ Expected: **Chennai Components, ₹15,00,000** (Bharat Logistics has ₹12,00,000). The tool does the adding; the agent only chooses to use it.\n\n### ▶ CELL 11: Scoreboard: check every exercise in code"))
c6.append(code('''
# ▶ CELL 11 · Final check: run all four exercise questions and score the tools used
FINAL = [  # (question, tools that must be used, word the answer must contain)
    ("What is the status of PO 4500012345?",                              {"check_order_status"},                 "block"),
    ("Who is the vendor for PO 4500012346 and how do I contact them?",    {"get_vendor_details"},                 "rahul"),
    ("Can PO 4500012347 be approved by a line manager?",                  {"check_order_status", "check_policy"}, "yes"),
    ("Who must approve PO 4500012348?",                                   {"check_policy"},                       "director"),
]
points = 0
for question, need, keyword in FINAL:
    r = run_agent(question, verbose=False)
    ok = need <= set(r["tools"]) and bool(r["answer"]) and keyword in r["answer"].lower()
    points += ok
    print(f"{'✅' if ok else '❌'} {question}   tools: {r['tools']}")
print(f"\\nScore: {points} / {len(FINAL)}")
'''))
c6.append(md("""
---
## ✅ Remember three things
1. **Agent = Brain + Tools + Memory + Instructions.**
2. It works in a **loop: Think → Act → Observe → Repeat**.
3. **The AI decides; the system executes**, and only the tools we allow.

> 🌉 **Bridge to Day 4:** Our tools were built by hand for this one agent. A real company has dozens of systems. *How do agents connect to real systems in a standard way, and how do we keep them safe?*
""" + TROUBLE))
save(c6, DAY3 + "/Class_6_Agents/notebooks/Class_6_Neo_Opens_SAP.ipynb", "Class 6 · Neo Opens SAP")
