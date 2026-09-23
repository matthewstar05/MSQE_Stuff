"""
Step 7 - Reproduce every published exhibit from the parsed CSV files alone, under the same
numbered file names as the originals in replication-targets/, plus side-by-side comparisons.

Input: only output/data/choice_long.csv and output/data/respondents.csv (written by
01_parse_data.py). Models are re-estimated here, so nothing else from the pipeline is reused.

  01_table1_respondent_characteristics   shares of respondents by gender, age, residence, town size
  02_table2_attributes_and_levels        how each attribute level is coded in our data, how often it
                                         was shown, and which "$ shown" term it gets (the published
                                         Table 2 is the questionnaire wording; ours is its data coding)
  03_fig1_responses_per_choice_scenario  answers per design card in each treatment (pure counting)
  04_table3_regression_results           models 1-2: conditional logit grouped as the authors did
                                         (by design card); models 3-4: mixed logit, 500 Halton draws
  05_fig2_treatment_effect_densities     spread across respondents of their own "$ shown" coefficients
                                         (model 3: the published peaks match model 3, although the
                                         text says model 4). Stata-style Epanechnikov densities.

Our versions are coloured (violet numbers in tables; treatment colours in figures) so they can't be
mistaken for the black-and-white originals. Table cells that differ from the published value are shaded.

Outputs (output/paper_figures/):
  01_ ... 05_*.png         reproductions, same names as replication-targets/
  05b_fig2_vs_published.png, 05c_fig2_model4_variant.png   Figure 2 extras
  01_/03_/04_/05_*.csv     ours vs published, number by number
  side_by_side/01_ ... 05_*.png   published (left) next to ours (right)
"""
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import HERE, DATA_OUT, OUT, VARS, TREAT, PAPER_T1, PAPER_T3, stars, fit_clogit, MixedLogit

FIG_DIR = OUT / "paper_figures"; FIG_DIR.mkdir(exist_ok=True)
SBS_DIR = FIG_DIR / "side_by_side"; SBS_DIR.mkdir(exist_ok=True)
TARGETS = HERE / "replication-targets"
EXHIBITS = {1: "01_table1_respondent_characteristics", 2: "02_table2_attributes_and_levels",
            3: "03_fig1_responses_per_choice_scenario", 4: "04_table3_regression_results",
            5: "05_fig2_treatment_effect_densities"}
DRAWS, SEED = 500, 2016          # the paper's number of Halton draws; fixed seed for reproducibility
# Treatment colours as in the dashboard (T1 blue, T2 orange, T3 green). Figure 2's development panels
# take T2's orange (the first group shown development $), its water panels T3's green (only T3 saw water $).
TCOL = {1: "#2a78d6", 2: "#eb6834", 3: "#16a06f"}
PANEL_COL = {"lim_money": ("#eb6834", "#a8431a"), "res_money": ("#eb6834", "#a8431a"), "com_money": ("#eb6834", "#a8431a"),
             "med_money": ("#16a06f", "#0b6b49"), "low_money": ("#16a06f", "#0b6b49")}   # (line/fill, dashed lines)
OURS, FLAG, RULE = "#4a3aa7", "#fbe3b0", "#9a9a9a"   # our numbers, differs-from-published shading, table rules
plt.rcParams.update({"font.family": "sans-serif", "font.size": 11, "axes.edgecolor": "#222222",
                     "axes.linewidth": 0.9, "xtick.color": "#222222", "ytick.color": "#222222"})

# ---------------------------------------------------------------- data: the parsed CSVs only
read = lambda f: pd.read_csv(DATA_OUT / f, keep_default_na=False, na_values=[""])
long, resp = read("choice_long.csv"), read("respondents.csv")
sample = long[long.complete == 1]                 # the 164 respondents who answered all 4 cards
counc = sample[sample.councillor == 1]            # the 123 councillors among them
print(f"Read choice_long.csv ({len(long):,} rows) and respondents.csv ({len(resp)} rows); "
      f"samples: {sample.id.nunique()} all, {counc.id.nunique()} councillors")

