# Lecture 10 Interpretation of OLS Short Answer Questions

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

- Show that \[
\mathrm{P}_XH=0.
\]

- State the result from part (b) in words.

- Consider predicting the OLS errors using \(X\): \[
\hat{e}_i=
x_{i1}a_1+
x_{i2}a_2+
\cdots+
x_{iK}a_K.
\]

Show that the OLS coefficient vector \(a\) is equal to zero.

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

- Consider the matrix product \(P_ZX\). Describe the result completely.
What are its dimensions, and what is the value of every element of the
resulting vector?

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
