"""
ECON 5015: Model Selection Assignment
Matthew Suban
@matthewsuban
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import LeaveOneOut, cross_val_predict

boston = pd.read_csv("http://ashafran.github.io/boston.csv")
y = boston["MEDV"]
X = boston.drop(columns="MEDV")
n = len(y)

X1 = X
X2 = PolynomialFeatures(degree=2, include_bias=False, interaction_only=True).fit_transform(X)
X3 = PolynomialFeatures(degree=2, include_bias=False).fit_transform(X)

bic = []
loo = []
for log in [False, True]:
    for Xm in [X1, X2, X3]:
        target = y
        if log:
            target = np.log(y)

        y_pred = LinearRegression().fit(Xm, target).predict(Xm)
        y_cv = cross_val_predict(LinearRegression(), Xm, target, cv=LeaveOneOut())
        if log:
            y_pred = np.exp(y_pred)
            y_cv = np.exp(y_cv)

        p = Xm.shape[1] + 1
        bic.append(n * np.log(np.mean((y_pred - y) ** 2)) + np.log(n) * p)
        loo.append(np.mean((y_cv - y) ** 2))

bic = np.array(bic)
loo = np.array(loo)
best_bic = np.argmin(bic)
best_loo = np.argmin(loo)

# best is model 4 (log-linear with interactions)
best = LinearRegression().fit(X2, np.log(y))
best_coef = np.append(best.intercept_, best.coef_)
