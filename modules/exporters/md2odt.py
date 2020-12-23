# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-----------------------------------------------------------------------------
# Name:         Metadata to ODT
# Purpose:      Export Metadata dictionnary into a ODF document (.odt).
# Python:       2.7.x
# Author:       Julien Moura (https://github.com/Guts)
# Created:      13/10/2013
# Updated:      11/02/2014
# credits:      inspired by the code snippets included in Linux Magazine HS 53
#-----------------------------------------------------------------------------

##############################################################################
######## Libraries import #########
###################################

# Standard library
from datetime import date
from os import path

# 3rd party library
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties,\
                    ParagraphProperties, ListLevelProperties,\
                    FontFace, TableCellProperties
from odf.text import P, H, A, List, ListItem, ListStyle, \
                    ListLevelStyleBullet, ListLevelStyleNumber,\
                    Span
from odf.text import Section
from odf.table import Table, TableColumn, TableRow, TableCell

###############################################################################
############# Classes #############
###################################


class ExportToODT():
    """ object to export metadata dictionary to html """
    def __init__(self, dest, dico_layer, dico_fields, dico_profil,
                 dico_rekurs, dico_text):
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
        doc_obj = OpenDocumentText()            # create a new document object

        # BASIC STYLES
        doc_styles = doc_obj.styles
            # styles settings
        StandardStyle = Style(name="Standard",
                              family="paragraph")
        TextBodyStyle = Style(name="Text_20_body",
                              family="paragraph",
                              parentstylename='Standard',
                              displayname="Text body")
        TextBodyStyle.addElement(ParagraphProperties(margintop="0in",
                                                     marginbottom="0.0835in"))

            # adding the styles
        doc_styles.addElement(StandardStyle)
        doc_styles.addElement(TextBodyStyle)

            # fonts
        doc_obj.fontfacedecls.addElement((FontFace(name="Arial",
                                                   fontfamily="Arial",
                                                   fontfamilygeneric="swiss",
                                                   fontpitch="variable")))
        # AUTOMATIC STYLES
            # 1st type of paragraph (P1)
        P1_style = Style(name="P1",
                        family="paragraph",
                        parentstylename="Standard",
                        liststylename="L1")
        doc_obj.automaticstyles.addElement(P1_style)
            # 2nd type of paragraph (P2)
        P2_style = Style(name="P2",
                        family="paragraph",
                        liststylename="L2")
        P2_style.addElement(TextProperties(fontweight="bold",
                                           fontweightasian="bold",
                                           fontweightcomplex="bold"))
        doc_obj.automaticstyles.addElement(P2_style)
            # List 1 (unordered)
        L1_style = ListStyle(name="L1")
        L1_bullet = ListLevelStyleBullet(level="1",
                                       stylename="Numbering_20_Symbols",
                                       numsuffix=".",
                                       bulletchar=u'\u2022') # bullet char (utf8)
        L1_prop = ListLevelProperties(spacebefore="0.25in",
                                      minlabelwidth="0.25in")
        L1_bullet.addElement(L1_prop)
        L1_style.addElement(L1_bullet)
        # adding the style
        doc_obj.automaticstyles.addElement(L1_style)
            # List 2 (ordered)
        L2_style = ListStyle(name="L2")
        L2_num = ListLevelStyleNumber(level="1",
                                         stylename="Numbering_20_Symbols",
                                         numsuffix=" - ",
                                         numformat='1')
        L2_prop = ListLevelProperties(spacebefore="0.25in",
                                      minlabelwidth="0.25in")
        L2_num.addElement(L2_prop)
        L2_style.addElement(L2_num)
        # adding the style
        doc_obj.automaticstyles.addElement(L2_style)

        # Text 5: bold
        T5_style = Style(name="T5", family="text")
        T5_style.addElement(TextProperties(color="#ff0000",fontname="Arial"))
        doc_obj.automaticstyles.addElement(T5_style)

        # Text 2: bold
        T2_style = Style(name="T2", family="text")
        T2_style.addElement(TextProperties(fontweight="bold",
                                          fontweightasian="bold",
                                          fontweightcomplex="bold"))
        doc_obj.automaticstyles.addElement(T2_style)

        # Table : cell formatting
        TAB_style = Style(name="Table", family="table-cell", parentstylename="Standard")
        TAB_style.addElement(TableCellProperties(border="0.05pt solid #000000"))
        doc_obj.automaticstyles.addElement(TAB_style)

                # BODY - table
            # table creation
        doc_table = Table(name="Metadata")
        doc_table.addElement(TableColumn(numbercolumnsrepeated="2"))

            # title
        tr_title = TableRow()
        doc_table.addElement(tr_title)
            # merged columns
        tc_1_title = TableCell(valuetype="string", stylename="Table", numbercolumnsspanned="2")
        tc_1_title.addElement(P(text = "Metadata of %s" % dico_layer.get('title'), stylename='P1'))
        tr_title.addElement(tc_1_title)

            # file name
        tr_name = TableRow()
        doc_table.addElement(tr_name)
        # column 1
        tc_1_name = TableCell(valuetype="string", stylename="Table")
        tc_1_name.addElement(P(text = dico_text.get('nomfic'), stylename='P2'))
        tr_name.addElement(tc_1_name)
        # column 2
        tc_2_name = TableCell(valuetype="string", stylename="Table")
        tc_2_name.addElement(P(text = dico_layer.get(u'name')))
        tr_name.addElement(tc_2_name)

            # thematic keywords
        tr_themes = TableRow()
        doc_table.addElement(tr_themes)
        # column 1
        tc_1_themes = TableCell(valuetype="string", stylename="Table")
        tc_1_themes.addElement(P(text = dico_text.get('mtcthem'), stylename='P2'))
        tr_themes.addElement(tc_1_themes)
        # column 2
        tc_2_themes = TableCell(valuetype="string", stylename="Table")
        tc_2_themes.addElement(P(text = ', '.join(dico_profil.get(u'keywords'))))
        tr_themes.addElement(tc_2_themes)

            # places keywords
        tr_places = TableRow()
        doc_table.addElement(tr_places)
        # column 1
        tc_1_places = TableCell(valuetype="string", stylename="Table")
        tc_1_places.addElement(P(text = dico_text.get('mtcgeo'), stylename='P2'))
        tr_places.addElement(tc_1_places)
        # column 2
        tc_2_places = TableCell(valuetype="string", stylename="Table")
        tc_2_places.addElement(P(text = ', '.join(dico_profil.get(u'geokeywords'))))
        tr_places.addElement(tc_2_places)

            # description
        tr_description = TableRow()
        doc_table.addElement(tr_description)
        # column 1
        tc_1_description = TableCell(valuetype="string", stylename="Table")
        tc_1_description.addElement(P(text = dico_text.get('description'), stylename='P2'))
        tr_description.addElement(tc_1_description)
        # column 2
        tc_2_description = TableCell(valuetype="string", stylename="Table")
        tc_2_description.addElement(P(text = ''))
        tr_description.addElement(tc_2_description)

            # context/summary
        tr_summary = TableRow()
        doc_table.addElement(tr_summary)
        # column 1
        tc_1_summary = TableCell(valuetype="string", stylename="Table")
        tc_1_summary.addElement(P(text = dico_text.get('cadre'), stylename='P2'))
        tr_summary.addElement(tc_1_summary)
        # column 2
        tc_2_summary = TableCell(valuetype="string", stylename="Table")
        tc_2_summary.addElement(P(text = dico_profil.get('description')))
        tr_summary.addElement(tc_2_summary)

            # objects count
        tr_features = TableRow()
        doc_table.addElement(tr_features)
        # column 1
        tc_1_features = TableCell(valuetype="string", stylename="Table")
        tc_1_features.addElement(P(text = dico_text.get('num_objets'), stylename='P2'))
        tr_features.addElement(tc_1_features)
        # column 2
        tc_2_features = TableCell(valuetype="string", stylename="Table")
        tc_2_features.addElement(P(text = dico_layer.get('num_obj')))
        tr_features.addElement(tc_2_features)

            # fields count
        tr_fields = TableRow()
        doc_table.addElement(tr_fields)
        # column 1
        tc_1_fields = TableCell(valuetype="string", stylename="Table")
        tc_1_fields.addElement(P(text = dico_text.get('num_attrib'), stylename='P2'))
        tr_fields.addElement(tc_1_fields)
        # column 2
        tc_2_fields = TableCell(valuetype="string", stylename="Table")
        tc_2_fields.addElement(P(text = dico_layer.get('num_fields')))
        tr_fields.addElement(tc_2_fields)

            # creation date (on computer)
        tr_date_crea = TableRow()
        doc_table.addElement(tr_date_crea)
        # column 1
        tc_1_date_crea = TableCell(valuetype="string", stylename="Table")
        tc_1_date_crea.addElement(P(text = dico_text.get('date_crea'), stylename='P2'))
        tr_date_crea.addElement(tc_1_date_crea)
        # column 2
        tc_2_date_crea = TableCell(valuetype="string", stylename="Table")
        tc_2_date_crea.addElement(P(text = dico_layer.get('date_crea')))
        tr_date_crea.addElement(tc_2_date_crea)

            # last update
        tr_date_up = TableRow()
        doc_table.addElement(tr_date_up)
        # column 1
        tc_1_date_up = TableCell(valuetype="string", stylename="Table")
        tc_1_date_up.addElement(P(text = dico_text.get('date_actu'), stylename='P2'))
        tr_date_up.addElement(tc_1_date_up)
        # column 2
        tc_2_date_up = TableCell(valuetype="string", stylename="Table")
        tc_2_date_up.addElement(P(text = dico_layer.get('date_actu')))
        tr_date_up.addElement(tc_2_date_up)

            # sources
        tr_sources = TableRow()
        doc_table.addElement(tr_sources)
        # column 1
        tc_1_sources = TableCell(valuetype="string", stylename="Table")
        tc_1_sources.addElement(P(text = dico_text.get('source'), stylename='P2'))
        tr_sources.addElement(tc_1_sources)
        # column 2
        tc_2_sources = TableCell(valuetype="string", stylename="Table")
        tc_2_sources.addElement(P(text = dico_profil.get('sources')))
        tr_sources.addElement(tc_2_sources)

            # global responsable
        tr_resp = TableRow()
        doc_table.addElement(tr_resp)
        # column 1
        tc_1_resp = TableCell(valuetype="string", stylename="Table")
        tc_1_resp.addElement(P(text = dico_text.get('responsable'), stylename='P2'))
        tr_resp.addElement(tc_1_resp)
        # column 2
        tc_2_resp = TableCell(valuetype="string", stylename="Table")
        tc_2_resp.addElement(P(text = dico_profil.get('resp_name') \
                                    + u' ('   + dico_profil.get('resp_orga') \
                                    + u'), '  + dico_profil.get('resp_mail')))
        tr_resp.addElement(tc_2_resp)

            # point of contact
        tr_cont = TableRow()
        doc_table.addElement(tr_cont)
        # column 1
        tc_1_cont = TableCell(valuetype="string", stylename="Table")
        tc_1_cont.addElement(P(text = dico_text.get('ptcontact'), stylename='P2'))
        tr_cont.addElement(tc_1_cont)
        # column 2
        tc_2_cont = TableCell(valuetype="string", stylename="Table")
        tc_2_cont.addElement(P(text = dico_profil.get('cont_name') \
                                    + u' ('   + dico_profil.get('cont_orga') \
                                    + u'), '  + dico_profil.get('cont_mail')))
        tr_cont.addElement(tc_2_cont)

            # URL
        tr_url = TableRow()
        doc_table.addElement(tr_url)
        # column 1
        tc_1_url = TableCell(valuetype="string", stylename="Table")
        tc_1_url.addElement(P(text = dico_text.get('siteweb'), stylename='P2'))
        tr_url.addElement(tc_1_url)
        # column 2
        tc_2_url = TableCell(valuetype="string", stylename="Table")
        urlink = A(type="simple", href=dico_profil.get('url'), text=dico_profil.get('url_label'))
        plink = P(text="")
        plink.addElement(urlink)
        tc_2_url.addElement(plink)
        tr_url.addElement(tc_2_url)

            # geometry type
        tr_geom=TableRow()
        doc_table.addElement(tr_geom)
        # column 1
        tc_1_geom = TableCell(valuetype="string", stylename="Table")
        tc_1_geom.addElement(P(text=dico_text.get('geometrie'), stylename='P2'))
        tr_geom.addElement(tc_1_geom)
        # column 2
        tc_2_geom = TableCell(valuetype="string", stylename="Table")
        tc_2_geom.addElement(P(text=dico_layer.get('type_geom')))
        tr_geom.addElement(tc_2_geom)

            # scale
        tr_scale=TableRow()
        doc_table.addElement(tr_scale)
        # column 1
        tc_1_scale=TableCell(valuetype="string", stylename="Table")
        tc_1_scale.addElement(P(text = dico_text.get('echelle'), stylename='P2'))
        tr_scale.addElement(tc_1_scale)
        # column 2
        tc_2_sources = TableCell(valuetype="string", stylename="Table")
        tc_2_sources.addElement(P(text = "1:"))
        tr_scale.addElement(tc_2_sources)

            # precision
        tr_prec = TableRow()
        doc_table.addElement(tr_prec)
        # column 1
        tc_1_prec = TableCell(valuetype="string", stylename="Table")
        tc_1_prec.addElement(P(text = dico_text.get('precision'), stylename='P2'))
        tr_prec.addElement(tc_1_prec)
        # column 2
        tc_2_prec = TableCell(valuetype="string", stylename="Table")
        tc_2_prec.addElement(P(text = " m"))
        tr_prec.addElement(tc_2_prec)

            # SRS
        tr_srs = TableRow()
        doc_table.addElement(tr_srs)
        # column 1
        tc_1_srs = TableCell(valuetype="string", stylename="Table")
        tc_1_srs.addElement(P(text = dico_text.get('srs'), stylename='P2'))
        tr_srs.addElement(tc_1_srs)
        # column 2
        tc_2_srs = TableCell(valuetype="string", stylename="Table")
        srs_text = 'SRS : %s\u000A%s%s' % (dico_layer.get('srs'), dico_text.get('codepsg'), dico_layer.get('EPSG'))
        tc_2_srs.addElement(P(text = srs_text))
        tr_srs.addElement(tc_2_srs)

            # spatial extension
        tr_extent = TableRow()
        doc_table.addElement(tr_extent)
        # column 1
        tc_1_extent = TableCell(valuetype="string", stylename="Table")
        tc_1_extent.addElement(P(text = dico_text.get('emprise'), stylename='P2'))
        tr_extent.addElement(tc_1_extent)
        # column 2
        tc_2_extent = TableCell(valuetype="string", stylename="Table")
        spatial_extent = "\tMax Y : %s \tMin X : %s\t\tMax X : %s\tMin Y : %s" % (dico_layer[u'Ymax'],\
                                                                                   dico_layer[u'Xmin'],\
                                                                                   dico_layer[u'Xmax'],\
                                                                                   dico_layer[u'Ymin'],)
        tc_2_extent.addElement(P(text = spatial_extent))
        tr_extent.addElement(tc_2_extent)

        # adding the table
        doc_obj.text.addElement(doc_table)

            ## BODY - attributes
        doc_obj.text.addElement(Section(name="Attributes"))
        doc_obj.text.addElement(H(outlinelevel=1,
                                  text=dico_text.get('listattributs')))
        x = 0    # rank of the field
        for chp in dico_fields.keys():
            u""" parsing fields"""
            x = x + 1
            # field name
            try:
                u""" check the encoding of the field name """
                p_name = P(text=str(x) + ' - ' + chp, stylename='P2')
            except UnicodeDecodeError:
                u""" raise the exception and re-encode it """
                p_name = P(text=str(x) + ' - ' + chp.decode('latin1'),
                           stylename='T2')
            doc_obj.text.addElement(p_name)

            # more friendly local variables
            lg = dico_fields.get(chp)[0][1]
            prec = dico_fields.get(chp)[0][2]
            desc = dico_fields.get(chp)[1]

            # field information depending on field type
            if dico_fields[chp][0][0] == 'Integer':
                u""" for integers """
                # type
                p_type = P(text='')
                s_type = Span(text=dico_text.get('type'), stylename='T2')
                p_type.addElement(s_type)
                p_type.addText(" %s" % dico_text.get('entier'))
                doc_obj.text.addElement(p_type)

                # length
                p_lg = P(text='')
                s_lg = Span(text=dico_text.get('longueur'), stylename='T2')
                p_lg.addElement(s_lg)
                p_lg.addText(" %s" % lg)
                doc_obj.text.addElement(p_lg)

                # description
                p_descr = P(text='')
                s_descr = Span(text=dico_text.get('description'), stylename='T2')
                p_descr.addElement(s_descr)
                p_descr.addText(" %s" % desc)
                doc_obj.text.addElement(p_descr)

                # basics stats only if there are'nt disabled
                if dico_fields[chp][2]:
                    # more friendly local variables
                    som = dico_fields[chp][2][0]
                    med = dico_fields[chp][2][1]
                    moy = dico_fields[chp][2][2]
                    uppest = dico_fields[chp][2][3]
                    bottom = dico_fields[chp][2][4]
                    freq = dico_fields[chp][2][5]
                    mod = dico_fields[chp][2][6]
                    ect = dico_fields[chp][2][7]
                    vid = dico_fields[chp][2][8]

                    # basics stats
                    p_stats = P(text='')
                    s_stats = Span(text=dico_text.get('statsbase'),
                                   stylename='T2')
                    p_stats.addElement(s_stats)
                    doc_obj.text.addElement(p_stats)
                    stats_list = List(stylename="L5")
                    item = ListItem()
                    item.addElement(P(text='%s (%s)' % (dico_text.get('somme'), som),
                                      stylename="P1"))
                    stats_list.addElement(item)
                    if vid != 0:    # for null values
                        perc = round(float(vid)*100/dico_layer.get(u'num_obj'), 2)
                        item = ListItem()
                        item.addElement(P(text='%s%s (%s %s%s)' % (dico_text.get('valnulles'), vid,
                                                                   dico_text.get('soit'),
                                                                   perc, dico_text.get('perctotal')), stylename="P1"))
                        stats_list.addElement(item)
                    item = ListItem()
                    item.addElement(P(text='%s%s' % (dico_text.get('min'), bottom), stylename="P1"))
                    stats_list.addElement(item)
                    item = ListItem()
                    item.addElement(P(text='%s%s' % (dico_text.get('max'), uppest), stylename="P1"))
                    stats_list.addElement(item)
                    item = ListItem()
                    item.addElement(P(text='%s%s' % (dico_text.get('moyenne'), moy), stylename="P1"))
                    stats_list.addElement(item)
                    item = ListItem()
                    item.addElement(P(text='%s%s' % (dico_text.get('mediane'), med), stylename="P1"))
                    stats_list.addElement(item)
                    item = ListItem()
                    item.addElement(P(text='%s%s' % (dico_text.get('ecartype'), ect), stylename="P1"))
                    stats_list.addElement(item)
                    doc_obj.text.addElement(stats_list)

                    # modalities
                    p_moda = P(text='')
                    s_moda = Span(text=dico_text.get('val_freq'), stylename='T2')
                    p_moda.addElement(s_moda)
                    p_moda.addText(" %s" % mod.replace(u'\n', u'<br>'))
                    doc_obj.text.addElement(p_moda)
                    if freq > 0:
                        freq_list = List(stylename="L5")
                        for val, okur in freq:
                            item = ListItem()
                            item.addElement(P(text='%s (%s)' % (val, okur), stylename="P1"))
                            freq_list.addElement(item)
                    else:
                        pass
                    doc_obj.text.addElement(freq_list)
                else:
                    pass

            elif dico_fields[chp][0][0] == u'Real':
                u""" for real / float """
                # type
                p_type = P(text='')
                s_type = Span(text=dico_text.get('type'), stylename='T2')
                p_type.addElement(s_type)
                p_type.addText(" %s" % dico_text.get('reel'))
                doc_obj.text.addElement(p_type)

                # length
                p_lg = P(text='')
                s_lg = Span(text=dico_text.get('longueur'), stylename='T2')
                p_lg.addElement(s_lg)
                p_lg.addText(" %s" % lg)
                doc_obj.text.addElement(p_lg)

                # precision
                p_prec = P(text='')
                s_prec = Span(text=dico_text.get('precision'), stylename='T2')
                p_prec.addElement(s_prec)
                p_prec.addText(" %s" % prec)
                doc_obj.text.addElement(p_prec)

                # description
                p_descr = P(text='')
                s_descr = Span(text=dico_text.get('description'), stylename='T2')
                p_descr.addElement(s_descr)
                p_descr.addText(" %s" % desc)
                doc_obj.text.addElement(p_descr)

                # basics stats only if there are'nt disabled
                if dico_fields[chp][2]:
                    # more friendly local variables
                    som = dico_fields[chp][2][0]
                    med = dico_fields[chp][2][1]
                    moy = dico_fields[chp][2][2]
                    uppest = dico_fields[chp][2][3]
                    bottom = dico_fields[chp][2][4]
                    freq = dico_fields[chp][2][5]
                    mod = dico_fields[chp][2][6]
                    ect = dico_fields[chp][2][7]
                    vid = dico_fields[chp][2][8]

                    # basics stats
                    p_stats = P(text='')
                    s_stats = Span(text=dico_text.get('statsbase'), stylename='T2')
                    p_stats.addElement(s_stats)
                    doc_obj.text.addElement(p_stats)
                    stats_list = List(stylename="L5")
                    item = ListItem()
                    item.addElement(P(text='%s (%s)' % (dico_text.get('somme'), som), stylename="P1"))
                    stats_list.addElement(item)
                    if vid != 0:    # for null values
                        perc = round(float(vid)*100/dico_layer.get(u'num_obj'), 2)
                        item = ListItem()
                        item.addElement(P(text='%s%s (%s %s%s)' % (dico_text.get('valnulles'), vid,
                                                                   dico_text.get('soit'),
                                                                   perc, dico_text.get('perctotal')), stylename="P1"))
                        stats_list.addElement(item)
                    item = ListItem()
                    item.addElement(P(text='%s%s' % (dico_text.get('min'), bottom), stylename="P1"))
                    stats_list.addElement(item)
                    item = ListItem()
                    item.addElement(P(text='%s%s' % (dico_text.get('max'), uppest), stylename="P1"))
                    stats_list.addElement(item)
                    item = ListItem()
                    item.addElement(P(text='%s%s' % (dico_text.get('moyenne'), moy), stylename="P1"))
                    stats_list.addElement(item)
                    item = ListItem()
                    item.addElement(P(text='%s%s' % (dico_text.get('mediane'), med), stylename="P1"))
                    stats_list.addElement(item)
                    item = ListItem()
                    item.addElement(P(text='%s%s' % (dico_text.get('ecartype'), ect), stylename="P1"))
                    stats_list.addElement(item)
                    doc_obj.text.addElement(stats_list)

                    # modalities
                    p_moda = P(text='')
                    s_moda = Span(text=dico_text.get('val_freq'), stylename='T2')
                    p_moda.addElement(s_moda)
                    p_moda.addText(" %s" % mod.replace(u'\n', u'<br>'))
                    doc_obj.text.addElement(p_moda)
                    if freq > 0:
                        freq_list = List(stylename="L5")
                        for val, okur in freq:
                            item = ListItem()
                            item.addElement(P(text='%s (%s)' % (val, okur), stylename="P1"))
                            freq_list.addElement(item)
                    else:
                        pass
                    doc_obj.text.addElement(freq_list)
                else:
                    pass

            elif dico_fields[chp][0][0] == 'String':
                u""" for caracter string """
                # type
                p_type = P(text='')
                s_type = Span(text=dico_text.get('type'), stylename='T2')
                p_type.addElement(s_type)
                p_type.addText(" %s" % dico_text.get('string'))
                doc_obj.text.addElement(p_type)

                # length
                p_lg = P(text='')
                s_lg = Span(text=dico_text.get('longueur'), stylename='T2')
                p_lg.addElement(s_lg)
                p_lg.addText(" %s" % lg)
                doc_obj.text.addElement(p_lg)

                # description
                p_descr = P(text='')
                s_descr = Span(text=dico_text.get('description'), stylename='T2')
                p_descr.addElement(s_descr)
                p_descr.addText(" %s" % desc)
                doc_obj.text.addElement(p_descr)

                # basics stats only if there are'nt disabled
                if dico_fields[chp][2]:
                    # more friendly local variables
                    mod = dico_fields[chp][2][0]
                    freq = dico_fields[chp][2][1]
                    vid = dico_fields[chp][2][2]

                    # modalities
                    p_moda = P(text='')
                    s_moda = Span(text=dico_text.get('txt_moda'), stylename='T2')
                    p_moda.addElement(s_moda)
                    p_moda.addText(" %s" % mod.replace(u'\n', u'<br>'))
                    doc_obj.text.addElement(p_moda)
                    if freq > 0:
                        freq_list = List(stylename="L5")
                        for val, okur in freq:
                            item = ListItem()
                            try:
                                item.addElement(P(text='%s (%s)' % (val, okur), stylename="P1"))
                            except UnicodeDecodeError:
                                val = val.decode('latin1')
                                item.addElement(P(text='%s (%s)' % (val, okur), stylename="P1"))
                            freq_list.addElement(item)
                        # if null values
                        if vid != 0:
                            item = ListItem()
                            item.addElement(P(text='%s (%s)' % (dico_text.get('valnulles'), vid), stylename="P1"))
                            freq_list.addElement(item)
                        else:
                            pass
                        doc_obj.text.addElement(freq_list)
                    else:
                        pass

            elif dico_fields[chp][0][0] == 'Date':
                u""" for dates """
                # type
                p_type = P(text='')
                s_type = Span(text=dico_text.get('type'), stylename='T2')
                p_type.addElement(s_type)
                p_type.addText(" %s" % dico_text.get('date'))
                doc_obj.text.addElement(p_type)

                # description
                p_descr = P(text='')
                s_descr = Span(text=dico_text.get('description'), stylename='T2')
                p_descr.addElement(s_descr)
                p_descr.addText(" %s" % desc)
                doc_obj.text.addElement(p_descr)

                # basics stats only if there are'nt disabled
                if dico_fields[chp][2]:
                    # more friendly local variables
                    uppest = dico_fields[chp][2][0]
                    bottom = dico_fields[chp][2][1]
                    diffdays = dico_fields[chp][2][2]
                    freq = dico_fields[chp][2][3]
                    mod = dico_fields[chp][2][4]
                    vid = dico_fields[chp][2][5]

                    # dates delta
                    if vid != dico_layer.get(u'num_obj'):
                        u""" check if attribute is empty """
                        # oldest
                        p_old = P(text='')
                        s_old = Span(text=dico_text.get('datancienne'), stylename='T2')
                        p_old.addElement(s_old)
                        p_old.addText(" %s" % date.isoformat(bottom))
                        doc_obj.text.addElement(p_old)

                        # recent
                        p_rec = P(text='')
                        s_rec = Span(text=dico_text.get('daterecente'), stylename='T2')
                        p_rec.addElement(s_rec)
                        p_rec.addText(" %s" % date.isoformat(uppest))
                        doc_obj.text.addElement(p_rec)

                        # interval
                        p_interv = P(text='')
                        s_interv = Span(text=dico_text.get('date_intervmax'), stylename='T2')
                        p_interv.addElement(s_interv)
                        p_interv.addText(" %s" % diffdays)
                        doc_obj.text.addElement(p_interv)

            # separating line
            doc_obj.text.addElement(P(text=u"______________________________________\n"))

            ## END
        # saving the document
        output = path.join(dest, "{0}_MD.odt".format(dico_layer.get('name')[:-4]))
        doc_obj.save(output)

##############################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    """ stand-alone execution """
    pass