# ---------------------------------------------------------------- estimation (Table 3 and Figure 2)
def fit_ml(df):
    """Panel mixed logit from the CSV: 500 Halton draws, all 12 coefficients normal (as in Stata mixlogit)."""
    start = np.r_[fit_clogit(df, "occasion")["coef"], 0.1 * np.ones(len(VARS))]
    m = MixedLogit(df, n_draws=DRAWS, seed=SEED).fit(start)
    se = m.std_errors()[:len(VARS)]
    return m, 2 * stats.norm.sf(np.abs(m.theta[:len(VARS)] / se))

cl1, cl2 = fit_clogit(sample, "card"), fit_clogit(counc, "card")     # grouping that reproduces the paper
(m3, p3), (m4, p4) = fit_ml(sample), fit_ml(counc)
OUR_T3 = {"m1": (cl1["coef"], cl1["p"], cl1["ll"]), "m2": (cl2["coef"], cl2["p"], cl2["ll"]),
          "m3": (m3.theta[:12], p3, m3.ll), "m4": (m4.theta[:12], p4, m4.ll)}
for k, (b, p, ll) in OUR_T3.items():
    print(f"  {PAPER_T3[k]['name']:22s} log likelihood {ll:9.2f}  (paper {PAPER_T3[k]['ll']})")

# ---------------------------------------------------------------- table renderer (PLOS layout)
def draw_table(path, rows, col_w, notes, n_header=1):
    """rows: dicts with cells (list of str), bold, a0 ('left'|'right'|'indent'), flags (set of column indices)."""
    rh, W = 0.32, sum(col_w)
    H = rh * len(rows) + 0.26 * len(notes) + 0.25
    fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
    edges = np.r_[0, np.cumsum(col_w)]
    for r, row in enumerate(rows):
        y = r * rh
        ax.plot([0, W], [y, y], color=RULE, lw=0.8)
        for c, text in enumerate(row["cells"]):
            x0, x1 = edges[c], edges[c + 1]
            if c in row.get("flags", ()):
                ax.add_patch(plt.Rectangle((x0, y), x1 - x0, rh, color=FLAG, lw=0, zorder=0))
            if c == 0:
                a0 = row.get("a0", "left")
                x, ha = {"left": (x0 + 0.06, "left"), "indent": (x0 + 0.16, "left"), "right": (x1 - 0.08, "right")}[a0]
                color = "#111111"
            else:
                x, ha = ((x0 + 0.08, "left") if row.get("left_cells") else ((x0 + x1) / 2, "center"))
                color = "#111111" if r < n_header else OURS
            ax.text(x, y + rh / 2, text, ha=ha, va="center", fontsize=11, color=color,
                    weight="bold" if row.get("bold") or r < n_header else "normal")
    bottom = len(rows) * rh
    ax.plot([0, W], [bottom, bottom], color=RULE, lw=0.8)
    for x in edges[1:-1]:
        ax.plot([x, x], [0, bottom], color=RULE, lw=0.8)
    for i, note in enumerate(notes):
        ax.text(0.06, bottom + 0.2 + 0.26 * i, note, fontsize=9.5, va="center", color="#333333",
                weight="bold" if i == len(notes) - 1 else "normal")
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)

# ---------------------------------------------------------------- 01 Table 1
age = pd.cut(resp.age_group, [0, 2, 3, 4, 5, 6], labels=["<40", "40–49", "50–59", "60–69", ">70"])
town = resp.town_size.map({"50,000+": ">50,000", "15,000-50,000": "15,001–50,000", "5,000-15,000": "5,000–15,000", "<5,000": "<5,000"})
cols = {"Gender": resp.gender, "Age": age, "Personal residence": resp.residence, "City inhabitants": town}
rows, cmp = [{"cells": ["", "Share of respondents (%)"]}], []
for var, cats in PAPER_T1.items():
    share = cols[var].value_counts(normalize=True) * 100
    rows.append({"cells": [var, ""], "bold": True})
    for cat, paper in cats.items():
        ours = round(share.get(cat, np.nan), 1)
        rows.append({"cells": [cat.replace(">", "> ").replace("<", "< ") if var != "Age" else cat, f"{ours:.1f}"],
                     "a0": "right", "flags": {1} if abs(ours - paper) > 0.05 else set()})
        cmp.append({"variable": var, "category": cat, "paper": paper, "ours": ours, "match": abs(ours - paper) <= 0.05})
