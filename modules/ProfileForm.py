# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
#------------------------------------------------------------------------------
# Name:         Metadata profile form
# Purpose:      Allow to create a metadata profile which could be used after in
#                   metadator. Profiles are saved as xml files.
# Author:       Julien Moura (https://github.com/Guts/)
# Python :      2.7.x
# Encoding:     utf-8
# Created:      17/11/2011
# Updated:      20/08/2014
#------------------------------------------------------------------------------

###############################################################################
######## Libraries import #########
###################################

from Tkinter import Tk, Canvas, IntVar, StringVar, Entry, Text, Listbox, PhotoImage
from Tkinter import VERTICAL, HORIZONTAL, S, E, W, NE, NW, SE, END, WORD, DISABLED, NORMAL, ACTIVE
from ttk import Combobox, Style, Labelframe, Frame, Label, Button, Radiobutton, Sizegrip, Scrollbar, Separator

from tkMessageBox import showerror as avert     # fenêtre d'avertissement
from tkMessageBox import askyesno as okno       # fenêtre de confirmation

from os import environ as env               # paramètres d'environnement
from os import chdir, path                 # gestion fichiers/dossiers
from sys import platform

from datetime import date                   # gestion dates

from xml.etree import ElementTree as ET     # pour les xml

# from re import compile, IGNORECASE          # expressions régulières

# Python 3 backported
from collections import OrderedDict as OD

# Custom modules
from InfoBulles import InfoBulle

###############################################################################
############# Classes #############
###################################


