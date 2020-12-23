# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         Metadata to HTML
# Purpose:      Export Metadata dictionnary to a html file
# Python:       2.7.x
# Author:       Julien Moura (https://github.com/Guts)
# Created:      07/04/2013
# Updated:      21/06/2013
#-------------------------------------------------------------------------------

################################################################################
######## Libraries import #########
###################################

# Standard library
from datetime import date, datetime
from os import environ as env
from os import  path

# 3rd party library
import codecs   # make encoding easier


################################################################################
############# Classes #############
###################################

class ExportToHTML():
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
        # variables
        html_path = path.join(dest, "{0}_MD.html".format(dico_layer['name'][:-4]))
        self.tab = u'\t' # just a tab
        self.style_normal = u"style = font-family:Calibri; font-size: 11pt"
        self.style_title = u"style = font-family:Calibri; font-size: 12pt; background:#F3F3F3"
        with codecs.open(html_path, 'wb', 'utf-8-sig') as self.html:
            self.basic_html(dico_layer, dico_fields, dico_profil, dico_text, dico_rekurs)

    def basic_html(self, layer, fields, profil, text, rekurs):
        """  """
        # local variables
        tab = self.tab
        style_normal = self.style_normal
        style_title = self.style_title
        # main tag
        self.html.write(u"<!DOCTYPE html>\n<HTML lang='%s'>\n" % profil.get(u'lang_md')[:2])
            ## HEAD
        self.html.write(u"<HEAD>\n<TITLE>%s%s</TITLE>" % (text.get('titre'), layer.get('name')))
        self.html.write(u"\n<META CHARSET='UTF-8'>")
        self.html.write(u"\n<meta name='author' content='%s' >" % env.get(u'USERNAME'))
        self.html.write(u"\n<meta name='revised' content='%s' >" % date.isoformat(date.today()))
        self.html.write(u"\n<meta name='description' content='%s' >" % profil.get('description'))
        self.html.write(u"\n<meta name='keywords' content='%s' >" %  ', '.join(profil.get('keywords')))
        self.html.write(u"\n<meta name='generator' content=Metadator' >")
        self.html.write(u"\n</HEAD>\n")

            ## BODY - table
        self.html.write(tab + u'<BODY>\n')
        # create the table
        self.html.write(tab*2 + u'<table border="1" style="border-collapse: collapse" cellpadding="3" cellspacing="0">\n')

        # title
        self.html.write(tab*3 + '<tr>\n')
        self.html.write(tab*4 + u'<th align="center" colspan="2" "%s"><h2>%s %s </h2></th>\n'\
                        % (style_title, text.get('titre'), layer.get('title')))
        self.html.write(tab*3 + '</tr>\n')

        # file name
        self.html.write(tab*3 + u'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('nomfic'), 'si' )
        self.tagauto(4, u'td', u'&nbsp;' + layer.get(u'name'))
        self.html.write(tab*3 + u'</tr>\n')

        # thematic keywords
        self.html.write(tab*3 + u'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('mtcthem'), 'si')
        self.tagauto(4, u'td', u'&nbsp;' + ', '.join(profil.get(u'keywords')))
        self.html.write(tab*3 + '</tr>\n')

        # places keywords
        self.html.write(tab*3+'<tr>\n')
        self.tagauto(4,'th',u'&nbsp;' + text.get('mtcgeo'), 'si')
        self.tagauto(4, u'td', u'&nbsp;' + ', '.join(profil.get(u'geokeywords')))
        self.html.write(tab*3+'</tr>\n')

        # description
        self.html.write(tab*3 + '<tr>\n')
        self.tagauto(4, 'th', u'&nbsp;' + text.get('description'), 'si')
        self.tagauto(4, 'td', u'&nbsp;')
        self.html.write(tab*3 + '</tr>\n')

        # context / summary
        self.html.write(tab*3 + u'<tr>\n')
        self.tagauto(4, 'th', u'&nbsp;' + text.get('cadre'), 'si')
        self.tagauto(4, 'td', u'<p align = "justify">&nbsp;%s</p>' % profil.get(u'description'))
        self.html.write(tab*3 + '</tr>\n')

        # objects (lines) count
        self.html.write(tab*3 + u'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;%s' % text.get('num_objets'), 'si')
        self.tagauto(4, u'td', u'&nbsp;%s' % str(layer.get(u'num_obj')))
        self.html.write(tab*3 + '</tr>\n')

        # fields count
        self.html.write(tab*3 + u'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('num_attrib'), 'si')
        self.tagauto(4, u'td', u'&nbsp;' + str(layer.get(u'num_fields')))
        self.html.write(tab*3 + u'</tr>\n')

        # creation date on computer
        self.html.write(tab*3+'<tr>\n')
        self.tagauto(4,'th',u'&nbsp;' + text.get('date_crea'), 'si')
        self.tagauto(4,'td',u'&nbsp;' + str(layer.get(u'date_crea')))
        self.html.write(tab*3+'</tr>\n')

        # last update
        self.html.write(tab*3+'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('date_actu'), 'si')
        self.tagauto(4, u'td', u'&nbsp;' + layer.get(u'date_actu'))
        self.html.write(tab*3 + u'</tr>\n')

        # sources
        self.html.write(tab*3+'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('source'), 'si')
        self.tagauto(4, u'td', u'&nbsp;' + profil.get('sources'))
        self.html.write(tab*3 + '</tr>\n')

        # contraints
        self.html.write(tab*3+'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('diffusion'), 'si')
        self.tagauto(4, u'td', u'&nbsp;' + profil.get('diffusion'))
        self.html.write(tab*3 + u'</tr>\n')

        # global responsable
        self.html.write(tab*3+'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('responsable'), 'si')
        self.tagauto(4, u'td', u'&nbsp;' + profil.get('resp_name') \
                          + u' ('   + profil.get('resp_orga') \
                          + u'), '  + profil.get('resp_mail'))
        self.html.write(tab*3+'</tr>\n')

        # contact point
        self.html.write(tab*3+'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('ptcontact'), 'si')
        self.tagauto(4, u'td', u'&nbsp;' + profil.get('cont_name') \
                          + u' ('   + profil.get('cont_orga') \
                          + u'), '  + profil.get('cont_mail'))
        self.html.write(tab*3+'</tr>\n')

        # URL
        self.html.write(tab*3+'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('siteweb'), 'si')
        self.tagauto(4, u'td', u'&nbsp;<a href="' +\
                          profil.get('url') +\
                          u'" target="_blank">' +\
                          profil.get('url_label') + u'</a>')
        self.html.write(tab*3+'</tr>\n')

        # geometry
        self.html.write(tab*3 + u'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('geometrie'), 'si')
        self.tagauto(4, u'td', u'&nbsp;' + layer.get('type_geom'))
        self.html.write(tab*3 + u'</tr>\n')

        # scale
        self.html.write(tab*3+'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('echelle'), 'si')
        self.tagauto(4, u'td', u'&nbsp;1: ')
        self.html.write(tab*3 + u'</tr>\n')

        # precision
        self.html.write(tab*3+'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('precision'), 'si')
        self.tagauto(4, u'td', u'&nbsp; m')
        self.html.write(tab*3 + u'</tr>\n')

        # SRS
        self.html.write(tab*3 + u'<tr>\n')
        self.tagauto(4, u'th', u'&nbsp;' + text.get('srs'), 'si')
        self.tagauto(4, u'td', u'&nbsp;Projection : ' + \
                                  layer.get('srs') + \
                                  u'<br>' + text.get('codepsg') +
                                  unicode(layer.get('EPSG')))
        self.html.write(tab*3 + u'</tr>\n')

        # spatial extension
        self.html.write(tab*3 + u'<tr>\n')
        self.tagauto(4, u'th', tab + u'&nbsp;' + text.get('emprise'), 'si')
        self.tagauto(4, u'td align="center"', u'Max Y : ' +
                                         str(layer[u'Ymax']) +
                                         u'<br>Min X : '+
                                         str(layer[u'Xmin']) +
                                         u'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Max X : ' +
                                         str(layer[u'Xmax']) +
                                         u'<br>Min Y : '+
                                         str(layer[u'Ymin']))
        self.html.write(tab*3 + u'</tr>\n')

        # closing the table
        self.html.write(tab*2 + u'</table>\n<hr>')

            ## BODY - attributes
        self.tagauto(2, u'p', u'<br>\n' + text.get('listattributs'), 'si')
        self.html.write(tab*2 + '<p %s >' % style_normal)
        x = 0    # for the rank of the field
        for chp in fields.keys():
            u""" parsing fields"""
            x = x+1
            # field name
            self.html.write(tab*3 + u'<br>')
            try:
                u""" check the encoding of the field name """
                self.html.write(tab*3 + u'<b>' + str(x) + ' - ' + chp + u'</b>')
            except UnicodeDecodeError:
                u""" raise the exception and re-encode it """
                self.html.write(tab*3 + u'<b>' + str(x)
                                      + ' - ' + chp.decode('latin1')  # décode
                                      + u'</b>')
            self.html.write(tab*3 + u'<br>')
            # more friendly local variables
            lg = fields[chp][0][1]
            prec = fields[chp][0][2]
            desc = fields[chp][1]

##            # filters for recurring fields
##
##            li_rekurs_case = [rek.lower() for rek in rekurs.keys()]
##            if chp.lower() in li_rekurs_case:
##                print "\nHere! there is a recurring attribute!", chp
##                if rekurs.get(chp.lower())[1] == 1:
##                    print "case sensitive"
##                else:
##                    print 'no case sensitive'
##            else:
##                print "Okay, go on."

            # field information depending on field type
            if fields[chp][0][0] == 'Integer':
                u""" for integers """
                # type
                self.html.write(tab*3 + u'<b>%s</b> %s' % (text.get('type'), text.get('entier')))
                self.html.write(tab*3 + u'<br>')

                # lengh
                self.html.write(tab*3 + u'<b>%s</b> %s' % (text.get('longueur'), lg))
                self.html.write(tab*3 + u'<br>')

                # description
                self.html.write(tab*3 + u'<b>%s</b> %s' % (text.get('description'), desc))
                self.html.write(tab*3 + u'<br>')

                # basics stats only if there are'nt disabled
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

                    # basics stats
                    self.html.write(tab*3 + u'<b>%s</b>' % text.get('statsbase'))
                    self.html.write(tab*3 + u'<ul %s>' % style_normal)
                    self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('somme'), som))
                    if vid != 0:    # for null values
                        perc = round(float(vid)*100/layer.get(u'num_obj'), 2)
                        self.html.write(tab*5 + u'<li>%s%s (%s %s%s)</li>' % (text.get('valnulles'), vid, text.get('soit'), perc, text.get('perctotal')))
                    self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('min'), bottom))
                    self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('max'), uppest))
                    self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('moyenne'), moy))
                    self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('mediane'), med))
                    self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('ecartype'), ect))
                    self.html.write(tab*3 + u'</ul>')

                    # modalities
                    self.html.write(tab*3 + u'<b>%s</b> %s' % (text.get('valfreq'), mod.replace(u'\n', u'<br>')))
                    if freq > 0:
                        self.html.write(tab*3 + u'<ul %s>' % style_normal)
                        for val, okur in freq:
                            self.html.write(tab*5 + u'<li>%s (%s)</li>' % (val, okur))
                        self.html.write(tab*3 + u'</ul>')
                    else:
                        pass
                else:
                    pass

            elif fields[chp][0][0] == u'Real':
                u""" for reals / float """
                # type
                self.html.write(tab*3 + u'<b>%s</b> %s' % (text.get('type'), text.get('reel')))
                self.html.write(tab*3 + u'<br>')

                # lengh
                self.html.write(tab*3 + u'<b>%s</b> %s' % (text.get('longueur'), lg))
                self.html.write(tab*3 + u'<br>')

                # precision
                self.html.write(tab*3 + u'<b>%s</b> %s' % (text.get('precision'), prec))
                self.html.write(tab*3 + u'<br>')

                # description
                self.html.write(tab*3 + u'<b>%s</b> %s' % (text.get('description'), desc))
                self.html.write(tab*3 + u'<br>')

                # basics stats only if there are'nt disabled
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

                    # basics stats
                    self.html.write(tab*3 + u'<b>%s</b>' % text.get('statsbase'))
                    self.html.write(tab*3 + u'<ul %s>' % style_normal)
                    self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('somme'), som))
                    if vid != 0:    # for null values
                        perc = round(float(vid)*100/layer.get(u'num_obj'), 2)
                        self.html.write(tab*5 + u'<li>%s%s (%s %s%s)</li>' % (text.get('valnulles'), vid, text.get('soit'), perc, text.get('perctotal')))
                    self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('min'), bottom))
                    self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('max'), uppest))
                    self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('moyenne'), moy))
                    self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('mediane'), med))
                    self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('ecartype'), ect))
                    self.html.write(tab*3 + u'</ul>')

                    # modalities
                    self.html.write(tab*3 + u'<b>%s</b> %s' % (text.get('valfreq'), mod.replace(u'\n', u'<br>')))
                    if freq > 0:
                        self.html.write(tab*3 + u'<ul %s>' % style_normal)
                        for val, okur in freq:
                            self.html.write(tab*5 + u'<li>%s (%s)</li>' % (val, okur))
                        self.html.write(tab*3 + u'</ul>')
                    else:
                        pass

            elif fields[chp][0][0] == 'String':
                u""" for caracter string """
                # type
                self.html.write(tab*3 + u'<b>%s</b>%s' % (text.get('type'), text.get('string')))
                self.html.write(tab*3 + u'<br>')

                # lengh
                self.html.write(tab*3 + u'<b>%s</b>%s' % (text.get('longueur'), lg))
                self.html.write(tab*3 + u'<br>')

                # description
                self.html.write(tab*3 + u'<b>%s</b>%s' % (text.get('description'), desc))
                self.html.write(tab*3 + u'<br>')

                # basics stats only if there are'nt disabled
                if fields[chp][2]:
                    # more friendly local variables
                    mod = fields[chp][2][0]
                    freq = fields[chp][2][1]
                    vid = fields[chp][2][2]

                    # modalities
                    self.html.write(tab*3 + u'<b>%s</b> %s' % (text.get('txt_moda'), mod.replace(u'\n', u'<br>')))
                    if freq > 0:
                        self.html.write(tab*3 + u'<ul %s>' % style_normal)
                        for val, okur in freq:
                            try:
                                self.html.write(tab*5 + u'<li>%s (%s)</li>' % (val, okur))
                            except UnicodeDecodeError:
                                val = val.decode('latin1')
                                self.html.write(tab*5 + u'<li>%s (%s)</li>' % (val, okur))
                        self.html.write(tab*3 + u'</ul>')
                        # if null values
                        if vid != 0:
                            self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('valnulles'), vid))
                        else:
                            pass
                        self.html.write(tab*3 + '</ul>\n')
                    else:
                        pass

            elif fields[chp][0][0] == 'Date':
                u""" for dates """
                # type
                self.html.write(tab*3 + u'<b>%s</b>%s' % (text.get('type'), text.get('date')))
                self.html.write(tab*3 + u'<br>')

                # description
                self.html.write(tab*3 + u'<b>%s</b>%s' % (text.get('description'), desc))
                self.html.write(tab*3 + u'<br>')

                # basics stats only if there are'nt disabled
                if fields[chp][2]:
                    # more friendly local variables
                    uppest = fields[chp][2][0]
                    bottom = fields[chp][2][1]
                    diffdays = fields[chp][2][2]
                    freq = fields[chp][2][3]
                    mod = fields[chp][2][4]
                    vid = fields[chp][2][5]

                    # dates delta
                    if vid != layer.get(u'num_obj'):
                        u"""Si le champ n'est pas vide"""
                        self.html.write(tab*3 + u'<b>' + text.get('datancienne')
                                              + '</b> '
                                              + date.isoformat(bottom))
                        self.html.write(tab*3 + u'<br>')
                        self.html.write(tab*3 + u'<b>' + text.get('daterecente')
                                              + '</b> '
                                              + date.isoformat(uppest))
                        self.html.write(tab*3 + u'<br>')
                        self.html.write(tab*3 + u'<b>' + text.get('date_intervmax')
                                              + '</b> '
                                              + diffdays)
                        self.html.write(tab*3 + u'<br>')

                        # modalities
                        self.html.write(tab*3 + u'<b>' + text.get('txt_moda') + '</b> '
                                              + mod.replace(u'\n', u'<br>'))
                        if freq > 0:
                            self.html.write(tab*3 + u'<ul %s>' % style_normal)
                            for val, okur in freq:
                                try:
                                    self.html.write(tab*5 + u'<li>%s (%s)</li>' % (val, okur))
                                except UnicodeDecodeError:
                                    val = val.decode('utf8')
                                    self.html.write(tab*5 + u'<li>%s (%s)</li>' % (val, okur))
                            self.html.write(tab*3 + u'</ul>')
                            # if null values
                            if vid != 0:
                                self.html.write(tab*5 + u'<li>%s%s</li>' % (text.get('valnulles'), vid))
                            else:
                                pass
                            self.html.write(tab*3 + '</ul>\n')
                        else:
                            pass
                    else:
                        self.html.write(tab*3 + u'<b>' + text.get('attvide') + '</b>')
