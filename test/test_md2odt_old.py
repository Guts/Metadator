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
import operator

# 3rd party library
from odf import text
from odf.opendocument import OpenDocumentText, load
from odf.style import Style, TextProperties, ParagraphProperties, TableColumnProperties
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell

################################################################################
############# Classes #############
###################################

class Document_Generic(object):
    """Example of document"""
    def __init__(self):
        self.document = OpenDocumentText()
        self.defineStyles()

    def defineStyles(self):
        """  """
        pass

    def addParagraphStyle(self, id, name, paragraph_properties={}, text_properties={}):
        """  """
        style = Style(name=name, family="paragraph")
        if len(paragraph_properties) > 0:
            style.addElement(ParagraphProperties(**paragraph_properties))
        if len(text_properties) > 0:
            style.addElement(TextProperties(**text_properties))
        setattr(self, id, style)
        self.document.styles.addElement(style)

    def addTableColumnStyle(self, id, name, properties={}):
        """  """
        style = Style(name=name, family="table-column")
        style.addElement(TableColumnProperties(**properties))
        setattr(self, id, style)
        self.document.automaticstyles.addElement(style)

    def addParagraph(self, text, stylename):
        """  """
        stylename = getattr(self, stylename, None)
        p = P(stylename=stylename, text=text)
        self.document.text.addElement(p)

    def addTable(self, content, cell_style, column_styles=[]):
        """  """
        cell_style = getattr(self, cell_style, None)
        table = Table()
        for style in column_styles:
            if "stylename" in style.keys():
                style["stylename"] = getattr(self, style["stylename"], None)
                table.addElement(TableColumn(**style))
        for row in content:
            tr = TableRow()
            table.addElement(tr)
            for cell in row:
                tc = TableCell()
                tr.addElement(tc)
                p = P(stylename=cell_style,text=cell)
                tc.addElement(p)
        self.document.text.addElement(table)

    def save(self, filename):
        """  """
        self.document.save(filename)



class Document_Template(Document_Generic):
    """Example of document"""
    def defineStyles(self):
        """ """
        self.addParagraphStyle("heading1", "Heading 1",
                               paragraph_properties={"breakbefore" : "true", "lineheight" : "24pt"},
                               text_properties={"fontfamily" : "Verdana", "fontweight" : "bold", "fontsize" : "20pt"}
                               )

        self.addParagraphStyle("heading2", "Heading 2",
                               paragraph_properties={"breakbefore" : "false", "lineheight" : "24pt"},
                               text_properties={"fontfamily" : "Verdana", "fontweight" : "italic", "fontsize" : "16pt"}
                               )

        self.addParagraphStyle("heading3", "Heading 3",
                               paragraph_properties={"breakbefore" : "false", "lineheight" : "24pt"},
                               text_properties={"fontfamily" : "Verdana", "fontsize" : "14pt"}
                               )

        self.addParagraphStyle("tablecontents", "Table Contents",
                               paragraph_properties={"numberlines" : "false", "linenumber" : "0"}
                               )

        self.addTableColumnStyle("column1", "Left Column",
                                 properties={"columnwidth" : "3cm"}
                                 )

        self.addTableColumnStyle("column2", "Right Column",
                                 properties={"columnwidth" : "7.5cm"}
                                 )

################################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    """ """
    # test data
    datas = {
            "Nouvelle-Zelande" : "93.19",
            "Australie" : "87.45",
            "Afrique du Sud" : "86.44",
            "Angleterre" : "82.48",
            "Irlande" : "81.79",
            "France" : "81.66",
            "Ecosse" : "81.20",
            "Argentine" : "78.97",
            "Pays de Galles" : "77.04",
            "Fidji" : "74.05",
            }
    # formatting data
    table_content = [(k, v) for k, v in datas.items()]
    table_content.sort(key=operator.itemgetter(1), reverse=True)
    table_content = [(k+1, v[0], v[1]) for k, v in enumerate(table_content)]
    # test
    doc_new = Document_Template()
    doc_new.addParagraph("Metadata of ", "heading1")
    doc_new.addParagraph("Global information", "heading2")
    doc_new.addParagraph("Airports", "heading3")
    doc_new.addTable(table_content, "tablecontents",
                 [
                 {"numbercolumnsrepeated" : 1, "stylename" : "column1"},
                 {"numbercolumnsrepeated" : 2, "stylename" : "column2"}
                 ]
                 )
    # finalizing the document
    doc_new.save("../test/test_odfpy.odt")

    # opening an existing doc (previously created) and modifying it
    doc_in = load("../test/test_odfpy_2.odt")
    for paragraph in doc_in.getElementsByType(text.P):
        print paragraph
        print paragraph.getAttribute('id')
        if str(paragraph) == "France":
            print 'youpi'
            paragraph.addText('TTMETADATOR')
            paragraph = 'replaced'
    doc_in.save('test_odfpy_2.odt')