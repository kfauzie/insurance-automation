# 6. Design (pm-4)

> **SYNTHETIC.** Fernway is a made-up name; all data is synthetic. Numbers on the screens are placeholders taken from the data review; `pm-5` calculates them in code.

**Built as an upgrade, not a new system.** The team very likely already has a view of override rates by claim type. The design keeps that view and adds a **By mistake** tab next to it on the platform's existing Overrides page. The platform's navigation (Workspace, Claims, Overrides, Reports) is assumed.

| # | Screen | User | Status |
|---|---|---|---|
| 1 | [Overrides, By mistake](design/1-mistake-log.png) ([HTML](design/1-mistake-log.html)) | VP of Claims, with the engineering leads | Designed: for your review |
| 2 | Team lead review | Team lead | Specified; designed once screen 1 is agreed |
| 3 | Record a fix (pop-up on screen 1) | Engineering lead | Specified; designed once screen 1 is agreed |
| Hand-over | Handlers see "Fixed [date] · [n] repeats" next to the AI's recommendation in the claims workspace | Handler | A change to the existing workspace; later |

## Screen 1: Overrides, By mistake

**Job:** decide what the engineers fix next, and check each fix landed.

| Part | Shows | Acceptance criteria |
|---|---|---|
| Header | Team, user, job to be done; title "Overrides" with a "Synthetic data" tag; the date range and claim count | Short labelled lines, no paragraph |
| Tabs | "By claim type" (the existing view, unchanged) and "By mistake" (New) | The existing view is one click away |
| Three numbers | Overrides (count and % of claims); £ at stake if the AI had been followed, split into overpaid, underpaid and delayed; valid claims the AI denied (count and £) | Each label has a hover definition; the split adds up to the total |
| Notice | Overrides the AI couldn't name, with their £, and a button to send them to team lead review | Shown only when there are any; disappears once all are named |
| Rank by | £ at stake (Default), Valid claims denied first, Overrides | Changing it re-sorts the table and keeps the open row open |
| Table | One row per mistake: rank, name (with a one-line description when expanded), step (Policy check, Fraud check, Document reading, Documents requested), overrides, £ at stake, valid claims denied (red when above 0), the last 14 weeks as weekly bars, fix status | Rows add up to the three numbers; claim type is not a column (it doesn't separate the mistakes: 16.7% to 20.0%) |
| Fix status | Not started (grey); Fixed [date] · [n] repeats in [n] weeks (green); Fixed [date] · came back [n] times (red, with the repeats after the fix shown in red in the bars) | Repeats are counted only after the fix date |
| Expanded row | Every claim behind the mistake, one line each: claim, claim type and date, the AI's call and the handler's call with £, the handler's note as written (in quotes), and what it would have done ("Valid claim denied", "Paid too much", "Paid too little", "Delayed"). Beside it: the AI summary of why the AI got it wrong, marked "AI summary" and "Confirmed by a team lead" (or "Not confirmed yet"), first and last seen, claim types, and the main action, **Record a fix** | The handler's words and the AI's summary look different; one primary button |

**Example input:** the 300 synthetic claims; 55 overrides. **Expected output:** 55 overrides, £68,714 at stake; 14 valid claims denied, £27,611; top row "Missed cover on the policy schedule": 5 overrides, £14,502, 5 denied.

**Edge cases:**
- A mistake with one override: listed, but marked "Seen once" so a single claim doesn't look like a pattern.
- A mistake that came back after a fix: red status and bars; it rises in the ranking on repeats after the fix.
- No overrides in the range: "No overrides between [dates]" in place of the table.
- A team lead changes a mistake's name or merges two: the table updates and the expanded row says "Renamed by a team lead".

**Handoff:** Send to team lead review → screen 2. Record a fix → screen 3.

## Screen 2: Team lead review
- **Job:** confirm or correct how the AI named each override, starting with the ones it couldn't name.
- **Input:** overrides marked "Not sure" or "Not confirmed yet": the claim, the AI's and the handler's call, the note as written, and the claim documents.
- **Output:** each override confirmed against a mistake, moved to another, or given a new mistake name.
- **Happy path:** one override at a time: the AI's suggested mistake with its reason, beside the note and the document page it relied on. Confirm with one click, or pick another mistake. A progress count ("4 of 10 done") and a short confirmation after each.
- **Edge cases:** documents missing → "Ask the handler", which sends them a one-line question; the override stays open. Quitting midway → progress is kept.
- **Acceptance criteria:** about 15 minutes a week for a team lead (an estimate, to check in the MVP review); nothing reaches screen 1 as confirmed until a person confirms it.

## Screen 3: Record a fix (pop-up)
- **Job:** record that a fix shipped, so repeats are counted from that date.
- **Input:** the mistake; the fix date (default today), what changed (one line) and an optional link to the engineering ticket.
- **Output:** the status becomes "Fixed [date] · 0 repeats so far"; the bars mark the date.
- **Edge cases:** a fix date before the last override → warn: "[n] overrides after this date will count as repeats."
- **Acceptance criteria:** done in under a minute; can be edited or undone.

## Design notes
- **No Figma or design system:** neutral defaults from `context/design-system.md`. Grey for the page and navigation; indigo only on the main action; red for harm (valid claims denied, a mistake that came back); green for a fix holding; amber for what needs a person; violet for anything the AI wrote. Colour is never the only signal; each has words.
- **Patterns, from memory of public product pages, not fresh screenshots this time:**
  - Grouped errors ranked by impact, with weekly bars and a "resolved in release [x]" status that flips if the error comes back: error-tracking tools (Sentry, Datadog Error Tracking).
  - A queue where a person confirms or corrects an AI's label, one item at a time: AI evaluation tools (LangSmith annotation queues, Braintrust).
  - Detail in an expanded row rather than a new page: most B2B tables.
- **Proposed glossary terms** (to add to `context/glossary.md` once you OK them): Mistake, £ at stake, Valid claim denied, Delayed, Fixed, Came back, Needs a team lead.

## Review before you see it (what changed)
- Fixed the clipped "Valid claim denied" tags and the wrapping claim lines.
- Evened the number cards (the first ran to two lines).
- Took the indigo off the navigation, the tab and the "New" tag, so it marks only **Record a fix**.
