L = int(input())  
string = input()  

r = 31
M = 1234567891

hash_value = 0

for i in range(L):
    a_i = ord(string[i]) - ord('a') + 1
    
    hash_value += a_i * (r ** i)

print(hash_value % M)