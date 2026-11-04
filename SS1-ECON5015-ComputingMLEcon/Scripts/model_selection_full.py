# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 14:17:09 2020

@author: aric
"""
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from scipy.stats import chi2
from sklearn.model_selection import train_test_split
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import KFold
from sklearn.model_selection import GroupKFold
from sklearn.model_selection import GroupShuffleSplit
from sklearn.model_selection import cross_val_score

# Chaper 5 Lab: Cross-Validation (and Model Selection)
Auto=pd.read_csv("Auto.csv")

#compare 3 models, linear, quadratic, and cubic - how does horsepower affect gas mileage?

#linear model  (3 parameters, coefficient, intercept, variance)
model1_sm=smf.ols("mpg ~ horsepower",data=Auto).fit()
model1_sm.summary()
1178.7*2+2*2

y=Auto.mpg
X=pd.DataFrame(Auto.horsepower)
model1=LinearRegression()   #class in sklean for linear regression
model1.fit(X,y)   #fit method is used to estimate the model using data X (explantory variables) and y (dependent variable)
model1.coef_
model1.intercept_

y_pred=model1.predict(X)    #predict method used to generate predictions for y given X (does not have to be same X used to fit the model)
mse1=mean_squared_error(y,y_pred)  #calculate mean squared error given y and y-hat
np.mean((y-y_pred)**2)


#quadratic model (3 parameters)
yp = Auto.mpg
poly = PolynomialFeatures(degree = 2)  
Xp = pd.DataFrame(poly.fit_transform(X))  #Xp includes X^0, X^1, X^2  (and would include interactions if we had more than one variable in X)

model2=LinearRegression(fit_intercept=False)  #fir_intercept=false since Xp already includes the intercept (column of 1's)
model2.fit(Xp,yp)
model2.coef_

yp_pred=model2.predict(Xp)
mse2=mean_squared_error(yp,yp_pred)



#cubic model  (4 parameters)
yc = Auto.mpg
poly = PolynomialFeatures(degree = 3)
Xc = pd.DataFrame(poly.fit_transform(X))

model3=LinearRegression(fit_intercept=False)
model3.fit(Xc,yc)
model3.coef_

yc_pred=model3.predict(Xc)
mse3=mean_squared_error(yc,yc_pred)


#LR Tests  calc p-value
lrtest_1v2=chi2.sf(len(Auto)*np.log(mse1)-len(Auto)*np.log(mse2),1)  #reject
lrtest_2v3=chi2.sf(len(Auto)*np.log(mse2)-len(Auto)*np.log(mse3),1)   #do not reject
lrtest_1v3=chi2.sf(len(Auto)*np.log(mse1)-len(Auto)*np.log(mse3),2)   #reject


#AIC, smaller = better
aic1 = len(Auto)*np.log(mse1)+2*2
aic2 = len(Auto)*np.log(mse2)+2*3
aic3 = len(Auto)*np.log(mse3)+2*4

#BIC, smaller = better
bic1 = len(Auto)*np.log(mse1)+2*np.log(len(Auto))
bic2 = len(Auto)*np.log(mse2)+3*np.log(len(Auto))
bic3 = len(Auto)*np.log(mse3)+4*np.log(len(Auto))

# The Validation Set Approach
n = len(Auto)

#compute test MSE for linear model
y=Auto.mpg
X=pd.DataFrame(Auto.horsepower)
Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,train_size=0.5,random_state=0)  #could also use np.random.sample to divide data into training and test sets
model1=LinearRegression()
model1.fit(Xtrain,ytrain)
ytest_pred=model1.predict(Xtest)  #note we are generating predictions for Xtest but we trained the model with Xtrain
testmse1=mean_squared_error(ytest,ytest_pred)

#compute test MSE for quadratic model
y=Auto.mpg
X= pd.DataFrame(PolynomialFeatures(degree = 2).fit_transform(pd.DataFrame(Auto.horsepower)))
Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,train_size=0.5,random_state=0)
model2=LinearRegression(fit_intercept=False)
model2.fit(Xtrain,ytrain)
ytest_pred=model2.predict(Xtest)
testmse2=mean_squared_error(ytest,ytest_pred)

#compute test MSE for cubic model
y=Auto.mpg
X= pd.DataFrame(PolynomialFeatures(degree = 3).fit_transform(pd.DataFrame(Auto.horsepower)))
Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,train_size=0.5,random_state=0)
model3=LinearRegression(fit_intercept=False)
model3.fit(Xtrain,ytrain)
ytest_pred=model3.predict(Xtest)
testmse3=mean_squared_error(ytest,ytest_pred)


#How sensitive are results to chosen training set?  Re-do with different random seed
y=Auto.mpg
X=pd.DataFrame(Auto.horsepower)
Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,train_size=0.5,random_state=1)
model1=LinearRegression()
model1.fit(Xtrain,ytrain)
ytest_pred=model1.predict(Xtest)
testmse1=mean_squared_error(ytest,ytest_pred)

y=Auto.mpg
X= pd.DataFrame(PolynomialFeatures(degree = 2).fit_transform(pd.DataFrame(Auto.horsepower)))
Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,train_size=0.5,random_state=1)  
model2=LinearRegression(fit_intercept=False)
model2.fit(Xtrain,ytrain)
ytest_pred=model2.predict(Xtest)
testmse2=mean_squared_error(ytest,ytest_pred)

y=Auto.mpg
X= pd.DataFrame(PolynomialFeatures(degree = 3).fit_transform(pd.DataFrame(Auto.horsepower)))
Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,train_size=0.5,random_state=1)
model3=LinearRegression(fit_intercept=False)
model3.fit(Xtrain,ytrain)
ytest_pred=model3.predict(Xtest)
testmse3=mean_squared_error(ytest,ytest_pred)

# Leave-One-Out Cross-Validation
y=Auto.mpg
X=pd.DataFrame(Auto.horsepower)

#LOOCV manually
loomse1=0
for i in range(n):
  train = np.delete(np.arange(n),i)
  Xtrain=X.iloc[train,:]
  ytrain=y[train]
  model1=LinearRegression()
  model1.fit(Xtrain,ytrain)
  ytest_pred=model1.predict(X.iloc[[i]])[0]
  loomse1=loomse1+(y[i]-ytest_pred)**2

loomse1=loomse1/n

#LOOCV using cross_val_score method
loo1_scores=cross_val_score(LinearRegression(),X,y,cv=LeaveOneOut(),scoring="neg_mean_squared_error")
loo1=np.mean(loo1_scores)

#Re-do both ways for quadratic
y=Auto.mpg
X= pd.DataFrame(PolynomialFeatures(degree = 2).fit_transform(pd.DataFrame(Auto.horsepower)))
loomse2=0
for i in range(n):
  train = np.delete(np.arange(n),i)
  Xtrain=X.iloc[train,:]
  ytrain=y[train]
  model2=LinearRegression(fit_intercept=False)
  model2.fit(Xtrain,ytrain)
  ytest_pred=model2.predict(X.iloc[[i]])[0]
  loomse2=loomse2+(y[i]-ytest_pred)**2

loomse2=loomse2/n

loo2_scores=cross_val_score(LinearRegression(fit_intercept=False),X,y,cv=LeaveOneOut(),scoring="neg_mean_squared_error")
loo2=np.mean(loo2_scores)

#Re-do both ways for cubic
y=Auto.mpg
X= pd.DataFrame(PolynomialFeatures(degree = 3).fit_transform(pd.DataFrame(Auto.horsepower)))
loomse3=0
for i in range(n):
  train = np.delete(np.arange(n),i)
  Xtrain=X.iloc[train,:]
  ytrain=y[train]
  model3=LinearRegression(fit_intercept=False)
  model3.fit(Xtrain,ytrain)
  ytest_pred=model3.predict(X.iloc[[i]])[0]
  loomse3=loomse3+(y[i]-ytest_pred)**2

loomse3=loomse3/n

loo3_scores=cross_val_score(LinearRegression(),X,y,cv=LeaveOneOut(),scoring="neg_mean_squared_error")
loo3=np.mean(loo3_scores)

# k-Fold Cross-Validation, k=5
k=5
y=Auto.mpg
X=pd.DataFrame(Auto.horsepower)

#k-Fold done manually
n=len(Auto)
np.random.seed(0)
kfold=np.random.choice(np.arange(k),n)
msek1=0
for i in range(k):
    Xtrain=X.iloc[kfold!=i,:]
    ytrain=y[kfold!=i]
    model1=LinearRegression()
    model1.fit(Xtrain,ytrain)
    ytest_pred=model1.predict(X.iloc[kfold==i,:])
    msek1=msek1+np.mean((y[kfold==i]-ytest_pred)**2)

msek1=msek1/k

#k-fold using cross_val_score
scores=cross_val_score(LinearRegression(),X,y,cv=KFold(k,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
mseksk1=np.mean(scores)


#Re-do both ways for quadratic
y=Auto.mpg
X= pd.DataFrame(PolynomialFeatures(degree = 2).fit_transform(pd.DataFrame(Auto.horsepower)))
n=len(Auto)
np.random.seed(0)
kfold=np.random.choice(np.arange(k),n)
msek2=0
for i in range(k):
    Xtrain=X.iloc[kfold!=i,:]
    ytrain=y[kfold!=i]
    model2=LinearRegression(fit_intercept=False)
    model2.fit(Xtrain,ytrain)
    ytest_pred=model2.predict(X.iloc[kfold==i,:])
    msek2=msek2+np.mean((y[kfold==i]-ytest_pred)**2)

msek2=msek2/k

scores=cross_val_score(LinearRegression(fit_intercept=False),X,y,cv=KFold(k,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
mseksk2=np.mean(scores)

#Re-do both ways for cubic
y=Auto.mpg
X= pd.DataFrame(PolynomialFeatures(degree = 3).fit_transform(pd.DataFrame(Auto.horsepower)))
n=len(Auto)
np.random.seed(0)
kfold=np.random.choice(np.arange(k),n)
msek3=0
for i in range(k):
    Xtrain=X.iloc[kfold!=i,:]
    ytrain=y[kfold!=i]
    model3=LinearRegression(fit_intercept=False)
    model3.fit(Xtrain,ytrain)
    ytest_pred=model3.predict(X.iloc[kfold==i,:])
    msek3=msek3+np.mean((y[kfold==i]-ytest_pred)**2)

msek3=msek3/k

scores=cross_val_score(LinearRegression(fit_intercept=False),X,y,cv=KFold(k,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
mseksk3=np.mean(scores)


#cross validation with panel data
f=pd.read_csv("f.csv")
model=LinearRegression()
y=f["ins"]
X=f[["mit1","mit2","mit3"]]
model.fit(X,y)
model.coef_

y_pred=model.predict(X)
training_mse=mean_squared_error(y,y_pred)

#GroupKFold divides data into k folds and uses (k-1) folds for training and the k-th fold for testing
#Folds are based on "id" rather than individual rows, so all data for a given "id" is put in the same fold
#For some reason, it does not have a random seed to randomize how ids are assigned to folds
scores=cross_val_score(LinearRegression(),X,y,cv=GroupKFold(n_splits=5),groups=f.id,scoring="neg_mean_squared_error")
panelmse=np.mean(scores)

#GroupShuffleSplit also creates folds by "id" so that all observations for an "id" are in same fold
#It differs from GroupKFold because it draws each train/test split randomly and independently
#This means some id's could appear in multiple test folds and others may never appear in test folds
scores=cross_val_score(LinearRegression(),X,y,cv=GroupShuffleSplit(n_splits=5,test_size=0.2,random_state=0),groups=f.id,scoring="neg_mean_squared_error")
panelmse2=np.mean(scores)

#print id's for test samples 
print(pd.unique(f.id))
g=GroupKFold(n_splits=5)
for i,j in g.split(X,y,f.id):
    print(pd.unique(f.id[j]))
    
g=GroupShuffleSplit(n_splits=5,test_size=0.2,random_state=2)
for i,j in g.split(X,y,f.id):
    print(pd.unique(f.id[j]))

