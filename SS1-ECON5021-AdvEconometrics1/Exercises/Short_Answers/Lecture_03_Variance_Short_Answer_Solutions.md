# Lecture 03 Variance Short Answer Solutions

Question #1
Suppose \(x_1\) and \(x_2\) are random variables and \(a_1\) and \(a_2\) are constants. Define \[
w = a_1 x_1 + a_2 x_2.
\] The variance of \(w\) is
\[
\mathrm{Var}(w)
=
a_1^2 \mathrm{Var}(x_1)
+
a_2^2 \mathrm{Var}(x_2)
+
2a_1a_2\mathrm{Cov}(x_1,x_2).
\]

Use the definition of variance, \[
\mathrm{Var}(w)=\mathrm{E}\left[(w-\mathrm{E}(w))^2\right],
\] to show that the variance formula given above is correct.

**Solution:**

First, \[
\begin{aligned}
\mathrm{E}(w)
&amp;=
\mathrm{E}(a_1x_1+a_2x_2) \\
&amp;=
a_1\mathrm{E}(x_1)+a_2\mathrm{E}(x_2).
\end{aligned}
\]

Therefore, \[
\begin{aligned}
w-\mathrm{E}(w)
&amp;=
a_1x_1+a_2x_2
-
\left[
a_1\mathrm{E}(x_1)+a_2\mathrm{E}(x_2)
\right] \\
&amp;=
a_1\left[x_1-\mathrm{E}(x_1)\right]
+
a_2\left[x_2-\mathrm{E}(x_2)\right].
\end{aligned}
\]

Using the definition of variance, \[
\begin{aligned}
\mathrm{Var}(w)
&amp;=
\mathrm{E}\left[
\left(
a_1[x_1-\mathrm{E}(x_1)]
+
a_2[x_2-\mathrm{E}(x_2)]
\right)^2
\right] \\
&amp;=
\mathrm{E}\left[
a_1^2[x_1-\mathrm{E}(x_1)]^2
+
a_2^2[x_2-\mathrm{E}(x_2)]^2
+
2a_1a_2[x_1-\mathrm{E}(x_1)][x_2-\mathrm{E}(x_2)]
\right] \\
&amp;=
a_1^2\mathrm{E}\left[[x_1-\mathrm{E}(x_1)]^2\right]
+
a_2^2\mathrm{E}\left[[x_2-\mathrm{E}(x_2)]^2\right] \\
&amp;\qquad
+
2a_1a_2
\mathrm{E}\left[
[x_1-\mathrm{E}(x_1)][x_2-\mathrm{E}(x_2)]
\right] \\
&amp;=
a_1^2 \mathrm{Var}(x_1)
+
a_2^2 \mathrm{Var}(x_2)
+
2a_1a_2 \mathrm{Cov}(x_1,x_2).
\end{aligned}
\]

