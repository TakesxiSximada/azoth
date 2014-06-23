#-*- coding: utf-8 -*-
import configparser
import transaction
from .sessions import (
    SessionSetup,
    SessionManager,
    )

class GlobalTestFixture(object):
    def create_db(self):
        settings = {
            'sqlalchemy.url': 'sqlite://',
            'sqlalchemy.echo': True,
            }
        SessionSetup.setup(settings)

    def destroy_db(self):
        manager = SessionManager()
        manager.reset()
