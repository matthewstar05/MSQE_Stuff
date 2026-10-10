# Lecture 09 Properties of OLS Short Answer Questions

Question #1
Suppose \[
Y=X\beta+\pmb{\varepsilon},
\] with \[
\mathrm{E}(\pmb{\varepsilon}\mid X)=0.
\] The OLS estimator is \[
b=(X'X)^{-1}X'Y.
\]

Show that the OLS estimator is conditionally unbiased: \[
\mathrm{E}(b\mid X)=\beta.
\]

Using the result from part (a), show that the OLS estimator is
unconditionally unbiased: \[
\mathrm{E}(b)=\beta.
\]

Question #2
Suppose \[
Y=X\beta+\pmb{\varepsilon}.
\] The OLS estimator is \[
b=(X'X)^{-1}X'Y.
\]

Show that the OLS estimator can be written as \[
b=
\beta+(X'X)^{-1}X'\pmb{\varepsilon}.
\]

The conditional variance of the OLS estimator is \[
\mathrm{Var}(b\mid X)=
\mathrm{E}\left[
\left(b-\mathrm{E}(b\mid X)\right)
\left(b-\mathrm{E}(b\mid X)\right)'
\mid X
\right].
\] Assuming that \(b\) is
conditionally unbiased, show that \[
\mathrm{Var}(b\mid X)=
(X'X)^{-1}X'
\mathrm{E}\left[
\pmb{\varepsilon}\pmb{\varepsilon}'\mid X
\right]
X(X'X)^{-1}.
\]

Assuming \(\mathrm{E}(\pmb{\varepsilon}\mid X)=0\),
explain why \[
\mathrm{E}\left[
\pmb{\varepsilon}\pmb{\varepsilon}'\mid X
\right]=
\mathrm{Var}(\pmb{\varepsilon}\mid X).
\]

Explain the implications of homoskedasticity and
non-autocorrelation for the structure of \(\mathrm{Var}(\pmb{\varepsilon}\mid X)\).
Show that under these assumptions, \[
\mathrm{Var}(\pmb{\varepsilon}\mid X)=
\sigma^2 I_{n\times n},
\] where \(\mathrm{Var}(\varepsilon_i\mid
X)=\sigma^2\) and use this result to show that \[
\mathrm{Var}(b\mid X)=
\sigma^2(X'X)^{-1},
\]

Question #3
Suppose \[
Y=X\beta+\pmb{\varepsilon}.
\] The OLS estimator can be written as \[
b=\beta+(X'X)^{-1}X'\pmb{\varepsilon}.
\]

Let \(x_i'\) denote the \(i\)th row of \(X\), so that \(x_i\) is a \(K\times1\) vector, and let \(\varepsilon_i\) denote the \(i\)th element of \(\pmb{\varepsilon}\). Define \[
w_i=x_i\varepsilon_i.
\]

The sample average of \(w_i\) is
\[
\bar{w}=
\frac{1}{n}\sum_{i=1}^n w_i=
\frac{1}{n}\sum_{i=1}^n x_i\varepsilon_i.
\]

Show that the OLS estimator can be written as \[
b=
\beta+
\left(\frac{X'X}{n}\right)^{-1}\bar{w}.
\]

Given that the OLS estimator is a function of the sample average
\(\bar{w}\) and that \[
\mathrm{E}(w_i)=0,
\] explain what the Law of Large Numbers implies about the OLS
estimator.

Given that the OLS estimator is a function of the sample average
\(\bar{w}\), explain what the Central
Limit Theorem implies about the sampling distribution of the OLS
estimator.
