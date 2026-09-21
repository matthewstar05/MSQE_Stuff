library(quantmod)
library(dplyr)

x = getSymbols("NVDA", from = "2013-02-01", 
               to = "2026-06-30", auto.assign = FALSE) %>%
  Ad() %>% monthlyReturn() %>% as.data.frame() %>% pull(monthly.returns)

length(x)
100*quantile(x, probs = 0.2)
100*IQR(x)
mean(x > 0)
mean(x < -0.1)