pd.DataFrame(cmp).to_csv(FIG_DIR / f"{EXHIBITS[1]}_comparison.csv", index=False)
draw_table(FIG_DIR / f"{EXHIBITS[1]}.png", rows, [3.6, 3.6],
           ["All 180 respondents in respondents.csv (the published table also uses all 180).",
            "Shaded cells differ from the published value.",
            "Table 1 reproduced from the parsed data."])
print(f"01 Table 1: {sum(c['match'] for c in cmp)} of {len(cmp)} cells match")

# ---------------------------------------------------------------- 02 Table 2 (as coded in the data)
money_rule = {"lim_money": ("Limited", "development", [2, 3]), "res_money": ("Residential", "development", [2, 3]),
              "com_money": ("Commercial", "development", [2, 3]), "med_money": ("Medium", "water", [3]),
              "low_money": ("Low", "water", [3])}
for col, (lev, attr, ts) in money_rule.items():      # verify the "$ shown" terms follow the rule exactly
    assert (long[col] == ((long[attr] == lev) & long.treatment.isin(ts)).astype(int)).all(), col
spec = [("Development", "development", [("None", "base (status quo only)", "no revenue shown"),
                                        ("Limited", "dev_limited", "lim_money  (T2, T3: +$1M)"),
                                        ("Residential", "dev_high", "res_money  (T2, T3: +$2M)"),
                                        ("Residential and Commercial", "dev_com", "com_money  (T2, T3: +$3M)")]),
        ("Water quality", "water", [("Low", "wat_low", "low_money  (T3: $500k loss)"),
                                    ("Medium", "wat_med", "med_money  (T3: $250k loss)"),
                                    ("High", "base", "T3: \"no losses\" (no term)")]),
        ("Cultural", "cultural", [("None", "base", "never priced"), ("Stables", "cult_s", "never priced"),
                                  ("Stables & landscape", "cult_sl", "never priced")])]
rows = [{"cells": ["Attribute", "Levels", "Variable in our data", "Options shown", "“$ shown” term"], "left_cells": True}]
for attr, col, levels in spec:
    for j, (lev, var, money) in enumerate(levels):
        n = int((sample[col] == ("Commercial" if lev.startswith("Residential and") else lev)).sum())
        rows.append({"cells": [attr if j == 0 else "", lev, var, f"{n:,}", money], "left_cells": True,
                     "bold": False})
        rows[-1]["cells"][0] = attr if j == 0 else ""
draw_table(FIG_DIR / f"{EXHIBITS[2]}.png", rows, [1.7, 2.5, 2.3, 1.6, 2.6],
           ["Options shown = rows in the 1,968-row analysis sample with that level (status quo rows included).",
            "Verified in the data: every “$ shown” term equals 1 exactly when that level appears in the listed treatments.",
            "Table 2 as coded in the parsed data (the published Table 2 gives the questionnaire wording)."])
print("02 Table 2: coding table written ($-shown terms verified against treatment rules)")

# ---------------------------------------------------------------- 03 Figure 1
PAPER_FIG1 = {1: [18, 19, 19, 22, 18, 17, 18, 21, 19, 21, 18, 18],      # bar heights read off the published figure
              2: [17, 15, 20, 18, 17, 20, 18, 19, 15, 18, 17, 14],
              3: [19, 20, 20, 16, 18, 18, 14, 22, 17, 18, 20, 18]}
counts = sample[sample.chosen == 1].groupby(["treatment", "card"]).size().unstack(fill_value=0)
cmp1 = pd.DataFrame([{"treatment": t, "card": c, "ours": int(counts.loc[t, c]), "paper": PAPER_FIG1[t][c - 1]}
                     for t in (1, 2, 3) for c in range(1, 13)])
cmp1["match"] = cmp1.ours == cmp1.paper
cmp1.to_csv(FIG_DIR / f"{EXHIBITS[3]}_comparison.csv", index=False)
print(f"03 Figure 1: {cmp1.match.sum()} of {len(cmp1)} bars match; totals {counts.sum(axis=1).to_dict()}")

