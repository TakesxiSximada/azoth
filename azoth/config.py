#-*- coding: utf-8 -*-
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

def config2dict(conf_or_dict, name=None):
    if isinstance(conf_or_dict, configparser.ConfigParser):
        return AzothConfigParser.get_section_dict(conf_or_dict, name)
    elif hasattr(conf_or_dict, '__getitem__'):
        return conf_or_dict
    else:
        raise TypeError('Illegal type')

class AzothConfigParser(configparser.SafeConfigParser):
    def get_section_dict(self, section_name):
        options = self.options(section_name)
        return dict((key, self.get(section_name, key)) for key in options)
