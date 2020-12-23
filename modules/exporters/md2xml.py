# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         Metadata to ISO 19139
# Purpose:      Export Metadata dictionnary to a XML file according to ISO 19139
# Python:       2.7.x
# Author:       Julien Moura (https://github.com/Guts)
# Created:      07/04/2013
# Updated:      18/06/2013
#-------------------------------------------------------------------------------

################################################################################
######## Libraries import #########
###################################
# Standard library
from datetime import datetime, date
from copy import deepcopy               # advanced copy
from os import getcwd, path

# Python 3 backported
from collections import OrderedDict as OD

# 3rd party libraries
from xml.etree import ElementTree as ET

# Custom modules
from Transproj import Transproj

################################################################################
############# Classes #############
###################################

class ExportToXML:
    def __init__(self, dest, dico_layer, dico_profil, dico_fields, blabla, general, attributes):
        u"""
        Export information to .XML files according to ISO 19139 or 19110.

        dico_layer = dictionary of general information about layer
        dico_fields = dictionary of  fields definition and description
                      (only needed in case of an export to iso 19110.)
        blabla = dictionary of texts according to the language selected
        general = option to export to iso 19139. Should be always = 1
        attributes = option to export to 19110, if an attributes catalog is needed
        """
        if general == 1:
            self.iso19139(dest, dico_layer, dico_profil, blabla)
        if attributes == 1:
            self.iso19110(dest, dico_layer, dico_profil, dico_fields, blabla)

    def iso19139(self, dest, dico_layer, dico_profil, blabla):
        u"""
        Export to xml file according to the ISO 19139
        """
        # opening the template
        with open(r"data/xml/template_iso19139.xml", 'r')as iso:
            # parser
            template = ET.parse(iso)
            # namespaces
            namespaces = ET.register_namespace("gts","http://www.isotc211.org/2005/gts")
            namespaces = ET.register_namespace("gml","http://www.opengis.net/gml")
            namespaces = ET.register_namespace("xsi","http://www.w3.org/2001/XMLSchema-instance")
            namespaces = ET.register_namespace("gco","http://www.isotc211.org/2005/gco")
            namespaces = ET.register_namespace("gmd","http://www.isotc211.org/2005/gmd")
            namespaces = ET.register_namespace("gmx","http://www.isotc211.org/2005/gmx")
            namespaces = ET.register_namespace("srv","http://www.isotc211.org/2005/srv")
            # getting the elements and sub-elements structure
            tpl_root = template.getroot()
            # transform coordinates to WGS84 for catalogs display
            if dico_layer.get('EPSG') != u'None':
                u""" if ogr found the ESPG code """
                srs84 = Transproj(epsg = int(dico_layer.get('EPSG')),
                                  Xmin = dico_layer.get('Xmin'),
                                  Ymin = dico_layer.get('Ymin'),
                                  Xmax = dico_layer.get('Xmax'),
                                  Ymax = dico_layer.get('Ymax')).tupwgs84
            else:
                u""" if not... """
                srs84 = (dico_layer.get('Xmin'),
                         dico_layer.get('Ymin'),
                         dico_layer.get('Xmax'),
                         dico_layer.get('Ymax'))
            # parsing and completing template structure
            for elem in tpl_root.getiterator():
                # universal identifier to know how the metadata has been created
                if elem.tag == '{http://www.isotc211.org/2005/gmd}fileIdentifier':
                    elem[0].text = "Metadator_" + \
                                   str(datetime.today()).replace(" ", "")\
                                                        .replace(":", "")\
                                                        .replace(".","-jm-")
                # EPSG code
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}code':
                    elem[0].text = dico_layer.get(u'srs') + u" (EPSG : " + unicode(dico_layer.get(u'EPSG')) + ")"
                    continue
                # standart projection EPSG
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}codeSpace':
                    elem[0].text = 'EPSG'
                    continue
                # title
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}title':
                    elem[0].text = dico_layer.get('title')
                    continue
                # spatial extension
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}westBoundLongitude':
                    elem[0].text = str(srs84[0])
    ##                elem[0].text = str(dico_layer['Xmin'])
                    continue
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}eastBoundLongitude':
                    elem[0].text = str(srs84[2])
    ##                elem[0].text = str(dico_layer['Xmax'])
                    continue
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}southBoundLatitude':
                    elem[0].text = str(srs84[1])
    ##                elem[0].text = str(dico_layer['Ymin'])
                    continue
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}northBoundLatitude':
                    elem[0].text = str(srs84[3])
    ##                elem[0].text = str(dico_layer['Ymax'])
                    continue
                # description
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}abstract':
                    elem[0].text = dico_profil['description']
                    continue
                # update rythm
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}status':
                    elem[0].attrib['codeListValue'] = dico_profil['rythm']
                    continue
                # infos descriptives
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}MD_DataIdentification':
                    infos = elem
                    mtc_them = infos[5]
                    mtc_geo = infos[6]
                    lg_don = infos[10]
                    continue
                # scale
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}MD_RepresentativeFraction':
                    scale = elem
                    scale[0][0].text = str(dico_profil.get('echelle'))
                    continue
                # distribution
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}MD_DigitalTransferOptions':
                    distrib = elem
                    siteweb = distrib[0][0]
                    siteweb[0][0].text = dico_profil.get('url')
                    siteweb[2][0].text = dico_profil.get('url_label')
                    continue
                # creation date
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}CI_Date' \
                and elem[1][0].attrib['codeListValue'] == 'creation':
                    elem[0][0].text = dico_layer.get(u'date_crea')
