# -*- coding: UTF-8 -*-
#!/usr/bin/env python

# test modules
from modules.Transproj import Transproj



srsWgs84 = Transproj(epsg = 4267,             # srs déjà au bon référentiel
                Xmin = -77.15,         # emprise du train de Lima et Callao
                Ymin = -12.05,
                Xmax = -76.69,
                Ymax = -11.93)

srsLima = Transproj(epsg = 32718,             # srs WGS84
                Xmin = 262028.43,         # emprise de Lima et Callao
                Ymin = 8619304.41,
                Xmax = 312275.75,
                Ymax = 8697720.65)


print srsWgs84.tupwgs84
print srsLima.tupwgs84