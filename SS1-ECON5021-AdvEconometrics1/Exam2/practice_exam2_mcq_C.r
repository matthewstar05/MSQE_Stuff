# ECON 5021 Unit 2 Data Analysis: Practice C (multiple choice) - exam 26101200004
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
# a. 6.2004   b. 6.3520   c. 6.1395   d. 5.9810   e. None of the above




# 2. Given the information above.
# How many missing values or NA's are there for the variable IQ in the dataset?
# a. 47   b. 949   c. 690   d. 0   e. None of the above




# 3. Given the information above.
# Consider the following linear regression model.
#     lwage = b0 + b1(educ) + b2(exper) + b3(exper^2) + b4(black) +
#     b5(smsa) + b6(south) + b7(momdad14) + b8(KWW) + e
# The model includes controls for education, experience and experience squared, and a test
# score on knowledge of the world of work (KWW). Finally, (black, smsa, south, momdad14),
# indicator variables for race, living in a metropolitan area, living in the south, and living
# with both parents at age 14 are included in the model.
# Estimate the model above with OLS. What is the estimated coefficient on education?
# a. 0.05482   b. 0.06213   c. 0.05570   d. 0.04911   e. 0.05823




# 4. Given the information above.
# What is the sum of squared errors of the model?
# a. 392.3281   b. 405.3401   c. 0.3704   d. 410.1124   e. None of the above




# 5. Given the information above.
# Suppose we wanted to create a confidence interval for one of the parameters of the model. If
# we wanted to create a 90% confidence interval, what critical value would we use?
# a. 1.6449   b. 1.2818   c. 1.9608   d. 1.6454   e. None of the above




# 6. Given the information above.
# Consider the null hypothesis that H0: b_momdad14 = 0. What is the strongest conclusion we
# can draw about this null hypothesis?
# a. Reject the null at the 0.1% level
# b. Reject the null at the 1% level
# c. Reject the null at the 5% level
# d. Reject the null at the 10% level
# e. Fail to reject the null at the 10% level




# 7. Given the information above.
# Consider the null hypothesis that H0: b_educ = 0.05. What is the p-value associated with
# this hypothesis test?
# a. 0.0925   b. 0.8150   c. 0.2533   d. 0.1850   e. None of the above




# 8. Given the information above.
# What is the covariance between the estimate of the parameter on educ and the parameter on
# KWW?
# a. 9.3490*10^-6   b. -2.7081*10^-6   c. 2.7081*10^-6   d. -2.6182*10^-6   e. -1.2120*10^-5




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
# a. 13.94%   b. 75.47%   c. 24.53%   d. 56.84%   e. None of the above




# 10. Given the information above.
# Estimate a linear probability model on highwage.
# Include in your model controls for years of education (educ), years of work experience
# (exper), age, and an indicator for living in a city (city). Your model should have 5
# parameters including the intercept.
# How many observations are used to estimate the model?
# a. 753   b. 428   c. 325   d. 423   e. None of the above




# 11. Given the information above.
# What is the correct interpretation of the parameter on educ? Holding fixed the variables in
# the model, one additional year of education increases the probability of earning a high wage
# by ...
# a. 7.7463 percent
# b. 0.0775 percentage points
# c. 0.7746 percentage points
# d. 7.7463 percentage points
# e. None of the above




# 12. Given the information above.
# What is the estimate of the lower bound of the 90% confidence interval for the intercept of
# the model?
# a. -1.1335   b. -0.5772   c. -1.0847   d. -1.0613   e. None of the above




# 13. Given the information above.
# Consider the null hypothesis that H0: b_city = 0. What is the strongest conclusion we can
# draw about this null hypothesis?
# a. Reject the null at the 0.1% level
# b. Reject the null at the 1% level
# c. Reject the null at the 5% level
# d. Reject the null at the 10% level
# e. Fail to reject the null at the 10% level




# 14. Given the information above.
# Re-estimate the model adding husband's years of education (huseduc) as an additional
# control. What is the percentage change in the parameter on educ when we control for
# husband's education?
# a. -8.63%   b. 8.63%   c. 7.95%   d. 108.63%   e. None of the above




# 15. Given the information above.
# Re-estimate the model adding husband's years of education (huseduc) as an additional
# control. What is the variance inflation factor for the parameter on educ when we control for
# husband's education? (note: if you are calculating the variance inflation factor from the
# formula you need to ensure that the same observations are used in the different regressions)
# a. 1.6279   b. 1.6137   c. 0.6441   d. 1.5525   e. None of the above



