# Lecture 02 Expected Value Short Answer Solutions

Question #1
Suppose \(y\) is a random variable
with density function \(f(y)\). \(y\) is independent of \(x\) if \[
f(y \mid x) = f(y),
\] where \(f(y \mid x)\) is the
conditional density of \(y\) given
\(x\). \(y\) is mean independent of \(x\) if \[
\mathrm{E}(y \mid x)=\mathrm{E}(y).
\] The covariance of \(y\) and
\(x\) is defined as \[
\mathrm{Cov}(y, x)
=
\mathrm{E} \left[(y - \mathrm{E}(y))(x - \mathrm{E}(x))\right].
\]

Use the definition of expected value, \[
\mathrm{E}(y) = \int y f(y) dy,
\] to show that if \(y\) is
independent of \(x\) then \(y\) is mean independent of \(x\).

**Solution:**

If \(y\) is independent of \(x\), then \[
f(y \mid x)=f(y).
\] Therefore, \[
\begin{aligned}
\mathrm{E}(y \mid x)
&amp;=
\int y f(y \mid x) dy \\
&amp;=
\int y f(y) dy \\
&amp;=
\mathrm{E}(y).
\end{aligned}
\] Thus, independence implies mean independence.

Show that if \(y\) is mean
independent of \(x\) then \[
\mathrm{E}(xy) = \mathrm{E}(x)\mathrm{E}(y).
\]

**Solution:**

Using the law of iterated expectations, \[
\begin{aligned}
\mathrm{E}(xy)
&amp;=
\mathrm{E}_x\left[\mathrm{E}(xy \mid x)\right] \\
&amp;=
\mathrm{E}_x\left[x \mathrm{E}(y \mid x)\right].
\end{aligned}
\] If \(y\) is mean independent
of \(x\), then \[
\mathrm{E}(y \mid x)=\mathrm{E}(y).
\] Therefore, \[
\begin{aligned}
\mathrm{E}(xy)
&amp;=
\mathrm{E}_x\left[x \mathrm{E}(y)\right] \\
&amp;=
\mathrm{E}(y)\mathrm{E}(x).
\end{aligned}
\] Thus, \[
\mathrm{E}(xy)=\mathrm{E}(x)\mathrm{E}(y).
\]

Using the definition of covariance, show that if \[
\mathrm{E}(xy) = \mathrm{E}(x)\mathrm{E}(y),
\] then \(\mathrm{Cov}(x,y) =
0\).

**Solution:**

By the definition of covariance, \[
\begin{aligned}
\mathrm{Cov}(x,y)
&amp;=
\mathrm{E}\left[(x-\mathrm{E}(x))(y-\mathrm{E}(y))\right] \\
&amp;=
\mathrm{E}\left[
xy
-
x\mathrm{E}(y)
-
y\mathrm{E}(x)
+
\mathrm{E}(x)\mathrm{E}(y)
\right] \\
&amp;=
\mathrm{E}(xy)
-
\mathrm{E}\left[x\mathrm{E}(y)\right]
-
\mathrm{E}\left[y\mathrm{E}(x)\right]
+
\mathrm{E}\left[\mathrm{E}(x)\mathrm{E}(y)\right] \\
&amp;=
\mathrm{E}(xy)
-
\mathrm{E}(y)\mathrm{E}(x)
-
\mathrm{E}(x)\mathrm{E}(y)
+
\mathrm{E}(x)\mathrm{E}(y) \\
&amp;=
\mathrm{E}(xy)
-
\mathrm{E}(x)\mathrm{E}(y).
\end{aligned}
\] If \[
\mathrm{E}(xy)=\mathrm{E}(x)\mathrm{E}(y),
\] then \[
\mathrm{Cov}(x,y)
=
\mathrm{E}(x)\mathrm{E}(y)
-
\mathrm{E}(x)\mathrm{E}(y)
=
0.
\]

Question #2
Let \(x_t\) be today’s return on an
asset and let \(x_{t+1}\) be tomorrow’s
return. The two-day return is given by \[
R_{\mathrm{2d}} = (1 + x_t)(1 + x_{t+1}) - 1.
\]

Show that the expected two-day return can be written as \[
\mathrm{E}(R_{\mathrm{2d}})
=
(1 + \mathrm{E}(x_t))(1 + \mathrm{E}(x_{t+1})) - 1 +
\mathrm{Cov}(x_t,x_{t+1}).
\]

**Solution:**

Start by expanding the two-day return: \[
\begin{aligned}
R_{\mathrm{2d}}
&amp;=
(1 + x_t)(1 + x_{t+1}) - 1 \\
&amp;=
1+x_t+x_{t+1}+x_tx_{t+1}-1 \\
&amp;=
x_t+x_{t+1}+x_tx_{t+1}.
\end{aligned}
\]

Taking expectations, \[
\begin{aligned}
\mathrm{E}(R_{\mathrm{2d}})
&amp;=
\mathrm{E}(x_t+x_{t+1}+x_tx_{t+1}) \\
&amp;=
\mathrm{E}(x_t)
+
\mathrm{E}(x_{t+1})
+
\mathrm{E}(x_tx_{t+1}).
\end{aligned}
\]

Using the covariance identity, \[
\mathrm{Cov}(x_t,x_{t+1})
=
\mathrm{E}(x_tx_{t+1})
-
\mathrm{E}(x_t)\mathrm{E}(x_{t+1}),
\] so \[
\mathrm{E}(x_tx_{t+1})
=
\mathrm{E}(x_t)\mathrm{E}(x_{t+1})
+
\mathrm{Cov}(x_t,x_{t+1}).
\]

Substituting, \[
\begin{aligned}
\mathrm{E}(R_{\mathrm{2d}})
&amp;=
\mathrm{E}(x_t)
+
\mathrm{E}(x_{t+1})
+
\mathrm{E}(x_t)\mathrm{E}(x_{t+1})
+
\mathrm{Cov}(x_t,x_{t+1}) \\
&amp;=
(1+\mathrm{E}(x_t))(1+\mathrm{E}(x_{t+1}))-1
+
\mathrm{Cov}(x_t,x_{t+1}).
\end{aligned}
\]

Show that if the covariance of daily returns is zero and \(\mathrm{E}(x_t)=\mathrm{E}(x_{t+1})=\mu\),
then \[
\mathrm{E}(R_{\mathrm{2d}}) = (1 + \mu)^2 - 1.
\]

**Solution:**

From part (a), \[
\mathrm{E}(R_{\mathrm{2d}})
=
(1+\mathrm{E}(x_t))(1+\mathrm{E}(x_{t+1}))-1
+
\mathrm{Cov}(x_t,x_{t+1}).
\]

If \(\mathrm{Cov}(x_t,x_{t+1})=0\),
then \[
\mathrm{E}(R_{\mathrm{2d}})
=
(1+\mathrm{E}(x_t))(1+\mathrm{E}(x_{t+1}))-1.
\]

If \(\mathrm{E}(x_t)=\mathrm{E}(x_{t+1})=\mu\),
then \[
\begin{aligned}
\mathrm{E}(R_{\mathrm{2d}})
&amp;=
(1+\mu)(1+\mu)-1 \\
&amp;=
(1+\mu)^2-1.
\end{aligned}
\]
