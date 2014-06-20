#-*- coding: utf-8 -*-
import unittest
from unittest import TestCase

class UsecaseTest(TestCase):
    def test_session(self):
        try:
            import configparser
        except ImportError:
            import ConfigParser as configparser
        from azoth.sessions import (
            SessionManager,
            SessionPool,
            DEFAULT_TARGET,
            )

        conf = configparser.SafeConfigParser()
        conf.add_section(DEFAULT_TARGET)
        conf.set(DEFAULT_TARGET, 'sqlalchemy.url', 'sqlite:///test.sqlite3')

        manager = SessionManager(SessionPool)
        manager.install('master', conf)
        manager.group('slave', ['master'])

        session = manager.get('master')
        master_session = manager.get('master')
        self.assertEqual(session, master_session)

    def test_declarative_model(self):
        import sqlalchemy as sa
        import sqlalchemy.orm as sa_orm
        from azoth.models import (
            Base,
            IDBase,
            ActionBase,
            CopyBase,
            TimestampBase,
            LogicalDeleteBase,
            PowerBase,
            )

        class TestTable(Base, ActionBase, IDBase, CopyBase, TimestampBase, LogicalDeleteBase):
            __tablename__ = 'TestTable'
            name = sa.Column(sa.Unicode, primary_key=True)
            description = sa.Column(sa.Unicode)

        class TestRelTable(Base, PowerBase):
            __tablename__ = 'TestRelTable'
            test_table_id = sa.Column(sa.Integer)
            test_table = sa_orm.relationship('TestTable.id')

if __name__ == '__main__':
    unittest.main()
