#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julien
#
# Created:     16/07/2013
# Copyright:   (c) Julien 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Standard library
from operator import itemgetter     # avanced iteration functions
from os import path

# Python 3 backported
from collections import OrderedDict as OD

# 3rd party libraries
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta    # times delta calculation

from numpy import median, average   # median and mean calculation
from numpy import std as ectyp      # standart deviation (French abbreviation beacause std is a Python keywords)
from osgeo import ogr               # for geography objects


##########

##to solve :
##      File "E:\Mes documents\GitHub\Metadator\modules\StatsFields.py", line 164, in stats_ent
##    value = layer.GetFeature(obj).GetFieldAsInteger(field)
##AttributeError: 'NoneType' object has no attribute 'GetFieldAsInteger'

# variables
tab = r'datatest/airports_MI\tab\airports_MI.tab'
print path.isfile(tab)
dico_fields = OD()

# ogr basics
source = ogr.Open(tab, 0)

if not source:
    print 'ups'

layer = source.GetLayer()
obj = layer.GetFeature(1)
geom = obj.GetGeometryRef()
def_couche = layer.GetLayerDefn()
srs = layer.GetSpatialRef()

# srs
##print srs.ExportToPrettyWkt()


# fields
for i in range(def_couche.GetFieldCount()):
    champomy = def_couche.GetFieldDefn(i)           # ordered list of fields
    dico_fields[champomy.GetName()] = champomy.GetTypeName(),\
                                      champomy.GetWidth(),\
                                      champomy.GetPrecision()

for field in dico_fields.keys():
    print field
    if dico_fields[field][0] == 'Integer':
        print 'integer stats'
        for obj in range(1, layer.GetFeatureCount()+1):
            value = layer.GetFeature(obj).GetFieldAsInteger(field)
    elif dico_fields[field][0] == 'Real':
        print 'real stats'
    elif dico_fields[field][0] == 'String':
        print 'string stats'
    elif dico_fields[field][0] == 'Date':
        print 'date stats'


