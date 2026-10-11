"""
Shared paths, published numbers, and estimators for the Eppink et al. (2016) replication.

Paper: Eppink, Winden, Wright & Greenhalgh (2016), "Non-Market Values in a Cost-Benefit
World: Evidence from a Choice Experiment", PLoS ONE 11(10): e0165365.

Everything the numbered scripts share lives here so each script stays short:
  - PATHS         where the raw data is and where outputs go
  - PAPER_*       the numbers printed in the paper (Table 1, Table 3) to compare against
  - VARS / LABELS the 12 regressors of Table 3, in the paper's row order
  - fit_clogit()  conditional logit (statsmodels) + cluster-robust SEs
  - MixedLogit    panel mixed logit by simulated maximum likelihood (Halton draws)
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
from statsmodels.discrete.conditional_models import ConditionalLogit

# ----------------------------------------------------------------------------- paths
HERE = Path(__file__).resolve().parent
_CANDIDATES = [HERE.parent / "Resources" / "S1Table.DTA", HERE / "S1Table.DTA"]
RAW_DTA = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[0])
OUT = HERE / "output"
DATA_OUT, TAB_OUT, FIG_OUT, RES_OUT, LOG_OUT = (OUT / d for d in ("data", "tables", "figures", "results", "logs"))
for d in (DATA_OUT, TAB_OUT, FIG_OUT, RES_OUT, LOG_OUT):
    d.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------------- regressors
# Main effects (base levels: no development, high water quality, no cultural impact)
MAIN = ["dev_limited", "dev_high", "dev_com", "wat_med", "wat_low", "cult_s", "cult_sl"]
# Treatment effects = attribute level x "monetary information was shown for this attribute"
#   development $ shown in treatments 2 and 3; water-quality $ shown only in treatment 3
TREAT = ["lim_money", "res_money", "com_money", "med_money", "low_money"]
VARS = MAIN + TREAT
LABELS = {
    "dev_limited": "Development: Limited", "dev_high": "Development: Residential",
    "dev_com": "Development: Commercial", "wat_med": "Water quality: Medium",
    "wat_low": "Water quality: Low", "cult_s": "Cultural: Stables",
    "cult_sl": "Cultural: Stables & landscape",
    "lim_money": "Limited × $ shown", "res_money": "Residential × $ shown",
    "com_money": "Commercial × $ shown", "med_money": "Medium water × $ shown",
    "low_money": "Low water × $ shown",
}

# ----------------------------------------------------------------------------- published numbers
# Table 3 of the paper: (coefficient, p-value) in VARS order, plus log likelihood and N.
PAPER_T3 = {
    "m1": {"name": "(1) CL · All", "ll": -852.9, "n": 1968, "coef": [4.260, 4.553, 4.112, -3.954, -6.135, -0.822, -1.672, 0.205, 0.670, 0.308, -0.473, -0.919],
           "p": [0.000, 0.000, 0.000, 0.000, 0.000, 0.080, 0.031, 0.452, 0.018, 0.282, 0.076, 0.082]},
    "m2": {"name": "(2) CL · Councillors", "ll": -647.0, "n": 1476, "coef": [4.114, 4.545, 4.184, -0.393, -0.602, -0.758, -1.850, 0.084, 0.647, 0.254, -0.299, -0.592],
           "p": [0.000, 0.000, 0.000, 0.000, 0.000, 0.150, 0.001, 0.790, 0.058, 0.433, 0.323, 0.286]},
    "m3": {"name": "(3) ML · All", "ll": -421.92, "n": 1968, "coef": [6.819, 6.259, 6.387, -7.324, -14.950, -1.239, -2.765, 1.290, 3.222, 1.754, -2.272, -4.305],
           "p": [0.002, 0.006, 0.002, 0.000, 0.000, 0.294, 0.080, 0.187, 0.015, 0.082, 0.064, 0.018]},
    "m4": {"name": "(4) ML · Councillors", "ll": -316.4, "n": 1476, "coef": [6.878, 6.554, 6.663, -7.578, -19.020, -2.131, -2.366, 2.650, 3.450, 2.225, -2.085, -8.649],
           "p": [0.011, 0.013, 0.005, 0.000, 0.001, 0.244, 0.164, 0.109, 0.062, 0.166, 0.135, 0.015]},
}
# Table 1 of the paper (share of respondents, %)
PAPER_T1 = {
    "Gender": {"Female": 32.5, "Male": 67.5},
    "Age": {"<40": 8.4, "40–49": 14.8, "50–59": 27.7, "60–69": 36.8, ">70": 12.3},
    "Personal residence": {"Rural": 41.8, "Urban": 58.2},
    "City inhabitants": {">50,000": 36.7, "15,001–50,000": 30.9, "5,000–15,000": 21.3, "<5,000": 11.2},
}


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def load_long(sample="all"):
    """Parsed long-format choice data written by 01_parse_data.py."""
    df = pd.read_csv(DATA_OUT / "choice_long.csv", keep_default_na=False, na_values=[""])
    df = df[df.complete == 1]
    return df[df.councillor == 1] if sample == "councillors" else df


def save_json(obj, path):
    Path(path).write_text(json.dumps(obj, indent=1, default=float))


# ----------------------------------------------------------------------------- conditional logit
def fit_clogit(df, group, cluster="id"):
    """Conditional logit of `chosen` on VARS with choice groups defined by `group`.

    Returns dict with coef, model-based SE/p (what Stata's clogit prints), log likelihood,
    and -- when each group has exactly one chosen row -- respondent-clustered SE/p.
    """
    model = ConditionalLogit(df["chosen"], df[VARS], groups=df[group])
    res = model.fit(disp=0, method="bfgs", maxiter=5000, gtol=1e-10)
    res = model.fit(disp=0, method="newton", start_params=res.params.values, maxiter=200)
    b = res.params.values
    out = {"coef": b, "se": res.bse.values, "p": res.pvalues.values, "ll": res.llf, "n": int(res.nobs),
           "groups": int(df[group].nunique())}
    if (df.groupby(group)["chosen"].sum() == 1).all():      # standard one-choice-per-occasion data
        X, y = df[VARS].to_numpy(float), df["chosen"].to_numpy(float)
        g = df[group].to_numpy()
        v = X @ b
        ev = np.exp(v - pd.Series(v).groupby(g).transform("max").to_numpy())
        P = ev / pd.Series(ev).groupby(g).transform("sum").to_numpy()
        xbar = pd.DataFrame(P[:, None] * X).groupby(g).transform("sum").to_numpy()
        d = X - xbar
        H = (P[:, None] * d).T @ d                              # information matrix
        S = pd.DataFrame((y[:, None]) * d).groupby(df[cluster].to_numpy()).sum().to_numpy()
        Hinv = np.linalg.inv(H)
        C = len(S)
        V = Hinv @ (S.T @ S) @ Hinv * C / (C - 1)
        out["se_cl"] = np.sqrt(np.diag(V))
        out["p_cl"] = 2 * stats.norm.sf(np.abs(b / out["se_cl"]))
    return out


# ----------------------------------------------------------------------------- mixed logit
def halton_normal(n_people, n_draws, dim, seed=0, burn=15):
    """Scrambled ('shuffled') Halton draws mapped to standard normals: shape (people, draws, dim)."""
    h = stats.qmc.Halton(d=dim, scramble=True, seed=seed).random(n_people * n_draws + burn)[burn:]
    return stats.norm.ppf(h).reshape(n_people, n_draws, dim)


class MixedLogit:
    """Panel mixed logit, independent normal coefficients on all VARS (as in Stata's `mixlogit`).

    Each respondent n has coefficients beta_n ~ N(b, diag(s^2)). The likelihood of their four
    choices is integrated over beta_n by averaging over R Halton draws (Train 2009, chs. 6 and 9-11).
    """

    def __init__(self, df, n_draws=500, seed=0):
        d = df.sort_values(["id", "choice_set", "alternative"])
        self.ids = d["id"].unique()
        N, K = len(self.ids), len(VARS)
        self.X = d[VARS].to_numpy(float).reshape(N, 4, 3, K)    # person, choice set, alternative, var
        self.y = d["chosen"].to_numpy(float).reshape(N, 4, 3)
        self.Z = halton_normal(N, n_draws, K, seed)
        self.K = K

    def _probs(self, theta):
        b, s = theta[: self.K], theta[self.K:]
        B = b + s * self.Z                                     # (N, R, K) simulated coefficients
        U = np.einsum("ntjk,nrk->ntjr", self.X, B)
        E = np.exp(U - U.max(2, keepdims=True))
        P = E / E.sum(2, keepdims=True)                        # logit prob of each alternative
        L = (P * self.y[..., None]).sum(2).prod(1)             # (N, R) prob of person's 4 choices
        return B, P, L

    def negll(self, theta):
        B, P, L = self._probs(theta)
        Pn = L.mean(1)
        xbar = np.einsum("ntjr,ntjk->ntrk", P, self.X)
        xch = (self.X * self.y[..., None]).sum(2)
        sc = (xch[:, :, None, :] - xbar).sum(1)                # d log L_nr / d beta_nr
        w = L / Pn[:, None] / L.shape[1]
        G = np.hstack([np.einsum("nr,nrk->nk", w, sc), np.einsum("nr,nrk->nk", w, sc * self.Z)])
        self._scores = G
        return -np.log(Pn).sum(), -G.sum(0)

    def fit(self, start):
        r = minimize(self.negll, start, jac=True, method="BFGS", options={"maxiter": 5000, "gtol": 1e-6})
        self.theta, self.ll, self.converged = r.x, -r.fun, bool(r.success)
        return self

    def std_errors(self, eps=1e-4):
        """Standard errors from the numerical Hessian of the analytic gradient."""
        k = len(self.theta)
        H = np.zeros((k, k))
        for i in range(k):
            e = np.zeros(k); e[i] = eps
            H[:, i] = (self.negll(self.theta + e)[1] - self.negll(self.theta - e)[1]) / (2 * eps)
        cov = np.linalg.pinv((H + H.T) / 2)
        se = np.sqrt(np.clip(np.diag(cov), 0, None))
        self.negll(self.theta)
        return se

    def individual_means(self):
        """E[beta_n | person n's observed choices]: the respondent-level coefficients behind Fig 2."""
        B, _, L = self._probs(self.theta)
        return np.einsum("nr,nrk->nk", L, B) / L.sum(1, keepdims=True)
