# ECON 5021 Unit 2 Data Analysis: Practice B (multiple choice) - exam 26101200003
# 15 questions. Type each commented code block on the blank lines under it,
# then write the code that answers each question. Key: practice_solutions_B.r

# 1. This is the start of a multipart question. The information below pertains to question 1 to question 8.
# The data set wage2 contains data on working men in the US from the 1980 National
# Longitudinal Survey. You can load the data into R using the wooldridge library using:
#
# library(wooldridge)
# dat = wooldridge::wage2
library(wooldridge)
dat = wooldridge::wage2


# The main outcome of interest is the variable wage, which is monthly earnings in dollars.
# What is the median of the variable wage in the dataset?
# a. 957.95   b. 905.00   c. 925.00   d. 1000.00   e. None of the above
median(dat$wage)
# B

# 2. Given the information above.
# How many missing values or NA's are there for the variable meduc in the dataset?
# a. 83   b. 194   c. 0   d. 78   e. None of the above
sum(is.na(dat$meduc))
# D

# 3. Given the information above.
# Consider the following linear regression model.
#     log(wage) = b0 + b1(educ) + b2(exper) + b3(exper^2) + b4(tenure) + b5(married) +
#     b6(black) + b7(south) + b8(urban) + b9(meduc) + e
# The model includes controls for years of education, years of work experience and experience
# squared, and years with the current employer (tenure). The model also controls for mother's
# education (meduc). Finally, (married, black, south, urban) are indicator variables.
# Estimate the model above with OLS. What is the estimated coefficient on educ?
# a. 0.06541   b. 0.05982   c. 0.06313   d. 0.07012   e. 0.05433
mod = lm(log(wage) ~ educ + exper + I(exper^2) + tenure + married + black + south + urban + meduc, data = dat)
summary(mod)
# C

# 4. Given the information above.
# What is the residual standard error (sigma_hat) of the model?
# a. 0.1312   b. 0.3623   c. 0.3601   d. 111.152   e. None of the above
# B

# 5. Given the information above.
# Suppose we wanted to create a confidence interval for one of the parameters of the model. If
# we wanted to create a 98% confidence interval, what critical value would we use?
# a. 2.3263   b. 2.0569   c. 2.5816   d. 2.3304   e. None of the above
qt(0.99, df.residual(mod))
# 


# 6. Given the information above.
# Consider the null hypothesis that H0: b_south = 0. What is the strongest conclusion we can
# draw about this null hypothesis?
# a. Reject the null at the 0.1% level
# b. Reject the null at the 1% level
# c. Reject the null at the 5% level
# d. Reject the null at the 10% level
# e. Fail to reject the null at the 10% level
summary(mod)$coefficients["south", ]
# B

# 7. Given the information above.
# Consider the null hypothesis that H0: b_educ = 0.05. What is the p-value associated with
# this hypothesis test?
# a. 0.0266   b. 0.0531   c. 0.9469   d. 0.0000   e. None of the above
library(car)
linearHypothesis(mod, "educ = 0.05")
# B

# 8. Given the information above.
# What is the covariance between the estimate of the parameter on exper and the parameter on
# exper^2?
# a. -7.4233*10^-6
# b. 7.4233*10^-6
# c. -5.8152*10^-4
# d. -3.2770*10^-4
# e. None of the above
vcov(mod)["exper", "I(exper^2)"]
# A

# 9. This is the start of a multipart question. The information below pertains to question 9 to question 15.
# The data set crime1 contains data on young men in California who were arrested at least once
# before 1986. You can load the data into R using the wooldridge library using:
#
# library(wooldridge)
# dat = wooldridge::crime1
library(wooldridge)
dat  = wooldridge::crime1

# We would like to study what are the main determinants of being arrested in 1986 using a
# linear probability model. To answer this question you will need to add a new variable to the
# data set called arrested which should equal 1 if the man was arrested at least once in 1986
# (i.e., narr86 >0) and zero otherwise.
# What percent of the population were arrested?
# a. 72.29%   b. 40.48%   c. 27.71%   d. 7.21%   e. None of the above
dat$arrested = as.numeric(dat$narr86 > 0)
mean(dat$arrested)
#C

# 10. Given the information above.
# Estimate a linear probability model on arrested.
# Include in your model controls for the proportion of prior arrests that led to a conviction
# (pcnv), months spent in prison in 1986 (ptime86), the number of quarters employed in 1986
# (qemp86), and black. Your model should have 5 parameters including the intercept.
# What is the adjusted R-squared from the estimated model?
# a. 0.06053   b. 0.05915   c. 0.04412   d. 0.07230   e. 0.05121
m1 = lm(arrested ~ pcnv + ptime86 + qemp86 + black, data = dat)
summary(m1)$adj.r.squared
# B

# 11. Given the information above.
# What is the correct interpretation of the parameter on qemp86? Holding fixed the variables
# in the model, one additional quarter of employment changes the probability of being arrested
# by ...
# a. -3.8155 percent
# b. -0.0382 percentage points
# c. -3.8155 percentage points
# d. -38.155 percentage points
# e. None of the above
coef(m1)["qemp86"]
# C

# 12. Given the information above.
# What is the estimate of the lower bound of the 95% confidence interval for the parameter on
# qemp86?
# a. -0.04707   b. -0.02754   c. -0.04914   d. -0.04878   e. None of the above
confint(m1, "qemp86", level = 0.95)
# D

# 13. Given the information above.
# Consider the null hypothesis that H0: b_pcnv = 0. What is the strongest conclusion we can
# draw about this null hypothesis?
# a. Reject the null at the 0.1% level
# b. Reject the null at the 1% level
# c. Reject the null at the 5% level
# d. Reject the null at the 10% level
# e. Fail to reject the null at the 10% level
summary(m1)$coefficients["pcnv", ]
# A

# 14. Given the information above.
# Re-estimate the model adding legal income in 1986 (inc86) as an additional control. What is
# the percentage change in the parameter on qemp86 when we control for income?
# a. -92.23%   b. 92.23%   c. -12.87%   d. 7.77%   e. None of the above




# 15. Given the information above.
# Re-estimate the model adding legal income in 1986 (inc86) as an additional control. What is
# the variance inflation factor for the parameter on qemp86 when we control for income? (note:
# if you are calculating the variance inflation factor from the formula you need to ensure
# that the same observations are used in the different regressions)
# a. 2.0362   b. 1.0833   c. 2.1398   d. 0.4673   e. None of the above



