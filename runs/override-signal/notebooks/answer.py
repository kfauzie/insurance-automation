"""pm-1 Answer: test the claims from the discovery call against data/claims_synthetic.csv (SYNTHETIC).
Reuses the override, cause and money-at-stake definitions from review.py. Run from runs/override-signal."""
import pandas as pd
d = pd.read_csv("data/claims_synthetic.csv", parse_dates=["date_received"])
d["override_reason"] = d["override_reason"].fillna("").str.strip()
d["decision_changed"] = d.ai_recommendation != d.handler_final_decision
d["amount_changed"] = (~d.decision_changed) & (d.ai_payout_gbp != d.final_payout_gbp)
d["override"] = d.decision_changed | d.amount_changed
VAGUE = {"wrong", "see notes", "per team lead", "disagree w ai", "changed after call"}
def cause(r):
    r = r.lower()
    if r == "" or r in VAGUE: return "Not stated"
    if any(k in r for k in ["ocr", "read ", "misread", "vat", "estimate not", "line item", "pulled from quote"]): return "Read the document wrong"
    if any(k in r for k in ["flag", "pattern", "red flag"]): return "Fraud flag wrong"
    if any(k in r for k in ["missing photos", "second quote", "already sent", "email thread"]): return "Documents: asked or missed"
    return "Applied the policy wrong"
o = d[d.override].copy()
o["cause"] = o.override_reason.map(cause)
o["month"] = o.date_received.dt.strftime("%Y-%m")

def kind(r):  # what the AI's mistake would have done to the claim
    if r.amount_changed: return "Paid too much" if r.ai_payout_gbp > r.final_payout_gbp else "Paid too little"
    if r.ai_recommendation == "Deny" and r.handler_final_decision == "Approve": return "Denied a valid claim"
    if r.ai_recommendation == "Approve" and r.handler_final_decision == "Deny": return "Paid a claim it should deny"
    return "Other decision change"
def gbp(r):
    if r.amount_changed: return abs(r.ai_payout_gbp - r.final_payout_gbp)
    if r.ai_recommendation == "Deny" and r.handler_final_decision == "Approve": return r.final_payout_gbp
    if r.ai_recommendation == "Approve" and r.handler_final_decision == "Deny": return r.ai_payout_gbp
    if r.handler_final_decision == "Approve": return r.final_payout_gbp
    return 0
o["kind"] = o.apply(kind, axis=1); o["gbp"] = o.apply(gbp, axis=1)

print("== C1 The AI leans to Deny when something's unclear (old condition, dates); many turn out fine")
dn = o[(o.ai_recommendation=="Deny") & (o.handler_final_decision=="Approve")]
print(len(dn), "overturned denials; reasons:"); print(dn.override_reason.str.lower().value_counts().to_string())
TIME = ["30 day", "waiting period", "dates mixed", "inception", "date"]
dated = dn.override_reason.str.lower().apply(lambda s: any(k in s for k in TIME))
CLAUSE = ["extension clause", "endorsement", "cover applies"]
clause = dn.override_reason.str.lower().apply(lambda s: any(k in s for k in CLAUSE))
print("about dates or time windows:", dated.sum(), "| about cover the AI missed (extension clause, endorsement):", clause.sum(), "| not stated:", (dn.cause=="Not stated").sum())
print("Deny rate overall:", round((d.ai_recommendation=="Deny").mean(),3), "| Deny overturned:", round(len(dn)/(d.ai_recommendation=="Deny").sum(),3))

print("\n== C3 Overpayment is the bigger total cost; wrong denials are rarer")
k = o.groupby("kind").agg(n=("claim_id","size"), gbp=("gbp","sum")).sort_values("gbp", ascending=False); print(k.to_string())
over = k.loc[["Paid too much","Paid a claim it should deny"]].sum(); under = k.loc[["Denied a valid claim","Paid too little"]].sum()
print("AI would overpay (too much + paid a claim to deny):", int(over.n), "£", int(over.gbp), "| AI would underpay (denied valid + too little):", int(under.n), "£", int(under.gbp))

print("\n== C4 September misreads: new pet client with vet invoices from many practices")
mr = o[o.cause=="Read the document wrong"]
print(pd.crosstab(mr.month, mr.claim_type).to_string())
print("September misreads:"); print(mr[mr.month=="2026-09"][["claim_id","claim_type","override_reason"]].to_string(index=False))
pet = d[d.claim_type=="Pet vet bills"]; print("pet claims by month:", pet.date_received.dt.strftime("%Y-%m").value_counts().sort_index().to_dict())
print("claims by month:", d.date_received.dt.strftime("%Y-%m").value_counts().sort_index().to_dict())

print("\n== C5 A required reason exists, but half say 'wrong' or 'see notes'")
print("overrides with any reason:", (o.override_reason!="").sum(), "of", len(o), "| not stated (blank or vague):", (o.cause=="Not stated").sum(),
      f"({(o.cause=='Not stated').mean():.0%})", "| 'wrong' or 'see notes' exactly:", o.override_reason.str.lower().isin(["wrong","see notes"]).sum())
print("not stated by month:", o[o.cause=="Not stated"].month.value_counts().sort_index().to_dict(), "| overrides by month:", o.month.value_counts().sort_index().to_dict())

print("\n== C8 An override-rate-by-claim-type view says where, not why")
t = d.groupby("claim_type").override.mean().round(3).sort_values(); print("override rate by type:", t.to_dict())
print(pd.crosstab(o.claim_type, o.cause).to_string())

print("\n== C9 The same mistake keeps coming back")
o["r"] = o.override_reason.str.lower().str.replace(r"£\d+", "£N", regex=True).str.replace(r"repair quote|receipt|invoice|police report", "DOC", regex=True)
rep = o[o.cause!="Not stated"].groupby("r").agg(times=("claim_id","size"), months=("month","nunique"), gbp=("gbp","sum")).query("times>=2").sort_values("times", ascending=False)
print(rep.to_string()); print("stated overrides that repeat an earlier mistake:", int(rep.times.sum()), "of", int((o.cause!="Not stated").sum()), "| in 2+ months:", int((rep.months>=2).sum()), "of", len(rep), "patterns | £", int(rep.gbp.sum()))
