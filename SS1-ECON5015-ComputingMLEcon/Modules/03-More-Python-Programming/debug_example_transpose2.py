# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 10:23:56 2020

@author: aric
"""


import numpy as np

def transpose(m):
  row = m.shape[0]  #set row to number of rows in m
  col = m.shape[1]  #set col to number of columns in m
  r=m.copy()
  for i in range(row):
    for j in range(col):
      if (i != j):
        r[i,j] = m[j,i]
        r[j,i] = m[i,j]

    return(r)
  
    
  



x=np.array([[4,3,7],[9,1,12],[0,5,1]])
transpose(x)
