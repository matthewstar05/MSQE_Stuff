"""
ECON 5015: Homework 3
Matthew Suban
@matthewsuban
"""
import numpy as np
import pandas as pd

a = np.arange(1, 101) # 1-100

b = a ** 2 # a^2

c = a * (a + 1) // 2 # a*(a+1)/2

d = c % 3 == 0 # x e c is divisible by 3, bool

e = np.nonzero(d)[0] # indicies of x e c // 3 == 0

f = c[d] # x e c is divisible by 3, numbers

g = np.cumsum(b) # sum of b

aapl = pd.read_csv("aapl.csv")
high = np.max(aapl["High"]) # max high
low = np.min(aapl["Low"]) # min low
avg = np.mean(aapl["Close"]) # mean close
sd = np.std(aapl["Close"]) # sd close
date = aapl["Date"][np.argmax(aapl["Volume"])] # date of max volume
