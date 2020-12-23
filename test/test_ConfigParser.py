# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julien
#
# Created:     09/07/2013
# Copyright:   (c) Julien 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# testing config parser library to get and save configurations files


import ConfigParser
from os import path


def load_settings():
    confile = r'test_options.ini'
    print path.isfile(confile)
    config = ConfigParser.RawConfigParser()
    config.read(confile)
    # basics
    def_lang = config.get('basics', 'def_codelang')
    def_rep = config.get('basics', 'def_rep')
    # export preferences
    def_doc = config.get('export_preferences', 'def_word')
    def_cat = config.get('export_preferences', 'def_cat')
    def_xls = config.get('export_preferences', 'def_xls')
    def_xml = config.get('export_preferences', 'def_xml')
    def_dict = config.get('export_preferences', 'def_dict')
    # end of function
    return def_lang, def_rep,def_doc, def_xls, def_xml, def_cat, def_dict


def save_settings():
    confile = r'test_options.ini'
    print path.isfile(confile)
    config = ConfigParser.RawConfigParser()
    # add sections
    config.add_section('basics')
    config.add_section('export_preferences')
    # basics
    config.set('basics', 'def_codelang', 'FR')
    config.set('basics', 'def_rep', 'test/datatest/')
    # export preferences
    config.set('export_preferences', 'def_word', 1)
    config.set('export_preferences', 'def_cat', 0)
    config.set('export_preferences', 'def_xls', 1)
    config.set('export_preferences', 'def_xml', 0)
    config.set('export_preferences', 'def_dict', 0)
    # Writing the configuration file
    with open(confile, 'wb') as configfile:
        config.write(configfile)


load_settings()
save_settings()









