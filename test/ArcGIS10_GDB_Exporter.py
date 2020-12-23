# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name : GDB Exporter
# Purpose : Export all features classes from a GDB rebuilding the same
#           organization of the database
# Authors : Julien Moura
# Contact : julien.moura@ird.fr
# Python : 2.6.5
# Encoding: utf-8
# Created : 07/11/2012
# Updated : 13/11/2012
#-------------------------------------------------------------------------------

## Import modules
from arcpy import env
from arcpy import ListDatasets, ListFeatureClasses, AddMessage, AddWarning
from arcpy import GetParameterAsText, FeatureClassToShapefile_conversion
from arcpy import SearchCursor
from os import mkdir, chdir, getcwd, makedirs

## Variables environnement ArcGIS
env.overwriteOutput = 1
env.maintainSpatialIndex = True
env.configKeyword = 'DEFAULTS'
env.outputCoordinateSystem = "Coordinate Systems/Projected Coordinate Systems/UTM/WGS 1984/Southern Hemisphere/WGS 1984 UTM Zone 18S.prj"
env.scratchWorkspace = r'C:\ArcGIS\\'

## Paramètres
gdb = GetParameterAsText(0)
env.workspace = gdb
AddMessage(u"Workspace: %s" % env.workspace)

cible = GetParameterAsText(1)
AddMessage(u"Carpeta de destino: %s" % cible)

table = GetParameterAsText(2)
AddMessage(u"Tabla de los temas y prefijos: %s" % table)
dico_temas = {}
for row in SearchCursor(table):
    dico_temas[row.getValue("DATASET")] = row.getValue("NUM_TEMA"),\
                                          row.getValue("TEMA_LARGO")
AddMessage(u"\tDiccionario de los temas construido")

## Programme principal
# Création dossier de configuration
chdir(cible)
try:
    mkdir('SIRAD')
    cible = cible + '\SIRAD'
except:
    cible = cible + '\SIRAD'
chdir(cible)

# Export
for dataset in ListDatasets("","featuredataset"):
    AddMessage(u"Dataset: %s" % dataset)
    folder = dico_temas.get(dataset)[0] + '_' + dico_temas.get(dataset)[1]
    mkdir(folder)
    env.workspace = gdb + '\\' + dataset
    if len(ListFeatureClasses()) > 0:
        FeatureClassToShapefile_conversion(ListFeatureClasses(), cible + '\\' + folder)
        AddMessage(u'\tCapas de información de %s exportadas\n' % dataset)
    else:
        AddWarning(u'\t\tNinguna capa de información encontrada en %s\n' % dataset)