##                    crea = date.isoformat(datetime(crea[0], crea[1], crea[2]))
##                    elem[0][0].text = crea
                # last update
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}CI_Date' \
                and elem[1][0].attrib['codeListValue'] == 'revision':
                    elem[0][0].text = dico_layer.get(u'date_actu')
##                    reviz = date.isoformat(datetime(reviz[0], reviz[1], reviz[2]))
##                    elem[0][0].text = reviz
                # format
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}MD_Format':
                    elem[0][0].text = 'ESRI Shapefile'

            tpl_cat = list(tpl_root)

            # metadata language
            lg_met = tpl_cat[1]
            list(lg_met)[0].text = dico_profil[u'lang_md']

            # data language
            list(lg_don)[0].text = dico_profil[u'lang_data']

            # metadata date
            tpl_cat[4][0].text = str(datetime.today())[:-7]

            # Contact
            ct_cont = tpl_cat[3][0]
            list(ct_cont)[0][0].text = dico_profil[u'cont_name']
            list(ct_cont)[1][0].text = dico_profil[u'cont_orga']
            list(ct_cont)[2][0].text = dico_profil[u'cont_role']
            cont_info = list(ct_cont)[3][0]
            cont_phone = list(cont_info)[0]
            list(cont_phone)[0][0][0].text = dico_profil['cont_phone']
            cont_adress = list(cont_info)[1]
            adress = list(cont_adress[0])[0]
            adress[0].text = dico_profil['cont_street']
            ville = list(cont_adress[0])[1]
            ville[0].text = dico_profil['cont_city']
            cp = list(cont_adress[0])[2]
            cp[0].text = dico_profil['cont_cp']
            pays = list(cont_adress[0])[3]
            pays[0].text = dico_profil['cont_country']
            mail = list(cont_adress[0])[4]
            mail[0].text = dico_profil['cont_mail']
            fonction = list(ct_cont)[4]
            fonction[0].attrib['codeListValue'] = dico_profil['cont_func']

            # Responsable
            ct_resp = list(infos[3][0])
            ct_resp[0][0].text = dico_profil[u'resp_name']
            ct_resp[1][0].text = dico_profil[u'resp_orga']
            ct_resp[2][0].text = dico_profil[u'resp_role']
            resp_info = list(ct_resp[3][0])
            resp_info[0][0][0][0].text = dico_profil[u'resp_phone']
            resp_adress = list(resp_info[1][0])
            resp_adress[0][0].text = dico_profil['resp_street']
            resp_adress[1][0].text = dico_profil['resp_city']
            resp_adress[2][0].text = dico_profil['resp_cp']
            resp_adress[3][0].text = dico_profil['resp_country']
            resp_adress[4][0].text = dico_profil['resp_mail']

            # thematics keywords
            for i in dico_profil.get('keywords'):
                infos.append(deepcopy(mtc_them))
            infos.remove(mtc_them)
            x = 0
            for tem in list(infos):
                if tem.tag == '{http://www.isotc211.org/2005/gmd}descriptiveKeywords' \
                and tem[0][1][0].attrib['codeListValue'] == 'theme':
                    tem[0][0][0].text = dico_profil.get('keywords')[x]
                    x = x+1

            # places keywords
            for i in dico_profil.get('geokeywords'):
                infos.append(deepcopy(mtc_geo))
            infos.remove(mtc_geo)
            y = 0
            for tem in list(infos):
                if tem.tag == '{http://www.isotc211.org/2005/gmd}descriptiveKeywords' \
                and tem[0][1][0].attrib['codeListValue'] == 'place':
                    tem[0][0][0].text = dico_profil.get('geokeywords')[y]
                    y = y+1

            # saving the xml file
            template.write(path.join(dest + "/{0}_MD.html".format(dico_layer['name'][:-4])),
                           encoding='utf-8',
                           xml_declaration='version="1.0"',
                           default_namespace=namespaces,
                           method='xml')
        # End of function
        return template

    def iso19110(self, dest, dico_layer, dico_profil, dico_fields, blabla):
        u"""
        Export to xml file according to the ISO 19110
        """
        print 'attributes catalog '

################################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    """ Test parameters for a stand-alone run """
    print 'Only for a use with Metadator'
