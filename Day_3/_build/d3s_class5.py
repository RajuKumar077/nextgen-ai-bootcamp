# Class 5 slides · "Neo Reads the Policy Binder" (RAG) · light theme, teal -> blue
exec(open(os.path.expanduser("~/Desktop/Day_3/_build/d3s_core.py"), encoding="utf-8").read()) if "DAY3" not in globals() else None

BASE += """
.map{position:relative;height:430px;border-radius:30px;background:var(--card);border:1px solid var(--hair);box-shadow:inset 0 1px 0 var(--gloss),0 22px 50px var(--cardsh);overflow:hidden}
.map .zone{position:absolute;border-radius:50%;background:var(--acc-s);border:1.5px dashed var(--acc-line)}
.map .zl{position:absolute;font:700 14px @UI@;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.map .dot{position:absolute;width:16px;height:16px;border-radius:50%;background:var(--grad);box-shadow:0 4px 10px var(--orbsh)}
.map .dl{position:absolute;font:600 15px @UI@;color:var(--muted)}
.map .star{position:absolute;font-size:44px;line-height:1;color:#ff9f0a;filter:drop-shadow(0 4px 8px rgba(255,159,10,.5))}
.map .ql{position:absolute;font:700 17px @UI@;color:var(--text);background:var(--card);border:1px solid var(--hair);border-radius:12px;padding:6px 12px;box-shadow:0 8px 20px var(--cardsh)}
.fp{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 4px}
.fp span{font:600 17px @MONO@;background:var(--seg);border-radius:10px;padding:6px 10px;color:var(--text)}
.chunk{background:var(--card);border:1px solid var(--hair);border-radius:28px;box-shadow:inset 0 1px 0 var(--gloss),0 22px 50px var(--cardsh);overflow:hidden}
.chunk .ch{display:flex;gap:12px;align-items:center;padding:16px 26px;background:var(--seg);font:600 15px @UI@;color:var(--muted)}
.chunk .ch b{color:var(--accent);font-family:@MONO@}
.chunk .cb{padding:22px 28px;font-size:25px;line-height:1.5}
.chunk .cb .tg{color:var(--accent);font:600 18px @MONO@}
.ans{border-left:6px solid var(--ok);padding-left:22px}
""".replace("@UI@", UI).replace("@MONO@", MONO)

TERMS["Class 5"] = [
 ("Part 1", [("Key terms: why Neo can't answer", [
    ("Context window", "The most text the model can read at one time: your instructions, any documents, and its own answer, all together.", "The size of Neo's desk. A bigger pile does not fit.", "2"),
    ("Context stuffing", "Pasting a whole document into the prompt. Fine for one short document. It does not scale to hundreds.", "Photocopying the whole binder for every question.", "2"),
    ("Conversation history", "The earlier messages that the app sends again with every new message. The model itself remembers nothing.", "Re-reading the email thread before each reply.", "3")])]),
 ("Part 2", [("Key terms: the open-book exam (1 of 2)", [
    ("RAG", "Retrieval-Augmented Generation: find the right pages first, add them to the prompt, then let the AI write the answer.", "An open-book exam: find the page, then answer.", "8"),
    ("Chunk", "A small piece of a document, kept whole enough to make sense on its own. Here: one numbered clause.", "One clause of the policy, with its section number.", "4"),
    ("Embedding", "A list of numbers that captures what a text means. Similar meanings give similar numbers. It is not encryption.", "A meaning fingerprint for each clause.", "6")]),
  ("Key terms: the open-book exam (2 of 2)", [
    ("Semantic search", "Searching by meaning, not by matching words. It finds the right clause even when the question uses different words.", "\"Really big orders\" still finds the Director rule.", "7"),
    ("Vector store", "Where the chunks and their embeddings are saved so they can be searched. Here: a simple Python list.", "The index at the back of the binder.", "6"),
    ("Top-k retrieval", "Taking the k most similar chunks (here k = 3), not only the single best one.", "Pulling the three most likely pages.", "7"),
    ("Citation", "The source of each answer, such as [Procurement_Policy §3.3], so anyone can check it.", "A footnote an auditor can follow.", "8")])]),
 ("Part 3", [("Key terms: trusting the answer (1 of 2)", [
    ("Grounding", "Making the AI answer only from the sources you supplied, not from its general knowledge.", "\"Answer only from the binder.\"", "10"),
    ("Refusal", "Saying \"Not in the documents\" when the sources do not contain the answer. A correct answer, not a failure.", "\"I'll check and come back to you.\"", "10"),
    ("Retrieval test", "A fixed list of questions, each with the clause that must come back, checked by code every time you change something.", "A UAT script for the binder.", "11")]),
  ("Key terms: trusting the answer (2 of 2)", [
    ("Stale source", "An outdated document that is still stored. RAG will quote it confidently.", "The 2024 policy left in the shared folder.", "12"),
    ("Chunk size", "How big each piece is. Too big: vague citations and a long prompt. Too small: the meaning is cut in half.", "A whole chapter versus one clause.", "13")])]),
 ("Part 4", [("Key terms: where RAG fits", [
    ("Fine-tuning", "Retraining the model on your data. Costly, hard to update, and it cannot show its sources. Rarely needed for policies.", "Re-printing the whole binder for every change.", None),
    ("Local (private) RAG", "RAG that runs on your own laptop or server, so documents never leave your control.", "The binder never leaves the building.", "14")])]),
]
TAGS["Class 5"] = [("who approves a po above", "Vague prompt"), ("paste the whole policy", "Context stuffing"), ("memory is something", "Conversation history"),
  ("where does", "Conversation history"), ("closed book", "RAG"), ("rag in three words", "RAG"), ("the 4 steps", "RAG"), ("step 1", "Chunk"), ("what a chunk looks like", "Chunk"),
  ("keyword search", "Semantic search"), ("step 2", "Embedding"), ("meaning fingerprint", "Embedding"), ("a map of meaning", "Embedding"), ("step 3", "Top-k retrieval"),
  ("why the top 3", "Top-k retrieval"), ("step 4", "Citation"), ("reworded", "Semantic search"), ("rag or retraining", "Fine-tuning"), ("not in the documents", "Refusal"),
  ("a correct answer", "Refusal"), ("test five", "Retrieval test"), ("three kinds of test", "Retrieval test"), ("outdated", "Stale source"), ("chunk size", "Chunk size"),
  ("another document pack", "Local (private) RAG"), ("never upload", "Grounding"), ("chunker in action", "Chunk"), ("three document packs", "Chunk"), ("same idea, different words", "Semantic search"), ("store the fingerprints", "Embedding"), ("cell 7: find", "Top-k retrieval"), ("a cited answer", "Citation"), ("remember email d", "Grounding"), ("reading a", "Retrieval test"), ("the fix is not", "Stale source"), ("your scoreboard", "Retrieval test"), ("why we can't paste", "Context window"), ("with and without history", "Conversation history"), ("neo runs on", "Embedding")]
