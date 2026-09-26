 # ECON 5021 Unit 1 Data Analysis: Practice Exam 0 (multiple choice) - the 9/21 midterm
# 20 questions, 35 minutes. Type each commented code block on the blank lines under it,
# then write the code that answers each question. Key: exam1_solution.r

# 1. This is the start of a multipart question. The information below pertains to question 1 to question 4.
# WMT is the ticker symbol for Walmart. Consider the weekly returns for this stock between
# August 24, 2014 and December 09, 2017.
# The following code creates a vector x containing the weekly returns:
#
# library(quantmod)
# library(dplyr)
#
# x = getSymbols("WMT",
#                from = "2014-08-24",
#                to = "2017-12-09",
#                auto.assign = FALSE) %>%
#   Ad() %>%
#   weeklyReturn() %>%
#   as.data.frame() %>%
#   pull(weekly.returns)

library(quantmod)
library(dplyr)

print("question 1-4")
x = getSymbols("WMT",
              from = "2014-08-24",
              to = "2017-12-09",
              auto.assign = FALSE) %>%
  Ad() %>%
  weeklyReturn() %>%
  as.data.frame() %>%
  pull(weekly.returns)

# The returns are calculated using the adjusted closing price, which accounts for dividends
# and stock splits. x should contain 172 weekly returns.
# What was the maximum weekly return over this time period?
# a. 13.94%   b. 13.09%   c. 16.81%   d. 9.65%   e. None of the above
max(x) # D

# 2. Given the information above.
# What was the interquartile range of weekly returns over this time period?
# a. 4.67%   b. 3.20%   c. 5.10%   d. 2.66%   e. None of the above
IQR(x) # D

# 3. Given the information above.
# What is the 0.95-quantile of the weekly returns?
# a. 3.07%   b. 1.04%   c. 3.68%   d. 0.26%   e. None of the above
quantile(x, probs = 0.95) # E

# 4. Given the information above.
# What is the empirical probability that the weekly return is greater than zero?
# a. 0.4903   b. 0.3293   c. 0.3958   d. 0.3476   e. None of the above
mean(x > 0) # E

# 5. This is the start of a multipart question. The information below pertains to question 5 to question 6.
# TSLA is the ticker symbol for Tesla. Consider the monthly returns for this stock between
# January 01, 2013 and July 31, 2026.
# The following code creates a vector x containing the monthly returns:
#
# library(quantmod)
# library(dplyr)
#
# x = getSymbols("TSLA",
#                from = "2013-01-01",
#                to = "2026-07-31",
#                auto.assign = FALSE) %>%
#   Ad() %>%
#   monthlyReturn() %>%
#   as.data.frame() %>%
#   pull(monthly.returns)

print("question 5-6")
x1 = getSymbols("TSLA",
                from = "2013-01-01",
                to = "2026-07-31",
                auto.assign = FALSE) %>%
  Ad() %>%
  monthlyReturn() %>%
  as.data.frame() %>%
  pull(monthly.returns)

# The returns are calculated using the adjusted closing price, which accounts for dividends
# and stock splits. x should contain 163 monthly returns.
# We would like to compare the empirical distribution of monthly returns to a normal
# approximation with mean 0.045 and standard deviation 0.185.
# Focus on the 0.01-quantile. This is the return value such that approximately 1% of monthly
# returns are less than or equal to it. Which pair correctly reports the empirical 0.01-quantile
# and the 0.01-quantile from the normal approximation?
# a. The empirical 0.01-quantile is -26.96%, and the normal approximation 0.01-quantile is -38.54%
# b. The empirical 0.01-quantile is -23.98%, and the normal approximation 0.01-quantile is -38.54%
# c. The empirical 0.01-quantile is -23.98%, and the normal approximation 0.01-quantile is -44.93%
# d. The empirical 0.01-quantile is -23.98%, and the normal approximation 0.01-quantile is -14.70%
# e. None of the above

#empirical quantile 
# A
quantile(x1, probs = 0.01)
qnorm(0.01, mean = 0.045, sd = 0.185)


# 6. Given the information above.
# The CDF is defined as F(a) = Pr(x <= a). In this context, F(a) is the probability that the
# monthly return is less than or equal to a. Evaluate the CDF at a = 0.09. Which pair
# correctly reports the empirical probability and the probability implied by the normal
# approximation?
# a. The empirical probability is 0.6469, and the normal approximation probability is 0.1781
# b. The empirical probability is 0.6810, and the normal approximation probability is 0.5961
# c. The empirical probability is 0.6810, and the normal approximation probability is 0.1781
# d. The empirical probability is 0.6810, and the normal approximation probability is 0.3282
# e. None of the above
#helped, B
mean(x1 <= 0.09) #cdf
pnorm(0.09, mean = 0.045, sd = 0.185)

