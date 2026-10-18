# Lecture 12 OLS in Practice Short Answer Solutions

# Question #1

Suppose that the one-way ticket price, \(fare_i\), for airline ticket \(i\) is related to distance, measured in
hundreds of miles, \(dist_i\), by \[
\log(fare_i)
=
4.666
+
0.043\,dist_i.
\]

- Write \(fare_i\) as a function of
\(dist_i\) rather than \(\log(fare_i)\).

<blockquote>
<strong>Solution:</strong>

Exponentiating both sides, \[
fare_i
=
\exp\left(4.666+0.043\,dist_i\right).
\]

</blockquote>

- What is the marginal effect of \(dist_i\) on \(fare_i\)? \[
\frac{\partial fare_i}{\partial dist_i}
\]

<blockquote>
<strong>Solution:</strong>

\[
\frac{\partial fare_i}{\partial dist_i}
=
\exp\left(4.666+0.043\,dist_i\right)(0.043)
=
0.043\,fare_i.
\]

</blockquote>

- Let \[
100\frac{\partial fare_i}{fare_i}
\] approximate the percentage change in \(fare_i\). Show that the coefficient \(0.043\) implies that increasing distance by
1 mile, rather than increasing \(dist_i\) by one unit (which corresponds to
100 miles), is associated with an approximate \(0.043\%\) increase in fare.

<blockquote>
<strong>Solution:</strong>

See lecture notes.
</blockquote>

# Question #2

Suppose that the one-way ticket price, \(fare_i\), for airline ticket \(i\) is related to distance, measured in
hundreds of miles, \(dist_i\), by \[
fare_i = 41 + 66\log(dist_i)
\]

- What is the marginal effect of \(dist_i\) on \(fare_i\)? \[
\frac{\partial fare_i}{\partial dist_i}
\]

<blockquote>
<strong>Solution:</strong>

\[
\frac{\partial fare_i}{\partial dist_i}
=
\frac{66}{dist_i}
\]

</blockquote>

- Let \[
100\frac{\partial dist_i}{dist_i}
\] approximate the percentage change in \(dist_i\). Re-write the marginal effect to
indicate that the formula above shows that a 1% increase in \(dist_i\) corresponds to a $0.66 increase in
\(fare_i\).

<blockquote>
<strong>Solution:</strong>

Re-arranging the marignal effect \[
\frac{\partial fare_i}{\frac{\partial dist_i}{dist_i}} = 66
\] \[
\frac{\partial fare_i}{100\frac{\partial dist_i}{dist_i}} =
\frac{66}{100} = 0.66
\]

</blockquote>

- Show that the interpretation of the coefficient \(66\) does not depend on the units of \(dist_i\). For example, if \(dist_i\) were measured in miles instead of
hundreds of miles, show that a 1% increase in distance would still
increase \(fare_i\) by approximately
$0.66.

<blockquote>
<strong>Solution:</strong>

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

</blockquote>

# Question #3

Suppose that the one-way ticket price, \(fare_i\), for airline ticket \(i\) is related to distance, measured in
hundreds of miles, \(dist_i\), by \[
\log(fare_i)
=
4.25+0.40\log(dist_i).
\]

- Write \(fare_i\) as a function of
\(dist_i\) rather than \(\log(fare_i)\).

<blockquote>
<strong>Solution:</strong>

See the lecture notes.

</blockquote>

- What is the marginal effect of \(dist_i\) on \(fare_i\)? \[
\frac{\partial fare_i}{\partial dist_i}
\]

<blockquote>
<strong>Solution:</strong>

See the lecture notes.

</blockquote>

- Let \[
100\frac{\partial fare_i}{fare_i}
\qquad\text{and}\qquad
100\frac{\partial dist_i}{dist_i}
\] approximate the percentage changes in \(fare_i\) and \(dist_i\), respectively. Show that the
coefficient \(0.40\) implies that a 10%
increase in distance is associated with an approximate 4% increase in
fare.

<blockquote>
<strong>Solution:</strong>

See the lecture notes.
</blockquote>
