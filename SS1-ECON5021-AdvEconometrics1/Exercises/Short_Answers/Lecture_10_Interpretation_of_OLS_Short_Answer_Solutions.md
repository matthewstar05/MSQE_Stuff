# Lecture 10 Interpretation of OLS Short Answer Solutions

# Question #1

The OLS estimator is \[
b=(X'X)^{-1}X'Y,
\] where \(X\) is \(n\times K\), \(Y\) is \(n\times
1\), and \(b\) is \(K\times 1\).

Define the prediction error associated with the OLS coefficients as
\[
e_i=y_i-x_i'b.
\]

Let \(H\) denote the \(n\times 1\) vector of OLS prediction
errors: \[
H=
\begin{bmatrix}
e_1\\
e_2\\
\vdots\\
e_n
\end{bmatrix}.
\]

- Define the projection matrix for \(X\), \(\mathrm{P}_X\).

<blockquote>
<strong>Solution:</strong>

The projection matrix for \(X\) is
\[
\mathrm{P}_X=
X(X'X)^{-1}X'.
\]

</blockquote>

- Show that \[
\mathrm{P}_XH=0.
\]

<blockquote>
<strong>Solution:</strong>

Since \[
H=Y-Xb,
\] we have \[
\begin{aligned}
\mathrm{P}_XH
&amp;=X(X'X)^{-1}X'(Y-Xb)\\
&amp;=X(X'X)^{-1}X'Y-X(X'X)^{-1}X'Xb.
\end{aligned}
\]

Using \[
b=(X'X)^{-1}X'Y,
\] it follows that \[
\mathrm{P}_XH=
Xb-Xb=0.
\]

</blockquote>

- State the result from part (b) in words.

<blockquote>
<strong>Solution:</strong>

The OLS prediction errors cannot be predicted by a linear combination
of the columns of \(X\).

</blockquote>

- Consider predicting the OLS errors using \(X\): \[
\hat{e}_i=
x_{i1}a_1+
x_{i2}a_2+
\cdots+
x_{iK}a_K.
\]

Show that the OLS coefficient vector \(a\) is equal to zero.

<blockquote>
<strong>Solution:</strong>

Using \(H\) as the dependent
variable, the OLS estimator is \[
a=(X'X)^{-1}X'H.
\]

Since \[
H=Y-Xb,
\] we have \[
\begin{aligned}
a&amp;=(X'X)^{-1}X'(Y-Xb)\\
&amp;=(X'X)^{-1}X'Y-(X'X)^{-1}X'Xb\\
&amp;=b-b\\
&amp;=0.
\end{aligned}
\]
</blockquote>

# Question #2

Let \(Y\), \(Z\), \(X\), and \(\pmb{\varepsilon}\) be \(n\times1\) vectors related by \[
Y=\tau Z+\kappa X+\pmb{\varepsilon}.
\]

Suppose every element of \(Z\) is
equal to 1. For context, let \(Y\)
denote total sales across \(n\)
observations, \(X\) the price at each
observation, and \(\pmb{\varepsilon}\)
all other factors affecting sales.

- Define the projection matrix for \(Z\) as \[
P_Z=Z(Z'Z)^{-1}Z'.
\] Describe \(P_Z\) completely.
What are its dimensions, and what is the value of every element of the
matrix?

<blockquote>
<strong>Solution:</strong>

Since \(Z\) is an \(n\times1\) vector of ones, \[
Z'Z
=
\sum_{i=1}^n 1\cdot1
=
n.
\]

Therefore, \[
P_Z
=
Z(Z'Z)^{-1}Z'
=
\frac{1}{n}ZZ'.
\]

Since \[
ZZ'
=
\begin{bmatrix}
1\\
1\\
\vdots\\
1
\end{bmatrix}
\begin{bmatrix}
1&amp;1&amp;\cdots&amp;1
\end{bmatrix}
=
\mathbf{1}_{n\times n},
\] where \(\mathbf{1}_{n\times
n}\) is an \(n\times n\) matrix
of ones, \[
P_Z
=
\frac{1}{n}\mathbf{1}_{n\times n}.
\]

Thus, \(P_Z\) is an \(n\times n\) matrix in which every element
is \(1/n\).

</blockquote>

- Consider the matrix product \(P_ZX\). Describe the result completely.
What are its dimensions, and what is the value of every element of the
resulting vector?

<blockquote>
<strong>Solution:</strong>

Since \(P_Z\) is \(n\times n\) and \(X\) is \(n\times1\), \(P_ZX\) is \(n\times1\).

Since every element of \(P_Z\) is
\(1/n\), \[
P_ZX
=
\begin{bmatrix}
\displaystyle \frac{1}{n}\sum_{i=1}^n x_i\\
\displaystyle \frac{1}{n}\sum_{i=1}^n x_i\\
\vdots\\
\displaystyle \frac{1}{n}\sum_{i=1}^n x_i
\end{bmatrix}
=
\begin{bmatrix}
\bar{x}\\
\bar{x}\\
\vdots\\
\bar{x}
\end{bmatrix}.
\]

Thus, every element of \(P_ZX\) is
the sample average of the observations in \(X\).

</blockquote>

- Define the residual-maker matrix for \(Z\) as \[
M_Z
=
I-Z(Z'Z)^{-1}Z'.
\] Multiplying the model by \(M_Z\) gives \[
Y^*=
\kappa X^*+
\pmb{\varepsilon}^*,
\] Describe \(X^*\) in this
equation completely. What are its dimensions, and what is the value of
every element of the vector?

<blockquote>
<strong>Solution:</strong>

Work this out on your own.
</blockquote>
