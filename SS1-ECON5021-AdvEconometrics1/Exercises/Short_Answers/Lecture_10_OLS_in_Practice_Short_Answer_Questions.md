# Lecture 10 OLS in Practice Short Answer Questions

Question #1
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

Define the projection matrix for \(X\), \(\mathrm{P}_X\).

Show that \[
\mathrm{P}_XH=0.
\]

State the result from part (b) in words.

Consider predicting the OLS errors using \(X\): \[
\hat{e}_i=
x_{i1}a_1+
x_{i2}a_2+
\cdots+
x_{iK}a_K.
\]

Show that the OLS coefficient vector \(a\) is equal to zero.

Question #2
Let \(Y\), \(Z\), \(X\), and \(\pmb{\varepsilon}\) be \(n\times1\) vectors related by \[
Y=\tau Z+\kappa X+\pmb{\varepsilon}.
\]

Suppose every element of \(Z\) is
equal to 1. For context, let \(Y\)
denote total sales across \(n\)
observations, \(X\) the price at each
observation, and \(\pmb{\varepsilon}\)
all other factors affecting sales.

Define the projection matrix for \(Z\) as \[
P_Z=Z(Z'Z)^{-1}Z'.
\] Describe \(P_Z\) completely.
What are its dimensions, and what is the value of every element of the
matrix?

Consider the matrix product \(P_ZX\). Describe the result completely.
What are its dimensions, and what is the value of every element of the
resulting vector?

Define the residual-maker matrix for \(Z\) as \[
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

Question #3
Suppose that the one-way ticket price, \(fare_i\), for airline ticket \(i\) is related to distance, measured in
hundreds of miles, \(dist_i\), by \[
\log(fare_i)
=
4.666
+
0.043\,dist_i.
\]

Write \(fare_i\) as a function
of \(dist_i\) rather than \(\log(fare_i)\).

What is the marginal effect of \(dist_i\) on \(fare_i\)? \[
\frac{\partial fare_i}{\partial dist_i}
\]

Let \[
100\frac{\partial fare_i}{fare_i}
\] approximate the percentage change in \(fare_i\). Show that the coefficient \(0.043\) implies that increasing distance by
1 mile, rather than increasing \(dist_i\) by one unit (which corresponds to
100 miles), is associated with an approximate \(0.043\%\) increase in fare.

Question #4
Suppose that the one-way ticket price, \(fare_i\), for airline ticket \(i\) is related to distance, measured in
hundreds of miles, \(dist_i\), by \[
fare_i = 41 + 66\log(dist_i)
\]

What is the marginal effect of \(dist_i\) on \(fare_i\)? \[
\frac{\partial fare_i}{\partial dist_i}
\]

Let \[
100\frac{\partial dist_i}{dist_i}
\] approximate the percentage change in \(dist_i\). Re-write the marginal effect to
indicate that the formula above shows that a 1% increase in \(dist_i\) corresponds to a $0.66 increase in
\(fare_i\).

Show that the interpretation of the coefficient \(66\) does not depend on the units of \(dist_i\). For example, if \(dist_i\) were measured in miles instead of
hundreds of miles, show that a 1% increase in distance would still
increase \(fare_i\) by approximately
$0.66.

Question #5
Suppose that the one-way ticket price, \(fare_i\), for airline ticket \(i\) is related to distance, measured in
hundreds of miles, \(dist_i\), by \[
\log(fare_i)
=
4.25+0.40\log(dist_i).
\]

Write \(fare_i\) as a function
of \(dist_i\) rather than \(\log(fare_i)\).

What is the marginal effect of \(dist_i\) on \(fare_i\)? \[
\frac{\partial fare_i}{\partial dist_i}
\]

Let \[
100\frac{\partial fare_i}{fare_i}
\qquad\text{and}\qquad
100\frac{\partial dist_i}{dist_i}
\] approximate the percentage changes in \(fare_i\) and \(dist_i\), respectively. Show that the
coefficient \(0.40\) implies that a 10%
increase in distance is associated with an approximate 4% increase in
fare.
