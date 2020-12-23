# -*- coding: UTF-8 -*-
#!/usr/bin/env python
##from __future__ import unicode_literals
#------------------------------------------------------------------------------
# Name:         InfosOGR
# Purpose:      Use GDAL/OGR library to extract informations about
#                   geographic data. It permits a more friendly use as
#                   submodule.
#
# Author:       Julien Moura (https://github.com/Guts/)
#
# Python:       2.7.x
# Created:      18/02/2013
# Updated:      13/08/2014
# Licence:      GPL 3
#------------------------------------------------------------------------------

###############################################################################
########### Libraries #############
###################################
# Standard library
from os import path, chdir, listdir  # files and folder managing
from time import localtime, strftime

# Python 3 backported
from collections import OrderedDict as OD

# 3rd party libraries
try:
    from osgeo import gdal
    from osgeo import ogr  # handler for vector spatial files
    from osgeo import osr
except ImportError:
    import gdal
    import ogr  # handler for vector spatial files
    import osr

###############################################################################
########### Classes #############
#################################


class OGRErrorHandler(object):
    def __init__(self):
        """ Callable error handler
        see: http://trac.osgeo.org/gdal/wiki/PythonGotchas#Exceptionsraisedincustomerrorhandlersdonotgetcaught
        and http://pcjericks.github.io/py-gdalogr-cookbook/gdal_general.html#install-gdal-ogr-error-handler
        """
        self.err_level = gdal.CE_None
        self.err_type = 0
        self.err_msg = ''

    def handler(self, err_level, err_type, err_msg):
        """ Making errors messages more readable """
        # available types
        err_class = {
                    gdal.CE_None: 'None',
                    gdal.CE_Debug: 'Debug',
                    gdal.CE_Warning: 'Warning',
                    gdal.CE_Failure: 'Failure',
                    gdal.CE_Fatal: 'Fatal'
                    }
        # getting type
        err_type = err_class.get(err_type, 'None')
        
        # cleaning message
        err_msg = err_msg.replace('\n', ' ')

        # disabling OGR exceptions raising to avoid future troubles
        ogr.DontUseExceptions()

        # propagating
        self.err_level = err_level
        self.err_type = err_type
        self.err_msg = err_msg

        # end of function
        return self.err_level, self.err_type, self.err_msg


