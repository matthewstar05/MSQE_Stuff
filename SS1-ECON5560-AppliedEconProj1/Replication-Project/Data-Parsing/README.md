# Data-Parsing: replication of Eppink et al. (2016)

**Team 3 · ECON S5560 Applied Economics Project · Fall 2026**

> Eppink, F. V., Winden, M., Wright, W. C. C., & Greenhalgh, S. (2016). Non-market values in a cost-benefit world: Evidence from a choice experiment. *PLoS ONE, 11*(10), e0165365. https://doi.org/10.1371/journal.pone.0165365

**The paper's question:** New Zealand councillors and council staff chose between hypothetical urban-expansion plans. They were randomly split into three groups: no dollar figures (T1), dollar revenue for development (T2), and dollar revenue plus dollar water-quality losses (T3). Does showing a price for some impacts shift choices toward those impacts?

**Our replication in one table**

| Target | Result |
|---|---|
| Estimation samples (N = 1,968 all / 1,476 councillors) | ✅ Exact. 164 people answered all 4 cards; 123 of them are councillors (121 by role code + a Mayor and a Councillor/Commissioner from the free-text answers) |
| Table 1 (respondent characteristics) | ✅ 9 of 13 cells exact on all 180 respondents; ❗ the town-size row does not match |
| Table 3, models 1–2 (conditional logit) | ✅ 20 of 24 coefficient + p-value pairs exact to 3 decimals; the other 4 look like typos in the paper; identical results in R |
| Table 3, models 3–4 (mixed logit) | ≈ Same signs and similar magnitudes; 21 of 24 published values fall inside our simulation-draw range; model 4 is fragile |
| Figure 1, Figure 2 | ✅ Rebuilt |

**Main appraisal finding:** the published conditional logit reproduces *only* if each design card is treated as a single choice pooled across everyone who answered it. The textbook grouping is one person answering one card. The published log likelihood (−852.9) is below the minimum a correctly grouped 3-option model can reach (656 · ln ⅓ = −720.7), which is how we spotted it. Grouping correctly roughly halves the main coefficients. **Every sign survives**, and the "$ shown" effects keep their direction.

## View the results
- **Interactive dashboard:** `dashboard/index.html`. Open it in any browser; it works offline with no installs. It is also published through GitHub Pages from the team repo.
- **Narrated walkthrough:** [`replication_walkthrough.ipynb`](replication_walkthrough.ipynb) shows the whole discovery process, including dead ends, and renders directly on GitHub.
- **Process log:** [`REPLICATION_LOG.md`](REPLICATION_LOG.md) is the step-by-step record of what we tried and decided.
- **Check-in brief:** [`CHECKIN_WEEK5.md`](CHECKIN_WEEK5.md) covers where we stand, open questions, and next steps.

## Run it
```bash
pip install -r requirements.txt
python run_all.py              # ~5 min; the mixed-logit sensitivity runs are the slow part
Rscript crosscheck_clogit.R    # optional: independent check of models 1-2 in R (needs the survival package)
```
The raw data file is read from `../Resources/S1Table.DTA`.

## Pipeline

| Step | File | What it does | Main outputs |
|---|---|---|---|
| 1 | `01_parse_data.py` | Reads `S1Table.DTA`, verifies its structure with assertions, rebuilds both estimation samples and the "$ shown" interaction terms | `output/data/choice_long.csv`, `respondents.csv`, `design_cards.csv`, `sample_flow.json`, `output/logs/01_parse_data.log` |
| 2 | `02_descriptives.py` | Table 1 (paper vs ours), Figure 1, raw pick rates by treatment | `output/tables/table1_comparison.csv`, `fig1_responses_per_card.csv`, `choice_rates_by_treatment.csv`, figures |
| 3 | `03_conditional_logit.py` | Models 1–2 as published (grouped by design card) and corrected (grouped by person × card, respondent-clustered SEs) | `output/tables/table3_cl.csv` |
| 4 | `04_mixed_logit.py` | Models 3–4 by simulated maximum likelihood (own implementation), 20-seed draw-sensitivity, Figure 2 | `output/tables/table3_ml.csv`, `ml_sensitivity.png`, `fig2_individual_effects.png` |
| 5 | `05_build_dashboard.py` | Injects all results into `dashboard/template.html` | `dashboard/index.html` |
| 6 | `06_slide_figures.py` | Slide-ready 16:9 figures with headline titles | `output/slides/*.png` |
| — | `crosscheck_clogit.R` | Models 1–2 again with `survival::clogit` | `output/tables/r_crosscheck_clogit.csv` |
| — | `common.py` | Paths, published numbers, estimators (conditional logit wrapper, `MixedLogit`) | — |

## Key coding decisions
1. **Sample.** Keep respondents with 4 answered cards (`T{t}_{card}a` non-missing). The 16 incomplete respondents have their unanswered cards filled with copies of answered ones in the long file.
2. **Councillors.** `role == 1`, plus the "Other" free-text answers "Mayor" and "Councillor but also Resource Consent Hearing Commissioner".
3. **Treatment terms.** Development level × (T2 or T3); water level × T3. The file's own `water_high{t}` dummies are *high* water × treatment, not low, so we build the low-water term ourselves.
4. **Conditional logit grouping.** As published: `group = design card`. Corrected: `group = respondent × card`.
5. **Mixed logit.** All 12 coefficients are independent normals. Starting values are the corrected CL means with SDs of 0.1 (the `mixlogit` default). We use scrambled Halton draws with the first 15 points burned: 2,000 draws for the primary estimate, plus 20 × 500-draw runs (the paper's setting) to measure simulation noise.

## Folder layout
```
Data-Parsing/
├── 01_parse_data.py … 06_slide_figures.py, run_all.py, common.py
├── crosscheck_clogit.R
├── replication_walkthrough.ipynb
├── dashboard/        template.html (source) → index.html (built)
└── output/
    ├── data/         parsed analysis files
    ├── tables/       every replicated table, paper vs ours
    ├── figures/      PNG figures for the memo
    ├── slides/       16:9 slide-ready figures
    ├── results/      JSON results used by the dashboard
    └── logs/         parsing log
```

## AI-use disclosure
Following our team charter, the code, dashboard and documentation were drafted with an AI coding assistant (Claude, Anthropic). Every number was verified by running the scripts, comparing against the published tables, and re-estimating models 1–2 independently in R. Team members must be able to explain every step before any of it is submitted.
