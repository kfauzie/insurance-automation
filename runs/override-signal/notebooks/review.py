"""pm-1 Initial review of data/claims_synthetic_v2.csv (SYNTHETIC). Run from runs/override-signal: python3 notebooks/review.py"""
import pandas as pd
pd.set_option("display.width", 200); pd.set_option("display.max_columns", 20)
d = pd.read_csv("data/claims_synthetic_v2.csv", parse_dates=["date_received"])
d["override_reason"] = d["override_reason"].fillna("").str.strip()

print("== Shape"); print(len(d), "claims;", d.date_received.min().date(), "to", d.date_received.max().date())
print(d.claim_id.is_unique, "unique ids"); print(d.claim_type.value_counts().to_string())
print(d.ai_recommendation.value_counts().to_string())

# What counts as an override: the handler's decision differs, or the payout differs
d["decision_changed"] = d.ai_recommendation != d.handler_final_decision
d["amount_changed"] = (~d.decision_changed) & (d.ai_payout_gbp != d.final_payout_gbp)
d["override"] = d.decision_changed | d.amount_changed
d["has_reason"] = d.override_reason != ""
print("\n== Overrides"); o = d[d.override]
print("overrides", len(o), f"({len(o)/len(d):.1%})", "| decision changed", d.decision_changed.sum(), "| amount only", d.amount_changed.sum())
print("reason but no override:", (d.has_reason & ~d.override).sum(), "| override with no reason:", (d.override & ~d.has_reason).sum())
print(o[~o.has_reason][["claim_id","claim_type","ai_recommendation","handler_final_decision","ai_payout_gbp","final_payout_gbp"]].to_string())

# Reasons too vague for an engineer to act on
VAGUE = {"wrong", "see notes", "per team lead", "disagree w ai", "changed after call"}
d["vague"] = d.override & d.override_reason.str.lower().isin(VAGUE)
print("vague reasons:", d.vague.sum(), d[d.vague].override_reason.str.lower().value_counts().to_dict())

# Group reasons into what went wrong (keyword rules, judgement; checked by listing every reason below)
def cause(r):
    r = r.lower()
    if r == "" or r in VAGUE: return "Not stated"
    if any(k in r for k in ["ocr", "read ", "misread", "vat", "estimate not", "line item", "pulled from quote"]): return "Read the document wrong"
    if any(k in r for k in ["flag", "pattern", "red flag"]): return "Fraud flag wrong"
    if any(k in r for k in ["missing photos", "second quote", "already sent", "email thread"]): return "Documents: asked or missed"
    return "Applied the policy wrong"
d["cause"] = ""
d.loc[d.override, "cause"] = d.loc[d.override, "override_reason"].map(cause)
o = d[d.override].copy()
print("\n== Every reason with its group"); print(o.groupby(["cause", o.override_reason.str.lower()]).size().to_string())

# £ at stake if the handler had followed the AI
def stake(r):
    if r.amount_changed: return r.ai_payout_gbp - r.final_payout_gbp          # + overpay, - underpay
    if r.ai_recommendation == "Approve" and r.handler_final_decision == "Deny": return r.ai_payout_gbp  # would have paid
    if r.handler_final_decision == "Approve": return -r.final_payout_gbp        # valid claim AI blocked or delayed
    return 0
o["stake"] = o.apply(stake, axis=1)
o["direction"] = o.stake.map(lambda s: "AI would overpay" if s > 0 else ("AI would underpay or block" if s < 0 else "no £"))
o["abs_stake"] = o.stake.abs()
print("\n== £ at stake by direction"); print(o.groupby("direction").agg(n=("claim_id","size"), gbp=("abs_stake","sum")).to_string())

print("\n== By cause: count vs £")
g = o.groupby("cause").agg(n=("claim_id","size"), gbp=("abs_stake","sum")).sort_values("gbp", ascending=False)
g["share_n"] = (g.n/g.n.sum()).round(3); g["share_gbp"] = (g.gbp/g.gbp.sum()).round(3); print(g.to_string())

