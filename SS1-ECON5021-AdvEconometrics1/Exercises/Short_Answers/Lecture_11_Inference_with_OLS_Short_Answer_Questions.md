# Lecture 11 Inference with OLS Short Answer Questions

# Question #1

The least squares estimator is \[
b=(X'X)^{-1}X'Y.
\] Under the classical linear regression model assumptions,
including normally distributed disturbances, the sampling distribution
is \[
b\mid X\sim N\left(\beta,\sigma^2(X'X)^{-1}\right).
\]

For confidence intervals and hypothesis testing for \(\beta_k\), we use the standardized
estimate. Explain how the standardized estimate is constructed and
describe its sampling distribution.

# Question #2

In the linear regression model: \[
Y=X\beta+\pmb{\varepsilon},
\] define the residual maker for \(X\) as \[
M_X=I-X(X'X)^{-1}X'.
\] The OLS estimator \(b\)
satisfies \[
Y=Xb+e.
\]

- Given that \[
e=M_X\pmb{\varepsilon},
\] show that \(e'e=\pmb{\varepsilon}'M_X\pmb{\varepsilon}\)
(working through the matrix algebra)

- Given that \[
\mathrm{E}(e'e\mid
X)=\mathrm{tr}\left(M_X\mathrm{E}(\pmb{\varepsilon}\pmb{\varepsilon}'\mid
X)\right),
\] show that under homoskedasticity and non-autocorrelation,
\[
\mathrm{E}\left(\frac{e'e}{n-K}\mid X\right)=\sigma^2.
\] (Please, no short cuts. Make all of your steps and
simplifications clear)

# Question #3

The least squares estimator is \[
b=(X'X)^{-1}X'Y,
\] where \(X\) is \(n\times K\), \(Y\) is \(n\times
1\), and \(b\) is \(K\times 1\). Under the classical
assumptions, the variance of the estimator is \[
\mathrm{Var}(b\mid X)=\sigma^2(X'X)^{-1}.
\]

Consider the bivariate regression model \[
y_i=\beta_1+\beta_2x_i+\varepsilon_i.
\] In this case, \(X\) is an
\(n\times 2\) matrix with a first
column of ones and a second column containing the observed values of
\(x_i\): \[
X=
\begin{bmatrix}
1 &amp; x_1\\
1 &amp; x_2\\
\vdots &amp; \vdots\\
1 &amp; x_n
\end{bmatrix},
\qquad
Y=
\begin{bmatrix}
y_1\\
y_2\\
\vdots\\
y_n
\end{bmatrix}.
\]

- Taking \(\sigma^2\) as given,
use matrix algebra to derive the variance of the OLS slope estimator
\(b_2\).

- Using your result from Part (a), identify and explain the three
factors that determine the variance of the OLS slope estimator.

# Question #4

Consider the linear regression model: \[
y_i = \beta_1 + \beta_2 x_{i2} + \beta_3 x_{i3} + \cdots + \beta_K
x_{iK} + \varepsilon_i.
\]

- Consider the OLS estimate \(b_3\) of \(\beta_3\) under the classical assumptions.
Write down the formula for the variance of this estimator, taking \(\sigma^2\) as given.

- Explain what each of the three components of the formula
represents and under what conditions they would improve the precision of
the estimator.

# Question #5

Consider the linear regression model: \[
y_i = \beta_1 + \beta_2 x_{i2} + \beta_3 x_{i3} + \cdots + \beta_K
x_{iK} + \varepsilon_i.
\]

- Explain what multicollinearity is and how it affects the
precision of OLS estimates.

- Explain why removing highly correlated regressors may improve
precision but can also introduce bias into OLS estimates.
