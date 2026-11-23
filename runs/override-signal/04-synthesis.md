# 4. Research synthesis (pm-1, Answer)

> **Claim types updated (23 Nov):** the data is now `data/claims_synthetic_v2.csv`, made from the provided file by [`notebooks/make_data.py`](notebooks/make_data.py). Every claim, decision, amount and note is unchanged; claim types are now Motor (including vans), Home, Commercial property, Travel, Pet and Gadget, each with an example such as "Burst pipe". Liability is no longer a claim type. Only the claim-type numbers below changed.

> **SYNTHETIC.** Fernway is a made-up name; the data is synthetic and the discovery call was a simulated conversation with a VP of Claims (23 Nov). Quotes are from its transcript. Every number comes from [`notebooks/answer.py`](notebooks/answer.py).

| # | Claim from the call (quote) | Verdict | What the data shows | Follow-up |
|---|---|---|---|---|
| C1 | "the AI is cautious when something's unclear, like an old condition in the history or a date that doesn't quite line up. It leans towards denying" | **Partly supported** | Of 14 overturned denials, 4 are about time windows or dates (30-day window, waiting period, loss date). 5 are cover the AI didn't see (an extension clause, an endorsement): not caution, missing information. 4 don't say | Does the AI see endorsements and extensions on the policy schedule? |
| C2 | "approvals often get waved through … the 2 in 10 on approvals may be undercounted" | **Data can't answer** | Agreed approvals look consistent (AI payout 85% to 100% of claimed), but an error nobody caught leaves no trace | Re-review a sample of agreed approvals |
| C3 | "overpayment is the bigger total cost, but a wrong denial is the one that loses us a client" | **Not supported in this sample** | The AI would have underpaid 21 times, £30,390 (14 valid claims denied, £27,611), and overpaid 21 times, £24,599. Denying a valid claim is the largest single kind, not the rarer one. C2 could flip this | Is leakage found later, in client audits, that this export doesn't show? |
| C4 | "In September, we onboarded a new MGA client, a pet insurer … My bet is the AI hadn't seen formats like that before" | **Not supported** | September misreads: 4 on property claims (Home and Commercial property), 2 Motor, 2 Travel, 0 Pet. Pet misreads total 2 in the period, both in October. 4 of September's 8 are a total read from the wrong page ("on page 2"). There is no client column | Check the document reader on multi-page quotes and receipts |
| C5 | "We added a required override reason … half of them write wrong or see notes" | **Partly supported** | 54 of 55 overrides have a reason, so it's required. But 10 (18%) don't say what went wrong, not half; 6 of the 10 are from August | |
| C6 | "Mostly on working out why it's wrong … rereading the documents" | **Data can't answer** | No time data | Time per override, from the platform's logs |
| C7 | "Once a handler gets burnt a couple of times on a claim type, they stop trusting the AI there and recheck everything" | **Data can't answer** | No time or recheck data | Time per claim by claim type, before and after a fix |
| C8 | "a dashboard of override rates by claim type. It tells me where the AI gets overridden, but not why" | **Supported** | Override rate by claim type sits between 17.0% and 20.0% for five types; Gadget is 25.0% on 12 claims. The causes differ: Home is 5 misreads and 4 policy mistakes; Pet is 5 of 10 not stated | |
| C9 | "If handlers keep fixing the same misread vet invoice every week, we're not dealing with it, we're just absorbing it" | **Supported** | 12 mistakes happen at least twice. Together they are 33 of the 45 overrides with a usable reason, £42,041; 9 of the 12 recur in 2 or more months | |

## Answer for the VP: do the September misreads cluster?
On claim type, yes, but not on pet: 4 of 8 are property claims and none are pet. The common thread is the document, not the client: 4 of 8 read a total from the wrong page of a multi-page quote or receipt. The data has no client column, so it can't say whether one client sends those documents.

## What the call adds that the data can't
- Overrides happen in the claims workspace, through an Override button, a decision and a required note. "It sits on the claim, but nobody reads it unless there's a complaint."
- What's been tried: the required reason; a monthly review of "a sample of maybe 20 claims" that's "the first thing to go when we're busy"; a by-type override-rate dashboard.
- Ranking of harm (the VP's): a wrongly denied valid claim first, overpayment second, handler time last ("the most frequent").
- To trust it: handlers want "the exact line in the vet notes it's relying on" and an "I'm not sure"; the VP wants a track record by claim type; insurers want "proof that when we found a problem, we fixed it and it didn't come back".
- Constraint: "Whatever you build has to work with that mess, not assume people will suddenly fill in perfect forms."
- Estimate (the VP's guess): each handler loses "30 to 45 minutes a day to rechecking and fixing the AI".
