# =============================================================================
# Monte Carlo: 10-year return of an 80/20 VTI/AGG portfolio
#
# Source: ECON 5021 lecture notes, Section 6 (Simulation Methods),
#         especially slides 6.12–6.19.
#
# Question we cannot answer well from the raw sample:
#   We have ~20 years of monthly returns, so only about two non-overlapping
#   10-year windows. That is not enough to estimate the mean, variance, or
#   loss probability of a 10-year return.
#
# Monte Carlo idea:
#   Treat historical monthly returns as the population. Draw many artificial
#   10-year histories of 120 months (with replacement, iid months), compound
#   each history into one 10-year return, then treat those simulated 10-year
#   returns as a sample.
#
#   R_{10Y} = prod_{j=0}^{119} (1 + x_{t+j}) - 1
#
# For the 80/20 portfolio the monthly return is the weighted sum
#   R_t = 0.8 * VTI_t + 0.2 * AGG_t
# =============================================================================

# ---- packages ---------------------------------------------------------------
# quantmod: Yahoo Finance prices, Ad(), monthlyReturn()
# tidyverse: pipes, dplyr verbs used on the lecture slides
# lubridate: floor_date() for a clean end-of-sample date
# Rscript has no interactive CRAN picker, so set a mirror explicitly.
cran <- "https://cloud.r-project.org"
for (pkg in c("quantmod", "tidyverse", "lubridate")) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg, repos = cran)
  }
}

library(quantmod)
library(tidyverse)
library(lubridate)

set.seed(5021)  # reproducibility; the lecture slides do not set a seed

# ---- 6.4-style data: monthly VTI and AGG returns ----------------------------
# Adjusted close prices from 2004-01-01 through the last completed month.
getSymbols(
  c("VTI", "AGG"),
  from = "2004-01-01",
  to   = floor_date(Sys.Date(), "month") - 1
)

# Convert each series to monthly simple returns and name the columns.
VTI <- VTI %>%
  Ad() %>%
  monthlyReturn()
names(VTI) <- "VTI"

AGG <- AGG %>%
  Ad() %>%
  monthlyReturn()
names(AGG) <- "AGG"

# Align on common dates and keep a data frame with date, VTI, AGG.
ETF_data <- merge(VTI, AGG) %>%
  as.data.frame() %>%
  tibble::rownames_to_column("date") %>%
  mutate(date = as_date(date))

cat("Monthly return observations:", nrow(ETF_data), "\n")
print(tail(ETF_data, 3))

# ---- analytical 10-year mean (iid months) -----------------------------------
# If monthly returns are uncorrelated with common mean xbar,
# E[R_10Y] can be estimated as (1 + xbar)^120 - 1.
# This is easy for the mean; Monte Carlo is more useful for variance,
# because compounding expands into 2^120 - 1 product terms.

portfolio_monthly <- 0.8 * ETF_data$VTI + 0.2 * ETF_data$AGG
xbar_port <- mean(portfolio_monthly)
R10Y_closed_port <- (1 + xbar_port)^120 - 1

cat(sprintf(
  "Close-form expected 10-year 80/20 return: %.3f%%\n",
  100 * R10Y_closed_port
))

# ---- 6.19 Monte Carlo: 80/20 10-year returns --------------------------------
# n_mc histories, each with 120 monthly draws (with replacement).
# Months are drawn independently, matching the lecture assumption that
# monthly returns are uncorrelated.
#
# Implementation (same as the slide):
#   1. slice_sample n_mc * 120 rows with replacement from ETF_data
#   2. label blocks of 120 consecutive draws as simulation s = 1, ..., n_mc
#   3. within each block, compound 1 + 0.8 VTI + 0.2 AGG

n_mc <- 10000

Portfolio_MC <- ETF_data %>%
  slice_sample(n = n_mc * 120, replace = TRUE) %>%
  mutate(mc_idx = rep(1:n_mc, each = 120)) %>%
  group_by(mc_idx) %>%
  summarize(R10Y = prod(1 + 0.8 * VTI + 0.2 * AGG) - 1)

# Sample moments of the simulated 10-year returns.
Portfolio_10Y_mean <- mean(Portfolio_MC$R10Y)
Portfolio_10Y_sd   <- sd(Portfolio_MC$R10Y)
Portfolio_10Y_rar  <- Portfolio_10Y_mean / Portfolio_10Y_sd
Portfolio_10Y_loss <- mean(Portfolio_MC$R10Y < 0)

cat("\n80/20 Portfolio 10-year return\n")
cat(sprintf("Average return:          %.2f%%\n", 100 * Portfolio_10Y_mean))
cat(sprintf("Standard deviation:      %.2f%%\n", 100 * Portfolio_10Y_sd))
cat(sprintf("Risk-adjusted return:    %.4f\n", Portfolio_10Y_rar))
cat(sprintf("Pr(10-year return < 0):  %.2f%%\n", 100 * Portfolio_10Y_loss))

# Lecture slide output (from their sample / seed) was about:
#   Average return: 166.02%
#   Standard deviation: 105.55%
#   Risk-adjusted return: 1.5729
# Your numbers will differ slightly because Yahoo history grows over time
# and because resampling is random.

# ---- optional: compare with 100% VTI (slides 6.16 and 6.18) -----------------
VTI_mean <- mean(ETF_data$VTI)
VTI_10Y_closed <- (1 + VTI_mean)^120 - 1

VTI_MC <- ETF_data %>%
  slice_sample(n = n_mc * 120, replace = TRUE) %>%
  mutate(mc_idx = rep(1:n_mc, each = 120)) %>%
  group_by(mc_idx) %>%
  summarize(R10Y = prod(1 + VTI) - 1)

VTI_10Y_mean <- mean(VTI_MC$R10Y)
VTI_10Y_sd   <- sd(VTI_MC$R10Y)
VTI_10Y_rar  <- VTI_10Y_mean / VTI_10Y_sd

cat("\nVTI 10-year return\n")
cat(sprintf("Close-form analytical:   %.3f%%\n", 100 * VTI_10Y_closed))
cat(sprintf("Simulated average:       %.2f%%\n", 100 * VTI_10Y_mean))
cat(sprintf("Standard deviation:      %.2f%%\n", 100 * VTI_10Y_sd))
cat(sprintf("Risk-adjusted return:    %.4f\n", VTI_10Y_rar))

# Mixing 20% AGG typically lowers mean and SD; the lecture's risk-adjusted
# return (mean / SD of the 10-year return) is higher for 80/20 than for VTI.
