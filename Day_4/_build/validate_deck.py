"""Structural checks for a generated slide deck (no browser needed). Run:  python validate_deck.py <deck.html> <notebook.ipynb>

Limits come from MEASURING the finished Day 3 decks (Class 5 and 6):
    text per slide     <= 800 characters   (Day 3 maximum: 791)
    table rows         <= 6                (Day 3 maximum: 6)
    code lines (<pre>) <= 13               (Day 3 maximum: 13)
    cards in one grid  <= 4
It also checks: tag balance, notes on every slide, every ▶ CELL tag exists in the notebook, every notebook cell is used by a slide,
the JavaScript parses (node --check), no leftover placeholders, and the cover pill counts the key terms.
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

MAX_CHARS, MAX_ROWS, MAX_PRE, MAX_CARDS = 800, 6, 13, 4
VOID = {"meta", "br", "hr", "img", "input", "link"}


class Balance(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"</{tag}> closes <{self.stack[-1] if self.stack else None}> (line {self.getpos()[0]})")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()


def cells_in_notebook(path):
    nb = json.load(open(path, encoding="utf-8"))
    out = set()
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            m = re.match(r"#\s*▶ CELL (\w+)", "".join(c["source"]).splitlines()[0])
            if m:
                out.add(m.group(1))
    return out


def expand(tag):
    """'11–12' -> {'11','12'}"""
    m = re.match(r"^(\d+)[–-](\d+)$", tag)
    return {str(i) for i in range(int(m.group(1)), int(m.group(2)) + 1)} if m else {tag}


def validate(deck, notebook):
    h = open(deck, encoding="utf-8").read()
    problems, notes = [], []
    p = Balance(); p.feed(h)
    if p.errors: problems += ["tag balance: " + e for e in p.errors[:5]]
    if p.stack: problems.append("unclosed tags: " + str(p.stack[:6]))
    if "{{" in h: problems.append("unfilled {{placeholder}}")

    slides = re.findall(r'<section class="(slide[^"]*)" data-section="([^"]*)">(.*?)</section>', h, re.S)
    nb_cells = cells_in_notebook(notebook)
    used, kinds = set(), {"div": 0, "terms": 0, "title": 0}
    worst = {"chars": (0, 0), "rows": (0, 0), "pre": (0, 0), "cards": (0, 0)}
    for i, (cls, section, inner) in enumerate(slides, 1):
        if "slide div" in cls: kinds["div"] += 1
        if "title" in cls: kinds["title"] += 1
        if 'class="terms' in inner: kinds["terms"] += 1
        if '<aside class="notes">' not in inner: problems.append(f"slide {i}: no speaker notes")
        for m in re.finditer(r'data-cell="([^"]+)"', inner):
            for c in expand(m.group(1)):
                used.add(c)
                if c not in nb_cells: problems.append(f"slide {i}: points at CELL {c}, which is not in the notebook")
        body = re.sub(r'<aside class="notes">.*?</aside>', "", inner, flags=re.S)
        body = re.sub(r'<div class="shell">.*?</div>\n', "", body, count=1, flags=re.S)
        body = re.sub(r'<div class="hint">.*?</div>', "", body, flags=re.S)
        chars = len(re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body))).strip())
        rows = max([t.count("<tr") for t in re.findall(r"<table.*?</table>", body, re.S)] or [0])
        pre = max([x.count("\n") + 1 for x in re.findall(r"<pre[^>]*>(.*?)</pre>", body, re.S)] or [0])
        cards = max([g.count('class="card') for g in re.findall(r'<div class="g[2-5]".*?(?=</div></div>|$)', body, re.S)] or [0])
        for k, v in (("chars", chars), ("rows", rows), ("pre", pre), ("cards", cards)):
            if v > worst[k][0]: worst[k] = (v, i)
        if chars > MAX_CHARS: problems.append(f"slide {i}: {chars} characters (limit {MAX_CHARS}): too much text")
        if rows > MAX_ROWS: problems.append(f"slide {i}: table has {rows} rows (limit {MAX_ROWS})")
        if pre > MAX_PRE: problems.append(f"slide {i}: code block has {pre} lines (limit {MAX_PRE})")
        if cards > MAX_CARDS: problems.append(f"slide {i}: {cards} cards in one grid (limit {MAX_CARDS})")
        if not body.strip(): problems.append(f"slide {i}: empty")
    unused = sorted(nb_cells - used, key=lambda c: (c == "S", int(c) if c.isdigit() else 0))
    unused = [c for c in unused]
    if unused: problems.append("notebook cells with no slide: " + ", ".join(unused))

    terms = len(re.findall(r'class="term f"', h))
    m = re.search(r'class="pill hl">(\d+) key terms', h)
    if not m or int(m.group(1)) != terms: problems.append(f"cover says {m.group(1) if m else 'nothing'} key terms, slides hold {terms}")

    # slide numbering of Term xx runs 01..N without gaps
    nums = [int(x) for x in re.findall(r'<span class="tno">Term (\d+)</span>', h)]
    if nums != list(range(1, len(nums) + 1)): problems.append("Term numbers are not 01..N in order")

    # the JavaScript must parse
    js = re.search(r"<script>(.*?)</script>", h, re.S).group(1)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
    r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
    os.unlink(f.name)
    if r.returncode: problems.append("JavaScript does not parse: " + r.stderr.strip().splitlines()[0][:200])

    summary = (f"{len(slides)} slides · {kinds['div']} dividers · {kinds['terms']} key-term slides ({terms} terms) · cells used: {len(used)}/{len(nb_cells)} · "
               f"max chars {worst['chars'][0]} (slide {worst['chars'][1]}) · max table rows {worst['rows'][0]} · max code lines {worst['pre'][0]} · max cards {worst['cards'][0]}")
    return problems, summary


if __name__ == "__main__":
    problems, summary = validate(sys.argv[1], sys.argv[2])
    print(os.path.basename(sys.argv[1]), "→", summary)
    if problems:
        print("PROBLEMS:"); [print("  -", x) for x in problems]; sys.exit(1)
    print("✅ structure OK")
