# Antigravity demo tasks (Class 7)

Two live demos, about 10 minutes each: **(1) Antigravity + MCP** and **(2) the guardrail: approval before a change**.

## Before class (once)

1. From the `Day_4` folder run: `python setup/make_mcp_config.py` (use the `.venv` Python). It writes `.vscode/mcp.json` for VS Code and
   `Class_7_MCP_Guardrails/antigravity/mcp_config.json` for Antigravity, both with the absolute path for **this** laptop, and test-starts each server.
2. **VS Code:** open the `Day_4` folder. The servers appear in the MCP / Tools list of the chat view. Start them there.
3. **Antigravity:** open the MCP settings (Agent panel → MCP servers → manage → raw config) and paste the contents of `antigravity/mcp_config.json`. Restart the agent.
4. Run both demos once. **Use the names you actually see** on screen: Antigravity and VS Code change their menus often. Keep a backup recording.

The two servers are the **same Python file** (`mcp_server/sap_orders_server.py`) started with different flags:

| Server name | Flags | What it can do |
|---|---|---|
| `nova-sap-orders` | none | **Read-only.** 5 read tools. `create_ticket` is refused. |
| `nova-sap-orders-write` | `--allow-write --with-scorecard` | Adds `vendor_scorecard`; `create_ticket` really writes to `mcp_server/tickets.jsonl`. |

## Demo 1 · Antigravity + MCP

Enable **only** `nova-sap-orders`. Paste this into the agent:

```
Use the nova-sap-orders MCP tools to answer: Which orders for Plant 1000 are blocked and why?
Show a table with PO number, vendor, value in INR and block reason. Use only facts from the tools.
```

| What you see | Say |
|---|---|
| The agent lists the available tools | **DISCOVERY.** It asked the server what it offers. |
| It calls `list_orders` with `plant: "1000"` and `status: "Blocked"` | **ACT.** It chose the tool and the arguments itself. |
| The result appears | **OBSERVE.** The facts come from the server, not from the model. |
| It writes the table | **FINISH.** Compare with `expected_blocked_plant_1000.md`. |

Then try the MCP **prompt**: in VS Code, type `/` and pick `blocked_orders_report` (plant: `1000`). That is the "ready-made prompt" the server offers.

## Demo 2 · Guardrail: approval before a change

Enable `nova-sap-orders-write`. In Antigravity's settings choose the mode that **asks before running commands or tools**. Paste:

```
Create a follow-up ticket for PO 4500012345 about the credit check, using the nova-sap-orders-write tools.
```

Expected: the agent **pauses** and shows the `create_ticket` call with its arguments. **Do not click yet.** Say: *"That pause is the guardrail. Nothing has changed."*
Click **approve** once, then show `mcp_server/tickets.jsonl`. Run it again and **decline**; the file does not grow.

Contrast: with only `nova-sap-orders` enabled, the same request is refused by the server (`This server is READ-ONLY`). Two layers: the **server** can refuse, and the **client** can ask.

## Hands-on questions

See `expected_answers.md`. Teams note, for each question, **which tool** the agent chose and **whether it needed approval**.

> Antigravity and VS Code send your prompts to a cloud model. Get IT/security approval first. The data here is **mock only**.
