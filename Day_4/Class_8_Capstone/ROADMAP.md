# Roadmap · keep learning with the same free tools

You finished the course with five free tools: **Ollama**, **VS Code**, **NotebookLM**, **Antigravity** and **MCP**. Here is how to keep going. Always in this order.

## Step 1 · Prompts (week 1)
- Pick one repeated text job: summarise a supplier email, draft a reminder, classify tickets.
- Save your best prompt as **Role · Task · Context · Format · Rules**. Test it on five real examples (with data you are allowed to use).
- Tools: Ollama + VS Code. *Exit test: the same prompt gives a usable answer 5 times out of 5.*

## Step 2 · Knowledge (weeks 2-3)
- Pick **one** small, approved, current document set (a process guide, an error handbook). Remove old versions.
- Build a RAG on it (Class 5, or NotebookLM). Write a **test plan**: direct, reworded and missing questions.
- *Exit test: every answer cites its source, and "Not in the documents" is returned when it should be.*

## Step 3 · Tools (weeks 4-6)
- Pick **one** read-only data source (an export, a report). Write a small MCP server over it (copy `sap_orders_server.py`).
- Connect it to Antigravity or VS Code. Start with **read-only tools only**.
- *Exit test: the agent picks the right tool for ten different questions.*

## Step 4 · Guardrails and pilot (weeks 7-8)
- Add the four guardrails: **read-only first**, **allow-list**, **step limit**, **human approval**. Check answers in code (Class 8, CELL 7).
- Get IT and security approval. Agree an **owner** for the documents and the tools.
- Run a pilot on **one** process with a small group. Count the time saved and the mistakes caught.

## Rules of thumb
1. **Start simple.** Prompt, then knowledge, then an agent. Only when the problem needs it.
2. **A fixed rule is not an agent.** Use normal automation for rule-based work.
3. **Business rules live in code**, not in the prompt.
4. **A person approves any change.**
5. **Mock or approved data only** in cloud tools.

## Where to look
- Ollama models: https://ollama.com/library
- MCP: https://modelcontextprotocol.io
- This bundle: `Class_7_MCP_Guardrails/mcp_server/sap_orders_server.py` is a complete, small, readable example server.