print("\n== By claim type: override rate, £")
t = d.groupby("claim_type").agg(claims=("claim_id","size"), overrides=("override","sum"))
t["rate"] = (t.overrides/t.claims).round(3)
t = t.join(o.groupby("claim_type").abs_stake.sum().rename("gbp")).sort_values("rate", ascending=False); print(t.to_string())

print("\n== By AI recommendation: how often overridden")
a = d.groupby("ai_recommendation").agg(n=("claim_id","size"), overrides=("override","sum")); a["rate"]=(a.overrides/a.n).round(3); print(a.to_string())
print(pd.crosstab(o.ai_recommendation, o.handler_final_decision).to_string())

print("\n== Document reading: does the AI's amount sit over or under the final?")
r = o[o.cause=="Read the document wrong"]; print(r.direction.value_counts().to_string(), "| £", r.abs_stake.sum())

print("\n== Over time, by month")
d["month"] = d.date_received.dt.to_period("M")
m = d.groupby("month").agg(claims=("claim_id","size"), overrides=("override","sum")); m["rate"]=(m.overrides/m.claims).round(3)
m = m.join(d[d.override].groupby("month").cause.apply(lambda s: (s=="Read the document wrong").sum()).rename("doc_reading")); print(m.to_string())

print("\n== Quality checks")
print("final paid above claimed:", (d.final_payout_gbp > d.claimed_amount_gbp).sum(), d[d.final_payout_gbp > d.claimed_amount_gbp][["claim_id","claimed_amount_gbp","ai_payout_gbp","final_payout_gbp","override_reason"]].to_string())
print("AI payout above claimed:", (d.ai_payout_gbp > d.claimed_amount_gbp).sum())
q = o[o.override_reason.str.contains("but it's", case=False)][["claim_id","ai_payout_gbp","final_payout_gbp","override_reason"]]; print("reasons quoting a figure:\n", q.to_string())
print("approved, AI vs final equal:", ((d.ai_recommendation=="Approve")&(~d.override)).sum(), "| ratio AI payout/claimed on agreed approvals:",
      (d[(d.ai_recommendation=="Approve")&(~d.override)].ai_payout_gbp/d[(d.ai_recommendation=="Approve")&(~d.override)].claimed_amount_gbp).describe().round(3).to_dict())
print("non-approve with payout:", ((d.ai_recommendation!="Approve")&(d.ai_payout_gbp>0)).sum(), "| round claimed amounts (to £10):", (d.claimed_amount_gbp%10==0).mean())

print("\n== Extra checks for the findings")
print("distinct reasons as written:", o.override_reason.nunique(), "| after lower-casing:", o.override_reason.str.lower().nunique(), "| groups:", o.cause.nunique())
da = o[(o.ai_recommendation=="Deny") & (o.handler_final_decision=="Approve")]
print("AI Deny -> handler Approve:", len(da), "claims, £", da.final_payout_gbp.sum(), "| causes:", da.cause.value_counts().to_dict())
ad = o[(o.ai_recommendation=="Approve") & (o.handler_final_decision=="Deny")]
print("AI Approve -> handler Deny:", len(ad), "claims, £", ad.ai_payout_gbp.sum(), "| causes:", ad.cause.value_counts().to_dict())
pol = o[o.cause=="Applied the policy wrong"]; print("policy errors by AI rec:", pol.ai_recommendation.value_counts().to_dict(), "| by claim type:", pol.claim_type.value_counts().to_dict())
print("doc reading by claim type:", o[o.cause=="Read the document wrong"].claim_type.value_counts().to_dict())
print("cause by month:\n", pd.crosstab(o.date_received.dt.to_period("M"), o.cause).to_string())
ns = o[o.cause=="Not stated"]; print("not stated: n", len(ns), "£", ns.abs_stake.sum(), "| largest:", ns.nlargest(3,"abs_stake")[["claim_id","abs_stake","override_reason"]].values.tolist())
print("total £ at stake:", o.abs_stake.sum())
