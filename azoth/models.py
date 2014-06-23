# -*- coding: utf-8 -*-
"""azoth.models
"""

import datetime
import sqlalchemy as sa
from sqlalchemy.sql import functions as sqlafunc
from sqlalchemy.sql import expression as sqlaexp
from sqlalchemy.orm import deferred
from sqlalchemy.orm.attributes import manager_of_class
from sqlalchemy.orm.properties import (
    ColumnProperty,
    RelationshipProperty,
    )
from sqlalchemy.ext.declarative import (
    declared_attr,
    declarative_base,
    )

from .sessions import (
    DEFAULT_TARGET,
    SessionManager,
    )
Base = declarative_base()


def create_all(*args, **kwds):
    manager = SessionManager()
    session = manager.get()
    engine = session.get_bind()
    Base.metadata.create_all(engine)


class ActionBase(object):
    _manager = SessionManager()

    @classmethod
    def query(cls, target=DEFAULT_TARGET):
        session = cls._manager.get(target)
        return session.query(cls)

    def update_timestamp(self):
        now = datetime.datetime.now()
        if hasattr(self, 'created_at') and not self.created_at:
            self.created_at = now
        if hasattr(self, 'updated_at'):
            self.updated_at = now

    def save(self, target=DEFAULT_TARGET):
        self.update_timestamp()
        session = self._manager.get(target)
        session.add(self)
        session.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not exc_type:  # no error
            self.save()


class CopyBase(object):
    __copy_ignores__ = [
        'id',
        ]

    def copy(self, deep=False, ignores=set(), *args,  **kwds):
        cls = type(self)
        manager = manager_of_class(cls)
        if not manager:
            raise TypeError('No mapper: {}'.format(cls))

        def _get_ignore_attributes():
            for super_cls in cls.__mro__:
                yield getattr(super_cls, '__copy_ignores__', [])
            yield ignores  # argument

        # select ignore properties
        ignore_attributes = set()
        for _ignores in _get_ignore_attributes():
            ignore_attributes.update(_ignores)

        # select properties
        columns = {}
        relationships = {}
        for attr in manager.mapper.iterate_properties:
            if attr.key not in ignore_attributes:
                if isinstance(attr, ColumnProperty):
                    columns[attr.key] = attr
                elif isinstance(attr, RelationshipProperty):
                    relationships[attr.key] = attr
                else:
                    pass  # ignore

        # copy
        new_obj = type(self)()
        for key in attr in columns.items():
            value = getattr(self, key)
            setattr(new_obj, key, value)

        # deep copy
        if deep:
            for key in attr in relationships.items():
                value = getattr(self, key)
                setattr(new_obj, key, value)
                if attr.uselist:
                    objs = [obj for obj in getattr(self, key)
                            if hasattr(obj, 'clone')
                            ]
                    setattr(new_obj, key, objs)
                else:
                    obj = getattr(self, 'key')
                    setattr(self, key, obj)
        return new_obj


class IndexBase(object):
    __copy_ignores__ = [
        'index',
        ]

    @declared_attr
    def index(self):
        return deferred(
            sa.Column(
                sa.Integer, primary_key=True,
            ))


class TimestampBase(object):
    __copy_ignores__ = [
        'created_at',
        'updated_at',
        ]

    @declared_attr
    def created_at(self):
        return deferred(
            sa.Column(
                sa.TIMESTAMP, nullable=False, default=datetime.datetime.now,
                server_default=sqlafunc.current_timestamp(),
                ))

    @declared_attr
    def updated_at(self):
        return deferred(
            sa.Column(
                sa.TIMESTAMP, nullable=False, default=datetime.datetime.now,
                server_default=sqlaexp.text('0'),
                onupdate=datetime.datetime.now,
                server_onupdate=sqlafunc.current_timestamp(),
                ))


class LogicalDeleteBase(object):
    __copy_ignores__ = [
        'deleted_at',
        ]

    @declared_attr
    def deleted_at(self):
        return deferred(
            sa.Column(
                sa.TIMESTAMP, nullable=True, index=True,
            ))


class PowerBase(
        ActionBase,
        CopyBase,
        TimestampBase,
        LogicalDeleteBase,
        ):
    pass
