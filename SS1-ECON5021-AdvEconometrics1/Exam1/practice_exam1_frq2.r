# ECON 5021 Unit 1 Data Analysis: Practice Exam 4 (free response)
# 20 questions, 35 minutes. Type each commented code block on the blank lines under it,
# then write the code that answers each question. Key: practice_solutions.r

# 1. This is the start of a multipart question. The information below pertains to question 1 to question 4.
# JPM is the ticker symbol for JPMorgan Chase. Consider the monthly returns for this stock
# between June 01, 2011 and May 31, 2026.
# The following code creates a vector x containing the monthly returns:
#
# library(quantmod)
# library(dplyr)
#
# x = getSymbols("JPM",
#                from = "2011-06-01",
#                to = "2026-05-31",
#                auto.assign = FALSE) %>%
#   Ad() %>%
#   monthlyReturn() %>%
#   as.data.frame() %>%
#   pull(monthly.returns)









# The returns are calculated using the adjusted closing price, which accounts for dividends
# and stock splits. x should contain 180 monthly returns.
# What was the maximum monthly return over this time period?




# 2. Given the information above.
# What is the 0.75-quantile of the monthly returns?




# 3. Given the information above.
# What was the median monthly return over this time period?




# 4. Given the information above.
# What is the empirical probability that the monthly return is less than or equal to -0.10?




# 5. This is the start of a multipart question. The information below pertains to question 5 to question 6.
# MSFT is the ticker symbol for Microsoft. Consider the weekly returns for this stock between
# January 01, 2018 and December 31, 2025.
# The following code creates a vector x containing the weekly returns:
#
# library(quantmod)
# library(dplyr)
#
# x = getSymbols("MSFT",
#                from = "2018-01-01",
#                to = "2025-12-31",
#                auto.assign = FALSE) %>%
#   Ad() %>%
#   weeklyReturn() %>%
#   as.data.frame() %>%
#   pull(weekly.returns)









# The returns are calculated using the adjusted closing price, which accounts for dividends
# and stock splits. x should contain 418 weekly returns.
# We would like to compare the empirical distribution of weekly returns to a normal
# approximation with mean 0.005 and standard deviation 0.034.
# Focus on the 0.99-quantile. This is the return value such that approximately 99% of weekly
# returns are less than or equal to it. Report the empirical 0.99-quantile and the
# 0.99-quantile from the normal approximation.




# 6. Given the information above.
# The CDF is defined as F(a) = Pr(x <= a). In this context, F(a) is the probability that the
# weekly return is less than or equal to a. Evaluate the CDF at a = -0.04. Report the
# empirical probability and the probability implied by the normal approximation.




# 7. This is the start of a multipart question. The information below pertains to question 7 to question 10.
# A sector portfolio contains a mix of technology stocks, real estate, and international
# bonds. Suppose you have a three-fund portfolio with target allocation of 45% VGT (Vanguard
# Information Technology ETF), 25% VNQ (Vanguard Real Estate ETF), and 30% BNDX (Vanguard
# Total International Bond ETF).
# The following code retrieves the MONTHLY returns for five years for these three ETFs:
#
# library(quantmod)
# library(dplyr)
#
# getSymbols(c("VGT","VNQ","BNDX"),
#            from = "2021-08-01",
#            to = "2026-07-31")
#
# monthly_return = merge(VGT %>% Ad() %>% monthlyReturn(),
#                        VNQ %>% Ad() %>% monthlyReturn(),
#                        BNDX %>% Ad() %>% monthlyReturn())









# Define r = (r_VGT, r_VNQ, r_BNDX)' as the vector of monthly returns (60 months).
# From the monthly returns r, we construct a linear approximation to annual returns R. The
# mean and variance of annual returns are E(R) = 12E(r) and Var(R) = 12Var(r).
# Using this approximation of annual returns, what is the expected annual return of VNQ in
# the data?




# 8. Given the information above.
# In the data, what is the annualized standard deviation of returns for VGT?




# 9. Given the information above.
# Using the target allocation weights, what is the expected annual return of the three-fund
# portfolio over these five years?




# 10. Given the information above.
# Using the target allocation weights, what is the standard deviation of annual returns for
# the three-fund portfolio over these five years?




# 11. This is the start of a multipart question. The information below pertains to question 11 to question 16.
# The following code retrieves monthly unemployment rate data for Kern County, California,
# for the period from January 2018 through May 2026. During this period, no observation is
# available for 2025-10-01 because of a government shutdown. Remove this observation before
# conducting any analysis.
#
# library(fredr)
# fredr("CAKERN0URN",
#       observation_start = "2018-01-01",
#       observation_end = "2026-05-01")









# Consider the mean unemployment rate in Kern County. Let mu denote the population mean
# unemployment rate. Estimate this parameter using the sample average, and denote the
# estimator by mu_hat. We will assume that the variance of this estimator is
#     Var(mu_hat) = sigma^2 / n,
# where sigma^2 is the variance of the unemployment rate for that county and n is the number
# of observations used in the analysis. Using the sample variance to estimate sigma^2, assume
# that the standardized statistic follows a t distribution with 99 degrees of freedom.
# What is your point estimate, mu_hat?




# 12. Given the information above.
# What is your estimated standard error for mu_hat?




# 13. Given the information above.
# Suppose we wanted to conduct a two-sided hypothesis test under the null that the mean
# unemployment rate in Kern County was equal to a given value, say v, i.e., H0: mu = v.
# Using the t distribution, what critical value should we use for a 1% significance test?




# 14. Given the information above.
# During this same time period, the overall unemployment rate in California was 5.68%. Given
# your estimate, mu_hat, and its standard error, consider the null hypothesis that the mean
# unemployment rate in Kern County was the same as the state, i.e., H0: mu = 5.68.
# What is the test statistic associated with this test?




# 15. Given the information above.
# Consider the null hypothesis, H0: mu = 5.68. Given the data, what is the strongest
# conclusion we can draw about this null hypothesis using a two-sided test?




# 16. Given the information above.
# What is the correct 90% confidence interval for your estimate?




# 17. This is the start of a multipart question. The information below pertains to question 17 to question 20.
# In this question, you will use Monte Carlo simulation to study the sampling properties of
# OLS. Use a sufficiently large number of Monte Carlo replications to obtain the requested
# level of precision.
# In this example, we relate daily high temperature (temp) and a promotion indicator (promo)
# to daily ice cream sales in hundreds of dollars (sales) using the prediction equation
#     sales_hat = b1 + b2*temp + b3*promo.
# The following code generates one simulated data set:
#
# n = 1000
# temp = rnorm(n, mean = 70, sd = 10)
# promo = rbinom(n, 1, 0.3)
# err = rnorm(n, mean = 0, sd = sqrt(250))
# sales = 20 + 0.8*temp + 12*promo + err









# Generate many simulated data sets using this data-generating process. For each simulated
# data set, estimate the OLS regression and save the requested statistic. Use the resulting
# Monte Carlo distribution to answer the question below.
# The mean of the simulated estimates of b3 should be close to its population value of 12.
# Estimate the standard error of b3 using the standard deviation of its simulated estimates.
# What is the estimated standard error?




# 18. Given the information above.
# Using the simulated regressions, what is the expected value of R^2 under this
# data-generating process?




# 19. Given the information above.
# Using the simulated estimates of b3, what is the lower bound of the 95% interval for the
# sampling distribution of b3 under this data-generating process?




# 20. Given the information above.
# Using the simulated estimates of b3, what is the upper bound of the 95% interval for the
# sampling distribution of b3 under this data-generating process?



