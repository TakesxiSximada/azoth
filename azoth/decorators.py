# -*- coding: utf-8 -*-


def singleton(cls):
    _instance = None

    def _wrap(self, *args, **kwds):
        nonlocal _instance
        if not _instance:
            _instance = cls(self, *args, **kwds)
        return _instance
    return _wrap