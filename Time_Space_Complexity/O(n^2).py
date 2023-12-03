import time

array = ['a', 'b', 'c', 'd', 'e']


def log_all_pairs(array):

  #There are nested for loops in this function but there is only one variable array.

  for i in range(len(array)):  #n*O(n)
    for j in range(len(array)):  #n*O(n)
      print(array[i], array[j])  #n*n*O(1)


log_all_pairs(array)

#Total time complexity of the log_all_pairs function =
#O(n*n + n*n + n*n*1) = O(3n^2)
#The constants can be safely ignored.
#Therefore, O(3n^2) = O(n^2)

new_array = [1, 2, 3, 4, 5]


def print_numbers_then_pairs(array):

  print("The numbers are : ")  #O(1)
  for i in range(len(array)):  #O(n)
    print(array[i])  #n*O(1)

  print("The pairs are :")  #O(1)
  for i in range(len(array)):  #n*O(n)
    for j in range(len(array)):  #n*O(n)
      print(array[i], array[j])  #n*n*O(1)


print_numbers_then_pairs(new_array)
