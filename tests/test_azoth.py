# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

from azoth.testutils import (
    create_db,
    destroy_db,
    )


class OneTest(TestCase):
    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_it(self):
        import sqlalchemy as sa
        import transaction
        from azoth.models import (
            Base,
            PowerBase,
            create_all,
            )

        # class User(Base, PowerBase):
        #     __tablename__ = 'User'
        #     __table_args__ = (
        #         {'sqlite_autoincrement': True},
        #         )

        #     id = sa.Column(sa.Integer, primary_key=True)
        #     name = sa.Column(sa.Unicode, nullable=False, default=u'')
        # create_all()

        # for ii in range(10):
        #     user = User()
        #     user.save()
        # transaction.commit()

        # for user in User.query().all():
        #     user.name = 'user-{}'.format(user.id)
        #     user.save()
        # transaction.commit()

        # for user in User.query().all():
        #     user_id = int(user.name.strip('user-'))
        #     self.assertEqual(user.id, user_id)

if __name__ == '__main__':
    unittest.main()
