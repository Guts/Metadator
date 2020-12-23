# -*- coding: UTF-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         metadator2exe
# Purpose:      Script to transform Metadator scripts into an Windows executable
#                   software. It uses py2exe.
#
# Author:       Julien Moura (https://github.com/Guts/)
#
# Python:       2.7.x
# Created:      19/12/2011
# Updated:      12/07/2014
#
# Licence:      GPL 3
#-------------------------------------------------------------------------------

################################################################################
########### Libraries #############
###################################
# Standard library
from distutils.core import setup
import py2exe
import os
import ConfigParser
import numpy

# custom modules
from modules import InfosOGR
from modules import StatsFields
from modules import ExportToHTML
from modules import ExportToODT
from modules import ExportToXML
from modules import ExportToXLS
from modules import ExportToDocX
from modules import DocxMerger
from modules import NewProfile

################################################################################
########## Main program ###########
###################################

# version
num_version = "v2.0-beta.4"

## reset the options.ini
confile = 'options.ini'
config = ConfigParser.RawConfigParser()
# add sections
config.add_section('basics')
config.add_section('export_preferences')
# basics
config.set('basics', 'def_codelang', 'EN')
config.set('basics', 'def_rep', './')
# export preferences
config.set('export_preferences', 'def_word', 1)
config.set('export_preferences', 'def_cat', 0)
config.set('export_preferences', 'def_xls', 1)
config.set('export_preferences', 'def_xml', 1)
config.set('export_preferences', 'def_dict', 0)
config.set('export_preferences', 'def_odt', 1)
# Writing the configuration file
with open(confile, 'wb') as configfile:
    config.write(configfile)


# Specific dll for pywin module
mfcdir = r'C:\Python27\Lib\site-packages\pythonwin'
mfcfiles = [os.path.join(mfcdir, i) for i in ["mfc90.dll", "mfc90u.dll", "mfcm90.dll", "mfcm90u.dll", "Microsoft.VC90.MFC.manifest"]]

# Specific data for gdal
gdal_dir = r'data/gdal'
gdal_files = [os.path.join(gdal_dir, i) for i in os.listdir(gdal_dir)]


# build settings
build_options = dict(
                    build_base='setup/temp_build',
                    )

# conversion settings 
py2exe_options = dict(
                      excludes=['_ssl',  # Exclude _ssl
                                'pyreadline', 'doctest', 'email',
                                'optparse', 'pickle'],  # Exclude standard library
                      dll_excludes = ['MSVCP90.dll'],
                      compressed=True,  # Compress library.zip
                      optimize = 2,
                      dist_dir = 'setup/Metadator_{}'.format(num_version)
                      )
