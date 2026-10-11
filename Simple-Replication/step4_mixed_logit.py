# Step 4: Mixed logit, Table 3 models (3) and (4), and Figure 2.
#
# The conditional logit gives everyone the SAME b's. The mixed logit lets each person
# have their OWN b's. We assume each b is spread across people like a bell curve:
#
#   person's b_k = average_k + spread_k * (random normal number)
#
# So instead of 12 numbers we estimate 24: an average and a spread for each variable.
#
# Problem: we never see a person's own b's, so we can't plug them in. The fix is simulation.
# For each person, try 500 possible sets of b's drawn from the bell curves,
# work out how likely that person's 4 actual choices are under each set, and average.
# (The paper does the same with 500 "Halton draws", which are evenly spread pseudo-random numbers.)
#
# Then, like before, choose the averages and spreads that make everyone's choices most likely.
# Note: results move a bit depending on which random draws you use. That is normal for this model.

import warnings
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

VARIABLES = ["limited", "residential", "commercial", "water_medium", "water_low",
             "stables", "stables_landscape",
             "limited_x_money", "residential_x_money", "commercial_x_money",
             "water_medium_x_money", "water_low_x_money"]
K = len(VARIABLES)
warnings.filterwarnings("ignore", category=RuntimeWarning)  # false "overflow" warnings from numpy on Macs
DRAWS = 500
SEED = 0      # change this to see how much the results move with different random draws

# Published Table 3 coefficients (the averages) for models (3) and (4)
PAPER = {
    "all": [6.819, 6.259, 6.387, -7.324, -14.950, -1.239, -2.765, 1.290, 3.222, 1.754, -2.272, -4.305],
    "councillors": [6.878, 6.554, 6.663, -7.578, -19.020, -2.131, -2.366, 2.650, 3.450, 2.225, -2.085, -8.649],
}


def prepare(df):
    df = df.sort_values(["person", "card_number", "option"])
    n_people = df["person"].nunique()
    X = df[VARIABLES].to_numpy(float).reshape(n_people, 4, 3, K)   # person, card, option, variable
    chosen = df["chosen"].to_numpy(float).reshape(n_people, 4, 3)
    # Halton draws turned into normal random numbers: one set per person per draw
    halton = stats.qmc.Halton(d=K, scramble=True, seed=SEED).random(n_people * DRAWS)
    normal_draws = stats.norm.ppf(halton).reshape(n_people, DRAWS, K)
    return X, chosen, normal_draws


def person_likelihoods(params, X, chosen, normal_draws):
    average, spread = params[:K], params[K:]
    b = average + spread * normal_draws                          # each person's simulated b's: (person, draw, variable)
    scores = np.einsum("pcok,pdk->pcod", X, b)                   # score of every option under every draw
    scores -= scores.max(axis=2, keepdims=True)                  # keeps exp() from overflowing
    prob = np.exp(scores) / np.exp(scores).sum(axis=2, keepdims=True)
    prob_of_choice = (prob * chosen[..., None]).sum(axis=2)      # chance of the option actually picked on each card
    return prob_of_choice.prod(axis=1), b                        # chance of all 4 of a person's choices, per draw


def negative_log_likelihood(params, X, chosen, normal_draws):
    L, _ = person_likelihoods(params, X, chosen, normal_draws)
    return -np.log(L.mean(axis=1)).sum()                         # average over draws, then add up over people


def standard_errors(f, params, step=1e-3):
    # Curvature of the likelihood at the best estimate (the "Hessian"), by finite differences.
    n = len(params)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            ei, ej = np.eye(n)[i] * step, np.eye(n)[j] * step
            H[i, j] = H[j, i] = (f(params + ei + ej) - f(params + ei - ej)
                                 - f(params - ei + ej) + f(params - ei - ej)) / (4 * step ** 2)
    return np.sqrt(np.abs(np.diag(np.linalg.pinv(H))))


data = pd.read_csv("clean_data.csv")
cl = pd.read_csv("results_conditional_logit.csv", index_col=0)
all_tables = []
for sample in ["all", "councillors"]:
    df = data if sample == "all" else data[data["councillor"] == 1]
    X, chosen, normal_draws = prepare(df)
    f = lambda params: negative_log_likelihood(params, X, chosen, normal_draws)

    # Start from the standard conditional logit answer, with small spreads
    start = np.r_[cl[cl["sample"] == sample]["ours_standard_version"].to_numpy(), 0.1 * np.ones(K)]
    result = minimize(f, start, method="BFGS", options={"maxiter": 3000})
    se = standard_errors(f, result.x)
    average = result.x[:K]
    p = 2 * stats.norm.sf(np.abs(average / se[:K]))

    table = pd.DataFrame({"paper": PAPER[sample], "ours_average": average.round(3), "p": p.round(3),
                          "ours_spread": np.abs(result.x[K:]).round(3)}, index=VARIABLES)
    print(f"\n===== Sample: {sample}   log likelihood {-result.fun:.1f} (paper: {-421.92 if sample == 'all' else -316.4})")
    print(table.to_string())
    all_tables.append(table.assign(sample=sample))

    # Figure 2: each person's own "$ shown" effects. For each person, weight the 500 simulated
    # b's by how well each one explains that person's actual choices, then average.
    if sample == "all":   # the published Figure 2 matches model (3), the all-respondents model
        L, b = person_likelihoods(result.x, X, chosen, normal_draws)
        weights = L / L.sum(axis=1, keepdims=True)
        own_b = np.einsum("pd,pdk->pk", weights, b)
        fig, axes = plt.subplots(1, 5, figsize=(13, 2.8))
        for ax, name in zip(axes, VARIABLES[7:]):
            ax.hist(own_b[:, VARIABLES.index(name)], bins=20, color="steelblue")
            ax.axvline(0, color="black", lw=0.8)
            ax.set_title(name, fontsize=9)
        fig.suptitle("Each respondent's own '$ shown' effect (Figure 2)")
        fig.tight_layout()
        fig.savefig("figure2_individual_effects.png", dpi=150)

pd.concat(all_tables).to_csv("results_mixed_logit.csv")
print("\nSaved results_mixed_logit.csv and figure2_individual_effects.png")