TAGS["Class 5"] = [(k, v) for k, v in TAGS["Class 5"] if v != "Vague prompt"] + [("who approves a po above", "Grounding")]
for _tc, _t in {"Part 1": "Neo doesn't know the binder", "Part 2": "The open-book exam", "Part 3": "Trust but verify", "Part 4": "Your turn"}.items(): PART_TITLES[("Class 5", _tc)] = _t

D = Deck("Class 5", "Neo", "Day 3 · Morning")
A = "Start"
D.add(A, """<div class="body"><div class="label" style="color:var(--accent)">Day 3 · Class 5 · Giving AI our knowledge</div>
<h1>Neo reads the<br><span class="mono">policy binder</span></h1>
<p class="lead" style="margin-top:0">Neo is smart, but has never seen <b>your</b> policies. Today we hand Neo the binder and teach it to <b>look up the right page</b> before it answers.</p>
<div><span class="pill">RAG, step by step</span><span class="pill">Citations</span><span class="pill">Testing</span><span class="pill">Runs on your laptop</span></div></div>""" + HINT,
 "Before class: open Day_3/Class_5_RAG/notebooks/Class_5_Neo_Policy_Binder.ipynb, choose the .venv kernel and run CELL S. Same story as Day 2: Neo covers your inbox. Today's theme is knowledge.", "title")
D.add(A, slide("Yesterday in 30 seconds", grid(3,
  card("Prompt = handover note", "Role · Task · Context · Format · Rules", "📝"),
  card("Fixed columns", "One row, same fields, checked by code", "📊"),
  card("Scam emails", "Mark outside text, standing rule, locks and people", "🛡️")),
  lead("Neo now follows a good note. <b>But the note can't contain the whole company.</b> Neo still doesn't know our policies.")),
 "Quick recap of Day 2, 30 seconds. Then the bridge: it follows our instructions, but it doesn't know our policies.")
D.add(A, slide("The situation", chat(
  '<div class="bub neo f"><div class="av" style="background:#ff9f0a">P</div><div class="tx"><b>Priya, Alpha Supplies:</b> We have a ₹12 lakh order coming. Whose approval do you need on your side before you confirm the PO?</div></div>',
  me("Neo, reply using our policy.")), lead("The answer is in the <b>policy binder</b>. Neo has never opened it.")),
 "Set the scene: you are on leave, Neo is covering the inbox, and a vendor asks something that only the binder answers.")
D.add(A, """<div class="hero"><div class="orb">Neo</div><div>
<div class="label" style="color:var(--accent)">Neo, today</div><h2 style="margin-bottom:18px">Smart. Fast. New.</h2>
<p class="f">⚡ Reads and writes in seconds</p><p class="f">📚 Knows business in general</p>
<p class="f">🙈 Has <b>never seen</b> your policies, limits or vendors</p><p class="f">📖 Today: we give Neo the <b>binder</b></p></div></div>""",
 "Neo is still the same character. What changes today is what Neo can read.")
D.add(A, """<div class="body center"><div class="big">Don't paste the whole binder.<br>Hand Neo <em>the right page</em>.</div>
<p class="lead f">That is RAG. By the end of the class you will build it, test it and know when to trust it.</p></div>""",
 "The one idea for the morning. Pause here.")
D.add(A, """<h2>Today's plan · 2 hours</h2><div class="body"><table class="agenda">
<tr><th>Time</th><th>Topic</th><th>Question</th><th>Cells</th></tr>
<tr><td class="t">0:00</td><td>Neo doesn't know the binder</td><td>Why can't a smart AI answer this?</td><td class="m">S, 1–3</td></tr>
<tr><td class="t">0:20</td><td>The open-book exam: RAG in 4 steps</td><td>How do we hand Neo the right page?</td><td class="m">4–9</td></tr>
<tr><td class="t">1:00</td><td>Trust but verify</td><td>When is the answer safe to use?</td><td class="m">10–13</td></tr>
<tr><td class="t">1:20</td><td>Your turn</td><td>Build and test your own</td><td class="m">14–15</td></tr></table></div>""",
 "Each part starts with a key-terms slide: say the names first, then run the demos.")