class Read_TAB():
    def __init__(self, layerpath, dico_layer, dico_fields, tipo, text=''):
        u""" Uses OGR functions to extract basic informations about
        geographic vector file (handles shapefile or MapInfo tables)
        and store into dictionaries.

        layerpath = path to the geographic file
        dico_layer = dictionary for global informations
        dico_fields = dictionary for the fields' informations
        li_fieds = ordered list of fields
        tipo = shp or tab
        text = dictionary of text in the selected language

        """
        # handling ogr specific exceptions
        ogrerr = OGRErrorHandler()
        errhandler = ogrerr.handler
        gdal.PushErrorHandler(errhandler)
        ogr.UseExceptions()
        
        # changing working directory to layer folder
        # chdir(path.dirname(layerpath))

        # Creating variables
        self.alert = 0
        # raising corrupt files
        source = ogr.Open(layerpath, 0)     # OGR driver
        if not source:
            u""" if layer doesn't have any object, return an error """
            self.erratum(dico_layer, layerpath, u'err_nobjet')
            self.alert = self.alert + 1
        else:
            pass
        self.layer = source.GetLayer()          # get the layer
        if self.layer.GetFeatureCount() == 0:
            u""" if layer doesn't have any object, return an error """
            self.erratum(dico_layer, layerpath, u'err_nobjet')
            self.alert = self.alert + 1
            return None
        else:
            pass

        obj = self.layer.GetFeature(1)        # get the first object (tab)
        self.geom = obj.GetGeometryRef()      # get the geometry

        self.def_couche = self.layer.GetLayerDefn()  # get layer definitions
        self.srs = self.layer.GetSpatialRef()   # get spatial system reference
        self.srs.AutoIdentifyEPSG()     # try to determine the EPSG code

        # basic information
        dico_layer[u'type'] = tipo
        self.infos_basics(layerpath, dico_layer, text)
        # geometry information
        self.infos_geom(dico_layer, text)
        # fields information
        self.infos_fields(dico_fields)

        # warnings messages
        dico_layer['err_gdal'] = ogrerr.err_type, ogrerr.err_msg

        # safe exit
        del source

    def infos_basics(self, layerpath, dico_layer, txt):
        u""" get the global informations about the layer """
        # srs type
        srsmetod = [
                    (self.srs.IsCompound(), txt.get('srs_comp')),
                    (self.srs.IsGeocentric(), txt.get('srs_geoc')),
                    (self.srs.IsGeographic(), txt.get('srs_geog')),
                    (self.srs.IsLocal(), txt.get('srs_loca')),
                    (self.srs.IsProjected(), txt.get('srs_proj')),
                    (self.srs.IsVertical(), txt.get('srs_vert'))
                   ]
        # searching for a match with one of srs types
        for srsmet in srsmetod:
            if srsmet[0] == 1:
                typsrs = srsmet[1]
            else:
                continue
        # in case of not match
        try:
            dico_layer[u'srs_type'] = unicode(typsrs)
        except UnboundLocalError:
            typsrs = txt.get('srs_nr')
            dico_layer[u'srs_type'] = unicode(typsrs)
        # Storing into the dictionary
        dico_layer[u'name'] = path.basename(layerpath)
        dico_layer[u'folder'] = path.dirname(layerpath)
        dico_layer[u'title'] = dico_layer[u'name'][:-4].replace('_', ' ').capitalize()
        dico_layer[u'num_obj'] = self.layer.GetFeatureCount()
        dico_layer[u'num_fields'] = self.def_couche.GetFieldCount()
        
        # dependencies
        dependencies = [f for f in listdir(path.dirname(layerpath))
                        if path.splitext(path.abspath(f))[0] == path.splitext(layerpath)[0]
                        and not path.splitext(path.abspath(f).lower())[1] == ".tab"]
        dico_layer[u'dependencies'] = dependencies

        # total file and dependencies size
        dependencies.append(layerpath)
        total_size = sum([path.getsize(f) for f in dependencies])
        dico_layer[u"total_size"] = self.sizeof(total_size)
        dependencies.pop(-1)

        # Handling exception in srs names'encoding
        try:
            if self.srs.GetAttrValue('PROJCS') != 'unnamed':
                dico_layer[u'srs'] = unicode(self.srs.GetAttrValue('PROJCS')).replace('_', ' ')
            else:
                dico_layer[u'srs'] = unicode(self.srs.GetAttrValue('PROJECTION')).replace('_', ' ')
        except UnicodeDecodeError:
            if self.srs.GetAttrValue('PROJCS') != 'unnamed':
                dico_layer[u'srs'] = self.srs.GetAttrValue('PROJCS').decode('latin1').replace('_', ' ')
            else:
                dico_layer[u'srs'] = self.srs.GetAttrValue('PROJECTION').decode('latin1').replace('_', ' ')
        finally:
            dico_layer[u'EPSG'] = unicode(self.srs.GetAttrValue("AUTHORITY", 1))
        # Getting basic dates
        dico_layer[u'date_actu'] = strftime('%Y-%m-%d',
                                            localtime(path.getmtime(layerpath)))
        dico_layer[u'date_crea'] = strftime('%Y-%m-%d',
                                            localtime(path.getctime(layerpath)))
        # World SRS default
        if dico_layer[u'EPSG'] == u'4326' and dico_layer[u'srs'] == u'None':
            dico_layer[u'srs'] = u'WGS 84'
        else:
            pass

        # end of function
        return dico_layer

    def infos_geom(self, dico_layer, txt):
        u""" get the informations about geometry """
        # type géométrie
        if self.geom.GetGeometryName() == u'POINT':
            dico_layer[u'type_geom'] = txt.get('geom_point')
        elif u'LINESTRING' in self.geom.GetGeometryName():
            dico_layer[u'type_geom'] = txt.get('geom_ligne')
        elif u'POLYGON' in self.geom.GetGeometryName():
            dico_layer[u'type_geom'] = txt.get('geom_polyg')
        else:
            dico_layer[u'type_geom'] = self.geom.GetGeometryName()
        # Spatial extent (bounding box)
        dico_layer[u'Xmin'] = round(self.layer.GetExtent()[0], 2)
        dico_layer[u'Xmax'] = round(self.layer.GetExtent()[1], 2)
        dico_layer[u'Ymin'] = round(self.layer.GetExtent()[2], 2)
        dico_layer[u'Ymax'] = round(self.layer.GetExtent()[3], 2)
        # end of function
        return dico_layer

    def infos_fields(self, dico_fields):
        u""" get the informations about fields definitions """
        for i in range(self.def_couche.GetFieldCount()):
            champomy = self.def_couche.GetFieldDefn(i)  # ordered fields
            dico_fields[champomy.GetName()] = champomy.GetTypeName(),\
                                              champomy.GetWidth(),\
                                              champomy.GetPrecision()
        # end of function
        return dico_fields

    def sizeof(self, os_size):
        u""" return size in different units depending on size
        see http://stackoverflow.com/a/1094933 """
        for size_cat in ['octets', 'Ko', 'Mo', 'Go']:
            if os_size < 1024.0:
                return "%3.1f %s" % (os_size, size_cat)
            os_size /= 1024.0
        return "%3.1f %s" % (os_size, " To")

    def erratum(self, dicolayer, layerpath, mess):
        u""" errors handling """
        # local variables
        dicolayer[u'name'] = path.basename(layerpath)
        dicolayer[u'folder'] = path.dirname(layerpath)
        try:
            def_couche = self.layer.GetLayerDefn()
            dicolayer[u'num_fields'] = def_couche.GetFieldCount()
        except AttributeError:
            mess = mess    
        finally:
            dicolayer[u'error'] = mess
        # End of function
        return dicolayer

###############################################################################
###### Stand alone program ########
###################################

if __name__ == '__main__':
    u""" standalone execution for tests. Paths are relative considering a test
    within the official repository (https://github.com/Guts/DicoGIS)"""
    # libraries import
    from os import getcwd
    # test files
    li_tab = [path.join(getcwd(),
                        r'..\..\\test\samples\tab\airports_MI.tab')
              ]  # MapInfo table
    # test text dictionary
    textos = OD()
    textos['srs_comp'] = u'Compound'
    textos['srs_geoc'] = u'Geocentric'
    textos['srs_geog'] = u'Geographic'
    textos['srs_loca'] = u'Local'
    textos['srs_proj'] = u'Projected'
    textos['srs_vert'] = u'Vertical'
    textos['geom_point'] = u'Point'
    textos['geom_ligne'] = u'Line'
    textos['geom_polyg'] = u'Polygon'
    # recipient datas
    dico_layer = OD()     # dictionary where will be stored informations
    dico_fields = OD()     # dictionary for fields information
    # execution
    for tab in li_tab:
        """ looping on MapInfo tables list """
        # reset recipient data
        dico_layer.clear()
        dico_fields.clear()
        # getting the informations
        info_tab = Read_TAB(path.abspath(tab),
                            dico_layer,
                            dico_fields,
                            'MI table',
                            textos)
        print '\n', dico_layer, dico_fields
