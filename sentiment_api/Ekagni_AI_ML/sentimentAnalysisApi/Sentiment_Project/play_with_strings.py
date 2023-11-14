def getNumbers():
    list1 = []
    for i in range(0,6):
        
        num = int(input(f"Enter the {i} number: "))
        list1.append(num)
    return list1

l1 = getNumbers()
l1 = l1[::-2]
print(l1)