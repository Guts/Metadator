# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
# -----------------------------------------------------------------------------
# Name:        Transproj
# Purpose:     Reproject coordinates from a bounding box into WGS84 according
#              to EPSG code
# Python:      2.7.x
# Author:      Julien Moura
# Created:     22/01/2013
# Updated:     18/06/2013
# -----------------------------------------------------------------------------

###############################################################################
######## Libraries import #########
###################################

# 3rd party libraries
from osgeo import osr   # pour les projections
from osgeo.gdal import SetConfigOption    # variables environnement de gdal

###############################################################################
############# Classes #############
###################################

class Transproj:
    u""" Transforme les coordonnées des bornes de l'emprise  spatiale en wgs84
    d'après le code EPSG, s'il est différent du référentiel voulu. """
    def __init__(self, epsg, Xmin, Ymin, Xmax, Ymax):
        u""" Teste si le code EPSG est différent du srs WGS84 (4362) """
        if epsg == 4326:
            self.tupliz(Xmin, Ymin, Xmax, Ymax)
        else:
            # projection en entrée
            self.projou = osr.SpatialReference()
            self.projou.ImportFromEPSG(epsg)
            # projection en sortie
            self.wgs84 = osr.SpatialReference()
            self.wgs84.ImportFromEPSG(4326)
            # reprojection
            self.reproj(self.projou, self.wgs84, Xmin, Ymin, Xmax, Ymax)

    def reproj(self, FromProj, ToProj, minX, minY, maxX, maxY):
        u""" Reprojette les bornes de l'emprise spatiale en
        paramètres (minX, minY, maxX, maxY) depuis la projection FromProj vers
        ToProj (WGS84). """
        # crée l'instance de transformation
        self.transf = osr.CoordinateTransformation(self.projou, self.wgs84)
        # transformation
        self.res1 = self.transf.TransformPoint(minX, minY)
        self.res2 = self.transf.TransformPoint(maxX, maxY)
        # tuplization !
        self.tupliz(self.res1[1], self.res1[0], self.res2[1], self.res2[0])

    def tupliz(self, X1, Y1, X2, Y2):
        u""" Création tuple des coordonnées en WGS 84 - EPSG 4326 """
        self.tupwgs84 = (X1,  # Xmin
                         Y1,  # Ymin
                         X2,  # Xmax
                         Y2)  # Ymax
        # End of function
        return self.tupwgs84

###############################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    """ Test parameters for a stand-alone run """
    from os import environ as env
    # checking the path
    if "GDAL_DATA" not in env.keys():
        SetConfigOption(str('GDAL_DATA'), str(path.abspath(r'data/gdal')))
    else:
        pass
    # transforming coordinates
    srstest = Transproj(epsg=32718,             # srs WGS84 UTM 18 S
                        Xmin=262028.43,         # emprise de Lima et Callao
                        Ymin=8619304.41,
                        Xmax=312275.75,
                        Ymax=8697720.65)
    print srstest.tupwgs84

    srstest2 = Transproj(epsg=4267,             # from the airports sample data
                         Xmin=-4480198.52,
                         Ymin=1433525.8,
                         Xmax=4615124.98,
                         Ymax=6502586.83)
    print srstest2.tupwgs84
