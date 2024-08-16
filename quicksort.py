from typing import List, Optional
from min_sorting import test_running_time


def partition(A: List[int], start: int, end: int) -> int:
    x = A[end]
    i = start - 1
    for j in range(start, end):
        if A[j] <= x:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[end] = A[end], A[i+1]
    return i + 1


def quicksort(A: List[int], start: Optional[int] = None, end: Optional[int] = None) -> None:
    if start is None:
        start = 0
    if end is None:
        end = len(A) - 1
    if start < end:
        pivot = partition(A, start, end)
        quicksort(A, start, pivot - 1)
        quicksort(A, pivot + 1, end)
        


unsorted_list = [8, 4, 2, 10, 5]
quicksort(unsorted_list)
assert unsorted_list == [2, 4, 5, 8, 10]

test_running_time(quicksort)