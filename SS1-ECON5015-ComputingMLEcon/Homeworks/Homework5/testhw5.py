from hw5 import f, f1, f2, gridsearch, newton

print(f([1,2]))
print(f1([1,2]))
print(f2([1,2]))
print(gridsearch(-10, 10, 2000, f))
print(newton([0,0], 0.001, f1, f2))