# Lecture 10 OLS in Practice Short Answer Solutions

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

**Solution:**

The projection matrix for \(X\) is
\[
\mathrm{P}_X=
X(X'X)^{-1}X'.
\]

Show that \[
\mathrm{P}_XH=0.
\]

**Solution:**

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

State the result from part (b) in words.

**Solution:**

The OLS prediction errors cannot be predicted by a linear combination
of the columns of \(X\).

Consider predicting the OLS errors using \(X\): \[
\hat{e}_i=
x_{i1}a_1+
x_{i2}a_2+
\cdots+
x_{iK}a_K.
\]

Show that the OLS coefficient vector \(a\) is equal to zero.

**Solution:**

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

**Solution:**

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

Consider the matrix product \(P_ZX\). Describe the result completely.
What are its dimensions, and what is the value of every element of the
resulting vector?

**Solution:**

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

**Solution:**

Work this out on your own.

Question #3
Suppose that the one-way ticket price, \(fare_i\), for airline ticket \(i\) is related to distance, measured in
hundreds of miles, \(dist_i\), by \[
\log(fare_i)
=
4.666
+
0.043\,dist_i.
\]

Write \(fare_i\) as a function of
\(dist_i\) rather than \(\log(fare_i)\).

**Solution:**

Exponentiating both sides, \[
fare_i
=
\exp\left(4.666+0.043\,dist_i\right).
\]

What is the marginal effect of \(dist_i\) on \(fare_i\)? \[
\frac{\partial fare_i}{\partial dist_i}
\]

**Solution:**

\[
\frac{\partial fare_i}{\partial dist_i}
=
\exp\left(4.666+0.043\,dist_i\right)(0.043)
=
0.043\,fare_i.
\]

Let \[
100\frac{\partial fare_i}{fare_i}
\] approximate the percentage change in \(fare_i\). Show that the coefficient \(0.043\) implies that increasing distance by
1 mile, rather than increasing \(dist_i\) by one unit (which corresponds to
100 miles), is associated with an approximate \(0.043\%\) increase in fare.

**Solution:**

See lecture notes.

Question #4
Suppose that the one-way ticket price, \(fare_i\), for airline ticket \(i\) is related to distance, measured in
hundreds of miles, \(dist_i\), by \[
fare_i = 41 + 66\log(dist_i)
\]

What is the marginal effect of \(dist_i\) on \(fare_i\)? \[
\frac{\partial fare_i}{\partial dist_i}
\]

**Solution:**

\[
\frac{\partial fare_i}{\partial dist_i}
=
\frac{66}{dist_i}
\]

Let \[
100\frac{\partial dist_i}{dist_i}
\] approximate the percentage change in \(dist_i\). Re-write the marginal effect to
indicate that the formula above shows that a 1% increase in \(dist_i\) corresponds to a $0.66 increase in
\(fare_i\).

**Solution:**

Re-arranging the marignal effect \[
\frac{\partial fare_i}{\frac{\partial dist_i}{dist_i}} = 66
\] \[
\frac{\partial fare_i}{100\frac{\partial dist_i}{dist_i}} =
\frac{66}{100} = 0.66
\]

Show that the interpretation of the coefficient \(66\) does not depend on the units of \(dist_i\). For example, if \(dist_i\) were measured in miles instead of
hundreds of miles, show that a 1% increase in distance would still
increase \(fare_i\) by approximately
$0.66.

**Solution:**

If \(dist_i\) is measured in miles,
then the original variable measured in hundreds of miles is \(dist_i/100\). The model becomes \[
fare_i
=
41+66\log(dist_i/100).
\]

Using the properties of logarithms, \[
\begin{aligned}
fare_i
&amp;=
41+66\left[\log(dist_i)-\log(100)\right]\\
&amp;=
\left(41-66\log(100)\right)+
66\log(dist_i).
\end{aligned}
\]

Changing the units of distance changes only the intercept. The slope
coefficient on \(\log(dist_i)\) remains
\(66\), so its interpretation is
unchanged: a 1% increase in distance is associated with an approximate
$0.66 increase in \(fare_i\).

Question #5
Suppose that the one-way ticket price, \(fare_i\), for airline ticket \(i\) is related to distance, measured in
hundreds of miles, \(dist_i\), by \[
\log(fare_i)
=
4.25+0.40\log(dist_i).
\]

Write \(fare_i\) as a function of
\(dist_i\) rather than \(\log(fare_i)\).

**Solution:**

See the lecture notes.

What is the marginal effect of \(dist_i\) on \(fare_i\)? \[
\frac{\partial fare_i}{\partial dist_i}
\]

**Solution:**

See the lecture notes.

Let \[
100\frac{\partial fare_i}{fare_i}
\qquad\text{and}\qquad
100\frac{\partial dist_i}{dist_i}
\] approximate the percentage changes in \(fare_i\) and \(dist_i\), respectively. Show that the
coefficient \(0.40\) implies that a 10%
increase in distance is associated with an approximate 4% increase in
fare.

**Solution:**

See the lecture notes.
