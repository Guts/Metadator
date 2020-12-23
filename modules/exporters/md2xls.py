# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         Metadata to Excel
# Purpose:      Export Metadata dictionnary into a Excel (.xls) file.
# Python:       2.7.x
# Author:       Julien Moura (https://github.com/Guts)
# Created:      07/04/2013
# Updated:      21/06/2013
#-------------------------------------------------------------------------------

################################################################################
######## Libraries import #########
###################################

# Standard library
from os import  path
#from threading import Thread
#from threading import Event

# 3rd party library
from xlwt import Workbook, easyxf, Font, XFStyle, Formula, Alignment  # Excel handler

################################################################################
############# Classes #############
###################################

class ExportToXLS():
    """ object to export metadata dictionary to html """
    def __init__(self, dest, dico_layer, dico_fields, dico_profil, dico_rekurs, dico_text):
        u"""
        Parameters depending on Metadator main class
        dest : destination folder path
        dico_layer : dictionary about layer
        dico_fields : dictionary about layers's fields
        dico_profil : dictionary about profile selected informations
        dico_rekurs : dictionary about recurring fields
        dico_text : dictionary of text according to language selected
        """
        # creating the excel workbook
        self.wb = Workbook(encoding='utf8')
        self.feuy1 = self.wb.add_sheet(dico_text.get('xls_feuy1'), cell_overwrite_ok = True)
        self.feuy2 = self.wb.add_sheet(dico_text.get('xls_feuy2'), cell_overwrite_ok = True)

        self.xls_headers(dico_text, dico_layer.get('title'))
        self.xls_globalmd(dico_layer, dico_profil, dico_text)
        self.xls_attributes(dico_layer, dico_fields, dico_profil, dico_text, dico_rekurs)



        # some adjustments
        self.feuy1.col(0).width = 44*256
        self.feuy2.col(2).width = 10*256
        self.feuy2.col(2).width = 18*256

        # saving the excel
        outxls = path.join(dest, "{0}_MD.xls".format(dico_layer['name'][:-4]))
        self.wb.save(outxls)


    def xls_headers(self, text, title):
        u"""

        """
        # headers style
        header1 = easyxf()
        header2 = easyxf()
            # font
        font1 = Font()
        font1.name = 'Times New Roman'
        font1.bold = True
            # alignment
        alig1 = Alignment()
        alig1.horz = 2
            # assign
        header1.font = font1
        header1.alignment = alig1
        header2.font = font1

        # headers 1st sheet
        self.feuy1.write_merge(0, 0, 0, 1,  text.get('titre') +
                                            title,
                                            header1)
        self.feuy1.write(1, 0, text.get('nomfic'), header2)
        self.feuy1.write(2, 0, text.get('mtcthem'), header2)
        self.feuy1.write(3, 0, text.get('mtcgeo'), header2)
        self.feuy1.write(4, 0, text.get('description'), header2)
        self.feuy1.write(5, 0, text.get('cadre'), header2)
        self.feuy1.write(6, 0, text.get('num_objets'), header2)
        self.feuy1.write(7, 0, text.get('num_attrib'), header2)
        self.feuy1.write(8, 0, text.get('date_crea'), header2)
        self.feuy1.write(9, 0, text.get('date_actu'), header2)
        self.feuy1.write(10, 0, text.get('source'), header2)
        self.feuy1.write(11, 0, text.get('diffusion'), header2)
        self.feuy1.write(12, 0, text.get('responsable'), header2)
        self.feuy1.write(13, 0, text.get('ptcontact'), header2)
        self.feuy1.write(14, 0, text.get('siteweb'), header2)
        self.feuy1.write(15, 0, text.get('geometrie'), header2)
        self.feuy1.write(16, 0, text.get('echelle'), header2)
        self.feuy1.write(17, 0, text.get('precision'), header2)
        self.feuy1.write(18, 0, text.get('srs'), header2)
        self.feuy1.write(19, 0, text.get('emprise'), header2)
        # headers 2nd sheet
        self.feuy2.write(0, 0,  text.get('numero'), header2)
        self.feuy2.write(0, 1,  text.get('nom'), header2)
        self.feuy2.write(0, 2,  text.get('type'), header2)
        self.feuy2.write(0, 3,  text.get('longueur'), header2)
        self.feuy2.write(0, 4,  text.get('precision'), header2)
        self.feuy2.write(0, 5,  text.get('description'), header2)
        self.feuy2.write(0, 6,  text.get('somme'), header2)
        self.feuy2.write(0, 7,  text.get('moyenne'), header2)
        self.feuy2.write(0, 8,  text.get('mediane'), header2)
        self.feuy2.write(0, 9,  text.get('min'), header2)
        self.feuy2.write(0, 10,  text.get('max'), header2)
        self.feuy2.write(0, 11,  text.get('ecartype'), header2)

        # End of function
        return self.feuy1, self.feuy2

    def xls_globalmd(self, layer, profil, text):
        u"""

        """
        # styles
        hyperlien = easyxf(u'font: underline single')   # for weblinks

        # remplissage fiche générale (feuille 1)
        self.feuy1.write(1, 1, layer[u'name'])
        keywords = ', '.join(profil.get(u'keywords'))
        self.feuy1.write(2, 1, keywords)
        geokeywords = ', '.join(profil.get(u'geokeywords'))
        self.feuy1.write(3, 1, geokeywords)
        self.feuy1.write(4, 1,  text.get('acompleter'))
        self.feuy1.write(5, 1, profil.get(u'description'))
        self.feuy1.write(6, 1, str(layer.get(u'num_obj')))
        self.feuy1.write(7, 1, str(layer.get(u'num_fields')))
        self.feuy1.write(8, 1, layer.get(u'date_crea'))
        self.feuy1.write(9, 1, layer.get(u'date_actu'))
        self.feuy1.write(10, 1, profil.get('sources'))
        self.feuy1.write(11, 1, profil.get('diffusion'))
        self.feuy1.write(12, 1, profil.get('resp_name') \
                           + u' ('   + profil.get('resp_orga') \
                           + u'), '  + profil.get('resp_mail'))
        self.feuy1.write(13, 1, profil.get('cont_name') \
                           + u' ('   + profil.get('cont_orga') \
                           + u'), '  + profil.get('cont_mail'))
        lien = 'HYPERLINK("' + profil.get('url') + '"; "' \
                + profil.get('url_label') + '")'    # formatage URL
        self.feuy1.write(14, 1, Formula(lien), hyperlien)
        self.feuy1.write(15, 1, layer.get('type_geom'))
    ##    self.feuy1.write(16, 1, unicode(profil.get('echelle')))
    ##    self.feuy1.write(17, 1, unicode(profil.get('precision')))
        self.feuy1.write(18, 1, u"Projection : " + \
                           layer.get('srs') + \
                           u" - Code EPSG : " +
                           unicode(layer.get('EPSG')))
        self.feuy1.write(19, 1, u'Min X : '+
                           str(layer[u'Xmin']) +
                           u' - Max X : ' +
                           str(layer[u'Xmax']) +
                           u' // Min Y : '+
                           str(layer[u'Ymin']) +
                           u' - Max Y : ' +
                           str(layer[u'Ymax']))
        # End of function
        return self.feuy1

    def xls_attributes(self, layer, fields, profil, text, rekurs):
        u"""

        """
        # styles




        # attributes on 2nd sheet
        lig = 1
        for chp in fields.keys():
            """ parsing the fields """
            # more friendly local variables
            lg = fields[chp][0][1]
            prec = fields[chp][0][2]
            desc = fields[chp][1]
            # common informations
            self.feuy2.write(lig, 0, str(lig))          # order
            try:
                self.feuy2.write(lig, 1, chp)               # name
            except UnicodeDecodeError:
                self.feuy2.write(lig, 1, chp.decode('latin1'))               # name
            self.feuy2.write(lig, 5, desc)          # description
            self.feuy2.write(lig, 3, lg)            # lenght
            # field information depending on field type
            if fields[chp][0][0] == 'Integer':
                u""" for integers """
                self.feuy2.write(lig, 2, text.get('entier'))      # type
                if fields[chp][2]:
                    # more friendly local variables
                    som = fields[chp][2][0]
                    med = fields[chp][2][1]
                    moy = fields[chp][2][2]
                    uppest = fields[chp][2][3]
                    bottom = fields[chp][2][4]
                    freq = fields[chp][2][5]
                    mod = fields[chp][2][6]
                    ect = fields[chp][2][7]
                    vid = fields[chp][2][8]
                    # write informations
                    self.feuy2.write(lig, 6, som)                   # sum
                    self.feuy2.write(lig, 7, moy)                   # mean
                    self.feuy2.write(lig, 8, med)                   # mediane
                    self.feuy2.write(lig, 9, bottom)                # minimum
                    self.feuy2.write(lig, 10, uppest)               # maximum
                    self.feuy2.write(lig, 11, ect)                  # std deviation
                else:
                    pass
            elif fields[chp][0][0] == 'Real':
                u""" for reals / float """
                self.feuy2.write(lig, 2, text.get('reel'))      # type
                self.feuy2.write(lig, 4, prec)        # precision
                if fields[chp][2]:
                    # more friendly local variables
                    som = fields[chp][2][0]
                    med = fields[chp][2][1]
                    moy = fields[chp][2][2]
                    uppest = fields[chp][2][3]
                    bottom = fields[chp][2][4]
                    freq = fields[chp][2][5]
                    mod = fields[chp][2][6]
                    ect = fields[chp][2][7]
                    vid = fields[chp][2][8]
                    # write informations
                    self.feuy2.write(lig, 6, som)                   # sum
                    self.feuy2.write(lig, 7, moy)                   # mean
                    self.feuy2.write(lig, 8, med)                   # mediane
                    self.feuy2.write(lig, 9, bottom)                # minimum
                    self.feuy2.write(lig, 10, uppest)               # maximum
                    self.feuy2.write(lig, 11, ect)                  # std deviation
                else:
                    pass
            elif fields[chp][0][0] == 'String':
                u""" for caracter string """
                self.feuy2.write(lig, 2,  text.get('string'))   # type
            elif fields[chp][0][0] == 'Date':
                u""" for dates """
                self.feuy2.write(lig, 2,  text.get('date'))     #type
            # next field -> new line
            lig = lig +1
        # End of function
        return self.feuy2


################################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    """  """
    test = ExportToXLS()
