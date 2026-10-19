# ECON 5021 Unit 2 Data Analysis: Practice B (26101200003) - solution key
# Covers practice_exam2_mcq_B.r and practice_exam2_frq_B.r (same questions).
# MCQ: 1b 2d 3c 4b 5e 6b 7b 8a 9c 10b 11c 12d 13a 14a 15c
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

# ---- Q1-8: wage2 ----
dat = wooldridge::wage2

# Q1. What is the median of the variable wage in the dataset?
median(dat$wage)                                 # 905     (b)

# Q2. How many missing values or NA's are there for the variable meduc?
sum(is.na(dat$meduc))                            # 78      (d)

# Q3. Estimate the model with OLS. Coefficient on educ?
m = lm(log(wage) ~ educ + exper + I(exper^2) + tenure + married + black + south + urban + meduc, data = dat)
summary(m)                                       # 0.06313 (c)   n = 857

# Q4. What is the residual standard error (sigma-hat) of the model?
summary(m)$sigma                                 # 0.3623  (b)

# Q5. Critical value for a 98% confidence interval?
qt(0.99, df.residual(m))                         # 2.3308  (e)   df = 847; 2.3304 uses the wrong df (935 - 10)

# Q6. H0: b_south = 0. Strongest conclusion?
summary(m)$coefficients["south", ]               # p = 0.0048 -> reject at 1% (b)

# Q7. H0: b_educ = 0.05. p-value?
linearHypothesis(m, "educ = 0.05")               # Pr(>F) 0.0531  (b)   F = t^2, same p as the t-test

# Q8. Covariance between the estimates on exper and exper^2?
vcov(m)["exper", "I(exper^2)"]                   # -7.4233e-06 (a)

# ---- Q9-15: crime1 ----
dat = wooldridge::crime1
dat$arrested = as.numeric(dat$narr86 > 0)

# Q9. What percent of the population were arrested in 1986?
100 * mean(dat$arrested)                         # 27.71%  (c)

# Q10. LPM of arrested on pcnv, ptime86, qemp86, black. Adjusted R-squared?
m1 = lm(arrested ~ pcnv + ptime86 + qemp86 + black, data = dat)
summary(m1)$adj.r.squared                        # 0.05915 (b)

# Q11. Interpretation of the parameter on qemp86?
coef(m1)["qemp86"]                               # -0.038155 -> -3.8155 percentage points (c)

# Q12. Lower bound of the 95% CI for the parameter on qemp86?
confint(m1, "qemp86", level = 0.95)              # -0.04878 (d)

# Q13. H0: b_pcnv = 0. Strongest conclusion?
summary(m1)$coefficients["pcnv", ]               # p ~ 6e-13 -> reject at 0.1% (a)

# Q14. Add inc86. Percentage change in the parameter on qemp86?
m2 = lm(arrested ~ pcnv + ptime86 + qemp86 + black + inc86, data = dat)
old = coef(m1)["qemp86"]
new = coef(m2)["qemp86"]
(new - old) / old * 100                          # -92.23% (a)

# Q15. VIF for qemp86 when we control for inc86?
vif(m2)["qemp86"]                                # 2.1398  (c)
