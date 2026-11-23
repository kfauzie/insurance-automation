# Run: override signal

> **SYNTHETIC.** Fernway is a made-up name; all data in this run is synthetic.

**The ask, word for word:**
> Claims handlers make the final call on every claim, and they often override or correct the AI's recommendation. Those overrides are the best signal of where the AI is wrong, but today they aren't captured consistently. Nobody can easily see which claim types or which steps go wrong most, how much each error costs, or whether a fix actually worked. So engineers end up debugging case by case, from whatever handlers happen to report

**Base product:** extends Fernway's existing internal claims platform and its AI automations; not a new claims system.
- Known from the call: handlers see the AI's recommendation in the claims workspace and use an Override button, pick a decision and type a required note. Engineers built a dashboard of override rates by claim type.
- Assumed: the platform logs the AI's recommendation and amount, the handler's decision and amount, and the note, for every claim (as in the export). It does not yet log which AI step or version made the call.
**Data:** `data/claims_synthetic.csv` (synthetic, provided): 300 claims, 3 Aug to 11 Nov 2026; one AI recommendation and the handler's final call per claim.

| Step | Skill | Output |
|---|---|---|
| 1. Data review | `pm-1-data-discovery` (Initial review) | [01-data-review.md](01-data-review.md) |
| 2. Discovery guide | `pm-2-discovery-interview` | Notion (private draft): [discovery questions](https://app.notion.com/p/4218f31ef05f81d6a8f1f4901db4057f) |
| 3. Discovery notes | the PM | Simulated call with a VP of Claims, transcript in the Notion page |
| 4. Research synthesis | `pm-1-data-discovery` (Answer) | [04-synthesis.md](04-synthesis.md) |
| 5. Spec: solution concept | `pm-3-problem-to-solution-concept` | Notion (private draft): [solution concept](https://app.notion.com/p/4218f31ef05f81f2bcf2f740895edcbf) |
| 6. Design | `pm-4-solution-design` | [06-screen-specs.md](06-screen-specs.md), [design/](design/) (screen 1 designed) |
| 7. Prototype | `pm-5-mvp-build` | |
| 8. MVP review | `pm-6-mvp-review` | |

## Decisions I made (and what I turned down)
| Decision | Why | What I turned down |
|---|---|---|
| Count an override when the decision or the payout differs, and size it by the £ the claim would have cost if the handler had followed the AI | The ask is about errors and their cost; a changed payout with the same decision is still an AI error | Counting only changed decisions (would miss 20 of 55) |
| Group the free-text reasons into 5 kinds of mistake with keyword rules, every reason listed in the script output | 39 wordings can't be compared; the rules are visible and easy to change | Using an LLM to group them at this stage (300 rows; rules are enough and testable) |
| Overrides to Request info or fraud review count as £0 | The money effect isn't known until the claim settles | Counting the AI's payout as at stake |
| Recommend a Mistake log that reads existing override notes, not a structured reason form | 45 of 55 overrides already say what went wrong; the VP: "has to work with that mess, not assume people will suddenly fill in perfect forms" | A structured reason at override (later, once the kinds of mistake are known); a weekly manual review (the monthly one lapsed) |
| Rank mistakes by kind, not by claim type | Override rate by claim type is flat (16.7% to 20.0%) | The existing claim-type view |
| Rank by £ at stake, and show how many were valid claims denied | Simple and checkable; whether denials should count extra is left to the MVP review | A weighted score nobody can check by hand |
| Add a "By mistake" tab to the existing Overrides page, keep "By claim type" | Feedback: the team very likely already tracks override rates; this upgrades it with the why, the £ and fix tracking | A new standalone tool |
| Fix status that flips to "came back" when a fixed mistake repeats | The VP's test of success is "the same mistake stopped coming back" (hypothesis); error trackers use the same pattern | A one-off "resolved" checkbox |
