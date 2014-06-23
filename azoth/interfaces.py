# -*- coding: utf-8 -*-

from zope.interface import (
    Interface,
    Attribute,
    )


class ISessionPool(Interface):
    alias = Attribute('')
    reset = Attribute('')
    install = Attribute('')
    keys = Attribute('')
    can_use_name = Attribute('')
    group = Attribute('')
    get = Attribute('')
    select = Attribute('')


class ISessionManager(Interface):
    alias = Attribute('')
    reset = Attribute('')
    install = Attribute('')
    group = Attribute('')
    get = Attribute('')
