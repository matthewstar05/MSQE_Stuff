# Lecture 09 Properties of OLS Short Answer Solutions

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

**Solution:**

See the lecture notes.

Using the result from part (a), show that the OLS estimator is
unconditionally unbiased: \[
\mathrm{E}(b)=\beta.
\]

**Solution:**

See the lecture notes.

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

**Solution:**

Substituting \(Y=X\beta+\pmb{\varepsilon}\) into the OLS
estimator, \[
\begin{aligned}
b
&amp;=(X'X)^{-1}X'(X\beta+\pmb{\varepsilon})\\
&amp;=(X'X)^{-1}X'X\beta+
(X'X)^{-1}X'\pmb{\varepsilon}.
\end{aligned}
\]

Since \[
(X'X)^{-1}(X'X)=I,
\] it follows that \[
b=\beta+(X'X)^{-1}X'\pmb{\varepsilon}.
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

**Solution:**

Using the result from part (a) and \[
\mathrm{E}(b\mid X)=\beta,
\] we have \[
\begin{aligned}
\mathrm{Var}(b\mid X)
&amp;=
\mathrm{E}\left[
\left((X'X)^{-1}X'\pmb{\varepsilon}\right)
\left((X'X)^{-1}X'\pmb{\varepsilon}\right)'
\mid X
\right].
\end{aligned}
\]

Using the properties of matrix transposes, \[
\left((X'X)^{-1}X'\pmb{\varepsilon}\right)'=
\pmb{\varepsilon}'X(X'X)^{-1}.
\]

Therefore, \[
\mathrm{Var}(b\mid X)=
\mathrm{E}\left[
(X'X)^{-1}X'
\pmb{\varepsilon}\pmb{\varepsilon}'
X(X'X)^{-1}
\mid X
\right].
\]

Conditioning on \(X\) treats all
functions of \(X\) as fixed, so \[
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

**Solution:**

The conditional variance of \(\pmb{\varepsilon}\) is \[
\mathrm{Var}(\pmb{\varepsilon}\mid X)=
\mathrm{E}\left(
\pmb{\varepsilon}\pmb{\varepsilon}'\mid X
\right)-
\mathrm{E}(\pmb{\varepsilon}\mid X)
\mathrm{E}(\pmb{\varepsilon}\mid X)'.
\]

Since \[
\mathrm{E}(\pmb{\varepsilon}\mid X)=0,
\] the second term is zero. Therefore, \[
\mathrm{Var}(\pmb{\varepsilon}\mid X)=
\mathrm{E}\left(
\pmb{\varepsilon}\pmb{\varepsilon}'\mid X
\right).
\]

Explain the implications of homoskedasticity and non-autocorrelation
for the structure of \(\mathrm{Var}(\pmb{\varepsilon}\mid X)\).
Show that under these assumptions, \[
\mathrm{Var}(\pmb{\varepsilon}\mid X)=
\sigma^2 I_{n\times n},
\] where \(\mathrm{Var}(\varepsilon_i\mid
X)=\sigma^2\) and use this result to show that \[
\mathrm{Var}(b\mid X)=
\sigma^2(X'X)^{-1},
\]

**Solution:**

See the lecture notes.

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

**Solution:**

The matrix product \(X'\pmb{\varepsilon}\) can be written as
\[
X'\pmb{\varepsilon}=
\begin{bmatrix}
\sum_{i=1}^n x_{i1}\varepsilon_i\\
\sum_{i=1}^n x_{i2}\varepsilon_i\\
\vdots\\
\sum_{i=1}^n x_{iK}\varepsilon_i
\end{bmatrix}=
\sum_{i=1}^n x_i\varepsilon_i.
\]

Therefore, \[
X'\pmb{\varepsilon}
=
n\bar{w} = (n^{-1})^{-1} \bar{w}.
\]

Substituting into the OLS estimator, \[
\begin{aligned}
b
&amp;=
\beta+(X'X)^{-1}(n^{-1})^{-1} \bar{w}\\
&amp;=
\beta+
\left(\frac{X'X}{n}\right)^{-1}\bar{w}.
\end{aligned}
\]

Given that the OLS estimator is a function of the sample average
\(\bar{w}\) and that \[
\mathrm{E}(w_i)=0,
\] explain what the Law of Large Numbers implies about the OLS
estimator.

**Solution:**

See the lecture notes.

Given that the OLS estimator is a function of the sample average
\(\bar{w}\), explain what the Central
Limit Theorem implies about the sampling distribution of the OLS
estimator.

**Solution:**

See the lecture notes.
