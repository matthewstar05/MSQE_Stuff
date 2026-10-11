"""
Step 1 - Parse the raw Stata file (S1Table.DTA) into clean, documented analysis files.

What the raw file is
  The authors' supplementary data: 2,160 rows x 147 columns, already in "long" format -
  one row per option shown to a respondent. Each respondent saw 4 choice cards, each card
  had 3 options (Option A, Option B, Status quo), so every respondent has 4 x 3 = 12 rows.

What this script does
  1. reads the file and its Stata value labels
  2. rebuilds readable variables (attribute levels, treatment, which option was chosen)
  3. rebuilds the paper's two estimation samples and documents how we identified them
       - All respondents who answered all 4 cards      -> 164 people x 12 rows = 1,968 (paper N)
       - Councillors among them                        -> 123 people x 12 rows = 1,476 (paper N)
  4. creates the "monetary information shown" interaction terms used in Table 3
  5. runs validation checks (assertions) and writes a parsing log

Outputs (output/data): choice_long.csv, respondents.csv, design_cards.csv, sample_flow.json
Log: output/logs/01_parse_data.log
"""
import numpy as np
import pandas as pd
from common import RAW_DTA, DATA_OUT, LOG_OUT, save_json

log_lines = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s); log_lines.append(s)

# ---------------------------------------------------------------- 1. read raw file
reader = pd.io.stata.StataReader(RAW_DTA)
raw = reader.read(convert_categoricals=False)
value_labels = reader.value_labels()
log(f"Raw file: {RAW_DTA.name}  rows={len(raw):,}  columns={raw.shape[1]}  respondents={raw.id.nunique()}")
assert raw.groupby("id").size().eq(12).all(), "every respondent should have 12 rows (4 cards x 3 options)"
log("Each respondent has 12 rows = 4 choice cards x 3 options.")

# ---------------------------------------------------------------- 2. readable variables
DEV = {1: "None", 2: "Limited", 3: "Residential", 4: "Commercial"}   # Stata label 3 = "High" = residential
WAT = {1: "High", 2: "Medium", 3: "Low"}
CUL = {1: "None", 2: "Stables", 3: "Stables & landscape"}
ALT = {1: "Option A", 2: "Option B", 3: "Status quo"}
ROLE = {1: "Councillor", 2: "Policy staff", 3: "Compliance staff", 4: "Science staff", 6: "Other"}

df = pd.DataFrame({
    "id": raw.id.astype(int),
    "treatment": raw.treatment.astype(int),                  # 1 = no $, 2 = $ for development, 3 = $ for development + water
    "choice_set": raw.choice_set.astype(int),                # 1st..4th card this person answered
    "card": raw.choice_variables.astype(int),                # which of the 12 design cards (Ngene design row)
    "alternative": raw.alternatives.astype(int),
    "chosen": raw.alternative_choice.astype(int),
    "development": raw.development.map(DEV),
    "water": raw.waterquality.map(WAT),
    "cultural": raw.cult_impact.map(CUL),
})
df["alt_label"] = df.alternative.map(ALT)
for c in ["dev_limited", "dev_high", "dev_com", "wat_med", "wat_low", "cult_s", "cult_sl"]:
    df[c] = raw[c].astype(int)

# sanity: dummies agree with the categorical codes; status quo is always none / high / none
assert (df.dev_limited == (df.development == "Limited")).all() and (df.dev_high == (df.development == "Residential")).all()
assert (df.wat_low == (df.water == "Low")).all() and (df.cult_sl == (df.cultural == "Stables & landscape")).all()
sq = df.alternative == 3
assert ((df.development == "None") == sq).all(), "'no development' only ever appears as the status quo"
assert (df[sq].water == "High").all() and (df[sq].cultural == "None").all()
assert df.groupby(["id", "choice_set"]).chosen.sum().eq(1).all(), "exactly one option chosen per card"
assert df.groupby(["card", "alternative"])[["development", "water", "cultural"]].nunique().max().max() == 1, \
    "each of the 12 cards shows the same options to everyone"
log("Checks passed: attribute dummies match codes; status quo = none/high/none; one choice per card;")
log("  the 12 design cards are identical across respondents (each person got a random 4 of the 12).")

# A trap in the raw file: 'water_high1..3' is HIGH water quality x treatment (the base level),
# not LOW water x treatment, so the Low x $ interaction has to be built by hand.
assert (raw.water_high3 == ((raw.waterquality == 1) & (raw.treatment == 3))).all()
log("Note: raw 'water_high{t}' = High water x treatment t (base level). We build Low x $ ourselves.")

