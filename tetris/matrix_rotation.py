# tuple(zip(*matrix[::-1]))

matrix = (
    (1, 2, 0),
    (4, 5, 6),
    (6, 7, 8),
)

some_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)

# print(matrix[::-1])

a = (1, 2, 3)
b = ("a", "b", "c")
c = (True, False, True)
d = (1, 2)

print(tuple(zip(a, b, c, d)))


def test_func(a, b, c):
    return a + b + c

g = (5, 10, 15)
print(test_func(*g))
