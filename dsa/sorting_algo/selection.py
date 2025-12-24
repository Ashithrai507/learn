list = [5, 2, 9, 1, 5, 6]
list = [int(x) for x in list]
n = len(list)
for i in range(n):
    c=i
    for j in range(i+1, n):
        if list[c] > list[j]:
            c = j
    list[i], list[c] = list[c], list[i]
print("Sorted list is:", list)