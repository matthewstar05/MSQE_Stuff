# ECON 5021 Unit 2 Data Analysis: Practice A (multiple choice) - exam 26101200002
# 15 questions. Type each commented code block on the blank lines under it,
# then write the code that answers each question. Key: practice_solutions_A.r

# 1. This is the start of a multipart question. The information below pertains to question 1 to question 8.
# The data set bwght contains data on births in the US from the 1988 National Health Interview
# Survey. You can load the data into R using the wooldridge library using:
#
# library(wooldridge)
# dat = wooldridge::bwght









# The main outcome of interest is the variable bwght, which is the birth weight of the child
# in ounces.
# What is the mean of the variable bwght in the dataset?
# a. 120.0000   b. 118.6996   c. 116.9325   d. 119.5121   e. None of the above




# 2. Given the information above.
# How many missing values or NA's are there for the variable fatheduc in the dataset?
# a. 0   b. 1   c. 196   d. 197   e. None of the above




# 3. Given the information above.
# Consider the following linear regression model.
#     bwght = b0 + b1(cigs) + b2(faminc) + b3(faminc^2) + b4(parity) +
#     b5(motheduc) + b6(fatheduc) + b7(male) + b8(white) + e
# The model includes the number of cigarettes smoked per day by the mother during pregnancy
# (cigs), family income and family income squared, and the birth order of the child (parity).
# The model also controls for the education of the mother and father. Finally, (male, white),
# indicator variables for the sex and race of the child are included in the model.
# Estimate the model above with OLS. What is the estimated coefficient on cigs?
# a. -0.4634   b. -0.5950   c. -0.5137   d. -0.6211   e. -0.4772




# 4. Given the information above.
# What is the sum of squared errors of the model?
# a. 461992.3   b. 13340.2   c. 390114.8   d. 511023.7   e. None of the above




# 5. Given the information above.
# Suppose we wanted to create a confidence interval for one of the parameters of the model. If
# we wanted to create a 99% confidence interval, what critical value would we use?
# a. 2.5758   b. 2.3295   c. 2.5800   d. 1.9620   e. None of the above




# 6. Given the information above.
# Consider the null hypothesis that H0: b_male = 0. What is the strongest conclusion we can
# draw about this null hypothesis?
# a. Reject the null at the 0.1% level
# b. Reject the null at the 1% level
# c. Reject the null at the 5% level
# d. Reject the null at the 10% level
# e. Fail to reject the null at the 10% level




# 7. Given the information above.
# Consider the null hypothesis that H0: b_cigs = -0.5. What is the p-value associated with
# this hypothesis test?
# a. 0.1935   b. 0.3871   c. 0.6129   d. 0.0000   e. None of the above




# 8. Given the information above.
# What is the covariance between the estimate of the parameter on (Intercept) and the
# parameter on white?
# a. -0.9241   b. 2.6122   c. -1.6775   d. 1.6775   e. -0.0017




# 9. This is the start of a multipart question. The information below pertains to question 9 to question 15.
# The data set k401ksubs contains data on workers from the 1991 Survey of Income and Program
# Participation. You can load the data into R using the wooldridge library using:
#
# library(wooldridge)
# dat = wooldridge::k401ksubs









# The variable of interest is e401k which indicates if the worker is eligible for a 401(k)
# plan through their employer. We would like to study what are the main determinants of 401(k)
# eligibility using a linear probability model. To answer this question you will need to add a
# new variable to the data set called young which should equal 1 if the worker is younger than
# 35 (i.e., age <35) and zero otherwise.
# What percent of the population are young?
# a. 28.42%   b. 68.31%   c. 35.11%   d. 31.69%   e. None of the above




# 10. Given the information above.
# Estimate a linear probability model on 401(k) eligibility e401k.
# Include in your model controls for young, annual family income in $1000s (inc), and
# indicators for whether the worker is male (male) and married (marr). Your model should have
# 5 parameters including the intercept.
# What is the R-squared from the estimated model?
# a. 0.07355   b. 0.07394   c. 0.06112   d. 0.08227   e. 0.05930




# 11. Given the information above.
# What is the correct interpretation of the parameter on young? Holding fixed the variables in
# the model, being younger than 35 changes the probability of being eligible for a 401(k) by
# ...
# a. -4.0627 percent
# b. -0.0406 percentage points
# c. -4.0627 percentage points
# d. -0.4063 percentage points
# e. None of the above




# 12. Given the information above.
# What is the estimate of the upper bound of the 99% confidence interval for the parameter on
# marr?
# a. -0.0015   b. -0.0543   c. 0.0092   d. 0.0057   e. None of the above




# 13. Given the information above.
# Consider the null hypothesis that H0: b_marr = 0. What is the strongest conclusion we can
# draw about this null hypothesis?
# a. Reject the null at the 0.1% level
# b. Reject the null at the 1% level
# c. Reject the null at the 5% level
# d. Reject the null at the 10% level
# e. Fail to reject the null at the 10% level




# 14. Given the information above.
# Re-estimate the model adding family size (fsize) as an additional control. What is the
# percentage change in the parameter on marr when we control for family size?
# a. -41.27%   b. 41.27%   c. -29.12%   d. -70.27%   e. None of the above




# 15. Given the information above.
# Re-estimate the model adding family size (fsize) as an additional control. What is the
# variance inflation factor for the parameter on marr when we control for family size? (note:
# if you are calculating the variance inflation factor from the formula you need to ensure
# that the same observations are used in the different regressions)
# a. 1.5284   b. 1.1983   c. 1.8029   d. 0.5547   e. None of the above