setup(
    name="Metadator",
    version=num_version,
    description="Automatize the creation of metadata from geographic data",
    author="Julien Moura",
    author_mail = "julien.moura@gmail.com",
    url = "https://github.com/Guts/Metadator",
    license="license GPL v3.0",
    data_files=[
                # pywin and numpy
                ("Microsoft.VC90.MFC", mfcfiles, "C:\\Python27\\Lib\\site-packages\\numpy\\core\\libiomp5md.dll"),
                # gdal
                ("data/gdal", gdal_files),
                ## English version
                ("locale/EN", ["locale/EN/champignons_EN.xml",
                               "locale/EN/contacts_EN.xml",
                               "locale/EN/help_EN.xml",
                               "locale/EN/keywords_EN.xml",
                               "locale/EN/geokeywords_EN.xml",
                               "locale/EN/lang_EN.xml"
                               ]
                ),
                # inspire
                ("locale/EN/inspire", ["locale/EN/inspire/diffusion_EN.xml",
                                       "locale/EN/inspire/fonctions_EN.xml",
                                       "locale/EN/inspire/rythmes_EN.xml",
                                       "locale/EN/inspire/specifications_EN.xml",
                                       "locale/EN/inspire/themes_inspire_EN.xml",
                                       "locale/EN/inspire/themes_iso_EN.xml"
                                       ]
                ),
                # profiles
                ("locale/EN/profiles", ["locale/EN/profiles/Metadator_ProfileDemo_EN.xml"]),
                ## Spanish version
                # locales
                ("locale/ES", ["locale/ES/champignons_ES.xml",
                               "locale/ES/contacts_ES.xml",
                               "locale/ES/help_ES.xml",
                               "locale/ES/keywords_ES.xml",
                               "locale/ES/geokeywords_ES.xml",
                               "locale/ES/lang_ES.xml"
                               ]
                ),
                # inspire
                ("locale/ES/inspire", ["locale/ES/inspire/diffusion_ES.xml",
                                       "locale/ES/inspire/fonctions_ES.xml",
                                       "locale/ES/inspire/rythmes_ES.xml",
                                       "locale/ES/inspire/specifications_ES.xml",
                                       "locale/ES/inspire/themes_inspire_ES.xml",
                                       "locale/ES/inspire/themes_iso_ES.xml"
                                       ]
                ),
                # profiles
                ("locale/ES/profiles", ["locale/ES/profiles/Metadator_PerfilDemo_ES.xml"]),
                ## French version
                # locales
                ("locale/FR", ["locale/FR/champignons_FR.xml",
                               "locale/FR/contacts_FR.xml",
                               "locale/FR/help_FR.xml",
                               "locale/FR/keywords_FR.xml",
                               "locale/FR/geokeywords_FR.xml",
                               "locale/FR/lang_FR.xml"
                               ]
                ),
                # inspire
                ("locale/FR/inspire", ["locale/FR/inspire/diffusion_FR.xml",
                                       "locale/FR/inspire/fonctions_FR.xml",
                                       "locale/FR/inspire/rythmes_FR.xml",
                                       "locale/FR/inspire/specifications_FR.xml",
                                       "locale/FR/inspire/themes_inspire_FR.xml",
                                       "locale/FR/inspire/themes_iso_FR.xml"
                                       ]
                ),
                # profiles
                ("locale/FR/profiles", ["locale/FR/profiles/Metadator_ProfilDemo_FR.xml"]),
                ## Polish version
                # locales
                ("locale/PL", ["locale/PL/champignons_PL.xml",
                               "locale/PL/contacts_PL.xml",
                               "locale/PL/help_PL.xml",
                               "locale/PL/keywords_PL.xml",
                               "locale/PL/geokeywords_PL.xml",
                               "locale/PL/lang_PL.xml"
                               ]
                ),
                # inspire
                ("locale/PL/inspire", ["locale/PL/inspire/diffusion_PL.xml",
                                       "locale/PL/inspire/fonctions_PL.xml",
                                       "locale/PL/inspire/rythmes_PL.xml",
                                       "locale/PL/inspire/specifications_PL.xml",
                                       "locale/PL/inspire/themes_inspire_PL.xml",
                                       "locale/PL/inspire/themes_iso_PL.xml"
                                       ]
                ),
                # profiles
                ("locale/PL/profiles", ["locale/PL/profiles/Metadator_ProfilDemo_PL.xml"]),
                ## data
                ("data/img", ["data/img/metadator.gif",
                              "data/img/icon_AddTag_np8755.gif",
                              "data/img/icon_DelTag_np8756.gif",
                              "data/img/icon_INSPIRE_np23902.gif",
                              "data/img/icon_NewProfile_np7782.gif",
                              "data/img/icon_ImportProfile_np14001.gif",
                              "data/img/icon_share_33023.gif",
                              "data/img/modele_metadator_Wordp1.gif",
                              "data/img/modele_metadator_Excelp1.gif",
                              "data/img/modele_metadator_ODT.gif",
                              "data/img/modele_metadator_XML.gif",
                              "data/img/modele_metadator_CAT.gif",
                              "Metadator.ico"
                             ]
                ),
                ("data/xml", ["data/xml/languages.xml",
                              "data/xml/template_iso19110.xml",
                              "data/xml/template_iso19139.xml",
                             ]
                ),
                ## options file and icon
                ("", ["options.ini"]),
                ("", ["Metadator.ico"])
                ],
    options={'py2exe': py2exe_options, 'build': build_options},
    windows = [
        {
            "script": "Metadator.py",                    ### Main Python script
            "icon_resources": [(1, "Metadator.ico")]     ### Icon to embed into the PE file.
        }
              ],
    )