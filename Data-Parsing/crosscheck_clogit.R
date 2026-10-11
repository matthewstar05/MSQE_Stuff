# Independent cross-check of Table 3, models 1-2, in R with survival::clogit.
#
# Uses the parsed file from 01_parse_data.py and re-estimates both specifications:
#   strata(card)     -> the grouping that reproduces the published numbers
#   strata(occasion) -> the corrected grouping (one person x one card)
# method = "exact" computes the exact conditional likelihood, which is what Stata's clogit
# uses when a group contains several chosen rows (as it does when grouping by card).
#
# Run from this folder:  Rscript crosscheck_clogit.R
suppressPackageStartupMessages(library(survival))

d <- read.csv("output/data/choice_long.csv")
d <- d[d$complete == 1, ]
f <- chosen ~ dev_limited + dev_high + dev_com + wat_med + wat_low + cult_s + cult_sl +
  lim_money + res_money + com_money + med_money + low_money

fit <- function(data, strata_var, label) {
  data$g <- data[[strata_var]]
  m <- clogit(update(f, . ~ . + strata(g)), data = data, method = "exact")
  s <- summary(m)$coefficients
  cat(sprintf("\n== %s  (strata = %s)  logLik = %.2f  N = %d\n", label, strata_var, m$loglik[2], nrow(data)))
  print(round(s[, c("coef", "Pr(>|z|)")], 3))
  data.frame(model = label, grouping = strata_var, variable = rownames(s),
             coef = round(s[, "coef"], 3), p = round(s[, "Pr(>|z|)"], 3), loglik = round(m$loglik[2], 2))
}

out <- rbind(
  fit(d, "card", "(1) CL All"),
  fit(d[d$councillor == 1, ], "card", "(2) CL Councillors"),
  fit(d, "occasion", "(1c) corrected All"),
  fit(d[d$councillor == 1, ], "occasion", "(2c) corrected Councillors")
)
write.csv(out, "output/tables/r_crosscheck_clogit.csv", row.names = FALSE)
cat("\nWrote output/tables/r_crosscheck_clogit.csv\n")
