# ECON 5021 Unit 2 Data Analysis: Practice A (free response) - exam 26101200002
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




# 2. Given the information above.
# How many missing values or NA's are there for the variable fatheduc in the dataset?




# 3. Given the information above.
# Consider the following linear regression model.
#     bwght = b0 + b1(cigs) + b2(faminc) + b3(faminc^2) + b4(parity) +
#     b5(motheduc) + b6(fatheduc) + b7(male) + b8(white) + e
# The model includes the number of cigarettes smoked per day by the mother during pregnancy
# (cigs), family income and family income squared, and the birth order of the child (parity).
# The model also controls for the education of the mother and father. Finally, (male, white),
# indicator variables for the sex and race of the child are included in the model.
# Estimate the model above with OLS. What is the estimated coefficient on cigs?




# 4. Given the information above.
# What is the sum of squared errors of the model?




# 5. Given the information above.
# Suppose we wanted to create a confidence interval for one of the parameters of the model. If
# we wanted to create a 99% confidence interval, what critical value would we use?




# 6. Given the information above.
# Consider the null hypothesis that H0: b_male = 0. What is the strongest conclusion we can
# draw about this null hypothesis?




# 7. Given the information above.
# Consider the null hypothesis that H0: b_cigs = -0.5. What is the p-value associated with
# this hypothesis test?




# 8. Given the information above.
# What is the covariance between the estimate of the parameter on (Intercept) and the
# parameter on white?




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




# 10. Given the information above.
# Estimate a linear probability model on 401(k) eligibility e401k.
# Include in your model controls for young, annual family income in $1000s (inc), and
# indicators for whether the worker is male (male) and married (marr). Your model should have
# 5 parameters including the intercept.
# What is the R-squared from the estimated model?




# 11. Given the information above.
# What is the correct interpretation of the parameter on young? Holding fixed the variables in
# the model, being younger than 35 changes the probability of being eligible for a 401(k) by
# ...




# 12. Given the information above.
# What is the estimate of the upper bound of the 99% confidence interval for the parameter on
# marr?




# 13. Given the information above.
# Consider the null hypothesis that H0: b_marr = 0. What is the strongest conclusion we can
# draw about this null hypothesis?




# 14. Given the information above.
# Re-estimate the model adding family size (fsize) as an additional control. What is the
# percentage change in the parameter on marr when we control for family size?




# 15. Given the information above.
# Re-estimate the model adding family size (fsize) as an additional control. What is the
# variance inflation factor for the parameter on marr when we control for family size? (note:
# if you are calculating the variance inflation factor from the formula you need to ensure
# that the same observations are used in the different regressions)



