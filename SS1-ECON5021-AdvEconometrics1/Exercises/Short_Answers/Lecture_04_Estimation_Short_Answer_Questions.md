# Lecture 04 Estimation Short Answer Questions

Question #1
Suppose we observe a sample of \(n\)
observations of a variable \(x\) that
are independent and identically distributed, with \[
\mathrm{E}(x_i)=\mu,
\qquad
\mathrm{Var}(x_i)=\sigma^2.
\]

Let \[
x=
\begin{bmatrix}
x_1\\
x_2\\
\vdots\\
x_n
\end{bmatrix}
\] denote the \(n\times 1\)
vector of observations, and let \(a\)
be an \(n\times 1\) vector of ones. The
sample mean can be written as \[
\bar{x}=n^{-1}a'x.
\]

Prove that \(\bar{x}\) is an
unbiased estimator of \(\mu\) by
showing that \(\mathrm{E}(\bar{x})=\mu\). In your answer,
explain the role of independence in establishing unbiasedness and the
role of identical distributions in establishing unbiasedness. Also
explain how the observations could fail to satisfy one or both of these
assumptions while \(\bar{x}\) remains
unbiased for \(\mu\).

Question #2
Suppose we observe a sample of \(n\)
observations of a variable \(x\) that
are independent and identically distributed, with \[
\mathrm{E}(x_i)=\mu,
\qquad
\mathrm{Var}(x_i)=\sigma^2.
\]

Let \[
x=
\begin{bmatrix}
x_1\\
x_2\\
\vdots\\
x_n
\end{bmatrix}
\] denote the \(n\times 1\)
vector of observations, and let \(a\)
be an \(n\times 1\) vector of ones. The
sample mean can be written as \[
\bar{x}=n^{-1}a'x.
\]

Prove that the variance of the sample mean is \[
\mathrm{Var}(\bar{x})=\frac{\sigma^2}{n}.
\] In your answer, explain how the variance-covariance matrix
\(\mathrm{Var}(x)\) is constructed and
the role of independence and identical distributions in determining its
elements.

Question #3
Suppose we observe a sample of \(n\)
observations of a variable \(x\) that
are independent but *not* identically distributed, with \[
\mathrm{E}(x_i)=\mu,
\qquad
\mathrm{Var}(x_i)=\sigma_i^2.
\]

Let \[
x=
\begin{bmatrix}
x_1\\
x_2\\
\vdots\\
x_n
\end{bmatrix}
\] denote the \(n\times 1\)
vector of observations, and let \(a\)
be an \(n\times 1\) vector of ones. The
sample mean can be written as \[
\bar{x}=n^{-1}a'x.
\]

Derive the formula for \(\mathrm{Var}(\bar{x})\). Express your final
answer in scalar summation notation rather than matrix notation.

Question #4
Suppose we observe a sample of \(n\)
observations of a variable \(x\) that
are *not* independent but are identically distributed, with \[
\mathrm{E}(x_i)=\mu,
\qquad
\mathrm{Var}(x_i)=\sigma^2.
\]

Suppose the observations have the following dependence structure:
\[
\mathrm{Cov}(x_i,x_{i-1})=\gamma,
\qquad i=2,\ldots,n,
\] and \[
\mathrm{Cov}(x_i,x_{i-j})=0,
\qquad j&gt;1.
\]

Let \[
x=
\begin{bmatrix}
x_1\\
x_2\\
\vdots\\
x_n
\end{bmatrix}
\] denote the \(n\times 1\)
vector of observations, and let \(a\)
be an \(n\times 1\) vector of ones. The
sample mean can be written as \[
\bar{x}=n^{-1}a'x.
\]

Derive the formula for \(\mathrm{Var}(\bar{x})\). Express your final
answer in scalar notation rather than matrix notation.
