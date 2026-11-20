# Econ 5015 Model Selection Assignment

*For this assignment, you may choose to work alone or work in a group of 2 people. If you work with a partner, please submit only one project with both names included.*

For this assignment, we will use the same Boston housing data as the last assignment. This is data on the Boston housing market from an environmental economics paper published in 1978. The dependent variable for our analysis is the MEDV variable, the median house value in a tract. There are 13 predictors in addition to the MEDV variable.

In this assignment, we will compare the same 6 models as in the previous assignment to predict MEDV based on the other 13 variables. We will use 10-folds CV to choose the best model.

**For each of the six models, you should apply the forward stepwise selection method to choose which predictors to keep in the model and which to exclude.** Note that all of the models this week should perform better than the corresponding models from last week because the selection process includes the possibility of keeping in the full model – thus, any selection will occur only if it improves out-of-sample prediction.

Your scripts should create three variables:

**kfold**: an array with 6 test MSE values for the 6 models using K-fold CV with k=10 (in the same order the models are presented in below, all positively-valued). Set random_state=0 when using KFold.

**best:** an integer between 0 and 5 that identifies the best model using k-fold CV.

**best_coef**: an array of coefficients for the best model. Re-estimate your model using the full data set (use all observations but only the selected predictors) to get coefficients. Include the intercept as the first element in the array, followed by other coefficients (in order based on the original data frame/results of PolynomialFeatures).

Your linear_model_selection.py script should read the boston.csv file from my personal website: <http://ashafran.github.io/boston.csv>. So, you can use the following statement to load the data into a dataframe:

```python
pd.read_csv("http://ashafran.github.io/boston.csv")
```

The linear_model_selection.py script should define the 3 variables described above. I am expecting that you will use sklearn cross validation (specifically, cross_val_predict) to complete this assignment. My test cases will use values generated using cross_val_predict.

## The 6 Models:

Model 0: Linear regression with all 13 predictors.

Model 1: Linear regression with all 13 predictors and all interactions. To do this, you can use the PolynomialFeatues with degree 2 (like in class) but add interaction_only=True so that it does not include squared terms (only includes interactions). I also suggest using include_bias=False so that it does not add the intercept column (this is a little different than in class but has advantage of making your LinearRegression call the same as for Model 1):

```python
PolynomialFeatures(degree = 2, include_bias=False,interaction_only=True)
```

Model 2: Linear regression with all 13 predictors, all interactions, and quadratic term for all predictors. This is similar to Model 2 but without interaction_only=True.

Model 3: Log-linear regression with all 13 predictors. This is like model 1 but perform log transformation of y values (but not X values).

Model 4: Log-linear regression with all 13 predictors and all interactions.

Model 5: Log-linear regression with all 13 predictors, all interactions, and quadratic term for all predictors.

## More Details on Model Selection:

Follow the algorithm in the slides for forward stepwise selection. Use training MSE to select the best k-predictor model (M_k) for all k=0,1,2,…,p. Use 10-folds CV to choose among the chosen models M_0, M_1, M_2, …, M_p.

For all 6 models, calculate the 10-folds CV test MSE using cross_val_predict, as explained in the previous assignment. If y_pred is the array returned by cross_val_predict and y is the unlogged y array, then:

For linear models, `np.mean((y_pred-y)**2)` is the test MSE

For log-linear models, `np.mean((np.exp(y_pred)-y)**2)` is the test MSE