##
##            else:
##                u"""Type de champ non répertorié"""
##                # Type de champ
##                self.html.write(tab*3 + u'<b>' + text.get('type')
##                                      + u' :</b> ' + text.get('inconnu'))
##                self.html.write(tab*3 + u'<br>')
##
##                # Longueur du champ
##                self.html.write(tab*3 + u'<b>' + text.get('longueur') +
##                                        u' :</b> ' + unicode(fields[chp][1]))
##                self.html.write(tab*3 + u'<br>')
##
##                # Précision du champ
##                self.html.write(tab*3 + u'<b>' + text.get('precision') +
##                                        u' :</b> ' + unicode(fields[chp][2]))
##                self.html.write(tab*3 + u'<br>')
##
##                # Description du champ
##                self.html.write(tab*3 + u'<b>' + text.get('description') +
##                                        u':</b> ' + descript)
##                self.html.write(tab*3 + u'<br>')
##
            # separate ligne
            self.html.write('<hr>')

                    ## End of html file
        # closing
        self.html.write(tab+'<p>')
        self.html.write(tab+'</BODY>')
        self.html.write('</HTML>')

        # end of function
        return self.html


    def tagauto(self, nb_tab, mu, valor, ng =''):
        u""" Easier formatting of html tags """
        tab = self.tab
        style_normal = self.style_normal
        if ng <> u'':
            self.html.write(tab*nb_tab \
                            + u'<' \
                            + mu + ' ' + str(style_normal) \
                            + u'><b>' + valor \
                            + u'</b></'+ mu + u'>\n')
        else:
            self.html.write(tab*nb_tab \
                            + u'<' \
                            + mu + ' ' + str(style_normal) \
                            + u'>' + valor + u'</'+ mu + u'>\n')
        # End of function
        return self.html


################################################################################
##### Stand alone execution #######
###################################
if __name__ == '__main__':
    """  stand-alone execution"""
    print 'To be launched from Metadator'
