x = [0, 0, 1, 1]

# n arithmetic mean problem
def arithmetic_mean(x):
    sum = 0
    for i in x:
        sum = sum + i
    m = sum / len(x)
    return m


# n-1 largest arithmetic mean problem
def n1_arithmetic_mean(x):
    skip = False
    sum1 = 0
    for j in x:
        if (j == 0 and skip == False):
            skip = True
        else:
            sum1 = sum1 + j
    m1 = sum1 / (len(x)-1)
    return m1
    
print("arithmetic_mean: " + str(arithmetic_mean(x)))
print("n1_arithmetic_mean: " + str(n1_arithmetic_mean(x)))