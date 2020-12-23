# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
# ------------------------------------------------------------------------------
# Name:         Metadator
# Purpose:      Automatize the creation of metadata files from geographic data
#                   contained in a folders structures.
#                   It produces an Excel output file (.xls)
#
# Author:       Julien Moura (https://github.com/Guts/)
#
# Python:       2.7.x
# Created:      19/12/2011
# Updated:      20/02/2015
#
# Licence:      GPL 3
# -----------------------------------------------------------------------------

MetadatorVersion = "2.1.0"

###############################################################################
########### Libraries #############
###################################
# Standard library
from Tkinter import Tk, Text, StringVar, IntVar, END, Image     # GUI
from Tkinter import N, S, E, W, ACTIVE, DISABLED, PhotoImage, WORD, NORMAL, X
from tkFileDialog import askdirectory
from tkMessageBox import showinfo as info, askyesno
from ttk import Button, Checkbutton, Combobox, Entry, Frame
from ttk import Label, Labelframe, Progressbar, Notebook, Style
import tkFont

from sys import platform as opersys
from os import listdir, walk, path, mkdir   # files and folder managing
from os import environ as env, access, R_OK
import platform  # about operating systems
from time import strftime
from webbrowser import open_new

import ConfigParser         # to manipulate the options.ini file

import threading            # multi threads handling
import subprocess           # subprocesses

import logging      # log files
from logging.handlers import RotatingFileHandler

# Python 3 backported
from collections import OrderedDict as OD

# 3rd party libraries
try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import gdal
    import ogr
    import osr

gdal.AllRegister()
ogr.UseExceptions()
gdal.UseExceptions()

from xml.etree import ElementTree as ET

# Custom modules
from modules import Read_SHP
from modules import Read_TAB
from modules import StatsFields
from modules import ExportToHTML
from modules import ExportToODT
from modules import ExportToXML
from modules import ExportToXLS
from modules import NewProfile
from modules import InfoBulle

# Imports depending on operating system
if opersys == 'win32':
    u""" windows """
    from os import startfile            # to open a folder/file
    from modules import ExportToDocX
    from modules import DocxMerger
else:
    pass

###############################################################################
############ Classes ##############
###################################