# 7. This is the start of a multipart question. The information below pertains to question 7 to question 10.
# A balanced portfolio contains a mix of domestic stocks, international stocks, and bonds.
# Suppose you have a three-fund portfolio with target allocation of 48% VOO (Vanguard S&P
# 500 ETF), 26% VIGI (Vanguard International Dividend Appreciation ETF), and 26% VGIT
# (Vanguard Intermediate-Term Treasury ETF).
# The following code retrieves the weekly returns for the last three years for these three ETFs:
#
# library(quantmod)
# library(dplyr)
#
# getSymbols(c("VOO","VIGI","VGIT"),
#            from = "2023-09-24",
#            to = "2026-09-19")
#
# weekly_return = merge(VOO %>% Ad() %>% weeklyReturn(),
#                       VIGI %>% Ad() %>% weeklyReturn(),
#                       VGIT %>% Ad() %>% weeklyReturn())
print("question 7-10")
getSymbols(c("VOO", "VIGI", "VGIT"),
           from = "2023-09-24",
           to = "2026-09-19")

weekly_return = merge(VOO %>% Ad() %>% weeklyReturn(),
                      VIGI %>% Ad() %>% weeklyReturn(),
                      VGIT %>% Ad() %>% weeklyReturn())

r = as.data.frame(weekly_return) %>% na.omit()
names(r) = c("VOO, VIGI, VGIT")
w = c(0.48, 0.26, 0.26)

# Define r = (r_VOO, r_VIGI, r_VGIT)' as the vector of weekly returns.
# From the weekly returns r, we construct a linear approximation to annual returns R. The
# question uses this annualized approximation. The mean and variance of annual returns are
# E(R) = 52E(r) and Var(R) = 52Var(r).
# Using this approximation of annual returns, what is the expected annual return of VOO in
# the data?
# a. 19.2%   b. 9.8%   c. 32.8%   d. 30.7%   e. None of the above
annual = 100*52
annual*mean(r$VOO) # E

# 8. Given the information above.
# In the data, what is the annualized standard deviation of returns for VOO?
# a. 6.73%   b. 18.16%   c. 24.58%   d. 14.25%   e. None of the above
100*(sqrt(52*var(r$VOO))) # D

# 9. Given the information above.
# Using the target allocation weights, what is the expected annual return of the three-fund
# portfolio over the last three years?
# a. 10.0%   b. 19.1%   c. 13.0%   d. 24.0%   e. None of the above
100*52*sum(w*colMeans(r)) # E

# 10. Given the information above.
# Using the target allocation weights, what is the standard deviation of annual returns for
# the three-fund portfolio over the last three years?
# a. 6.03%   b. 11.79%   c. 14.11%   d. 10.68%   e. None of the above
100*sqrt(52*t(w) %*% cov(r) %*% w) # E 

# 11. This is the start of a multipart question. The information below pertains to question 11 to question 16.
# The following code retrieves monthly unemployment rate data for Mariposa County,
# California, for the period from July 2019 through July 2026. During this period, no
# observation is available for 2025-10-01 because of a government shutdown. Remove this
# observation before conducting any analysis.
#
# library(fredr)
# fredr("CAMARI3URN",
#       observation_start = "2019-07-01",
#       observation_end = "2026-07-01")

library(fredr)
fredr_set_key("296957903c04db2287e557c017c3ad45")
x = fredr("CAMARI3URN",
          observation_start = as.Date("2019-07-01"),
          observation_end = as.Date("2026-07-01")) %>%
  filter(!is.na(value)) %>%
  pull(value)

n = length(x)
mu = mean(x)
se = sd(x)/sqrt(n)

# Consider the mean unemployment rate in Mariposa County. Let mu denote the population mean
# unemployment rate. Estimate this parameter using the sample average, and denote the
# estimator by mu_hat. We will assume that the variance of this estimator is
#     Var(mu_hat) = sigma^2 / n,
# where sigma^2 is the variance of the unemployment rate for that county and n is the number
# of observations used in the analysis. Using the sample variance to estimate sigma^2, assume
# that the standardized statistic follows a t distribution with 83 degrees of freedom.
# What is your point estimate, mu_hat?
# a. 1.55%   b. 0.96%   c. 0.32%   d. 8.13%   e. None of the above
mu # E