D.add(A, slide("Neo runs on this laptop", '<div class="g2" style="align-items:center">' + card("Two models, not one", "A <b>chat model</b> writes the answer. An <b>embedding model</b> turns text into meaning fingerprints. Both are in <span class=\"mono\">bootcamp_config.json</span>.", "💻") +
  '<div class="f">' + msg("s", "Ollama is running at localhost:11434") + '<div style="height:12px"></div>' + msg("s", "Main model · Small model · <b>Embed model</b> found") + '<div style="height:12px"></div>' + msg("s", "Neo replies <b>Connection OK</b>") + "</div></div>"),
 "Run CELL S. You should see three green ticks. If the embedding model is missing: ollama pull nomic-embed-text.", cell="S")

B1 = "1 · Neo and the binder"
D.divider("Part 1", "Neo doesn't know", "The binder", "Why can't a smart AI answer a simple policy question?", B1, divnote("Part 1 has three demos: no documents, paste the policy, and where chat memory really lives."))
D.add(B1, life_ai("<div class='emoji'>🧑‍💼</div><p>A new colleague on day one is asked <b>\"Who approves a PO above ₹10 lakh?\"</b></p><p>A careful one says <b>\"I'll check the policy.\"</b> A confident one guesses.</p>",
                  "<div class='emoji'>🤖</div><p>You ask Neo the same question.</p><p>Neo has <b>no binder</b>, so it fills the gap with the most likely words.</p>"), "Same problem in both worlds.")
D.add(B1, slide("\"Who approves a PO above ₹10 lakh?\"", qa("In our company, who approves a purchase order above ₹10 lakh?",
  "A confident, generic answer such as: <i>\"Usually a senior manager or the CFO, depending on company policy…\"</i>", "bad"), exp("Typical answer pattern · your model's wording will differ")),
 "Run CELL 1. Expect a generic, plausible answer. Ask: is that our policy?", cell=1)
D.add(B1, slide("Is that our policy?", grid(2, card("What Neo said", "\"A senior manager or the CFO\"<br>Sounds right. Source: none.", "🎭", "bad"),
  card("What our policy says", "<b>Director</b> approval above ₹10,00,000<br>Section 3.3 of the Procurement Policy.", "📖", "ok")), lead("A better prompt can't fix this. <b>Neo never saw the document.</b>")),
 "The point: this is not a prompting problem. The knowledge is missing.")
D.add(B1, slide("Option 1: paste the whole policy", '<div class="g2" style="align-items:start">' + pycode('''prompt = f"""Answer ONLY from the policy below.
If the answer is not in it, say "Not in the documents."

POLICY:
<<<
{policy}
>>>

Question: {QUESTION}"""''', (0, 1)) + "<div>" + qa("Who approves a PO above ₹10 lakh?", "<b>Director</b> approval is required (Section 3.3).", "good") + exp() + "</div></div>"),
 "Run CELL 2. With the policy inside the prompt, Neo answers correctly. This is context stuffing. It works for one short document.", cell=2)
D.add(B1, slide("Why we can't paste everything", grid(3,
  '<div class="card f" style="text-align:center"><div class="num">' + str(POLICY_WORDS) + '</div><h3>words</h3><p>One mock policy</p></div>',
  '<div class="card f" style="text-align:center"><div class="num">' + str(TOTAL_WORDS) + '</div><h3>words</h3><p>All 4 mock documents</p></div>',
  '<div class="card bad f" style="text-align:center"><div class="num">500+</div><h3>documents</h3><p>A real company</p></div>'),
  lead("They won't fit in the <b>context window</b>, and every question would re-read all of them. We need <b>only the right page</b>.")),
 "The first two numbers are counted from the actual files by the notebook (CELL 2 prints them).", cell=2)
D.add(B1, slide("Chat \"memory\": where does it live?", '<div class="flow">' +
  '<div class="st f"><h3>Message 1</h3><p>You: <i>My PO is 4500012345</i></p></div><div class="ar f">→</div>' +
  '<div class="st f"><h3>Message 2</h3><p>The app re-sends <b>message 1 + Neo\'s reply</b> + your new question</p></div><div class="ar f">→</div>' +
  '<div class="st f"><h3>Message 3</h3><p>The app re-sends <b>everything so far</b> + the new one</p></div></div>', lead("Every time, the <b>app</b> sends the whole conversation again. The model keeps nothing.")),
 "Run CELL 3. Case A sends only the new question: the model has no idea. Case B re-sends the history: it knows.", cell=3)
D.add(B1, slide("Same question, with and without history", grid(2,
  card("A · Only the new message", "\"What was my PO number?\"<br><b>Neo:</b> <i>\"I don't have that information.\"</i>", "🙈", "bad"),
  card("B · History re-sent", "Earlier messages included.<br><b>Neo:</b> <i>\"4500012345.\"</i>", "🧠", "ok")), exp()),
 "Target behaviour for CELL 3. Wording varies. The lesson is that memory is something the app does, not the model.", cell=3)
D.add(B1, """<div class="body center"><div class="big">Memory is something<br>the <em>app</em> does, not the model.</div>
<p class="lead f">RAG uses the same trick: the app <b>adds the right pages</b> to what it sends.</p></div>""", "Bridge from memory to RAG: both are about what the app puts in front of the model.")

B2 = "2 · The open-book exam"
D.divider("Part 2", "The open-book exam", "RAG in 4 steps", "Find the right page first. Then answer from it.", B2, divnote("Part 2 is the core: cut, store, find, answer."))
D.add(B2, life_ai("<div class='emoji'>📕</div><p><b>Closed-book exam.</b> Answer from memory. When unsure, you guess.</p><p>That is Neo on its own.</p>",
                  "<div class='emoji'>📖</div><p><b>Open-book exam.</b> Find the right page first, then answer from it.</p><p>That is <b>RAG</b>.</p>", "Closed book", "Open book"),
 "Use the school exam comparison. Ask the room which one they trust for a policy question.")
