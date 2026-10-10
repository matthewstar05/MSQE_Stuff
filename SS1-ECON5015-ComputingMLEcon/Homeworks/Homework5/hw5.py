"""
ECON 5015: Homework 5
Matthew Suban
@matthewsuban
"""

import numpy as np
import itertools as it

# objective function
def f(x):
    return -(x[0]-1)**2-2*(x[1]+2)**2
# gradient
def f1(x):
    return np.array([-2*(x[0]-1),-4*(x[1]+2)])
# hessian matrix
def f2(x):
    return np.array(([-2,0],[0,-4]))

def gridsearch(x0, x1, n, f):
    x = np.linspace(x0, x1, n)
    y = np.linspace(x0, x1, n)
    return np.min(f(x, y))

def newton(x0, e, f1, f2):
    x = x0
    while True:
        x1 = x - f1(x)/f2(x)
        if np.linalg.norm(x1 - x) < e:
            return x1
        x = x1