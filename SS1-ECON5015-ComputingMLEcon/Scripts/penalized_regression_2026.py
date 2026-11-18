# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:25:55 2020

@author: aric
"""
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.model_selection import LeaveOneOut
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import LassoCV
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

import numpy as np
import pandas as pd

Hitters=pd.read_csv("Hitters.csv")

y=Hitters.Salary
Hitters.League=Hitters.League=="N"
Hitters.Division=Hitters.Division=="W"
Hitters.NewLeague=Hitters.NewLeague=="N"
X=Hitters.iloc[:,np.append(np.arange(1,19),20)]


linear_model=LinearRegression()
linear_model.fit(X,y)
coef=linear_model.coef_
np.sqrt(np.sum(coef**2))

#OLS scaled
scaler=StandardScaler()
scaled_x=scaler.fit_transform(X)
linear_model=LinearRegression()
linear_model.fit(scaled_x,y)
coef=linear_model.coef_
np.sqrt(np.sum(coef**2))

#same as above  (alpha=0)
ridge_model=Ridge(alpha=0)
ridge_model.fit(scaled_x,y)
ridge_model.coef_
np.sqrt(np.sum(ridge_model.coef_**2))

# Ridge Regression
#scaler=StandardScaler()
#scaled_x=scaler.fit_transform(X)
ridge_model=Ridge(alpha=0.01)
ridge_model.fit(scaled_x,y)
ridge_model.coef_
np.sqrt(np.sum(ridge_model.coef_**2))

scaler=StandardScaler()
scaled_x=scaler.fit_transform(X)
ridge_model=Ridge(alpha=1)
ridge_model.fit(scaled_x,y)
ridge_model.coef_
np.sqrt(np.sum(ridge_model.coef_**2))

scaler=StandardScaler()
scaled_x=scaler.fit_transform(X)
ridge_model=Ridge(alpha=100)
ridge_model.fit(scaled_x,y)
ridge_model.coef_
np.sqrt(np.sum(ridge_model.coef_**2))



#LOO
n=len(y)
grid=10**np.linspace(-2,8,100)
mse=np.empty((n,100))
for i in range(n):

    
    train=np.delete(np.arange(n),i)
    Xtrain=X.iloc[train,:]
    ytrain=y[train]
    scaler=StandardScaler()
    scaled_x=scaler.fit_transform(Xtrain)
    scaled_xtest=scaler.transform(X.iloc[[i]])
    
    for j in range(len(grid)):
        model1=Ridge(alpha=grid[j])
        model1.fit(scaled_x,ytrain)
        ridge_pred=model1.predict(scaled_xtest)
        mse[i,j] = np.mean((ridge_pred-y[i])**2)

   
grid[np.argmin(np.mean(mse,axis=0))]



pipe_ridge=Pipeline([
        ("scale", StandardScaler()),
        ("ridge", Ridge())
    ])

#parameter name in grid below is stepname__paramname
grid={"ridge__alpha": 10**np.linspace(-2,8,100)}
grid_ridge = GridSearchCV(pipe_ridge, grid, cv = LeaveOneOut(), scoring="neg_mean_squared_error")
grid_ridge.fit(X, y)
best_ridge = grid_ridge.best_params_["ridge__alpha"]

#efficient method of doing leaveoneout but scales based on all data, insteads of rescaling for each training set
scaler=StandardScaler()
scaled_x=scaler.fit_transform(X)
ridge = RidgeCV(alphas=10**np.linspace(-2,8,100),scoring="neg_mean_squared_error")
ridge.fit(scaled_x, y)
ridge.alpha_

#re-estimate best model
pipe_ridge=Pipeline([
        ("scale", StandardScaler()),
        ("ridge", Ridge(alpha=best_ridge))
    ])
pipe_ridge.fit(X,y)


#Lasso
scaler=StandardScaler()
scaled_x=scaler.fit_transform(X)
lasso_model=Lasso(alpha=0.01,max_iter=100000)
lasso_model.fit(scaled_x,y)
lasso_model.coef_
np.sqrt(np.sum(lasso_model.coef_**2))

lasso_model=Lasso(alpha=1,max_iter=100000)
lasso_model.fit(scaled_x,y)
lasso_model.coef_
np.sqrt(np.sum(lasso_model.coef_**2))

lasso_model=Lasso(alpha=10,max_iter=10000)
lasso_model.fit(scaled_x,y)
lasso_model.coef_
np.sqrt(np.sum(lasso_model.coef_**2))



pipe_lasso=Pipeline([
        ("scale", StandardScaler()),
        ("lasso", Lasso(max_iter=100000))
    ])

#parameter name in grid below is stepname__paramname
grid={"lasso__alpha": 10**np.linspace(-2,8,100)}
grid_lasso = GridSearchCV(pipe_lasso, grid, cv = LeaveOneOut(), scoring="neg_mean_squared_error")
grid_lasso.fit(X, y)
best_lasso = grid_lasso.best_params_["lasso__alpha"]


pipe_lasso=Pipeline([
        ("scale", StandardScaler()),
        ("lasso", Lasso(alpha=best_lasso,max_iter=100000))
    ])


#comparing OLS, Ridge, Lasso
scores=cross_val_score(LinearRegression(),X,y,cv=KFold(10,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
mselinear=np.mean(scores)
scores=cross_val_score(pipe_ridge,X,y,cv=KFold(10,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
mseridge=np.mean(scores)
scores=cross_val_score(pipe_lasso,X,y,cv=KFold(10,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
mselasso=np.mean(scores)

