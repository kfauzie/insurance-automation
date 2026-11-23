"""Numbers quoted in the solution concept (SYNTHETIC data). Run from runs/override-signal."""
import pandas as pd, runpy, io, contextlib
with contextlib.redirect_stdout(io.StringIO()): ns = runpy.run_path("notebooks/answer.py")
o = ns["o"]; r = o.override_reason.str.lower()
def show(name, m): print(f"{name}: {int(m.sum())} overrides, £{int(o[m].gbp.sum())}, claims {o[m].claim_id.tolist()}")
show("Missed cover in the schedule (extension clause, endorsement)", r.str.contains("extension clause|endorsement"))
show("Time window or date read wrong on a denial", (o.ai_recommendation=="Deny") & r.str.contains("30 day|waiting period|dates mixed"))
show("Total read from the wrong page", r.str.contains("on page 2"))
show("Wrong policy version", r.str.contains("policy version"))
show("Not stated", o.cause=="Not stated")
print("usable reason today (not 'Not stated'):", int((o.cause!="Not stated").sum()), "of", len(o))
for c in ["CLM-1018","CLM-1109","CLM-1052","CLM-1298","CLM-1086"]:
    x = o[o.claim_id==c].iloc[0]; print(c, x.claim_type, x.ai_recommendation, x.ai_payout_gbp, "->", x.handler_final_decision, x.final_payout_gbp, "|", x.kind, "£", int(x.gbp), "|", x.override_reason)
