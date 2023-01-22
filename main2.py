def sort(list2):
    for i in range(1, len(list2)):
        cur = list2[i]
        index = i

        while index > 0 and cur < list2[index-1]:
            list2[index] = list2[index-1]
            index -=1
    
        list2[index] = cur
    return list2

print(sort([6,7,9,8,10]))