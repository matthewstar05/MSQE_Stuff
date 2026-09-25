# ECON 5021 Unit 1 Data Analysis: 26092000003 (9/21 midterm) - solution key
# Key: 1d 2d 3e 4e 5a 6b 7e 8d 9e 10e 11e 12a 13b 14c 15c 16a 17d 18b 19a 20b

library(quantmod)
library(dplyr)
library(fredr)
fredr_set_key("296957903c04db2287e557c017c3ad45")

# ---- Q1-4: WMT weekly returns, 2014-08-24 to 2017-12-09 (172 obs) ----
x = getSymbols("WMT",
               from = "2014-08-24",
               to = "2017-12-09",
               auto.assign = FALSE) %>%
  Ad() %>%
  weeklyReturn() %>%
  as.data.frame() %>%
  pull(weekly.returns)
length(x)                                   # 172

# Q1. What was the maximum weekly return over this time period?
100*max(x)                                  # 9.65%  (d)

# Q2. What was the interquartile range of weekly returns over this time period?
100*IQR(x)                                  # 2.66%  (d)

# Q3. What is the 0.95-quantile of the weekly returns?
100*quantile(x, probs = 0.95)               # 4.03%  (e) not listed

# Q4. What is the empirical probability that the weekly return is greater than zero?
mean(x > 0)                                 # 0.5058 (e) not listed

# ---- Q5-6: TSLA monthly returns, 2013-01-01 to 2026-07-31 (163 obs), normal approx N(0.045, 0.185) ----
x = getSymbols("TSLA",
               from = "2013-01-01",
               to = "2026-07-31",
               auto.assign = FALSE) %>%
  Ad() %>%
  monthlyReturn() %>%
  as.data.frame() %>%
  pull(monthly.returns)
length(x)                                   # 163

# Q5. Which pair reports the empirical 0.01-quantile and the normal-approximation 0.01-quantile?
100*quantile(x, probs = 0.01)               # -26.96%
100*qnorm(0.01, mean = 0.045, sd = 0.185)   # -38.54%  (a)

# Q6. Evaluate the CDF at a = 0.09. Which pair reports the empirical and normal-approximation probability?
mean(x <= 0.09)                             # 0.6810
pnorm(0.09, mean = 0.045, sd = 0.185)       # 0.5961   (b)

# ---- Q7-10: 48% VOO / 26% VIGI / 26% VGIT, weekly, E(R) = 52E(r), Var(R) = 52Var(r) ----
getSymbols(c("VOO", "VIGI", "VGIT"),
           from = "2023-09-24",
           to = "2026-09-19")
weekly_return = merge(VOO %>% Ad() %>% weeklyReturn(),
                      VIGI %>% Ad() %>% weeklyReturn(),
                      VGIT %>% Ad() %>% weeklyReturn())
r = as.data.frame(weekly_return) %>% na.omit()
names(r) = c("VOO", "VIGI", "VGIT")
w = c(0.48, 0.26, 0.26)

# Q7. What is the expected annual return of VOO in the data?
100*52*mean(r$VOO)                          # 21.21% (e) not listed

# Q8. What is the annualized standard deviation of returns for VOO?
100*sqrt(52*var(r$VOO))                     # 14.25% (d)

# Q9. Using the target weights, what is the expected annual return of the three-fund portfolio?
100*52*sum(w*colMeans(r))                   # 14.43% (e) not listed

# Q10. Using the target weights, what is the SD of annual returns for the three-fund portfolio?
100*sqrt(52*t(w) %*% cov(r) %*% w)          # 9.93%  (e) not listed; upper bound sum(w*SD_i) = 11.51%

# ---- Q11-16: Mariposa County unemployment rate, 2019-07 to 2026-07, drop 2025-10-01 (n = 84, df = 83) ----
# fredr needs as.Date(); the bare strings printed on the exam throw an error
x = fredr("CAMARI3URN",
          observation_start = as.Date("2019-07-01"),
          observation_end = as.Date("2026-07-01")) %>%
  filter(!is.na(value)) %>%
  pull(value)
n = length(x)                               # 84
mu = mean(x)
se = sd(x)/sqrt(n)

# Q11. What is your point estimate, mu_hat?
mu                                          # 6.80%  (e) not listed

# Q12. What is your estimated standard error for mu_hat?
se                                          # 0.3604 (a)

# Q13. Two-sided test of H0: mu = v. What critical value for a 0.1% significance test?
qt(1 - 0.001/2, df = n - 1)                 # 3.4116 (b)

# Q14. H0: mu = 5.98 (state rate). What is the test statistic?
tstat = (mu - 5.98)/se
tstat                                       # 2.285  (c)

# Q15. H0: mu = 5.98. Strongest conclusion from a two-sided test?
2*(1 - pt(abs(tstat), df = n - 1))          # p = 0.0248 -> reject at 5%  (c)

# Q16. Correct 99% confidence interval for your estimate?
mu + c(-1, 1)*qt(0.995, df = n - 1)*se      # [5.8535, 7.7536]  (a)

# ---- Q17-20: Monte Carlo study of OLS, cost_hat = b1 + b2*days + b3*age ----
set.seed(1)
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

# Q17. Estimate the standard error of b1 using the SD of its simulated estimates.
sd(b1)                                      # 1.73   (d) 1.733

# Q18. What is the expected value of R^2 under this data-generating process?
mean(r2)                                    # 0.241  (b)

# Q19. Lower bound of the 95% interval for the sampling distribution of R^2?
# Q20. Upper bound of the 95% interval for the sampling distribution of R^2?
quantile(r2, c(0.025, 0.975))               # 0.199 (a), 0.284 (b)
