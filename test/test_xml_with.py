# -*- coding: UTF-8 -*-
#!/usr/bin/env python

from xml.etree import ElementTree as ET     # pour les xml
import xlwt

dico_fonctions = {}

print u'youpiño'
print 'youpiño'

with open(r'locale\FR\fonctions_FR.xml', 'r') as fic:
    xml = ET.parse(fic)
    for fonction in xml.findall('fonction'):
        nom = fonction.find('intitule').text
        trad = fonction.find('identifiant').text
        dico_fonctions[nom] = trad
    fic.close()



