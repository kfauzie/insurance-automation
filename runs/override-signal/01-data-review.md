# 1. Data review (pm-1, Initial review)

> **SYNTHETIC DATA.** Fernway is a made-up name; every claim is invented. Every number below comes from [`notebooks/review.py`](notebooks/review.py) (run from this folder: `python3 notebooks/review.py`).

> **Claim types updated (23 Nov):** the data is now `data/claims_synthetic_v2.csv`, made from the provided file by [`notebooks/make_data.py`](notebooks/make_data.py). Every claim, decision, amount and note is unchanged; claim types are now Motor (including vans), Home, Commercial property, Travel, Pet and Gadget, each with an example such as "Burst pipe". Liability is no longer a claim type. Only the claim-type numbers below changed.

## 1. The data

| claim_id | date_received | claim_type | claimed_amount_gbp | ai_recommendation | ai_payout_gbp | handler_final_decision | final_payout_gbp | override_reason |
|---|---|---|---|---|---|---|---|---|
| CLM-1001 | 2026-08-13 | Liability | 15750 | Approve | 13428 | Approve | 13428 | |
| CLM-1002 | 2026-09-06 | Motor | 4010 | Flag for fraud review | 0 | Flag for fraud review | 0 | |
| CLM-1003 | 2026-11-01 | Property damage | 740 | Deny | 0 | Deny | 0 | |
| CLM-1004 | 2026-08-29 | Motor | 4350 | Approve | 4208 | Approve | 4208 | |
| CLM-1005 | 2026-09-18 | Pet vet bills | 2090 | Approve | 1954 | Approve | 1954 | |

- **In two lines:** 300 claims received 3 Aug to 11 Nov 2026, across 6 claim types (Motor 94, Home 61, Pet 56, Travel 40, Commercial property 37, Gadget 12). Each row has one AI recommendation (Approve, Deny, Request info or Flag for fraud review) and amount, the handler's final decision and amount, and a free-text reason when they differ.
- **How I counted an override:** the handler's decision differs from the AI's, or the decision is the same but the payout differs. That gives **55 overrides (18.3%)**: 35 changed decisions, 20 changed amounts only.
- **Money at stake:** what the claim would have cost if the handler had followed the AI: the payout difference for amount changes; the payout lost for a Deny the handler approved; the payout made for an Approve the handler denied. Overrides to Request info or a fraud review count as £0 (judgement: the money effect isn't known yet). Total: **£68,714**.
- **Quality check (doesn't change the findings):** every claimed amount is a round £10, which real data rarely is. 7 claims were paid more than claimed (e.g. CLM-1008: claimed £840, paid £1,193), all amount corrections. 4 reasons quote a figure that doesn't match the final payout (CLM-1109: the reason says £3,771, but £2,609 was paid; maybe after the excess). There is no step, model version or handler column, so the data can't show which AI step went wrong or when a fix shipped.

## 2. Findings

| # | Finding | Why it might matter (guess) |
|---|---|---|
| 1 | **Policy mistakes are a third of overrides but half the money.** The AI applying the policy wrong (missed endorsement, extension clause, exclusion, the wrong policy version, the 30-day window) is 17 of 55 overrides (31%) but £36,690 of £68,714 at stake (53%). Misread documents are more frequent (18 overrides, 33%) but carry £12,049 (18%) | Fixing whatever handlers mention most often would start with the cheaper problem |
| 2 | **When the AI says Deny, handlers overturn it 29% of the time** (14 of 48), against 16% for Approve (33 of 208). All 14 were approved: £27,611 that valid claimants would have lost. 10 of the 14 are policy mistakes | Wrongly denied valid claims mean complaints and regulator exposure for the insurer, a different cost from overpaying |
| 3 | **Misread-document overrides jump from 1 in August to 8 in September,** out of 20 and 12 overrides in those months; then 6 in October | Something may have changed in how documents are read (a model, the text reader, a new document type). Or August's misreads were written up as "see notes" and "wrong": 6 of August's 20 overrides don't say what went wrong |
| 4 | **The reasons can't be counted without reading them one by one:** 39 different wordings for 5 kinds of mistake, and 10 of 55 overrides (18%), £11,281, don't say what went wrong ("disagree w AI", "per team lead", "see notes", "changed after call", one blank) | Engineers learn what handlers happen to write, not where the AI goes wrong most |

How I grouped the reasons (judgement, keyword rules in the script, every reason listed in its output):

| What went wrong | Overrides | £ at stake |
|---|---|---|
| Applied the policy wrong | 17 | £36,690 |
| Read the document wrong (OCR, totals on page 2, dates, VAT twice, estimate not invoice) | 18 | £12,049 |
| Not stated | 10 | £11,281 |
| Fraud flag wrong (4 false flags, 1 missed) | 5 | £7,425 |
| Documents: asked again, or missed the gap | 5 | £1,269 |

## 3. Questions for handlers and their lead
1. The data shows policy mistakes are a third of overrides but half the money at stake. Walk me through the last time the AI got the policy wrong on one of your claims. *How did you spot it?*
2. When the AI says Deny, handlers overturn it about 3 times in 10. What happens if a wrong Deny isn't caught? *How do you handle a Deny you're not sure about?*
3. Overrides for misread documents go from 1 in August to 8 in September. What changed around then?
4. Tell me about the last override you made. What did you write in the reason, and who reads it? *What happens to it after that?*

## 4. Clarifications to confirm
- Is there one AI recommendation per claim, or one per step (coverage, fraud, payout) that this export rolls up?
- Is the claimed amount the first figure the customer gave, or the latest? Does the payout include the excess?
- Is Request info a final decision here, or a pause before one?
- When were AI changes shipped in this period, and to which part (document reading, policy rules, fraud)?
- Is the reason required when a handler changes the AI's call? Only 1 of 55 is blank.

## 5. Looked at, nothing to ask about
- **Claim type doesn't separate the mistakes.** The override rate sits between 17.0% and 20.0% for five of the six types (Travel 20.0%, Commercial property 18.9%, Home 18.0%, Pet 17.9%, Motor 17.0%); Gadget is 25.0%, but on only 12 claims (3 overrides). What went wrong separates them; the claim type doesn't. Commercial property carries the most money (£21,466), because its claims are bigger.
- **Overall rate over time:** 20.4% in August, 14.3% in September, 19.5% in October, 19.4% in November (31 claims so far). With 80 to 100 claims a month, a move of a few points can't be told apart from chance.
- **Agreed approvals:** the AI's payout is 85% to 100% of the claimed amount (median 93%), so deductions look consistent when handlers agree.

## 6. Follow-ups you can ask Claude Code
- Do misread totals cluster in multi-page documents ("on page 2")?
- Overpay against underpay by claim type, and by month.
- Before and after a fix, once the ship dates are known.
