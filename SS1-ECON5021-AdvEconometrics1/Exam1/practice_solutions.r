# ECON 5021 Unit 1 practice exams 1-4 - solution key
# MCQ 1: 1c 2e 3a 4d 5b 6c 7d 8e 9b 10e 11b 12e 13c 14b 15b 16c 17b 18c 19d 20a
# MCQ 2: 1d 2e 3b 4e 5c 6a 7e 8c 9b 10d 11b 12e 13d 14a 15e 16b 17c 18a 19b 20c
# Numbers pulled 2026-09-23; later Yahoo/FRED revisions can move the last digit.

library(quantmod)
library(dplyr)
library(fredr)
fredr_set_key("296957903c04db2287e557c017c3ad45")

# ======================= PRACTICE EXAM 1 (mcq1) =======================

# ---- Q1-4: COST monthly, 2012-03-01 to 2025-11-30 (165 obs) ----
x = getSymbols("COST", from = "2012-03-01", to = "2025-11-30", auto.assign = FALSE) %>%
  Ad() %>% monthlyReturn() %>% as.data.frame() %>% pull(monthly.returns)
length(x)                                   # 165
100*min(x)                                  # Q1  -15.35%  (c)
100*quantile(x, probs = 0.25)               # Q2  -1.71%   (e) not listed
100*sd(x)                                   # Q3  5.52%    (a)
mean(x < -0.05)                             # Q4  0.1333   (d)

# ---- Q5-6: AMZN weekly, 2016-01-01 to 2024-06-30 (443 obs), N(0.005, 0.041) ----
x = getSymbols("AMZN", from = "2016-01-01", to = "2024-06-30", auto.assign = FALSE) %>%
  Ad() %>% weeklyReturn() %>% as.data.frame() %>% pull(weekly.returns)
length(x)                                   # 443
100*quantile(x, probs = 0.95)               # Q5  7.00%
100*qnorm(0.95, mean = 0.005, sd = 0.041)   #     7.24%    (b)
mean(x > 0.06)                              # Q6  0.0722   Pr(x > a) = 1 - F(a)
1 - pnorm(0.06, mean = 0.005, sd = 0.041)   #     0.0899   (c)

# ---- Q7-10: 55% VTI / 30% VXUS / 15% BND, weekly ----
getSymbols(c("VTI", "VXUS", "BND"), from = "2023-06-04", to = "2026-05-30")
weekly_return = merge(VTI %>% Ad() %>% weeklyReturn(),
                      VXUS %>% Ad() %>% weeklyReturn(),
                      BND %>% Ad() %>% weeklyReturn())
r = as.data.frame(weekly_return) %>% na.omit()
names(r) = c("VTI", "VXUS", "BND")
w = c(0.55, 0.30, 0.15)
100*sqrt(52*var(r$VXUS))                    # Q7  14.73%   (d)
100*52*mean(r$BND)                          # Q8  4.1%     (e) not listed
100*52*sum(w*colMeans(r))                   # Q9  18.0%    (b)
100*sqrt(52*t(w) %*% cov(r) %*% w)          # Q10 12.10%   (e) not listed

# ---- Q11-16: El Dorado County, 2020-01 to 2026-06, drop 2025-10-01 (n = 77, df = 76), state = 6.14 ----
x = fredr("CAELDO5URN", observation_start = as.Date("2020-01-01"),
          observation_end = as.Date("2026-06-01")) %>%
  filter(!is.na(value)) %>% pull(value)
n = length(x)
mu = mean(x)
se = sd(x)/sqrt(n)
mu                                          # Q11 5.38%    (b)
se                                          # Q12 0.2730   (e) not listed; 0.2712 = NA row left in n
qt(1 - 0.01/2, df = n - 1)                  # Q13 2.6421   (c)
tstat = (mu - 6.14)/se
tstat                                       # Q14 -2.768   (b)
2*(1 - pt(abs(tstat), df = n - 1))          # Q15 p = 0.0071 -> reject at 1%  (b)
mu + c(-1, 1)*qt(0.975, df = n - 1)*se      # Q16 [4.8407, 5.9281]  (c)

