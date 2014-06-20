#-*- coding: utf-8 -*-
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

class AzothConfigParser(configparser.SafeConfigParser):
    def get_section_dict(self, section_name):
        options = self.options(section_name)
        return dict((key, self.get(section_name, key)) for key in options)
