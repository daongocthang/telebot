import functools


def command(name: str | list[str]):
    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pass

        return wrapper

    return inner
