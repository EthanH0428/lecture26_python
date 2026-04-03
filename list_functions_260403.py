def getIndex(num_list, target):
    for i in range(len(num_list)):
        if num_list[i] == target:
            return i
    return -1  

def getMax(num_list):
    if not num_list: return None
    max_val = num_list[0]
    for num in num_list:
        if num > max_val:
            max_val = num
    return max_val

def getMin(num_list):
    if not num_list: return None
    min_val = num_list[0]
    for num in num_list:
        if num < min_val:
            min_val = num
    return min_val

def countGT(num_list, target):
    count = 0
    for num in num_list:
        if num > target:
            count += 1
    return count

def sumList(num_list):
    total = 0
    for num in num_list:
        total += num
    return total

def swapList(num_list):
    n = len(num_list)
    for i in range(n // 2):
        num_list[i], num_list[n - 1 - i] = num_list[n - 1 - i], num_list[i]

number_list = [23, 45, 27, 11, 25, 65, 78]

print(getIndex(number_list, 25))    
print(getMax(number_list))          
print(getMin(number_list))          
print(countGT(number_list, 42))     
print(sumList(number_list))         
swapList(number_list)
print(number_list)                  