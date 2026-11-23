# Run: override signal

> **SYNTHETIC.** Fernway is a made-up name; all data in this run is synthetic.

**The ask, word for word:**
> Claims handlers make the final call on every claim, and they often override or correct the AI's recommendation. Those overrides are the best signal of where the AI is wrong, but today they aren't captured consistently. Nobody can easily see which claim types or which steps go wrong most, how much each error costs, or whether a fix actually worked. So engineers end up debugging case by case, from whatever handlers happen to report

**Base product:** extends Fernway's existing internal claims platform and its AI automations; not a new claims system.
**Data:** to be provided (synthetic), in `data/`.

| Step | Skill | Output |
|---|---|---|
| 1. Data review | `pm-1-data-discovery` (Initial review) | Waiting for data |
| 2. Discovery guide | `pm-2-discovery-interview` | |
| 3. Discovery notes | the PM | |
| 4. Research synthesis | `pm-1-data-discovery` (Answer) | |
| 5. Spec: solution concept | `pm-3-problem-to-solution-concept` | |
| 6. Design | `pm-4-solution-design` | |
| 7. Prototype | `pm-5-mvp-build` | |
| 8. MVP review | `pm-6-mvp-review` | |

## Decisions I made (and what I turned down)
| Decision | Why | What I turned down |
|---|---|---|
