# Simple replication: Eppink et al. (2016)

A short, step-by-step version of our replication. Start with **`Eppink2016_Explained_Simply.pdf`** for a plain-language walkthrough of the paper, the models, and what we found.

## Run it
From this folder:

```
python3 run_all.py
```

Or run the steps one at a time:

| Script | What it does | Paper exhibit |
|---|---|---|
| `step1_prepare_data.py` | Loads `../Resources/S1Table.DTA`, builds the "$ shown" variables, picks the 164 complete respondents and the 123 councillors | N in Table 3 |
| `step2_look_at_raw_choices.py` | How often each option was picked, by group (no model) | Background |
| `step3_conditional_logit.py` | Conditional logit, both the paper's grouping and the standard grouping | Table 3, columns 1–2 |
| `step4_mixed_logit.py` | Mixed logit by simulation (500 Halton draws), plus each person's own effects (takes about 2 minutes) | Table 3, columns 3–4; Figure 2 |

Outputs: `clean_data.csv`, `results_conditional_logit.csv`, `results_mixed_logit.csv`, `figure2_individual_effects.png`.

`explainer/` has the source for the PDF (`explainer.html`) and the script that draws its charts (`make_charts.py`).

Needs: pandas, numpy, scipy, statsmodels, matplotlib.