Define the \(2 \times 1\) vectors
\[
a = \begin{bmatrix} a_1 \\ a_2 \end{bmatrix},
\qquad
x = \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}.
\] Show, using matrix algebra, that \[
\mathrm{Var}(w)=\mathrm{Var}(a'x)=a'\mathrm{Var}(x)a
\] also yields the same equation above. Make sure to first define
the elements of the \(2 \times 2\)
matrix \(\mathrm{Var}(x)\).

**Solution:**

The variance-covariance matrix of \(x\) is \[
\mathrm{Var}(x)
=
\begin{bmatrix}
\mathrm{Var}(x_1) &amp; \mathrm{Cov}(x_1,x_2) \\
\mathrm{Cov}(x_2,x_1) &amp; \mathrm{Var}(x_2)
\end{bmatrix}.
\]

Since covariance is symmetric, \[
\mathrm{Cov}(x_1,x_2)=\mathrm{Cov}(x_2,x_1).
\]

Now compute \[
\begin{aligned}
a'\mathrm{Var}(x)a
&amp;=
\begin{bmatrix}
a_1 &amp; a_2
\end{bmatrix}
\begin{bmatrix}
\mathrm{Var}(x_1) &amp; \mathrm{Cov}(x_1,x_2) \\
\mathrm{Cov}(x_2,x_1) &amp; \mathrm{Var}(x_2)
\end{bmatrix}
\begin{bmatrix}
a_1 \\
a_2
\end{bmatrix}.
\end{aligned}
\]

First multiply the matrix by \(a\):
\[
\begin{aligned}
\mathrm{Var}(x)a
&amp;=
\begin{bmatrix}
\mathrm{Var}(x_1) &amp; \mathrm{Cov}(x_1,x_2) \\
\mathrm{Cov}(x_2,x_1) &amp; \mathrm{Var}(x_2)
\end{bmatrix}
\begin{bmatrix}
a_1 \\
a_2
\end{bmatrix} \\
&amp;=
\begin{bmatrix}
a_1\mathrm{Var}(x_1)+a_2\mathrm{Cov}(x_1,x_2) \\
a_1\mathrm{Cov}(x_2,x_1)+a_2\mathrm{Var}(x_2)
\end{bmatrix}.
\end{aligned}
\]

Then multiply by \(a'\): \[
\begin{aligned}
a'\mathrm{Var}(x)a
&amp;=
\begin{bmatrix}
a_1 &amp; a_2
\end{bmatrix}
\begin{bmatrix}
a_1\mathrm{Var}(x_1)+a_2\mathrm{Cov}(x_1,x_2) \\
a_1\mathrm{Cov}(x_2,x_1)+a_2\mathrm{Var}(x_2)
\end{bmatrix} \\
&amp;=
a_1^2\mathrm{Var}(x_1)
+
a_1a_2\mathrm{Cov}(x_1,x_2)
+
a_1a_2\mathrm{Cov}(x_2,x_1)
+
a_2^2\mathrm{Var}(x_2) \\
&amp;=
a_1^2\mathrm{Var}(x_1)
+
2a_1a_2\mathrm{Cov}(x_1,x_2)
+
a_2^2\mathrm{Var}(x_2).
\end{aligned}
\]

Thus, \[
\mathrm{Var}(a'x)
=
a'\mathrm{Var}(x)a
=
a_1^2 \mathrm{Var}(x_1)
+
a_2^2 \mathrm{Var}(x_2)
+
2a_1a_2\mathrm{Cov}(x_1,x_2).
\]

Question #2
Define \(X\) as an \(n \times 1\) random vector. The variance of
the random vector \(X\) is defined as
\[
\mathrm{Var}(X)
=
\mathrm{E}\left[
(X-\mathrm{E}(X))(X-\mathrm{E}(X))'
\right],
\] where \('\) indicates
transpose.

Use the properties of expectation and matrix algebra to show that
the variance can also be written as \[
\mathrm{Var}(X)
=
\mathrm{E}(XX')-\mathrm{E}(X)\mathrm{E}(X)'.
\]

**Solution:**

Starting from the definition, \[
\mathrm{Var}(X)
=
\mathrm{E}\left[
(X-\mathrm{E}(X))(X-\mathrm{E}(X))'
\right].
\]

Expand the product inside the expectation: \[
\begin{aligned}
(X-\mathrm{E}(X))(X-\mathrm{E}(X))'
&amp;=
(X-\mathrm{E}(X))(X'-\mathrm{E}(X)') \\
&amp;=
XX'
-
X\mathrm{E}(X)'
-
\mathrm{E}(X)X'
+
\mathrm{E}(X)\mathrm{E}(X)'.
\end{aligned}
\]

Taking expectations, \[
\begin{aligned}
\mathrm{Var}(X)
&amp;=
\mathrm{E}\left[
XX'
-
X\mathrm{E}(X)'
-
\mathrm{E}(X)X'
+
\mathrm{E}(X)\mathrm{E}(X)'
\right] \\
&amp;=
\mathrm{E}(XX')
-
\mathrm{E}\left[X\mathrm{E}(X)'\right]
-
\mathrm{E}\left[\mathrm{E}(X)X'\right]
+
\mathrm{E}\left[\mathrm{E}(X)\mathrm{E}(X)'\right].
\end{aligned}
\]

Since \(\mathrm{E}(X)\) is not
random, \[
\mathrm{E}\left[X\mathrm{E}(X)'\right]
=
\mathrm{E}(X)\mathrm{E}(X)',
\] \[
\mathrm{E}\left[\mathrm{E}(X)X'\right]
=
\mathrm{E}(X)\mathrm{E}(X)',
\] and \[
\mathrm{E}\left[\mathrm{E}(X)\mathrm{E}(X)'\right]
=
\mathrm{E}(X)\mathrm{E}(X)'.
\]

Therefore, \[
\begin{aligned}
\mathrm{Var}(X)
&amp;=
\mathrm{E}(XX')
-
\mathrm{E}(X)\mathrm{E}(X)'
-
\mathrm{E}(X)\mathrm{E}(X)'
+
\mathrm{E}(X)\mathrm{E}(X)' \\
&amp;=
\mathrm{E}(XX')-\mathrm{E}(X)\mathrm{E}(X)'.
\end{aligned}
\]

Now let \(A\) be an \(n \times m\) matrix and define \[
b=A'X.
\] Since \(X\) is \(n \times 1\), \(b\) is an \(m
\times 1\) random vector. Show using the initial definition of
variance applied to \(b\) that \[
\mathrm{Var}(b)
=
\mathrm{E}\left[
(b-\mathrm{E}(b))(b-\mathrm{E}(b))'
\right]=A'\mathrm{Var}(X)A.
\]

**Solution:**

Start with the initial definition of variance applied to \(b\): \[
\mathrm{Var}(b)
=
\mathrm{E}\left[
(b-\mathrm{E}(b))(b-\mathrm{E}(b))'
\right].
\]

Since \[
b=A'X,
\] we have \[
\mathrm{E}(b)
=
\mathrm{E}(A'X)
=
A'\mathrm{E}(X).
\]

Therefore, \[
\begin{aligned}
b-\mathrm{E}(b)
&amp;=
A'X-A'\mathrm{E}(X) \\
&amp;=
A'(X-\mathrm{E}(X)).
\end{aligned}
\]

Substitute this into the definition of \(\mathrm{Var}(b)\): \[
\begin{aligned}
\mathrm{Var}(b)
&amp;=
\mathrm{E}\left[
A'(X-\mathrm{E}(X))
\left(A'(X-\mathrm{E}(X))\right)'
\right].
\end{aligned}
\]

Using the transpose rule, \[
\left(A'(X-\mathrm{E}(X))\right)'
=
(X-\mathrm{E}(X))'A.
\]

Therefore, \[
\begin{aligned}
\mathrm{Var}(b)
&amp;=
\mathrm{E}\left[
A'(X-\mathrm{E}(X))(X-\mathrm{E}(X))'A
\right] \\
&amp;=
A'
\mathrm{E}\left[
(X-\mathrm{E}(X))(X-\mathrm{E}(X))'
\right]
A.
\end{aligned}
\]

By the definition of \(\mathrm{Var}(X)\), \[
\mathrm{Var}(X)
=
\mathrm{E}\left[
(X-\mathrm{E}(X))(X-\mathrm{E}(X))'
\right].
\]

Thus, \[
\mathrm{Var}(b)
=
A'\mathrm{Var}(X)A.
\]

Now, show using the definition of variance in part (a) applied to
\(b\) that \[
\mathrm{Var}(b)
=
\mathrm{E}(bb')-\mathrm{E}(b)\mathrm{E}(b)'
=
A'\mathrm{Var}(X)A
\]

**Solution:**

Using the variance formula from part (a), applied to \(b\), \[
\mathrm{Var}(b)
=
\mathrm{E}(bb')-\mathrm{E}(b)\mathrm{E}(b)'.
\]

Since \(b=A'X\), \[
bb'
=
(A'X)(A'X)'.
\]

Using the transpose rule, \[
(A'X)'=X'A.
\]

Therefore, \[
bb'
=
A'XX'A.
\]

Taking expectations, \[
\begin{aligned}
\mathrm{E}(bb')
&amp;=
\mathrm{E}(A'XX'A) \\
&amp;=
A'\mathrm{E}(XX')A.
\end{aligned}
\]

Next, \[
\mathrm{E}(b)
=
\mathrm{E}(A'X)
=
A'\mathrm{E}(X).
\]

Therefore, \[
\begin{aligned}
\mathrm{E}(b)\mathrm{E}(b)'
&amp;=
A'\mathrm{E}(X)
\left(A'\mathrm{E}(X)\right)' \\
&amp;=
A'\mathrm{E}(X)\mathrm{E}(X)'A.
\end{aligned}
\]

Substitute these into the variance formula for \(b\): \[
\begin{aligned}
\mathrm{Var}(b)
&amp;=
\mathrm{E}(bb')-\mathrm{E}(b)\mathrm{E}(b)' \\
&amp;=
A'\mathrm{E}(XX')A
-
A'\mathrm{E}(X)\mathrm{E}(X)'A \\
&amp;=
A'
\left[
\mathrm{E}(XX')-\mathrm{E}(X)\mathrm{E}(X)'
\right]
A.
\end{aligned}
\]

From part (a), \[
\mathrm{Var}(X)
=
\mathrm{E}(XX')-\mathrm{E}(X)\mathrm{E}(X)'.
\]

Therefore, \[
\mathrm{Var}(b)
=
A'\mathrm{Var}(X)A.
\]
