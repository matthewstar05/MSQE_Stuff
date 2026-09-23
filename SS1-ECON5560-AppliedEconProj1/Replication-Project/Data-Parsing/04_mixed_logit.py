"""
Step 4 - Main result, part 2: mixed logit (Table 3, models 3 and 4) and Figure 2.

The mixed logit lets every respondent have their own coefficients (normally distributed across
people) and ties each person's 4 answers together. It has no closed form, so the likelihood is
simulated with Halton draws (paper: 500 "shuffled" Halton draws, Stata `mixlogit`).

Because simulation adds noise, we estimate it two ways:
  PRIMARY      2,000 scrambled Halton draws (4x the paper) -> coefficients, SEs, p-values
  SENSITIVITY  the paper's 500 draws, repeated with 20 different draw sequences, to show how
               much the estimates move purely because of which random draws were used

Figure 2 in the paper plots each councillor's own (posterior mean) treatment coefficients from
model 4; we rebuild it from the primary model-4 run.

Outputs: output/tables/table3_ml.csv, output/figures/ml_sensitivity.png,
         output/figures/fig2_individual_effects.png, output/results/ml.json
"""
import json
import time
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import VARS, TREAT, LABELS, PAPER_T3, TAB_OUT, FIG_OUT, RES_OUT, load_long, MixedLogit, stars, save_json

K = len(VARS)
PRIMARY_DRAWS, PRIMARY_SEED = 2000, 2016
SENS_DRAWS, SENS_SEEDS = 500, range(20)
cl = json.loads((RES_OUT / "cl.json").read_text())
pairs = dict(zip(TREAT, ["dev_limited", "dev_high", "dev_com", "wat_med", "wat_low"]))

out, rows = {}, []
for key, cl_key, sample in [("m3", "m1", "all"), ("m4", "m2", "councillors")]:
    df = load_long(sample)
    start = np.r_[cl[cl_key]["corrected"]["coef"], 0.1 * np.ones(K)]   # clogit means, small SDs (mixlogit default)
    t0 = time.time()
    prim = MixedLogit(df, PRIMARY_DRAWS, PRIMARY_SEED).fit(start)
    se = prim.std_errors()
    b, p = prim.theta[:K], 2 * stats.norm.sf(np.abs(prim.theta / se))[:K]
    sens = []
    for s in SENS_SEEDS:
        m = MixedLogit(df, SENS_DRAWS, s).fit(start)
        sens.append({"seed": s, "ll": m.ll, "coef": m.theta[:K].tolist(), "sd": np.abs(m.theta[K:]).tolist()})
    S = np.array([r["coef"] for r in sens])
    paper = PAPER_T3[key]
    print(f"\n=== Model {paper['name']}  ({time.time() - t0:.0f}s)")
    print(f"log likelihood: primary ({PRIMARY_DRAWS} draws) {prim.ll:.2f} | paper {paper['ll']} | "
          f"{len(sens)} x {SENS_DRAWS}-draw runs: {min(r['ll'] for r in sens):.1f} to {max(r['ll'] for r in sens):.1f}")
    print(f"{'':32s}{'paper':>15s}{'primary':>17s}{'500-draw runs: median [min, max]':>36s}  paper inside?")
    for i, v in enumerate(VARS):
        lo, med, hi = S[:, i].min(), np.median(S[:, i]), S[:, i].max()
        inside = lo <= paper["coef"][i] <= hi
        print(f"{LABELS[v]:32s}{paper['coef'][i]:8.3f} ({paper['p'][i]:.3f}){b[i]:8.3f}{stars(p[i]):3s}({p[i]:.3f})"
              f"{med:12.2f} [{lo:6.2f}, {hi:6.2f}]{'yes' if inside else 'no':>10s}")
        rows.append({"model": paper["name"], "variable": LABELS[v], "paper_coef": paper["coef"][i], "paper_p": paper["p"][i],
                     "primary_coef": round(b[i], 3), "primary_se": round(se[i], 3), "primary_p": round(p[i], 3),
                     "primary_sd": round(abs(prim.theta[K + i]), 3),
                     "sens_median": round(med, 3), "sens_min": round(lo, 3), "sens_max": round(hi, 3),
                     "paper_inside_range": inside})
    rel_runs = [{t: r["coef"][VARS.index(t)] / r["coef"][VARS.index(m)] for t, m in pairs.items()} for r in sens]
    out[key] = {"primary": {"coef": b.tolist(), "se": se[:K].tolist(), "p": p.tolist(), "sd": np.abs(prim.theta[K:]).tolist(),
                            "sd_se": se[K:].tolist(), "ll": prim.ll, "draws": PRIMARY_DRAWS, "converged": prim.converged},
                "sensitivity": sens,
                "relative": {"paper": {t: paper["coef"][VARS.index(t)] / paper["coef"][VARS.index(m)] for t, m in pairs.items()},
                             "median": {t: float(np.median([r[t] for r in rel_runs])) for t in TREAT},
                             "min": {t: float(min(r[t] for r in rel_runs)) for t in TREAT},
                             "max": {t: float(max(r[t] for r in rel_runs)) for t in TREAT}}}
    if key == "m4":
        ind = prim.individual_means()                     # (people, K) posterior-mean coefficients
        fig2 = {}
        for t in TREAT:
            x = ind[:, VARS.index(t)]
            grid = np.linspace(x.min() - 0.5, x.max() + 0.5, 120)
            dens = stats.gaussian_kde(x)(grid) if x.std() > 1e-6 else np.zeros_like(grid)
            fig2[t] = {"values": x.tolist(), "grid": grid.tolist(), "density": dens.tolist(),
                       "p2_5": float(np.percentile(x, 2.5)), "p97_5": float(np.percentile(x, 97.5)), "mean": float(x.mean())}
        out["fig2"] = fig2

