# Run: override signal

> **SYNTHETIC.** Fernway is a made-up name; all data in this run is synthetic.

**The ask, word for word:**
> Claims handlers make the final call on every claim, and they often override or correct the AI's recommendation. Those overrides are the best signal of where the AI is wrong, but today they aren't captured consistently. Nobody can easily see which claim types or which steps go wrong most, how much each error costs, or whether a fix actually worked. So engineers end up debugging case by case, from whatever handlers happen to report

**Base product:** extends Fernway's existing internal claims platform and its AI automations; not a new claims system.
**Data:** `data/claims_synthetic.csv` (synthetic, provided): 300 claims, 3 Aug to 11 Nov 2026; one AI recommendation and the handler's final call per claim.

| Step | Skill | Output |
|---|---|---|
| 1. Data review | `pm-1-data-discovery` (Initial review) | [01-data-review.md](01-data-review.md) |
| 2. Discovery guide | `pm-2-discovery-interview` | Notion (private draft): [discovery questions](https://app.notion.com/p/4218f31ef05f81d6a8f1f4901db4057f) |
| 3. Discovery notes | the PM | |
| 4. Research synthesis | `pm-1-data-discovery` (Answer) | |
| 5. Spec: solution concept | `pm-3-problem-to-solution-concept` | |
| 6. Design | `pm-4-solution-design` | |
| 7. Prototype | `pm-5-mvp-build` | |
| 8. MVP review | `pm-6-mvp-review` | |

## Decisions I made (and what I turned down)
| Decision | Why | What I turned down |
|---|---|---|
| Count an override when the decision or the payout differs, and size it by the £ the claim would have cost if the handler had followed the AI | The ask is about errors and their cost; a changed payout with the same decision is still an AI error | Counting only changed decisions (would miss 20 of 55) |
| Group the free-text reasons into 5 kinds of mistake with keyword rules, every reason listed in the script output | 39 wordings can't be compared; the rules are visible and easy to change | Using an LLM to group them at this stage (300 rows; rules are enough and testable) |
| Overrides to Request info or fraud review count as £0 | The money effect isn't known until the claim settles | Counting the AI's payout as at stake |
