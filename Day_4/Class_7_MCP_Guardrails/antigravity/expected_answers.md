# Answer key · the five hands-on questions (Class 7, CELL 11)

| # | Question | Tools we expect | Approval? | The answer has |
|---|---|---|---|---|
| 1 | Which orders for Plant 1000 are blocked and why? | `list_orders` | no | 4 orders (see `expected_blocked_plant_1000.md`) |
| 2 | Who is the vendor contact for PO 4500012346? | `get_order` → `get_vendor` | no | Rahul Verma, rahul@bharat.example (Bharat Logistics) |
| 3 | Who must approve PO 4500012348? | `get_order` → `check_approval` | no | Director (₹12,00,000, policy 3.3) |
| 4 | Which vendor has the most delayed order value? | `delayed_summary` | no | Chennai Components, ₹15,00,000 |
| 5 | Create a ticket for PO 4500012345 about the credit check. | `create_ticket` | **YES** | a ticket id such as `TCK-0001` |

## Delayed orders by vendor (question 4)

| Vendor | Delayed POs | Total value (INR) |
|---|---|---|
| Bharat Logistics | 2 | ₹12,00,000 |
| Chennai Components | 2 | ₹15,00,000 |

## With the scorecard tool (CELL 7)

Question: *Which vendor has the highest total order value?* → **Chennai Components**, ₹27,00,000, 2 delayed and 1 blocked.

_A different tool order is a discussion point, not an error. Tool results are exact; the agent's wording will differ._