# ---------------------------------------------------------------- 3. estimation samples
# (a) Complete respondents. The recoded answer columns T{t}_{card}a hold the option each person
#     picked on each card. People with fewer than 4 answers still have 4 "chosen" cards in the
#     long file because their unanswered cards were filled with copies of answered ones.
ans_cols = [f"T{t}_{k}a" for t in (1, 2, 3) for k in range(1, 13)]
first = raw.groupby("id").first()
n_answered = first[ans_cols].notna().sum(axis=1).astype(int)
df["n_answered"] = df.id.map(n_answered)
df["complete"] = (df.n_answered == 4).astype(int)
dup = df[df.complete == 0].groupby("id").card.nunique()
log(f"Answered all 4 cards: {int((n_answered == 4).sum())} respondents; fewer than 4: {int((n_answered < 4).sum())}")
log(f"  incomplete respondents show only {dup.min()}-{dup.max()} distinct cards across their 4 'answers' (duplicated rows)")

# the chosen option always equals the recoded survey answer for that card
ans = raw.apply(lambda r: r[f"T{int(r.treatment)}_{int(r.choice_variables)}a"], axis=1)
assert (ans[df.chosen == 1].astype(int).values == df.alternative[df.chosen == 1].values).all()
log("Check passed: 'chosen' agrees with the recoded survey answers on every card.")

# (b) Councillors: role code 1, plus two 'Other' respondents whose free text says they are elected
#     members ('Mayor', 'Councillor but also Resource Consent Hearing Commissioner').
role_text = first.role_text.fillna("")
is_councillor = (first.role == 1) | role_text.str.contains("Councillor|Mayor", case=False)
df["councillor"] = df.id.map(is_councillor).astype(int)
df["role"] = df.id.map(first.role.map(ROLE)).fillna("Not answered")

# ---------------------------------------------------------------- 4. treatment interactions
money_dev = df.treatment.isin([2, 3]).astype(int)          # development $ shown in T2 and T3
money_wat = (df.treatment == 3).astype(int)                 # water-quality $ shown in T3 only
df["lim_money"], df["res_money"], df["com_money"] = df.dev_limited * money_dev, df.dev_high * money_dev, df.dev_com * money_dev
df["med_money"], df["low_money"] = df.wat_med * money_wat, df.wat_low * money_wat
df["occasion"] = df.id * 10 + df.choice_set                 # one person's answer to one card

# ---------------------------------------------------------------- 5. sample flow + outputs
comp = df[df.complete == 1]
flow = {
    "raw_rows": len(df), "raw_respondents": int(df.id.nunique()),
    "finished_flag": int(first.finished.sum()),
    "incomplete_respondents": int((n_answered < 4).sum()),
    "complete_respondents": int(comp.id.nunique()), "complete_rows": len(comp),
    "choice_occasions": int(comp.occasion.nunique()),
    "councillor_respondents": int(comp[comp.councillor == 1].id.nunique()),
    "councillor_rows": int((comp.councillor == 1).sum()),
    "councillor_by_code": int(((first.role == 1) & (n_answered == 4)).sum()),
    "respondents_by_treatment": comp.groupby("treatment").id.nunique().to_dict(),
    "status_quo_share": float(comp[comp.alternative == 3].chosen.mean()),
}
assert flow["complete_rows"] == 1968 and flow["councillor_rows"] == 1476, "should match Table 3 N"
log(f"Sample 'All': {flow['complete_respondents']} respondents -> {flow['complete_rows']:,} rows (paper N = 1,968)")
log(f"Sample 'Councillors': {flow['councillor_respondents']} respondents -> {flow['councillor_rows']:,} rows (paper N = 1,476); "
    f"{flow['councillor_by_code']} by role code + 2 from free text")
log(f"Respondents per treatment (complete): {flow['respondents_by_treatment']}")
log(f"Status quo chosen on {flow['status_quo_share']:.1%} of cards")

df.to_csv(DATA_OUT / "choice_long.csv", index=False)

resp = pd.DataFrame({
    "id": first.index.astype(int), "treatment": first.treatment.astype(int).values,
    "n_answered": n_answered.values, "complete": (n_answered == 4).astype(int).values,
    "councillor": is_councillor.astype(int).values, "role": first.role.map(ROLE).fillna("Not answered").values,
    "role_text": role_text.values, "finished": first.finished.values,
    "gender": first.gender.map({1: "Male", 2: "Female"}).values,
    "age": first.age.values, "age_group": first.age_group.values,
    "residence": first.residence_area.map({1: "Urban", 2: "Rural"}).values,
    "town_size": first.size_town.map(value_labels["population_size"]).values,
    "years_planning": first.years_planning.values,
    "n_status_quo": df[df.alternative == 3].groupby("id").chosen.sum().reindex(first.index).astype(int).values,
})
resp.to_csv(DATA_OUT / "respondents.csv", index=False)

cards = (df[df.alternative < 3].drop_duplicates(["card", "alternative"])
         .pivot(index="card", columns="alt_label", values=["development", "water", "cultural"]))
cards.columns = [f"{b}_{a}".replace("Option ", "").lower() for a, b in cards.columns]
cards.sort_index().to_csv(DATA_OUT / "design_cards.csv")

save_json(flow, DATA_OUT / "sample_flow.json")
(LOG_OUT / "01_parse_data.log").write_text("\n".join(log_lines) + "\n")
log(f"Wrote choice_long.csv ({len(df):,} rows), respondents.csv ({len(resp)}), design_cards.csv (12 cards)")
