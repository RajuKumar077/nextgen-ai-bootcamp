# Capstone guide · the SAP Operations Assistant (Class 8)

**Goal:** one assistant that answers a multi-step SAP question using **a prompt, knowledge (RAG), an agent and MCP tools**, with a checked answer and guardrails.
Teams of 3 or 4 · 40 minutes to build and test · then a 5-minute pitch each.

## The four parts

| Part | Tool | What teams do | Notebook alternative (no cloud) |
|---|---|---|---|
| Brain | Ollama | Use the local model | CELL S |
| Knowledge | NotebookLM | Load the team's policy and process documents | CELL 3 (`data/docs/`) |
| Prompts | Ollama / VS Code | Write the assistant's role, rules and output format | CELL 5 (`ROLE`, `RULES`, `FORMAT`) |
| Agent + tools | Antigravity + MCP | Answer multi-step questions on the mock SAP data | CELLs 4 and 6 |

NotebookLM and Antigravity are **cloud** tools: get approval, use **mock documents only**. The notebook does the same thing locally.

## Five use cases to choose from

| Use case | A question to start with | What it needs | Sources |
|---|---|---|---|
| Invoice exception | PO 4500012348: price variance | Orders + approver + policy + vendor | MCP + RAG |
| PO delay analysis | Delayed orders on plant 2000 | Orders + vendor contact | MCP |
| IDoc error triage | IDoc stuck at status 51 | IDoc handbook (§1.1, §2.3) | RAG |
| Vendor query | Contact for PO 4500012346 | Order + vendor | MCP |
| Month-end close | Blocked orders + 3-way match | Orders + policy (§4.1) | MCP + RAG |

## Steps

1. Pick **one** process (CELL 10: `MY_USE_CASE`) or write your own question.
2. Run the agent. Look at the tools it chose and the facts it observed.
3. Change one rule or the format (CELL 5, `# ← change me`) and run again. What changed?
4. Test it (CELL 11): direct, reworded and missing questions, scored by code.
5. Fill in the pitch card (CELL 12). It prints from what you built.

## Capstone check (Antigravity + MCP, optional)

Enable `nova-sap-orders` and ask:

```
PO 4500012348 is blocked. Why, who must approve it, and who is the vendor contact?
Use only facts from the tools.
```

Expected facts: blocked for **price variance**, value **₹12,00,000**, approver **Director** (policy 3.3), contact **Lakshmi Iyer** (lakshmi@chennai.example).
The policy clause on price variance is **Procurement_Policy §6.2**: *6.2 A price variance above 1% between the PO and the invoice blocks the invoice for review.* (this part needs the documents, so it comes from NotebookLM or CELL 3).

## Team presentation (5 minutes)

1. **One SAP process.** What is the question and who asks it?
2. **The prompt used.** Role, rules, format.
3. **A live demo.** Which tools did it call? Was the answer checked?
4. **The guardrails you would require** before this touches real data.

## Judging: one question

*Would I trust this answer?* Listen for: sources named, a step limit, read-only by default, a person approving changes, and mock data in cloud tools.
