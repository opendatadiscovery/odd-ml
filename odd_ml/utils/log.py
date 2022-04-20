import functools


def log(func):
    def wrapper(*args, **kwargs):
        print(
            f"Function {func.__name__} with args { ', '.join([arg for arg in args ]) }"
        )
        return func(*args, **kwargs)

    return wrapper
