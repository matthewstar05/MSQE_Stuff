# Lecture 03 Variance Short Answer Questions

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
\] to show that the variance formula given above is
correct.

Define the \(2 \times 1\)
vectors \[
a = \begin{bmatrix} a_1 \\ a_2 \end{bmatrix},
\qquad
x = \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}.
\] Show, using matrix algebra, that \[
\mathrm{Var}(w)=\mathrm{Var}(a'x)=a'\mathrm{Var}(x)a
\] also yields the same equation above. Make sure to first define
the elements of the \(2 \times 2\)
matrix \(\mathrm{Var}(x)\).

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

Now, show using the definition of variance in part (a) applied to
\(b\) that \[
\mathrm{Var}(b)
=
\mathrm{E}(bb')-\mathrm{E}(b)\mathrm{E}(b)'
=
A'\mathrm{Var}(X)A
\]
