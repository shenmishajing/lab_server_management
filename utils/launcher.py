import os
from functools import wraps


def launcher(parser_builder):
    def wrapper(func):
        @wraps(func)
        def f():
            parser = parser_builder()
            args = parser.parse_args()
            func(**args.__dict__)

        return f

    return wrapper
