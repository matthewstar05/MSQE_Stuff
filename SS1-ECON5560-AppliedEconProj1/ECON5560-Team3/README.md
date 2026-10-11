# Does putting a dollar figure on it change the decision?
### Team 3's replication of *"Non-Market Values in a Cost-Benefit World: Evidence from a Choice Experiment"* (Eppink et al., 2016)

**ECON S5560 Applied Economics Project · Cal Poly · Fall 2026**

**[▶ Open the interactive dashboard](https://matthewstar05.github.io/ECON5560-Team3/)** &nbsp;·&nbsp; [Walkthrough notebook](Data-Parsing/replication_walkthrough.ipynb) &nbsp;·&nbsp; [Replication log](Data-Parsing/REPLICATION_LOG.md) &nbsp;·&nbsp; [Presentation guide](presentation/README.md) &nbsp;·&nbsp; [The paper (PDF)](Resources/Eppink_2016_PLoSONE_paper.pdf)

> **In one paragraph.** A 2016 study asked New Zealand councillors to choose between hypothetical housing developments. Some saw the dollar value of a development's revenue and of its damage to water quality; others didn't. The authors conclude that showing dollar figures makes decision-makers weigh those effects more. We rebuilt the study's main results from the authors' raw data. **We reproduce their main table to three decimals, apart from a few apparent typos**, but only after discovering an unusual modelling choice in how their choices were grouped. Done the standard way, the effects point the same direction but are less certain. This repository holds all of it: the data, the code, the results, an interactive dashboard, and slide-ready figures.

---

## Contents
1. [The paper in plain language](#1-the-paper-in-plain-language)
2. [What "replicating" means here](#2-what-replicating-means-here)
3. [Results at a glance](#3-results-at-a-glance)
4. [How we did it, step by step](#4-how-we-did-it-step-by-step)
5. [What the replication turned up](#5-what-the-replication-turned-up)
6. [Key terms](#6-key-terms)
7. [What's in this repository](#7-whats-in-this-repository)
8. [Reproduce everything yourself](#8-reproduce-everything-yourself)
9. [FAQ](#9-faq)
10. [Course milestones](#10-course-milestones)
11. [Team, AI use, citation](#11-team-ai-use-citation)

---

## 1. The paper in plain language

**The worry.** Governments increasingly put dollar values on nature ("this wetland is worth $X a year"). Critics argue that when *some* effects of a decision have a price tag and others don't, decision-makers fixate on the priced ones. This paper tests that idea with real decision-makers.

**Who took part.** 164 New Zealand regional and district **councillors and council staff** (75% councillors), surveyed online in November–December 2015. The response rate was 17.4%.

**What they were asked.** Imagine a town of 20,000 people growing 4% a year. On each "choice card", pick one of three options: **Option A**, **Option B**, or **keep things as they are** (the *status quo*). Everyone answered 4 cards. Each option is described by three *attributes*:

| Attribute | Levels | Status quo |
|---|---|---|
| **Development** | Limited (half the growth housed) · Residential (all growth housed) · Commercial (all growth, plus shops and a "super store") | None |
| **Water quality** in the local stream | High (clear, swimmable) · Medium (slightly murky, not swimmable) · Low (very murky, unsafe) | High |
| **Cultural heritage** (a historic tavern called The Stables) | Stables (surrounded by new buildings) · Stables & landscape (also visible across the landscape) | No impact |

**The experiment.** Respondents were **randomly split into three groups** that saw the *same* options with *different information*:

| Group | What they saw | Respondents in analysis |
|---|---|---|
| **T1** | Words only: no dollar figures | 57 |
| **T2** | Plus the district **revenue** of each development level: $1M / $2M / $3M | 52 |
| **T3** | Plus the **well-being loss** from worse water: $250k (medium) / $500k (low) | 55 |

Cultural heritage was **never** given a dollar value. Because the groups were random, differences in choices between groups can be attributed to the information itself.

**What the authors concluded.** Seeing revenue in dollars made development more attractive; seeing water losses in dollars made people avoid polluted outcomes more; the unpriced cultural impact barely registered. Their policy message: if you price some impacts, price them all (or be aware of the tilt).

## 2. What "replicating" means here
The authors published **one data file** (`Resources/S1Table.DTA`, Stata format) and **no code**. We rebuilt their analysis from scratch in Python and checked the key models in R. Our targets were:

- **Table 1**: who the respondents were (gender, age, residence, town size)
- **Table 3**, the main result: four regression models of the choices
  - (1) conditional logit, all respondents · (2) conditional logit, councillors only
  - (3) mixed logit, all respondents · (4) mixed logit, councillors only
- **Figure 1** (responses per choice card) and **Figure 2** (each councillor's individual effect)

## 3. Results at a glance

| Target | Result |
|---|---|
| Sample sizes (N = 1,968 all / 1,476 councillors) | ✅ **Exact.** We identified precisely which 164 people (and which 123 councillors) the authors used |
| Table 1 | ✅ 9 of 13 numbers exact; ❗ the town-size row only fits 188 respondents, so it came from a larger version of the data than the one published |
| Table 3, models 1–2 (conditional logit) | ✅ **20 of 24 coefficient + p-value pairs exact to 3 decimals.** The other 4 are reporting errors in the paper, including two standard errors printed as coefficients (see finding 3). R gives identical numbers |
| Table 3, models 3–4 (mixed logit) | ≈ Same signs and similar sizes; 21 of 24 published values fall inside our range. The councillor-only model is fragile |
| Figures 1 and 2 | ✅ Figure 1: all 36 bars exact. Figure 2: shape reproduced, 4 of 5 peaks close. The published Figure 2 is model 3, although the text says model 4 |

**Before any model, the raw choices already move with the information shown:**
![Raw pattern](Data-Parsing/output/slides/slide1_raw_pattern.png)

**We reproduce the main model from the raw data (the few differences are reporting errors in the paper):**
![Reproduced](Data-Parsing/output/slides/slide2_reproduced.png)

**…but only with an unusual grouping of the data. Grouped the standard way, the effects keep their direction but are less certain:**
![Grouping issue](Data-Parsing/output/slides/slide3_grouping_issue.png)

**The bottom line for decision-makers: a price tag makes an impact weigh noticeably more:**
![Effect size](Data-Parsing/output/slides/slide4_effect_size.png)

## 4. How we did it, step by step
Each step is a short script in [`Data-Parsing/`](Data-Parsing). The [walkthrough notebook](Data-Parsing/replication_walkthrough.ipynb) runs the same steps with commentary, including the attempts that *didn't* work.

**Step 1: Understand the raw file** (`01_parse_data.py`). The file has 2,160 rows and 147 columns. It is in "long" format: **one row per option shown to a person**. 180 people × 4 cards × 3 options = 12 rows each, and a `chosen` flag marks the pick. For example, one respondent's first card:

| person | card | option | development | water | cultural | chosen |
|---|---|---|---|---|---|---|
| 2 | 6 | Option A | Residential | Low | None | |
| 2 | 6 | Option B | Limited | High | Stables & landscape | ✓ |
| 2 | 6 | Status quo | None | High | None | |

**Step 2: Find the authors' sample.** The paper's N = 1,968 means 164 people × 12 rows, but the file has 180 people. The obvious filters ("finished the survey", "answered the role question", and so on) gave 161–171, never 164. The answer was in the raw answer columns: **164 people answered all 4 cards**. The other 16 answered fewer, and the file silently fills their blanks with *copies of cards they did answer*. Dropping them gives exactly 1,968. ✅

**Step 3: Find the councillors.** The "Councillor" role code gives 121, two short of the paper's 123. Two more people chose "Other" and wrote **"Mayor"** and **"Councillor but also Resource Consent Hearing Commissioner"**. Adding them gives 123 (= 1,476 rows, and the paper's "75% councillors"). ✅

**Step 4: Reproduce Table 1** (`02_descriptives.py`). Gender, age and residence match exactly, using *all 180* respondents. Town size doesn't match any sample of the file. Its percentages only work out to whole-number counts for 188 respondents, so that row was computed on a larger version of the data than the one published.

**Step 5: Build the regression variables.** Each option gets yes/no indicators for its attribute levels, plus "**$ shown**" indicators (for example, "Residential development *and* this person was in T2 or T3"). One trap: the file's ready-made variable `water_high3` means *high* water in T3, not low, so we built these ourselves.

**Step 6: Reproduce models 1–2** (`03_conditional_logit.py`). Our first, standard attempt gave coefficients about half the published size. The published fit statistic gave it away. Its log likelihood of −852.9 is *worse than a model that gives every option a 1-in-3 chance* (−720.7), which is impossible for a correctly set-up model of 3-option choices. Testing different ways of grouping the rows, we found the one that reproduces the paper **exactly**: each of the 12 survey cards is treated as *one big choice* pooled across everyone who answered it. We then also estimated the standard version (one person answering one card = one choice), with standard errors that account for each person answering 4 cards. R's `survival::clogit` (`crosscheck_clogit.R`) gives identical numbers.

**Step 7: Reproduce models 3–4** (`04_mixed_logit.py`). The mixed logit lets every person have their own preferences, which requires computer simulation. Stata wasn't available, so we wrote the estimator ourselves, following Train (2009). The fit statistics match the paper closely (−425.4 vs −421.9). The coefficients, however, move noticeably depending on the random numbers used in the simulation, so we report our estimate *and* the range across 20 re-runs. We also rebuilt Figure 2 from this model.

**Step 8: Present it** (`05_build_dashboard.py`, `06_slide_figures.py`, `07_paper_figures.py`). The dashboard and slide figures come from the same result files, so nothing is typed in by hand. `07_paper_figures.py` redraws all five published exhibits from the parsed CSVs, with names numbered to match the originals in `replication-targets/`, and puts each pair side by side in `output/paper_figures/side_by_side/`.

**Step 9: Debug every difference** (`08_debug_discrepancies.py`). For each published number we couldn't reproduce, the script tests concrete explanations against the data and records the evidence in `output/tables/discrepancy_diagnosis.csv`. None of the differences came from our code (finding 3).

## 5. What the replication turned up
1. **The conditional logit pools each card across people.** That grouping is the only way to reproduce the published numbers, and it is not the standard setup. Grouped the standard way, the main effects roughly halve. **Every effect keeps its direction.** Among the "$ shown" effects, residential development stays significant and the water-quality effects are borderline.
2. **The mixed logit results depend on the random simulation draws.** The model 3 numbers are well within our range. For councillors (model 4), the paper's headline "low water × $" effect (−8.65, p = 0.015) comes out at about −3 (p = 0.38) in our high-precision run.
3. **Every number we couldn't match traces to a reporting problem in the paper** (`08_debug_discrepancies.py`):
   - Model 2's water "coefficients" (−0.393, −0.602) are exactly its **standard errors** (0.393, 0.602), printed in place of the coefficients (−3.891, −6.184).
   - Model 1's residential × $ is printed 0.670, but its printed p-value (0.018) is what the data's 0.699 gives; 0.670 would give 0.023.
   - Model 1's Stables & landscape p-value is printed 0.031 (data: 0.001). The same model on all 180 respondents gives exactly 0.031, so it's likely left over from an earlier run.
   - Table 1's town-size shares only fit 188 respondents; the published file has 180.
   - Model 4's residential × $ is marked \*\* with p = 0.062.
4. **Descriptions that don't match the data.** "15 individuals are randomly dropped" in each simulation draw most likely describes a Stata setting that discards the first 15 random numbers; no people are dropped. The survey is described as using "two blocks", but each person got a random 4 of 12 cards. Table 1 describes all 180 starters, not the 164 analysed. Figure 2 is described as model 4 but matches model 3.
5. **Design limits worth knowing.** "No development" only ever appears in the status quo, so the development effects also capture a general preference for *any* new plan. There are about 55 people per group. In T3, development and water prices always appear together. The water-loss dollar amounts were chosen by the authors rather than taken from a valuation study.

**Our overall read:** the paper's *direction* is robust. Showing a price tag does seem to make people weigh that impact more. How *big* the effect is, and how statistically certain, depends on modelling choices the paper doesn't disclose.

## 6. Key terms
| Term | Meaning here |
|---|---|
| **Choice experiment** | A survey where people pick between made-up options, so researchers can see which features drive choices |
| **Attribute / level** | A feature of an option (water quality) and its possible values (high/medium/low) |
| **Status quo** | "Keep things as they are": no development, high water quality, no heritage impact |
| **Treatment (T1/T2/T3)** | Which information a randomly assigned group saw |
| **Coefficient** | How strongly a feature pulls people toward an option relative to the status quo. Positive means more attractive, negative less. Only signs and relative sizes matter |
| **Conditional logit (CL)** | The standard model for choices among options: each option gets a score from its features, and higher scores are picked more often |
| **Mixed logit (ML)** | A CL where every person has their own coefficients (drawn from a bell curve), so tastes can differ between people |
| **Log likelihood** | How well a model fits the observed choices. Closer to zero is better |
| **p-value / stars** | How surprising the estimate would be if the true effect were zero. \* p < 0.1, \*\* p < 0.05, \*\*\* p < 0.01 |
| **Clustered standard errors** | Uncertainty estimates that account for each person answering 4 cards, since their answers aren't independent |
| **Halton draws** | Evenly spread "random" numbers used to simulate the mixed logit. More draws means less simulation noise |

## 7. What's in this repository
```
ECON5560-Team3/
├── README.md                     ← you are here
├── docs/index.html               ← the interactive dashboard (served by GitHub Pages)
├── presentation/README.md        ← presentation arc, slide plan, likely Q&A
├── Data-Parsing/                 ← all code and results
│   ├── 01_parse_data.py          read + clean the raw file, build the samples
│   ├── 02_descriptives.py        Table 1, Figure 1, raw pick rates
│   ├── 03_conditional_logit.py   Table 3 models 1–2 (published and corrected versions)
│   ├── 04_mixed_logit.py         Table 3 models 3–4, simulation sensitivity, Figure 2
│   ├── 05_build_dashboard.py     builds the dashboard from the results
│   ├── 06_slide_figures.py       16:9 figures for slides
│   ├── 07_paper_figures.py       all 5 published exhibits redrawn from the parsed CSVs, plus side-by-sides
│   ├── 08_debug_discrepancies.py diagnoses every number we couldn't reproduce
│   ├── common.py                 shared settings, published numbers, estimators
│   ├── run_all.py                runs steps 1–8 in order
│   ├── crosscheck_clogit.R       independent check of models 1–2 in R
│   ├── replication_walkthrough.ipynb   narrated version, with outputs
│   ├── REPLICATION_LOG.md        detailed record of every decision and dead end
│   ├── CHECKIN_WEEK5.md          status, open questions, appraisal skeleton
│   ├── dashboard/                dashboard source (template.html) and build
│   ├── replication-targets/      the paper's 5 published exhibits, numbered 01–05
│   └── output/                   data/ tables/ figures/ slides/ paper_figures/ results/ logs/
└── Resources/                    ← supporting files (see Resources/README.md)
    ├── Eppink_2016_PLoSONE_paper.pdf
    ├── S1Table.DTA               the authors' data
    ├── Team3_Charter.pdf
    └── COURSE_REQUIREMENTS.md    memo and presentation requirements, summarised
```
The most useful outputs to open directly: `output/tables/table3_cl.csv` and `table3_ml.csv` (paper vs ours, every coefficient), `output/tables/table1_comparison.csv`, `output/tables/discrepancy_diagnosis.csv` (why each unmatched number differs), `output/paper_figures/side_by_side/*.png` (published vs ours, exhibit by exhibit), and `output/slides/*.png`.

## 8. Reproduce everything yourself
Requires Python 3.10+ (and optionally R with the `survival` package).
```bash
git clone https://github.com/matthewstar05/ECON5560-Team3.git
cd ECON5560-Team3/Data-Parsing
pip install -r requirements.txt
python run_all.py              # about 6 minutes; rebuilds every table, figure, the dashboard, slides and paper exhibits
Rscript crosscheck_clogit.R    # optional, a few seconds
```
- To view the dashboard offline, open `docs/index.html` (or `Data-Parsing/dashboard/index.html`) in any browser. No installs needed.
- To edit the dashboard, change `Data-Parsing/dashboard/template.html` and re-run `python 05_build_dashboard.py`, which also refreshes `docs/index.html`.
- The mixed-logit results use fixed random seeds, so re-running gives the same numbers.

## 9. FAQ
**Is the paper wrong?** Its *direction* holds in every version we ran. What we question is how precisely the effect is measured: the grouping choice, the sensitivity of the mixed logit, and several reporting errors. That's a normal and useful outcome for a replication.

**Why didn't you use Stata like the authors?** We didn't have a licence. Python and R are free, and running the conditional logit in both gives identical numbers, which is stronger evidence than a single run.

**Why don't the mixed logit numbers match exactly?** Mixed logit is estimated by simulation, and the paper's "shuffled" random draws can't be recreated outside Stata. We show that the published numbers fall inside the spread we get from re-running with different draws. That spread is itself a finding.

**Why are some published coefficients about 2× ours in the corrected model?** Pooling each card across ~55 people changes what the model measures. See Step 6 and finding 1.

**Is any sensitive data in here?** No. The survey data is the authors' public supplementary file (CC BY 4.0) and has no names or contact details. Our derived files also leave out respondents' free-text comments. Course-portal pages and the syllabus are deliberately not included; see Canvas for those.

## 10. Course milestones
| Week | Milestone | Status |
|---|---|---|
| 3 | Team charter + data-access check | ✅ `Resources/Team3_Charter.pdf` |
| 4 | Reproduce one number | ✅ Table 1 |
| 5 | Main result attempt documented | ✅ This repository |
| 6 | Appraisal outline + audience split | ⏳ Skeleton in [`CHECKIN_WEEK5.md`](Data-Parsing/CHECKIN_WEEK5.md) |
| 7 | Full memo draft | ⏳ Draft "What we did" from [`REPLICATION_LOG.md`](Data-Parsing/REPLICATION_LOG.md) |
| 8 | Slides draft | ⏳ Figures ready in `Data-Parsing/output/slides/`; plan in [`presentation/`](presentation/README.md) |
| 9 | Rehearse + finalise | ⏳ |
| 10 | Present + final memo | ⏳ |

## 11. Team, AI use, citation
**Team 3:** Daniel T., Alistair K., Matthew S., Sam W. Charter roles: point of contact Sam W.; data analysis leads Alistair K. & Matthew S.; writing/presentation Daniel T. & Sam W.; note-taker/organiser Daniel T.

**AI-use disclosure.** As our charter requires: the code, dashboard and documentation were drafted with an AI coding assistant (Claude, Anthropic). Every estimate was verified by running the code, comparing against the published tables, and re-estimating independently in R. Candidate literature references in `CHECKIN_WEEK5.md` must be checked against the original sources before being cited.

**The paper:** Eppink, F. V., Winden, M., Wright, W. C. C., & Greenhalgh, S. (2016). Non-market values in a cost-benefit world: Evidence from a choice experiment. *PLoS ONE, 11*(10), e0165365. https://doi.org/10.1371/journal.pone.0165365. The article and its data are published under CC BY 4.0.
