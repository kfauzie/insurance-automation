"""Inline data/claims_synthetic_v2.csv into build/mvp.html between the csv script tags. Run from runs/override-signal: python3 build/make_mvp.py"""
import re
csv = open("data/claims_synthetic_v2.csv").read().strip()
p = "build/mvp.html"; s = open(p).read()
s = re.sub(r'(<script type="text/csv" id="csv">\n).*?(\n</script>)', lambda m: m.group(1) + csv + m.group(2), s, flags=re.S)
open(p, "w").write(s); print("inlined", csv.count("\n"), "rows")
