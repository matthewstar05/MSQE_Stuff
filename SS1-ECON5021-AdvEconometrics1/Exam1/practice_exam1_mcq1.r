# ECON 5021 Unit 1 Data Analysis: Practice Exam 1 (multiple choice)
# 20 questions, 35 minutes. Type each commented code block on the blank lines under it,
# then write the code that answers each question. Key: practice_solutions.r

# 1. This is the start of a multipart question. The information below pertains to question 1 to question 4.
# COST is the ticker symbol for Costco. Consider the monthly returns for this stock between
# March 01, 2012 and November 30, 2025.
# The following code creates a vector x containing the monthly returns:
#
# library(quantmod)
# library(dplyr)
#
# x = getSymbols("COST",
#                from = "2012-03-01",
#                to = "2025-11-30",
#                auto.assign = FALSE) %>%
#   Ad() %>%
#   monthlyReturn() %>%
#   as.data.frame() %>%
#   pull(monthly.returns)

library(quantmod)
library(dplyr)
library(fredr)
fredr_set_key("296957903c04db2287e557c017c3ad45")

x = getSymbols("COST",
               from = "2012-03-01",
               to = "2025-11-30",
               auto.assign = FALSE) %>%
  Ad() %>%
  monthlyReturn() %>%
  as.data.frame() %>%
  pull(monthly.returns)

# The returns are calculated using the adjusted closing price, which accounts for dividends
# and stock splits. x should contain 165 monthly returns.
# What was the minimum monthly return over this time period?
# a. -12.06%   b. -7.30%   c. -15.35%   d. -5.34%   e. None of the above

min(x) # C


# 2. Given the information above.
# What is the 0.25-quantile of the monthly returns?
# a. 5.79%   b. -2.96%   c. 7.50%   d. -0.84%   e. None of the above

quantile(x, 0.25) # E


# 3. Given the information above.
# What is the standard deviation of the monthly returns over this time period?
# a. 5.52%   b. 1.79%   c. 19.13%   d. 0.31%   e. None of the above

sd(x, na.rm = TRUE) # A


# 4. Given the information above.
# What is the empirical probability that the monthly return is less than -0.05 (a loss of more than 5%)?
# a. 0.3515   b. 0.0303   c. 0.8667   d. 0.1333   e. None of the above

mean(x < -0.05) # D


# 5. This is the start of a multipart question. The information below pertains to question 5 to question 6.
# AMZN is the ticker symbol for Amazon. Consider the weekly returns for this stock between
# January 01, 2016 and June 30, 2024.
# The following code creates a vector x containing the weekly returns:
#
# library(quantmod)
# library(dplyr)
#
x = getSymbols("AMZN",
                from = "2016-01-01",
                to = "2024-06-30",
                auto.assign = FALSE) %>%
   Ad() %>%
   weeklyReturn() %>%
   as.data.frame() %>%
   pull(weekly.returns)



# The returns are calculated using the adjusted closing price, which accounts for dividends
# and stock splits. x should contain 443 weekly returns.
# We would like to compare the empirical distribution of weekly returns to a normal
# approximation with mean 0.005 and standard deviation 0.041.
# Focus on the 0.95-quantile. This is the return value such that approximately 95% of weekly
# returns are less than or equal to it. Which pair correctly reports the empirical 0.95-quantile
# and the 0.95-quantile from the normal approximation?
# a. The empirical 0.95-quantile is 5.63%, and the normal approximation 0.95-quantile is 7.24%
# b. The empirical 0.95-quantile is 7.00%, and the normal approximation 0.95-quantile is 7.24%
# c. The empirical 0.95-quantile is 5.63%, and the normal approximation 0.95-quantile is 8.54%
# d. The empirical 0.95-quantile is 5.63%, and the normal approximation 0.95-quantile is -6.24%
# e. None of the above
quantile(x, 0.95)
qnorm(0.95, 0.005, 0.041) # B


# 6. Given the information above.
# Consider Pr(x > a), the probability that the weekly return is greater than a = 0.06.
# Which pair correctly reports the empirical probability and the probability implied by the
# normal approximation?
# a. The empirical probability is 0.9278, and the normal approximation probability is 0.9101
# b. The empirical probability is 0.0722, and the normal approximation probability is 0.9101
# c. The empirical probability is 0.0722, and the normal approximation probability is 0.0899
# d. The empirical probability is 0.0722, and the normal approximation probability is 1.0899
# e. None of the above

