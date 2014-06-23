#-*- coding: utf-8 -*-
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import transaction
from zope.interface import implementer
from zope.sqlalchemy import ZopeTransactionExtension
from .interfaces import (
    ISessionManager,
    ISessionPool,
    )
from .decorators import singleton
from .config  import AzothConfigParser

DEFAULT_TARGET = 'master'


class SessionSetup(object):
    @classmethod
    def setup_from_file(cls, path, *args, **kwds):
        conf = AzothConfigParser()
        conf.read([path])
        cls.setup(conf, *args, **kwds)

    @classmethod
    def setup(cls, conf, name=DEFAULT_TARGET, alias=None, *args, **kwds):
        manager = SessionManager(*args, **kwds)
        manager.install(name, conf)
        if alias:
            manager.alias(name, alias)

@implementer(ISessionPool)
class SessionPool(object):
    def __init__(self):
        self.reset()

    def reset(self):
        transaction.abort()
        self._sessions = {}
        self._sessiongroups = {}
        self._aliases = {}

    def alias(self, src, dst):
        if not src in self.keys():
            raise ValueError('Session not found: {}'.format(src))
        self.can_use_name(dst)
        self._aliases[dst] = src

    def install(self, name, config, prefix='sqlalchemy.'):
        self.can_use_name(name)
        options = AzothConfigParser.get_section_dict(config, name)
        engine = sa.engine_from_config(options, prefix)

        extension = ZopeTransactionExtension()
        session = sa_orm.sessionmaker(extension=extension)
        DBSession = sa_orm.scoped_session(session)
        DBSession.configure(bind=engine)
        self._sessions[name] = DBSession

    def keys(self):
        return list(self._sessions.keys()) + \
          list(self._sessiongroups.keys()) + \
          list(self._aliases.keys())

    def can_use_name(self, name):
        if name in self.keys():
            raise ValueError('already used: {}'.format(name))

    def group(self, name, session_names):
        self.can_use_name(name)
        sessions = [self._sessions[name] for name in session_names]
        self._sessiongroups[name] = sessions

    def get(self, name, choice=None):
        return self.select(name, choice)

    def select(self, name, choice=None):
        if choice is None:
            choice = random.choice

        if name in self._aliases:
            name = self._aliases[name]

        if name in self._sessions:
            return self._sessions[name]
        elif name in self._sessiongroups:
            return choice(self._sessiongroups[name])
        else:
            raise ValueError('Session not found: {}'.format(name))

#@singleton
@implementer(ISessionManager)
class SessionManager(object):
    def __new__(cls, *args, **kwds):
        if not hasattr(cls, '_instance'):
            self = object.__new__(cls)
            cls.__init__(self, *args, **kwds)
            setattr(cls, '_instance', self)
        return getattr(cls, '_instance')

    def __init__(self, pool_class=SessionPool, *args, **kwds):
        self.pool = pool_class()

    def reset(self):
        return self.pool.reset()

    def alias(self, *args, **kwds):
        return self.pool.alias(*args, **kwds)

    def install(self, *args, **kwds):
        return self.pool.install(*args, **kwds)

    def group(self, *args, **kwds):
        return self.pool.group(*args, **kwds)

    def get(self, *args, **kwds):
        return self.pool.get(*args, **kwds)