D.add(B2, slide("RAG in three words", grid(3, card("Retrieval", "Find the relevant pages", "🔎", "acc"), card("Augmented", "Add them to the prompt", "➕", "acc"), card("Generation", "Neo writes the answer from them", "✍️", "acc")),
  lead("Like a good consultant who <b>checks the blueprint</b> before answering, instead of answering from memory.")), "Plain meaning of each word, plus the SAP comparison.")
D.add(B2, slide("The 4 steps", '<div class="flow">' + "".join('<div class="st f"><h3>' + t + "</h3><p>" + p + '</p></div>' + ('<div class="ar f">→</div>' if i < 3 else "")
  for i, (t, p) in enumerate([("1 · CUT", "Split documents into small pieces (chunks)"), ("2 · STORE", "Save them by <b>meaning</b> (embeddings)"), ("3 · FIND", "Get the best pieces for the question"), ("4 · ANSWER", "Give pieces + question to Neo → cited answer")])) +
  "</div>", lead("Notebook cells: <span class=\"mono\">4</span> cut · <span class=\"mono\">6</span> store · <span class=\"mono\">7</span> find · <span class=\"mono\">8</span> answer.")),
 "Draw this on the board. We build each step in turn.")
D.add(B2, slide("Step 1 · Cut the documents into chunks", grid(3, card("Why cut?", "The whole binder won't fit, and a whole document is a vague thing to cite.", "✂️"),
  card("How we cut", "<b>One chunk per numbered clause</b>, so a clause is never split in half.", "📄"), card("What we add", "A <b>label</b>: the document, the section and the clause number.", "🏷️")),
  lead("The label is what makes a <b>citation</b> possible later.")), "Explain the idea before showing the code.")
D.add(B2, slide("Cell 4: the chunker in action", '<div class="g2" style="align-items:start">' + pycode('''chunks = [c for name in PACKS[DOC_PACK]
          for c in cut(f"{DOCS_DIR}/{name}")]

print(f"Pack {DOC_PACK}: {len(chunks)} chunks.")''', (0, 1)) +
  '<div class="out f"><div class="who">Notebook output · exact</div>Pack A: <b>' + str(len(CH["A"])) + "</b> chunks. The first three:<br>" +
  "".join("• <span class=\"mono\">" + esc(c["id"]) + "</span> → " + esc(c["text"][:62]) + "…<br>" for c in CH["A"][:3]) + "</div></div>", exp("exact")),
 "Run CELL 4. The numbers on this slide are computed from the same chunker and the same files you run, so they match your screen exactly.", cell=4)
D.add(B2, slide("What a chunk looks like", '<div class="chunk f"><div class="ch">id <b>' + esc(C33["id"]) + '</b></div><div class="cb"><span class="tg">[Procurement_Policy · 3. PO APPROVAL LIMITS]</span> 3.3 POs above ₹10,00,000 require Director approval.</div></div>' +
  lead("The <b>id</b> becomes the citation. The <b>label in brackets</b> keeps the context. The <b>clause</b> is the content. Only " + str(C33_WORDS) + " words, against " + str(POLICY_WORDS) + " for the whole policy."), ),
 "This is the Director rule from Section 3.3. Notice how small it is next to the whole document.", cell=4)
D.add(B2, slide("Three document packs", table(["Pack", "Documents", "Chunks"], [
  ["A · Procurement", "Procurement policy + SAP P2P process guide", "<b>" + str(len(CH["A"])) + "</b>"], ["B · Travel", "Travel policy", "<b>" + str(len(CH["B"])) + "</b>"], ["C · IDoc errors", "IDoc error handbook", "<b>" + str(len(CH["C"])) + "</b>"]]),
  lead("Change <span class=\"mono\">DOC_PACK</span> in the notebook to switch. All documents are <b>mock</b> (Nova Industries).")), exp("exact"), cell=4)
D.add(B2, life_ai("<div class='emoji'>🔍</div><p>Ctrl+F finds the <b>words</b> you typed.</p><p>If the policy says <i>\"Director approval\"</i> and you search <i>\"big orders\"</i>, you find nothing.</p>",
                  "<div class='emoji'>🧠</div><p>We want to find the <b>idea</b>, not the word.</p><p>That needs search by <b>meaning</b>.</p>", "In real life", "With Neo"), "Set up the keyword-search failure before showing it.")
D.add(B2, slide("Cell 5: keyword search, two questions", grid(2,
  '<div class="out f"><div class="who">❓ Who approves a PO above 10 lakh?</div>' + "<br>".join("<b>" + str(s) + "</b> matching words → <span class=\"mono\">" + esc(i) + "</span>" for s, i in KW1) + "</div>",
  '<div class="out bad f"><div class="who">❓ Who signs off on really big orders?</div>' + "<br>".join("<b>" + str(s) + "</b> matching word → <span class=\"mono\">" + esc(i) + "</span>" for s, i in KW2) +
  "<br><i>Section 3.3 is not even in the list.</i></div>"), exp("exact")), "Run CELL 5. Exact output, no AI. The reworded question picks the wrong clause because the words differ.", cell=5)
D.add(B2, slide("Same idea, different words", grid(2, card("The policy says", "\"POs <b>above ₹10,00,000</b> require <b>Director approval</b>.\"", "📖"),
  card("The question says", "\"Who <b>signs off</b> on <b>really big</b> orders?\"", "💬")), lead("Almost no shared words, but <b>the same meaning</b>. Keyword search fails. <b>Semantic search</b> does not.")), "Make the contrast explicit.", cell=5)
