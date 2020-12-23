#-*-coding: utf-8-*-
#!/usr/bin/env python

# tips from: http://pcjericks.github.io/py-gdalogr-cookbook/layers.html#get-all-postgis-layers-in-a-postgresql-database

import ogr

def shptopg():
    conn = ogr.Open("PG: host='postgresql1.alwaysdata.com' dbname='guts_gis' user='guts_player' password='letsplay'")
    print conn
    x = 0
    print "Number of layers: %s" % len(conn)


    for layer in conn:
        # get all the juice!
        srs = layer.GetSpatialRef()
        obj = layer.GetFeature(1)
        geom = obj.GetGeometryRef()
        def_couche = layer.GetLayerDefn()
        # print informations
        print "\n========\nLayer's name: %s" % layer.GetName()
        print "Geometry type: %s" % geom.GetGeometryName()
        print "Number of objects: %s" % layer.GetFeatureCount()
        print "Number of fields: %s" % def_couche.GetFieldCount()
        print "FID column: %s" % layer.GetFIDColumn()








    # for layer in conn:
    #     x = x+1
    #     print x
    #     j=1
    #     geom=layer.GetFeature(j)
    #     print layer, layer.GetFeatureCount()
    #     while (geom):
    #         geom=layer.GetFeature(j)
    #         geom.DumpReadable()
    #         j+=1

    conn.Destroy()

test = shptopg()