# -*- coding: UTF-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julien Moura
#
# Created:     03/04/2013
# Copyright:   (c) Utilisateur 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

###################################
##### Libraries importation #######
###################################

# standard library
from Tkinter import Tk, Toplevel, Label, Button, LabelFrame     # GUI modules
from Tkinter import PhotoImage, Checkbutton, Entry, StringVar
from Tkinter import IntVar, N, NW, W, E, S, RIDGE, HORIZONTAL, VERTICAL
from tkFileDialog import askopenfilename, askdirectory
from tkMessageBox import showerror
from ttk import Combobox, Progressbar

from os import mkdir, path, listdir, walk, environ as env
from glob import glob

# external library
from lxml import etree as ET


###################################
####### Classes definition ########
###################################

################################################################################
class FrGlobal(LabelFrame):
    def __init__(self, title, txt):
        LabelFrame.__init__(self, text=title)
        Label(self, text = txt.get('bonjour')
                    + env.get(u'USERNAME')).grid(row = 0, column = 0,
                                                 columnspan = 2, sticky = N+S+W+E,
                                                 padx = 2, pady = 1)
        self.numfiles = StringVar(self, 'Number of shapes and MapInfo tables')
        Label(self, textvariable = self.numfiles).grid(row = 3,
                                                      column = 1,
                                                      columnspan = 3)
        # target folder
        self.labtarg = Label(self, text = u'Target folder: ')
        self.target = Entry(self, width = 35)
        self.browsetarg = Button(self,
                                 text = 'Browse',
                                 command = self.setpathtarg)

        # widgets placement
        self.labtarg.grid(row = 2, column = 1, columnspan = 1)
        self.target.grid(row = 2, column = 2, columnspan = 1)
        self.browsetarg.grid(row = 2, column = 3, columnspan = 1)

    def setpathtarg(self):
        """ ...browse and insert the path of target folder """
        self.foldername = askdirectory(parent = self,
                                     title = 'Select the destination folder')
        if self.foldername:
            try:
                self.target.insert(0, self.foldername)
            except:
                print 'no folder indicated'
        # calculate number of shapefiles and MapInfo files
        self.master.nbshp.set(len(self.ligeofiles(self.foldername)[0]))
        self.master.nbtab.set(len(self.ligeofiles(self.foldername)[1]))
        self.numfiles.set(self.master.nbshp.get() + ' shapefiles and ' + self.master.nbtab.get() + ' MapInfo tables')
        # end of function
        return self.foldername

    def ligeofiles(self, foldertarget):
        u""" List shapefiles and MapInfo files (.tab, not .mid/mif) contained
        in the folders structure """
        # Lists objects
        self.lishp = [] # for shapefiles
        self.litab = [] # for MapInfo tables
        # Looping in folders structure
        for root, dirs, files in walk(foldertarget):
            for i in files:
                # Looping on files contained
                if path.splitext(path.join(root, i))[1] == u'.shp' and \
                   path.isfile(path.join(root, i)[:-4] + u'.dbf') and \
                   path.isfile(path.join(root, i)[:-4] + u'.shx') and \
                   path.isfile(path.join(root, i)[:-4] + u'.prj'):
                    # add complete path of shapefile
                    self.lishp.append(path.join(root, i))
                elif path.splitext(path.join(root, i))[1] == u'.tab' and \
                   path.isfile(path.join(root, i)[:-4] + u'.dat') and \
                   path.isfile(path.join(root, i)[:-4] + u'.map') and \
                   path.isfile(path.join(root, i)[:-4] + u'.id'):
                    # add complete path of MapInfo file
                    self.litab.append(path.join(root, i))
        # Lists ordering and tupling
        self.lishp.sort()
        self.lishp = tuple(self.lishp)
        self.litab.sort()
        self.litab = tuple(self.litab)
        # End of function
        return self.lishp, self.litab


################################################################################
class FrOptions(LabelFrame):
    def __init__(self, title, txt, dicoprofils):
        LabelFrame.__init__(self, text=title)
        self.listing_profils(dicoprofils)

        # Dropdowm list of available profiles
        self.ddprofils = Combobox(self,
                                  values = dicoprofils.keys(),
                                  width = 35,
                                  height = len(dicoprofils.keys())*20)
        self.ddprofils.current(1)   # set the dropdown list to first element

        # export options
        caz_doc = Checkbutton(self, text = u'HTML / Word (.doc/.docx)',
                                    variable = self.master.opt_doc)
        caz_xls = Checkbutton(self, text = u'Excel 2003 (.xls)',
                                    variable = self.master.opt_xls)
        caz_xml = Checkbutton(self, text = u'XML (ISO 19139)',
                                    variable = self.master.opt_xml)

        # Basic buttons
        self.action = StringVar()
        self.action.set(txt.get('gui_choprofil'))
        self.val = Button(self, textvariable = self.action,
                                relief= 'raised',
                                command = self.bell)
        can = Button(self, text = 'Cancel (quit)',
                                relief= 'groove',
                                command = self.master.destroy)
        # Widgets placement
        self.ddprofils.bind('<<ComboboxSelected>>', self.alter_val)
        self.ddprofils.grid(row = 1, column = 0, columnspan = 3, sticky = N+S+W+E, padx = 2, pady = 5)
        caz_doc.grid(row = 2, column = 0, sticky = N+S+W, padx = 2, pady = 1)
        caz_xls.grid(row = 3, column = 0, sticky = N+S+W, padx = 2, pady = 1)
        caz_xml.grid(row = 4, column = 0, sticky = N+S+W, padx = 2, pady = 1)
        self.val.grid(row = 5, column = 0, columnspan = 2,
                            sticky = N+S+W+E, padx = 2, pady = 5)
        can.grid(row = 5, column = 2, sticky = N+S+W+E, padx = 2, pady = 5)

    def listing_profils(self, dictprofils):
        u""" List existing profilesin folder \data\profils """
        for i in glob(r'../data/profils/*.xml'):
            dictprofils[path.splitext(path.basename(i))[0]] = i
