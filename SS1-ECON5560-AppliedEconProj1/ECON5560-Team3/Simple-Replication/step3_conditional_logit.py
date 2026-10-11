# Step 3: Conditional logit, Table 3 models (1) and (2).
#
# The idea: every option gets a "score" (utility) that adds up its features:
#
#   score = b1*limited + b2*residential + ... + b12*water_low_x_money
#
# The chance a person picks an option = exp(its score) / sum of exp(score) for all options on the card.
# The model picks the b's that make the choices people actually made as likely as possible.
#
# The status quo has every variable = 0, so its score is always 0. Each b therefore means
# "how much more (or less) attractive than leaving things as they are."
#
# We estimate it two ways:
#   paper version    - all answers to the same survey card are lumped into one group.
#                      This is the only setup that reproduces the published numbers.
#   standard version - one person answering one card = one choice (the textbook setup),
#                      with standard errors that allow each person's 4 answers to be related.

import warnings
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.discrete.conditional_models import ConditionalLogit

warnings.filterwarnings("ignore", category=RuntimeWarning)  # numpy on Macs prints false "overflow" warnings; results are fine

VARIABLES = ["limited", "residential", "commercial", "water_medium", "water_low",
             "stables", "stables_landscape",
             "limited_x_money", "residential_x_money", "commercial_x_money",
             "water_medium_x_money", "water_low_x_money"]

# Published Table 3 coefficients for models (1) and (2)
PAPER = {
    "all": [4.260, 4.553, 4.112, -3.954, -6.135, -0.822, -1.672, 0.205, 0.670, 0.308, -0.473, -0.919],
    "councillors": [4.114, 4.545, 4.184, -0.393, -0.602, -0.758, -1.850, 0.084, 0.647, 0.254, -0.299, -0.592],
}


def fit(df, grouping):
    model = ConditionalLogit(df["chosen"], df[VARIABLES], groups=df[grouping])
    return model.fit(disp=0, method="newton", maxiter=200)


def clustered_p_values(df, result):
    # Standard errors that treat each PERSON (not each answer) as the independent unit.
    # This is the usual "sandwich" formula: bread * meat * bread.
    X = df[VARIABLES].to_numpy(float)
    y = df["chosen"].to_numpy(float)
    b = result.params.to_numpy()
    score = np.exp(X @ b)
    prob = score / pd.Series(score).groupby(df["situation"].values).transform("sum").to_numpy()
    avg_X = pd.DataFrame(prob[:, None] * X).groupby(df["situation"].values).transform("sum").to_numpy()
    gap = X - avg_X                                     # each option's features minus the card's "expected" features
    bread = np.linalg.inv((prob[:, None] * gap).T @ gap)
    per_person = pd.DataFrame(y[:, None] * gap).groupby(df["person"].values).sum().to_numpy()
    n = len(per_person)
    covariance = bread @ (per_person.T @ per_person) @ bread * n / (n - 1)
    se = np.sqrt(np.diag(covariance))
    return 2 * stats.norm.sf(np.abs(b / se))


data = pd.read_csv("clean_data.csv")
all_tables = []
for sample in ["all", "councillors"]:
    df = data if sample == "all" else data[data["councillor"] == 1]

    paper_version = fit(df, "card_id")
    standard_version = fit(df, "situation")

    table = pd.DataFrame({
        "paper": PAPER[sample],
        "ours_paper_version": paper_version.params.round(3),
        "p_paper_version": paper_version.pvalues.round(3),
        "ours_standard_version": standard_version.params.round(3),
        "p_standard_clustered": clustered_p_values(df, standard_version).round(3),
    }, index=VARIABLES)
    print(f"\n===== Sample: {sample}   rows = {len(df)}")
    print(f"log likelihood: paper version {paper_version.llf:.1f}, standard version {standard_version.llf:.1f}")
    print(table.to_string())
    all_tables.append(table.assign(sample=sample))

pd.concat(all_tables).to_csv("results_conditional_logit.csv")
print("\nSaved results_conditional_logit.csv")
