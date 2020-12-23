# -*- coding: UTF-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        Metadata to Word
# Purpose:     Export Metadata dictionnary into a Word (.doc/.docx) file.
# Python:      2.7.x
# Author:      Julien Moura
# Created:     07/04/2013
# update:      16/07/2013
#-------------------------------------------------------------------------------

################################################################################
######## Libraries import #########
###################################

# Standard library
from os import  path, rename
from time import strftime

# 3rd party library
from win32com.client import Dispatch


################################################################################
############# Classes #############
###################################

class ExportToDocX():
    def __init__(self, html_input, dest):
        u""" converts an html file to a Microsoft Word document.
        Rename the file if ir already exists in the destination folder.

        html_input = html file input to convert
        dest = the destination folder
        """
        # variables
        today = strftime("%Y-%m-%d")
        output = path.abspath(html_input[:-5] + '.doc')
        outputx = path.abspath(html_input[:-5] + '.docx')
        output_alt = path.abspath(html_input[:-5] + '_%s.doc' % today)
        # Word application initialization
        word = Dispatch('Word.Application')
        word.Visible = False
        # Creating new Word file object
        doc = word.Documents.Add()
        # Page numbers
        sec = doc.Sections.Item(1)
        bdp = sec.Footers.Item(1)
        bdp.PageNumbers.Add()
        # Place the insertion cursor
        rng = doc.Range()
        rng.Paragraphs.Add()
        rng.Collapse(1)
        # Inserting the html
        rng.InsertFile(html_input)
        # saving the document
        if not path.isfile(output) and not path.isfile(outputx):
            doc.SaveAs(output, FileFormat=0)
        else:
            doc.SaveAs(output_alt, FileFormat=0)
        # Trying to convert into newer version of Office
        try:
            doc.Convert()
        except:
            None
        # clean up
        doc.Close()
        word.Quit()


################################################################################
##### Stand alone execution #######
###################################
if __name__ == '__main__':
    # imports needed
    from os import  chdir, path
    # moving in the main directory
    chdir('..//')
    if path.isfile(r'test/datatest/shp/metadator/metadator_OSM_TrenElectrico.html'):
        ExportToDocX(path.abspath('test/datatest/metadator/metadator_OSM_TrenElectrico.html'),
                     'test/datatest/')

