# Replication log: how we got to the main result

A chronological record of what we tried, what worked, and what didn't. It is written so the memo's "What we did" section can be drafted from it directly. The runnable version of every step is in `replication_walkthrough.ipynb`.

---

## 1. Data access and structure
- **Source:** `S1Table.DTA`, the paper's only supplementary file (PLoS ONE S1 Table, CC BY 4.0). No code was published.
- Read with `pandas.read_stata` (numeric codes kept; value labels read separately).
- **2,160 rows × 147 columns, 180 respondents.** Every respondent has exactly 12 rows: 4 choice cards × 3 options (Option A, Option B, status quo). Exactly one option is marked chosen on every card.
- The status quo is always *no development / high water quality / no cultural impact*, as the paper describes.
- There are 12 design cards (Ngene design rows, variable `choice_variables`). They are identical across respondents, and each respondent got a **random 4 of the 12**, not the fixed "two blocks" the paper describes.

## 2. First reproduced number: Table 1
- Gender (67.5 / 32.5), all five age bands, and residence (58.2 / 41.8) match **exactly using all 180 respondents**, so Table 1 describes everyone who started the survey.
- **Not reproduced:** the town-size row. The paper has 36.7 / 30.9 / 21.3 / 11.2%; the file gives 39.1 / 29.0 / 20.1 / 11.8% (180 respondents) and no sample we tried matches. The published shares only correspond to whole-number counts at **188 respondents** (69 / 58 / 40 / 21); the file has 180, of whom 169 answered (66 / 49 / 34 / 20). So this row was computed on a different, larger version of the data than the one published (see §11).

## 3. Identifying the estimation sample (N = 1,968)
Table 3 reports N = 1,968 (all) and 1,476 (councillors). With 12 rows per person, that means 164 and 123 people.

**Dead ends (none gives 164):**

| Filter | Respondents |
|---|---|
| everyone | 180 |
| `finished == 1` | 171 |
| role question answered | 167 |
| finished & role answered | 161 |
| not an always-status-quo respondent (`statusquo == 0`) | 167 |
| involved in planning | 169 |

**What worked:** the recoded answer columns `T{treatment}_{card}a`. **164 respondents answered all four cards**, and 16 answered one to three. In the long file those 16 still have four "chosen" cards, because their unanswered cards were **filled with duplicates of answered ones** (for example, respondent 179 has card 9 four times). Dropping them gives exactly 1,968 rows. We also verified that for every complete respondent the `chosen` flag equals the recoded survey answer.

## 4. Councillor subsample (N = 1,476)
- `role == 1` ("Councillor") among complete respondents gives **121**, two short.
- The paper says 75% of completed surveys came from councillors: 123 / 164 = 75.0%.
- Two "Other" respondents wrote **"Mayor"** and **"Councillor but also Resource Consent Hearing Commissioner"**. Both are elected members; adding them gives **123 → 1,476 rows**. ✔

## 5. Coding the regressors
- Main effects are dummies relative to the status quo: 3 development levels, 2 water levels, 2 cultural levels.
- The paper's "treatment effects" interact each attribute level with "monetary information shown for this attribute". Development $ appears in T2 and T3; water $ only in T3.
- **Trap in the file:** the ready-made `water_high1/2/3` dummies are *high* water × treatment (the base level), not low water. We built all five interaction terms ourselves.
- Structural point for the appraisal: "no development" only ever appears in the status quo, so the development dummies also act as a "choose a new plan" constant.

## 6. First conditional logit attempt: close, but not the published numbers
- A textbook McFadden conditional logit (one group = one person answering one card) gives development ≈ 2.2–2.3, water −2.2 / −3.8, and a log likelihood of **−485.2**.
- The paper has development ≈ 4.1–4.6, water −3.95 / −6.1, and **LL = −852.9**.
- **Diagnosis:** a correctly grouped model of 656 three-option choices can never fit worse than giving every option probability ⅓, which scores 656 × ln(⅓) = **−720.7**. The published −852.9 is below that floor, so the authors' model must be grouped differently.

## 7. Search over groupings: design-card pooling reproduces the table

