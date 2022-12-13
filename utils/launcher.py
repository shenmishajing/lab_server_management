import os
from functools import wraps


def launcher(func, parser_builder):
    @wraps(func)
    def wrapper():
        parser = parser_builder()
        args = parser.parse_args()
        func(**args.__dict__)

    return wrapper
