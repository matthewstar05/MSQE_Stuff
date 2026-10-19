# ECON 5021 Unit 2 Data Analysis Practice A: 26101200002 - solution key
# Key: 1b 2c 3b 4e 5c 6a 7b 8c 9d 10b 11c 12d 13c 14a 15c

library(wooldridge)
library(car)

# ---- Q1-8: bwght ----
dat = wooldridge::bwght

# Q1. What is the mean of the variable bwght in the dataset?
mean(dat$bwght)                                  # 118.6996 (b)

# Q2. How many missing values or NA's are there for the variable fatheduc?
sum(is.na(dat$fatheduc))                         # 196     (c)

# Q3. Estimate the model with OLS. Coefficient on cigs?
m = lm(bwght ~ cigs + faminc + I(faminc^2) + parity + motheduc + fatheduc + male + white, data = dat)
summary(m)                                       # -0.5950 (b)   n = 1191

# Q4. What is the sum of squared errors of the model?
deviance(m)                                      # 456161.5 (e)

# Q5. Critical value for a 99% confidence interval?
qt(0.995, df.residual(m))                        # 2.5800  (c)   df = 1182, NOT 1388 - 9

# Q6. H0: b_male = 0. Strongest conclusion?
summary(m)$coefficients["male", ]                # p = 0.00077 -> reject at 0.1% (a)

# Q7. H0: b_cigs = -0.5. p-value?
linearHypothesis(m, "cigs = -0.5")               # Pr(>F) 0.3871  (b)   F = t^2, same p as the t-test

# Q8. Covariance between the estimates on (Intercept) and white?
vcov(m)["(Intercept)", "white"]                  # -1.6775 (c)

# ---- Q9-15: k401ksubs ----
dat = wooldridge::k401ksubs
dat$young = as.numeric(dat$age < 35)

# Q9. What percent of the population are young?
100 * mean(dat$young)                            # 31.69%  (d)

# Q10. LPM of e401k on young, inc, male, marr. R-squared?
m1 = lm(e401k ~ young + inc + male + marr, data = dat)
summary(m1)$r.squared                            # 0.07394 (b)

# Q11. Interpretation of the parameter on young?
coef(m1)["young"]                                # -0.040627 -> -4.0627 percentage points (c)

# Q12. Upper bound of the 99% CI for the parameter on marr?
confint(m1, "marr", level = 0.99)                # 0.005662 (d)

# Q13. H0: b_marr = 0. Strongest conclusion?
summary(m1)$coefficients["marr", ]               # p = 0.0367 -> reject at 5% (c)

# Q14. Add fsize. Percentage change in the parameter on marr?
m2 = lm(e401k ~ young + inc + male + marr + fsize, data = dat)
old = coef(m1)["marr"]
new = coef(m2)["marr"]
(new - old) / old * 100                          # -41.27% (a)

# Q15. VIF for marr when we control for fsize?
vif(m2)["marr"]                                  # 1.8029  (c)