| Grouping of rows into "choice sets" | log L | Limited | Residential | Commercial |
|---|---|---|---|---|
| person × card (textbook) | −485.18 | 2.235 | 2.338 | 2.174 |
| person (all 4 cards) | −733.23 | 1.825 | 1.739 | 1.721 |
| card position 1–4 | −938.23 | 2.143 | 1.965 | 1.910 |
| binary logit (no grouping) | −954.14 | 2.059 | 1.884 | 1.840 |
| **design card 1–12, pooled across people** | **−852.92** | **4.260** | **4.553** | **4.112** |
| *published* | *−852.9* | *4.260* | *4.553* | *4.112* |

With `group = design card` (as in Stata `clogit …, group(choice_variables)`), **20 of 24 coefficient and p-value pairs match to 3 decimals** across models 1 and 2. The remaining differences are reporting errors in the paper, diagnosed in §11:

| Where | Published | From data | Diagnosis |
|---|---|---|---|
| Model 2, water: medium | −0.393 | −3.891 | −0.393 is our **standard error** (0.3926), printed in place of the coefficient (§11) |
| Model 2, water: low | −0.602 | −6.184 | −0.602 is our **standard error** (0.6017) (§11) |
| Model 1, Residential × $ | 0.670 | 0.699 | The printed p (0.018) is what 0.699 gives; 0.670 would give 0.023 (§11) |
| Model 1, Stables & landscape (p) | 0.031 | 0.001 | The same model on all 180 respondents gives exactly p = 0.031: likely a stale value (§11) |
| Model 4, Residential × $ | 3.450** (p = 0.062) | — | Stars inconsistent with the printed p |

**Independent check:** `crosscheck_clogit.R` (R, `survival::clogit`, exact conditional likelihood) gives identical numbers, including LL −852.92 / −646.98.

## 8. Corrected specification
Same regressors, grouped by person × card, with standard errors clustered by respondent (each person contributes 4 choices):

| "$ shown" effect | Model 1 published | Model 1 corrected (clustered p) | Model 2 corrected (clustered p) |
|---|---|---|---|
| Limited × $ | 0.205 (0.452) | 0.397 (0.273) | 0.250 (0.554) |
| Residential × $ | 0.670 (0.018) | 0.836 (0.039) | 0.754 (0.103) |
| Commercial × $ | 0.308 (0.282) | 0.512 (0.191) | 0.429 (0.361) |
| Medium water × $ | −0.473 (0.076) | −0.584 (0.084) | −0.364 (0.346) |
| Low water × $ | −0.919 (0.082) | −1.023 (0.100) | −0.645 (0.329) |

Scale-free version (the "$ shown" effect as a share of its main effect), corrected model 1: low water becomes **27%** more aversive and residential development **36%** more attractive when priced. The paper's model 1 implies 15% and 15%. **Direction is robust; size and significance depend on specification.**

## 9. Mixed logit (models 3–4)
- Stata was not available, so we wrote a panel mixed logit estimator in numpy/scipy (`common.MixedLogit`, following Train 2009, chapters 6 and 9–11). All 12 coefficients are independent normals, estimated by simulated maximum likelihood with scrambled Halton draws.
- Stata's `mixlogit` sorts by respondent and then by the group variable, so card grouping *within* a respondent is the correct grouping. Consistent with this, our log likelihoods match closely: model 3 −425.4 vs −421.9; model 4 −317.5 vs −316.4.
- **Simulation sensitivity:** with the paper's 500 draws, 20 different draw sequences move the log likelihood by only about 8 points but shift coefficients a lot (model 3 Limited: 5.8 to 18.2). The likelihood surface is flat: 24 parameters, 656 choices.
- 21 of the 24 published ML coefficients fall inside our 20-run range. Model 3 matches well (2,000-draw estimate: Limited 7.20 vs 6.82, Low water −14.59 vs −14.95, Residential × $ 2.98 vs 3.22).
- **Model 4 is fragile:** the headline "Low water × $" effect is −8.65 (p = 0.015) in the paper, and −3.05 (p = 0.38) in our 2,000-draw run.
- The paper's "in each Halton draw, 15 individuals are randomly dropped" most likely describes Stata's `burn(15)` option, which discards the first 15 Halton points. No individuals are dropped.

## 10. Published exhibits side by side (`07_paper_figures.py`, reading only the parsed CSVs)
The paper's five exhibits are saved in `replication-targets/` and numbered in the order they appear in the paper. Our reproductions in `output/paper_figures/` use the same names, and `output/paper_figures/side_by_side/` puts each published/ours pair next to each other:

