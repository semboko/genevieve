from typing import List
from min_sorting import test_sorting_accuracy, test_running_time


def merge_sort(A: List[int]) -> List[int]:
    if len(A) <= 1:
        return A
    
    if len(A) == 2:
        if A[0] <= A[1]:
            return A
        else:
            return [A[1], A[0]]
    
    middle = len(A) // 2
    
    left = A[:middle]
    right = A[middle:]
    
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)
    
    final_result = []
    
    left_min = 0
    right_min = 0
    
    while left_min < len(left_sorted) and right_min < len(right_sorted):
        if left_sorted[left_min] <= right_sorted[right_min]:
            final_result.append(left_sorted[left_min])
            left_min += 1
        else:
            final_result.append(right_sorted[right_min])
            right_min += 1
    
    if left_min < len(left_sorted):
        final_result.extend(left_sorted[left_min:])
    
    if right_min < len(right_sorted):
        final_result.extend(right_sorted[right_min:])
    
    return final_result


test_sorting_accuracy(merge_sort)
test_running_time(merge_sort)