mean(x > 0.06)
1-pnorm(0.06, 0.005, 0.041) #B


# 7. This is the start of a multipart question. The information below pertains to question 7 to question 10.
# A balanced portfolio contains a mix of domestic stocks, international stocks, and bonds.
# Suppose you have a three-fund portfolio with target allocation of 55% VTI (Vanguard Total
# Stock Market ETF), 30% VXUS (Vanguard Total International Stock ETF), and 15% BND
# (Vanguard Total Bond Market ETF).
# The following code retrieves the weekly returns for three years for these three ETFs:
#
# library(quantmod)
# library(dplyr)
#
# getSymbols(c("VTI","VXUS","BND"),
#            from = "2023-06-04",
#            to = "2026-05-30")
#
# weekly_return = merge(VTI %>% Ad() %>% weeklyReturn(),
#                       VXUS %>% Ad() %>% weeklyReturn(),
#                       BND %>% Ad() %>% weeklyReturn())


getSymbols(c("VTI","VXUS","BND"),
            from = "2023-06-04",
            to = "2026-05-30")
weekly_return = merge(VTI %>% Ad() %>% weeklyReturn(),
                       VXUS %>% Ad() %>% weeklyReturn(),
                       BND %>% Ad() %>% weeklyReturn())

r = as.data.frame(weekly_return) %>% na.omit()
names(r) = c("VTI", "VXUS", "BND")
w = c(0.55, 0.30, 0.15)




# Define r = (r_VTI, r_VXUS, r_BND)' as the vector of weekly returns.
# From the weekly returns r, we construct a linear approximation to annual returns R. The
# mean and variance of annual returns are E(R) = 52E(r) and Var(R) = 52Var(r).
# Using this approximation of annual returns, what is the annualized standard deviation of
# returns for VXUS?
# a. 2.04%   b. 18.90%   c. 106.23%   d. 14.73%   e. None of the above
100*sqrt(52*var(r$VXUS)) # D

# 8. Given the information above.
# In the data, what is the expected annual return of BND?
# a. 5.3%   b. 21.2%   c. 1.0%   d. 18.9%   e. None of the above
100*52*mean(r$BND) # E

# 9. Given the information above.
# Using the target allocation weights, what is the expected annual return of the three-fund
# portfolio over these three years?
# a. 14.7%   b. 18.0%   c. 12.1%   d. 44.2%   e. None of the above
100*52*sum(w*colMeans(r)) # B

# 10. Given the information above.
# Using the target allocation weights, what is the standard deviation of annual returns for
# the three-fund portfolio over these three years?
# a. 9.23%   b. 13.29%   c. 1.46%   d. 87.26%   e. None of the above
100*sqrt(52*t(w) %*% cov(r) %*% w) # E

# 11. This is the start of a multipart question. The information below pertains to question 11 to question 16.
# The following code retrieves monthly unemployment rate data for El Dorado County,
# California, for the period from January 2020 through June 2026. During this period, no
# observation is available for 2025-10-01 because of a government shutdown. Remove this
# observation before conducting any analysis.
#
library(fredr)
x = fredr("CAELDO5URN",
      observation_start = as.Date("2020-01-01"),
      observation_end = as.Date("2026-06-01")) %>%
  filter(!is.na(value)) %>% pull(value)
n = length(x)
mu = mean(x)
se = sd(x) / sqrt(n)

# Consider the mean unemployment rate in El Dorado County. Let mu denote the population mean
# unemployment rate. Estimate this parameter using the sample average, and denote the
# estimator by mu_hat. We will assume that the variance of this estimator is
#     Var(mu_hat) = sigma^2 / n,
# where sigma^2 is the variance of the unemployment rate for that county and n is the number
# of observations used in the analysis. Using the sample variance to estimate sigma^2, assume
# that the standardized statistic follows a t distribution with 76 degrees of freedom.
# What is your point estimate, mu_hat?
# a. 6.14%   b. 5.38%   c. 2.40%   d. 0.27%   e. None of the above
mu #B



