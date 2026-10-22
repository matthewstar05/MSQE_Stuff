# start
library(wooldridge)
library(car)
dat = wooldridge::fertil1

#q1
var(dat$age)
#q2
sum(is.na(dat$kids))
#q3
model = lm(kids ~ educ + age + I(age^2) + feduc + farm + othrural + town + smcity, data = dat)
summary(model)
#q4-8
deviance(model)
#5
qt(0.9775, df.residual(model))
#6
summary(model)$coefficients["othrural", ]
#7
linearHypothesis(model, "educ = -0.15")
#8
vcov(model)["(Intercept)", "othrural"]

#Q9
library(wooldridge)
dat2 = wooldridge::catholic
dat2$nonparcath = as.numeric(dat2$parcath)
100 * mean(dat2$nonparcath, na.rm = TRUE)
#Q10
model2 = lm(hsgrad ~ cathhs + nonparcath + read12 + math12, data = dat2)
summary(model2)$r.squared
mean(dat$Y)
#Q11
100 * coef(model2)["cathhs"]
#Q12
confint(model2, "(Intercept)", level = 0.99)
#13
summary(model2)$coefficients["nonparcath", ]
#14
model3 = lm(hsgrad ~ cathhs + nonparcath + read12 + math12 + lfaminc, data = dat2)
old = coef(model2)["cathhs"]; new = coef(model3)["cathhs"]
(new - old) / old * 100

vif(model3)["lfaminc"]



