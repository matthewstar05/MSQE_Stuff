"""
Step 6 - Slide-ready figures (16:9, large type) for the Week 10 presentation.

Each figure's title is the sentence the slide should say out loud:
  slide1_raw_pattern.png      the raw choices already move with the information shown
  slide2_reproduced.png       every published model-1 number reproduces (paper vs ours)
  slide3_grouping_issue.png   ...but only with card-level pooling; correct grouping = smaller, same direction
  slide4_effect_size.png      how much stronger a preference gets once it has a price tag

Outputs: output/slides/*.png
"""
import json
import textwrap
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import OUT, TAB_OUT, RES_OUT, VARS, TREAT, PAPER_T3

SLIDES = OUT / "slides"; SLIDES.mkdir(exist_ok=True)
INK, INK2, MUTED, HAIR, US, PAPER = "#14201b", "#48554f", "#7a8680", "#dbe1da", "#4a3aa7", "#4f5550"
TCOL = {1: "#2a78d6", 2: "#eb6834", 3: "#1baf7a"}
TNAME = {1: "T1 · no $", 2: "T2 · $ development", 3: "T3 · $ development + water"}
SHORT = ["Limited", "Residential", "Commercial", "Medium water", "Low water", "Stables", "Stables & landscape",
         "Limited × $", "Residential × $", "Commercial × $", "Medium water × $", "Low water × $"]
