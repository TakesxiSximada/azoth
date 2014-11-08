# -*- coding: utf-8 -*-

from unittest import TestCase


def open_dummy_config(conf_class=None):
    try:
        import io
    except ImportError:
        import StringIO as io
    from azoth.config import AzothConfigParser

    if conf_class is None:
        conf_class = AzothConfigParser

    conf_file = io.StringIO()
    conf_file.write('[master]\n')
    conf_file.write('sqlalchemy.url = sqlite://\n')
    conf_file.write('sqlalchemy.echo = 1\n')
    conf_file.seek(0)

    conf = conf_class()
    conf.readfp(conf_file)
    return conf


class Config2DictFunctionTest(TestCase):
    def test_config2dict(self):
        from azoth.config import (
            config2dict,
            AzothConfigParser,
            )

        # conf
        conf = open_dummy_config()
        options = config2dict(conf, 'master')
        self.assertEqual(options['sqlalchemy.url'], 'sqlite://')
        self.assertEqual(options['sqlalchemy.echo'], '1')

        # type error
        with self.assertRaises(TypeError):
            config2dict(object)

class AzothConfigParserTest(TestCase):
    def test_get_section_dict(self):
        conf = open_dummy_config()
        options = conf.get_section_dict('master')
        self.assertEqual(options['sqlalchemy.url'], 'sqlite://')
        self.assertEqual(options['sqlalchemy.echo'], '1')
