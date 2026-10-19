# ECON 5021 Unit 2 Data Analysis: Original practice exam (26101200001) - solution key
# Covers practice_exam2_mcq_original.r and practice_exam2_frq_original.r (same questions).
# MCQ: 1a 2a 3e 4b 5c 6c 7e 8d 9b 10d 11c 12d 13a 14e 15a
# FRQ: the number in each comment is the answer; the letter is the MCQ choice.

# Syntax to memorize
#   SSE                       deviance(m)                       (= sum(resid(m)^2))
#   critical value, C% CI     qt(1 - (1 - C)/2, df.residual(m))  e.g. 95% -> qt(0.975, ...)
#   test b = v (v != 0)       linearHypothesis(m, "educ = -0.15")  Pr(>F) = two-sided t p-value
#   test b = 0                summary(m)  -> read the Pr(>|t|) column
#   coefficient covariance    vcov(m)["(Intercept)", "west"]
#   one CI                    confint(m, "educ", level = 0.90)
#   percent change            (new - old) / old * 100
#   VIF                       vif(m)["cathhs"]                  (car)

library(wooldridge)
library(car)

# ---- Q1-8: fertil1 ----
dat = wooldridge::fertil1

# Q1. What is the mean of the variable kids in the dataset?
mean(dat$kids)                                   # 2.7431  (a)

# Q2. How many missing values or NA's are there for the variable age?
sum(is.na(dat$age))                              # 0       (a)

# Q3. Estimate the model with OLS. Coefficient on education?
m = lm(kids ~ educ + age + I(age^2) + year + east + northcen + west, data = dat)
summary(m)                                       # -0.12260 (e)

# Q4. What is the sum of squared errors of the model?
deviance(m)                                      # 2809.876 (b)

# Q5. Critical value for a 97.50% confidence interval?
qt(0.9875, df.residual(m))                       # 2.2444  (c)   df = 1121

# Q6. H0: b_northcen = 0. Strongest conclusion?
summary(m)$coefficients["northcen", ]            # p = 0.0237 -> reject at 5% (c)

# Q7. H0: b_educ = -0.15. p-value?
linearHypothesis(m, "educ = -0.15")              # Pr(>F) 0.1351  (e)   F = t^2, same p as the t-test

# Q8. Covariance between the estimates on (Intercept) and west?
vcov(m)["(Intercept)", "west"]                   # -0.02994 (d)

# ---- Q9-15: catholic ----
dat = wooldridge::catholic
dat$nonwhite = as.numeric(dat$asian == 1 | dat$hispan == 1 | dat$black == 1)

# Q9. What percent of the population are nonwhite?
100 * mean(dat$nonwhite)                         # 22.58%  (b)

# Q10. LPM of hsgrad on cathhs, nonwhite, read12, math12. R-squared?
m1 = lm(hsgrad ~ cathhs + nonwhite + read12 + math12, data = dat)
summary(m1)$r.squared                            # 0.07493 (d)   n = 5970 (hsgrad has 1460 NAs)

# Q11. Interpretation of the parameter on cathhs?
coef(m1)["cathhs"]                               # 0.030198 -> 3.0198 percentage points (c)

# Q12. Lower bound of the 90% CI for the intercept?
confint(m1, "(Intercept)", level = 0.90)         # 0.5120  (d)

# Q13. H0: b_math12 = 0. Strongest conclusion?
summary(m1)$coefficients["math12", ]             # p ~ 1e-43 -> reject at 0.1% (a)

# Q14. Add lfaminc. Percentage change in the parameter on cathhs?
m2 = lm(hsgrad ~ cathhs + nonwhite + read12 + math12 + lfaminc, data = dat)
old = coef(m1)["cathhs"]
new = coef(m2)["cathhs"]
(new - old) / old * 100                          # -39.46% (e)

# Q15. VIF for cathhs when we control for lfaminc?
vif(m2)["cathhs"]                                # 1.0249  (a)
# by hand: same observations as m2 (drop the rows where hsgrad is NA)
d = dat[!is.na(dat$hsgrad), ]
1 / (1 - summary(lm(cathhs ~ nonwhite + read12 + math12 + lfaminc, data = d))$r.squared)  # 1.0249
