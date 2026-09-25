# ECON 5021 Unit 1 Data Analysis: Practice Exam 2 (multiple choice)
# 20 questions, 35 minutes. Type each commented code block on the blank lines under it,
# then write the code that answers each question. Key: practice_solutions.r

# 1. This is the start of a multipart question. The information below pertains to question 1 to question 4.
# KO is the ticker symbol for Coca-Cola. Consider the daily returns for this stock between
# January 01, 2021 and December 31, 2022.
# The following code creates a vector x containing the daily returns:
#
# library(quantmod)
# library(dplyr)
#
# x = getSymbols("KO",
#                from = "2021-01-01",
#                to = "2022-12-31",
#                auto.assign = FALSE) %>%
#   Ad() %>%
#   dailyReturn() %>%
#   as.data.frame() %>%
#   pull(daily.returns)









# The returns are calculated using the adjusted closing price, which accounts for dividends
# and stock splits. x should contain 503 daily returns.
# What was the maximum daily return over this time period?
# a. 6.96%   b. 10.83%   c. 1.28%   d. 3.87%   e. None of the above




# 2. Given the information above.
# What was the median daily return over this time period?
# a. 0.06%   b. 0.68%   c. -0.50%   d. 0.55%   e. None of the above




# 3. Given the information above.
# What is the 0.05-quantile of the daily returns?
# a. -1.33%   b. -1.72%   c. -6.96%   d. 1.72%   e. None of the above




# 4. Given the information above.
# What is the empirical probability that the daily return is less than or equal to zero?
# a. 0.5547   b. 0.0020   c. 0.4990   d. 0.5000   e. None of the above




# 5. This is the start of a multipart question. The information below pertains to question 5 to question 6.
# AAPL is the ticker symbol for Apple. Consider the monthly returns for this stock between
# January 01, 2010 and December 31, 2025.
# The following code creates a vector x containing the monthly returns:
#
# library(quantmod)
# library(dplyr)
#
# x = getSymbols("AAPL",
#                from = "2010-01-01",
#                to = "2025-12-31",
#                auto.assign = FALSE) %>%
#   Ad() %>%
#   monthlyReturn() %>%
#   as.data.frame() %>%
#   pull(monthly.returns)









# The returns are calculated using the adjusted closing price, which accounts for dividends
# and stock splits. x should contain 192 monthly returns.
# We would like to compare the empirical distribution of monthly returns to a normal
# approximation with mean 0.023 and standard deviation 0.077.
# Focus on the 0.90-quantile. This is the return value such that approximately 90% of monthly
# returns are less than or equal to it. Which pair correctly reports the empirical 0.90-quantile
# and the 0.90-quantile from the normal approximation?
# a. The empirical 0.90-quantile is 13.93%, and the normal approximation 0.90-quantile is 12.17%
# b. The empirical 0.90-quantile is 13.93%, and the normal approximation 0.90-quantile is -7.57%
# c. The empirical 0.90-quantile is 11.45%, and the normal approximation 0.90-quantile is 12.17%
# d. The empirical 0.90-quantile is 13.93%, and the normal approximation 0.90-quantile is 14.97%
# e. None of the above




# 6. Given the information above.
# The CDF is defined as F(a) = Pr(x <= a). In this context, F(a) is the probability that the
# monthly return is less than or equal to a. Evaluate the CDF at a = -0.05. Which pair
# correctly reports the empirical probability and the probability implied by the normal
# approximation?
# a. The empirical probability is 0.1927, and the normal approximation probability is 0.1716
# b. The empirical probability is 0.8073, and the normal approximation probability is 0.1716
# c. The empirical probability is 0.1927, and the normal approximation probability is 0.8284
# d. The empirical probability is 1.1927, and the normal approximation probability is 0.1716
# e. None of the above




# 7. This is the start of a multipart question. The information below pertains to question 7 to question 10.
# A style-tilted portfolio contains a mix of growth stocks, value stocks, and bonds. Suppose
# you have a three-fund portfolio with target allocation of 40% VUG (Vanguard Growth ETF),
# 35% VTV (Vanguard Value ETF), and 25% BIV (Vanguard Intermediate-Term Bond ETF).
# The following code retrieves the weekly returns for three years for these three ETFs:
#
# library(quantmod)
# library(dplyr)
#
# getSymbols(c("VUG","VTV","BIV"),
#            from = "2022-10-02",
#            to = "2025-09-27")
#
# weekly_return = merge(VUG %>% Ad() %>% weeklyReturn(),
#                       VTV %>% Ad() %>% weeklyReturn(),
#                       BIV %>% Ad() %>% weeklyReturn())









# Define r = (r_VUG, r_VTV, r_BIV)' as the vector of weekly returns.
# From the weekly returns r, we construct a linear approximation to annual returns R. The
# mean and variance of annual returns are E(R) = 52E(r) and Var(R) = 52Var(r).
# Using this approximation of annual returns, what is the expected annual return of VTV in
# the data?
# a. 28.5%   b. 13.1%   c. 5.3%   d. 0.3%   e. None of the above




# 8. Given the information above.
# In the data, what is the annualized standard deviation of returns for BIV?
# a. 47.40%   b. 0.91%   c. 6.57%   d. 13.09%   e. None of the above




