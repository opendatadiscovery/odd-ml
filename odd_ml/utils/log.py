import functools
import logging


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Function {func.__name__} with args {', '.join(list(args))}")
        return func(*args, **kwargs)

    return wrapper
