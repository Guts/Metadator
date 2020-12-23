#-*-coding: utf-8-*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         OGR Drivers'availability
# Purpose:      Class to test if GDAL/OGR and their Python bindings are installed
#               and which drivers are installed. Could be imported as a submodule.
#
# Author:       Julien Moura (https://github.com/Guts)
#
# Created:      24/06/2013
# Updated:      16/07/2013
# Licence:      GPL 3
# Credits:      http://pcjericks.github.io/py-gdalogr-cookbook
#-------------------------------------------------------------------------------

################################################################################
######## Libraries import #########
###################################

# 3rd party libraries
try:
  from osgeo import ogr
  print "Import worked. All seems to be fine. Let's got to work!\n"
except:
  print 'Import failed: check your installation.\n\n'


################################################################################
############# Classes #############
###################################

class OGR_DriversCheck:
    """ Main class """
    def __init__(self):
        """ """

    def check_shp(self):
        """ Is Shapefile ogr driver available ?"""
        driverName = "ESRI Shapefile"
        driver = ogr.GetDriverByName( driverName )
        if driver is None:
            print "%s driver not available." % driverName
            return 0
        else:
            print  "%s driver IS available." % driverName
            return 1

    def check_pg(self):
        """ Is PostgreSQL ogr driver available ? """
        driverName = "PostgreSQL"
        driver = ogr.GetDriverByName( driverName )
        if driver is None:
            print "%s driver not available." % driverName
            return 0
        else:
            print  "%s driver IS available." % driverName
            return 1

    def check_gdb(self):
        """ Is File GeoDatabase ogr driver available ?? """
        driverName = "FileGDB"
        driver = ogr.GetDriverByName( driverName )
        if driver is None:
            print "%s driver not available." % driverName
            return 0
        else:
            print  "%s driver IS available." % driverName
            return 1

    def list_drivers(self):
        """ return an alphabetical list of available ogr drivers """
        cnt = ogr.GetDriverCount()  # number of available drivers
        driversList = []
        for i in range(cnt):
            driver = ogr.GetDriver(i)
            driverName = driver.GetName()
            if not driverName in driversList:
                driversList.append(driverName)
        # end of function
        return driversList

################################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    """ Test parameters for a stand-alone run """
    ogr_check = OGR_DriversCheck()
    ogr_check.check_shp()
    ogr_check.check_pg()
    ogr_check.check_gdb()
    print ogr_check.list_drivers()
