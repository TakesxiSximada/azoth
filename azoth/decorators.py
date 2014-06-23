# -*- coding: utf-8 -*-


def singleton(cls):
    """The singleton decorato.r
    """
    _instances = {}

    def _wrap(*args, **kwds):
        nonlocal _instances
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwds)
        return _instances[cls]
    return _wrap
