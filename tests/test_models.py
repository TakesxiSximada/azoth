# -*- coding: utf-8 -*-
from unittest import TestCase
from azoth.testutils import (
    create_db,
    destroy_db,
    )


class ActionBaseTest(TestCase):
    @create_db
    def setUp(self):
        pass

    @destroy_db
    def tearDown(self):
        pass

    def test_it(self):
        pass