tab = pd.DataFrame(rows)
tab.to_csv(TAB_OUT / "table3_ml.csv", index=False)
print(f"\nPaper's ML coefficient inside our 500-draw range: {tab.paper_inside_range.sum()} of {len(tab)}")

# ---------------------------------------------------------------- figures
fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), sharey=True)
for ax, key in zip(axes, ("m3", "m4")):
    S = np.array([r["coef"] for r in out[key]["sensitivity"]])
    for i in range(K):
        ax.scatter(S[:, i], np.full(len(S), -i) + np.random.default_rng(i).uniform(-0.18, 0.18, len(S)),
                   s=9, color="#2a78d6", alpha=0.45, lw=0)
        ax.scatter(PAPER_T3[key]["coef"][i], -i, marker="D", s=30, color="#eb6834", zorder=3)
        ax.scatter(out[key]["primary"]["coef"][i], -i, marker="|", s=160, color="#0b0b0b", zorder=3)
    ax.axvline(0, color="#c3c2b7", lw=0.8); ax.set_title(PAPER_T3[key]["name"], loc="left", fontsize=10)
    ax.grid(axis="x", color="#e1e0d9", lw=0.6)
axes[0].set_yticks([-i for i in range(K)]); axes[0].set_yticklabels([LABELS[v] for v in VARS], fontsize=8)
fig.suptitle("Mixed logit: 20 runs with different Halton draws (blue), our 2,000-draw estimate (|), paper (◆)",
             x=0.01, ha="left", fontsize=10, fontweight="bold")
fig.tight_layout(); fig.savefig(FIG_OUT / "ml_sensitivity.png", dpi=150); plt.close(fig)

fig, axes = plt.subplots(1, 5, figsize=(12, 2.6))
for ax, t in zip(axes, TREAT):
    f = out["fig2"][t]
    ax.fill_between(f["grid"], f["density"], color="#2a78d6", alpha=0.25, lw=0)
    ax.plot(f["grid"], f["density"], color="#2a78d6", lw=1.5)
    for q in (f["p2_5"], f["p97_5"]):
        ax.axvline(q, color="#52514e", ls=":", lw=1)
    ax.axvline(0, color="#c3c2b7", lw=0.8)
    ax.set_title(LABELS[t], fontsize=8.5, loc="left"); ax.set_yticks([])
fig.suptitle("Figure 2 replicated: each councillor's own treatment-effect coefficient (model 4)", x=0.01, ha="left",
             fontsize=10, fontweight="bold")
fig.tight_layout(); fig.savefig(FIG_OUT / "fig2_individual_effects.png", dpi=150); plt.close(fig)

save_json(out, RES_OUT / "ml.json")
print("Wrote output/tables/table3_ml.csv, figures, and output/results/ml.json")
