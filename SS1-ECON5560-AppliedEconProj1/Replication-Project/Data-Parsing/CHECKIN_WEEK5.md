# Week 5 check-in brief (Team 3)

*For the in-class check-in with Prof. Doremus. The course milestone for this week is "main result attempt documented".*

## Where the replication stands

| Piece | Status | Evidence |
|---|---|---|
| Data opened and understood | ✅ Done | `01_parse_data.py`, `output/logs/01_parse_data.log` |
| Estimation sample (N = 1,968 / 1,476) | ✅ Exact | Complete respondents (164) and councillors (123); see `REPLICATION_LOG.md` §3–4 |
| Table 1 | ✅ 9 / 13 cells exact | Town-size row doesn't match |
| **Main result: Table 3, conditional logit** | ✅ 20 / 24 exact, the rest likely typos | Python + R agree |
| **Main result: Table 3, mixed logit** | ≈ Reproduced within simulation noise | Model 4 fragile |
| Figures 1 & 2 | ✅ Rebuilt | `output/figures/` |
| Interactive dashboard | ✅ | `dashboard/index.html` and GitHub Pages |

**Headline for the check-in:** we can reproduce every published conditional-logit number, but only by grouping choices the way the authors apparently did, which pools each design card across respondents. Done the textbook way, the effects are smaller. They point the same direction and are partly still significant.

## Where we're stuck / questions for Prof. Doremus
1. **Which version counts as "our replication"?** We plan to report both: an exact reproduction of the published specification, and a corrected specification. We'd lead the appraisal with the grouping issue. Is that the right framing for the memo?
2. **Mixed logit without Stata.** We wrote our own estimator. The fit statistics match, but coefficients vary with the random draws. Is comparing against a 20-run range an acceptable standard, or should we try to get Stata `mixlogit` access to confirm?
3. **Unexplained Table 1 row (town size).** Should we contact the authors about this and the Table 3 typos, or simply document them?
4. **Client translation.** Which local stakeholder should the recommendations target? A county or city planning body and a water-quality agency both fit the paper's question, which is whether to price non-market impacts in development decisions.

## Next steps (course timeline)
- **Week 6, appraisal outline + audience split:** bullet skeleton below. Owners per charter: writing/presentation (Daniel, Sam) with data leads (Alistair, Matthew) on the methods bullets.
- **Week 7, full memo draft:** "What we did" can be drafted from `REPLICATION_LOG.md`; figures from `output/figures/`.
- Optional analysis: Hausman–McFadden IIA test; split T2-vs-T1 and T3-vs-T2 contrasts.

## Appraisal skeleton (bullets, to be written up by the team)
**Methods audience**
- Identification: randomised information treatments (credible), but about 55 people per arm, and in T3 development and water prices are always shown together.
- Specification: CL grouping pools choices across people (the LL is below the 3-option floor); the corrected estimates are smaller; no clustering by respondent.
- Robustness: the ML is sensitive to simulation draws; the model 4 headline effect isn't stable; the paper describes `burn(15)` as dropping individuals.
- Design: "no development" appears only in the status quo, so the development coefficients double as an opt-out constant; the water $ values were chosen by the authors, not taken from a valuation study; culture was never priced, so "culture barely mattered" may reflect the attribute framing (the authors say so themselves).
- Reporting: typos in Table 3; the Table 1 town-size mismatch; Table 1 describes 180 respondents, not the 164 in the models.

**Real-world audience**
- Takeaway that survives: showing a dollar figure makes decision-makers weigh that impact more. The direction holds in every version we ran.
- Caution: the size of the effect is uncertain. It depends on how the model is set up, and the sample is small (164 people, one country, surveyed Nov–Dec 2015).
- Practical implication: if an analysis prices some impacts, present unpriced ones (culture, habitat) with equal prominence, or price them where credible.

## Candidate references for the literature section
*Course rule: verify every one against the actual source before citing. None of these has been checked against the full text yet.*
- Train, K. E. (2009). *Discrete choice methods with simulation* (2nd ed.). Cambridge University Press.
- McFadden, D. (1974). Conditional logit analysis of qualitative choice behavior. In P. Zarembka (Ed.), *Frontiers in econometrics* (pp. 105–142). Academic Press.
- Revelt, D., & Train, K. (1998). Mixed logit with repeated choices: Households' choices of appliance efficiency level. *Review of Economics and Statistics, 80*(4), 647–657.
- Hole, A. R. (2007). Fitting mixed logit models by using maximum simulated likelihood. *The Stata Journal, 7*(3), 388–401.
- Hausman, J., & McFadden, D. (1984). Specification tests for the multinomial logit model. *Econometrica, 52*(5), 1219–1240.
- Cameron, A. C., & Miller, D. L. (2015). A practitioner's guide to cluster-robust inference. *Journal of Human Resources, 50*(2), 317–372.
- Bhat, C. R. (2003). Simulation estimation of mixed discrete choice models using randomized and scrambled Halton sequences. *Transportation Research Part B, 37*(9), 837–855.
- Johnston, R. J., et al. (2017). Contemporary guidance for stated preference studies. *Journal of the Association of Environmental and Resource Economists, 4*(2), 319–405.
- Kallis, G., Gómez-Baggethun, E., & Zografos, C. (2013). To value or not to value? That is not the question. *Ecological Economics, 94*, 97–105. (Cited by the paper.)
- Rode, J., Gómez-Baggethun, E., & Krause, T. (2015). Motivation crowding by economic incentives in conservation policy: A review of the empirical evidence. *Ecological Economics, 117*, 270–282. (Cited by the paper.)
