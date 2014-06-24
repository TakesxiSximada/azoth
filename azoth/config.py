# -*- coding: utf-8 -*-
import sys
import six

if six.PY2:
    import ConfigParser as configparser
elif six.PY3:
    import configparser


def config2dict(conf_or_dict, name=None):
    if isinstance(conf_or_dict, configparser.ConfigParser):
        return AzothConfigParser.get_section_dict(conf_or_dict, name)
    elif hasattr(conf_or_dict, '__getitem__'):
        return conf_or_dict
    else:
        raise TypeError('Illegal type')


class AzothConfigParser(configparser.SafeConfigParser):
    """ The configuration file parser for Azoth.
    """

    def get_section_dict(self, section_name):
        """ The dictionary creator.
        """
        if sys.version_info[0] == 2:
            options = self.options(section_name)
            return dict((key, self.get(section_name, key)) for key in options)
        else:  # only python3
            return self[section_name]
