library(quantmod)
library(dplyr)

# fredr stuff
fredr_set_key("296957903c04db2287e557c017c3ad45")
library(fredr)
x = fredr("CAHUMB0URN",
          observation_start = as.Date("2017-09-01"),
          observation_end = as.Date("2026-07-01")) %>%
  filter(!is.na(value)) %>% pull(value) 

n = length(x)
mu = mean(x)
se = sd(x) / sqrt(n)

mu
se
qt(1-0.1/2, df = n - 1)
tstat = (mu-5.62) / se
tstat
2*(1-pt(abs(tstat), df = n-1))*se
qt(c(0.075, 0.9925), df = n-1)
#q1
library(quantmod)
library(dplyr)

x = getSymbols("KO",
               from = "2013-01-01",
               to = "2026-07-31",
               auto.assign = FALSE) %>%
  Ad() %>%
  monthlyReturn() %>%
  as.data.frame() %>%
  pull(monthly.returns)

length(x)
max(x)
IQR(x)
quantile(x, 0.05)
mean(x<0)

#q2
x = getSymbols("MCD",
               from = "2014-12-21",
               to = "2026-05-02",
               auto.assign = FALSE) %>%
  Ad() %>%
  weeklyReturn() %>%
  as.data.frame() %>%
  pull(weekly.returns)
length(x)

quantile(x, 0.80)
qnorm(p = 0.80, mean = 0.003, sd = 0.026)

mean(x < -0.03)
pnorm(q = -0.03,mean = 0.003, sd = 0.026)

# 3fund question
library(quantmod)
library(dplyr)
x = getSymbols(c("IBB", "VXUS", "VGSH"),
               from = "2023-09-24",
               to = "2026-09-19")
weekly_return = merge (IBB %>% Ad() %>% weeklyReturn(),
                       VXUS %>% Ad() %>% weeklyReturn(),
                       VGSH %>% Ad() %>% weeklyReturn()) %>% na.omit()
r = as.data.frame(weekly_return)
names(r) = c("IBB", "VXUS", "VGSH")
w = c(0.26, 0.29, 0.45)

100*52*mean(r$VXUS)
100*sqrt(52*var(r$VXUS))
100*52*sum(w*colMeans(r))
100*sqrt(52*t(w) %*% cov(r) %*% w)


#monte carlo
n_sims = 10000
n = 1400
b1 = numeric(n_sims)
r2 = numeric(n_sims)

for (s in 1:n_sims) {
  age = runif(n, 18, 80)
  claims = rpois(n, 1.5)
  err = rnorm(n, mean = 0, sd = sqrt(986660))
  premium = 675 + 8*age + 375*claims + err
  w = lm(premium ~ age + claims)
  b1[1] = coef(w)[1]
  r2[1] = summary(w)$r.squared
}

n_sims*mean(b1)
n_sims*sd(b1)
n_sims*mean(r2)
quantile(r2)
quantile(r2, probs = c(0.025, 0.975))
