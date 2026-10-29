"""Shared pieces for the Day 3 builders (notebooks + slides). Not needed to run the course."""
import os, re, glob, csv

DAY3 = os.path.expanduser("~/Desktop/Day_3")
DOCS = DAY3 + "/Class_5_RAG/data/docs"
PACKS = {"A": ["Procurement_Policy.txt", "SAP_P2P_Process_Guide.txt"], "B": ["Travel_Policy.txt"], "C": ["IDoc_Error_Guide.txt"]}

# The exact chunker that goes into the notebook (CELL 4). The slide builder runs the same text to get REAL numbers.
CUT_SRC = '''def cut(path):
    """Split one document into chunks: one chunk per numbered clause, labelled with its source and section."""
    name = os.path.basename(path).replace(".txt", "")
    heading, chunks = "", []
    for block in open(path, encoding="utf-8").read().split("\\n\\n"):
        for line in block.strip().splitlines():
            m = re.match(r"^(\\d+\\.\\d+)\\s+(.*)", line)
            if m:                                    # a numbered clause, e.g. "3.3 POs above ..."
                chunks.append({"id": f"{name} §{m.group(1)}", "text": f"[{name} · {heading}] {line}"})
            elif re.match(r"^\\d+\\.\\s", line):        # a section heading, e.g. "3. PO APPROVAL LIMITS"
                heading = line
    return chunks
'''
_ns = {"os": os, "re": re}
exec(CUT_SRC, _ns)
cut = _ns["cut"]

def pack_chunks(p): return [c for n in PACKS[p] for c in cut(f"{DOCS}/{n}")]
def words(path): return len(open(path, encoding="utf-8").read().split())
