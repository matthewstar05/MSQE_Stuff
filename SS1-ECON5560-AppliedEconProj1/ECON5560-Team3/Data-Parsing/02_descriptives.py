"""
Step 2 - Descriptive replication: Table 1, Figure 1, and model-free evidence.

  Table 1   respondent characteristics (paper vs. ours)
  Figure 1  number of responses per choice card, by treatment
  Extra     "model-free" treatment comparison: how often options with a given attribute level
            were picked in each treatment - the raw pattern the regressions later formalise.

Outputs: output/tables/table1_comparison.csv, fig1_responses_per_card.csv,
         choice_rates_by_treatment.csv, card_shares.csv; output/figures/*.png;
         output/results/descriptives.json
"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import DATA_OUT, TAB_OUT, FIG_OUT, RES_OUT, PAPER_T1, save_json

resp = pd.read_csv(DATA_OUT / "respondents.csv", keep_default_na=False, na_values=[""])
long = pd.read_csv(DATA_OUT / "choice_long.csv", keep_default_na=False, na_values=[""])
TREAT_NAMES = {1: "T1 · no $ figures", 2: "T2 · $ for development", 3: "T3 · $ for development + water"}
COLORS = {1: "#2a78d6", 2: "#eb6834", 3: "#1baf7a"}
plt.rcParams.update({"font.family": "sans-serif", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#c3c2b7", "axes.labelcolor": "#52514e", "xtick.color": "#52514e",
                     "ytick.color": "#52514e", "axes.titleweight": "bold", "figure.dpi": 150})

# ---------------------------------------------------------------- Table 1
def shares(r):
    """Percent of respondents (with a non-missing answer) in each category, Table 1 layout."""
    age = pd.cut(r.age_group, [0, 2, 3, 4, 5, 6], labels=["<40", "40–49", "50–59", "60–69", ">70"])
    town = r.town_size.map({"50,000+": ">50,000", "15,000-50,000": "15,001–50,000",
                            "5,000-15,000": "5,000–15,000", "<5,000": "<5,000"})
    cols = {"Gender": r.gender, "Age": age, "Personal residence": r.residence, "City inhabitants": town}
    return {k: (v.value_counts(normalize=True) * 100).to_dict() for k, v in cols.items()}

ours_all, ours_comp = shares(resp), shares(resp[resp.complete == 1])
rows = []
for var, cats in PAPER_T1.items():
    for cat, paper in cats.items():
        a, c = ours_all[var].get(cat, np.nan), ours_comp[var].get(cat, np.nan)
        rows.append({"variable": var, "category": cat, "paper": paper, "ours_all_180": round(a, 1),
                     "ours_complete_164": round(c, 1), "diff_all": round(a - paper, 1)})
t1 = pd.DataFrame(rows)
t1.to_csv(TAB_OUT / "table1_comparison.csv", index=False)
print("Table 1 - paper vs. ours\n", t1.to_string(index=False))
exact = (t1.diff_all.abs() <= 0.05)
print(f"\n{exact.sum()} of {len(t1)} Table 1 cells reproduced exactly on all 180 respondents;"
      f" mismatches: {', '.join(t1[~exact].category)}")

# ---------------------------------------------------------------- Figure 1
comp = long[long.complete == 1]
chosen = comp[comp.chosen == 1]
fig1 = chosen.groupby(["card", "treatment"]).size().unstack(fill_value=0)
fig1.to_csv(TAB_OUT / "fig1_responses_per_card.csv")

fig, ax = plt.subplots(figsize=(8, 3.6))
w = 0.26
for i, t in enumerate((1, 2, 3)):
    ax.bar(fig1.index + (i - 1) * w, fig1[t], width=w - 0.03, color=COLORS[t], label=TREAT_NAMES[t])
ax.set_xticks(fig1.index); ax.set_xlabel("Choice card (design row)"); ax.set_ylabel("Responses")
ax.set_title("Figure 1 replicated: responses per choice card", loc="left")
ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper left", bbox_to_anchor=(0, -0.2))
ax.grid(axis="y", color="#e1e0d9", lw=0.6); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig(FIG_OUT / "fig1_responses_per_card.png"); plt.close(fig)

# ---------------------------------------------------------------- model-free treatment comparison
opts = comp[comp.alternative < 3]
rates = []
for attr, levels in {"development": ["Limited", "Residential", "Commercial"],
                     "water": ["High", "Medium", "Low"],
                     "cultural": ["None", "Stables", "Stables & landscape"]}.items():
    for lev in levels:
        for t in (1, 2, 3):
            s = opts[(opts[attr] == lev) & (opts.treatment == t)].chosen
            rates.append({"attribute": attr, "level": lev, "treatment": t, "shown": len(s),
                          "chosen": int(s.sum()), "rate": s.mean()})
for t in (1, 2, 3):
    s = comp[(comp.alternative == 3) & (comp.treatment == t)].chosen
    rates.append({"attribute": "status quo", "level": "Status quo", "treatment": t, "shown": len(s),
                  "chosen": int(s.sum()), "rate": s.mean()})
rates = pd.DataFrame(rates)
rates.to_csv(TAB_OUT / "choice_rates_by_treatment.csv", index=False)
print("\nHow often an option was picked when it was on the card, by treatment:")
print(rates.pivot_table(index=["attribute", "level"], columns="treatment", values="rate").round(3).to_string())

fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
for ax, (attr, levels) in zip(axes, {"water": ["High", "Medium", "Low"],
                                     "development": ["Limited", "Residential", "Commercial"]}.items()):
    sub = rates[rates.attribute == attr]
    for i, t in enumerate((1, 2, 3)):
        v = sub[sub.treatment == t].set_index("level").loc[levels, "rate"]
        ax.bar(np.arange(3) + (i - 1) * w, v * 100, width=w - 0.03, color=COLORS[t], label=TREAT_NAMES[t])
    ax.set_xticks(range(3)); ax.set_xticklabels(levels); ax.set_title(f"{attr.title()} level on the option", loc="left", fontsize=10)
    ax.grid(axis="y", color="#e1e0d9", lw=0.6); ax.set_axisbelow(True)
axes[0].set_ylabel("% of times option was picked")
axes[0].legend(frameon=False, fontsize=7.5, loc="upper right")
fig.tight_layout(); fig.savefig(FIG_OUT / "choice_rates_by_treatment.png"); plt.close(fig)

# ---------------------------------------------------------------- per-card observed shares (dashboard)
card_sh = (chosen.groupby(["card", "treatment"]).alternative.value_counts().unstack(fill_value=0)
           .rename(columns={1: "A", 2: "B", 3: "SQ"}).reset_index())
card_sh.to_csv(TAB_OUT / "card_shares.csv", index=False)

save_json({
    "table1": t1.to_dict(orient="records"),
    "fig1": {int(c): {int(t): int(v) for t, v in r.items()} for c, r in fig1.iterrows()},
    "rates": rates.to_dict(orient="records"),
    "card_shares": card_sh.to_dict(orient="records"),
    "cards": pd.read_csv(DATA_OUT / "design_cards.csv", keep_default_na=False, na_values=[""]).to_dict(orient="records"),
    "flow": json.loads((DATA_OUT / "sample_flow.json").read_text()),
    "sq_by_person": resp[resp.complete == 1].n_status_quo.value_counts().sort_index().to_dict(),
}, RES_OUT / "descriptives.json")
print("\nWrote Table 1, Figure 1, choice-rate tables and figures.")