D.add(B2, slide("Step 2 · Store chunks by meaning", '<div class="g2" style="align-items:center"><div>' +
  '<div class="chunk f"><div class="ch">chunk <b>§3.3</b></div><div class="cb" style="font-size:21px">POs above ₹10,00,000 require Director approval.</div></div>' +
  '<p class="f" style="text-align:center;font-size:30px;margin:8px 0">↓ embedding model ↓</p>' +
  '<div class="card f"><h3>A meaning fingerprint</h3><p>A list of <b>hundreds of numbers</b> that captures what the text means.</p><div class="fp"><span>0.12</span><span>-0.41</span><span>0.07</span><span>0.88</span><span>…</span></div></div></div>' +
  '<div>' + card("Similar meaning → similar numbers", "\"Big purchase order approval\" and \"Director approves large orders\" end up close together.", "🧭", "acc") +
  '<div style="height:16px"></div>' + card("Not encryption", "An embedding is only a way to search. It is not a security feature.", "🔓", "warn") + "</div></div>"),
 "Illustration only: the digits shown are placeholders. In the notebook, CELL 6 prints the real length for your model.", cell=6)
D.add(B2, slide("A map of meaning", '<div class="map f">' +
  '<div class="zone" style="left:40px;top:28px;width:330px;height:190px"></div><div class="zl" style="left:78px;top:34px">Approvals</div>' +
  '<div class="dot" style="left:96px;top:90px"></div><div class="dl" style="left:118px;top:84px">§3.1</div><div class="dot" style="left:170px;top:130px"></div><div class="dl" style="left:192px;top:124px">§3.2</div><div class="dot" style="left:244px;top:92px"></div><div class="dl" style="left:266px;top:86px">§3.3</div>' +
  '<div class="zone" style="left:690px;top:30px;width:320px;height:190px"></div><div class="zl" style="left:738px;top:36px">Payment</div>' +
  '<div class="dot" style="left:760px;top:100px"></div><div class="dl" style="left:782px;top:94px">§4.1</div><div class="dot" style="left:850px;top:140px"></div><div class="dl" style="left:872px;top:134px">§4.3</div>' +
  '<div class="zone" style="left:60px;top:250px;width:320px;height:160px"></div><div class="zl" style="left:96px;top:300px">Vendors</div>' +
  '<div class="dot" style="left:130px;top:350px"></div><div class="dl" style="left:152px;top:344px">§5.2</div>' +
  '<div class="zone" style="left:680px;top:250px;width:330px;height:160px"></div><div class="zl" style="left:722px;top:300px">Disputes</div>' +
  '<div class="dot" style="left:780px;top:350px"></div><div class="dl" style="left:802px;top:344px">§6.2</div>' +
  '<div class="star" style="left:392px;top:84px">★</div><div class="ql" style="left:300px;top:150px">“Who signs off on really big orders?”</div></div>' +
  '<p class="expect warn f">Illustration of the idea · real fingerprints have hundreds of dimensions</p>'), "The star is the question. It lands next to the approval rules, even though no words match. Search = find the nearest dots.", cell=6)
D.add(B2, slide("Cell 6: store the fingerprints", '<div class="g2" style="align-items:start">' + pycode('''fingerprints = embed([c["text"] for c in chunks])
store = list(zip(chunks, fingerprints))

a, b, c_ = embed([
  "Who approves a big purchase order?",
  "Director approval is needed above ₹10 lakh",
  "Payment runs happen on Tuesday and Friday"])
print(cosine(a, b), cosine(a, c_))''', (0, 1)) +
  '<div class="out f"><div class="who">What you will see</div>Stored <b>' + str(len(CH["A"])) + '</b> chunks. Each fingerprint is a list of <b>N</b> numbers.<br><br>big PO question ↔ Director rule: <b>higher</b><br>big PO question ↔ Tuesday payment run: <b>lower</b></div></div>',
  exp("N depends on the embedding model · the first score should be clearly higher than the second")), "Run CELL 6. The chunk count is exact; N and the two scores depend on your model. The related pair must score higher than the unrelated pair.", cell=6)
D.add(B2, slide("Step 3 · Find the best chunks", '<div class="flow">' +
  '<div class="st f"><h3>Fingerprint the question</h3><p>Same embedding model</p></div><div class="ar f">→</div>' +
  '<div class="st f"><h3>Compare with every chunk</h3><p>Cosine similarity: 1.0 = same meaning</p></div><div class="ar f">→</div>' +
  '<div class="st f"><h3>Keep the top 3</h3><p>Highest scores first</p></div></div>', lead("That is the whole search engine. <b>No keywords involved.</b>")), "Explain cosine similarity as how closely two arrows point the same way. No maths needed.", cell=7)
D.add(B2, slide("Cell 7: find", '<div class="g2" style="align-items:start">' + pycode('''def find(question, top=3):
    q = embed(question)
    ranked = sorted(store,
        key=lambda s: cosine(q, s[1]),
        reverse=True)[:top]
    return ranked''', (1, 2)) +
  '<div class="out f"><div class="who">❓ Who signs off on really big orders?</div>Expected: <b>Procurement_Policy §3.3</b> appears in the top 3, with no shared keywords.<br><br><i>A small model may rank it 2nd or 3rd.</i></div></div>',
  exp("Target · your scores will differ")), "Run CELL 7. If §3.3 is not first, that is fine: it is in the top 3. Contrast with CELL 5.", cell=7)
D.add(B2, slide("Why the top 3, not just the top 1?", grid(3, card("Safety net", "The best match is not always rank 1 on a small model.", "🛟"), card("Context", "Neighbouring clauses often help the answer.", "🧩"),
  card("Cost", "Three small chunks are still tiny next to the whole binder.", "⚖️")), lead("Neo reads the three and decides which one answers the question.")), "Explain top-k. We use k = 3.", cell=7)