fig, ax = plt.subplots(figsize=(8.2, 5.4))
x = np.concatenate([np.arange(12) + g * 13.5 for g in range(3)])          # gap between treatments
ax.bar(x, np.concatenate([counts.loc[t].values for t in (1, 2, 3)]), width=0.62,
       color=np.repeat([TCOL[t] for t in (1, 2, 3)], 12))
ax.set_xticks(x); ax.set_xticklabels([str(c) for c in range(1, 13)] * 3, fontsize=8.5)
for g, t in enumerate((1, 2, 3)):
    ax.text(g * 13.5 + 5.5, -3.4, f"Choice sets\nin treatment {t}", ha="center", va="top", fontsize=13.5, color=TCOL[t])
ax.set_ylabel("Number of responses", fontsize=13.5)
ax.set_yticks(range(0, 25, 5)); ax.set_ylim(0, 23.3); ax.set_xlim(-0.8, x[-1] + 0.8)
ax.tick_params(axis="y", labelrotation=90, labelsize=12)
ax.grid(axis="y", color="#d9d9d9", lw=0.8); ax.set_axisbelow(True)
fig.subplots_adjust(bottom=0.27, left=0.1, right=0.98, top=0.97)
fig.text(0.01, 0.015, "Fig 1. Responses per choice scenario (reproduced from the parsed data).", fontsize=9.5, weight="bold")
fig.savefig(FIG_DIR / f"{EXHIBITS[3]}.png", dpi=200); plt.close(fig)

# ---------------------------------------------------------------- 04 Table 3
SECTIONS = [("Main effects", None), ("Development", ["dev_limited", "dev_high", "dev_com"]),
            ("Water quality", ["wat_med", "wat_low"]), ("Cultural", ["cult_s", "cult_sl"]),
            ("Treatment effects", None), ("Development", ["lim_money", "res_money", "com_money"]),
            ("Water quality", ["med_money", "low_money"])]
NAMES = {"dev_limited": "Limited", "dev_high": "Residential", "dev_com": "Commercial", "wat_med": "Medium",
         "wat_low": "Low", "cult_s": "Stables", "cult_sl": "Stables & landscape", "lim_money": "Limited",
         "res_money": "Residential", "com_money": "Commercial", "med_money": "Medium", "low_money": "Low"}
M = ["m1", "m2", "m3", "m4"]
rows = [{"cells": ["", "(1)", "(2)", "(3)", "(4)"]}, {"cells": ["", "CL", "CL", "ML", "ML"]},
        {"cells": ["", "All", "Councillors", "All", "Councillors"]}]
cmp = []
for head, vs in SECTIONS:
    rows.append({"cells": [head, "", "", "", ""], "bold": True})
    for v in vs or []:
        i = VARS.index(v)
        coef_cells, p_cells, fc, fp = [], [], set(), set()
        for c, k in enumerate(M, start=1):
            b, p, _ = OUR_T3[k]
            coef_cells.append(f"{b[i]:.3f}{stars(p[i])}".replace("-", "−")); p_cells.append(f"({p[i]:.3f})")
            pb, pp = PAPER_T3[k]["coef"][i], PAPER_T3[k]["p"][i]
            if k in ("m1", "m2"):                       # exact targets; ML columns vary with the draws
                if abs(b[i] - pb) >= 0.0015: fc.add(c)
                if abs(p[i] - pp) >= 0.0015: fp.add(c)
            cmp.append({"model": PAPER_T3[k]["name"], "variable": v, "paper_coef": pb, "ours_coef": round(b[i], 3),
                        "paper_p": pp, "ours_p": round(p[i], 3)})
        sub = "(monetary information shown)" if v in TREAT else ""
        rows.append({"cells": [NAMES[v]] + coef_cells, "a0": "indent", "flags": fc})
        rows.append({"cells": [sub] + p_cells, "a0": "indent", "flags": fp})
rows.append({"cells": ["Log likelihood"] + [f"{OUR_T3[k][2]:.2f}".replace("-", "−") for k in M],
             "flags": {c for c, k in enumerate(M, 1) if k in ("m1", "m2") and abs(OUR_T3[k][2] - PAPER_T3[k]["ll"]) > 0.05}})