# 12. Given the information above.
# What is your estimated standard error for mu_hat?
# a. 2.3954   b. 0.0745   c. 0.2712   d. 0.3172   e. None of the above
se #C



# 13. Given the information above.
# Suppose we wanted to conduct a two-sided hypothesis test under the null that the mean
# unemployment rate in El Dorado County was equal to a given value, say v, i.e., H0: mu = v.
# Using the t distribution, what critical value should we use for a 1% significance test?
# a. 2.5758   b. 2.3764   c. 2.6421   d. 1.9917   e. None of the above
qt(1-0.01/2, df = n-1) #C 

# 14. Given the information above.
# During this same time period, the overall unemployment rate in California was 6.14%. Given
# your estimate, mu_hat, and its standard error, consider the null hypothesis that the mean
# unemployment rate in El Dorado County was the same as the state, i.e., H0: mu = 6.14.
# What is the test statistic associated with this test?
# a. 2.768   b. -2.768   c. -2.786   d. -0.316   e. None of the above
tstat = (mu-6.14)/se
tstat #A

# 15. Given the information above.
# Consider the null hypothesis, H0: mu = 6.14. Given the data, what is the strongest
# conclusion we can draw about this null hypothesis using a two-sided test?
# a. Reject the null at the 0.1% level
# b. Reject the null at the 1% level
# c. Reject the null at the 5% level
# d. Reject the null at the 10% level
# e. Fail to reject the null at the 10% level
2*(1-pt(abs(tstat), df = n-1))

# 16. Given the information above.
# Which of the following is the correct 95% confidence interval for your estimate?
# a. [4.6632, 6.1057]   b. [0.6136, 10.1553]   c. [4.8407, 5.9281]   d. [4.9299, 5.8390]
# e. None of the above
mu + c(-1,1)*qt(0.975, df = n-1)*se # C

# 17. This is the start of a multipart question. The information below pertains to question 17 to question 20.
# In this question, you will use Monte Carlo simulation to study the sampling properties of
# OLS. None of the answer choices includes "None of the above," so use a sufficiently large
# number of Monte Carlo replications to obtain the requested level of precision.
# In this example, we relate weekly hours worked (hours) and years of experience (exper) to
# hourly wage in dollars (wage) using the prediction equation
#     wage_hat = b1 + b2*hours + b3*exper.
# The following code generates one simulated data set:
#

set.seed(1)
n_sims = 10000
n = 900
b2 = numeric(n_sims)
r2 = numeric(n_sims)

for (s in 1:n_sims) {
  hours = runif(n, 20, 50)
  exper = rgamma(n, shape = 3, scale = 4)
  err = rnorm(n, mean = 0, sd = sqrt(180))
  wage = 5 + 0.40*hours + 0.75*exper + err
  
  w = lm(wage ~ hours + exper)
  b2[s] = coef(w)[2]
  r2[s] = summary(w)$r.squared
}










# Generate many simulated data sets using this data-generating process. For each simulated
# data set, estimate the OLS regression and save the requested statistic. Use the resulting
# Monte Carlo distribution to answer the question below.
# The mean of the simulated estimates of b2 should be close to its population value of 0.40.
# Estimate the standard error of b2 using the standard deviation of its simulated estimates.
# What is the estimated standard error?
# a. 0.0642   b. 0.0515   c. 0.0447   d. 0.0730   e. 0.0366
sd(b2) #B

# 18. Given the information above.
# Using the simulated regressions, what is the expected value of R^2 under this
# data-generating process?
# a. 0.137   b. 0.221   c. 0.179   d. 0.160   e. 0.256
mean(r2) #C



# 19. Given the information above.
# Using the simulated R^2 values, which of the following is the lower bound of the 95%
# interval for the sampling distribution of R^2 under this data-generating process?
# a. 0.098   b. 0.156   c. 0.112   d. 0.134   e. 0.179
quantile(r2, c(0.025, 0.975)) #D 



# 20. Given the information above.
# Using the simulated R^2 values, which of the following is the upper bound of the 95%
# interval for the sampling distribution of R^2 under this data-generating process?
# a. 0.227   b. 0.203   c. 0.262   d. 0.245   e. 0.199
#A 