plt.rcParams.update({"font.family": "sans-serif", "font.size": 15, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#bfc6be", "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.titlesize": 16, "axes.titleweight": "bold", "axes.titlecolor": INK, "axes.titlelocation": "left"})

def slide(title, sub):
    fig = plt.figure(figsize=(13.33, 7.5), dpi=150)
    fig.text(0.04, 0.93, title, fontsize=26, fontweight="bold", color=INK)
    fig.text(0.04, 0.9, textwrap.fill(sub, 118), fontsize=15, color=INK2, va="top", linespacing=1.4)
    return fig

def save(fig, name):
    fig.text(0.04, 0.025, "Team 3 replication of Eppink et al. (2016), PLoS ONE 11(10): e0165365 · data: authors' S1 Table",
             fontsize=10, color=MUTED)
    fig.savefig(SLIDES / name, facecolor="white"); plt.close(fig)

# ---------------------------------------------------------------- slide 1: raw pattern
rates = pd.read_csv(TAB_OUT / "choice_rates_by_treatment.csv", keep_default_na=False, na_values=[""])
fig = slide("Before any model, choices already move with the price tags",
            "Share of choices, by which information the respondent's group was shown (164 respondents, 656 choices)")
for i, (attr, lev, ttl) in enumerate([("status quo", "Status quo", "Kept things as they are"),
                                      ("water", "Low", "Picked an option with LOW water quality")]):
    ax = fig.add_axes([0.06 + i * 0.48, 0.12, 0.4, 0.62])
    v = rates[(rates.attribute == attr) & (rates.level == lev)].set_index("treatment").rate
    bars = ax.bar([TNAME[t] for t in (1, 2, 3)], v.values * 100, color=[TCOL[t] for t in (1, 2, 3)], width=0.62)
    for b, x in zip(bars, v.values):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.6, f"{x:.1%}", ha="center", fontsize=17, color=INK, fontweight="bold")
    ax.set_title(ttl); ax.set_ylim(0, max(v.values) * 100 * 1.25); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.tick_params(axis="x", labelsize=12.5)
save(fig, "slide1_raw_pattern.png")

# ---------------------------------------------------------------- slide 2: reproduced
cl = json.loads((RES_OUT / "cl.json").read_text())
fig = slide("We reproduce the paper's main model from its raw data",
            "Model 1 (conditional logit, all respondents): published coefficients (◇) vs our estimates (●). 20 of 24 CL numbers match to 3 decimals; the other 4 are reporting errors in the paper")
ax = fig.add_axes([0.2, 0.12, 0.74, 0.66])
y = np.arange(len(VARS))[::-1]
ax.scatter(cl["m1"]["paper_spec"]["coef"], y, s=110, color=US, zorder=3, label="Ours (replicated)")
ax.scatter(PAPER_T3["m1"]["coef"], y, s=260, marker="D", facecolor="none", edgecolor=PAPER, lw=1.8, zorder=4, label="Published")
ax.axvline(0, color="#bfc6be", lw=1.2); ax.axhline(4.5, color=HAIR, lw=1)
ax.set_yticks(y); ax.set_yticklabels(SHORT); ax.grid(axis="x", color=HAIR); ax.set_axisbelow(True)
ax.text(ax.get_xlim()[0], 4.1, "  extra effect when $ shown ↓", color=MUTED, fontsize=12, va="top")
ax.set_xlabel("Coefficient (pull toward an option vs. keeping things as they are)")
ax.legend(frameon=False, loc="lower right", fontsize=13)
save(fig, "slide2_reproduced.png")

# ---------------------------------------------------------------- slide 3: grouping issue
fig = slide("…but only by pooling each survey card across respondents",
            "A correct model of 3-option choices can't score below the 1-in-3 guess. Grouped correctly (one person × one card), every $ effect keeps its direction, but the confidence intervals are wide")
ax = fig.add_axes([0.06, 0.16, 0.36, 0.55])
floor = cl["m1"]["null_ll_occasion"]
ax.axvspan(-900, floor, color="#d03b3b", alpha=0.08); ax.axvline(floor, color="#a02828", ls="--", lw=1.4)
ax.text(floor - 6, 2.55, "1-in-3 guess\n(floor)", color="#a02828", ha="right", va="top", fontsize=12)
pts = [("Published CL", -852.9, PAPER), ("Corrected CL", cl["m1"]["corrected"]["ll"], US)]
for i, (lab, v, c) in enumerate(pts):
    ax.scatter(v, 1 - i, s=180, color=c, marker="D" if i == 0 else "o", zorder=3)
    ax.text(v, 1 - i + 0.28, f"{lab}\n{v:,.1f}".replace("-", "−"), ha="center", fontsize=12.5, color=INK)
ax.set_xlim(-900, -400); ax.set_ylim(-0.6, 2.6); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_title("Log likelihood (higher = better fit)"); ax.set_xlabel("Model 1, all respondents")
ax2 = fig.add_axes([0.55, 0.16, 0.41, 0.55])
k = [VARS.index(t) for t in TREAT]
pub = np.array(PAPER_T3["m1"]["coef"])[k]
cor = np.array(cl["m1"]["corrected"]["coef"])[k]; se = np.array(cl["m1"]["corrected"]["se_cl"])[k]
yy = np.arange(5)[::-1]
ax2.errorbar(cor, yy - 0.12, xerr=1.96 * se, fmt="o", color=US, ms=10, capsize=0, lw=2.5, label="Corrected, 95% CI (clustered)")
ax2.scatter(pub, yy + 0.12, s=150, marker="D", facecolor="none", edgecolor=PAPER, lw=1.8, label="Published")
ax2.axvline(0, color="#bfc6be", lw=1.2); ax2.set_yticks(yy); ax2.set_yticklabels(SHORT[7:])
ax2.set_title("Extra effect when a $ figure is shown"); ax2.grid(axis="x", color=HAIR); ax2.set_axisbelow(True)
ax2.legend(frameon=False, fontsize=12, loc="upper center", bbox_to_anchor=(0.45, -0.07), ncol=2)
save(fig, "slide3_grouping_issue.png")

# ---------------------------------------------------------------- slide 4: effect size
ml = json.loads((RES_OUT / "ml.json").read_text())
rc = [cl["relative"]["m1"]["corrected"][t] * 100 for t in TREAT]
fig = slide(f"Priced impacts weigh {min(rc):.0f}–{max(rc):.0f}% more (our corrected model)",
            "Each “$ shown” effect as a share of the same attribute's effect without prices. Scale-free, so the models can be compared")
ax = fig.add_axes([0.3, 0.2, 0.66, 0.6])
labs = ["Limited development", "Residential development", "Commercial development", "Medium water quality (aversion)", "Low water quality (aversion)"]
yy = np.arange(5)[::-1]
rel_p = [cl["relative"]["m1"]["paper"][t] for t in TREAT]
rel_c = [cl["relative"]["m1"]["corrected"][t] for t in TREAT]
r = ml["m3"]["relative"]; med = [r["median"][t] for t in TREAT]; lo = [r["min"][t] for t in TREAT]; hi = [r["max"][t] for t in TREAT]
ax.hlines(yy - 0.2, np.array(lo) * 100, np.array(hi) * 100, color=US, alpha=0.25, lw=9)
ax.scatter(np.array(med) * 100, yy - 0.2, s=110, facecolor="white", edgecolor=US, lw=2.2, zorder=3, label="Ours, mixed logit (median and range of 20 runs)")
ax.scatter(np.array(rel_c) * 100, yy + 0.05, s=120, color=US, zorder=3, label="Ours, corrected conditional logit")
ax.scatter(np.array(rel_p) * 100, yy + 0.25, s=170, marker="D", facecolor="none", edgecolor=PAPER, lw=1.8, zorder=3, label="Paper, model 1")
ax.set_yticks(yy); ax.set_yticklabels(labs); ax.axvline(0, color="#bfc6be", lw=1.2)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.set_xlabel("How much stronger the preference is when $ is shown", labelpad=2); ax.grid(axis="x", color=HAIR); ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=12, loc="upper center", bbox_to_anchor=(0.4, -0.13), ncol=3)
save(fig, "slide4_effect_size.png")
print("Wrote", ", ".join(sorted(p.name for p in SLIDES.glob("*.png"))))
