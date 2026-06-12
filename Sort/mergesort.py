def merge(A, left, mid, right):
    k = i = left
    j = mid + 1
    
    while i <= mid and j <= right:
        if A[i] <= A[j]:
            sorted_list[k] = A[i]
            k, i = k + 1, i + 1
        else:
            sorted_list[k] = A[j]
            k, j = k + 1, j + 1
            
    if i > mid:
        sorted_list[k : k + right - j + 1] = A[j : right + 1]
    else:
        sorted_list[k : k + mid - i + 1] = A[i : mid + 1]
        
    A[left : right + 1] = sorted_list[left : right + 1]


def merge_sort(A, left, right):

    if left < right:
        mid = (left + right) // 2   
        merge_sort(A, left, mid)    
        merge_sort(A, mid + 1, right) 
        merge(A, left, mid, right)  


if __name__ == "__main__":
    data = [10, 12, 20, 27, 13, 15, 22, 25]
    sorted_list = [0] * len(data)
    print("정렬 전 :", data)
    merge_sort(data, 0, len(data) - 1)   
    print("정렬 후 :", data)