rows.append({"cells": ["N", f"{len(sample):,}", f"{len(counc):,}", f"{len(sample):,}", f"{len(counc):,}"]})
pd.DataFrame(cmp).to_csv(FIG_DIR / f"{EXHIBITS[4]}_comparison.csv", index=False)
draw_table(FIG_DIR / f"{EXHIBITS[4]}.png", rows, [3.0, 1.9, 1.9, 1.9, 1.9],
           ["p-values in parentheses. *** p < 0.01, ** p < 0.05, * p < 0.1.",
            "(1)-(2): conditional logit grouped by design card, as the authors did. Shaded = differs from the published value.",
            f"(3)-(4): mixed logit, {DRAWS} Halton draws; values shift with the draws (see table3_ml.csv for a 20-run range).",
            "Table 3 reproduced from the parsed data."], n_header=3)
print("04 Table 3 written")

# ---------------------------------------------------------------- 05 Figure 2
def epanechnikov_kde(v, n_points=50):
    """Stata `kdensity` defaults: Epanechnikov kernel, bandwidth 0.9*min(sd, IQR/1.349)*n^-1/5, 50 points."""
    v = np.asarray(v); n = len(v)
    spread = min(v.std(ddof=1), np.subtract(*np.percentile(v, [75, 25])) / 1.349) or v.std(ddof=1) or 1e-3
    h = 0.9 * spread * n ** -0.2
    grid = np.linspace(v.min(), v.max(), n_points)
    u = (grid[:, None] - v[None, :]) / h
    k = np.where(np.abs(u) < np.sqrt(5), 0.75 * (1 - u ** 2 / 5) / np.sqrt(5), 0)
    return grid, k.sum(1) / (n * h)

TITLES = ["Development limited treatment", "Development residential treatment", "Development commercial treatment",
          "WQ medium treatment", "WQ low treatment"]
# Peak and dashed-line positions read off the published Figure 2 (approximate, from a 250-dpi render)
PAPER_FIG2 = {"lim_money": (1.27, 1.14, 1.46), "res_money": (3.30, 1.78, 4.70), "com_money": (1.85, -0.40, 2.90),
              "med_money": (-2.30, -2.65, -1.88), "low_money": (-4.33, -4.44, -4.15)}

def draw_fig2(ind, path, caption, compare=False):
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 6.6))
    for i, (ax, t) in enumerate(zip(axes.flat, TREAT)):
        grid, dens = epanechnikov_kde(ind[:, i])
        lo, hi = np.percentile(ind[:, i], [2.5, 97.5])
        col, dark = PANEL_COL[t]
        ax.fill_between(grid, dens, color=col, alpha=0.16, lw=0)
        ax.plot(grid, dens, color=col, lw=1.6)
        for q in (lo, hi):
            ax.axvline(q, color=dark, ls=(0, (6, 3)), lw=1.3)
        if compare:
            pk, plo, phi = PAPER_FIG2[t]
            for q in (plo, phi):
                ax.axvline(q, color="black", ls=":", lw=2)
            ax.plot(pk, dens.max() * 1.04, marker="v", color="black", ms=8, clip_on=False)
            lo_x, hi_x = min(grid.min(), plo), max(grid.max(), phi)          # keep published lines in view
            ax.set_xlim(lo_x - 0.04 * (hi_x - lo_x), hi_x + 0.04 * (hi_x - lo_x))
        ax.set_xlabel(TITLES[i], fontsize=11); ax.set_ylabel("Density", fontsize=11)
        ax.tick_params(axis="y", labelrotation=90)
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
        ax.set_ylim(bottom=-0.04 * dens.max())
    axes.flat[5].axis("off")
    if compare:
        axes.flat[5].legend(handles=[plt.Line2D([], [], color="#eb6834", lw=1.6, label="Ours: development panels"),
                                     plt.Line2D([], [], color="#16a06f", lw=1.6, label="Ours: water-quality panels"),
                                     plt.Line2D([], [], color="#555555", ls=(0, (6, 3)), label="Ours: 95% of respondents"),
                                     plt.Line2D([], [], color="black", ls=":", lw=2, label="Published: 95% lines"),
                                     plt.Line2D([], [], color="black", marker="v", ls="", label="Published: peak")],
                            loc="center", frameon=False, fontsize=10.5)
    fig.text(0.01, 0.01, caption, fontsize=9.5, weight="bold")
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(path, dpi=200); plt.close(fig)

