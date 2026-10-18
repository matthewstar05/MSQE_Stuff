# ECON 5021 Unit 2 Data Analysis Practice C: 26101200004 - solution key
# Key: 1e 2b 3c 4b 5d 6e 7d 8b 9c 10b 11d 12c 13e 14b 15d

library(wooldridge)
library(car)

# ---- Q1-8: card ----
dat = wooldridge::card

# Q1. What is the mean of the variable lwage in the dataset?
mean(dat$lwage)                                  # 6.2618  (e)

# Q2. How many missing values or NA's are there for the variable IQ?
sum(is.na(dat$IQ))                               # 949     (b)

# Q3. Estimate the model with OLS. Coefficient on educ?
m = lm(lwage ~ educ + exper + I(exper^2) + black + smsa + south + momdad14 + KWW, data = dat)
summary(m)                                       # 0.05570 (c)   n = 2963 (KWW has 47 NAs)

# Q4. What is the sum of squared errors of the model?
sum(resid(m)^2)                                  # 405.3401 (b)

# Q5. Critical value for a 90% confidence interval?
qt(1 - 0.10/2, df = df.residual(m))              # 1.6454  (d)   qnorm gives 1.6449

# Q6. H0: b_momdad14 = 0. Strongest conclusion?
summary(m)$coefficients["momdad14", ]            # p = 0.1134 -> fail to reject at 10% (e)

# Q7. H0: b_educ = 0.05. p-value?
t = (coef(m)["educ"] - 0.05) / sqrt(vcov(m)["educ", "educ"])
2 * pt(-abs(t), df = df.residual(m))             # 0.1850  (d)

# Q8. Covariance between the estimates on educ and KWW?
vcov(m)["educ", "KWW"]                           # -2.7081e-06 (b)

# ---- Q9-15: mroz ----
dat = wooldridge::mroz
dat$highwage = as.numeric(dat$wage > 5)          # NA whenever wage is NA (women not working)

# Q9. Among women with a reported wage, what percent are highwage?
100 * mean(dat$highwage, na.rm = TRUE)           # 24.53%  (c)   NOT sum/753 = 13.94%

# Q10. LPM of highwage on educ, exper, age, city. How many observations are used?
m1 = lm(highwage ~ educ + exper + age + city, data = dat)
nobs(m1)                                         # 428     (b)

# Q11. Interpretation of the parameter on educ?
coef(m1)["educ"]                                 # 0.077463 -> 7.7463 percentage points (d)

# Q12. Lower bound of the 90% CI for the intercept?
confint(m1, level = 0.90)                        # -1.0847 (c)

# Q13. H0: b_city = 0. Strongest conclusion?
summary(m1)$coefficients["city", ]               # p = 0.2229 -> fail to reject at 10% (e)

# Q14. Add huseduc. Percentage change in the parameter on educ?
m2 = lm(highwage ~ educ + exper + age + city + huseduc, data = dat)
100 * (coef(m2)["educ"] / coef(m1)["educ"] - 1)  # 8.63%   (b)

# Q15. VIF for educ when we control for huseduc?
vif(m2)["educ"]                                  # 1.5525  (d)
# by hand: same observations as m2 (drop the rows where highwage is NA)
d = dat[!is.na(dat$highwage), ]
1 / (1 - summary(lm(educ ~ exper + age + city + huseduc, data = d))$r.squared)        # 1.5525
# WRONG: full sample (753 rows) gives 1.6279
