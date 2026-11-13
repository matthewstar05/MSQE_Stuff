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
X = boston.drop(columns="MEDV") # the 13 predictors
n = len(boston)

X_lin = X.values
X_int = PolynomialFeatures(degree=2, include_bias=False, interaction_only=True).fit_transform(X) # + interactions
X_quad = PolynomialFeatures(degree=2, include_bias=False).fit_transform(X) # + interactions and squares

# (X, logged y?) for models 0-5
models = [(X_lin, False), (X_int, False), (X_quad, False),
          (X_lin, True), (X_int, True), (X_quad, True)]

bic = np.zeros(6)
loo = np.zeros(6)
for i, (Xm, logy) in enumerate(models):
    yt = np.log(y) if logy else y # log-linear models fit log(y)

    # BIC from the full-sample fit
    y_pred = LinearRegression().fit(Xm, yt).predict(Xm)
    if logy:
        y_pred = np.exp(y_pred) # back to MEDV units so MSE compares to y
    mse = np.mean((y_pred - y) ** 2)
    p = Xm.shape[1] + 1 # predictors + intercept
    bic[i] = n * np.log(mse) + np.log(n) * p

    # LOOCV test MSE from the held-out predictions
    y_cv = cross_val_predict(LinearRegression(), Xm, yt, cv=LeaveOneOut())
    if logy:
        y_cv = np.exp(y_cv)
    loo[i] = np.mean((y_cv - y) ** 2)

best_bic = int(np.argmin(bic))
best_loo = int(np.argmin(loo))

# re-estimate the LOOCV winner on the full data, intercept first
Xb, logb = models[best_loo]
best_model = LinearRegression().fit(Xb, np.log(y) if logb else y)
best_coef = np.concatenate(([best_model.intercept_], best_model.coef_))
