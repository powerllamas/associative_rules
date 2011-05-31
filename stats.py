# -*- coding: utf-8 -*-

import os
import functools

def is_posix():
    return False
    return os.name == 'posix'

def get_stats(storage):
    def decorator(function):
        if is_posix():
            import resource
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                result = function(*args, **kwargs)
                return result
            return wrapper
        else:
            return function
    return decorator
