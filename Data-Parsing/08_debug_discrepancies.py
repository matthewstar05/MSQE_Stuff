"""
Step 8 - Diagnose every published number we could not reproduce (the shaded cells in
output/paper_figures/01_ and 04_).

For each cell this script tests concrete explanations against the parsed data and prints the evidence.
Inputs: output/data/choice_long.csv, output/data/respondents.csv, and the raw file (for the
survey-completion flags that the respondent file does not carry).

  Table 3, model 2, water quality (-0.393, -0.602)  -> the published values equal our STANDARD ERRORS
  Table 3, model 1, Residential x $ (0.670)         -> the published p-value only fits our 0.699
  Table 3, model 1, Stables & landscape p (0.031)   -> matches a run on all 180 respondents
  Table 1, town size (36.7/30.9/21.3/11.2)          -> only consistent with 188 respondents; the file has 180

Output: output/tables/discrepancy_diagnosis.csv
"""
import numpy as np
import pandas as pd
from scipy import stats
from common import DATA_OUT, TAB_OUT, RAW_DTA, VARS, PAPER_T1, PAPER_T3, fit_clogit

read = lambda f: pd.read_csv(DATA_OUT / f, keep_default_na=False, na_values=[""])
long, resp = read("choice_long.csv"), read("respondents.csv")
sample, counc = long[long.complete == 1], long[(long.complete == 1) & (long.councillor == 1)]
m1, m2, m180 = fit_clogit(sample, "card"), fit_clogit(counc, "card"), fit_clogit(long, "card")
i = {v: VARS.index(v) for v in VARS}
rows = []
def report(cell, published, ours, diagnosis, evidence, verdict):
    rows.append(dict(cell=cell, published=published, ours=ours, diagnosis=diagnosis, evidence=evidence, verdict=verdict))
    print(f"\n### {cell}\n  published {published} | ours {ours}\n  diagnosis: {diagnosis}\n  evidence:  {evidence}\n  verdict:   {verdict}")

# ---- 1. Model 2 water coefficients: standard errors printed in place of coefficients
for v, lab in (("wat_med", "Medium"), ("wat_low", "Low")):
    pub = PAPER_T3["m2"]["coef"][i[v]]
    report(f"Table 3 (2) CL Councillors - Water quality: {lab}", f"{pub:.3f}", f"{m2['coef'][i[v]]:.3f}",
           "Standard error printed in the coefficient cell (with a minus sign)",
           f"our standard error is {m2['se'][i[v]]:.4f}, which rounds to |{pub:.3f}|; every other model-2 number matches",
           "Explained: reporting error in the paper")
assert all(abs(abs(PAPER_T3["m2"]["coef"][i[v]]) - round(m2["se"][i[v]], 3)) < 0.0015 for v in ("wat_med", "wat_low"))

# ---- 2. Model 1 Residential x $: coefficient typo; the printed p-value belongs to our coefficient
v = "res_money"; se = m1["se"][i[v]]
p_if_pub = 2 * stats.norm.sf(PAPER_T3["m1"]["coef"][i[v]] / se)
report("Table 3 (1) CL All - Residential x $ shown", f"{PAPER_T3['m1']['coef'][i[v]]:.3f} (p {PAPER_T3['m1']['p'][i[v]]:.3f})",
       f"{m1['coef'][i[v]]:.3f} (p {m1['p'][i[v]]:.3f})",
       "Coefficient mistyped; the printed p-value is the one our coefficient produces",
       f"with SE {se:.3f}, 0.670 would give p = {p_if_pub:.3f}, but the paper prints 0.018 = p for 0.699. "
       "No alternative sample or coding we tried gives 0.670",
       "Explained: typo in the paper (0.699 is correct)")

# ---- 3. Model 1 Stables & landscape p-value: carried over from a run on all 180 respondents
v = "cult_sl"
report("Table 3 (1) CL All - Stables & landscape (p-value)", f"{PAPER_T3['m1']['p'][i[v]]:.3f} (**)", f"{m1['p'][i[v]]:.3f} (***)",
       "p-value (and its **) likely left over from an earlier run on all 180 respondents",
       f"the same model on all 180 respondents gives p = {m180['p'][i[v]]:.3f} for this row; Table 1 also uses all 180. "
       f"The coefficient in that run ({m180['coef'][i[v]]:.3f}) differs, so the match is suggestive, not proof",
       "Likely explained: stale value from a different sample")

# ---- 4. Table 1 town size: shares imply 188 respondents; the file has 180 (169 answered)
target = np.array(list(PAPER_T1["City inhabitants"].values()))
fits = [n for n in range(100, 400) if (c := np.round(target * n / 100)).sum() == n
        and np.allclose(np.round(c / n * 100, 1), target)]
ours = resp.town_size.value_counts().reindex(["50,000+", "15,000-50,000", "5,000-15,000", "<5,000"])
raw = pd.read_stata(RAW_DTA, convert_categoricals=False).groupby("id").first()
alt = {name: (pd.to_numeric(raw.size_town[m], errors="coerce").value_counts(normalize=True).sort_index() * 100).round(1).tolist()
       for name, m in {"finished": raw.finished == 1, "complete 164": resp.set_index("id").complete.reindex(raw.index) == 1}.items()}
report("Table 1 - City inhabitants (4 rows)", "36.7 / 30.9 / 21.3 / 11.2",
       " / ".join(f"{x:.1f}" for x in ours / ours.sum() * 100),
       "Computed on a different (larger) version of the data than the one published",
       f"the published shares are whole-number counts only for n = {fits} (n=188: 69/58/40/21); the file has 180 "
       f"respondents, {int(ours.sum())} of whom answered ({'/'.join(map(str, ours.astype(int)))}). "
       f"Other samples don't match either: {alt}. The gender, age and residence rows fit the published file exactly",
       "Explained as far as the public data allow: not reproducible from S1 Table")

# ---- 5. (not shaded, noted) Model 4 Residential x $ stars
report("Table 3 (4) ML Councillors - Residential x $ shown (stars)", "3.450** (p 0.062)", "n/a (simulation-based column)",
       "Significance stars inconsistent with the printed p-value",
       "** means p < 0.05 in the table's own legend, but the printed p is 0.062 (would be *)", "Explained: reporting error in the paper")

pd.DataFrame(rows).to_csv(TAB_OUT / "discrepancy_diagnosis.csv", index=False)
print(f"\nWrote output/tables/discrepancy_diagnosis.csv ({len(rows)} diagnosed cells)")
