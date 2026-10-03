"""
ECON 5015: Homework 5
Matthew Suban
@matthewsuban
"""
import numpy as np
import itertools

# checks a grid of n values between xmin and xmax in each dimension
# and returns the point where f is largest, plus how many points were checked
def gridsearch(xmin, xmax, n, f):
    y = np.transpose(np.linspace(xmin, xmax, n)) # k x n, one row of test values per dimension
    testvals = np.array(list(itertools.product(*y))) # every combination of those values

    workingmax = float("-inf")
    iters = 0 # times we hit the inner loop
    for x in testvals:
        f_val = f(x)
        if f_val > workingmax:
            workingmax = f_val
            xbest = x
        iters = iters + 1
    return (xbest, iters) # tuple, f largest, iteration count

# starts at some guess x and steps using the gradient and hessian
# until the gradient is smaller than e (epsilon)
def newton(x, e, f1, f2):
    x = np.array(x, dtype=float) # initial guess
    iters = 0
    while (np.linalg.norm(f1(x)) > e): # stop once the gradient is close to 0
        x = x - np.linalg.inv(f2(x)) @ f1(x)
        iters = iters + 1
    return (x, iters) # tuple, point where f is largest, iteration count
