list = input("Enter numbers separated by spaces: ").split()
list = [int(x) for x in list]
n= len(list)
for i in range(n):
    for j in range(0, n-i-1):
        if list[j] > list[j+1]:
            list[j], list[j+1] = list[j+1], list[j]
print("Sorted list is:", list)  