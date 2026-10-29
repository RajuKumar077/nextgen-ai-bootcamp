# Antigravity demo task (Class 6)

**Open this folder in Antigravity:** `Class_6_Agents/data` (it contains `orders.csv` and `vendors.csv`).

## Paste this task into the agent

```
Read orders.csv. Find all purchase orders with status "Delayed".
Create a summary report grouped by vendor showing the number of delayed POs
and their total value in INR. Save it as delayed_report.md and explain your steps.
```

## Narrate it with the agent loop

| What you see in Antigravity | Say |
|---|---|
| A plan or task list appears | **THINK.** It is planning before acting. |
| It opens or reads `orders.csv` | **ACT.** It uses a tool: reading a file. |
| It runs a script or command | **ACT** again. It may write a small script itself. |
| It checks the output | **OBSERVE.** It checks its own result. |
| It writes `delayed_report.md` | **FINISH.** Goal achieved. |

If Antigravity asks for approval before running a command, point it out: *"See, it asks before running anything. That is a guardrail, and it is tomorrow's topic."*

## Check the result

Compare `delayed_report.md` with `expected_delayed_report.md` in this folder.
Both vendors must appear with the right counts and totals.

## More tasks for the hands-on

- "Create a table of orders by plant with the count and total value."
- "List all blocked orders with their block reason."
- "Which vendor has the highest total order value?"

> Antigravity changes quickly. Run this task once before class and use the **names you actually see** for its views, plans and task lists.
> Use **mock data only**. Antigravity sends data to a cloud model, so get IT/security approval first.
