# Lecture 11 Inference with OLS Short Answer Solutions

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

<blockquote>
<strong>Solution:</strong>

Let \(\left[(X'X)^{-1}\right]_{kk}\) denote
the \(k\)th diagonal element of the
matrix inverse. The standardized estimate is \[
\frac{b_k-\beta_k}{\sqrt{\sigma^2\left[(X'X)^{-1}\right]_{kk}}}\sim
N(0,1).
\]

However, since \(\sigma^2\) is
unobserved, it must be estimated using \[
s^2=\frac{1}{n-K}\sum_{i=1}^n e_i^2.
\]

Replacing \(\sigma^2\) with \(s^2\) changes the sampling distribution of
the standardized estimate to a t-distribution with \(n-K\) degrees of freedom: \[
\frac{b_k-\beta_k}{\sqrt{s^2\left[(X'X)^{-1}\right]_{kk}}}\sim
t_{n-K}.
\]
</blockquote>

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

<blockquote>
<strong>Solution:</strong>

Starting with \(e=M_X\pmb{\varepsilon}\), \[
e'e=\pmb{\varepsilon}'M_X'M_X\pmb{\varepsilon}.
\] Since \(M_X\) is symmetric,
\[
\begin{aligned}
M_X'M_X
&amp;=\left(I-X(X'X)^{-1}X'\right)
  \left(I-X(X'X)^{-1}X'\right)\\
&amp;=I-2X(X'X)^{-1}X'
  +X(X'X)^{-1}X'X(X'X)^{-1}X'\\
&amp;=I-2X(X'X)^{-1}X'+X(X'X)^{-1}X'\\
&amp;=I-X(X'X)^{-1}X'\\
&amp;=M_X.
\end{aligned}
\] Therefore, \[
e'e=\pmb{\varepsilon}'M_X\pmb{\varepsilon}.
\]

</blockquote>

- Given that \[
\mathrm{E}(e'e\mid
X)=\mathrm{tr}\left(M_X\mathrm{E}(\pmb{\varepsilon}\pmb{\varepsilon}'\mid
X)\right),
\] show that under homoskedasticity and non-autocorrelation,
\[
\mathrm{E}\left(\frac{e'e}{n-K}\mid X\right)=\sigma^2.
\] (Please, no short cuts. Make all of your steps and
simplifications clear)

<blockquote>
<strong>Solution:</strong>

Under homoskedasticity and non-autocorrelation, \[
\mathrm{E}(\pmb{\varepsilon}\pmb{\varepsilon}'\mid X)=\sigma^2I.
\] Substituting: \[
\begin{aligned}
\mathrm{E}(e'e\mid X)
&amp;=\mathrm{tr}(M_X\sigma^2I)\\
&amp;=\sigma^2\mathrm{tr}(M_X)\\
&amp;=\sigma^2(n-K).
\end{aligned}
\] The final equality follows from \[
\begin{aligned}
\mathrm{tr}(M_X)
&amp;=\mathrm{tr}(I)-\mathrm{tr}\left(X(X'X)^{-1}X'\right)\\
&amp;=n-\mathrm{tr}\left((X'X)^{-1}X'X\right)\\
&amp;=n-\mathrm{tr}(I_K)\\
&amp;=n-K.
\end{aligned}
\] Therefore, \[
\mathrm{E}\left(\frac{e'e}{n-K}\mid X\right)=\sigma^2.
\]
</blockquote>

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

- Taking \(\sigma^2\) as given, use
matrix algebra to derive the variance of the OLS slope estimator \(b_2\).

<blockquote>
<strong>Solution:</strong>

Here you need to show the matrix algebra leading to \[
\mathrm{Var(b_2 \mid X)} = \frac{\sigma^2}{\sum_{i=1}^n (x_i -
\bar{x})^2}
\]

</blockquote>

- Using your result from Part (a), identify and explain the three
factors that determine the variance of the OLS slope estimator.

<blockquote>
<strong>Solution:</strong>

We can rewrite the denominator using the sample variance of \(x\): \[
s_x^2=\frac{1}{n-1}\sum_{i=1}^n(x_i-\bar{x})^2.
\] The variance of the OLS slope estimator can then be expressed
as \[
\mathrm{Var}(b_2\mid X)=\frac{\sigma^2}{(n-1)s_x^2}.
\]

This highlights three factors that determine the variance of \(b_2\):

- Disturbance variance: Greater \(\sigma^2\) increases the variance of \(b_2\).

- Sample size: More observations reduce the variance of \(b_2\), holding the variation in \(x\) fixed.

- Variation in \(x\): Greater
variation in \(x\) reduces the variance
of \(b_2\), holding sample size
fixed.

</blockquote>

# Question #4

Consider the linear regression model: \[
y_i = \beta_1 + \beta_2 x_{i2} + \beta_3 x_{i3} + \cdots + \beta_K
x_{iK} + \varepsilon_i.
\]

- Consider the OLS estimate \(b_3\)
of \(\beta_3\) under the classical
assumptions. Write down the formula for the variance of this estimator,
taking \(\sigma^2\) as given.

<blockquote>
<strong>Solution:</strong>

The formula you should have memorized and written down should be of
the form \[
\mathrm{Var}(b_3 \mid X) = \frac{\sigma^2}{(1 - R^2_{3})
\mathrm{SST}_{x_3}}.
\]

</blockquote>

- Explain what each of the three components of the formula represents
and under what conditions they would improve the precision of the
estimator.

<blockquote>
<strong>Solution:</strong>

Explain all three components in detail, making especially clear what
the \(R_3^2\) component represents. For
example, it comes from a regression of \(x_3\) on all the other regressors and
measures the fraction of variation in \(x_3\) explained by those regressors.
Explain how this affects the precision of \(b_3\).

See the lecture notes.
</blockquote>

# Question #5

Consider the linear regression model: \[
y_i = \beta_1 + \beta_2 x_{i2} + \beta_3 x_{i3} + \cdots + \beta_K
x_{iK} + \varepsilon_i.
\]

- Explain what multicollinearity is and how it affects the precision
of OLS estimates.

<blockquote>
<strong>Solution:</strong>

Multicollinearity describes the degree to which regressors are
correlated with one another. If a regressor is highly correlated with
the other regressors, its OLS coefficient estimate will be less precise.
Recall that \[
\mathrm{Var}(b_k \mid X) = \frac{\sigma^2}{(1-R_k^2)\mathrm{SST}_{x_k}}.
\] Here, \(R_k^2\) is the
fraction of variation in \(x_k\)
explained by the other regressors. As \(R_k^2\) increases, the denominator
decreases, causing \(\mathrm{Var}(b_k \mid
X)\) to increase.

</blockquote>

- Explain why removing highly correlated regressors may improve
precision but can also introduce bias into OLS estimates.

<blockquote>
<strong>Solution:</strong>

Removing highly correlated regressors can reduce \(R_k^2\), increasing the denominator in the
variance formula and reducing the variance of \(b_k\).

However, moving these variables from the explained part of the model
to the unexplained part may cause a violation of mean independence.

In particular, the nature of multicollinearity is that one variable
is highly predictive of another. If one of these variables is moved to
the unobserved part of the model, the remaining variables will be highly
predictive of the disturbance, which is exactly the situation that
creates a violation of mean independence.

</blockquote>
