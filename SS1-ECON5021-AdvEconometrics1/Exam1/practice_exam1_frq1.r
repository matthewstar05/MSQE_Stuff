# ECON 5021 Unit 1 Data Analysis: Practice Exam 3 (free response)
# 20 questions, 35 minutes. Type each commented code block on the blank lines under it,
# then write the code that answers each question. Key: practice_solutions.r

# 1. This is the start of a multipart question. The information below pertains to question 1 to question 4.
# MCD is the ticker symbol for McDonald's. Consider the weekly returns for this stock between
# March 01, 2015 and February 29, 2020.
# The following code creates a vector x containing the weekly returns:
#
# library(quantmod)
# library(dplyr)
#
# x = getSymbols("MCD",
#                from = "2015-03-01",
#                to = "2020-02-29",
#                auto.assign = FALSE) %>%
#   Ad() %>%
#   weeklyReturn() %>%
#   as.data.frame() %>%
#   pull(weekly.returns)









# The returns are calculated using the adjusted closing price, which accounts for dividends
# and stock splits. x should contain 261 weekly returns.
# What was the range of weekly returns (maximum minus minimum) over this time period?




# 2. Given the information above.
# What was the interquartile range of weekly returns over this time period?




# 3. Given the information above.
# What is the 0.90-quantile of the weekly returns?




# 4. Given the information above.
# What is the empirical probability that the weekly return is greater than 0.02?




# 5. This is the start of a multipart question. The information below pertains to question 5 to question 6.
# NVDA is the ticker symbol for NVIDIA. Consider the monthly returns for this stock between
# January 01, 2014 and June 30, 2025.
# The following code creates a vector x containing the monthly returns:
#
# library(quantmod)
# library(dplyr)
#
# x = getSymbols("NVDA",
#                from = "2014-01-01",
#                to = "2025-06-30",
#                auto.assign = FALSE) %>%
#   Ad() %>%
#   monthlyReturn() %>%
#   as.data.frame() %>%
#   pull(monthly.returns)









# The returns are calculated using the adjusted closing price, which accounts for dividends
# and stock splits. x should contain 138 monthly returns.
# We would like to compare the empirical distribution of monthly returns to a normal
# approximation with mean 0.053 and standard deviation 0.131.
# Focus on the 0.05-quantile. This is the return value such that approximately 5% of monthly
# returns are less than or equal to it. Report the empirical 0.05-quantile and the
# 0.05-quantile from the normal approximation.




# 6. Given the information above.
# The CDF is defined as F(a) = Pr(x <= a). In this context, F(a) is the probability that the
# monthly return is less than or equal to a. Evaluate the CDF at a = 0. Report the empirical
# probability and the probability implied by the normal approximation.




# 7. This is the start of a multipart question. The information below pertains to question 7 to question 10.
# A balanced portfolio contains a mix of domestic stocks, emerging-market stocks, and bonds.
# Suppose you have a three-fund portfolio with target allocation of 50% VTI (Vanguard Total
# Stock Market ETF), 20% VWO (Vanguard FTSE Emerging Markets ETF), and 30% VGLT (Vanguard
# Long-Term Treasury ETF).
# The following code retrieves the weekly returns for three years for these three ETFs:
#
# library(quantmod)
# library(dplyr)
#
# getSymbols(c("VTI","VWO","VGLT"),
#            from = "2023-01-08",
#            to = "2025-12-27")
#
# weekly_return = merge(VTI %>% Ad() %>% weeklyReturn(),
#                       VWO %>% Ad() %>% weeklyReturn(),
#                       VGLT %>% Ad() %>% weeklyReturn())









# Define r = (r_VTI, r_VWO, r_VGLT)' as the vector of weekly returns.
# From the weekly returns r, we construct a linear approximation to annual returns R. The
# mean and variance of annual returns are E(R) = 52E(r) and Var(R) = 52Var(r).
# Using this approximation of annual returns, what is the annualized standard deviation of
# returns for VWO?




# 8. Given the information above.
# In the data, what is the expected annual return of VGLT?




# 9. Given the information above.
# Using the target allocation weights, what is the expected annual return of the three-fund
# portfolio over these three years?




# 10. Given the information above.
# Using the target allocation weights, what is the standard deviation of annual returns for
# the three-fund portfolio over these three years?




# 11. This is the start of a multipart question. The information below pertains to question 11 to question 16.
# The following code retrieves monthly unemployment rate data for Mendocino County,
# California, for the period from July 2021 through July 2026. During this period, no
# observation is available for 2025-10-01 because of a government shutdown. Remove this
# observation before conducting any analysis.
#
# library(fredr)
# fredr("CAMEND5URN",
#       observation_start = "2021-07-01",
#       observation_end = "2026-07-01")









# Consider the mean unemployment rate in Mendocino County. Let mu denote the population mean
# unemployment rate. Estimate this parameter using the sample average, and denote the
# estimator by mu_hat. We will assume that the variance of this estimator is
#     Var(mu_hat) = sigma^2 / n,
# where sigma^2 is the variance of the unemployment rate for that county and n is the number
# of observations used in the analysis. Using the sample variance to estimate sigma^2, assume
# that the standardized statistic follows a t distribution with 59 degrees of freedom.
# What is your point estimate, mu_hat?




# 12. Given the information above.
# What is your estimated standard error for mu_hat?




# 13. Given the information above.
# Suppose we wanted to conduct a two-sided hypothesis test under the null that the mean
# unemployment rate in Mendocino County was equal to a given value, say v, i.e., H0: mu = v.
# Using the t distribution, what critical value should we use for a 10% significance test?




# 14. Given the information above.
# During this same time period, the overall unemployment rate in California was 5.10%. Given
# your estimate, mu_hat, and its standard error, consider the null hypothesis that the mean
# unemployment rate in Mendocino County was the same as the state, i.e., H0: mu = 5.10.
# What is the test statistic associated with this test?




# 15. Given the information above.
# Consider the null hypothesis, H0: mu = 5.10. Given the data, what is the strongest
# conclusion we can draw about this null hypothesis using a two-sided test?




# 16. Given the information above.
# What is the correct 99% confidence interval for your estimate?




# 17. This is the start of a multipart question. The information below pertains to question 17 to question 20.
# In this question, you will use Monte Carlo simulation to study the sampling properties of
# OLS. Use a sufficiently large number of Monte Carlo replications to obtain the requested
# level of precision.
# In this example, we relate years of education (educ) and years of experience (exper) to
# hourly wage in dollars (wage) using the prediction equation
#     wage_hat = b1 + b2*educ + b3*exper.
# The following code generates one simulated data set:
#
# n = 600
# educ = rpois(n, 14)
# exper = runif(n, 0, 40)
# err = rnorm(n, mean = 0, sd = sqrt(50))
# wage = -4 + 1.2*educ + 0.15*exper + err









# Generate many simulated data sets using this data-generating process. For each simulated
# data set, estimate the OLS regression and save the requested statistic. Use the resulting
# Monte Carlo distribution to answer the question below.
# The mean of the simulated estimates of b1 should be close to its population value of -4.
# Estimate the standard error of b1 using the standard deviation of its simulated estimates.
# What is the estimated standard error?




# 18. Given the information above.
# Using the simulated regressions, what is the expected value of R^2 under this
# data-generating process?




# 19. Given the information above.
# Using the simulated R^2 values, what is the lower bound of the 95% interval for the
# sampling distribution of R^2 under this data-generating process?




# 20. Given the information above.
# Using the simulated R^2 values, what is the upper bound of the 95% interval for the
# sampling distribution of R^2 under this data-generating process?



