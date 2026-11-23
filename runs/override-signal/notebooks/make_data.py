"""SYNTHETIC. Makes data/claims_synthetic_v2.csv from the provided data/claims_synthetic.csv.

Keeps every claim, date, AI recommendation, handler decision, amount and override note unchanged.
Only replaces claim_type with the claim types agreed for this run, and adds claim_example (what happened):
- Liability -> Commercial property (liability isn't a claim type here; these are the largest claims)
- Property damage -> Gadget if claimed <= £900, Commercial property if >= £4,000, otherwise Home
- Motor, Travel, Pet stay (Pet vet bills -> Pet)
Examples are picked by amount where it matters (windscreens and lost baggage are small) and otherwise by a stable hash of the claim id.
Run from runs/override-signal:  python3 notebooks/make_data.py
"""
import csv, zlib
EXAMPLES = {"Home": ["Burst pipe", "Storm damage", "Accidental damage"],
            "Commercial property": ["Warehouse fire", "Flood", "Break-in"],
            "Gadget": ["Cracked phone screen", "Water damage", "Stolen laptop"],
            "Motor": ["Car accident", "Van accident"],
            "Travel": ["Grounded flight", "Cancelled trip"]}
pick = lambda kind, cid: EXAMPLES[kind][zlib.crc32(cid.encode()) % len(EXAMPLES[kind])]
rows = list(csv.DictReader(open("data/claims_synthetic.csv")))
for r in rows:
    t, amt, cid = r["claim_type"], float(r["claimed_amount_gbp"]), r["claim_id"]
    if t == "Liability": t = "Commercial property"
    elif t == "Property damage": t = "Gadget" if amt <= 900 else ("Commercial property" if amt >= 4000 else "Home")
    elif t == "Pet vet bills": t = "Pet"
    if t == "Pet": ex = "Vet bills"
    elif t == "Motor": ex = "Windscreen" if amt < 800 else pick("Motor", cid)
    elif t == "Travel": ex = "Lost baggage" if amt < 500 else ("Medical abroad" if amt > 1500 else pick("Travel", cid))
    else: ex = pick(t, cid)
    r["claim_type"], r["claim_example"] = t, ex
cols = ["claim_id", "date_received", "claim_type", "claim_example"] + [c for c in rows[0] if c not in ("claim_id", "date_received", "claim_type", "claim_example")]
with open("data/claims_synthetic_v2.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), "claims ->", dict(Counter(r["claim_type"] for r in rows)))
