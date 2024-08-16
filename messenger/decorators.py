


def decorator(fun):
    def wrapper():
        print("Something before")
        result = fun()
        print("Something after")
        return result
    return wrapper


@decorator
def one_plus_one():
    return 2


print(one_plus_one())
