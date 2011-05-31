# -*- coding: utf-8 -*-

import os
import functools

def is_posix():
    return os.name == 'posix'

def get_stats(storage):
    def decorator(function):
        if is_posix():
            import resource
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                storage.append(resource.getrusage(resource.RUSAGE_SELF))
                result = function(*args, **kwargs)
                storage.append(resource.getrusage(resource.RUSAGE_SELF))
                return result
            return wrapper
        else:
            return function
    return decorator
