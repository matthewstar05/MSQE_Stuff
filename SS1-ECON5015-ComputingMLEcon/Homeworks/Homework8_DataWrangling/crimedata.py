"""
ECON 5015: Homework 8
Matthew Suban
@matthewsuban
"""
import pandas as pd

full_data = pd.DataFrame() 
for i in range(1, 52): # 50 states+dc loaded into crime_1 to crime_51
    df = pd.read_csv("http://ashafran.github.io/crime_" + str(i) + ".csv")
    full_data = pd.concat([full_data, df], ignore_index=True) # stack under the previous states

# Part B
totals = ["Population", "Violent crime total", "Murder and nonnegligent Manslaughter", "Forcible rape",
          "Robbery", "Aggravated assault", "Property crime total", "Burglary", "Larceny-theft",
          "Motor vehicle theft"] # population + the 9 crime totals, skip the rates
us_data = full_data.groupby("Year")[totals].sum() # add up every state in each year, index is the year
