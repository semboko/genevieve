from typing import List, Tuple


def mountain_scape(tops):
    stack = [*tops]
    visited = set()
    
    while stack:
        top = stack.pop()
        visited.add(top)
        if top[1] == 1:
            continue
        n1 = (top[0] - 1, top[1] - 1)
        n2 = (top[0] + 1, top[1] - 1)
        stack.extend((n1, n2))
    
    # counter = 0
    # for top in visited:
    #     if top[1] > 1:
    #         counter += 2
    #     else:
    #         counter += 1
        
    # return counter
    
    return sum([2 if y > 1 else 1 for x, y in visited])

assert mountain_scape([(1, 1), (4, 2), (7, 3)]) == 13
assert mountain_scape([(0, 2), (5, 3), (7, 5)]) == 29
assert mountain_scape([(1, 3), (5, 3), (5, 5), (8, 4)]) == 37
print("Done")