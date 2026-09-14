"""
ECON 5015: Homework 2
Matthew Suban
@matthewsuban
"""

a = [] # 1-100
for i in range(1, 101):
    a.append(i)

b = [] # (1-100)^2
for i in range(1, 101):
    b.append(i * i)

c = [] # (1-100)*(1-100+1)/2
for n in range(1, 101):
    c.append(n * (n + 1) // 2)

d = [] # x e c is divisible by 3, bool
for x in c:
    d.append(x % 3 == 0)

e = [] # indicies of x e c // 3 == 0
for i in range(len(c)):
    if c[i] % 3 == 0:
        e.append(i)

f = [] # x e c is divisible by 3, numbers
for x in c:
    if x % 3 == 0:
        f.append(x)

g = [b[0]] # sum of b
for i in range(1, len(b)):
    g.append(b[i] + g[i - 1])
