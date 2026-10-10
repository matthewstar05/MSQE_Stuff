"""
ECON 5015: Homework 5 (Algorithmic Efficiency)
Matthew Suban
@matthewsuban
"""

# 1. search_matrix worst case: O(n^2)
# value isnt in m (or its the very last entry), so both loops run all the way, n*n checks
def search_matrix(m,value):
  n=m.shape[0]
  for i in range(n):
    for j in range(n):
      if (m[i,j]==value):
        return True

  return False

# 4. search_matrix best case: Omega(1)
# value is at m[0,0], returns on the first check no matter how big n is


# 2. search_matrix2 worst case: O(n^2)
# never returns early, always n*n checks
def search_matrix2(m,value):
  n=m.shape[0]
  found=False
  for i in range(n):
    for j in range(n):
      if(m[i,j]==value):
        found=True

  return(found)

# 5. search_matrix2 best case: Omega(n^2)
# same as worst case since it keeps looping after finding it, so its theta(n^2)


# 3. search_sorted_array worst case: O(log(n))
# value isnt there, array gets cut in half every loop until 2 or fewer are left
# so about log2(n) iterations, same idea as power2 in lecture
def search_sorted_array(a, value):
  while(len(a)>2):
    n=len(a)
    mid=n//2
    if(a[mid]==value):
      return True
    elif (a[mid]>value):
      a=a[0:mid]
    else:
      a=a[(mid+1):n]
  if a[0]==value:
    return True
  if len(a)>1:
    if a[1]==value:
      return True
  return False

# 6. search_sorted_array best case: Omega(1)
# value is right at the middle, returns on the first pass


# 7. (not turned in) y = 8
# z = 6, y = 2
# f(z) -> f(6), inside f y is local and equals 6
# 6 < 6 is false so skip the first return
# y = 6 + 8 = 14 but its just the local y, then return z which is 6
# everything after that never runs
# y = f(z) + y = 6 + 2 = 8 (global y was still 2)
