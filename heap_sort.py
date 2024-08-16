from typing import List, Optional
from math import ceil
from random import shuffle
from min_sorting import test_running_time


def parent(i):
    return ceil(i/2 - 1)


def left(i):
    return 2 * i + 1


def right(i):
    return 2 * i + 2


def max_heapify(A: List[int], i: int, heap_size: Optional[int] = None):
    if heap_size is None:
        heap_size = len(A)
    left_idx = left(i)
    right_idx = right(i)
    largest_idx = i
    if left_idx < heap_size and A[left_idx] > A[i]:
        largest_idx = left_idx
    if right_idx < heap_size and A[right_idx] > A[largest_idx]:
        largest_idx = right_idx
        
    if largest_idx != i:
        A[i], A[largest_idx] = A[largest_idx], A[i]
        max_heapify(A, largest_idx, heap_size)
        
A = [16, 4, 10, 14, 7, 9, 3, 2, 8, 1]
max_heapify(A, 1)
assert A == [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]


def build_max_heap(A: List[int]) -> None:
    for i in range(ceil(len(A)/2 - 1), -1, -1):
        max_heapify(A, i)
        

def validate_max_heap(A: List[int]) -> bool:
    for idx in range(len(A)-1, 0, -1):
        pidx = parent(idx)
        if A[idx] > A[pidx]:
            return False
    return True
        
shuffle(A)
build_max_heap(A)
assert validate_max_heap(A)


def heap_sort(A: List[int]) -> List[int]:
    heap_size = len(A)
    build_max_heap(A)
    for idx in range(len(A)-1, 0, -1):
        A[0], A[idx] = A[idx], A[0]
        heap_size -= 1
        max_heapify(A, 0, heap_size)
        

shuffle(A)
heap_sort(A)
assert A == sorted(A)

test_running_time(heap_sort)
test_running_time(sorted)