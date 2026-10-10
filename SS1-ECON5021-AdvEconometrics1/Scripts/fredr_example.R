# FRED API example for ECON 5021
# Run install.packages("fredr") once if the package is not already installed.

library(fredr)

# API key supplied for this project. Do not commit this file to a public repository.
fredr_set_key("296957903c04db2287e557c017c3ad45")

# Retrieve the monthly U.S. civilian unemployment rate (UNRATE).
unemployment <- fredr(
  series_id = "UNRATE",
  observation_start = as.Date("2020-01-01"),
  observation_end = Sys.Date()
)

# Keep the fields typically used in class and inspect the newest observations.
unemployment <- unemployment[, c("date", "series_id", "value")]
print(tail(unemployment))

# Optional quick plot.
plot(
  unemployment$date,
  unemployment$value,
  type = "l",
  xlab = "Date",
  ylab = "Percent",
  main = "U.S. Civilian Unemployment Rate (FRED: UNRATE)"
)