D.add(B2, slide("Step 4 · Build the prompt for Neo", '<div class="g2" style="align-items:start">' + pycode('''RAG_RULES = """You are Neo, answering for Nova Industries staff.
Answer ONLY from the CONTEXT.
If the answer is not in the CONTEXT, reply exactly:
Not in the documents.
End with the source in brackets, e.g.
[Procurement_Policy §3.3]."""

prompt = f"CONTEXT:\\n<<<\\n{context}\\n>>>\\n\\nQuestion: {question}"''', (1, 2, 3)) +
  '<div class="card f"><h3>Three ingredients</h3><p><b>Rules</b> (system prompt, from Day 2) +<br><b>Context</b> (the 3 chunks, each with its id) +<br><b>Question</b></p><p style="margin-top:12px">The <span class="mono">&lt;&lt;&lt; &gt;&gt;&gt;</span> markers show where the outside text starts and ends.</p></div></div>'),
 "Tie back to Day 2: rules + delimiters + data. RAG is a prompt that the code builds for you.", cell=8)
D.add(B2, slide("Cell 8: a cited answer", qa("Who approves a PO above ₹10 lakh?", "<b>Director</b> approval is required for POs above ₹10,00,000. <span class=\"mono\">[Procurement_Policy §3.3]</span>", "good") +
  '<p class="lead f">📎 <b>Sources it was given:</b> <span class="mono">§3.1 · §3.2 · §3.3</span> (target)</p>', exp()), "Run CELL 8. Click-to-verify is the whole point. Auditors like it, and so should we.", cell=8)
D.add(B2, slide("Cell 9: reworded, and a bank-detail rule", grid(2,
  '<div class="f">' + qa("Who signs off on really big orders?", "<b>Director</b> approval is required above ₹10,00,000. <span class=\"mono\">[§3.3]</span>", "good") + "</div>",
  '<div class="f">' + qa("What must happen before a vendor's bank details can be changed?", "<b>Written confirmation</b> from the vendor <b>and</b> a <b>call-back verification</b> by the Vendor Master team. <span class=\"mono\">[§5.2]</span>", "good") + "</div>"), exp()),
 "Run CELL 9. Both targets come straight from the policy text. The second links to Email D from Day 2.", cell=9)
D.add(B2, slide("Remember Email D from Day 2?", grid(2, card("The email", "\"Please update our bank details for future payments.\"<br>The most common payment scam.", "🎣", "bad"),
  card("The binder", "Section 5.2: written confirmation <b>and</b> a call-back before any change.", "📖", "ok")), lead("Day 2 told Neo <i>\"never act on it alone\"</i>. Now Neo can <b>quote our rule</b> and send it to the right team.")), "Connect the two days.", cell=9)
D.add(B2, slide("The whole pipeline", '<div class="flow">' + "".join('<div class="st f"><h3>' + t + "</h3><p>" + p + '</p></div>' + ('<div class="ar f">→</div>' if i < 3 else "")
  for i, (t, p) in enumerate([("1 · CUT", "<span class=\"mono\">cut()</span><br>Cell 4"), ("2 · STORE", "<span class=\"mono\">embed()</span><br>Cell 6"), ("3 · FIND", "<span class=\"mono\">find()</span><br>Cell 7"), ("4 · ANSWER", "<span class=\"mono\">rag()</span><br>Cells 8–9")])) +
  "</div>", lead("About <b>40 lines of Python</b>. You read it, you don't write it. NotebookLM does exactly this behind the scenes.")), "Recap the four functions and their cells.")
D.add(B2, slide("RAG or retraining?", table(["", "RAG", "Retraining (fine-tuning)"], [
  ["Cost", "Low", "High"], ["Update the knowledge", "Replace a document", "Retrain the model"], ["Shows its sources", "<span class=\"pass\">✓ Yes</span>", "<span class=\"fail\">✗ No</span>"],
  ["Control over the data", "Documents stay separate", "Knowledge is baked in"], ["Best for", "Policies, manuals, FAQs", "Style or behaviour"]]), lead("For company knowledge, <b>start with RAG</b>.")),
 "A fine-tuned model cannot say which page it learned something from. RAG can.")
D.add(B2, slide("What RAG is not for", grid(2, card("Good fit", "Policies · process guides · error handbooks · FAQs · specs", "📚", "ok"), card("Not the right tool", "<b>Live</b> data such as \"what is the status of PO 4500012345 right now?\"", "⚡", "warn")),
  lead("Documents don't change by the minute. <b>Live SAP data needs tools</b>, and that is this afternoon's class.")), "Plant the seed for Class 6.")

B3 = "3 · Trust but verify"
D.divider("Part 3", "Trust but verify", "When can we trust it?", "Refusing, testing, and outdated documents.", B3, divnote("Four demos: refusal, the test plan, outdated documents, chunk size."))
D.add(B3, slide("Cell 10: not in the documents", '<div class="pairs">' +
  '<div class="f"><div class="label">🔒 Strict rule</div>' + qa("What is the daily allowance for a trip to Singapore?", "<b>Not in the documents.</b>", "good") + "</div>" +
  '<div class="f"><div class="label">🔓 Weak rule</div>' + qa("What is the daily allowance for a trip to Singapore?", "A confident number from nowhere, for example <i>\"around SGD 100 per day\"</i>.", "bad") + "</div></div>" +
  "<p class=\"lead f\">Pack A has <b>no travel policy</b>. The only difference between the two answers is the <b>rule in the note</b>.</p>", exp("Target behaviour · a weak rule can still refuse, a strict one should always refuse")),
 "Run CELL 10. Run it a couple of times with the weak rule: small models often invent a number.", cell=10)
