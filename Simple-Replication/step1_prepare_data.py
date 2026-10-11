# Step 1: Load the authors' data file and build the two samples used in Table 3.
#
# The file S1Table.DTA has one row per OPTION shown to a person.
# Each person saw 4 choice cards, and each card had 3 options
# (Option A, Option B, Status quo), so each person has 4 x 3 = 12 rows.
# The column "chosen" is 1 for the option they picked and 0 otherwise.

import pandas as pd

raw = pd.read_stata("../Resources/S1Table.DTA", convert_categoricals=False)

data = pd.DataFrame()
data["person"] = raw["id"].astype(int)
data["group"] = raw["treatment"].astype(int)          # 1 = no $, 2 = $ for development, 3 = $ for development and water
data["card_number"] = raw["choice_set"].astype(int)    # 1st, 2nd, 3rd or 4th card this person answered
data["card_id"] = raw["choice_variables"].astype(int)  # which of the 12 survey cards it was
data["option"] = raw["alternatives"].astype(int)       # 1 = A, 2 = B, 3 = status quo
data["chosen"] = raw["alternative_choice"].astype(int)

# Attribute dummies (the authors already made these). The status quo is the base:
# no development, high water quality, no cultural impact.
data["limited"] = raw["dev_limited"]
data["residential"] = raw["dev_high"]       # the authors call residential "high" development
data["commercial"] = raw["dev_com"]
data["water_medium"] = raw["wat_med"]
data["water_low"] = raw["wat_low"]
data["stables"] = raw["cult_s"]
data["stables_landscape"] = raw["cult_sl"]

# "$ shown" variables: an attribute level only gets this extra effect
# if that person's group saw a dollar figure for it.
dev_money_shown = data["group"].isin([2, 3]).astype(int)    # groups 2 and 3 saw development revenue
water_money_shown = (data["group"] == 3).astype(int)        # only group 3 saw water losses in $
data["limited_x_money"] = data["limited"] * dev_money_shown
data["residential_x_money"] = data["residential"] * dev_money_shown
data["commercial_x_money"] = data["commercial"] * dev_money_shown
data["water_medium_x_money"] = data["water_medium"] * water_money_shown
data["water_low_x_money"] = data["water_low"] * water_money_shown

# --- Sample 1: people who actually answered all 4 cards ---
# 180 people are in the file, but 16 answered fewer than 4 cards. Their missing
# cards were filled in with copies of cards they did answer. The survey answers
# are stored in columns named T{group}_{card}a, so we count how many are filled in.
answer_columns = [f"T{g}_{c}a" for g in (1, 2, 3) for c in range(1, 13)]
per_person = raw.groupby("id").first()
cards_answered = per_person[answer_columns].notna().sum(axis=1)
data["complete"] = data["person"].map(cards_answered == 4).astype(int)

# --- Sample 2: councillors ---
# Role code 1 = councillor. Two more people picked "Other" and wrote
# "Mayor" or "Councillor but also ..." so we count them too.
role_text = per_person["role_text"].fillna("")
is_councillor = (per_person["role"] == 1) | role_text.str.contains("Councillor|Mayor", case=False)
data["councillor"] = data["person"].map(is_councillor).astype(int)

# One "choice situation" = one person looking at one card.
data["situation"] = data["person"] * 10 + data["card_number"]

data = data[data["complete"] == 1]
print("People in the 'all' sample:", data["person"].nunique(), "->", len(data), "rows (paper says N = 1,968)")
councillors = data[data["councillor"] == 1]
print("Councillors:", councillors["person"].nunique(), "->", len(councillors), "rows (paper says N = 1,476)")
print("People per group:", data.groupby("group")["person"].nunique().to_dict())

data.to_csv("clean_data.csv", index=False)
print("Saved clean_data.csv")
