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
AUTO_INCREMENT = {'sqlite_autoincrement': True}
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
        if hasattr(self, 'is_created') and not self.is_created:
            self.is_created = now
        if hasattr(self, 'is_updated'):
            self.is_updated = now

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

    @classmethod
    def _get_ignore_attributes(cls, ignores=[], *args, **kwds):
        for super_cls in cls.__mro__:
            for attr in getattr(super_cls, '__copy_ignores__', []):
                yield attr
        for attr in ignores:
            yield attr

    def _get_attribute_datas(self, manager, ignores=[]):
        type_properties = {
            ColumnProperty: {},
            RelationshipProperty: {},
            }

        for attr in manager.mapper.iterate_properties:
            if attr.key not in ignores:
                for typ, prop in type_properties.items():
                    if isinstance(attr, typ):
                        prop[attr.key] = attr
        return type_properties

    def merge(self, other, ignores=[], deep=False):
        cls = type(self)
        manager = manager_of_class(cls)
        if not manager:
            raise TypeError('This mapper is Unkown: {}'.format(cls))
        ignores = [attr for attr in self._get_ignore_attributes(ignores)]
        type_attributes = self._get_attribute_datas(manager, ignores)
        for key, attr in type_attributes[ColumnProperty].items():
            setattr(other, key, getattr(self, key))

        # deep copy, coping relationships.
        if deep:
            for key, attr in type_attributes[RelationshipProperty].items():
                setattr(other, key, getattr(self, key))
                if attr.uselist:
                    objs = [obj for obj in getattr(self, key)
                            if hasattr(obj, 'copy')
                            ]
                    setattr(other, key, objs)
                else:
                    setattr(other, key, getattr(self, key))
        return other

    def copy(self, *args, **kwds):
        new_obj = type(self)()
        return self.merge(new_obj, *args, **kwds)


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
        'is_created',
        'is_updated',
        ]

    @declared_attr
    def is_created(self):
        return deferred(
            sa.Column(
                sa.TIMESTAMP, nullable=False, default=datetime.datetime.now,
                server_default=sqlafunc.current_timestamp(),
                ))

    @declared_attr
    def is_updated(self):
        return deferred(
            sa.Column(
                sa.TIMESTAMP, nullable=False, default=datetime.datetime.now,
                server_default=sqlaexp.text('0'),
                onupdate=datetime.datetime.now,
                server_onupdate=sqlafunc.current_timestamp(),
                ))


class LogicalDeleteBase(object):
    __copy_ignores__ = [
        'is_deleted',
        ]

    def delete(self, as_save=True):
        self.is_deleted = datetime.datetime.now()
        if as_save:
            self.save()
        return self

    @declared_attr
    def is_deleted(self):
        return deferred(
            sa.Column(
                sa.TIMESTAMP, nullable=True, index=True,
                ))


class SmartBase(
        ActionBase,
        CopyBase,
        TimestampBase,
        ):
    pass


class PowerBase(
        SmartBase,
        LogicalDeleteBase,
        ):
    pass
