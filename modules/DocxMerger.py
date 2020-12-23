# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name :       Word Joiner
# Purpose :    Generate a Word file compiling all word files present in folder
#				and subfolders according to a prefix filter.
# Authors :    Julien Moura (https://github.com/Guts)
# Python :     2.7.x
# Encoding:    utf-8
# Created :    14/03/2013
# Updated :    16/07/2013
#
# Fork from https://github.com/Guts/WordFiles_Merger
#-------------------------------------------------------------------------------

################################################################################
######## Libraries import #########
###################################

# Standard library
from os import walk, path, listdir, getcwd

# 3rd party library
from win32com.client import *

################################################################################
############# Classes #############
###################################

class DocxMerger():
    """ object to merge various Word files """
    def __init__(self, input_folder, outname, prefix = '*'):
        u"""
        List all Microsoft Word documents and merge them in a unique file

        input_folder = folder where are the documents to get merged
        """
        # variables
        self.li_word_files = [] # list for word files paths

        # listing the compatible files in the input folders
        for files in listdir(input_folder):
            if files.endswith(".doc") or files.endswith(".docx") and files.startswith(prefix):
                self.li_word_files.append(path.abspath(path.join(input_folder, files)))
        self.li_word_files = tuple(self.li_word_files)
        # Merge all files
        self.merge_docs(self.li_word_files, input_folder, outname)

    def merge_docs(self, iterword, dest, output):
        u""" creates a new Word file (.doc/.docx) merging all others Word files
        contained into the iterable parameter (list or tuple) """
        # Initializing Word application
        #word = gencache.EnsureDispatch("Word.Application")
        word = Dispatch('Word.Application')
        word.Visible = False
        # Create the final document
        finaldoc = word.Documents.Add()
        rng = finaldoc.Range()
        # Title
        rng.Collapse(0)
        rng.InsertAfter('Metadator')
        try:
            rng.Style = 'Titre'
        except:
            rng.Style = 'Title'
        rng.Paragraphs.Add()
        # table of contents
        rng.Collapse(0)
        toc = finaldoc.TablesOfContents
        toc.Add(rng)
        toc1 = toc.Item(1)
        toc1.IncludePageNumbers = True
        toc1.RightAlignPageNumbers = True
        toc1.UseFields = True
        toc1.UseHeadingStyles = True
        del rng
        # Looping and merging
        for f in iterword:
            rng = finaldoc.Range()
            rng.Collapse(0)
            rng.InsertFile(f)
            rng.Collapse(0)
            rng.InsertBreak()
            del rng
        # Page numbers
        sec = finaldoc.Sections.Item(1)
        bdp = sec.Footers.Item(1)
        bdp.PageNumbers.Add()
        toc1.Update()
        # saving
        finaldoc.SaveAs(path.abspath(path.join(dest, output + '.doc')), FileFormat=0)
        # Trying to convert into newer version of Office
        try:
            """ Office newer than 2003 is installed """
            finaldoc.Convert()
        except:
            """ Just Office 2003 """
            None
        # clean up
        finaldoc.Close()
        word.Quit()
        # end of function
        return finaldoc

################################################################################
##### Stand alone execution #######
###################################
if __name__ == '__main__':
    """  stand-alone execution"""
    # imports needed
    from os import chdir
    from sys import platform, exit
    import random
    # Check if it's running on windows system
    if platform != 'win32':
        print(u"Sorry, it's only working for Windows operating system!")
        exit()
    # moving in the main directory
    chdir('..//')
    # initiliazing the object
    if path.isdir(r'test/datatest/metadator'):
        DocxMerger(r'test/datatest/metadator', 'test_' + str(random.randint(0, 1000)),'metadator_')
    exit()