# ---- Q17-20: Monte Carlo, wage_hat = b1 + b2*hours + b3*exper ----
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
  m = lm(wage ~ hours + exper)
  b2[s] = coef(m)[2]
  r2[s] = summary(m)$r.squared
}
sd(b2)                                      # Q17 0.0514   (b) 0.0515
mean(r2)                                    # Q18 0.180    (c) 0.179
quantile(r2, c(0.025, 0.975))               # Q19 0.135 (d) 0.134, Q20 0.226 (a) 0.227

# ======================= PRACTICE EXAM 2 (mcq2) =======================

# ---- Q1-4: KO daily, 2021-01-01 to 2022-12-31 (503 obs) ----
x = getSymbols("KO", from = "2021-01-01", to = "2022-12-31", auto.assign = FALSE) %>%
  Ad() %>% dailyReturn() %>% as.data.frame() %>% pull(daily.returns)
length(x)                                   # 503
100*max(x)                                  # Q1  3.87%    (d)
100*median(x)                               # Q2  0.11%    (e) not listed
100*quantile(x, probs = 0.05)               # Q3  -1.72%   (b)
mean(x <= 0)                                # Q4  0.4453   (e) not listed

# ---- Q5-6: AAPL monthly, 2010-01-01 to 2025-12-31 (192 obs), N(0.023, 0.077) ----
x = getSymbols("AAPL", from = "2010-01-01", to = "2025-12-31", auto.assign = FALSE) %>%
  Ad() %>% monthlyReturn() %>% as.data.frame() %>% pull(monthly.returns)
length(x)                                   # 192
100*quantile(x, probs = 0.90)               # Q5  11.45%
100*qnorm(0.90, mean = 0.023, sd = 0.077)   #     12.17%   (c)
mean(x <= -0.05)                            # Q6  0.1927
pnorm(-0.05, mean = 0.023, sd = 0.077)      #     0.1716   (a)

# ---- Q7-10: 40% VUG / 35% VTV / 25% BIV, weekly ----
getSymbols(c("VUG", "VTV", "BIV"), from = "2022-10-02", to = "2025-09-27")
weekly_return = merge(VUG %>% Ad() %>% weeklyReturn(),
                      VTV %>% Ad() %>% weeklyReturn(),
                      BIV %>% Ad() %>% weeklyReturn())
r = as.data.frame(weekly_return) %>% na.omit()
names(r) = c("VUG", "VTV", "BIV")
w = c(0.40, 0.35, 0.25)
100*52*mean(r$VTV)                          # Q7  16.0%    (e) not listed
100*sqrt(52*var(r$BIV))                     # Q8  6.57%    (c)
100*52*sum(w*colMeans(r))                   # Q9  18.3%    (b)
100*sqrt(52*t(w) %*% cov(r) %*% w)          # Q10 12.00%   (d)

# ---- Q11-16: Butte County, 2019-01 to 2026-03, drop 2025-10-01 (n = 86, df = 85), state = 5.90 ----
x = fredr("CABUTT5URN", observation_start = as.Date("2019-01-01"),
          observation_end = as.Date("2026-03-01")) %>%
  filter(!is.na(value)) %>% pull(value)
n = length(x)
mu = mean(x)
se = sd(x)/sqrt(n)
mu                                          # Q11 6.23%    (b)
se                                          # Q12 0.2183   (e) not listed; 0.2170 = NA row left in n
qt(1 - 0.05/2, df = n - 1)                  # Q13 1.9883   (d)
tstat = (mu - 5.90)/se
tstat                                       # Q14 1.491    (a)
2*(1 - pt(abs(tstat), df = n - 1))          # Q15 p = 0.1395 -> fail to reject at 10%  (e)
mu + c(-1, 1)*qt(0.95, df = n - 1)*se       # Q16 [5.8626, 6.5886]  (b); 90% CI uses qt(0.95)

# ---- Q17-20: Monte Carlo, price_hat = b1 + b2*sqft + b3*age ----
set.seed(1)
n_sims = 10000
n = 1500
b3 = numeric(n_sims)
r2 = numeric(n_sims)
for (s in 1:n_sims) {
  sqft = rnorm(n, mean = 18, sd = 4)
  age = runif(n, 0, 60)
  err = rnorm(n, mean = 0, sd = sqrt(900))
  price = 50 + 9*sqft - 0.5*age + err
  m = lm(price ~ sqft + age)
  b3[s] = coef(m)[3]
  r2[s] = summary(m)$r.squared
}
sd(b3)                                      # Q17 0.0444   (c) 0.0446
mean(r2)                                    # Q18 0.604    (a)
quantile(r2, c(0.05, 0.95))                 # Q19 0.577 (b), Q20 0.630 (c); 90% interval = 5%/95%

