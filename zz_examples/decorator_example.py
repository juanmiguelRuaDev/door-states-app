def wrapper( a, b):
    def decorator(f):
        print("soy decorator en {0} and {1}".format(a, b))
        return f
    return decorator


@wrapper("a", "b")
def return_string(c):
    return str(c)


if __name__ == "__main__":
    response = return_string("hol")
    print(response)


