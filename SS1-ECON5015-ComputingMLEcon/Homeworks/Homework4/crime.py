"""
ECON 5015: Homework 4
Matthew Suban
@matthewsuban
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# Part 1
fulldata = pd.read_csv("london_crime.csv")
fulldata["crimerate"] = fulldata["crime"] / fulldata["population"] # crimes per person
fulldata["policerate"] = fulldata["police"] / fulldata["population"] # police hours per person
fulldata["lcrime"] = np.log(fulldata["crimerate"])
fulldata["lpolice"] = np.log(fulldata["policerate"])
fulldata["lemp"] = np.log(fulldata["emp"])
fulldata["lun"] = np.log(fulldata["un"])
fulldata["lymale"] = np.log(fulldata["ymale"])
fulldata["lwhite"] = np.log(fulldata["white"])

model1 = smf.ols("lcrime ~ lpolice + lemp + lun + lymale + lwhite", data=fulldata).fit()

# Part 2
fulldata = fulldata.sort_values(["borough", "week"]).reset_index(drop=True)
df1 = fulldata[fulldata["week"] < 53].reset_index(drop=True) # year 1
df2 = fulldata[fulldata["week"] > 52].reset_index(drop=True) # year 2, same borough/week order as df1
diffdata = pd.DataFrame()
diffdata["borough"] = df2["borough"]
diffdata["week"] = df2["week"]
diffdata["dlcrime"] = df2["lcrime"] - df1["lcrime"]
diffdata["dlpolice"] = df2["lpolice"] - df1["lpolice"]
diffdata["dlun"] = df2["lun"] - df1["lun"]
diffdata["dlemp"] = df2["lemp"] - df1["lemp"]
diffdata["dlymale"] = df2["lymale"] - df1["lymale"]
diffdata["dlwhite"] = df2["lwhite"] - df1["lwhite"]

model2 = smf.ols("dlcrime ~ dlpolice + dlemp + dlun + dlymale + dlwhite + C(week)", data=diffdata).fit()

# Part 3
diffdata["sixweeks"] = ((diffdata["week"] >= 80) & (diffdata["week"] <= 85)).astype(int) # post-attack weeks
diffdata["sixweeks_treat"] = diffdata["sixweeks"] * diffdata["borough"].isin([1, 2, 3, 6, 14]).astype(int) # post-attack weeks, treated boroughs

model3 = smf.ols("dlcrime ~ dlemp + dlun + dlymale + dlwhite + sixweeks + sixweeks_treat + C(week)", data=diffdata).fit()

