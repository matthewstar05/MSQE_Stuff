# ECON 5021 Unit 2 Data Analysis: Original practice exam (free response) - exam 26101200001
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




# 2. Given the information above.
# How many missing values or NA's are there for the variable age in the dataset?




# 3. Given the information above.
# Consider the following linear regression model.
#     kids = b0 + b1(educ) + b2(age) + b3(age^2) + b4(year) +
#     b5(east) + b6(northcen) + b7(west) + e
# The model includes controls for education, age and age squared. The model also controls for
# year, which is year. Finally, (east, northcen, west), indicator variables for regional areas
# are included in the model.
# Estimate the model above with OLS. What is the estimated coefficient on education?




# 4. Given the information above.
# What is the sum of squared errors of the model?




# 5. Given the information above.
# Suppose we wanted to create a confidence interval for one of the parameters of the model. If
# we wanted to create a 97.50% confidence interval, what critical value would we use?




# 6. Given the information above.
# Consider the null hypothesis that H0: b_northcen = 0. What is the strongest conclusion we
# can draw about this null hypothesis?




# 7. Given the information above.
# Consider the null hypothesis that H0: b_educ = -0.15. What is the p-value associated with
# this hypothesis test?




# 8. Given the information above.
# What is the covariance between the estimate of the parameter on (Intercept) and the
# parameter on west?




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




# 10. Given the information above.
# Estimate a linear probability model on high school graduation hsgrad.
# Include in your model controls for if the student attended a Catholic high school (cathhs),
# nonwhite, and both the 12th grade reading and math scores. Your model should have 5
# parameters including the intercept.
# What is the R-squared from the estimated model?




# 11. Given the information above.
# What is the correct interpretation of the parameter on cathhs? Holding fixed the variables
# in the model, attending a Catholic high school increases the probability of high school
# graduation by ...




# 12. Given the information above.
# What is the estimate of the lower bound of the 90% confidence interval for the intercept of
# the model?




# 13. Given the information above.
# Consider the null hypothesis that H0: b_math12 = 0. What is the strongest conclusion we can
# draw about this null hypothesis?




# 14. Given the information above.
# Re-estimate the model adding log family income (lfaminc) as an additional control. What is
# the percentage change in the parameter on cathhs when we control for family income?




# 15. Given the information above.
# Re-estimate the model adding log family income (lfaminc) as an additional control. What is
# the variance inflation factor for the parameter on cathhs when we control for family income?
# (note: if you are calculating the variance inflation factor from the formula you need to
# ensure that the same observations are used in the different regressions)



