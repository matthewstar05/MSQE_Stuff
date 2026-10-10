# Lecture 08 LRM Short Answer Questions

Question #1
Let \(y\) be a random variable with
\(\mathrm{E}(y)=\mu\). The expected
squared error when \(a\) is used as a
prediction of \(y\) is \[
\mathrm{E}\left[(y-a)^2\right].
\]

Show that the value of \(a\) that
minimizes expected squared prediction error is the expected value of
\(y\).

Question #2
Let \(y\) be a random variable, and
let \[
m(x)=\mathrm{E}(y\mid x)
\] denote the conditional expectation function for \(y\).

Define \[
y=m(x)+u.
\] Show that \[
\mathrm{E}(u\mid x)=0.
\]

Let \(h(x)\) denote any function
of \(x\). Using the result from part
(a), show that \[
\mathrm{E}(h(x)u)=0.
\]

The expected squared error when the function \(g(x)\) is used as a prediction of \(y\) is \[
\mathrm{E}\left[(y-g(x))^2\right].
\]

Using the result from part (b), show that the function \(g(x)\) that minimizes expected squared
prediction error is the conditional expectation function \(m(x)\).

Question #3
The OLS estimator is \[
b=(X'X)^{-1}X'Y,
\] where \(X\) is \(n\times K\), \(Y\) is \(n\times
1\), and \(b\) is \(K\times 1\).

The OLS solution satisfies the first-order conditions \[
-2\sum_{i=1}^n
x_{ik}
\left(
y_i-x_{i1}b_1-x_{i2}b_2-\cdots-x_{iK}b_K
\right)
=
0,
\] for each \(k=1,2,\ldots,K\).

Define the OLS prediction error as \[
e_i=y_i-x_i'b.
\]

Suppose \(x_{i1}=1\) for all
\(i\), so that the first column of
\(X\) is a constant. Show that \[
\sum_{i=1}^n e_i=0.
\]

Suppose \(x_{i1}=1\) for all
\(i\). Show that \[
\bar{y}=\bar{x}'b,
\] where \[
\bar{y}=
\frac{1}{n}\sum_{i=1}^n y_i,
\qquad
\bar{x}=
\frac{1}{n}\sum_{i=1}^n x_i.
\]

Show that the OLS prediction errors have zero sample covariance
with each explanatory variable: \[
\widehat{\mathrm{Cov}}(x_k,e)=0,
\qquad
k=1,2,\ldots,K.
\] For this problem, define \[
\widehat{\mathrm{Cov}}(x_k,e)=
\frac{1}{n}
\sum_{i=1}^n
(x_{ik}-\bar{x}_k)(e_i-\bar{e}),
\] where \[
\bar{x}_k=
\frac{1}{n}\sum_{i=1}^n x_{ik},
\qquad
\bar{e}=
\frac{1}{n}\sum_{i=1}^n e_i.
\]

Question #4
The least squares estimator is \[
b=(X'X)^{-1}X'Y,
\] where \(X\) is \(n\times K\), \(Y\) is \(n\times
1\), and \(b\) is \(K\times 1\).

Consider the bivariate prediction equation \[
\hat{w}=b_1+b_2e.
\] For concreteness, let \(w\)
denote wage and let \(e\) denote
education. In this case, \(X\) is an
\(n\times 2\) matrix with a first
column of ones and a second column containing the observed values of
education: \[
X=
\begin{bmatrix}
1 &amp; e_1\\
1 &amp; e_2\\
\vdots &amp; \vdots\\
1 &amp; e_n
\end{bmatrix},
\qquad
Y=
\begin{bmatrix}
w_1\\
w_2\\
\vdots\\
w_n
\end{bmatrix}.
\]

Define the following sample averages: \[
\bar{e}
=
\frac{1}{n}\sum_{i=1}^n e_i,
\qquad
\overline{ee}
=
\frac{1}{n}\sum_{i=1}^n e_i^2,
\] \[
\bar{w}
=
\frac{1}{n}\sum_{i=1}^n w_i,
\qquad
\overline{ew}
=
\frac{1}{n}\sum_{i=1}^n e_iw_i.
\]

Starting from \(b=(X'X)^{-1}X'Y\), show that the
least squares estimator can be written as \[
b
=
\begin{bmatrix}
1 &amp; \bar{e}\\
\bar{e} &amp; \overline{ee}
\end{bmatrix}^{-1}
\begin{bmatrix}
\bar{w}\\
\overline{ew}
\end{bmatrix}.
\] In your derivation, explicitly show the matrix multiplication
using the elements of \(e\) and \(w\) that produce \(X'X\) and \(X'Y\), and then use the definitions of
the sample averages above to obtain the final expression.

Use matrix algebra to show that the slope estimator can be
written as \[
b_2
=
\frac{\widehat{\mathrm{Cov}}(e,w)}
{\widehat{\mathrm{Var}}(e)}.
\]

For this problem, define the sample covariance and variance as \[
\widehat{\mathrm{Cov}}(e,w)
=
\overline{ew}-\bar{e}\bar{w},
\qquad
\widehat{\mathrm{Var}}(e)
=
\overline{ee}-\bar{e}^{\,2}.
\]