D.add(B3, slide("\"Not in the documents\" is a correct answer", grid(3, card("Honest", "No guess, no made-up number.", "🤝"), card("Safe", "Nobody acts on an invented allowance.", "🛡️"), card("Useful", "It tells you what to add to the library.", "🧭")),
  lead("Compare with Day 1, when Neo <b>bluffed</b> with full confidence.")), "Contrast with the hallucination demo from Day 1.", cell=10)
D.add(B3, slide("Cell 11: test five questions", table(["Type", "Question", "Clause that must come back"], [
  ["direct", "Who approves a PO above ₹10 lakh?", "Procurement_Policy §3.3"], ["direct", "What must happen before a vendor's bank details can be changed?", "Procurement_Policy §5.2"],
  ["direct", "Which transaction posts a goods receipt?", "SAP_P2P_Process_Guide §1.3"], ["reworded", "Who signs off on really big orders?", "Procurement_Policy §3.3"],
  ["missing", "What is the daily allowance for a trip to Singapore?", "— (must say \"Not in the documents\")"]], mono=(2,)), exp("exact")),
 "Run CELL 11. The questions and expected clauses are exactly those in the notebook. The CODE scores the retrieval, not your eyes.", cell=11)
D.add(B3, slide("Three kinds of test", grid(3, card("Direct", "The answer is clearly in the document.", "🎯", "acc"), card("Reworded", "Same meaning, different words. Proves semantic search.", "🔁", "acc"), card("Missing", "Not in the documents. Must be refused.", "🚫", "acc")),
  lead("Always test <b>all three</b>, and re-run them after every change.")), "This mirrors the normal / edge / bad testing from Day 2.", cell=11)
D.add(B3, slide("Reading a ❌", grid(2, card("Retrieval failed", "The right clause was <b>not in the top 3</b>. Fix: the chunking, the wording of the clause, or the embedding model.", "🔎", "warn"),
  card("Generation failed", "The clause <b>was</b> there, but Neo ignored or misread it. Fix: the rules, or a stronger model.", "✍️", "warn")), lead("Because the notebook prints the <b>retrieved ids</b>, you can tell which one it was.")),
 "Celebrate a wrong answer: it teaches where to look.", cell=11)
D.add(B3, slide("Cell 12: the outdated document", grid(2,
  '<div class="out ok f"><div class="who">Current policy · v4.2</div>Above ₹1,00,000 and up to ₹10,00,000 → <b>Department Head</b> (§3.2)</div>',
  '<div class="out bad f"><div class="who">Old policy · 2024</div>Above ₹5,00,000 → <b>Director</b></div>') +
  lead("Question: <i>\"Who approves a PO of ₹7,00,000?\"</i> With <b>both versions stored</b> the answer is a coin toss. With the current policy only: <b>" + policy(700000)[0] + "</b>."), exp("exact · limits from the two documents")),
 "Run CELL 12. The two rules come from the actual files. RAG quotes whatever you give it.", cell=12)
D.add(B3, slide("The fix is not a better prompt", grid(3, card("Remove old versions", "Keep one current copy.", "🗑️"), card("Tag every document", "Version, effective date, owner.", "🏷️"), card("Name an owner", "Someone reviews the library on a schedule.", "👤")),
  lead("<b>RAG is only as good as your documents.</b>")), "A governance point, not a technical one.", cell=12)
D.add(B3, slide("Cell 13: chunk size", grid(2,
  card("Big chunks · whole documents", "Can only cite <b>\"Procurement_Policy\"</b>. Carries up to <b>" + str(POLICY_WORDS) + " words</b> into the prompt.", "📚", "warn"),
  card("Small chunks · one clause each", "Cites the <b>exact clause</b>. Carries about <b>" + str(round(sum(len(c["text"].split()) for c in CH["A"]) / len(CH["A"]))) + " words</b> per chunk (average).", "📄", "ok")), lead("Too big: vague citations, long prompts. Too small: the meaning gets cut in half."), exp("Words counted from the mock documents; token counts print in the notebook")),
 "Run CELL 13. The notebook prints the prompt size in tokens for both set-ups.", cell=13)
D.add(B3, slide("What should we never upload?", '<div class="pairs"><div><div class="label">Upload</div><ul class="yes f"><li>Approved documents</li><li>Current versions</li><li>Non-sensitive content</li><li>Mock data in training</li></ul></div>' +
  '<div><div class="label">Never upload</div><ul class="no f"><li>Client or personal data</li><li>Credentials and keys</li><li>Contracts, financial results</li><li>Anything IT has not approved</li></ul></div></div>' +
  lead("For sensitive documents use a <b>private</b> RAG like this notebook, or an approved enterprise platform.")), "This is the never-upload list. Ask the room to add to it.")

B4 = "4 · Your turn"
D.divider("Part 4", "Your turn", "Build and test", "Change one pack. Write five questions. Score them.", B4, divnote("40 minutes. Cells 14 and 15."))
D.add(B4, slide("Four tasks · 40 min", '<div class="g2"><div>' +
  '<div class="do f"><div class="n">1</div><div><h3>Pick a pack</h3><p>B (Travel) or C (IDoc errors). Cell 14.</p></div></div>' +
  '<div class="do f"><div class="n">2</div><div><h3>Ask a question</h3><p>Check the answer and the citation.</p></div></div></div><div>' +
  '<div class="do f"><div class="n">3</div><div><h3>Write 5 test questions</h3><p>3 direct · 1 reworded · 1 missing. Cell 15.</p></div></div>' +
  '<div class="do f"><div class="n">4</div><div><h3>Score and explain</h3><p>Retrieval failed or generation failed?</p></div></div></div></div>'), "Teams of 3 or 4. Remind them to change only lines marked ← change me.", cell="14–15")
