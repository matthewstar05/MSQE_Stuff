"""
ECON 5015: Linear Model Selection Assignment
Matthew Suban
@matthewsuban
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold, cross_val_predict

boston = pd.read_csv("http://ashafran.github.io/boston.csv")
y = boston["MEDV"]
X = boston.drop(columns="MEDV")
n = len(y)

X1 = X
X2 = pd.DataFrame(PolynomialFeatures(degree=2, include_bias=False, interaction_only=True).fit_transform(X))
X3 = pd.DataFrame(PolynomialFeatures(degree=2, include_bias=False).fit_transform(X))

kf = KFold(n_splits=10, shuffle=True, random_state=0)

kfold = []
best_X = []
best_target = []
best_cols = []
for log in [False, True]:
    for Xm in [X1, X2, X3]:
        target = y
        if log:
            target = np.log(y)

        # forward stepwise: M_0 has no predictors, M_k adds the predictor with the lowest training MSE
        p = Xm.shape[1]
        selected = []
        models = [selected]
        for k in range(p):
            candidates = []
            mse = []
            for j in range(p):
                if j not in selected:
                    cols = selected + [j]
                    y_pred = LinearRegression().fit(Xm.iloc[:, cols], target).predict(Xm.iloc[:, cols])
                    candidates.append(j)
                    mse.append(np.mean((y_pred - target) ** 2))
            selected = selected + [candidates[np.argmin(mse)]]
            models.append(selected)

        # 10-fold CV to choose among M_0, M_1, ..., M_p
        cv_mse = []
        for cols in models:
            X_sub = Xm.iloc[:, cols]
            if len(cols) == 0:
                X_sub = pd.DataFrame(np.ones(n)) # intercept only
            y_cv = cross_val_predict(LinearRegression(), X_sub, target, cv=kf)
            if log:
                y_cv = np.exp(y_cv)
            cv_mse.append(np.mean((y_cv - y) ** 2))

        kfold.append(np.min(cv_mse))
        best_X.append(Xm)
        best_target.append(target)
        best_cols.append(models[np.argmin(cv_mse)])

kfold = np.array(kfold)
best = np.argmin(kfold)

# refit the best model on the full data, predictors in their original order
cols = np.sort(best_cols[best])
if len(cols) == 0:
    best_coef = np.array([np.mean(best_target[best])])
else:
    model = LinearRegression().fit(best_X[best].iloc[:, cols], best_target[best])
    best_coef = np.append(model.intercept_, model.coef_)
