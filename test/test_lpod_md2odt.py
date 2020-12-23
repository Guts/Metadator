# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         Metadata to ODT
# Purpose:      Export Metadata dictionnary into a ODF document (.odt).
# Python:       2.7.x
# Author:       Julien Moura (https://github.com/Guts)
# Created:      13/10/2013
# Updated:      14/10/2013
# credits:      inspired by the code snippets included in Linux Magazine HS 53
#-------------------------------------------------------------------------------

################################################################################
######## Libraries import #########
###################################

# Standard library
from os import  path

# 3rd party library
##from lpod.document import odf_new_document
##from lpod.heading import odf_create_heading
##from lpod.paragraph import odf_create_paragraph
##from lpod.link import odf_create_link
##from lpod.list import odf_create_list, odf_create_list_item
##from lpod.table import odf_create_table, odf_create_row, odf_create_cell
##from lpod.section import odf_create_section
##
### for cell style
##from lpod.style import *
##from lpod.style import make_table_cell_border_string
##from lpod.style import odf_create_style

################################################################################
############# Classes #############
###################################

class ExportToODT():
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
        # creating the document
        doc_obj = odf_new_document("text")  # create a new document object
        self.doc_body = doc_obj.get_body()       # the body object

        # styles
        style_heading1 = odf_create_style('paragraph',
                                          name='Heading 1',
                                          parent='Standard',
                                          font='Verdana',
                                          size='54pt',
                                          weight='bold',
                                          break_before = 'page')
        style_heading2 = odf_create_style('paragraph',
                                          name='Heading 2',
                                          parent='Standard',
                                          font='Verdana',
                                          size='16pt',
                                          style='italic')
        style_heading3 = odf_create_style('paragraph',
                                          name='Heading 3',
                                          parent='Standard',
                                          font='Verdana',
                                          size='14pt')
        style_tab_title = odf_create_style('table-cell',
                                           name='StyleCellTitre',
                                           display_name='StyleCellTitre',
                                           area='text',
                                           weight='bold',
                                           size='13pt')

            ## BODY - table
        # table
        table = odf_create_table(u"Table", width=2, height=19)
        self.doc_body.append(table)

        # title
        row = odf_create_row()
        row.set_value(0, "Metadata of %s" % dico_layer.get('title'))
##        row.set_style(style_tab_title)
        table.set_row(0, row)
        table.set_span((0, 0, 1, 0))

        # file name
        row = odf_create_row()
        row.set_values((dico_text.get('nomfic'), dico_layer.get(u'name')), 0)
        table.set_row(1, row)

        # thematic keywords
        row = odf_create_row()
        row.set_values((dico_text.get('mtcthem'), ', '.join(dico_profil.get(u'keywords'))), 0)
        table.set_row(2, row)

        # places keywords
        row = odf_create_row()
        row.set_values((dico_text.get('mtcgeo'), ', '.join(dico_profil.get(u'geokeywords'))), 0)
        table.set_row(3, row)

        # description
        row = odf_create_row()
        row.set_values((dico_text.get('description'), ''), 0)
        table.set_row(4, row)

        # context/summary keywords
        row = odf_create_row()
        row.set_values((dico_text.get('cadre'), dico_profil.get('description')), 0)
        table.set_row(5, row)

        # objects count
        row = odf_create_row()
        row.set_values((dico_text.get('num_objets'), dico_layer.get('num_obj')), 0)
        table.set_row(6, row)

        # fields count
        row = odf_create_row()
        row.set_values((dico_text.get('num_attrib'), dico_layer.get('num_fields')), 0)
        table.set_row(7, row)

        # creation date on computer
        row = odf_create_row()
        row.set_values((dico_text.get('date_crea'), dico_layer.get('date_crea')), 0)
        table.set_row(8, row)

        # last update
        row = odf_create_row()
        row.set_values((dico_text.get('date_actu'), dico_layer.get('date_actu')), 0)
        table.set_row(9, row)

        # sources
        row = odf_create_row()
        row.set_values((dico_text.get('source'), dico_profil.get('sources')), 0)
        table.set_row(10, row)

        # global responsable
        row = odf_create_row()
        row.set_values((dico_text.get('responsable'),dico_profil.get('resp_name') \
                          + u' ('   + dico_profil.get('resp_orga') \
                          + u'), '  + dico_profil.get('resp_mail')), 0)
        table.set_row(11, row)

        # point of contact
        row = odf_create_row()
        row.set_values((dico_text.get('ptcontact'), dico_profil.get('cont_name') \
                          + u' ('   + dico_profil.get('cont_orga') \
                          + u'), '  + dico_profil.get('cont_mail')), 0)
        table.set_row(12, row)

        # URL
        row = odf_create_row()
##        url = odf_create_link(url = dico_profil.get('url'),
##                              name = dico_profil.get('url_label'))
##        row.set_values((dico_text.get('siteweb'), url), 0)
        row.set_values((dico_text.get('siteweb'), '<a href="' +\
                          dico_profil.get('url') +\
                          u'" target="_blank">' +\
                          dico_profil.get('url_label') + u'</a>'), 0)
        table.set_row(13, row)

        # geometry type
        row = odf_create_row()
        row.set_values((dico_text.get('geometrie'), dico_layer.get('type_geom')), 0)
        table.set_row(14, row)

        # scale
        row = odf_create_row()
        row.set_values((dico_text.get('echelle'), "1:"), 0)
        table.set_row(15, row)

        # precision
        row = odf_create_row()
        row.set_values((dico_text.get('precision'), "  m"), 0)
        table.set_row(16, row)

        # SRS
        row = odf_create_row()
        srs_text = 'Projection : %s\n%s%s' % (dico_layer.get('srs'), dico_text.get('codepsg'), dico_layer.get('EPSG'))
        row.set_values((dico_text.get('srs'), srs_text), 0)
        table.set_row(17, row)

        # spatial extension
        row = odf_create_row()
        spatial_extent = "\tMax Y : %s\nMin X : %s\t\tMax X : %s\n\tMin Y : %s" % (dico_layer[u'Ymax'],\
                                                                                 dico_layer[u'Xmin'],\
                                                                                 dico_layer[u'Xmax'],\
                                                                                 dico_layer[u'Ymin'],)

        row.set_values((dico_text.get('emprise'), spatial_extent), 0)
        table.set_row(18, row)

            ## BODY - attributes
##        test = odf_create_heading(1, dico_text.get('listattributs'), suppress_numbering = True)
        list_fields = odf_create_paragraph(dico_text.get('listattributs'), style = style_heading1)
        self.doc_body.append(list_fields)





            ## END
        # saving the document
        output = path.join(dest, "metadator_" + dico_layer.get('name')[:-4] + ".odt")
        doc_obj.save(target=output, pretty=True)




################################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    """ """
