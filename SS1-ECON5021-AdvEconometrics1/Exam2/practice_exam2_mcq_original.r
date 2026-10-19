# ECON 5021 Unit 2 Data Analysis: Original practice exam (multiple choice) - exam 26101200001
# 15 questions. Type each commented code block on the blank lines under it,
# then write the code that answers each question. Key: practice_solutions_original.r

# 1. This is the start of a multipart question. The information below pertains to question 1 to question 8.
# The data set fertil1 contains data from women in the US between the ages of 35 and 54. You
# can load the data into R using the wooldridge library using:
#
# library(wooldridge)
# dat = wooldridge::fertil1









# The main outcome of interest is the variable kids, which is the number of children the women
# has given birth to.
# What is the mean of the variable kids in the dataset?
# a. 2.7431   b. 1.8002   c. 3.8678   d. 2.5798   e. None of the above




# 2. Given the information above.
# How many missing values or NA's are there for the variable age in the dataset?
# a. 0   b. 265   c. 20   d. 33   e. None of the above




# 3. Given the information above.
# Consider the following linear regression model.
#     kids = b0 + b1(educ) + b2(age) + b3(age^2) + b4(year) +
#     b5(east) + b6(northcen) + b7(west) + e
# The model includes controls for education, age and age squared. The model also controls for
# year, which is year. Finally, (east, northcen, west), indicator variables for regional areas
# are included in the model.
# Estimate the model above with OLS. What is the estimated coefficient on education?
# a. -0.06932   b. -0.13712   c. -0.15261   d. -0.17425   e. -0.12260




# 4. Given the information above.
# What is the sum of squared errors of the model?
# a. 6632.205   b. 2809.876   c. 5223.497   d. 861.390   e. None of the above




# 5. Given the information above.
# Suppose we wanted to create a confidence interval for one of the parameters of the model. If
# we wanted to create a 97.50% confidence interval, what critical value would we use?
# a. 2.4559   b. 3.1180   c. 2.2444   d. 2.2664   e. None of the above




# 6. Given the information above.
# Consider the null hypothesis that H0: b_northcen = 0. What is the strongest conclusion we
# can draw about this null hypothesis?
# a. Reject the null at the 0.1% level
# b. Reject the null at the 1% level
# c. Reject the null at the 5% level
# d. Reject the null at the 10% level
# e. Fail to reject the null at the 10% level




# 7. Given the information above.
# Consider the null hypothesis that H0: b_educ = -0.15. What is the p-value associated with
# this hypothesis test?
# a. 0.1998   b. 0.1639   c. 0.1882   d. 0.1510   e. None of the above




# 8. Given the information above.
# What is the covariance between the estimate of the parameter on (Intercept) and the
# parameter on west?
# a. -0.03627   b. -0.04409   c. -0.04026   d. -0.02994   e. -0.02254




# 9. This is the start of a multipart question. The information below pertains to question 9 to question 15.
# The data set catholic contains data on students that have recently left high school. You can
# load the data into R using the wooldridge library using:
#
# library(wooldridge)
# dat = wooldridge::catholic









# The variable of interest is hsgrad which indicates if the student graduated high school. We
# would like to study what are the main determinants of high school graduation using a linear
# probability model. To answer this question you will need to add a new variable to the data
# set called nonwhite which should equal 1 if the student is non-white (i.e., asian, hispanic,
# or black) and zero otherwise.
# What percent of the population are nonwhite?
# a. 16.48%   b. 22.58%   c. 16.18%   d. 15.43%   e. None of the above




# 10. Given the information above.
# Estimate a linear probability model on high school graduation hsgrad.
# Include in your model controls for if the student attended a Catholic high school (cathhs),
# nonwhite, and both the 12th grade reading and math scores. Your model should have 5
# parameters including the intercept.
# What is the R-squared from the estimated model?
# a. 0.03834   b. 0.04439   c. 0.04080   d. 0.07493   e. 0.05675




# 11. Given the information above.
# What is the correct interpretation of the parameter on cathhs? Holding fixed the variables
# in the model, attending a Catholic high school increases the probability of high school
# graduation by ...
# a. 3.0198 percent
# b. 0.3020 percent
# c. 3.0198 percentage points
# d. 0.0302 percent
# e. None of the above




# 12. Given the information above.
# What is the estimate of the lower bound of the 90% confidence interval for the intercept of
# the model?
# a. 0.3342   b. 0.2780   c. 0.4815   d. 0.5120   e. None of the above




# 13. Given the information above.
# Consider the null hypothesis that H0: b_math12 = 0. What is the strongest conclusion we can
# draw about this null hypothesis?
# a. Reject the null at the 0.1% level
# b. Reject the null at the 1% level
# c. Reject the null at the 5% level
# d. Reject the null at the 10% level
# e. Fail to reject the null at the 10% level




# 14. Given the information above.
# Re-estimate the model adding log family income (lfaminc) as an additional control. What is
# the percentage change in the parameter on cathhs when we control for family income?
# a. -53.62%   b. -51.42%   c. 47.80%   d. -54.01%   e. None of the above




# 15. Given the information above.
# Re-estimate the model adding log family income (lfaminc) as an additional control. What is
# the variance inflation factor for the parameter on cathhs when we control for family income?
# (note: if you are calculating the variance inflation factor from the formula you need to
# ensure that the same observations are used in the different regressions)
# a. 1.0249   b. 1.2479   c. 1.2946   d. 0.9104   e. None of the above



