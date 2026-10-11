"""
Step 3 - Main result, part 1: conditional logit (Table 3, models 1 and 2).

The regression: for every option on every card, utility =
    development-level effects + water-quality effects + cultural-impact effects
  + extra effect of each development level when $ revenue figures were shown (T2, T3)
  + extra effect of each water level when $ well-being losses were shown (T3)
The status quo (no development, high water, no impact) is the base, so every coefficient is
"how much more (or less) attractive than keeping things as they are".

Two versions are estimated:
  PAPER SPEC  - groups = design card (all people who answered card k pooled into one group).
                This is the only grouping we found that reproduces the published numbers.
  CORRECTED   - groups = one person's answer to one card (3 options, 1 chosen), the textbook
                McFadden conditional logit, with SEs clustered by respondent (4 answers each).

Outputs: output/tables/table3_cl.csv, output/results/cl.json
"""
import numpy as np
import pandas as pd
from common import VARS, TREAT, MAIN, LABELS, PAPER_T3, TAB_OUT, RES_OUT, load_long, fit_clogit, stars, save_json

results, rows = {}, []
for key, sample in [("m1", "all"), ("m2", "councillors")]:
    df = load_long(sample)
    paper = PAPER_T3[key]
    rep = fit_clogit(df, group="card")          # replicate the published specification
    cor = fit_clogit(df, group="occasion")      # corrected specification
    null_ll = df.occasion.nunique() * np.log(1 / 3)
    results[key] = {"paper_spec": rep, "corrected": cor, "null_ll_occasion": null_ll}

    print(f"\n=== Model {paper['name']}   N={rep['n']:,} (paper {paper['n']:,})")
    print(f"log likelihood: replicated {rep['ll']:.2f} | paper {paper['ll']} | corrected {cor['ll']:.2f}"
          f" | null model for 3-option cards {null_ll:.1f}")
    print(f"{'':32s}{'paper':>14s}{'replicated':>16s}{'match':>7s}{'corrected (clustered p)':>28s}")
    for i, v in enumerate(VARS):
        pc, pp = paper["coef"][i], paper["p"][i]
        rc, rp = rep["coef"][i], rep["p"][i]
        match = "yes" if abs(rc - pc) < 0.0015 and abs(rp - pp) < 0.0015 else ("coef" if abs(rc - pc) < 0.0015 else "NO")
        print(f"{LABELS[v]:32s}{pc:8.3f} ({pp:.3f}){rc:8.3f}{stars(rp):3s}({rp:.3f}){match:>7s}"
              f"{cor['coef'][i]:10.3f}{stars(cor['p_cl'][i]):3s}({cor['p_cl'][i]:.3f})")
        rows.append({"model": paper["name"], "variable": LABELS[v], "paper_coef": pc, "paper_p": pp,
                     "rep_coef": round(rc, 3), "rep_se": round(rep["se"][i], 3), "rep_p": round(rp, 3),
                     "match": match, "corr_coef": round(cor["coef"][i], 3), "corr_se_cluster": round(cor["se_cl"][i], 3),
                     "corr_p_cluster": round(cor["p_cl"][i], 3), "corr_p_model": round(cor["p"][i], 3)})

tab = pd.DataFrame(rows)
tab.to_csv(TAB_OUT / "table3_cl.csv", index=False)
n_match = (tab.match == "yes").sum()
print(f"\n{n_match} of {len(tab)} coefficient+p-value pairs match the paper to 3 decimals; "
      f"{(tab.match == 'coef').sum()} match on the coefficient only; mismatches: "
      + "; ".join(f"{r.model} {r.variable}" for r in tab[tab.match == 'NO'].itertuples()))

# Scale-free comparison: each treatment effect as a % of its main effect
# (e.g. how much stronger the aversion to low water quality gets when $ losses are shown).
pairs = dict(zip(TREAT, ["dev_limited", "dev_high", "dev_com", "wat_med", "wat_low"]))
rel = {key: {"paper": {t: PAPER_T3[key]["coef"][VARS.index(t)] / PAPER_T3[key]["coef"][VARS.index(m)] for t, m in pairs.items()},
             **{spec: {t: r[spec]["coef"][VARS.index(t)] / r[spec]["coef"][VARS.index(m)] for t, m in pairs.items()}
                for spec in ("paper_spec", "corrected")}} for key, r in results.items()}

save_json({k: {"paper_spec": {kk: (vv.tolist() if hasattr(vv, "tolist") else vv) for kk, vv in r["paper_spec"].items()},
               "corrected": {kk: (vv.tolist() if hasattr(vv, "tolist") else vv) for kk, vv in r["corrected"].items()},
               "null_ll_occasion": r["null_ll_occasion"]} for k, r in results.items()} | {"relative": rel},
          RES_OUT / "cl.json")
print("Wrote output/tables/table3_cl.csv and output/results/cl.json")
