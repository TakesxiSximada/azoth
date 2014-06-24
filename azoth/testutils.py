# -*- coding: utf-8 -*-
import functools
from .sessions import (
    SessionSetup,
    SessionManager,
    )


def create_db(func):
    @functools.wraps(func)
    def _wrap(self, *args, **kwds):
        db_fixture = DBFixture()
        db_fixture.create_db()
        return func(self, *args, **kwds)
    return _wrap


def destroy_db(func):
    @functools.wraps(func)
    def _wrap(self, *args, **kwds):
        rc = func(self, *args, **kwds)
        db_fixture = DBFixture()
        db_fixture.destroy_db()
        return rc
    return _wrap


class DBFixture(object):
    def create_db(self):
        settings = {
            'sqlalchemy.url': 'sqlite://',
            'sqlalchemy.echo': True,
            }
        SessionSetup.setup(settings)

    def destroy_db(self):
        manager = SessionManager()
        manager.reset()
