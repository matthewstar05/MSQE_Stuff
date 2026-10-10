# Lecture 02 Expected Value Short Answer Questions

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

Show that if \(y\) is mean
independent of \(x\) then \[
\mathrm{E}(xy) = \mathrm{E}(x)\mathrm{E}(y).
\]

Using the definition of covariance, show that if \[
\mathrm{E}(xy) = \mathrm{E}(x)\mathrm{E}(y),
\] then \(\mathrm{Cov}(x,y) =
0\).

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

Show that if the covariance of daily returns is zero and \(\mathrm{E}(x_t)=\mathrm{E}(x_{t+1})=\mu\),
then \[
\mathrm{E}(R_{\mathrm{2d}}) = (1 + \mu)^2 - 1.
\]
