# -*- coding: utf-8 -*-
import random
from unittest import TestCase


from .models import (
    ActionBaseTestModel,
    CopyBaseTestModel,
    TimestampBaseTestModel,
    IndexBase,
    User,
    Organization,
    )


class ActionBaseTest(TestCase):
    def test_query(self):
        session = ActionBaseTestModel.query()
        self.assert_(session)

    def test_update_timestamp(self):
        abtm = ActionBaseTestModel()
        abtm.update_timestamp()

    def test_save(self):
        abtm = ActionBaseTestModel()
        abtm.save()

    def test_with_statement(self):
        with ActionBaseTestModel() as abtm:
            abtm.name = 'hgoeaihgroaehgroeaihgoai'


class CopyBaseTestModelTest(TestCase):
    def _make_one(self):
        import datetime
        obj = CopyBaseTestModel()
        obj.boolean = True
        obj.big_integer = 0xFF * 0xFF
        obj.integer = 0xFF
        obj.float_ = 0.123
        obj.string_ = 'gheroighaoi'
        obj.date_ = datetime.date.today()
        obj.datetime_ = datetime.datetime.now()
        obj.numeric_ = 1
        obj.unicode_ = u'aaaa'
        obj.unicodetext_ = u'unicodetext'
        obj.timestamp = datetime.datetime.now()
        return obj

    def test_copy(self):
        obj = self._make_one()
        new_obj = obj.copy(deep=True)
        self.assertEqual(obj, new_obj)

    def test_merge(self):
        obj = self._make_one()
        new_obj = CopyBaseTestModel()
        obj.merge(new_obj, deep=True, ignores=['date_'])
        self.assertNotEqual(obj, new_obj)
        new_obj.date_ = obj.date_
        self.assertEqual(obj, new_obj)


class IndexBaseTestModelTest(TestCase):
    def test_it(self):
        IndexBase()


class TimestampBaseTestModelTest(TestCase):
    def test_it(self):
        obj = TimestampBaseTestModel()
        obj.save()
        self.assert_(obj.is_created)
        self.assert_(obj.is_updated)
        is_updated = obj.is_updated
        new_obj = TimestampBaseTestModel\
          .query()\
          .filter(TimestampBaseTestModel.id == obj.id)\
          .one()
        new_obj.save()

        self.assertEqual(obj.is_created, new_obj.is_created)
        self.assertNotEqual(is_updated, new_obj.is_updated)


class SmartBasePowerBaseTest(TestCase):
    def test_It(self):
        org = Organization()
        org.save()
        org_id = org.id

        user = User()
        user.name = 'OK'
        user.organization_id = org_id
        user.save()

        user_ids = [user.id]
        for ii in range(10):
            new_user = user.copy(deep=True)
            new_user.save()
            user_ids.append(new_user.id)
        user_ids = set(user_ids)

        another_org = Organization()
        another_org.save()
        for ii in range(100):
            user = User()
            user.organization_id = another_org.id
            user.name = 'NG'
            user.save()

        users = User\
            .query()\
            .join(Organization)\
            .filter(Organization.id == org_id)\
            .all()

        get_user_ids = set(user.id for user in users)
        self.assertEqual(user_ids, get_user_ids)

        names = set(user.name for user in users)
        self.assertEqual(names, {'OK'})
