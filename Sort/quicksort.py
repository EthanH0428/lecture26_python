def partition(A, left, right):
    pivot = A[left]
    low = left + 1
    high = right
    
    while low <= high:
        while low <= right and A[low] < pivot:
            low += 1
        while high >= left and A[high] > pivot:
            high -= 1
            
        if low < high:
            A[low], A[high] = A[high], A[low]
            
    A[left], A[high] = A[high], A[left]
    return high


def quick_sort(A, left, right):
    if left < right:
        pivot_index = partition(A, left, right)        
        quick_sort(A, left, pivot_index - 1)
        quick_sort(A, pivot_index + 1, right)

if __name__ == "__main__":
    data = [27, 10, 12, 20, 25, 13, 15, 22]
    
    print("정렬 전 :", data)
    
    quick_sort(data, 0, len(data) - 1)
    
    print("정렬 후 :", data)