# Draws the charts used in the explainer PDF (run from the Simple-Replication folder).
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
COLORS = {1: "#9aa5b1", 2: "#e0913a", 3: "#2f6db3"}
NAMES = {1: "Group 1: no $", 2: "Group 2: development $", 3: "Group 3: development + water $"}

data = pd.read_csv("clean_data.csv")
opts = data[data.option != 3].copy()
opts["water"] = np.select([opts.water_low == 1, opts.water_medium == 1], ["Low", "Medium"], "High")
opts["development"] = np.select([opts.limited == 1, opts.residential == 1], ["Limited", "Residential"], "Commercial")

fig, axes = plt.subplots(1, 2, figsize=(9, 3.3), sharey=True)
for ax, attr, levels in [(axes[0], "water", ["High", "Medium", "Low"]),
                         (axes[1], "development", ["Limited", "Residential", "Commercial"])]:
    rates = opts.pivot_table(index=attr, columns="group", values="chosen", aggfunc="mean").loc[levels]
    for i, g in enumerate((1, 2, 3)):
        ax.bar(np.arange(3) + (i - 1) * 0.27, 100 * rates[g], width=0.25, color=COLORS[g], label=NAMES[g])
    ax.set_xticks(range(3)); ax.set_xticklabels(levels)
    ax.set_title(f"Option's {attr} level", loc="left", fontsize=10)
axes[0].set_ylabel("% of the time the option was picked")
axes[0].legend(frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig("explainer/chart_raw_choices.png", dpi=200)

cl = pd.read_csv("results_conditional_logit.csv", index_col=0)
cl = cl[cl["sample"] == "all"].iloc[7:]
labels = ["Limited\n× $", "Residential\n× $", "Commercial\n× $", "Medium water\n× $", "Low water\n× $"]
x = np.arange(5)
fig, ax = plt.subplots(figsize=(9, 3.2))
ax.bar(x - 0.2, cl["ours_paper_version"], 0.38, color="#2f6db3", label="Paper's setup (we match the published table)")
ax.bar(x + 0.2, cl["ours_standard_version"], 0.38, color="#e0913a", label="Standard setup (one person × one card = one choice)")
for i, (a, b, pa, pb) in enumerate(zip(cl["ours_paper_version"], cl["ours_standard_version"],
                                       cl["p_paper_version"], cl["p_standard_clustered"])):
    ax.text(i - 0.2, a + (0.05 if a > 0 else -0.12), f"p={pa:.2f}", ha="center", fontsize=7.5)
    ax.text(i + 0.2, b + (0.05 if b > 0 else -0.12), f"p={pb:.2f}", ha="center", fontsize=7.5)
ax.axhline(0, color="black", lw=0.8)
ax.set_ylim(-1.3, 1.0)
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("Extra effect of\nseeing a $ figure")
ax.legend(frameon=False, fontsize=8, loc="lower left")
fig.tight_layout(); fig.savefig("explainer/chart_money_effects.png", dpi=200)
print("charts saved")
