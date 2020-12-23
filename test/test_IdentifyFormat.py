# -*- coding: UTF-8 -*-
#!/usr/bin/env python
##from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         Identify format from geodatas
# Purpose:      Use GDAL/OGR library to guess the format of files.
#
# Author:       Julien Moura (https://github.com/Guts/)
#
# Python:       2.7.x
# Created:      23/06/2014
# Updated:      23/06/2014
# Licence:      GPL 3
#-------------------------------------------------------------------------------

################################################################################
########### Libraries #############
###################################

# 3rd party libraries
try:
    from osgeo import ogr    # spatial files
    from osgeo import osr    # srs
    from osgeo import gdal
    from osgeo.gdalconst import *
    gdal.UseExceptions()
except:
    print('GDAL/OGR is missing')

################################################################################
########### Classes #############
###################################

class GetFormat():
    def __init__(self, datapath):
        u""" 
        Uses gdal/ogr to determine the format of the input data
        """
        try:
            """ testing if data type is raster """
            source = gdal.Open(datapath)
            driver = source.GetDriver()
            # end of function
            print driver.GetName()
        except Exception as e:
            if u'not recognised as a supported file format.' in e.message:
                try:
                    """ testing if data type is vector """
                    source = ogr.Open(datapath)
                    driver = source.GetDriver()
                    # end of function
                    print driver.GetName()
                except:
                    print("Oups, neither GDAL and OGR couln't open this dataset.")
            else:
                pass

################################################################################
###### Stand alone program ########
###################################

if __name__ == '__main__':
    u""" standalone execution for tests. Paths are relative to the Isogeo private network (https://www.isogeo.com) """
    # Only for testing from Isogeo network
    mdb_esri = r'\\nas.hq.isogeo.fr\SIG\SIG_DATA_SERVICE\TEST\05_DB\MDB\mdb_esri\TEST_ISOGEO.mdb'
    mdb_intg = r'\\nas.hq.isogeo.fr\SIG\SIG_DATA_SERVICE\TEST\05_DB\MDB\mdb_intergraph\REC_RES_S.mdb'
    shapefiles = r'\\nas.hq.isogeo.fr\SIG\SIG_DATA_SERVICE\TEST\01_VECTOR\Shapefiles\Foret_Publiques_Basse_Normandie.shp'

    # getting formats
    GetFormat(mdb_esri)
    GetFormat(mdb_intg)
    GetFormat(shapefiles)