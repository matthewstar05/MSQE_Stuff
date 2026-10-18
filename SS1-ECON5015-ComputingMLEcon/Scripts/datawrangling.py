# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 22:27:12 2020

@author: aric
"""


import numpy as np
import pandas as pd

##groupby
labor=pd.read_csv("labordata.csv")

byperson = labor.groupby("id").mean()
byperson_gb = labor.groupby("id")[["units","hours","prod"]]
byperson2 = byperson_gb.mean()
byperson2 = labor.groupby("id")[["units","hours","prod"]].mean()
byperson3 = labor.groupby("id").agg({"units": "mean","hours": "mean","prod": np.mean})
byperson4 = labor.groupby("id").agg({"units": ["mean","sum"],"hours":["mean","sum"],"prod":"mean"})
byperson4.columns=["units_mean","units_sum","hours_mean","hours_sum","prod_mean"]
byperson4["prod2"]=byperson4.units_sum/byperson4.hours_sum


bypersonmonth=labor.groupby(["id","month"]).agg({"day":"count"}).reset_index()

bypersonmonth2=labor.groupby(["id","month"])["day"].first().reset_index() 

#5th day each person worked each month, rows dropped if person worked fewer than 5 days
bypersonmonth3=labor.groupby(["id","month"])["day"].nth(5).reset_index() 

bypersonmonth4=labor.groupby(["id","month"]).agg({"day": list})


#number of overtime days by person
def ot(s):
    return np.sum(s>8)
    
overtime=labor.groupby("id").agg({"hours": ot})


labor["prod_mean"]=labor.groupby("id")["prod"].transform("mean")


## Merge

#one to one
crime = pd.read_csv("crimepanel.csv")
pop = pd.read_csv("poppanel.csv")

d = pd.merge(crime,pop)

crime=crime.rename(columns={"State": "state", "Year":"year"})
d = pd.merge(crime,pop)
d=pd.merge(crime,pop,left_on=["state","year"],right_on=["State","Year"])
d=pd.merge(crime,pop,left_on=["year","state"],right_on=["Year","State"])

d=pd.merge(crime,pop,left_on=["year","state"],right_on=["State","Year"])


#many to one
e=pd.read_csv("e.csv")
f=pd.read_csv("f.csv")

merged=pd.merge(e,f,on="id")

merged=pd.merge(e,f) 

e=e.rename(columns={"id": "sid"})
merged=pd.merge(e,f) 
merged=pd.merge(e,f,left_on="sid",right_on="id")



#many to many
d=pd.merge(crime,pop,left_on="state",right_on="State") 
#What happens here?  matches Alabama 1960 in one dataframe with all Alabama entries
# in the other years (1960-2012)
#matches Alabama 1961 with all Alabama entries in other years (1960-2012)
#and so on, so new size is approx. 53*2968   (approx because missing 1960-64 in NY)

#inner join vs outer join
p2012=pop[pop.Year==2012]
p1960=pop[pop.Year==1960]
pm = pd.merge(p1960,p2012)
pm = pd.merge(p1960,p2012,on="State")
len(pm)
pm = pd.merge(p1960,p2012,on="State",how="outer")
len(pm)



##reshape
pm=pm.drop(columns=["Year_x","Year_y"])
pm=pm.rename(columns={"Population_x":"Population_1960","Population_y":"Population_2012"})

long=pd.wide_to_long(pm,"Population_","State","Year")  
long=long.reset_index()  #wide_to_long returns a dataframe with a multi-index, to instead have traditional columns, use rest_index

long=pd.wide_to_long(pm,"Population","State","Year",sep="_").reset_index()

firmsales=pd.read_csv("firmsales.csv")
firmlong = pd.wide_to_long(firmsales,"sales",["firm","firm_id"],"year",sep="_").reset_index()

firmwide=pd.pivot_table(firmlong,index=["firm","firm_id"],columns="year",values="sales").reset_index().sort_values("firm_id")

#Series.map
state_ids = pd.Series(range(51),pd.unique(long["State"]))

#How to create a column in long with state id's:
long["sid"] = long["State"].map(state_ids)
