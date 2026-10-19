# ECON 5021 Unit 2 Data Analysis: Practice B (free response) - exam 26101200003
# 15 questions. Type each commented code block on the blank lines under it,
# then write the code that answers each question. Key: practice_solutions_B.r

# 1. This is the start of a multipart question. The information below pertains to question 1 to question 8.
# The data set wage2 contains data on working men in the US from the 1980 National
# Longitudinal Survey. You can load the data into R using the wooldridge library using:
#
# library(wooldridge)
# dat = wooldridge::wage2









# The main outcome of interest is the variable wage, which is monthly earnings in dollars.
# What is the median of the variable wage in the dataset?




# 2. Given the information above.
# How many missing values or NA's are there for the variable meduc in the dataset?




# 3. Given the information above.
# Consider the following linear regression model.
#     log(wage) = b0 + b1(educ) + b2(exper) + b3(exper^2) + b4(tenure) + b5(married) +
#     b6(black) + b7(south) + b8(urban) + b9(meduc) + e
# The model includes controls for years of education, years of work experience and experience
# squared, and years with the current employer (tenure). The model also controls for mother's
# education (meduc). Finally, (married, black, south, urban) are indicator variables.
# Estimate the model above with OLS. What is the estimated coefficient on educ?




# 4. Given the information above.
# What is the residual standard error (sigma_hat) of the model?




# 5. Given the information above.
# Suppose we wanted to create a confidence interval for one of the parameters of the model. If
# we wanted to create a 98% confidence interval, what critical value would we use?




# 6. Given the information above.
# Consider the null hypothesis that H0: b_south = 0. What is the strongest conclusion we can
# draw about this null hypothesis?




# 7. Given the information above.
# Consider the null hypothesis that H0: b_educ = 0.05. What is the p-value associated with
# this hypothesis test?




# 8. Given the information above.
# What is the covariance between the estimate of the parameter on exper and the parameter on
# exper^2?




# 9. This is the start of a multipart question. The information below pertains to question 9 to question 15.
# The data set crime1 contains data on young men in California who were arrested at least once
# before 1986. You can load the data into R using the wooldridge library using:
#
# library(wooldridge)
# dat = wooldridge::crime1









# We would like to study what are the main determinants of being arrested in 1986 using a
# linear probability model. To answer this question you will need to add a new variable to the
# data set called arrested which should equal 1 if the man was arrested at least once in 1986
# (i.e., narr86 >0) and zero otherwise.
# What percent of the population were arrested?




# 10. Given the information above.
# Estimate a linear probability model on arrested.
# Include in your model controls for the proportion of prior arrests that led to a conviction
# (pcnv), months spent in prison in 1986 (ptime86), the number of quarters employed in 1986
# (qemp86), and black. Your model should have 5 parameters including the intercept.
# What is the adjusted R-squared from the estimated model?




# 11. Given the information above.
# What is the correct interpretation of the parameter on qemp86? Holding fixed the variables
# in the model, one additional quarter of employment changes the probability of being arrested
# by ...




# 12. Given the information above.
# What is the estimate of the lower bound of the 95% confidence interval for the parameter on
# qemp86?




# 13. Given the information above.
# Consider the null hypothesis that H0: b_pcnv = 0. What is the strongest conclusion we can
# draw about this null hypothesis?




# 14. Given the information above.
# Re-estimate the model adding legal income in 1986 (inc86) as an additional control. What is
# the percentage change in the parameter on qemp86 when we control for income?




# 15. Given the information above.
# Re-estimate the model adding legal income in 1986 (inc86) as an additional control. What is
# the variance inflation factor for the parameter on qemp86 when we control for income? (note:
# if you are calculating the variance inflation factor from the formula you need to ensure
# that the same observations are used in the different regressions)