class NewProfile(Tk):
    """ Graphic form to create a new profile for metadata """
    def __init__(self, txt, lang, txt_help, profiles):
        """
        New profile from Metadator
        txt = dictionary about text depending on language selected in Metadator
        lang = language selected
        txt_help = dictionary of help texts for tooltips
        profiles = list of existing profiles
        """
        Tk.__init__(self)               # constructor of parent graphic class
        # variables
        self.dico_keywords = OD()            # dict of user's keywords
        self.dico_geokeywords = OD()         # dict of user's geokeywords
        self.dico_inspire = OD()             # dict of INSPIRE thematics
        self.dico_iso = OD()                 # dict of ISO thematics
        self.dico_rythms = OD()              # dict of ISO update ryhms
        self.dico_diffusions = OD()          # dict of diffusion types
        self.dico_functions = OD()           # dict of INSPIRE functions
        self.dico_specifications = OD()      # dict of INSPIRE specifications
        self.dico_contacts = OD()            # dict of user's contacts
        self.dico_lang = OD()                # dict of languages ISO

        # getting the xml data
        self.recup_themes_INSPIRE(lang)
        self.recup_keywords(lang)
        self.recup_geo_keywords(lang)
        self.recup_rythms(lang)
        self.recup_diffusion(lang)
        self.recup_lang_ISO()
        self.recup_contacts(lang)
        self.recup_fonctions(lang)

        # basics settings
        max_height = self.winfo_screenheight() - 70
        self.geometry("740x%d+250+0" % max_height)      # dimensions
        self.style = Style()        # more friendly windows style
        if platform == 'win32':
            self.iconbitmap(r'metadator.ico')    # windows icon
            self.uzer = env.get(u'USERNAME')
        elif platform == 'linux2':
            self.uzer = env.get(u'USER')
            icon_2 = PhotoImage(master=self,
                                file=r'data/img/icon_NewProfile_np7782.gif')
            self.call('wm', 'iconphoto', self._w, icon_2)
            self.style.theme_use('clam')
            self.minsize(650, 100)
        elif platform == 'darwin':
            self.uzer = env.get(u'USER')
        else:
            print('Operating system unknown')
        self.resizable(width=True, height=True)     # window resizable
        self.title(txt.get('form_titre'))  # title
        sz = Sizegrip(self)
        sz.grid(column=1, row=1, sticky='se')
        self.protocol('WM_DELETE_WINDOW',
                      lambda: self.confirm_exit(txt))   # close control

        # GUI variables
        self.new_name = StringVar(self)              # name of new profile
        self.url = StringVar(self)                   # url link
        self.url_label = StringVar(self)             # link label
        self.new_kword = StringVar(self)             # new keyword
        self.new_geokword = StringVar(self)          # geographic keywords

        # icons
        path_icon_del_tag = r"data/img/icon_DelTag_np8756.gif"
        self.icon_del_tag = PhotoImage(master=self,
                                       name='remove_keyword',
                                       file=path_icon_del_tag)
        path_icon_new_tag = r"data/img/icon_AddTag_np8755.gif"
        self.icon_new_tag = PhotoImage(master=self,
                                       name='new_keyword',
                                       file=path_icon_new_tag)
        path_icon_inspire = r"data/img/icon_INSPIRE_np23902.gif"
        self.icon_inspire = PhotoImage(master=self,
                                       name='pineapple_inspire',
                                       file=path_icon_inspire)
        path_icon_new_profile = r"data/img/icon_NewProfile_np7782.gif"
        self.icon_new_profile = PhotoImage(master=self,
                                           name='new_profile',
                                           file=path_icon_new_profile)
        path_icon_import_profile = r"data/img/icon_ImportProfile_np14001.gif"
        self.icon_import_profile = PhotoImage(master=self,
                                              name='import_profile',
                                              file=path_icon_import_profile)
        path_icon_diffusion = r"data/img/icon_share_33023.gif"
        self.icon_diffusion = PhotoImage(master=self,
                                         name='diffusion_share',
                                         file=path_icon_diffusion)

        # scrollbars
        sb_vglob = Scrollbar(self, orient=VERTICAL)
        sb_vglob.grid(row=0, column=1, sticky="NS")
        sb_hglob = Scrollbar(self, orient=HORIZONTAL)
        sb_hglob.grid(row=1, column=0, sticky="EW")

        # activating the scrolling with mouse wheel
        self.bind("<MouseWheel>", self.mouse_wheel)          # Windows
        self.bind("<Button-4>", self.mouse_wheel)            # Unix
        self.bind("<Button-5>", self.mouse_wheel)

        # main canvas and scrollbars assignment
        self.c_main = Canvas(self,
                             yscrollcommand=sb_vglob.set,
                             xscrollcommand=sb_hglob.set)
        self.c_main.grid(row=0, column=0, sticky="NWSE")
        sb_vglob.config(command=self.c_main.yview)
        sb_hglob.config(command=self.c_main.xview)
        self.grid_rowconfigure(0, weight=1)         # row weight
        self.grid_columnconfigure(0, weight=1)      # column weight
        self.c_main.grid_columnconfigure(0, weight=1)
        self.c_main.grid_rowconfigure(0, weight=1)
        self.grid_propagate()

        # parent frame
        self.form = Frame(self.c_main)

        # frames
        self.FrMain = Labelframe(self.form,
                                 name='main',
                                 text=txt.get('form_param').upper())
        self.FrDescrip = Labelframe(self.form,
                                    name='description',
                                    text=txt.get('description').upper())
        self.FrThemes = Labelframe(self.form,
                                   name='themes',
                                   text=txt.get('chp_inspire').upper())
        self.FrKeyword = Labelframe(self.form,
                                    name='keywords',
                                    text=txt.get('mtcthem').upper())
        self.FrGeokeyw = Labelframe(self.form,
                                    name='geokeywords',
                                    text=txt.get('mtcgeo').upper())
        self.FrDivers = Labelframe(self.form,
                                   name='divers',
                                   text=txt.get('form_divers').upper())
        self.FrCgu = Labelframe(self.form,
                                name='inspire',
                                text=txt.get('form_cgu').upper())
        self.FrContact = Labelframe(self.form,
                                    name='contacts',
                                    text=txt.get('form_cont').upper())
        self.FrEndForm = Frame(self.form,
                               name='save_or_quit')

            ## Frame 1: basics informations
        self.FrMain.grid_columnconfigure(1, weight=1)
        # widgets
        self.lb_icon_new_profile = Label(self.FrMain,
                                         image=self.icon_new_profile)
        self.lb_name_profile = Label(self.FrMain, text=txt.get('chp_nomfic'))
        self.ent_name = Entry(self.FrMain, textvariable=self.new_name)

        self.lb_icon_import_profile = Label(self.FrMain, image=self.icon_import_profile)
        self.ent_name.insert(0, str(date.today()) + "_")
        self.bu_import_profile = Button(self.FrMain,
                                        text=txt.get('form_auto'),
                                        command=lambda: self.import_profile(lang, txt))
        self.ddl_prof = Combobox(self.FrMain, values=profiles)

        # widgets placement
        self.lb_icon_new_profile.grid(row=1, rowspan=2, column=0,
                                      padx=8, pady=2, sticky="NSW")
        self.lb_name_profile.grid(row=1, column=1, columnspan=2,
                                  padx=8, pady=2, sticky="NSWE")
        self.ent_name.grid(row=2, column=1, columnspan=2,
                           padx=8, pady=2, sticky="NSWE")
        Separator(master=self.FrMain, orient=VERTICAL).grid(row=1, rowspan=2,
                                                            column=3, pady=1,
                                                            sticky="NSWE")
        self.lb_icon_import_profile.grid(row=1, rowspan=2, column=4,
                                         padx=8, pady=2)
        self.bu_import_profile.grid(row=1, column=5, columnspan=2,
                                    padx=8, pady=2, sticky="EW")
        self.ddl_prof.grid(row=2, column=5, columnspan=2,
                           padx=8, pady=2, sticky="EW")

        # tooltips
        InfoBulle(self.ent_name, message=txt_help.get(1)[1])
        InfoBulle(self.ddl_prof, message=txt_help.get(2)[1])

            ## Frame 2: descriptive informations
        self.FrDescrip.grid_columnconfigure(0, weight=1)
        # widgets
        Label(self.FrDescrip, text=txt.get('form_resume')).grid(row=0,
                                                                column=0,
                                                                padx=8,
                                                                pady=8,
                                                                sticky=W)
        self.tex_desc = Text(self.FrDescrip,
                             height=10,
                             wrap=WORD)   # words case

        Label(self.FrDescrip, text=txt.get('form_sourc')).grid(row=2,
                                                               column=0,
                                                               padx=8,
                                                               pady=2,
                                                               sticky=W)
        self.tex_sour = Text(self.FrDescrip, height=2, wrap=WORD)
        # widgets placement
        self.tex_desc.grid(row=1, column=0, columnspan=2,
                           padx=8, pady=8, sticky="NSWE")
        self.tex_sour.grid(row=3, column=0, columnspan=2,
                           padx=8, pady=8, sticky="NSWE")

        # tooltips
        InfoBulle(self.tex_desc, message=txt_help.get(3)[1])
        InfoBulle(self.tex_sour, message=txt_help.get(4)[1])

            ## Frame 3: INSPIRE thematics
        # widgets
        self.lb_insp_orig = Listbox(self.FrThemes, height=10, width=43)
        self.lb_insp_added = Listbox(self.FrThemes, height=10, width=43)

        sb_vinsp1 = Scrollbar(self.FrThemes, command=self.lb_insp_orig.yview)
        sb_vinsp2 = Scrollbar(self.FrThemes, command=self.lb_insp_added.yview)

        x = 0
        for cle in sorted(self.dico_inspire.keys()):
            self.lb_insp_orig.insert(x, cle)
            x = x + 1

        self.lb_insp_orig.configure(yscrollcommand=sb_vinsp1.set)
        self.lb_insp_added.configure(yscrollcommand=sb_vinsp2.set)

        bu_add_inspire = Button(self.FrThemes, text='=>')
        self.lb_icon_inspire = Label(self.FrThemes, image=self.icon_inspire)
        bu_del_inspire = Button(self.FrThemes, text='<=')

        # widgets bind
        self.lb_insp_orig.bind('<Return>', self.add_inspire)
        self.lb_insp_added.bind('<Return>', self.del_inspire)
        self.lb_insp_orig.bind('<Double-1>', self.add_inspire)
        self.lb_insp_added.bind('<Double-1>', self.del_inspire)
        bu_add_inspire.bind('<Button-1>', self.add_inspire)
        bu_del_inspire.bind('<Button-1>', self.del_inspire)

        # widgets placement
        self.lb_insp_orig.grid(row=0, column=0, rowspan=3,
                               padx=8, pady=8, sticky="W")
        sb_vinsp1.grid(row=0, column=0, rowspan=3,
                       padx=0, pady=10, sticky=NE + SE)
        self.lb_insp_added.grid(row=0, column=2, rowspan=3,
                                padx=8, pady=8, sticky=W)
        sb_vinsp2.grid(row=0, column=2, rowspan=3,
                       padx=0, pady=10, sticky=NE + SE)
        bu_add_inspire.grid(row=0, column=1, padx=8, pady=8, sticky=W)
        self.lb_icon_inspire.grid(row=1, column=1, padx=8, pady=8)
        bu_del_inspire.grid(row=2, column=1, padx=8, pady=8, sticky=W)

        # tunning
        self.tunning_listbox(self.lb_insp_orig)

        # tooltips
        InfoBulle(self.lb_insp_orig, message=txt_help.get(5)[1])
        InfoBulle(self.lb_insp_added, message=txt_help.get(5)[1])

            ## Frame 4: thematic keywords
        # widgets
        bu_new_keyw = Button(self.FrKeyword,
                             image=self.icon_new_tag,
                             command=self.add_new_keyword)
        self.ent_keyw = Entry(self.FrKeyword, textvariable=self.new_kword)
        self.ent_keyw.insert(0, txt.get('form_newmtc'))
        self.lb_keyw_orig = Listbox(self.FrKeyword, height=10, width=43)
        self.lb_keyw_added = Listbox(self.FrKeyword, height=10, width=43)
        bu_add_keyw = Button(self.FrKeyword, text='=>')
        bu_del_keyw = Button(self.FrKeyword, text='<=')
        bu_rm_keyw = Button(self.FrKeyword,
                            image=self.icon_del_tag,
                            command=self.kill_keyword)

        # fillfulling the listbox
        x = 0
        for cle in sorted(self.dico_keywords.keys()):
            self.lb_keyw_orig.insert(x, cle)
            x = x + 1

        # scrollbars on listboxes
        sb_vkeyw1 = Scrollbar(self.FrKeyword, command=self.lb_keyw_orig.yview)
        sb_vkeyw2 = Scrollbar(self.FrKeyword, command=self.lb_keyw_added.yview)
        self.lb_keyw_orig.configure(yscrollcommand=sb_vkeyw1.set)
        self.lb_keyw_added.configure(yscrollcommand=sb_vkeyw2.set)

        # tooltips
        InfoBulle(bu_rm_keyw, message=txt.get('form_delmtc'))
        InfoBulle(bu_new_keyw, message=txt.get('form_addmtc'))

        # widgets bind
        self.lb_keyw_orig.bind('<Return>', self.add_keyword)
        self.lb_keyw_added.bind('<Return>', self.del_keyword)
        self.lb_keyw_orig.bind('<Double-1>', self.add_keyword)
        self.lb_keyw_added.bind('<Double-1>', self.del_keyword)
        self.ent_keyw.bind("<Return>", self.add_new_keyword)
        bu_add_keyw.bind('<Button-1>', self.add_keyword)
        bu_del_keyw.bind('<Button-1>', self.del_keyword)

        # widgets positioning
        bu_new_keyw.grid(row=0, column=0, padx=8, pady=8, sticky=W)
        self.ent_keyw.grid(row=0, column=0, columnspan=2,
                           padx=50, pady=0, sticky="EW")
        self.lb_keyw_orig.grid(row=1, column=0, rowspan=3,
                               padx=8, pady=8, sticky=W)
        self.lb_keyw_added.grid(row=1, column=2, rowspan=3,
                                padx=8, pady=8, sticky=W)
        sb_vkeyw1.grid(row=1, column=0, rowspan=3,
                       padx=0, pady=10, sticky=NE + SE)
        sb_vkeyw2.grid(row=1, column=2, rowspan=3,
                       padx=0, pady=10, sticky=NE + SE)
        bu_add_keyw.grid(row=1, column=1, padx=8, pady=8, sticky=W)
        bu_del_keyw.grid(row=3, column=1, padx=8, pady=8, sticky=W)
        bu_rm_keyw.grid(row=2, column=1, padx=8, pady=8, sticky=W + E)

        # tunning
        self.tunning_listbox(self.lb_keyw_orig)

        # tooltips
        InfoBulle(self.lb_keyw_orig, message=txt_help.get(6)[1])
        InfoBulle(self.lb_keyw_added, message=txt_help.get(6)[1])

            ## Frame 5: places keywords
        # widgets
        bu_new_geokeyw = Button(self.FrGeokeyw,
                                image=self.icon_new_tag,
                                command=self.add_new_geokeyword)
        self.lb_geokeyw_orig = Listbox(self.FrGeokeyw, height=10, width=43)
        self.lb_geokeyw_added = Listbox(self.FrGeokeyw, height=10, width=43)
        self.ent_geokeyw = Entry(self.FrGeokeyw, textvariable=self.new_geokword)
        self.ent_geokeyw.insert(0, txt.get('form_newmtc'))
        bu_add_geokeyw = Button(self.FrGeokeyw, text='=>')
        bu_del_geokeyw = Button(self.FrGeokeyw, text='<=')
        bu_rm_geokeyw = Button(self.FrGeokeyw,
                               image=self.icon_del_tag,
                               command=self.kill_geokeyword)

        # fillfulling the listbox
        x = 0
        for cle in sorted(self.dico_geokeywords.keys()):
            self.lb_geokeyw_orig.insert(x, cle)
            x = x + 1

        # scrollbars on listboxes
        sb_vgeokeyw1 = Scrollbar(self.FrGeokeyw,
                                 command=self.lb_geokeyw_orig.yview)
        sb_vgeokeyw2 = Scrollbar(self.FrGeokeyw,
                                 command=self.lb_geokeyw_added.yview)
        self.lb_geokeyw_orig.configure(yscrollcommand=sb_vgeokeyw1.set)
        self.lb_geokeyw_added.configure(yscrollcommand=sb_vgeokeyw2.set)

        # tooltips
        InfoBulle(bu_rm_geokeyw, message=txt.get('form_delmtc'))
        InfoBulle(bu_new_geokeyw, message=txt.get('form_addmtc'))

        # widgets bind
        self.lb_geokeyw_orig.bind('<Return>', self.add_geokeyword)
        self.lb_geokeyw_added.bind('<Return>', self.del_geokeyword)
        self.lb_geokeyw_orig.bind('<Double-1>', self.add_geokeyword)
        self.lb_geokeyw_added.bind('<Double-1>', self.del_geokeyword)
        self.ent_geokeyw.bind("<Return>", self.add_new_geokeyword)
        bu_add_geokeyw.bind('<Button-1>', self.add_geokeyword)
        bu_del_geokeyw.bind('<Button-1>', self.del_geokeyword)

        # widgets positioning
        bu_new_geokeyw.grid(row=0, column=0, padx=8, pady=8, sticky="W")
        self.ent_geokeyw.grid(row=0, column=0, columnspan=2,
                              padx=50, pady=0, sticky="EW")
        self.lb_geokeyw_orig.grid(row=1, column=0, rowspan=3,
                                  padx=8, pady=8, sticky="W")
        self.lb_geokeyw_added.grid(row=1, column=2, rowspan=3,
                                   padx=8, pady=8, sticky="W")
        sb_vgeokeyw1.grid(row=1, column=0, rowspan=3,
                          padx=0, pady=10, sticky=NE + SE)
        sb_vgeokeyw2.grid(row=1, column=2, rowspan=3,
                          padx=0, pady=10, sticky=NE + SE)
        bu_add_geokeyw.grid(row=1, column=1, padx=8, pady=8, sticky="W")
        bu_del_geokeyw.grid(row=3, column=1, padx=8, pady=8, sticky="W")
        bu_rm_geokeyw.grid(row=2, column=1, padx=8, pady=8, sticky="WE")

        # tunning
        self.tunning_listbox(self.lb_geokeyw_orig)

        # tooltips
        InfoBulle(self.lb_geokeyw_orig, message=txt_help.get(7)[1])
        InfoBulle(self.lb_geokeyw_added, message=txt_help.get(7)[1])

            ## Frame 5: others
        # widgets
            # url
        Label(self.FrDivers, text=txt.get('chp_url')).grid(row=0, column=0,
                                                           columnspan=2)

        self.ent_url = Entry(self.FrDivers, textvariable=self.url)
        self.ent_url.insert(0, u'http://')

        Label(self.FrDivers, text=txt.get('form_laburl')).grid(row=0, column=2,
                                                               columnspan=2)
        self.ent_url_label = Entry(self.FrDivers, textvariable=self.url_label)
        self.ent_url_label.insert(0, txt.get('form_exurl'))

            # update rythms
        Label(self.FrDivers, text=txt.get('form_rythm')).grid(row=2, column=0)
        self.ddl_rythm = Combobox(self.FrDivers,
                                  values=self.dico_rythms.keys())

            # data language
        Label(self.FrDivers, text=txt.get('form_langdo')).grid(row=2, column=2)
        self.ddl_lang_data = Combobox(self.FrDivers,
                                      values=self.dico_lang.keys())
            # metadata language
        Label(self.FrDivers, text=txt.get('form_langmd')).grid(row=2, column=3)
        self.ddl_lang_md = Combobox(self.FrDivers,
                                    values=self.dico_lang.keys())
            # scale
        Separator(self.FrDivers, orient=HORIZONTAL)

        # widgets placement
        self.ent_url.grid(row=1, column=0, columnspan=2,
                          padx=5, pady=3, sticky="WE")
        self.ent_url_label.grid(row=1, column=2, columnspan=2,
                                padx=5, pady=3, sticky="WE")
        self.ddl_rythm.grid(row=3, column=0,
                            padx=5, pady=3, sticky="WE")
        self.ddl_lang_data.grid(row=3, column=2,
                                padx=8, pady=3, sticky="WE")
        self.ddl_lang_md.grid(row=3, column=3,
                              padx=8, pady=3, sticky="WE")

        # tooltips
        InfoBulle(self.ent_url, message=txt_help.get(11)[1])
        InfoBulle(self.ent_url_label, message=txt_help.get(12)[1])
        InfoBulle(self.ddl_rythm, message=txt_help.get(15)[1])
        InfoBulle(self.ddl_lang_data, message=txt_help.get(17)[1])
        InfoBulle(self.ddl_lang_md, message=txt_help.get(18)[1])

            ## Frame 6: diffusion rules and conformity
          # specific variables
        self.lic_type = IntVar(self.FrCgu, 1)    # licence type
        # widgets
            # 1st part: license type switcher
        self.lb_icon_diff = Label(self.FrCgu, image=self.icon_diffusion)
        Label(self.FrCgu, text="Opened or not?").grid(row=0, column=0,
                                                      columnspan=2)
        rd_OpenData = Radiobutton(self.FrCgu,
                                  text=txt.get('form_open'),
                                  variable=self.lic_type,
                                  value=1,
                                  command=lambda: self.switch_license(lang=lang))
        rd_ClozData = Radiobutton(self.FrCgu,
                                  text=txt.get('form_close'),
                                  variable=self.lic_type,
                                  value=2,
                                  command=lambda: self.switch_license(lang=lang))

        # placement
        self.lb_icon_diff.grid(row=1, rowspan=3, column=0)
        rd_OpenData.grid(row=1, column=1, sticky="NSW", padx=2, pady=2)
        rd_ClozData.grid(row=2, column=1, sticky="NSW", padx=2, pady=2)
        Separator(master=self.FrCgu, orient=VERTICAL).grid(row=0, rowspan=3,
                                                           column=3, sticky="NSWE",
                                                           padx=5, pady=1)

            # 2nd part: licence/constraints list
        Label(self.FrCgu, text=txt.get('form_diff_pick_licence')).grid(row=0, column=4,
                                                           columnspan=2)
        self.ddl_diff_1 = Combobox(self.FrCgu,
                                   values=self.dico_diffusions.keys(),
                                   style='TCombobox')

        # placement
        self.ddl_diff_1.grid(row=1, column=4,
                             sticky="NSWE", padx=5, pady=1)

        Separator(master=self.FrCgu, orient=VERTICAL).grid(row=0, rowspan=3,
                                                           column=5, sticky="NSWE",
                                                           padx=5, pady=1)

        # 3rd part: INSPIRE constraints
        Label(self.FrCgu, text=txt.get('form_diff_pick_inspire')).grid(row=0, column=6,
                                                                    columnspan=2)
        self.ddl_diff_2 = Combobox(self.FrCgu,
                                   values=self.dico_diffusions.keys(),
                                   style='TCombobox')
        # placement
        self.ddl_diff_2.grid(row=1, column=6,
                             sticky="NSWE", padx=5, pady=1)

        # si ouverte => foutre liste inspire sur "pas de restriction publique" et désactiver 
        #           => ajouter mot-clé donnée ouverte 
        #           => charger liste licences ouvertes (à la place de licences fermées), pointer sur licence open data et laisser actif 
        #           => mettre liste sécurité sur pas de classification sécu et désactiver
        #           => conditions = Utilisation libre sous réserve de mentionner la source

        # si fermée => demander pourquoi ? indiquez une bonne raison !
        #           => liste inspire sans l'option pas de restriction
        #           => charger liste licences fermées (à la place de licences ouvertes) et laisser actif 
        #           => si inspire #2 => charger liste sécurité

        # quand élément sélectionner, afficher résumé dessous
        
        # une liste INSPIRE / code de l'environnement
        # une liste

        # self.ddl_diff_1.grid(row=1, column=1,
        #                    padx=8, pady=3, sticky=W+E)
        # self.ddl_diff_2.grid(row=1, column=2,
        #                    padx=8, pady=3, sticky=W+E)
        # self.ddl_diff.grid(row=3, column=1,
        #                    padx=8, pady=3, sticky=W+E)

        # tooltips
        # InfoBulle(self.ddl_diff, message=txt_help.get(16)[1])

            ## Frame 7: contacts
        # subframes
        self.FrContact_1 = Labelframe(self.FrContact, text=txt.get('ptcontact'))
        self.FrContact_2 = Labelframe(self.FrContact, text=txt.get('cont_resp'))
        self.FrContact_new = Labelframe(self.FrContact, text=txt.get('cont_new'))

        # widgets
            # contacts choosen
        # widgets
        self.ddl_cont1 = Combobox(self.FrContact_1, values=self.dico_contacts.keys())
        Label(self.FrContact_1, text=txt.get('cont_fonc')).grid(row=2, sticky=S)
        self.ddl_func1 = Combobox(self.FrContact_1)
        self.ddl_func1.insert(0, txt.get('ptcontact'))
        self.ddl_func1.config(state=DISABLED)
        self.ddl_cont2 = Combobox(self.FrContact_2, values=self.dico_contacts.keys())
        Label(self.FrContact_2,
              text=txt.get('cont_fonc')).grid(row=2,
                                              columnspan=2,
                                              sticky="S")
        self.ddl_func2 = Combobox(self.FrContact_2, values=self.dico_functions.keys())
        bu_add_contact = Button(self.FrContact_1,
                                text=txt.get('cont_new'),
                                command=lambda: self.new_contact_active())
        bu_del_contact = Button(self.FrContact_1,
                                text=txt.get('cont_del'),
                                command=lambda: self.del_contact())
        # widgets placement
        self.ddl_cont1.grid(row=1, columnspan=2,
                            padx=2, pady=5, sticky=NW + SE)
        bu_add_contact.grid(row=2, column=0,
                            padx=2, pady=5, sticky=NW + SE)
        bu_del_contact.grid(row=2, column=1,
                            padx=2, pady=5, sticky=NW + SE)
        self.ddl_func1.grid(row=4, columnspan=2,
                            padx=2, pady=5, sticky=W + E)
        self.ddl_cont2.grid(row=1, columnspan=2,
                            padx=2, pady=5, sticky=W + E)
        self.ddl_func2.grid(row=3, columnspan=2,
                            padx=2, pady=5, sticky=W + E)

        # new contact
            # labels
        Label(self.FrContact_new,
              text=txt.get('cont_nom'),
              state=DISABLED).grid(row=1, column=0,
                                   padx=2, pady=5,
                                   sticky="NSE")
        Label(self.FrContact_new,
              text=txt.get('cont_orga'),
              state=DISABLED).grid(row=2, column=0,
                                   padx=2, pady=5,
                                   sticky="NSE")
        Label(self.FrContact_new,
              text=txt.get('cont_role'),
              state=DISABLED).grid(row=3, column=0,
                                   padx=2, pady=5,
                                   sticky="NSE")
        Label(self.FrContact_new,
              text=txt.get('cont_tel'),
              state=DISABLED).grid(row=4, column=0,
                                   padx=2, pady=5,
                                   sticky="NSE")
        Label(self.FrContact_new,
              text=txt.get('cont_mail'),
              state=DISABLED).grid(row=5, column=0,
                                   padx=2, pady=5,
                                   sticky="NSE")
        Label(self.FrContact_new,
              text=txt.get('cont_rue'),
              state=DISABLED).grid(row=1, column=2,
                                   padx=2, pady=5,
                                   sticky="NSE")
        Label(self.FrContact_new,
              text=txt.get('cont_ville'),
              state=DISABLED).grid(row=2, column=2,
                                   padx=2, pady=5,
                                   sticky="NSE")
        Label(self.FrContact_new,
              text=txt.get('cont_cp'),
              state=DISABLED).grid(row=3, column=2,
                                   padx=2, pady=5,
                                   sticky="NSE")
        Label(self.FrContact_new,
              text=txt.get('cont_pays'),
              state=DISABLED).grid(row=4, column=2,
                                   padx=2, pady=5,
                                   sticky="NSE")
            # form
        # widgets
        self.new_cont_name = Entry(self.FrContact_new, state=DISABLED)
        self.new_cont_org = Entry(self.FrContact_new, state=DISABLED)
        self.new_cont_role = Entry(self.FrContact_new, state=DISABLED)
        self.new_cont_street = Entry(self.FrContact_new, state=DISABLED)
        self.new_cont_city = Entry(self.FrContact_new, state=DISABLED)
        self.new_cont_cp = Entry(self.FrContact_new, state=DISABLED)
        self.new_cont_country = Entry(self.FrContact_new, state=DISABLED)
        self.new_cont_tel = Entry(self.FrContact_new, state=DISABLED)
        self.new_cont_mail = Entry(self.FrContact_new, state=DISABLED)
        self.bu_cont_create = Button(self.FrContact_new,
                                     text=txt.get('cont_create'),
                                     command=lambda: self.new_contact_add(),
                                     state=DISABLED)
        self.bu_cont_cancel = Button(self.FrContact_new,
                                     text=txt.get('gui_cancel'),
                                     command=lambda: self.new_contact_disable(),
                                     state=DISABLED)

        # widgets placement
        self.new_cont_name.grid(row=1, column=1, padx=2, pady=5, sticky=NW + SE)
        self.new_cont_org.grid(row=2, column=1, padx=2, pady=5, sticky=NW + SE)
        self.new_cont_role.grid(row=3, column=1, padx=2, pady=5, sticky="NSWE")
        self.new_cont_tel.grid(row=4, column=1, padx=2, pady=5, sticky="NSWE")
        self.new_cont_mail.grid(row=5, column=1, padx=2, pady=5, sticky="NSWE")
        self.new_cont_street.grid(row=1, column=3, padx=2, pady=5, sticky="NSWE")
        self.new_cont_city.grid(row=2, column=3, padx=2, pady=5, sticky="NSWE")
        self.new_cont_cp.grid(row=3, column=3, padx=2, pady=5, sticky="NSWE")
        self.new_cont_country.grid(row=4, column=3, padx=2, pady=5, sticky="NSWE")
        self.bu_cont_create.grid(row=5, column=2, padx=2, pady=5, sticky="NSWE")
        self.bu_cont_cancel.grid(row=5, column=3, padx=2, pady=5, sticky="NSWE")

        # subframes placement
        self.FrContact_1.grid(row=0, column=0, padx=8, pady=8, sticky=NW + SE)
        self.FrContact_2.grid(row=1, column=0, padx=8, pady=8, sticky=NW + SE)
        self.FrContact_new.grid(row=0, column=1, rowspan=2,
                                padx=15, pady=8, sticky=NW + SE)

        # tooltips
        InfoBulle(self.ddl_cont1, message=txt_help.get(22)[1])
        InfoBulle(bu_add_contact, message=txt_help.get(23)[1])
        InfoBulle(self.ddl_func1, message=txt_help.get(24)[1])
        InfoBulle(self.ddl_func2, message=txt_help.get(24)[1])

            ## Frame 8: global buttons
        # widgets
        self.FrEndForm.grid_columnconfigure(0, weight=1)
        self.bu_validate = Button(master=self.FrEndForm,
                                  text=txt.get('form_save'),
                                  command=lambda: self.check_form(lang, txt))
        self.bu_cancel = Button(master=self.FrEndForm,
                                text=txt.get('form_back'),
                                command=lambda: self.confirm_exit(txt))

        # widgets positioning
        self.bu_validate.grid(row=0, rowspan=2,
                              column=0, columnspan=2,
                              padx=2, pady=3, sticky="nswe")
        self.bu_cancel.grid(row=0, rowspan=2,
                            column=2, columnspan=1,
                            padx=3, pady=3, sticky="nse")

        # tooltips
        InfoBulle(self.bu_validate, message=txt_help.get(25)[1])
        InfoBulle(self.bu_cancel, message=txt_help.get(26)[1])

            ## Main configuration
        # frames placement
        self.FrMain.grid(row=0, column=0, padx=0, pady=8, sticky="NSWE")
        self.FrDescrip.grid(row=1, column=0, padx=0, pady=8, sticky="NSWE")
        self.FrThemes.grid(row=2, column=0, padx=0, pady=8, sticky="NSWE")
        self.FrKeyword.grid(row=3, column=0, padx=0, pady=8, sticky="NSWE")
        self.FrGeokeyw.grid(row=4, column=0, padx=0, pady=8, sticky="NSWE")
        self.FrDivers.grid(row=5, column=0, padx=0, pady=8, sticky="NSWE")
        self.FrCgu.grid(row=6, column=0, padx=0, pady=8, sticky="NSWE")
        self.FrContact.grid(row=7, column=0, padx=0, pady=8, sticky="NSWE")
        self.FrEndForm.grid(row=8, column=0, padx=0, pady=8, sticky="NSWE")

        # final canvas configuration
        self.c_main.create_window(0, 0, window=self.form)
        self.form.update_idletasks()
        self.c_main.config(scrollregion=self.c_main.bbox("all"))
        self.c_main.yview_moveto(0)
        self.c_main.xview_moveto(0)

    ###########################################################################
    ###################### Methods: GUI #######################################
    ###########################################################################

    def alter_state(self, parent, new_state):
        """
        Easily switch  the state of  all children widgets
        inside a parent class

        parent = Tkinter class with children (Frame, Labelframe, Tk, etc.)
        new_state = Tkinter keyword for widget state (ACTIVE, NORMAL, DISABLED)
        """
        for child in parent.winfo_children():
            child.configure(state=new_state)
        # end of function
        return parent, new_state

    def confirm_exit(self, text):
        """ little popup which avoids an unexpected closing action """
        if okno(title=text.get('form_alert_cancel1'),
                message=text.get('form_alert_cancel2')):
            self.destroy()
        # end of function
        return

    def mouse_wheel(self, event):
        """ move the scrollbar according to the mouse wheel """
        # respond to Linux or Windows wheel event
        try:
            if event.num == 5 or event.delta == -120:
                dir = 1
            elif event.num == 4 or event.delta == 120:
                dir = -1
            self.c_main.yview_scroll(dir, 'units')
        except UnboundLocalError:
            pass
        # end of function
        return self.c_main.yview

    def switch_license(self, lang):
        u""" switch between the available types of data (files or database) """
        if self.lic_type.get() == 1:
            self.recup_diffusion(lang, 1)

        elif self.lic_type.get() == 2:
            self.recup_diffusion(lang, 0)

        # End of function
        print self.dico_diffusions
        self.ddl_diff_1.configure(values= self.dico_diffusions.keys())
        return self.lic_type

    def switch_sub_ddl(self, event):
        """ set the sub dropdownlist values according to the selected value """
        if event.widget.get() == 'yes':
            self.ddl_diff_2["values"] = ['open', 'your', 'mind']
        elif event.widget.get() == 'no':
            self.ddl_diff_2["values"] = ['limited', 'restricted', 'security']
        # end of function
        return

    def tunning_listbox(self, listbox):
        """ alternate lines background color of the listbox """
        for i in range(0, len(listbox.get(0, END)), 2):
            listbox.itemconfigure(i, background='#f0f0ff')
        # end of function
        return listbox

    ###########################################################################
    ###################### Methods: gathering #################################
    ###########################################################################

    def import_profile(self, lang, txt):
        """ import and insert informations from an existing profile """
        # getting all widgets from the GUI
        li_widgets = self.FrMain.winfo_children() +\
                     self.FrDescrip.winfo_children() +\
                     self.FrCgu.winfo_children() +\
                     self.FrKeyword.winfo_children() +\
                     self.FrDivers.winfo_children() +\
                     self.FrThemes.winfo_children()
        ## clean up
        # reset all widgets
        for child in li_widgets:
            if child.winfo_class() == 'TEntry' or child.winfo_class() == 'Entry':  # filter for Entry
                child.delete(0, END)
            elif child.winfo_class() == 'Text':     # filter for Text
                child.delete(1.0, END)
            elif child.winfo_class() == 'Listbox':  # filter for Listbox
                child.delete(0, END)
        # putting back the default information
        x = 0
        for cle in self.dico_inspire.keys():
            self.lb_insp_orig.insert(x, cle)
            x = x + 1
        x = 0
        for cle in self.dico_keywords.keys():
            self.lb_keyw_orig.insert(x, cle)
            x = x + 1

        # getting the information from the profile selected
        if self.ddl_prof.get() != txt.get('tab1_new'):
            dico_profil = self.recup_profil(self.ddl_prof.get(), lang)
        else:
            return

        ## inserting new data
        # profile name
        self.ent_name.insert(0, self.ddl_prof.get())
        # descriptive data
        self.tex_desc.insert(1.0, dico_profil.get('description'))
        self.tex_sour.insert(1.0, dico_profil.get('sources'))
        # INSPIRE
        for theme in dico_profil[u'themesinspire']:
            self.lb_insp_orig.selection_clear(0, END)
            self.lb_insp_orig.selection_set(self.lb_insp_orig.get(0, END).index(theme))
            self.add_inspire()
        # custom keywords
        for keyword in dico_profil[u'keywords']:
            self.lb_keyw_orig.selection_clear(0, END)
            self.lb_keyw_orig.selection_set(self.lb_keyw_orig.get(0, END).index(keyword))
            self.add_keyword()
        # places keywords
        for geokeyword in dico_profil[u'geokeywords']:
            self.lb_geokeyw_orig.selection_clear(0, END)
            self.lb_geokeyw_orig.selection_set(self.lb_geokeyw_orig.get(0, END).index(geokeyword))
            self.add_geokeyword()
        # miscellanous
        self.ent_url.insert(0, dico_profil.get('url'))
        self.ent_url_label.insert(0, dico_profil.get('url_label'))
        self.ddl_lang_data.current(self.dico_lang.keys().index(dico_profil['lang_data']))
        self.ddl_lang_md.current(self.dico_lang.keys().index(dico_profil['lang_md']))
        self.ddl_rythm.current(self.dico_rythms.keys().index(dico_profil['rythm']))
        self.ddl_diff.current(self.dico_diffusions.keys().index(dico_profil['diffusion']))
        # contacts
        self.ddl_cont1.current(self.dico_contacts.keys().index(dico_profil['cont_name']))
        self.ddl_cont2.current(self.dico_contacts.keys().index(dico_profil['resp_name']))
        self.ddl_func2.current(self.dico_functions.keys().index(dico_profil['resp_func']))

        # tunning the listboxes
        self.tunning_listbox(self.lb_insp_orig)
        self.tunning_listbox(self.lb_insp_added)
        self.tunning_listbox(self.lb_keyw_orig)
        self.tunning_listbox(self.lb_keyw_added)

        # end of function
        return

    def recup_contacts(self, lang):
        """ gathers data from adress book"""
        # specific path to xml file
        path_contacts = 'locale/{0}/contacts_{0}.xml'.format(lang)
        # reading and parsing the xml
        with open(path_contacts, 'r') as source:
            xml = ET.parse(source)                  # xml cursor
            for contact in xml.findall('contact'):
                name = contact.find(u'name').text
                org = contact.find(u'org').text
                role = contact.find(u'role').text
                street = contact.find(u'street').text
                city = contact.find(u'city').text
                cp = contact.find(u'cp').text
                country = contact.find(u'country').text
                tel = contact.find(u'tel').text
                mail = contact.find(u'mail').text
                # fillfulling the contacts dictionary
                self.dico_contacts[name] = org, role, street, city, cp, country, tel, mail
        # End of function
        return self.dico_contacts

    def recup_diffusion(self, lang, opened=1):
        """ get the diffusion rules """
        # specific path to xml file
        path_diff = 'locale/{0}/inspire/diffusion_{0}.xml'.format(lang)
        self.dico_diffusions.clear()
        # reading and parsing the xml
        with open(path_diff, 'r') as source:
            xml = ET.parse(source)  # xml cursor
            if opened == 1:
                xml = xml.find('opened')
                for diff in xml.findall('licence'):
                    name = diff.find('name').text
                    typo = diff.find('type').text
                    descr = diff.find('description').text
                    norm = diff.find('norm').text
                    doc = diff.find('doc').text
                    # fillfulling the diffusion dictionary
                    self.dico_diffusions[name] = typo, descr, norm, doc
            elif opened == 0:
                xml = xml.find('closed')
                print xml
                for diff in xml.findall('restriction'):
                    name = diff.find('name').text
                    typo = diff.find('type').text
                    descr = diff.find('description').text
                    norm = diff.find('norm').text
                    doc = diff.find('doc').text
                    # fillfulling the diffusion dictionary
                    self.dico_diffusions[name] = typo, descr, norm, doc

        # setting dropdown values
        # self.ddl_diff.config(values = self.dico_diffusions.keys())
        # End of function
        return self.dico_diffusions

    def recup_fonctions(self, lang):
        """ get the INSPIRE functions """
        # specific path to xml file
        path_fonctions = 'locale/{0}/inspire/fonctions_{0}.xml'.format(lang)
        # reading and parsing the xml
        with open(path_fonctions, 'r') as source:
            xml = ET.parse(source)                  # xml cursor
            for func in xml.findall('fonction'):
                name=func.find('name').text
                trad = func.find('norm').text
                # fillfulling the INSPIRE dictionary
                self.dico_functions[name] = trad
        # End of function
        return self.dico_functions

    def recup_geo_keywords(self, lang):
        """ get the user'places keywords """
        # specific path to xml file
        path_keywords = 'locale/{0}/geokeywords_{0}.xml'.format(lang)
        # reading and parsing the xml
        with open(path_keywords, 'r') as source:
            xml = ET.parse(source)                  # xml cursor
            for theme in xml.findall('geokeyword'):
                name = theme.find('name').text
                descr = theme.find('description').text
                # fillfulling the INSPIRE dictionary
                self.dico_geokeywords[name] = descr
        # End of function
        return self.dico_geokeywords

    def recup_keywords(self, lang):
        """ get the user's keywords """
        # specific path to xml file
        path_keywords = 'locale/{0}/keywords_{0}.xml'.format(lang)
        # reading and parsing the xml
        with open(path_keywords, 'r') as source:
            xml = ET.parse(source)                  # xml cursor
            for theme in xml.findall('keyword'):
                name = theme.find('name').text
                descr = theme.find('description').text
                # fillfulling the INSPIRE dictionary
                self.dico_keywords[name] = descr
        # End of function
        return self.dico_keywords

    def recup_lang_ISO(self):
        """ """
        # specific path to xml file
        path_lang = 'data/xml/languages.xml'
        # reading and parsing the xml
        with open(path_lang, 'r') as source:
            xml = ET.parse(source)                  # xml cursor
            for language in xml.findall('language'):
                name = language.find('name').text
                prefix2 = language.find('prefix2').text
                prefix3 = language.find('prefix3').text
                # fillfulling the INSPIRE dictionary
                self.dico_lang[name] = prefix2, prefix3
        # End of function
        return self.dico_lang

    def recup_profil(self, profil, lang):
        """ get the information from the profile selected """
        # clearing the profile dictionary
        dico_profil = OD()
        # specific path to profile file
        path_profile = path.join('locale/{0}/profiles/{1}'.format(lang, profil + ".xml"))
        with open(path_profile, 'r') as profile:
            # open xml parser
            xml = ET.parse(profile)
            # basic informations
            dico_profil['description'] = xml.find('description').text    # description
            dico_profil['sources'] = xml.find('sources').text            # sources
            dico_profil['url'] = xml.find('url').text           # URL
            dico_profil['url_label'] = xml.find('url_label').text      # nom lien
            dico_profil[u'diffusion'] = xml.find('diffusion').text       # diffusion
            # data language
            lang_data = xml.find(u'lang_data')
            dico_profil[u"lang_data"] = lang_data.find(u'name').text
            # metadata language
            lang_metad = xml.find(u'lang_metad')
            dico_profil[u"lang_md"] = lang_metad.find(u'name').text
            # diffusion constraints
            diff = xml.find(u'diffusion')
            dico_profil['diffusion'] = diff.find(u'name').text
            # update rythm
            rythm = xml.find(u'rythm')
            dico_profil['rythm'] = rythm.find(u'name').text
            # INSPIRE themes
            themes = xml.find('themesinspire')
            li_themesinspire = [theme.find('name').text for theme in themes.findall('theme')]
            dico_profil['themesinspire'] = li_themesinspire
            # custom keywords
            keywords = xml.find('keywords')
            li_keywords = [keyword.find('name').text for keyword in keywords.findall('keyword')]
            dico_profil['keywords'] = li_keywords
            # places keywords
            geokeywords = xml.find('geokeywords')
            li_geokeywords = [geokeyword.find('name').text for geokeyword in geokeywords.findall('geokeyword')]
            dico_profil['geokeywords'] = li_geokeywords
            # contacts
            contacts = xml.find(u'contacts')
            # point of contact
            cont = contacts.find(u'pointdecontact')
            dico_profil[u'cont_name'] = cont.find(u'name').text
            dico_profil[u'cont_orga'] = cont.find(u'org').text
            dico_profil[u'cont_mail'] = cont.find(u'mail').text
            dico_profil[u'cont_role'] = cont.find(u'role').text
            dico_profil[u'cont_func'] = cont.find(u'func')[0].text
            dico_profil[u'cont_street'] = cont.find(u'street').text
            dico_profil[u'cont_city'] = cont.find(u'city').text
            dico_profil[u'cont_cp'] = cont.find(u'cp').text
            dico_profil[u'cont_country'] = cont.find(u'country').text
            dico_profil[u'cont_phone'] = cont.find(u'tel').text
            # second contact (responsable, etc.)
            resp = contacts.find(u'second_contact')
            dico_profil[u'resp_name'] = resp.find(u'name').text
            dico_profil[u'resp_orga'] = resp.find(u'org').text
            dico_profil[u'resp_mail'] = resp.find(u'mail').text
            dico_profil[u'resp_role'] = resp.find(u'role').text
            dico_profil[u'resp_func'] = resp.find(u'func')[0].text
            dico_profil[u'resp_street'] = resp.find(u'street').text
            dico_profil[u'resp_city'] = resp.find(u'city').text
            dico_profil[u'resp_cp'] = resp.find(u'cp').text
            dico_profil[u'resp_country'] = resp.find(u'country').text
            dico_profil[u'resp_phone'] = resp.find(u'tel').text
        # End of function
        return dico_profil

    def recup_rythms(self, lang):
        """ get the update categories """
        # specific path to xml file
        path_rythm = 'locale/{0}/inspire/rythmes_{0}.xml'.format(lang)
        # reading and parsing the xml
        with open(path_rythm, 'r') as source:
            xml = ET.parse(source)                  # xml cursor
            for rythm in xml.findall('rythme'):
                name = rythm.find('name').text
                trad = rythm.find('norm').text
                # fillfulling the INSPIRE dictionary
                self.dico_rythms[name] = trad
        # End of function
        return self.dico_rythms

    def recup_specifications(self, lang):
        """ """
        print 'rythmes ISO'

    def recup_themes_INSPIRE(self, lang):
        """ get the INSPIRE thematics """
        # specific path to xml file
        path_inspire = 'locale/{0}/inspire/themes_inspire_{0}.xml'.format(lang)
        # reading and parsing the xml
        with open(path_inspire, 'r') as source:
            xml = ET.parse(source)                  # xml cursor
            for theme in xml.findall('keyword'):
                name=theme.find('intitule').text
                trad = theme.find('traduction').text
                descr = theme.find('description').text
                # fillfulling the INSPIRE dictionary
                self.dico_inspire[name] = trad, descr
        # End of function
        return self.dico_inspire

    def recup_themes_ISO(self, lang):
        """ get the ISO thematics """
        print 'themes ISO'

    ###########################################################################
    ###################### Methods: saving & closing ##########################
    ###########################################################################

    def check_form(self, lang, txt):
        """ check if all fields are correctly fillfulled """
        li_bad_fields = []
        # description
        if self.tex_desc.get(1.0, END) == '\n':
            self.tex_desc.config(bg='red')
            li_bad_fields.append(txt.get('form_resume'))
        else:
            self.tex_desc.config(bg='green')
        # sources
        if self.tex_sour.get(1.0, END) == '\n':
            self.tex_sour.config(bg='red')
            li_bad_fields.append(txt.get('form_sourc'))
        else:
            self.tex_sour.config(bg='green')
        # inspire
        if self.lb_insp_added.get(0, END) == ():
            self.lb_insp_added.config(bg='red')
            li_bad_fields.append(txt.get('chp_inspire'))
        else:
            self.lb_insp_added.config(bg='green')
        # thematic keywords
        if self.lb_keyw_added.get(0, END) == ():
            self.lb_keyw_added.config(bg='red')
            li_bad_fields.append(txt.get('mtcthem'))
        else:
            self.lb_keyw_added.config(bg='green')
        # places keywords
        if self.lb_geokeyw_added.get(0, END) == ():
            self.lb_geokeyw_added.config(bg='red')
            li_bad_fields.append(txt.get('mtcgeo'))
        else:
            self.lb_geokeyw_added.config(bg='green')
        # url
        if self.url.get() == '':
            self.ent_url.configure(background='red')
            li_bad_fields.append(txt.get('chp_url'))
        else:
            self.ent_url.configure(background='green')
        # url label
        if self.url_label.get() == '':
            self.ent_url_label.configure(background='red')
            li_bad_fields.append(txt.get('form_laburl'))
        else:
            self.ent_url_label.configure(background='green')
        # diffusion
        # if self.ddl_diff.get() == '':
        # ##            self.style.configure('C.TCombobox',  background='red')
        #             li_bad_fields.append(txt.get('diffusion'))
        #         else:
        # ##            self.style.configure('TCombobox',  background='green')
        #             pass
        # rythms
        if self.ddl_rythm.get() == '':
            li_bad_fields.append(txt.get('form_rythm'))
        else:
            pass
        # data language
        if self.ddl_lang_data.get() == '':
            li_bad_fields.append(txt.get('form_langdo'))
        else:
            pass
        # metadata language
        if self.ddl_lang_md.get() == '':
            li_bad_fields.append(txt.get('form_langmd'))
        else:
            pass
        # 1st contact
        if self.ddl_cont1.get() == '':
            li_bad_fields.append(txt.get('ptcontact'))
        else:
            pass
        # 2nd contact
        if self.ddl_cont2.get() == '':
            li_bad_fields.append(txt.get('cont_resp'))
        else:
            pass
        # 2nd contact function
        if self.ddl_func2.get() == '':
            li_bad_fields.append(txt.get('cont_fonc'))
        else:
            pass
        # final check: time to count!
        if li_bad_fields:
            avert(title=u'{} error(s)'.format(len(li_bad_fields)),
                  message=txt.get(u'check_err') + u'\n' + '\n'.join(li_bad_fields))
            return
        else:
            self.create_profile(lang, txt)
        # end of function
        return li_bad_fields

    def create_profile(self, lang, txt):
        """ transform the form into a profile (.xml)  """
        output_name = "%s_%s.xml" % (date.today(), self.new_name.get())
        # new xml structure
        elem = ET.Element(u"profil")
        # adding basics sub elements
        sub_descr = ET.SubElement(elem, u"description")  # description
        sub_descr.text = self.tex_desc.get(1.0, END).rstrip()
        sub_source = ET.SubElement(elem, u"sources")    # sources
        sub_source.text = self.tex_sour.get(1.0, END).rstrip()
        # adding INSPIRE themes
        sub_theminspire = ET.SubElement(elem, u"themesinspire")
        for theme in self.lb_insp_added.get(0, END):
            insp = ET.SubElement(sub_theminspire, u"theme")
            insp_name = ET.SubElement(insp, u"name")
            insp_name.text = theme
            insp_trad = ET.SubElement(insp, u"norm")
            insp_trad.text = self.dico_inspire.get(theme)[0]
            insp_descr = ET.SubElement(insp, u"description")
            insp_descr.text = self.dico_inspire.get(theme)[1]
        # adding custom keywords
        sub_motscles = ET.SubElement(elem, u"keywords")
        for keyword in self.lb_keyw_added.get(0, END):
            key = ET.SubElement(sub_motscles, u"keyword")
            key_name = ET.SubElement(key, u"name")
            key_name.text = keyword
            key_descr = ET.SubElement(key, u"description")
            key_descr.text = self.dico_keywords.get(keyword)
        # adding places keywords
        sub_mtcgeo = ET.SubElement(elem, u"geokeywords")
        for geokeyword in self.lb_geokeyw_added.get(0, END):
            key = ET.SubElement(sub_mtcgeo, u"geokeyword")
            key_name = ET.SubElement(key, u"name")
            key_name.text = geokeyword
            key_descr = ET.SubElement(key, u"description")
            key_descr.text = self.dico_geokeywords.get(geokeyword)
        # adding the URL and its label
        sub_lien = ET.SubElement(elem, u"url")
        sub_lien.text = self.ent_url.get()
        sub_lien_intit = ET.SubElement(elem, u"url_label")
        sub_lien_intit.text = self.url_label.get()
        # adding update rythm
        sub_rythme = ET.SubElement(elem, u"rythm")
        rythme_name = ET.SubElement(sub_rythme, u"name")
        rythme_name.text = self.ddl_rythm.get()
        rythme_trad = ET.SubElement(sub_rythme, u"norm")
        rythme_trad.text = self.dico_rythms[self.ddl_rythm.get()]
        # adding diffusion
        sub_diffusion = ET.SubElement(elem, u"diffusion")
        diffusion_name = ET.SubElement(sub_diffusion, u"name")
        diffusion_name.text = self.ddl_diff.get()
        diffusion_trad = ET.SubElement(sub_diffusion, u"norm")
        diffusion_trad.text = self.dico_diffusions[self.ddl_diff.get()]
        # adding language of data
        sub_langda = ET.SubElement(elem, u"lang_data")
        langda_name = ET.SubElement(sub_langda, u"name")
        langda_name.text = self.ddl_lang_data.get()
        langda_pref = ET.SubElement(sub_langda, u"prefix3")
        langda_pref.text = self.dico_lang.get(self.ddl_lang_data.get())[1]
        # adding language of metadata
        sub_langmd = ET.SubElement(elem, u"lang_metad")
        langmd_name = ET.SubElement(sub_langmd, u"name")
        langmd_name.text = self.ddl_lang_md.get()
        langmd_pref = ET.SubElement(sub_langmd, u"prefix3")
        langmd_pref.text = self.dico_lang.get(self.ddl_lang_md.get())[1]
        # Contacts
        sub_contact = ET.SubElement(elem, u"contacts")
        contact_1 = self.dico_contacts.get(self.ddl_cont1.get())
        contact_2 = self.dico_contacts.get(self.ddl_cont2.get())
        # Point of contact
        sub_ptcontact = ET.SubElement(sub_contact, u'pointdecontact')
        cont_pt_name = ET.SubElement(sub_ptcontact, u'name')
        cont_pt_name.text = self.ddl_cont1.get()
        cont_pt_orga = ET.SubElement(sub_ptcontact, u'org')
        cont_pt_orga.text = contact_1[0]
        cont_pt_role = ET.SubElement(sub_ptcontact, u'role')
        cont_pt_role.text = contact_1[1]
        cont_pt_rue = ET.SubElement(sub_ptcontact, u'street')
        cont_pt_rue.text = contact_1[2]
        cont_pt_ville = ET.SubElement(sub_ptcontact, u'city')
        cont_pt_ville.text = contact_1[3]
        cont_pt_cp = ET.SubElement(sub_ptcontact, u'cp')
        cont_pt_cp.text = contact_1[4]
        cont_pt_pays = ET.SubElement(sub_ptcontact, u'country')
        cont_pt_pays.text = contact_1[5]
        cont_pt_tel = ET.SubElement(sub_ptcontact, u'tel')
        cont_pt_tel.text = contact_1[6]
        cont_pt_mail = ET.SubElement(sub_ptcontact, u'mail')
        cont_pt_mail.text = contact_1[7]
        cont_pt_fonction = ET.SubElement(sub_ptcontact, u'func')
        cont_pt_fonction_name = ET.SubElement(cont_pt_fonction, u'name')
        cont_pt_fonction_name.text = txt.get('ptcontact')
        cont_pt_fonction_trad = ET.SubElement(cont_pt_fonction, u'norm')
        cont_pt_fonction_trad.text = self.dico_functions.get(txt.get('ptcontact'))

        # 2nd contact
        sub_ptcontact = ET.SubElement(sub_contact, u'second_contact')
        cont_pt_name = ET.SubElement(sub_ptcontact, u'name')
        cont_pt_name.text = self.ddl_cont2.get()
        cont_pt_orga = ET.SubElement(sub_ptcontact, u'org')
        cont_pt_orga.text = contact_2[0]
        cont_pt_role = ET.SubElement(sub_ptcontact, u'role')
        cont_pt_role.text = contact_2[1]
        cont_pt_rue = ET.SubElement(sub_ptcontact, u'street')
        cont_pt_rue.text = contact_2[2]
        cont_pt_ville = ET.SubElement(sub_ptcontact, u'city')
        cont_pt_ville.text = contact_2[3]
        cont_pt_cp = ET.SubElement(sub_ptcontact, u'cp')
        cont_pt_cp.text = contact_2[4]
        cont_pt_pays = ET.SubElement(sub_ptcontact, u'country')
        cont_pt_pays.text = contact_2[5]
        cont_pt_tel = ET.SubElement(sub_ptcontact, u'tel')
        cont_pt_tel.text = contact_2[6]
        cont_pt_mail = ET.SubElement(sub_ptcontact, u'mail')
        cont_pt_mail.text = contact_2[7]
        cont_pt_fonction = ET.SubElement(sub_ptcontact, u'func')
        cont_pt_fonction_name = ET.SubElement(cont_pt_fonction, u'name')
        cont_pt_fonction_name.text = self.ddl_func2.get()
        cont_pt_fonction_trad = ET.SubElement(cont_pt_fonction, u'norm')
        cont_pt_fonction_trad.text = self.dico_functions.get(self.ddl_func2.get())

        # finalization of XML tree structure
        final_profile = path.join('locale/', '%s/profiles/%s') % (lang, output_name)
        profile = ET.ElementTree(elem)    # finalisation de la structure xml
        # test s'il existe déjà un fichier de profil avec le même name
        if path.isfile(final_profile):
            if not okno(title=txt.get('prof_exist'),
                        message=txt.get('prof_exist2')):
                output_name = output_name[0:-4] + '_1' + '.xml'
                final_profile = path.join('locale/', '{0}/profiles/{1}'.format(lang, output_name))
        # writing the xml file
        profile.write(final_profile,
                      encoding='utf-8',
                      method="xml",
                      xml_declaration='version="1.0"')

        # save contacts
        self.save_contacts(lang)
        # save keywords
        self.save_keywords(lang, txt)
        self.save_geokeywords(lang, txt)

        # updating

        # killing the whole interface
        self.destroy()

        # end of function
        return final_profile

    def save_contacts(self, lang):
        """ write the contacts dictionary into the xml """
        # specific path to xml file
        path_contacts = 'locale/%s/contacts_%s.xml' % (lang, lang)
        # parsing and writing
        contacts = ET.Element(u'contacts')
        with open(path_contacts, 'wb') as xml_contacts:
            for ct in self.dico_contacts.keys():
                contact = ET.SubElement(contacts, u'contact')
                contact_name = ET.SubElement(contact, u'name')
                contact_name.text = ct
                contact_org = ET.SubElement(contact, u'org')
                contact_org.text = self.dico_contacts.get(ct)[0]
                contact_role = ET.SubElement(contact, u'role')
                contact_role.text = self.dico_contacts.get(ct)[1]
                contact_street = ET.SubElement(contact, u'street')
                contact_street.text = self.dico_contacts.get(ct)[2]
                contact_city = ET.SubElement(contact, u'city')
                contact_city.text = self.dico_contacts.get(ct)[3]
                contact_cp = ET.SubElement(contact, u'cp')
                contact_cp.text = self.dico_contacts.get(ct)[4]
                contact_country = ET.SubElement(contact, u'country')
                contact_country.text = self.dico_contacts.get(ct)[5]
                contact_tel = ET.SubElement(contact, u'tel')
                contact_tel.text = self.dico_contacts.get(ct)[6]
                contact_mail = ET.SubElement(contact, u'mail')
                contact_mail.text = self.dico_contacts.get(ct)[7]
            # creating the xml tree structure
            xml_contacts = ET.ElementTree(contacts)
            # remplacement du xml des contacts
            xml_contacts.write(path_contacts,
                               encoding='utf-8',
                               xml_declaration='version="1.0"',
                               method='xml')
        # end of function
        return xml_contacts

    def save_geokeywords(self, lang, text):
        """ write the user'keywords """
        # specific path to xml file
        path_geokeywords = 'locale/%s/geokeywords_%s.xml' % (lang, lang)
        # parsing and writing
        geokeywords = ET.Element(u'places')
        with open(path_geokeywords, 'wb') as xml_geokeywords:
            for geokeyw in self.dico_geokeywords.keys():
                geokeyword = ET.SubElement(geokeywords, u'geokeyword')
                geokeyword_name=ET.SubElement(geokeyword, u'name')
                geokeyword_name.text = geokeyw
                geokeyword_descript = ET.SubElement(geokeyword, u'description')
                geokeyword_descript.text = self.dico_geokeywords.get(geokeyw)
            # creating the xml tree structure
            xml_geokeywords = ET.ElementTree(geokeywords)
            # saving the xml output
            xml_geokeywords.write(path_geokeywords,
                                  encoding='utf-8',
                                  xml_declaration='version="1.0"',
                                  method='xml')
        # end of function
        return xml_geokeywords

    def save_keywords(self, lang, text):
        """ write the user'keywords """
        # specific path to xml file
        path_keywords = 'locale/%s/keywords_%s.xml' % (lang, lang)
        # parsing and writing
        keywords = ET.Element(u'keywords')
        with open(path_keywords, 'wb') as xml_keywords:
            for kw in self.dico_keywords.keys():
                keyword = ET.SubElement(keywords, u'keyword')
                keyword_name = ET.SubElement(keyword, u'name')
                keyword_name.text = kw
                keyword_descript = ET.SubElement(keyword, u'description')
                keyword_descript.text = self.dico_keywords.get(kw)
            # creating the xml tree structure
            xml_keywords = ET.ElementTree(keywords)
            # saving the xml output
            xml_keywords.write(path_keywords,
                               encoding='utf-8',
                               xml_declaration='version="1.0"',
                               method='xml')
        # end of function
        return xml_keywords

    ###########################################################################
    ###################### Methods: contacts form #############################
    ###########################################################################

    def new_contact_active(self):
        """ active the form to create a new contact """
        # active the form widgets
        self.alter_state(self.FrContact_new, NORMAL)
        # disable the others widgets to avoid potential conflicts
        self.alter_state(self.FrContact_1, DISABLED)
        self.alter_state(self.FrContact_2, DISABLED)
        # update contacts dictionary and dropdown lists

        # end of function
        return self.FrContact_1, self.FrContact_2, self.FrContact_new

    def new_contact_disable(self):
        """ active the form to create a new contact """
        # reset the Entry widgets
        for child in self.FrContact_new.winfo_children():
            if child.winfo_class() == 'TEntry':     # filter for Entry instances
                child.delete(0, END)
        # disable all the form widgets
        self.alter_state(self.FrContact_new, DISABLED)
        # disable the others widgets to avoid potential conflicts
        self.alter_state(self.FrContact_1, ACTIVE)
        self.alter_state(self.FrContact_2, ACTIVE)
        self.ddl_func1.config(state=DISABLED)  # except for this dropdown list
        # end of function
        return self.FrContact_1, self.FrContact_2, self.FrContact_new

    def new_contact_add(self):
        """ check and create a new contact """
        # checking the Entries
        for child in self.FrContact_new.winfo_children():
            if child.winfo_class() == 'TEntry' and child.get() == '':
                child.configure(state='INVALID')
                avert(message='error form')
                break

        # add the new contact to the dictionary
        self.dico_contacts[self.new_cont_name.get()] = self.new_cont_org.get(),\
                                                       self.new_cont_role.get(),\
                                                       self.new_cont_street.get(),\
                                                       self.new_cont_city.get(),\
                                                       self.new_cont_cp.get(),\
                                                       self.new_cont_country.get(),\
                                                       self.new_cont_tel.get(),\
                                                       self.new_cont_mail.get()
        # update the dropdown lists
        self.ddl_cont1['values'] = self.dico_contacts.keys()
        self.ddl_cont2['values'] = self.dico_contacts.keys()

        # reactive/disable
        self.new_contact_disable()
        # end of function
        return self.FrContact_1, self.FrContact_2, self.FrContact_new

    def del_contact(self):
        """ remove the selected contact from the dictionary """
        self.dico_contacts.pop(self.ddl_cont1.get())
        # update the dropdown lists
        self.ddl_cont1['values'] = self.dico_contacts.keys()
        self.ddl_cont2['values'] = self.dico_contacts.keys()
        self.ddl_cont1.delete(0, END)
        # end of function
        return self.dico_contacts

    ###########################################################################
    ###################### Methods: INSPIRE ###################################
    ###########################################################################

    def add_inspire(self, event='event'):
        """ add the selected theme from INSPIRE orig Listbox """
        # insertion
        self.lb_insp_added.insert(0, self.lb_insp_orig.get(self.lb_insp_orig.curselection()))
        # deletion
        self.lb_insp_orig.delete(self.lb_insp_orig.index(self.lb_insp_orig.curselection()))
        # auto-selection of the next one
        self.lb_insp_orig.selection_set(0)
        # tunning
        self.tunning_listbox(self.lb_insp_added)
        # End of function
        return event, self.lb_insp_added, self.lb_insp_orig

    def del_inspire(self, event='event'):
        """ del the selected theme from INSPIRE added Listbox """
        # insertion
        self.lb_insp_orig.insert(0, self.lb_insp_added.get(self.lb_insp_added.curselection()))
        # deletion
        self.lb_insp_added.delete(self.lb_insp_added.index(self.lb_insp_added.curselection()))
        # auto-selection of the next one
        self.lb_insp_added.selection_set(0)
        # tunning
        self.tunning_listbox(self.lb_insp_orig)
        # End of function
        return event, self.lb_insp_added, self.lb_insp_orig

    ###########################################################################
    ###################### Methods: keywords ##################################
    ###########################################################################

    def add_keyword(self, event='event'):
        """ add the selected keyword from keywords orig Listbox """
        # insertion
        self.lb_keyw_added.insert(0, self.lb_keyw_orig.get(self.lb_keyw_orig.curselection()))
        # deletion
        self.lb_keyw_orig.delete(self.lb_keyw_orig.index(self.lb_keyw_orig.curselection()))
        # auto-selection of the next one
        self.lb_keyw_orig.selection_set(0)
        # End of function
        return event, self.lb_keyw_added, self.lb_keyw_orig

    def add_new_keyword(self, event='event'):
        """ add the new keyword to the list """
        # test if the new keyword not already exists
        if self.ent_keyw.get() not in self.lb_keyw_added.get(0, END) and self.ent_keyw.get() != "":
            self.lb_keyw_added.insert(0, self.ent_keyw.get())
            self.dico_keywords[self.ent_keyw.get()] = 'former description'
        else:
            print "already exists"
        ## avert(title = txt.get('mtc_exist'),
        ## message=txt.get('mtc_exist2'))
        # reset the fields
        self.ent_keyw.delete(0, END)
        self.ent_keyw.delete(0, END)
        # end of function
        return self.ent_keyw

    def del_keyword(self, event='event'):
        """ del the selected keyword from keywords added Listbox """
        # insertion
        self.lb_keyw_orig.insert(0, self.lb_keyw_added.get(self.lb_keyw_added.curselection()))
        # deletion
        self.lb_keyw_added.delete(self.lb_keyw_added.index(self.lb_keyw_added.curselection()))
        # auto-selection of the next one
        self.lb_keyw_added.selection_set(0)
        # End of function
        return event, self.lb_keyw_added, self.lb_keyw_orig

    def kill_keyword(self, event='event'):
        """ eliminate the selected keyword from keywords xml """
        if self.lb_keyw_added.curselection():
            self.dico_keywords.pop(self.lb_keyw_added.get(self.lb_keyw_added.curselection()))
            self.lb_keyw_added.delete(self.lb_keyw_added.index(self.lb_keyw_added.curselection()))
            self.lb_keyw_added.selection_set(0)
        elif self.lb_keyw_orig.curselection():
            self.dico_keywords.pop(self.lb_keyw_orig.get(self.lb_keyw_orig.curselection()))
            self.lb_keyw_orig.delete(self.lb_keyw_orig.index(self.lb_keyw_orig.curselection()))
            self.lb_keyw_orig.selection_set(0)
        else:
            avert(title = txt.get('mtc_del'),
                  message=txt.get('mtc_del2'))

        # end of function
        return self.dico_keywords, self.lb_keyw_added, self.lb_keyw_orig

    ###########################################################################
    ###################### Methods: geokeywords (places) ######################
    ###########################################################################

    def add_geokeyword(self, event='event'):
        """ add the selected geokeyword from keywords orig Listbox """
        # insertion
        self.lb_geokeyw_added.insert(0, self.lb_geokeyw_orig.get(self.lb_geokeyw_orig.curselection()))
        # deletion
        self.lb_geokeyw_orig.delete(self.lb_geokeyw_orig.index(self.lb_geokeyw_orig.curselection()))
        # auto-selection of the next one
        self.lb_geokeyw_orig.selection_set(0)
        # End of function
        return event, self.lb_geokeyw_added, self.lb_geokeyw_orig

    def add_new_geokeyword(self, event='event'):
        """ add the new geokeyword to the list """
        # test if the new keyword not already exists
        if self.ent_geokeyw.get() not in self.lb_geokeyw_added.get(0, END) and self.ent_geokeyw.get() != "":
            self.lb_geokeyw_added.insert(0, self.ent_geokeyw.get())
            self.dico_geokeywords[self.ent_geokeyw.get()] = 'former description'
        else:
            print "already exists"
        ## avert(title = txt.get('mtc_exist'),
        ## message=txt.get('mtc_exist2'))
        # reset the fields
        self.ent_geokeyw.delete(0, END)
        self.ent_geokeyw.delete(0, END)
        # end of function
        return self.ent_geokeyw

    def del_geokeyword(self, event='event'):
        """ del the selected geokeyword from keywords added Listbox """
        # insertion
        self.lb_geokeyw_orig.insert(0, self.lb_geokeyw_added.get(self.lb_geokeyw_added.curselection()))
        # deletion
        self.lb_geokeyw_added.delete(self.lb_geokeyw_added.index(self.lb_geokeyw_added.curselection()))
        # auto-selection of the next one
        self.lb_geokeyw_added.selection_set(0)
        # End of function
        return event, self.lb_geokeyw_added, self.lb_geokeyw_orig

    def kill_geokeyword(self, event='event'):
        """ eliminate the selected geokeyword from geokeywords xml """
        if self.lb_geokeyw_added.curselection():
            self.dico_keywords.pop(self.lb_keyw_added.get(self.lb_keyw_added.curselection()))
            self.lb_keyw_added.delete(self.lb_keyw_added.index(self.lb_keyw_added.curselection()))
            self.lb_keyw_added.selection_set(0)
        elif self.lb_keyw_orig.curselection():
            self.dico_keywords.pop(self.lb_keyw_orig.get(self.lb_keyw_orig.curselection()))
            self.lb_keyw_orig.delete(self.lb_keyw_orig.index(self.lb_keyw_orig.curselection()))
            self.lb_keyw_orig.selection_set(0)
        else:
            avert(title = txt.get('mtc_del'),
                  message=txt.get('mtc_del2'))

        # end of function
        return self.dico_keywords, self.lb_keyw_added, self.lb_keyw_orig

###############################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    """ Test parameters for a stand-alone run """
    # imports needed
    from os import listdir
    # test variables
    lang = 'FR'
    dir_profiles = path.join('../locale/{0}/profiles'.format(lang))
    li_profiles = [lg[:-4] for lg in listdir(dir_profiles)]
    dict_text = OD()
    xml = ET.parse('../locale/{0}/lang_{0}.xml'.format(lang))
    for elem in xml.getroot().getiterator():
        dict_text[elem.tag] = elem.text

    # moving in the main directory
    chdir('..//')
    # getting the help
    dico_help = OD()
    path_help = 'locale/{0}/help_{0}.xml'.format(lang)
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
            dico_help[int(idu)] = ref, txt, img, doc
    # clean up
    del elem, xml, dir_profiles
    # initialization
    app = NewProfile(dict_text, lang, dico_help, li_profiles)
    app.mainloop()