# 9. Given the information above.
# Using the target allocation weights, what is the expected annual return of the three-fund
# portfolio over these three years?
# a. 16.6%   b. 18.3%   c. 12.0%   d. 49.8%   e. None of the above




# 10. Given the information above.
# Using the target allocation weights, what is the standard deviation of annual returns for
# the three-fund portfolio over these three years?
# a. 14.24%   b. 9.38%   c. 86.56%   d. 12.00%   e. None of the above




# 11. This is the start of a multipart question. The information below pertains to question 11 to question 16.
# The following code retrieves monthly unemployment rate data for Butte County, California,
# for the period from January 2019 through March 2026. During this period, no observation is
# available for 2025-10-01 because of a government shutdown. Remove this observation before
# conducting any analysis.
#
# library(fredr)
# fredr("CABUTT5URN",
#       observation_start = "2019-01-01",
#       observation_end = "2026-03-01")









# Consider the mean unemployment rate in Butte County. Let mu denote the population mean
# unemployment rate. Estimate this parameter using the sample average, and denote the
# estimator by mu_hat. We will assume that the variance of this estimator is
#     Var(mu_hat) = sigma^2 / n,
# where sigma^2 is the variance of the unemployment rate for that county and n is the number
# of observations used in the analysis. Using the sample variance to estimate sigma^2, assume
# that the standardized statistic follows a t distribution with 85 degrees of freedom.
# What is your point estimate, mu_hat?
# a. 5.90%   b. 6.23%   c. 2.02%   d. 0.22%   e. None of the above




# 12. Given the information above.
# What is your estimated standard error for mu_hat?
# a. 2.0244   b. 0.0477   c. 0.2170   d. 0.1856   e. None of the above




# 13. Given the information above.
# Suppose we wanted to conduct a two-sided hypothesis test under the null that the mean
# unemployment rate in Butte County was equal to a given value, say v, i.e., H0: mu = v.
# Using the t distribution, what critical value should we use for a 5% significance test?
# a. 1.9600   b. 1.6630   c. 2.6349   d. 1.9883   e. None of the above




# 14. Given the information above.
# During this same time period, the overall unemployment rate in California was 5.90%. Given
# your estimate, mu_hat, and its standard error, consider the null hypothesis that the mean
# unemployment rate in Butte County was the same as the state, i.e., H0: mu = 5.90.
# What is the test statistic associated with this test?
# a. 1.491   b. -1.491   c. 1.500   d. 0.161   e. None of the above




# 15. Given the information above.
# Consider the null hypothesis, H0: mu = 5.90. Given the data, what is the strongest
# conclusion we can draw about this null hypothesis using a two-sided test?
# a. Reject the null at the 0.1% level
# b. Reject the null at the 1% level
# c. Reject the null at the 5% level
# d. Reject the null at the 10% level
# e. Fail to reject the null at the 10% level




# 16. Given the information above.
# Which of the following is the correct 90% confidence interval for your estimate?
# a. [5.7916, 6.6596]   b. [5.8626, 6.5886]   c. [5.8665, 6.5846]   d. [2.8591, 9.5921]
# e. None of the above




# 17. This is the start of a multipart question. The information below pertains to question 17 to question 20.
# In this question, you will use Monte Carlo simulation to study the sampling properties of
# OLS. None of the answer choices includes "None of the above," so use a sufficiently large
# number of Monte Carlo replications to obtain the requested level of precision.
# In this example, we relate house size in hundreds of square feet (sqft) and house age in
# years (age) to sale price in thousands of dollars (price) using the prediction equation
#     price_hat = b1 + b2*sqft + b3*age.
# The following code generates one simulated data set:
#
# n = 1500
# sqft = rnorm(n, mean = 18, sd = 4)
# age = runif(n, 0, 60)
# err = rnorm(n, mean = 0, sd = sqrt(900))
# price = 50 + 9*sqft - 0.5*age + err









# Generate many simulated data sets using this data-generating process. For each simulated
# data set, estimate the OLS regression and save the requested statistic. Use the resulting
# Monte Carlo distribution to answer the question below.
# The mean of the simulated estimates of b3 should be close to its population value of -0.5.
# Estimate the standard error of b3 using the standard deviation of its simulated estimates.
# What is the estimated standard error?
# a. 0.1964   b. 0.0632   c. 0.0446   d. 0.0316   e. 0.0548




# 18. Given the information above.
# Using the simulated regressions, what is the expected value of R^2 under this
# data-generating process?
# a. 0.604   b. 0.571   c. 0.636   d. 0.550   e. 0.660




# 19. Given the information above.
# Using the simulated R^2 values, which of the following is the lower bound of the 90%
# interval for the sampling distribution of R^2 under this data-generating process?
# a. 0.572   b. 0.577   c. 0.590   d. 0.556   e. 0.604




# 20. Given the information above.
# Using the simulated R^2 values, which of the following is the upper bound of the 90%
# interval for the sampling distribution of R^2 under this data-generating process?
# a. 0.635   b. 0.652   c. 0.630   d. 0.618   e. 0.604