# ======================= PRACTICE EXAM 3 (frq1) =======================

# ---- Q1-4: MCD weekly, 2015-03-01 to 2020-02-29 (261 obs) ----
x = getSymbols("MCD", from = "2015-03-01", to = "2020-02-29", auto.assign = FALSE) %>%
  Ad() %>% weeklyReturn() %>% as.data.frame() %>% pull(weekly.returns)
length(x)                                   # 261
100*diff(range(x))                          # Q1  16.90%   (max - min)
100*IQR(x)                                  # Q2  2.43%
100*quantile(x, probs = 0.90)               # Q3  2.99%
mean(x > 0.02)                              # Q4  0.1916

# ---- Q5-6: NVDA monthly, 2014-01-01 to 2025-06-30 (138 obs), N(0.053, 0.131) ----
x = getSymbols("NVDA", from = "2014-01-01", to = "2025-06-30", auto.assign = FALSE) %>%
  Ad() %>% monthlyReturn() %>% as.data.frame() %>% pull(monthly.returns)
length(x)                                   # 138
100*quantile(x, probs = 0.05)               # Q5  -17.11%
100*qnorm(0.05, mean = 0.053, sd = 0.131)   #     -16.25%
mean(x <= 0)                                # Q6  0.3478
pnorm(0, mean = 0.053, sd = 0.131)          #     0.3429

# ---- Q7-10: 50% VTI / 20% VWO / 30% VGLT, weekly ----
getSymbols(c("VTI", "VWO", "VGLT"), from = "2023-01-08", to = "2025-12-27")
weekly_return = merge(VTI %>% Ad() %>% weeklyReturn(),
                      VWO %>% Ad() %>% weeklyReturn(),
                      VGLT %>% Ad() %>% weeklyReturn())
r = as.data.frame(weekly_return) %>% na.omit()
names(r) = c("VTI", "VWO", "VGLT")
w = c(0.50, 0.20, 0.30)
100*sqrt(52*var(r$VWO))                     # Q7  14.79%
100*52*mean(r$VGLT)                         # Q8  -0.22%
100*52*sum(w*colMeans(r))                   # Q9  13.25%
100*sqrt(52*t(w) %*% cov(r) %*% w)          # Q10 10.87%

# ---- Q11-16: Mendocino County, 2021-07 to 2026-07, drop 2025-10-01 (n = 60, df = 59), state = 5.10 ----
x = fredr("CAMEND5URN", observation_start = as.Date("2021-07-01"),
          observation_end = as.Date("2026-07-01")) %>%
  filter(!is.na(value)) %>% pull(value)
n = length(x)
mu = mean(x)
se = sd(x)/sqrt(n)
mu                                          # Q11 5.285%
se                                          # Q12 0.0991
qt(1 - 0.10/2, df = n - 1)                  # Q13 1.6711
tstat = (mu - 5.10)/se
tstat                                       # Q14 1.866
2*(1 - pt(abs(tstat), df = n - 1))          # Q15 p = 0.067 -> reject at 10%
mu + c(-1, 1)*qt(0.995, df = n - 1)*se      # Q16 [5.0211, 5.5489]

# ---- Q17-20: Monte Carlo, wage_hat = b1 + b2*educ + b3*exper ----
set.seed(1)
n_sims = 10000
n = 600
b1 = numeric(n_sims)
r2 = numeric(n_sims)
for (s in 1:n_sims) {
  educ = rpois(n, 14)
  exper = runif(n, 0, 40)
  err = rnorm(n, mean = 0, sd = sqrt(50))
  wage = -4 + 1.2*educ + 0.15*exper + err
  m = lm(wage ~ educ + exper)
  b1[s] = coef(m)[1]
  r2[s] = summary(m)$r.squared
}
sd(b1)                                      # Q17 about 1.22 (analytic 1.225)
mean(r2)                                    # Q18 0.318
quantile(r2, c(0.025, 0.975))               # Q19 0.256, Q20 0.380