##        if new > 0:
##            listing_lang()
##            load_textes(deroul_lang.get())
##            deroul_profils.setlist(sorted(dico_profils.keys()))
##            fen_choix.update()
        # End of function
        return dictprofils

    def alter_val(self, inutile):
        u""" Switch the label of the validation button contained in basics class
        in the case that a new profile is going to be created"""
        if self.ddprofils.get() == self.master.blabla.get('gui_nouvprofil'):
            self.action.set(self.master.blabla.get('gui_crprofil'))
        else:
            self.action.set(self.master.blabla.get('gui_choprofil'))
        # End of functionFin de fonction
        return self.action

################################################################################
class FrProgres(LabelFrame):
    def __init__(self, title, txt):
        LabelFrame.__init__(self, text=title)
        # Bar of global progress
        Label(self, text = 'Global progress').grid(row=1, column = 0)
        self.proglob = Progressbar(self,
                                orient = HORIZONTAL,
                                max = 50,
                                length = 200,
                                mode = 'determinate')
        # Bar of attributes progress
        Label(self, text = 'Attributes progress').grid(row=3, column = 0)
        self.progatt = Progressbar(self,
                                orient = HORIZONTAL,
                                max = 50,
                                length = 200,
                                mode = 'determinate')

        # Widgets placement
        self.proglob.grid(row=2, column = 0,  sticky = N+S+W+E,
                          padx = 2, pady = 2)
        self.progatt.grid(row=4, column = 0,  sticky = N+S+W+E,
                          padx = 2, pady = 2)


################################################################################
class Metadator_GUI(Tk):
    """ Main class """
    def __init__(self):
        # basics settings
        Tk.__init__(self)               # constructor of parent graphic class
        ### Variables
        # GUI variables
        self.nbshp = StringVar()    # number of shapefiles
        self.nbtab = StringVar()    # number of MapInfo files
        self.opt_doc = IntVar()  # option activer/désactiver l'export au format word
        self.opt_xls = IntVar()  # option activer/désactiver l'export au format excel
        self.opt_xml = IntVar()  # option activer/désactiver l'export au format xml

        # Dictionaries
        self.lang = {}
        self.blabla = {}
        self.profils = {}      # dictionnaire des profils existants

        # Settings
        self.deflang = 'Français'
        self.defcodlang = 'FR'
        self.defrep = './'
        self.defdoc = 1
        self.defxls = 0
        self.defxml = 0
        self.opt_doc.set(self.defdoc)    # activated by default
        self.opt_xls.set(self.defxls)
        self.opt_xml.set(self.defxml)

        # Load needed data
        self.load_settings()
        self.listing_lang()
        self.load_texts(self.defcodlang)
        self.profils[self.blabla.get('gui_nouvprofil')] = ""

        # Main frame basic settings
        self.focus_force()              # put the window on foreground
        self.resizable(width = True,      # freeze dimensions
                       height = False)
        self.iconbitmap('../data/images/metadator.ico')     # icon
        self.title(self.blabla.get('gui_titre'))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Frames
        FrGlobal('Global', self.blabla).grid(row = 1, column = 0,
                                             sticky = N+S+W+E, padx = 2, pady = 2)
        FrOptions('Settings', self.blabla, self.profils).grid(row = 2, column = 0,
                                             sticky = N+S+W+E, padx = 2, pady = 2)
        FrProgres('Progression', self.blabla).grid(row = 3, column = 0,
                                             sticky = N+S+W+E, padx = 2, pady = 2)

    def listing_lang(self):
        u""" List available languages  in folder 'locale' """
        self.lang.clear()   # reset the dictionary
        # Looping in language folders
        for lgfolders in listdir(r'../locale'):
            self.lang[lgfolders[:2]] = lgfolders[3:].decode('Latin1'), lgfolders
        # End of function
        return self.lang

    def load_settings(self):
        u""" Load the last settings used """
        # open xml cursor
        xml = ET.parse(r'../data/xml/parametadator.xml')
        # looping and  gathering default settings
        for elem in xml.getroot().getiterator():
            if elem.tag == 'langue':            # language name
                self.deflang = elem.text
                continue
            elif elem.tag == 'codelang':        # language code
                self.defcodlang = elem.text
                continue
            elif elem.tag == 'rep_defaut':      # default folder
                self.defrep = elem.text
                continue
            elif elem.tag == 'exp_word':        # export to Word
                self.defdoc = elem.text
                continue
            elif elem.tag == 'exp_xls':         # export to Excel
                self.defxls = elem.text
                continue
            elif elem.tag == 'exp_xml':         # export to xml
                self.defxml = elem.text
                continue

        # End of function
        return self.defcodlang, self.defdoc, self.deflang, self.defrep,\
               self.defxls, self.defxml

    def load_texts(self, lang='FR'):
        u""" Load texts according to the selected language """
        # open xml cursor
        xml = ET.parse('../locale/' + lang + r'/lang_' + lang + '.xml')
        # Looping and gathering texts from the xml file
        for elem in xml.getroot().getiterator():
            self.blabla[elem.tag] = elem.text
        # Fin de fonction
        return self.blabla

###################################
### Main program initialization ###
###################################

if __name__ == '__main__':
    app = Metadator_GUI()
    app.mainloop()
