def get_hash():
    r = 31
    M = 1234567891
    
    alpa_input = input('알파벳을 입력하시오 : ').lower()
    
    hash_value = 0
    current_r = 1 
    
    for target in alpa_input:
        if 'a' <= target <= 'z':
            alpa_no = ord(target) - ord('a') + 1
            hash_value = (hash_value + alpa_no * current_r) % M
            current_r = (current_r * r) % M
            
    return hash_value

a = get_hash()
print(a)