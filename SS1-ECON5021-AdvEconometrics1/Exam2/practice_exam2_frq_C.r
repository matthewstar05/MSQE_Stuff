# ECON 5021 Unit 2 Data Analysis: Practice C (free response) - exam 26101200004
# 15 questions. Type each commented code block on the blank lines under it,
# then write the code that answers each question. Key: practice_solutions_C.r

# 1. This is the start of a multipart question. The information below pertains to question 1 to question 8.
# The data set card contains data on young men in the US from the 1976 National Longitudinal
# Survey of Young Men. You can load the data into R using the wooldridge library using:
#
# library(wooldridge)
# dat = wooldridge::card









# The main outcome of interest is the variable lwage, which is the log of the hourly wage.
# What is the mean of the variable lwage in the dataset?




# 2. Given the information above.
# How many missing values or NA's are there for the variable IQ in the dataset?




# 3. Given the information above.
# Consider the following linear regression model.
#     lwage = b0 + b1(educ) + b2(exper) + b3(exper^2) + b4(black) +
#     b5(smsa) + b6(south) + b7(momdad14) + b8(KWW) + e
# The model includes controls for education, experience and experience squared, and a test
# score on knowledge of the world of work (KWW). Finally, (black, smsa, south, momdad14),
# indicator variables for race, living in a metropolitan area, living in the south, and living
# with both parents at age 14 are included in the model.
# Estimate the model above with OLS. What is the estimated coefficient on education?




# 4. Given the information above.
# What is the sum of squared errors of the model?




# 5. Given the information above.
# Suppose we wanted to create a confidence interval for one of the parameters of the model. If
# we wanted to create a 90% confidence interval, what critical value would we use?




# 6. Given the information above.
# Consider the null hypothesis that H0: b_momdad14 = 0. What is the strongest conclusion we
# can draw about this null hypothesis?




# 7. Given the information above.
# Consider the null hypothesis that H0: b_educ = 0.05. What is the p-value associated with
# this hypothesis test?




# 8. Given the information above.
# What is the covariance between the estimate of the parameter on educ and the parameter on
# KWW?




# 9. This is the start of a multipart question. The information below pertains to question 9 to question 15.
# The data set mroz contains data on married women in the US from the 1975 Panel Study of
# Income Dynamics. You can load the data into R using the wooldridge library using:
#
# library(wooldridge)
# dat = wooldridge::mroz









# We would like to study what are the main determinants of earning a high wage using a linear
# probability model. To answer this question you will need to add a new variable to the data
# set called highwage which should equal 1 if the woman's hourly wage is above $5 (i.e., wage
# >5) and zero otherwise. Women who did not work have a missing wage, so highwage should also
# be missing for them.
# Among women with a reported wage, what percent are highwage?




# 10. Given the information above.
# Estimate a linear probability model on highwage.
# Include in your model controls for years of education (educ), years of work experience
# (exper), age, and an indicator for living in a city (city). Your model should have 5
# parameters including the intercept.
# How many observations are used to estimate the model?




# 11. Given the information above.
# What is the correct interpretation of the parameter on educ? Holding fixed the variables in
# the model, one additional year of education increases the probability of earning a high wage
# by ...




# 12. Given the information above.
# What is the estimate of the lower bound of the 90% confidence interval for the intercept of
# the model?




# 13. Given the information above.
# Consider the null hypothesis that H0: b_city = 0. What is the strongest conclusion we can
# draw about this null hypothesis?




# 14. Given the information above.
# Re-estimate the model adding husband's years of education (huseduc) as an additional
# control. What is the percentage change in the parameter on educ when we control for
# husband's education?




# 15. Given the information above.
# Re-estimate the model adding husband's years of education (huseduc) as an additional
# control. What is the variance inflation factor for the parameter on educ when we control for
# husband's education? (note: if you are calculating the variance inflation factor from the
# formula you need to ensure that the same observations are used in the different regressions)