| # | Exhibit | Result |
|---|---|---|
| 01 | Table 1 | 9 of 13 cells exact; the town-size row was computed on 188 respondents, not the public file (§11) |
| 02 | Table 2 | Ours shows how each level is coded in the data. Every “$ shown” term follows the treatment rule exactly |
| 03 | Figure 1 | All 36 bars exact |
| 04 | Table 3 | CL columns exact apart from 4 reporting errors (shaded, diagnosed in §11); ML columns within simulation noise |
| 05 | Figure 2 | Shape reproduced; 4 of 5 peaks close (see below) |

- **Figure 1** (responses per choice card by treatment): **all 36 bar heights match** the published figure. It uses the 164 complete respondents: the totals of 228 / 208 / 220 are 4 × 57 / 52 / 55.
- **Figure 2** (density across respondents of their own "$ shown" coefficients, with dashed 95% lines): we re-estimated the mixed logit from the CSV with the paper's 500 draws and used posterior means E[βₙ | choicesₙ] with Stata-style Epanechnikov densities. The fit statistic is −421.06 (paper −421.92). Four of the five panel peaks land close to the published ones (1.39 / 3.23 / 1.73 / −2.26 vs 1.27 / 3.30 / 1.85 / −2.30). The low-water panel sits at −5.9 vs −4.3, which is the same draw sensitivity seen in Table 3. Our 95% bands are wider than the published ones for the development panels.
- **The published Figure 2 is from model 3, not model 4.** The text says model 4 (councillors), but the published peaks sit at the model 3 coefficients in Table 3 (1.29, 3.22, 1.75, −2.27, −4.31), not model 4's (2.65, 3.45, 2.23, −2.09, −8.65). We draw it from model 3 and also save a model-4 version (`05c_fig2_model4_variant.png`).

## 11. Debugging the differences (`08_debug_discrepancies.py`)
Every published number we could not reproduce was tested against concrete explanations. The results are in `output/tables/discrepancy_diagnosis.csv`.

| Cell | Published | Ours | Diagnosis | Confidence |
|---|---|---|---|---|
| Table 3 (2), water: medium | −0.393 | −3.891 | Our **standard error is 0.3926**. The SE was printed in the coefficient cell with a minus sign | Certain (both cells match the SEs to 3 decimals) |
| Table 3 (2), water: low | −0.602 | −6.184 | Our **standard error is 0.6017**. Same error | Certain |
| Table 3 (1), Residential × $ | 0.670 (p 0.018) | 0.699 (p 0.018) | With SE 0.295, 0.670 would give p = 0.023. The printed 0.018 is 0.699's p-value, so the coefficient is a typo. No alternative sample or coding gives 0.670 | High |
| Table 3 (1), Stables & landscape p | 0.031 (\*\*) | 0.001 (\*\*\*) | The same model on **all 180 respondents** gives exactly p = 0.031 for this row, and Table 1 also uses 180. Likely left over from an earlier run. That run's coefficient differs (−0.985), so this is suggestive rather than proof | Medium |
| Table 1, town size | 36.7 / 30.9 / 21.3 / 11.2 | 39.1 / 29.0 / 20.1 / 11.8 | The shares are whole-number counts only for **n = 188** (69/58/40/21). The file has 180 respondents, 169 of whom answered. The row was computed on a larger version of the data than the one published. No sample of the public file matches | High that it's not reproducible; its source is unknown |
| Table 3 (4), Residential × $ stars | 3.450\*\* (p 0.062) | — | \*\* contradicts the table's own legend (p 0.062 would be \*) | Certain |

**Bottom line:** none of the differences comes from our code or data parsing. Four are reporting errors in the paper, one is likely a stale value from an earlier sample, and the town-size row was computed on data not included in the published file.

## 12. Not done yet / open items
- Hausman–McFadden IIA test (the paper says IIA "could not be confirmed" but reports no test).
- Confirm the mixed logit in Stata `mixlogit` if a licence becomes available (Cal Poly labs).
- Ask the authors for the 188-respondent file behind Table 1's town-size row, and confirm where the p = 0.031 came from.
- Optional extensions: correlated random coefficients; separate T2-vs-T1 and T3-vs-T2 contrasts; a willingness-to-trade calculation using the $ amounts.
