def logger(func):
    def inner(*args, **kwargs):
        print("Arguments where %s, %s" % (args, kwargs))
        return func(*args, **kwargs)
    return inner


@logger
def foo1(x, y=1):
    return x * y


@logger
def foo2():
    return 2


if __name__ == "__main__":
    foo1(5, 4)
    foo2()
