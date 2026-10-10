library(quantmod)
library(dplyr)

library(fredr)
fredr_set_key("296957903c04db2287e557c017c3ad45")
x4 = fredr("CAMARI3URN",
      observation_start = as.Date("2019-07-01"),
      observation_end = as.Date("2026-07-01"))
remove()

mean(x4$value, na.rm = TRUE)
var(x4, na.rm = TRUE)
sqrt(var(x4, na.rm = TRUE))


x = getSymbols("WMT", from = "2014-08-24", 
               to = "2017-12-09", auto.assign = FALSE) %>%
  Ad() %>%
  weeklyReturn() %>%
  as.data.frame() %>%
  pull(weekly.returns)

#100*max(x)
#100*IQR(x)
#100*quantile(x, probs = 0.95)
#mean(x > 0)

x2 = getSymbols("TSLA", from = "2013-01-01", 
               to = "2026-07-31", auto.assign = FALSE) %>%
  Ad() %>%
  monthlyReturn() %>%
  as.data.frame() %>%
  pull(monthly.returns)

#length(x2)
#100*quantile(x2, probs = 0.01) # quantile @ 0.01
#100*qnorm(p = 0.01, mean = 0.045, sd = 0.185) # PDF calc
#100*quantile(x2, probs = 0.09) # idk if right 
#100*pnorm(q = 0.09, mean = 0.045, sd = 0.185) # CDF calc @ 0.09

getSymbols(c("VOO", "VIGI", "VGIT"),
           from = "2023-09-24",
           to = "2026-09-19")
weekly_return = merge(VOO %>% Ad() %>% weeklyReturn(),
                      VIGI %>% Ad() %>% weeklyReturn(),
                      VGIT %>% Ad() %>% weeklyReturn())
# r = as.vector(c(VOO, VIGI, VGIT))

#52*mean(x3)
#52*sqrt(var(x3))
