# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 10:17:56 2020

@author: aric
"""


#For each of the 3 functions below, determine the worst case O() and best case Omega() in terms of n.  
#For the first two functions, n is the number of rows and columns in the square matrix m
#For the third function, n is the length of the input array a

#search_matrix
#m: square matrix (2-dimensional numpy array) to search
#value:  value to search for
#return value:  TRUE if value is in matrix, FALSE otherwise
def search_matrix(m,value):
  n=m.shape[0]
  for i in range(n):
    for j in range(n):
      if (m[i,j]==value):
        return True

  return False



#search_matrix2
#m: square matrix (2-dimensional numpy array) to search  
#value:  value to search for
#return value:  TRUE if value is in matrix, FALSE otherwise
def search_matrix2(m,value):
  n=m.shape[0]
  found=False
  for i in range(n):
    for j in range(n):
      if(m[i,j]==value):
        found=True

  return(found)


#search_sorted_array
#a:  a float array in ascending order
#value:  value to search for
#return value:  TRUE if value is in array, FALSE otherwise
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
