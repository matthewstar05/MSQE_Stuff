"""
ECON 5015: Homework 9
Matthew Suban
@matthewsuban
"""
import requests
import pandas as pd

# imports the world bank data for one indicator code and year (all countries)
# and returns it as a data frame, one row per country in the same order as the json
def jsonimport(code, year):
    url = "https://api.worldbank.org/v2/country/all/indicator/" + code + "?format=json&date=" + str(year)
    output = requests.get(url).json()
    pages = output[0]["pages"] # first dictionary says how many pages there are

    df = pd.DataFrame()
    for p in range(1, pages + 1):
        if p > 1: # already have page 1 from above
            output = requests.get(url + "&page=" + str(p)).json()
        for row in output[1]: # second element is the list of rows
            row = dict(row)
            row["indicator"] = row["indicator"]["id"] # keep the id, drop the value
            row["country"] = row["country"]["id"]
            df = pd.concat([df, pd.DataFrame(row, index=pd.Index([0]))], ignore_index=True)
    return df
