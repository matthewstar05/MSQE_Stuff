# Past 1 year of Microsoft (MSFT) daily prices from Yahoo Finance

if (!require("quantmod", quietly = TRUE)) {
  install.packages("quantmod")
  library(quantmod)
}

end_date   <- Sys.Date()
start_date <- end_date - 365

getSymbols(
  "MSFT",
  src         = "yahoo",
  from        = start_date,
  to          = end_date,
  auto.assign = TRUE
)

head(MSFT)
tail(MSFT)
summary(MSFT)

# Convenient data frame with a date column
msft <- data.frame(date = index(MSFT), coredata(MSFT))
nrow(msft)
head(msft)
