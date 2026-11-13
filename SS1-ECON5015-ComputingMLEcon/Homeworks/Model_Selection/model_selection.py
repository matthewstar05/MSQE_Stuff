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
n = len(boston)

X1 = X
X2 = PolynomialFeatures(degree=2, include_bias=False, interaction_only=True).fit_transform(X)
X3 = PolynomialFeatures(degree=2, include_bias=False).fit_transform(X)


def get_bic(X, y, log):
    model = LinearRegression()
    if log:
        model.fit(X, np.log(y))
        y_pred = np.exp(model.predict(X)) # undo the log so we can compare to y
    else:
        model.fit(X, y)
        y_pred = model.predict(X)
    mse = np.mean((y_pred - y) ** 2)
    p = X.shape[1] + 1 # plus the intercept
    return n * np.log(mse) + np.log(n) * p


def get_loo(X, y, log):
    if log:
        y_pred = cross_val_predict(LinearRegression(), X, np.log(y), cv=LeaveOneOut())
        y_pred = np.exp(y_pred)
    else:
        y_pred = cross_val_predict(LinearRegression(), X, y, cv=LeaveOneOut())
    return np.mean((y_pred - y) ** 2)


bic = np.array([get_bic(X1, y, False), get_bic(X2, y, False), get_bic(X3, y, False),
                get_bic(X1, y, True), get_bic(X2, y, True), get_bic(X3, y, True)])

loo = np.array([get_loo(X1, y, False), get_loo(X2, y, False), get_loo(X3, y, False),
                get_loo(X1, y, True), get_loo(X2, y, True), get_loo(X3, y, True)])

best_bic = np.argmin(bic)
best_loo = np.argmin(loo)

# best LOOCV model is model 4 (log-linear with interactions), refit on all the data
best_model = LinearRegression()
best_model.fit(X2, np.log(y))
best_coef = np.append(best_model.intercept_, best_model.coef_)
