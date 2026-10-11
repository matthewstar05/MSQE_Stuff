# Step 2: Before any model, look at the raw choices.
#
# Question: when an option has (say) low water quality, how often do people pick it?
# And does that change depending on whether their group saw dollar figures?

import pandas as pd

data = pd.read_csv("clean_data.csv")
options = data[data["option"] != 3]     # Option A and B only (the status quo never changes)


def describe(row):
    if row["limited"]: dev = "Limited"
    elif row["residential"]: dev = "Residential"
    else: dev = "Commercial"
    if row["water_medium"]: water = "Medium"
    elif row["water_low"]: water = "Low"
    else: water = "High"
    return pd.Series({"development": dev, "water": water})


options = pd.concat([options, options.apply(describe, axis=1)], axis=1)

print("Share of the time an option was picked, by group (1 = no $, 2 = dev $, 3 = dev + water $)\n")
for attribute in ["water", "development"]:
    table = options.pivot_table(index=attribute, columns="group", values="chosen", aggfunc="mean")
    print((100 * table).round(1), "\n")

status_quo = data[data["option"] == 3]
print("Status quo picked (%):", (100 * status_quo.groupby("group")["chosen"].mean()).round(1).to_dict())