idx = [VARS.index(t) for t in TREAT]
ind3, ind4 = m3.individual_means()[:, idx], m4.individual_means()[:, idx]
draw_fig2(ind3, FIG_DIR / f"{EXHIBITS[5]}.png",
          "Fig 2. Density plots of the mean coefficients of the treatment effects (model 3, reproduced). "
          "Dashed lines: 95th percentile interval.")
draw_fig2(ind3, FIG_DIR / "05b_fig2_vs_published.png",
          "Figure 2: our reproduction (colour) against the peaks and 95% lines read off the published figure (black).",
          compare=True)
draw_fig2(ind4, FIG_DIR / "05c_fig2_model4_variant.png",
          "Figure 2 drawn from model 4 (councillors), as the text describes. The published peaks match the paper's model 3 coefficients instead.")
rows = []
for i, t in enumerate(TREAT):
    for name, ind, m in (("model 3", ind3, m3), ("model 4", ind4, m4)):
        grid, dens = epanechnikov_kde(ind[:, i])
        rows.append({"panel": TITLES[i], "source": f"ours, {name}", "mean_coef": round(m.theta[VARS.index(t)], 3),
                     "peak": round(grid[dens.argmax()], 2), "p2_5": round(np.percentile(ind[:, i], 2.5), 2),
                     "p97_5": round(np.percentile(ind[:, i], 97.5), 2)})
    pk, lo, hi = PAPER_FIG2[t]
    rows.append({"panel": TITLES[i], "source": "published (read off figure)", "mean_coef": None, "peak": pk, "p2_5": lo, "p97_5": hi})
pd.DataFrame(rows).to_csv(FIG_DIR / f"{EXHIBITS[5]}_summary.csv", index=False)
print("05 Figure 2 written (model 3), plus 05b comparison and 05c model-4 variant")

# ---------------------------------------------------------------- side-by-side comparisons
LABELS = {1: "Table 1", 2: "Table 2", 3: "Figure 1", 4: "Table 3", 5: "Figure 2"}
if TARGETS.is_dir():
    for n, name in EXHIBITS.items():
        a, b = plt.imread(TARGETS / f"{name}.png"), plt.imread(FIG_DIR / f"{name}.png")
        # two equal panels shaped like the published exhibit; each image is fitted inside its panel,
        # so exhibits with different aspect ratios (e.g. Table 2) still compare at a readable size
        box_h = 7.0; box_w = box_h * a.shape[1] / a.shape[0]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(2 * box_w + 0.4, box_h + 0.9))
        for ax, img, title, col in ((ax1, a, "Published (Eppink et al. 2016)", "#111111"),
                                    (ax2, b, "Our reproduction (from the parsed CSVs)", OURS)):
            ax.imshow(img); ax.axis("off"); ax.set_title(title, fontsize=15, weight="bold", color=col, pad=10)
            ih, iw = img.shape[:2]; ratio = box_w / box_h
            if iw / ih < ratio:                                   # narrower than the panel: pad the sides
                pad = (ih * ratio - iw) / 2; ax.set_xlim(-pad, iw + pad); ax.set_ylim(ih, 0)
            else:                                                 # wider: pad top and bottom
                pad = (iw / ratio - ih) / 2; ax.set_xlim(0, iw); ax.set_ylim(ih + pad, -pad)
        fig.suptitle(f"{n:02d} · {LABELS[n]}", fontsize=18, weight="bold", x=0.01, ha="left")
        fig.tight_layout(); fig.savefig(SBS_DIR / f"{name}.png", dpi=150, facecolor="white"); plt.close(fig)
    print(f"Side-by-side comparisons written to {SBS_DIR.relative_to(HERE)}/")
else:
    print("replication-targets/ not found: skipped side-by-side comparisons")
print("Files:", ", ".join(sorted(p.name for p in FIG_DIR.glob("*.*"))))