D.add(B4, slide("Cell 14: another document pack", '<div class="g2" style="align-items:start">' + pycode('''MY_PACK = "C"      # ← change me ("B" or "C")
my_chunks = [c for name in PACKS[MY_PACK]
             for c in cut(f"{DOCS_DIR}/{name}")]
my_store = list(zip(my_chunks,
    embed([c["text"] for c in my_chunks])))

MY_QUESTION = "What does IDoc status 51 mean?"   # ← change me''', (0, 6)) +
  '<div class="f">' + qa("What does IDoc status 51 mean?", "The IDoc reached SAP, but the application document was <b>not posted</b>. Typical causes: missing master data, a closed posting period, or a wrong plant. <span class=\"mono\">[IDoc_Error_Guide §1.1]</span>", "good") + "</div></div>", exp()),
 "Run CELL 14. The target answer is taken from IDoc_Error_Guide section 1.1.", cell=14)
D.add(B4, slide("Cell 15: your scoreboard", table(["#", "Type", "My question", "Clause that must return", "Retrieved?", "Answer OK?"],
  [["1", "direct", "", "", "", ""], ["2", "direct", "", "", "", ""], ["3", "direct", "", "", "", ""], ["4", "reworded", "", "", "", ""], ["5", "missing", "", "—", "", ""]]).replace("<td></td>", blank()),
  lead("Fast finishers: add a <b>contradicting</b> document and see how Neo copes.")), "Pass out the worksheet or have them copy it. They fill the blanks while the notebook scores.", cell=15)
D.add(B4, slide("Bonus · the same idea in NotebookLM", '<div class="g2" style="align-items:start"><div>' +
  '<div class="do f"><div class="n">1</div><div><h3>New notebook</h3><p>notebooklm.google.com</p></div></div><div class="do f"><div class="n">2</div><div><h3>Add sources</h3><p>The mock policy and process guide</p></div></div>' +
  '<div class="do f"><div class="n">3</div><div><h3>Ask, then click the citation</h3><p>It jumps to the source paragraph</p></div></div></div>' +
  card("Check before class", "NotebookLM is a <b>cloud</b> tool. Confirm it is allowed, use <b>mock documents only</b>, and have a backup recording.", "☁️", "warn") + "</div>"),
 "Optional, no code. Do this only if NotebookLM is approved and reachable. Otherwise the local notebook shows the same idea.")
D.add(B4, slide("Discussion", grid(3, card("Which documents first?", "Blueprints · specs · error handbooks · training manuals · release notes.", "📚"), card("What must stay out?", "Client data, personal data, credentials, unapproved material.", "🔒"),
  card("What if it is outdated?", "Neo will quote it with confidence. Who owns the library?", "⏳"))), "Two minutes per question.")
D.add(B4, slide("Common myths", table(["They might think…", "Better to say…"], [
  ["RAG removes hallucination", "It <b>reduces</b> it a lot. Always check the citation."], ["The AI learned our documents", "It <b>reads</b> them when asked. The model does not change."],
  ["Upload everything", "Only <b>approved, current, non-sensitive</b> documents."], ["Embeddings are encryption", "They are <b>meaning fingerprints</b> for search."]])), "Use as a quick correction list.")
D.add(B4, slide("RAG in one page", '<div class="g2"><div class="card f"><h3>The 4 steps</h3><p><b>1 Cut</b> into chunks<br><b>2 Store</b> as embeddings<br><b>3 Find</b> the top 3<br><b>4 Answer</b> with a citation</p></div>' +
  '<div class="card f"><h3>How to test</h3><p>✓ Direct question<br>✓ Reworded question<br>✓ Question not in the documents</p></div></div>' + lead("Golden rules: approved · current · non-sensitive documents. <b>Always check the citation.</b>")), "This is the participant handout.")

D.add("Wrap-up", """<h2>Quick quiz</h2><div class="body"><div class="quiz">
<div class="q f">Explain RAG in one sentence.<span class="a">Find the relevant pages of our documents, then let the AI answer from them.</span></div>
<div class="q f">What are the 4 steps?<span class="a">Cut · store · find · answer.</span></div>
<div class="q f">Why do we want a citation?<span class="a">So anyone can check the answer against its source.</span></div>
<div class="q f">Does the model remember our chat?<span class="a">No. The app re-sends the history each time.</span></div>
<div class="q f">RAG or retraining for a new travel policy?<span class="a">RAG: just replace the document.</span></div>
<div class="q f">What should Neo say when the answer is missing?<span class="a">"Not in the documents."</span></div></div></div>""", "Ask each question aloud before revealing the answer.")
D.add("Wrap-up", slide("Remember three things", grid(3, card("Open-book exam", "Find the right page first, then answer from it.", None, "acc", num="1"), card("Cite and refuse", "Citations make answers checkable. \"Not in the documents\" is a correct answer.", None, "acc", num="2"),
  card("Documents decide", "Current, approved, non-sensitive. RAG is only as good as the library.", None, "acc", num="3"))), "Three takeaways.")
D.add("Wrap-up", """<div class="body center"><div class="label" style="color:var(--accent)">After lunch · Class 6</div><div class="big">Neo can <em>answer</em>.<br>Can Neo <em>do</em>?</div>
<p class="lead">\"Why is PO 4500012345 delayed, and who should I contact?\" The answer isn't in any document. Neo must <b>check SAP, find the vendor and apply the policy</b>.</p></div>""", "Bridge to the afternoon.", "title")

finish(D, "Class_5_Neo_Policy_Binder_Slides.html", "Class 5 · Neo Reads the Policy Binder", LIGHT, "d3Class5Theme", DAY3 + "/Class_5_RAG/slides/")
