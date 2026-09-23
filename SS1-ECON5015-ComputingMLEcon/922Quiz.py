x = [0, 0, 1, 1]

# n arithmetic mean problem
sum = 0
for i in x:
    sum = sum + i
m = sum / len(x)
print(m)


# n-1 largest arithmetic mean problem
skip = False
sum1 = 0
for j in x:
    if (j == 0 and skip == False):
        skip = True
    else:
        sum1 = sum1 + j
m1 = sum1 / (len(x)-1)
print(m1)