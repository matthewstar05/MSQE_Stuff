# Data and output guide

## Source and units

`Replication/Resources/S1Table.DTA` is the paper's public Stata supplement, read without modification. Its 2,160 rows represent 180 respondents, four presented choice occasions and three alternatives per occasion. They are not 2,160 independent people. The raw file contains 147 variables. See `01_parse_data.py` for every transformation.

`output/data/choice_long.csv` retains all 2,160 rows and adds explicit analysis fields. Models filter `complete == 1`: 164 respondents, 656 occasions, 1,968 alternative rows. The councillor subset contains 123 respondents and 1,476 rows. The 16 incomplete respondents are excluded using raw answered-card fields, because the long source contains duplicated cards for their missing answers.

## Parsed fields

| Field | Meaning |
|---|---|
| `id` | Respondent identifier, not a name |
| `treatment` | 1: qualitative; 2: development revenue also shown; 3: development revenue and water losses shown |
| `choice_set` | Presented card position within respondent |
| `card` | Shared experimental design card, one of 12 |
| `occasion` | Respondent-by-choice-position group; one actual decision |
| `alternative` / `alt_label` | Option A, Option B or status quo (raw alternatives 1/2/3) |
| `chosen` | 0/1 selection indicator for this alternative row, derived from `alternative_choice`; not the chosen alternative number |
| `development`, `water`, `cultural` | Human-readable attribute levels |
| `dev_limited`, `dev_high`, `dev_com` | Limited/residential/commercial development indicators; base is no development |
| `wat_med`, `wat_low` | Water-quality indicators; base is high quality |
| `cult_s`, `cult_sl` | Heritage-impact indicators; base is no cultural impact |
| `lim_money`, `res_money`, `com_money` | Development-level indicator multiplied by treatment in {2,3} |
| `med_money`, `low_money` | Water-level indicator multiplied by treatment == 3 |
| `n_answered`, `complete` | Count of genuinely answered raw cards; `complete` is one when count equals four |
| `councillor`, `role` | Analysis membership and readable role label; two elected-member free-text answers supplement raw role code 1 |

The raw `statusquo` field is respondent-level and is distinct from both `chosen` and the status-quo alternative row. A selected status-quo option is identified by `alternative == 3` and `chosen == 1` in the parsed long data.

`respondents.csv` has 180 rows, one per person, including treatment, sample flags, roles, demographics and count of status-quo choices. Item-level demographic percentages use available responses. `design_cards.csv` has 12 rows describing Option A/B attribute combinations.

## Numerical evidence

- `tables/table1_comparison.csv`: published and replicated demographic shares, including denominator differences.
- `tables/fig1_responses_per_card.csv`: 36 card-by-treatment counts, not choice shares.
- `tables/table3_cl.csv`: published, replicated card-pooled and respondent-by-card CL estimates. `corr_p_cluster` uses respondent clustering; `corr_p_model` does not.
- `tables/table3_ml.csv`: 2,000-draw primary ML result and 20 separate 500-draw sensitivity fits. Min/max sensitivity is not a confidence interval.
- `tables/r_crosscheck_clogit.csv`: independent R estimates; p-values here are model-based.
- `tables/discrepancy_diagnosis.csv`: upstream diagnostic interpretations. These are not author-confirmed corrections.
- `paper_figures/04_table3_regression_results_comparison.csv`: separate 500-draw exhibit run used in the paper-style redraw.
- `paper_figures/05_fig2_treatment_effect_densities_summary.csv`: density summaries; published positions are approximate readings from an image.
- `results/cl.json`, `results/ml.json`: unrounded model results and simulation records.

In the Fig. 2 redraw, dashed lines are the 2.5th/97.5th percentiles of posterior mean coefficients across respondents. They are not confidence intervals for an average treatment effect. The repository's model-3 interpretation of the published figure is an inference based on panel locations. Keep that uncertainty in the memo.
