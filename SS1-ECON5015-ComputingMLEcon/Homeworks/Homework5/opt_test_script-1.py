# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 14:29:26 2024

@author: aric
"""
import numpy as np

from opt import newton, gridsearch

def f(x):
    return -(x[0]-1)**2-2*(x[1]+2)**2

def f1(x):
    return np.array([-2*(x[0]-1),-4*(x[1]+2)])

def f2(x):
    return np.array(([-2,0],[0,-4]))

ret_n = newton([0,0],0.001,f1,f2)   #tests newton with initial guess of [0,0] and e=0.001

ret_g = gridsearch([-10,-10],[10,10],2000,f)  #tests gridsearch with interval [-10,10] for both x and y and with precision~0.01
