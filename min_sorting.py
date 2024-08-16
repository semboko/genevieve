from typing import List, Callable
from time import time
from random import randint

def min_sorting(A: List[int]) -> List[int]:
    if len(A) <= 1:
        return A
    B = []
    for i in range(len(A)):
        min_a = min(A)
        B.append(min_a)
        A.remove(min_a)
    return B



def test_sorting_accuracy(sorting_func: Callable) -> None:
    assert sorting_func([]) == []
    assert sorting_func([1]) == [1]
    assert sorting_func([4, 3, 3]) == [3, 3, 4]
    assert sorting_func([6, 4, 1]) == [1, 4, 6]
    assert sorting_func([7, 4, 5, 2, 7, 8, 9, 3]) == [2, 3, 4, 5, 7, 7, 8, 9]
    print("Tests are passed!")
    

def test_running_time(sorting_func: Callable) -> None:
    test_data = [randint(10, 99) for _ in range(10 ** 4)]
    starting_time = time()
    sorting_func(test_data)
    finishing_time = time()

    print("min_sorting was executed in " + str(finishing_time - starting_time) + " seconds")
    

if __name__ == "__main__":
    test_sorting_accuracy(min_sorting)
    test_running_time(min_sorting)


    