# ======================= PRACTICE EXAM 4 (frq2) =======================

# ---- Q1-4: JPM monthly, 2011-06-01 to 2026-05-31 (180 obs) ----
x = getSymbols("JPM", from = "2011-06-01", to = "2026-05-31", auto.assign = FALSE) %>%
  Ad() %>% monthlyReturn() %>% as.data.frame() %>% pull(monthly.returns)
length(x)                                   # 180
100*max(x)                                  # Q1  21.54%
100*quantile(x, probs = 0.75)               # Q2  6.00%
100*median(x)                               # Q3  2.25%
mean(x <= -0.10)                            # Q4  0.0500

# ---- Q5-6: MSFT weekly, 2018-01-01 to 2025-12-31 (418 obs), N(0.005, 0.034) ----
x = getSymbols("MSFT", from = "2018-01-01", to = "2025-12-31", auto.assign = FALSE) %>%
  Ad() %>% weeklyReturn() %>% as.data.frame() %>% pull(weekly.returns)
length(x)                                   # 418
100*quantile(x, probs = 0.99)               # Q5  8.86%
100*qnorm(0.99, mean = 0.005, sd = 0.034)   #     8.41%
mean(x <= -0.04)                            # Q6  0.0766
pnorm(-0.04, mean = 0.005, sd = 0.034)      #     0.0928

# ---- Q7-10: 45% VGT / 25% VNQ / 30% BNDX, MONTHLY -> E(R) = 12E(r), Var(R) = 12Var(r) ----
getSymbols(c("VGT", "VNQ", "BNDX"), from = "2021-08-01", to = "2026-07-31")
monthly_return = merge(VGT %>% Ad() %>% monthlyReturn(),
                       VNQ %>% Ad() %>% monthlyReturn(),
                       BNDX %>% Ad() %>% monthlyReturn())
r = as.data.frame(monthly_return) %>% na.omit()
names(r) = c("VGT", "VNQ", "BNDX")
w = c(0.45, 0.25, 0.30)
100*12*mean(r$VNQ)                          # Q7  4.37%
100*sqrt(12*var(r$VGT))                     # Q8  23.50%
100*12*sum(w*colMeans(r))                   # Q9  9.80%
100*sqrt(12*t(w) %*% cov(r) %*% w)          # Q10 15.17%

# ---- Q11-16: Kern County, 2018-01 to 2026-05, drop 2025-10-01 (n = 100, df = 99), state = 5.68 ----
x = fredr("CAKERN0URN", observation_start = as.Date("2018-01-01"),
          observation_end = as.Date("2026-05-01")) %>%
  filter(!is.na(value)) %>% pull(value)
n = length(x)
mu = mean(x)
se = sd(x)/sqrt(n)
mu                                          # Q11 8.94%
se                                          # Q12 0.2154
qt(1 - 0.01/2, df = n - 1)                  # Q13 2.6264
tstat = (mu - 5.68)/se
tstat                                       # Q14 15.148
2*(1 - pt(abs(tstat), df = n - 1))          # Q15 p < 0.001 -> reject at 0.1%
mu + c(-1, 1)*qt(0.95, df = n - 1)*se       # Q16 [8.5853, 9.3007]

# ---- Q17-20: Monte Carlo, sales_hat = b1 + b2*temp + b3*promo ----
set.seed(1)
n_sims = 10000
n = 1000
b3 = numeric(n_sims)
r2 = numeric(n_sims)
for (s in 1:n_sims) {
  temp = rnorm(n, mean = 70, sd = 10)
  promo = rbinom(n, 1, 0.3)
  err = rnorm(n, mean = 0, sd = sqrt(250))
  sales = 20 + 0.8*temp + 12*promo + err
  m = lm(sales ~ temp + promo)
  b3[s] = coef(m)[3]
  r2[s] = summary(m)$r.squared
}
sd(b3)                                      # Q17 about 1.09-1.10 (analytic 1.091)
mean(r2)                                    # Q18 0.274
quantile(b3, c(0.025, 0.975))               # Q19 9.87, Q20 14.12; interval for b3, not R^2