# 12. Given the information above.
# What is your estimated standard error for mu_hat?
# a. 0.3604   b. 0.5160   c. 0.1525   d. 0.1185   e. None of the above
se # A

# 13. Given the information above.
# Suppose we wanted to conduct a two-sided hypothesis test under the null that the mean
# unemployment rate in Mariposa County was equal to a given value, say v, i.e., H0: mu = v.
# Using the t distribution, what critical value should we use for a 0.1% significance test?
# a. 4.1515   b. 3.4116   c. 2.7521   d. 1.8259   e. None of the above
qt(1-0.001/2, df = n-1) # B

# 14. Given the information above.
# During this same time period, the overall unemployment rate in California was 5.98%. Given
# your estimate, mu_hat, and its standard error, consider the null hypothesis that the mean
# unemployment rate in Mariposa County was the same as the state, i.e., H0: mu = 5.98.
# What is the test statistic associated with this test?
# a. -7.743   b. -2.285   c. 2.285   d. -4.114   e. None of the above
tstat = ((mu-5.98) / se)
tstat # C

# 15. Given the information above.
# Consider the null hypothesis, H0: mu = 5.98. Given the data, what is the strongest
# conclusion we can draw about this null hypothesis using a two-sided test?
# a. Reject the null at the 0.1% level
# b. Reject the null at the 1% level
# c. Reject the null at the 5% level
# d. Reject the null at the 10% level
# e. Fail to reject the null at the 10% level
2*( 1-pt(abs(tstat) , df = n-1)) # C
# 2.484 -> reject at the 5% level

# 16. Given the information above.
# Which of the following is the correct 99% confidence interval for your estimate?
# a. [5.8535, 7.7536]   b. [6.5139, 7.0932]   c. [6.5353, 7.0718]   d. [6.1813, 7.4258]
# e. None of the above
mu + c(-1, 1)*qt(0.995, df = n - 1)*se # A

# 17. This is the start of a multipart question. The information below pertains to question 17 to question 20.
# In this question, you will use Monte Carlo simulation to study the sampling properties of
# OLS. None of the answer choices includes "None of the above," so use a sufficiently large
# number of Monte Carlo replications to obtain the requested level of precision.
# In this example, we relate days hospitalized (days) and patient age (age) to hospital cost
# in thousands of dollars (cost) using the prediction equation
#     cost_hat = b1 + b2*days + b3*age.
# The following code generates one simulated data set:
#
set.seed = 1
n_sims = 10000
n = 1200
b1 = numeric(n_sims)
r2 = numeric(n_sims)

for (s in 1:n_sims) {
  days = rpois(n, 4)
  age = 80 * rbeta(n, 4, 3)
  err = rnorm(n, mean = 0, sd = sqrt(230))
  cost = 7 + 4.25*days + 0.05*age + err
  m = lm(cost ~ days + age)
  b1[s] = coef(m)[1]
  r2[s] = summary(m)$r.squared
}










# Generate many simulated data sets using this data-generating process. For each simulated
# data set, estimate the OLS regression and save the requested statistic. Use the resulting
# Monte Carlo distribution to answer the question below.
# The mean of the simulated estimates of b1 should be close to its population value of 7.
# Estimate the standard error of b1 using the standard deviation of its simulated estimates.
# What is the estimated standard error?
# a. 2.338   b. 2.162   c. 2.525   d. 1.733   e. 1.984
sd(b1)


# 18. Given the information above.
# Using the simulated regressions, what is the expected value of R^2 under this
# data-generating process?
# a. 0.199   b. 0.241   c. 0.104   d. 0.130   e. 0.169
mean(r2)

# 19. Given the information above.
# Using the simulated R^2 values, which of the following is the lower bound of the 95%
# interval for the sampling distribution of R^2 under this data-generating process?
# a. 0.199   b. 0.074   c. 0.134   d. 0.237   e. 0.163
quantile(r2, c(0.025, 0.975)) # A

# 20. Given the information above.
# Using the simulated R^2 values, which of the following is the upper bound of the 95%
# interval for the sampling distribution of R^2 under this data-generating process?
# a. 0.351   b. 0.284   c. 0.221   d. 0.256   e. 0.160
# B