class Metadator(Tk):
    def __init__(self):
        u"""
        Main window constructor
        Creates 1 frame and 2 labeled subframes
        """
        # first: the log
        # see: http://sametmax.com/ecrire-des-logs-en-python/
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)  # all errors will be get
        log_form = logging.Formatter('%(asctime)s || %(levelname)s || %(message)s')
        logfile = RotatingFileHandler('Metadator_LOG.log', 'a', 5000000, 1)
        logfile.setLevel(logging.DEBUG)
        logfile.setFormatter(log_form)
        self.logger.addHandler(logfile)
        self.logger.info('\n\t ======== Metadator ========')  # first messages
        self.logger.info('Starting the UI')

        # checking the path to GDAL in the path
        if "GDAL_DATA" not in env.keys():
            try:
                gdal.SetConfigOption(str('GDAL_DATA'),
                                     str(path.abspath(r'data/gdal')))
            except:
                print("Oups! Something has gone wrong...\
                      see: https://github.com/Guts/Metadator/issues/21")
        else:
            pass

        # basics settings
        Tk.__init__(self)           # constructor of parent graphic class
        self.title(u'Metadator {0}'.format(MetadatorVersion))
        self.style = Style()        # more friendly windows style
        if opersys == 'win32':
            self.logger.info('Op. system: {0}'.format(platform.platform()))
            self.iconbitmap('Metadator.ico')    # windows icon
            self.uzer = env.get(u'USERNAME')
        elif opersys == 'linux2':
            self.logger.info('Op. system: {0}'.format(platform.platform()))
            self.uzer = env.get(u'USER')
            icon = Image("photo", file=r'data/img/metadator.gif')
            self.call('wm', 'iconphoto', self._w, icon)
            self.minsize(580, 100)
            self.style.theme_use('clam')
        elif opersys == 'darwin':
            self.logger.info('Op. system: {0}'.format(platform.platform()))
            self.uzer = env.get(u'USER')
        else:
            self.logger.warning('Operating system not tested')
            self.logger.info('Op. system: {0}'.format(platform.platform()))
        self.resizable(width=False, height=False)
        self.focus_force()

        self.logger.info('GDAL version: {}'.format(gdal.__version__))

        # variables
        self.def_rep = ""       # folder to search for
        self.def_lang = 'FR'    # language to start
        self.def_doc = IntVar()     # to export into Word
        self.def_xls = IntVar()     # to export into Excel 2003
        self.def_xml = IntVar()     # to export into ISO 19139
        self.def_cat = IntVar()     # to merge all output Word files
        self.def_odt = IntVar()     # to export into OpenDocumentText
        self.def_dict = IntVar()    # to make a dictionnary of data
        self.def_kass = IntVar()    # to handle field name case sensitive
        self.def_stat = IntVar()    # to active/disable stats fields
        self.li_pro = []            # list for profiles in language selected
        self.li_shp = []            # list for shapefiles path
        self.li_tab = []            # list for MapInfo tables path
        self.num_folders = 0        # number of folders explored
        self.today = strftime("%Y-%m-%d")   # date of the day
        self.dico_layer = OD()      # dictionary about layer properties
        self.dico_profil = OD()     # dictionary from profile selected
        self.dico_fields = OD()     # dictionary for fields information
        self.dico_rekur = OD()      # dictionary of recurring attributes
        self.dico_err = OD()     # errors list
        self.dico_help = OD()                # dictionary of help texts
        li_lang = [lg for lg in listdir(r'locale')]   # available languages
        self.blabla = OD()      # texts dictionary

        # GUI fonts
        ft_tit = tkFont.Font(family="Times", size=10, weight=tkFont.BOLD)

        # fillfulling
        self.load_settings()
        self.load_texts(self.def_lang)
        self.li_profiles(self.def_lang)
        self.li_rekurs(self.def_lang)
        self.recup_help(self.def_lang)

        # Tabs
        self.nb = Notebook(self)
        self.tab_globals = Frame(self.nb)   # tab_id = 0
        self.tab_options = Frame(self.nb)   # tab_id = 1
        self.tab_attribs = Frame(self.nb)   # tab_id = 2
        self.nb.add(self.tab_globals,
                    text=self.blabla.get('gui_tab1'), padding=3)
        self.nb.add(self.tab_options,
                    text=self.blabla.get('gui_tab2'), padding=3)
        self.nb.add(self.tab_attribs,
                    text=self.blabla.get('gui_tab3'), padding=3)
        self.logger.info('UI created')

                ### Tab 1: global
        # Frames
        self.FrPath = Labelframe(self.tab_globals,
                                 name='main',
                                 text=self.blabla.get('tab1_fr1'))
        self.FrProg = Labelframe(self.tab_globals,
                                 name='progression',
                                 text=self.blabla.get('tab1_frprog'))
            ## Frame 1
        # target folder
        self.labtarg = Label(self.FrPath, text=self.blabla.get('tab1_path'))
        self.target = Entry(self.FrPath, width=25)
        self.browsetarg = Button(self.FrPath,       # browse button
                                 text=self.blabla.get('tab1_browse'),
                                 command=lambda: self.setpathtarg(),
                                 takefocus=True)
        self.browsetarg.focus_force()               # force the focus on
        self.profil = Label(self.FrPath, text=self.blabla.get('tab1_prof'))
        # profiles switcher
        self.ddl_profil = Combobox(self.FrPath, values=self.li_pro, width=5)
        self.ddl_profil.current(0)
        self.ddl_profil.bind("<<ComboboxSelected>>", self.select_profil)
        # widgets placement
        self.labtarg.grid(row=1, column=1, columnspan=1,
                          sticky=N + S + W + E, padx=2, pady=8)
        self.target.grid(row=1, column=2, columnspan=1,
                         sticky=N + S + W + E, padx=2, pady=8)
        self.browsetarg.grid(row=1, column=3,
                             sticky=N + S + W + E, padx=2, pady=8)
        self.profil.grid(row=2, column=1,
                         sticky=N + S + W + E, padx=2, pady=8)
        self.ddl_profil.grid(row=2, column=2, sticky=W + E + N + S,
                             columnspan=2, padx=2, pady=8)

        # tooltips
        InfoBulle(self.target, message=self.dico_help.get(30)[1])
        InfoBulle(self.browsetarg, message=self.dico_help.get(30)[1])
        InfoBulle(self.ddl_profil, message=self.dico_help.get(31)[1])

            ## Frame 2
        # variables
        self.status = StringVar(self.FrProg, '')
        # widgets
        self.prog_layers = Progressbar(self.FrProg, orient="horizontal")
        self.prog_fields = Progressbar(self.FrProg, orient="horizontal")
        # widgets placement
        Label(self.FrProg, textvariable=self.status,
                           foreground='DodgerBlue').pack(expand=1)
        self.prog_layers.pack(expand=1, fill=X)

        # Frames placement
        self.FrPath.pack(expand=1, fill='both')
        self.FrProg.pack(expand=1, fill='both')

                ### Tab 2: options
        # Export options
        caz_doc = Checkbutton(self.tab_options,
                              text=u'HTML / Word (.doc/.docx)',
                              variable=self.def_doc,
                              command=lambda: self.catalog_dependance())
        caz_xls = Checkbutton(self.tab_options,
                              text=u'Excel 2003 (.xls)',
                              variable=self.def_xls)
        caz_xml = Checkbutton(self.tab_options,
                              text=u'XML (ISO 19139)',
                              variable=self.def_xml)
        self.caz_cat = Checkbutton(self.tab_options,
                                   text=self.blabla.get('tab2_merge'),
                                   variable=self.def_cat)
        caz_odt = Checkbutton(self.tab_options,
                              text=u'Open Document Text (.odt)',
                              variable=self.def_odt)
        # widgets placement
        caz_doc.grid(row=1,
                     column=0,
                     sticky=N + S + W + E,
                     padx=2, pady=2)
        self.caz_cat.grid(row=2,
                          column=0,
                          sticky=N + S + W + E,
                          padx=2, pady=2)
        caz_xls.grid(row=1,
                     column=1,
                     sticky=N + S + W + E,
                     padx=2, pady=2)
        caz_xml.grid(row=2,
                     column=1,
                     sticky=N + S + W + E,
                     padx=2, pady=2)
        caz_odt.grid(row=3,
                     column=1,
                     sticky=N + S + W + E,
                     padx=2, pady=2)
        # disabling the widgets which work only on Windows OS
        if opersys != 'win32':
            self.logger.info('Disabling Windows reserved functions.')
            self.def_doc.set(0)
            self.def_cat.set(0)
            caz_doc.configure(state='disabled')
            self.caz_cat.configure(state='disabled')
        else:
            pass
        # make the catalog option depending on the Word option
        self.catalog_dependance()

        # tooltips
        InfoBulle(caz_doc,
                  message=self.dico_help.get(33)[1],
                  image=self.dico_help.get(33)[2])
        InfoBulle(caz_xls,
                  message=self.dico_help.get(34)[1],
                  image=self.dico_help.get(34)[2])
        InfoBulle(caz_xml,
                  message=self.dico_help.get(35)[1],
                  image=self.dico_help.get(35)[2])
        InfoBulle(caz_odt,
                  message=self.dico_help.get(36)[1],
                  image=self.dico_help.get(36)[2])
        InfoBulle(self.caz_cat,
                  message=self.dico_help.get(37)[1],
                  image=self.dico_help.get(37)[2])

                ### Tab 3: recurring attributes
        # Attribute selector
        self.lab_chps = Label(self.tab_attribs, text=self.blabla.get('tab3_sele'))
        self.ddl_attr = Combobox(self.tab_attribs, values=self.dico_rekur.keys())
        self.ddl_attr.bind("<<ComboboxSelected>>", self.edit_rekur)
        self.supr = Button(self.tab_attribs, text=self.blabla.get('tab3_supp'),
                           command=self.del_rekur)
        # frame
        self.FrRekur = Labelframe(self.tab_attribs,
                                  name='attributes',
                                  text=self.blabla.get('tab3_tit'))
        # attribute settings
        self.tab3_LBnom = Label(self.FrRekur,
                                text=self.blabla.get('tab3_nom'),
                                state=DISABLED)
        self.tab3_ENnom = Entry(self.FrRekur, state=DISABLED)
        self.tab3_LBdesc = Label(self.FrRekur,
                                 text=self.blabla.get('tab3_desc'),
                                 state=DISABLED)
        self.tab3_TXdesc = Text(self.FrRekur,
                                height=5, width=30,
                                wrap=WORD, state=DISABLED)
        self.tab3_CBcass = Checkbutton(self.FrRekur,
                                       text=self.blabla.get('tab3_cass'),
                                       variable=self.def_kass,
                                       state=DISABLED)
        self.tab3_CBstat = Checkbutton(self.FrRekur,
                                       text=self.blabla.get('tab3_stat'),
                                       variable=self.def_stat,
                                       state=DISABLED)
        # Validation button
        self.save = Button(self.FrRekur,
                           text=self.blabla.get('tab3_save'),
                           command=self.save_rekur,
                           state='disabled')

        # widgets placement
        self.lab_chps.grid(row=1, column=1, sticky=N + S + W,
                           padx=2, pady=2)
        self.ddl_attr.grid(row=1, column=2, sticky=N + S + W + E,
                           padx=2, pady=2)
        self.supr.grid(row=1, column=3, sticky=N + S + W + E,
                       padx=2, pady=2)
        self.tab3_LBnom.grid(row=1, column=0, columnspan=1,
                             sticky=N + S + W, padx=2, pady=2)
        self.tab3_ENnom.grid(row=1, column=1, columnspan=1,
                             sticky=N + S + W + E, padx=2, pady=2)
        self.tab3_LBdesc.grid(row=2, column=0, columnspan=1,
                              sticky=N + S + W + E, padx=2, pady=2)
        self.tab3_TXdesc.grid(row=2, column=1, columnspan=2,
                              sticky=N + S + W + E, padx=2, pady=2)
        self.tab3_CBcass.grid(row=3, column=0, columnspan=1,
                              sticky=N + S + W + E, padx=2, pady=2)
        self.tab3_CBstat.grid(row=3, column=1, columnspan=1,
                              sticky=N + S + W + E, padx=2, pady=2)
        self.save.grid(row=5, column=0, columnspan=4,
                       sticky=N + S + W + E, padx=2, pady=2)

        # Frame placement
        self.FrRekur.grid(row=2, column=1, columnspan=3,
                          sticky=N + S + W + E, padx=2, pady=2)

        # tooltips
        InfoBulle(self.lab_chps, message=self.dico_help.get(38)[1])
        InfoBulle(self.ddl_attr, message=self.dico_help.get(39)[1])
        InfoBulle(self.supr, message=self.dico_help.get(40)[1])
        InfoBulle(self.tab3_CBcass, message=self.dico_help.get(41)[1])
        InfoBulle(self.tab3_CBstat, message=self.dico_help.get(42)[1])

            ## Main frame
        # Hola
        self.welcome = Label(self,
                             text=self.blabla.get('hi') + self.uzer,
                             font=ft_tit,
                             foreground="red2")
        # Image
        self.icone = PhotoImage(master=self, file=r'data/img/metadator.gif')
        Label(self, image=self.icone).grid(row=2,
                                           column=0,
                                           padx=2,
                                           pady=2,
                                           sticky=N + S + W + E)
        # credits
        s = Style(self)
        s.configure('Kim.TButton', foreground='DodgerBlue',
                    borderwidth=0, relief="flat")
        Button(self,
               text='by Julien M. (2015)',
               style='Kim.TButton',
               command=lambda: open_new('https://github.com/Guts')).grid(row=3,
                                                                         padx=2,
                                                                         pady=2,
                                                                         sticky=W+E)
        # language switcher
        self.ddl_lang = Combobox(self, values=li_lang, width=5)
        self.ddl_lang.current(li_lang.index(self.def_lang))
        self.ddl_lang.bind("<<ComboboxSelected>>", self.change_lang)
        # Go go go button
        self.val = Button(self,
                          text=self.blabla.get('tab1_go'),
                          state='active',
                          command=lambda: self.process())
        # Cancel button
        self.can = Button(self,
                          text=self.blabla.get('gui_quit'),
                          command=self.destroy)
        # widgets placement
        self.welcome.grid(row=0, column=0, columnspan=1, sticky=N + S + W + E,
                          padx=2, pady=2)
        self.ddl_lang.grid(row=1, column=0, sticky=N, padx=2, pady=0)
        self.can.grid(row=4, column=0, sticky=N + S + W + E, padx=2, pady=2)
        self.val.grid(row=4, column=1, sticky=N + S + W + E, padx=2, pady=2)

        # tooltips
        InfoBulle(self.ddl_lang, message=self.dico_help.get(32)[1])

                ### Notebook placement
        self.nb.grid(row=0, rowspan=4, column=1, sticky=N + S + W + E)
        # keep updated list of profiles
        self.maj()

    def maj(self):
        """
        update the profiles dropdown list every second
        """
        try:
            self.li_profiles(self.ddl_lang.get())
            self.ddl_profil['values'] = self.li_pro
            self.after(1000, self.maj)
        except WindowsError:    # avoid an error occuring with browse button
            self.after(1000, self.maj)
            pass

    def alter_state(self, parent, new_state):
        """
        just a function to change easily  the state of  all children widgets
        of a parent class

        parent=Tkinter class with children (Frame, Labelframe, Tk, etc.)
        new_state=Tkinter keyword for widget state (ACTIVE, NORMAL, DISABLED)
        """
        for child in parent.winfo_children():
            child.configure(state=new_state)
        # end of function
        return parent, new_state

    def catalog_dependance(self):
        """ unselect the catalog option if the word option is unselected """
        if self.def_doc.get() == 0:
            self.def_cat.set(0)
            self.caz_cat.config(state='disabled')
        elif self.def_doc.get() == 1:
            self.caz_cat.config(state='normal')
        # end of function
        return

    def load_settings(self):
        u""" load settings from last execution """
        confile = 'options.ini'
        config = ConfigParser.RawConfigParser()
        config.read(confile)
        # basics
        self.def_lang = config.get('basics', 'def_codelang')
        self.def_rep = config.get('basics', 'def_rep')
        # export preferences
        self.def_doc.set(config.get('export_preferences', 'def_word'))
        self.def_cat.set(config.get('export_preferences', 'def_cat'))
        self.def_xls.set(config.get('export_preferences', 'def_xls'))
        self.def_xml.set(config.get('export_preferences', 'def_xml'))
        self.def_dict.set(config.get('export_preferences', 'def_dict'))
        self.def_odt.set(config.get('export_preferences', 'def_odt'))
        # log
        self.logger.info('Last options loaded')
        # End of function
        return config, self.def_rep, self.def_lang, self.def_doc

    def save_settings(self):
        u""" save options in order to make the next execution easier """
        confile = 'options.ini'
        config = ConfigParser.RawConfigParser()
        # add sections
        config.add_section('basics')
        config.add_section('export_preferences')
        # basics
        config.set('basics', 'def_codelang', self.ddl_lang.get())
        config.set('basics', 'def_rep', self.target.get())
        # export preferences
        config.set('export_preferences', 'def_word', self.def_doc.get())
        config.set('export_preferences', 'def_cat', self.def_cat.get())
        config.set('export_preferences', 'def_xls', self.def_xls.get())
        config.set('export_preferences', 'def_xml', self.def_xml.get())
        config.set('export_preferences', 'def_dict', self.def_dict.get())
        config.set('export_preferences', 'def_odt', self.def_odt.get())
        # Writing the configuration file
        with open(confile, 'wb') as configfile:
            config.write(configfile)
        # End of function
        return config

    def change_lang(self, event):
        u""" update the texts dictionary with the language selected """
        new_lang = event.widget.get()
        # change to the new language selected
        self.load_texts(new_lang)
        self.li_profiles(new_lang)
        self.li_rekurs(new_lang)
        self.ddl_profil.delete(0, END)
        self.ddl_profil.config(values=self.li_pro)
        self.ddl_profil.update()
        self.ddl_attr.config(values=self.dico_rekur.keys())
        self.recup_help(new_lang)
        # update widgets text
          # tab1
        self.nb.tab(0, text=self.blabla.get('gui_tab1'))
        self.welcome.config(text=self.blabla.get('hi') + self.uzer)
        self.can.config(text=self.blabla.get('gui_quit'))
        self.FrPath.config(text=self.blabla.get('tab1_fr1'))
        self.FrProg.config(text=self.blabla.get('tab1_frprog'))
        self.labtarg.config(text=self.blabla.get('tab1_path'))
        self.browsetarg.config(text=self.blabla.get('tab1_browse'))
        self.val.config(text=self.blabla.get('tab1_go'))
        self.profil.config(text=self.blabla.get('tab1_prof'))
          # tab2
        self.nb.tab(1, text=self.blabla.get('gui_tab2'))
        self.caz_cat.config(text=self.blabla.get('tab2_merge'))
          # tab3
        self.nb.tab(2, text=self.blabla.get('gui_tab3'))
        self.lab_chps.config(text=self.blabla.get('tab3_sele'))
        self.supr.config(text=self.blabla.get('tab3_supp'))
        self.FrRekur.config(text=self.blabla.get('tab3_tit'))
        self.tab3_LBnom.config(text=self.blabla.get('tab3_nom'))
        self.tab3_LBdesc.config(text=self.blabla.get('tab3_desc'))
        self.tab3_CBcass.config(text=self.blabla.get('tab3_cass'))
        self.tab3_CBstat.config(text=self.blabla.get('tab3_stat'))
        self.save.config(text=self.blabla.get('tab3_save'))

        # End of function
        return self.blabla

    def load_texts(self, lang='FR'):
        u"""
        Load texts according to the selected language
        """
        # clearing the text dictionary
        self.blabla.clear()
        # open xml cursor
        xml = ET.parse('locale/{0}/lang_{0}.xml'.format(lang))
        # Looping and gathering texts from the xml file
        for elem in xml.getroot().getiterator():
            self.blabla[elem.tag] = elem.text
        # updating the GUI
        self.update()
        # en of function
        return self.blabla

    def setpathtarg(self):
        """ ...browse and insert the path of target folder """
        foldername = askdirectory(parent=self,
                                  initialdir=self.def_rep,
                                  mustexist=True,
                                  title=self.blabla.get('gui_cible'))
        # check if a folder has been choosen
        if foldername:
            try:
                self.target.delete(0, END)
                self.target.insert(0, foldername)
            except:
                info(title=self.blabla.get('nofolder'),
                     message=self.blabla.get('nofolder'))
                return

        # count shapefiles and MapInfo files in a separated thread
        proc = threading.Thread(target=self.li_geofiles,
                                args=(foldername, ))
        proc.daemon = True
        proc.start()

        # end of function
        return foldername

    def li_geofiles(self, foldertarget):
        u""" List shapefiles and MapInfo files (.tab, not .mid/mif) contained
        in the folders structure """
        # reseting global variables
        self.li_shp = []
        self.li_tab = []
        self.browsetarg.config(state=DISABLED)
        # Looping in folders structure
        self.status.set(self.blabla.get('tab1_prog1'))
        self.prog_layers.start()
        for root, dirs, files in walk(unicode(foldertarget)):
            self.num_folders = self.num_folders + len(dirs)
            for f in files:
                """ looking for files with geographic data """
                try:
                    unicode(path.join(root, f))
                    full_path = path.join(root, f)
                except UnicodeDecodeError:
                    full_path = path.join(root, f.decode('latin1'))
                # Looping on files contained
                if path.splitext(full_path.lower())[1].lower() == '.shp'\
                   and (path.isfile('{0}.dbf'.format(full_path[:-4]))
                        or path.isfile('{0}.DBF'.format(full_path[:-4])))\
                   and (path.isfile('{0}.shx'.format(full_path[:-4]))
                        or path.isfile('{0}.SHX'.format(full_path[:-4]))):
                    """ listing compatible shapefiles """
                    # add complete path of shapefile
                    self.li_shp.append(full_path)
                elif path.splitext(full_path.lower())[1] == '.tab'\
                    and (path.isfile(full_path[:-4] + '.dat')
                         or path.isfile(full_path[:-4] + '.DAT'))\
                    and (path.isfile(full_path[:-4] + '.map')
                         or path.isfile(full_path[:-4] + '.MAP'))\
                    and (path.isfile(full_path[:-4] + '.id')
                         or path.isfile(full_path[:-4] + '.ID')):
                    """ listing MapInfo tables """
                    # add complete path of MapInfo file
                    self.li_tab.append(full_path)
        # stopping the progress bar
        self.prog_layers.stop()
        # Lists ordering and tupling
        self.li_shp.sort()
        self.li_shp = tuple(self.li_shp)
        self.li_tab.sort()
        self.li_tab = tuple(self.li_tab)
        # setting the label text and activing the buttons
        self.status.set(unicode(len(self.li_shp)) + u' shapefiles - '
                        + unicode(len(self.li_tab)) + u' tables (MapInfo) - '
                        + unicode(self.num_folders) + self.blabla.get('log_numfold'))
        self.browsetarg.config(state=ACTIVE)
        self.val.config(state=ACTIVE)
        # End of function
        return foldertarget, self.li_shp, self.li_tab

    def li_profiles(self, lang):
        u"""
        list profiles already existing
        """
        # reseting global variable
        self.li_pro = []
        # Looping in folders structure
        folder_profiles = path.join('locale/', lang + '/profiles/')
        self.li_pro = [lg[:-4] for lg in listdir(folder_profiles)]
        self.li_pro.append(self.blabla.get('tab1_new'))
        # End of function
        return folder_profiles, self.li_pro

    def li_rekurs(self, lang):
        u"""
        List recurring attributes that already exist in the selected language
        """
        # clearing the text dictionary
        self.dico_rekur.clear()
        champis = path.abspath(r'locale/{0}/champignons_{0}.xml'.format(lang))
        xml = ET.parse(champis)
        # Looping and gathering texts from the xml file
        for elem in xml.findall('champ'):
            rek_name = elem.find('intitule').text
            rek_desc = elem.find('description').text
            rek_kass = elem.find('case').text
            rek_stat = elem.find('stats').text
            self.dico_rekur[rek_name] = rek_desc, rek_kass, rek_stat
        self.dico_rekur[self.blabla.get('tab3_new')] = '', 0, 0
        # updating the GUI
        self.update()
        # End of function
        return self.dico_rekur

    def edit_rekur(self, event):
        u"""
        preparing the form to edit a recurring attribute
        """
        rekur = event.widget.get()
        # deactivate the selector
        self.ddl_attr.config(state=DISABLED)
        # activate the form
        self.alter_state(self.FrRekur, NORMAL)
        # change to the new language selected
        self.tab3_ENnom.insert(0, rekur)
        self.tab3_TXdesc.insert(1.0, self.dico_rekur.get(rekur)[0])
        self.def_kass.set(self.dico_rekur.get(rekur)[1])
        self.def_stat.set(self.dico_rekur.get(rekur)[2])
        # End of function
        return self.dico_rekur

    def save_rekur(self):
        u""" save the recurring attribute edited """
        # check if the attribute already exists
        if self.tab3_ENnom.get() in self.dico_rekur:
            if not askyesno(title=self.blabla.get('tab3_alert_exist1'),
                            message=self.blabla.get('tab3_alert_exist2')):
                return
            else:
                pass
        else:
            pass

        # save
        self.dico_rekur[self.tab3_ENnom.get()] = self.tab3_TXdesc.get(1.0, END).rstrip(),\
                                                 self.def_kass.get(),\
                                                 self.def_stat.get()
        # reset the form
        self.tab3_ENnom.delete(0, END)
        self.tab3_TXdesc.delete(1.0, END)
        self.def_kass.set(0)
        self.def_stat.set(0)
        # deactivate the form
        self.alter_state(self.FrRekur, DISABLED)
        # updating the dropdown list
        self.ddl_attr.config(state=NORMAL)
        self.ddl_attr.delete(0, END)
        self.ddl_attr['values'] = self.dico_rekur.keys()

        # End of function
        return self.dico_rekur

    def del_rekur(self):
        u""" delete the selected recurring attribute """
        # reactivate the selector
        self.ddl_attr.config(state=ACTIVE)
        self.dico_rekur.pop(self.ddl_attr.get())

        self.ddl_attr.delete(0, END)
        self.ddl_attr['values'] = self.dico_rekur.keys()
        # reset the form
        self.tab3_ENnom.delete(0, END)
        self.tab3_TXdesc.delete(1.0, END)
        self.def_kass.set(0)
        self.def_stat.set(0)
        # deactivate the form
        self.alter_state(self.FrRekur, DISABLED)

        # End of function
        return self.dico_rekur

    def saveas_rekurs(self, lang):
        u""" save the recurring fields into the file dedicated """
        rekur = ET.Element(u'champs')
        xml_path = r'locale/{0}/champignons_{0}.xml'.format(lang)
        self.dico_rekur.pop(self.blabla.get('tab3_new'))
        with open(xml_path, 'w') as champis:
            for elem in self.dico_rekur.keys():
                rek = ET.SubElement(rekur, u'champ')
                # name of recurring attribute
                rek_name = ET.SubElement(rek, u'intitule')
                rek_name.text = elem
                # description of recurring attribute
                rek_desc = ET.SubElement(rek, u'description')
                rek_desc.text = self.dico_rekur.get(elem)[0]
                # stats option of recurring attribute
                rek_stats = ET.SubElement(rek, u'stats')
                rek_stats.text = unicode(self.dico_rekur.get(elem)[1])
                # case sensitive option of recurring attribute
                rek_case = ET.SubElement(rek, u'case')
                rek_case.text = unicode(self.dico_rekur.get(elem)[2])

        # creating the xml tree
        out_rekurs = ET.ElementTree(rekur)
        # saving it
        out_rekurs.write(xml_path,
                         encoding='utf-8',
                         xml_declaration='version="1.0"',
                         method='xml')

        # End of function
        return self.dico_rekur

    def select_profil(self, event):
        """ when a profile is selected... """
        profsel = event.widget.get()
        # if user wants to use an existing profile or create a new one
        if profsel == self.blabla.get('tab1_new'):
            self.val.config(text=self.blabla.get('tab1_crprofil'))
        else:
            self.val.config(text=self.blabla.get('tab1_go'))

        # end of function
        return self.val

    def recup_profil(self, lang):
        """ get the information from the profile selected """
        # clearing the profile dictionary
        self.dico_profil.clear()
        # specific path to profile file
        path_profile = path.join('locale/{0}/profiles/{1}.xml'.format(lang,
                                                                      self.ddl_profil.get()))
        with open(path_profile, 'r') as profile:
            # open xml parser
            xml = ET.parse(profile)
            # basic informations
            self.dico_profil['description'] = xml.find('description').text
            self.dico_profil['sources'] = xml.find('sources').text
            self.dico_profil['url'] = xml.find('url').text
            self.dico_profil['url_label'] = xml.find('url_label').text
            self.dico_profil[u'diffusion'] = xml.find('diffusion').text
            # data language
            lang_data = xml.find(u'lang_data')
            self.dico_profil[u"lang_data"] = lang_data.find(u'name').text
            # metadata language
            lang_metad = xml.find(u'lang_metad')
            self.dico_profil[u"lang_md"] = lang_metad.find(u'name').text
            # diffusion constraints
            diff = xml.find(u'diffusion')
            self.dico_profil['diffusion'] = diff.find(u'name').text
            # update rythm
            rythm = xml.find(u'rythm')
            self.dico_profil['rythm'] = rythm.find(u'name').text
            # INSPIRE themes
            themes = xml.find('themesinspire')
            li_themesinspire = [theme.find('name').text for theme in themes.findall('theme')]
            self.dico_profil['themesinspire'] = li_themesinspire
            # custom keywords
            keywords = xml.find('keywords')
            li_keywords = [keyword.find('name').text for keyword in keywords.findall('keyword')]
            self.dico_profil['keywords'] = li_keywords
            # places keywords
            geokeywords = xml.find('geokeywords')
            li_geokeywords = [geokeyword.find('name').text for geokeyword in geokeywords.findall('geokeyword')]
            self.dico_profil['geokeywords'] = li_geokeywords
            # contacts
            contacts = xml.find(u'contacts')
            # point of contact
            cont = contacts.find(u'pointdecontact')
            self.dico_profil[u'cont_name'] = cont.find(u'name').text
            self.dico_profil[u'cont_orga'] = cont.find(u'org').text
            self.dico_profil[u'cont_mail'] = cont.find(u'mail').text
            self.dico_profil[u'cont_role'] = cont.find(u'role').text
            self.dico_profil[u'cont_func'] = cont.find(u'func')[0].text
            self.dico_profil[u'cont_street'] = cont.find(u'street').text
            self.dico_profil[u'cont_city'] = cont.find(u'city').text
            self.dico_profil[u'cont_cp'] = cont.find(u'cp').text
            self.dico_profil[u'cont_country'] = cont.find(u'country').text
            self.dico_profil[u'cont_phone'] = cont.find(u'tel').text
            # second contact (responsable, etc.)
            resp = contacts.find(u'second_contact')
            self.dico_profil[u'resp_name'] = resp.find(u'name').text
            self.dico_profil[u'resp_orga'] = resp.find(u'org').text
            self.dico_profil[u'resp_mail'] = resp.find(u'mail').text
            self.dico_profil[u'resp_role'] = resp.find(u'role').text
            self.dico_profil[u'resp_func'] = resp.find(u'func')[0].text
            self.dico_profil[u'resp_street'] = resp.find(u'street').text
            self.dico_profil[u'resp_city'] = resp.find(u'city').text
            self.dico_profil[u'resp_cp'] = resp.find(u'cp').text
            self.dico_profil[u'resp_country'] = resp.find(u'country').text
            self.dico_profil[u'resp_phone'] = resp.find(u'tel').text
        # End of function
        return self.dico_profil

    def recup_help(self, lang):
        """ get the help texts """
        # specific path to xml file
        path_help = 'locale/%s/help_%s.xml' % (lang, lang)
        # reading and parsing the xml
        with open(path_help, 'r') as source:
            xml = ET.parse(source)                  # xml cursor
            for tooltip in xml.findall('tooltip'):
                idu = tooltip.find('id').text
                ref = tooltip.find('ref').text
                txt = tooltip.find('txt').text
                img = tooltip.find('image').text
                doc = tooltip.find('doc').text
                # fillfulling the INSPIRE dictionary
                self.dico_help[int(idu)] = ref, txt, img, doc
        # End of function
        return self.dico_help

    def process(self):
        u""" launch the different processes """
        # display the main tab
        self.nb.select(0)
        # check option selected: process or create a new profile
        if self.ddl_profil.get() == self.blabla.get('tab1_new'):
            # launching the profile form
            self.logger.info('Creation of a new profile')
            tr_profile = threading.Thread(target=NewProfile,
                                          args=(self.blabla,
                                                self.ddl_lang.get(),
                                                self.dico_help,
                                                self.li_pro))
            tr_profile.daemon = True
            tr_profile.run()
            # NewProfile(self.blabla, self.ddl_lang.get(), self.li_pro)
            self.li_profiles(self.ddl_lang.get())   # updating the dropdow list
            self.ddl_profil['values'] = self.li_pro
            return
        # check if the target folder has been selected
        if self.target.get() == "":
            info(title=self.blabla.get('info_blanktarget1'),
                 message=self.blabla.get('info_blanktarget2'))
            return
        # check if a profile has been selected
        if self.ddl_profil.get() == "":
            info(title=self.blabla.get('info_blankprofile1'),
                 message=self.blabla.get('info_blankprofile2'))
            return
        # disabling others GUI parts
        self.tab_globals.focus_force()
        self.alter_state(self.FrPath, DISABLED)

        # check if there are some layers into the folder structure
        if len(self.li_shp) + len(self.li_tab) == 0:
            self.logger.warning("No geofiles found in the folder structure")
            self.status.set(self.blabla.get('log_nodata'))
            return
        # specific variables
        dest = path.join(self.target.get(), 'metadator')
        if not path.isdir(dest):    # test if folder already exists
            mkdir(dest, 0777)       # if not, we create it
        # getting profile informations
        self.recup_profil(self.ddl_lang.get())
        # saving options in a separated thread
        tr_options = threading.Thread(target=self.save_settings)
        tr_options.daemon = True
        tr_options.start()
        self.logger.info('Current options saved')
        # saving recurring fiels in a separated thread
        tr_rekurs = threading.Thread(target=self.saveas_rekurs,
                                     args=(self.ddl_lang.get(), ))
        tr_rekurs.daemon = True
        tr_rekurs.start()
        # configuring the progression bar
        self.prog_layers["maximum"] = len(self.li_shp) + len(self.li_tab)
        self.prog_layers["value"]
        # Processing the shapefiles
        self.logger.info('\tStart processing the files')
        for shp in self.li_shp:
            """ looping on shapefiles list """
            self.logger.info('Processing: %s' % path.basename(shp))
            self.status.set(path.basename(shp))
            # reset recipient data
            self.dico_layer.clear()
            self.dico_fields.clear()
            # getting separated process threads
            Read_SHP(shp,
                     self.dico_layer,
                     self.dico_fields,
                     'shape',
                     self.blabla)
            # checking layer error
            if self.dico_layer.get('error'):
                # increment the progress bar
                self.prog_layers["value"] = self.prog_layers["value"] + 1
                self.update()
                self.logger.warning('This shape has an issue: %s' % shp)
                continue
            # getting fields statistics only if needed
            if self.def_doc.get() == 1 or self.def_xls.get() == 1 or self.def_odt.get() == 1:
                StatsFields(shp, self.dico_fields, self.dico_rekur, self.blabla)
            # export according to options selected
            if self.def_doc.get() == 1:
                ExportToHTML(dest,
                             self.dico_layer,
                             self.dico_fields,
                             self.dico_profil,
                             self.dico_rekur,
                             self.blabla)
                html_path = path.join(dest,
                                      "{0}_MD.html".format(self.dico_layer['name'][:-4]))
                ExportToDocX(html_path, dest)
            if self.def_xls.get() == 1:
                ExportToXLS(dest,
                            self.dico_layer,
                            self.dico_fields,
                            self.dico_profil,
                            self.dico_rekur,
                            self.blabla)
            if self.def_xml.get() == 1:
                ExportToXML(dest,
                            self.dico_layer,
                            self.dico_profil,
                            '',
                            self.blabla,
                            1,
                            0)
            if self.def_odt.get() == 1:
                ExportToODT(dest,
                            self.dico_layer,
                            self.dico_fields,
                            self.dico_profil,
                            self.dico_rekur,
                            self.blabla)
            # increment the progress bar
            self.prog_layers["value"] = self.prog_layers["value"] + 1
            self.update()

        # Processing the MapInfo tables
        for tab in self.li_tab:
            """ looping on MapInfo tables list """
            self.logger.info('Processing: %s' % path.basename(tab))
            self.status.set(path.basename(tab))
            # reset recipient data
            self.dico_layer.clear()
            self.dico_fields.clear()
            # getting the informations
            Read_TAB(tab,
                     self.dico_layer,
                     self.dico_fields,
                     'table',
                     self.blabla)
            # checking layer error
            if self.dico_layer.get('error'):
                self.logger.warning('This MapInfo table has an issue: %s' % tab)
                # increment the progress bar
                self.prog_layers["value"] = self.prog_layers["value"] +1
                self.update()
                continue
            # getting fields statistics only if needed
            if self.def_doc.get() == 1 \
               or self.def_xls.get() == 1 \
               or self.def_odt.get() == 1:
                StatsFields(tab, self.dico_fields, self.dico_rekur, self.blabla)
            # export according to options selected
            if self.def_doc.get() == 1:
                ExportToHTML(dest,
                             self.dico_layer,
                             self.dico_fields,
                             self.dico_profil,
                             self.dico_rekur,
                             self.blabla)
                html_path = path.join(dest,
                                      "{0}_MD.html".format(self.dico_layer['name'][:-4]))
                ExportToDocX(html_path, dest)
            if self.def_xls.get() == 1:
                ExportToXLS(dest,
                            self.dico_layer,
                            self.dico_fields,
                            self.dico_profil,
                            self.dico_rekur,
                            self.blabla)
            if self.def_xml.get() == 1:
                ExportToXML(dest,
                            self.dico_layer,
                            self.dico_profil,
                            '',
                            self.blabla,
                            1,
                            0)
            if self.def_odt.get() == 1:
                ExportToODT(dest,
                            self.dico_layer,
                            self.dico_fields,
                            self.dico_profil,
                            self.dico_rekur,
                            self.blabla)
            # increment the progress bar
            self.prog_layers["value"] = self.prog_layers["value"] + 1
            self.update()

        # Word catalog export
        if self.def_doc.get() == 1 and self.def_cat.get() == 1:
            self.status.set(self.blabla.get('info_cat'))
            self.update()
            DocxMerger(dest, '00_Metadator_Catalog', 'metadator_')
        else:
            pass

        # final message
        # msg = self.blabla.get('info_end2') + self.blabla.get('info_end3')
        # info(title=self.blabla.get('info_end'), message=msg)
        # opening the destination folder
        self.open_dir_file(dest)
        # cleaning up
        logging.info('Hurray! It worked! All seem to have been fine!')
        self.destroy()
        # end of function
        return

    def open_dir_file(self, target):
        """
        Open a file or a directory in the explorer of the operating system
        http://sametmax.com/ouvrir-un-fichier-avec-le-bon-programme-en-python
        """
        # check if the file or the directory exists
        if not path.exists(target):
            raise IOError('No such file: {0}'.format(target))

        # check the read permission
        if not access(target, R_OK):
            raise IOError('Cannot access file: {0}'.format(target))

        # open the directory or the file according to the os
        if opersys == 'win32':  # Windows
            proc = startfile(target)

        elif opersys.startswith('linux'):  # Linux:
            proc = subprocess.Popen(['xdg-open', target],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)

        elif opersys == 'darwin':  # Mac:
            proc = subprocess.Popen(['open', '--', target],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)

        else:
            raise NotImplementedError(
                "Your `%s` isn't a supported operating system`." % opersys)

        # end of function
        return proc

###############################################################################
###### Stand alone program ########
###################################

if __name__ == '__main__':
    """ Test parameters for a stand-alone run """
    app = Metadator()
    app.mainloop()
