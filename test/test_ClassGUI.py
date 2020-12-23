# -*- coding: UTF-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        test new GUI metadator
# Purpose:
# Author:      Julien M.
# Created:     25/03/2013
# Licence:
#-------------------------------------------------------------------------------

###################################
##### Libraries importation #######
###################################

# standard library
from Tkinter import Tk, Frame, Label, Button, W, Entry, StringVar, LabelFrame, HORIZONTAL
from tkFileDialog import askopenfilename, askdirectory
from tkMessageBox import showerror
from ttk import Combobox, Progressbar

from os import mkdir, path, listdir, walk

# third party


###################################
####### Classes definition ########
###################################


class Metadator_GUI(Tk):
    """ Main class """
    def __init__(self):
        # basics settings
        Tk.__init__(self)               # constructor of parent graphic class
        self.focus_force()              # put the window on foreground
        self.resizable(width = False,      # freeze dimensions
                       height = False)
        self.iconbitmap('../data/images/metadator.ico')     # icon
        self.title(u'Choose your maps before and after')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # Frames
        self.frmain = LabelFrame(self, text = 'General')
        self.frprog = LabelFrame(self, text = 'Progression')

        # GUI variables
        self.nbshp = StringVar()    # number of shapefiles
        self.nbtab = StringVar()    # number of MapInfo files

        #### Main frame
        # Labels
        self.labglob = Label(self.frmain, text = u' Please paste or browse the path of your maps')
        self.labefore = Label(self, text = u'Map before: ')
        self.labafter = Label(self, text = u'Map after: ')
        self.numfiles = Label(self, textvariable = self.nbshp)
        # paths to image
        self.pathbefore = Entry(self, width = 35)
        self.pathafter = Entry(self, width = 35)
        # browse buttons
        self.browsebef = Button(self, text = 'Browse',
                                      command = self.setpathbef)
        self.browseaft = Button(self, text = 'Browse',
                                      command = self.setpathaft)

        # target folder
        self.labtarg = Label(self, text = u'Destination folder: ')
        self.target = Entry(self, width = 35)
        self.browsetarg = Button(self, text = 'Browse',
                              command = self.setpathtarg)
        # basic buttons
        self.validate = Button(self, text = 'Launch',
                                     relief= 'raised',
                                     command = self.bell)
        self.cancel = Button(self, text = 'Cancel (quit)',
                                   relief= 'groove',
                                   command = self.destroy)


        #### Progression frame
        # Progress bar
        self.prog = Progressbar(self,
                    orient=HORIZONTAL,
                    max = 50,
                    length=200,
                    mode='determinate')


        # widgets placement
        self.labglob.grid(row = 0, column = 0, columnspan = 3)
        self.labefore.grid(row = 1, column = 1, columnspan = 1)
        self.labafter.grid(row = 2, column = 1, columnspan = 1)
        self.labtarg.grid(row = 3, column = 1, columnspan = 1)
        self.pathbefore.grid(row = 1, column = 2, columnspan = 1)
        self.pathafter.grid(row = 2, column = 2, columnspan = 1)
        self.target.grid(row = 3, column = 2, columnspan = 1)
        self.browsebef.grid(row = 1, column = 3, columnspan = 1)
        self.browseaft.grid(row = 2, column = 3, columnspan = 1)
        self.browsetarg.grid(row = 3, column = 3, columnspan = 1)
        self.validate.grid(row = 4, column = 1, columnspan = 2)
        self.cancel.grid(row = 4, column = 3, columnspan = 1, sticky = "W")
        self.numfiles.grid(row=5, column= 2, columnspan = 2)
        self.prog.grid(row=6, column = 0, columnspan = 4)

        # frames placement
        self.frmain.grid(row=6)

    def setpathbef(self):
        """ ...browse and insert the path of FIRST image  """
        self.filename = askopenfilename(parent = self,
                                            title = 'Select the "before" image',
                                            filetypes = (("Images", "*.jpg;*.jpeg;*.png;*.tiff"),
                                                         ("All files", "*.*")))
        if self.filename:
            try:
                self.pathbefore.insert(0, self.filename)
            except:
                print 'no file indicated'
        # end of function
        return self.filename

    def setpathaft(self):
        """ ...browse and insert the path of SECOND image """
        self.filename = askopenfilename(parent = self,
                                        title = 'Select the "after" image',
                                        filetypes = (("Images", "*.jpg;*.jpeg;*.png;*.tiff"),
                                                     ("All files", "*.*")))
        if self.filename:
            try:
                self.pathafter.insert(0, self.filename)
            except:
                print 'no file indicated'
        # end of function
        return self.filename

    def setpathtarg(self):
        """ ...browse and insert the path of DESTINATION FOLDER """
        self.foldername = askdirectory(parent = self,
                                     title = 'Select the destination folder')
        if self.foldername:
            try:
                self.target.insert(0, self.foldername)
            except:
                print 'no folder indicated'
        # calculate number of shapefiles and MapInfo files
        self.nbshp.set(len(self.ligeofiles(self.foldername)[0]))
        self.nbtab.set(len(self.ligeofiles(self.foldername)[1]))
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

    def listing_profils(self):
        u""" Liste les profils existants contenus dans le répertoire dédié"""
        global dico_profils, new
        for i in glob(home + r'/data/profils/*.xml'):
            dico_profils[path.splitext(path.basename(i))[0]] = i
        if new > 0:
            listing_lang()
            load_textes(deroul_lang.get())
            deroul_profils.setlist(sorted(dico_profils.keys()))
            fen_choix.update()
        # Fin de fonction
        return dico_profils



##
##opt_doc = IntVar()  # option activer/désactiver l'export au format word
##opt_doc.set(defaut_doc)      # par défaut on active cette option
##opt_xls = IntVar()  # option activer/désactiver l'export au format excel
##opt_xls.set(defaut_xls)
##opt_xml = IntVar()  # option activer/désactiver l'export au format xml
##opt_xml.set(defaut_xml)
##
##fen_choix.title(blabla.get('gui_titre'))    # titre de la fenêtre
##
##Label(fen_choix, text = blabla.get('bonjour')           # dit bonjour à la dame..
##      + env.get(u'USERNAME') + ".").grid(row=0,         # ..en chopant le nom..
##                                         column=0,      # ..d'utilisateur du..
##                                         columnspan=2,  # système.
##                                         sticky = N+S+W+E,
##                                         padx = 2,
##                                         pady = 1)
### Indique le nombre de shapes trouvés dans l'arborescence
##Label(fen_choix, text= str(len(li_capas)) +
##                       blabla.get('gui_numshp')).grid(row = 1,
##                                                      column = 0,
##                                                      columnspan = 2,
##                                                      sticky = N+S+W+E,
##                                                      padx = 2,
##                                                      pady = 1)
### Liste déroulante des langues disponibles
##deroul_lang = ComboBox(fen_choix,
##                       labelpos = NW,
##                       label_text = blabla.get('gui_cholang'),
##                       scrolledlist_items = sorted(langues.keys()),
##                       listheight = len(langues.keys())*20,
##                       selectioncommand = changelang,
##                       entry_width = 4)
##deroul_lang.grid(row = 0,           # Placement du widget sur la ligne 0..
##                 column = 2,        # ..colonne 2..
##                 sticky = N+S,      # ..centrage vertical..
##                 padx = 2,          # ..marge horizontale de 2 pixel..
##                 pady = 1)          # ..marge verticale de 2 pixels.
### sélection de la langue enregistrée dans les paramètres par défaut
##deroul_lang.selectitem(sorted(langues.keys()).index(defaut_codlang))
##
### Liste déroulante des profils disponibles
##deroul_profils = ComboBox(fen_choix,
##                          labelpos = NW,
##                          label_text = blabla.get('gui_choix') + \
##                                       str(len(dico_profils.keys()) - 1) +\
##                                       blabla.get('gui_exist'),
##                          scrolledlist_items = sorted(dico_profils.keys()),
##                          listheight = len(dico_profils.keys())*20,
##                          selectioncommand = bouton_alt,
##                          entry_width = 28)
##deroul_profils.grid(row = 2,
##                    column = 0,
##                    columnspan = 2,
##                    sticky = N+S+W+E,
##                    padx = 2,
##                    pady = 5)
##deroul_profils.selectitem(0, setentry = 1)
##
### Bouton d'actualisation de la liste déroulante
##bout_actu = Button(fen_choix,
##                   text = blabla.get('gui_actualiser'),
##                   command = listing_profils)
##bout_actu.grid(row = 1,
##               rowspan = 2,
##               column = 2,
##               sticky = N+S+E+W,
##               padx = 2,
##               pady = 2)
##
### Options d'export
##caz_doc = Checkbutton(fen_choix,
##            text = u'HTML / Word (.doc/.docx)',
##            variable = opt_doc)
##caz_doc.grid(row = 3,
##             column = 0,
##             columnspan = 2,
##             sticky = N+S+W,
##             padx = 2,
##             pady = 1)
##
##caz_xls = Checkbutton(fen_choix,
##            text = u'Excel 2003 (.xls)',
##            variable = opt_xls)
##caz_xls.grid(row = 4,
##             column = 0,
##             sticky = N+S+W,
##             padx = 2,
##             pady = 1)
##
##caz_xml = Checkbutton(fen_choix,
##            text = u'XML (ISO 19139)',
##            variable = opt_xml)
##caz_xml.grid(row = 5,
##             column = 0,
##             sticky = N+S+W,
##             padx = 2,
##             pady = 1)
##
### Boutons confirmation/annulation
##bouton = Button(fen_choix,
##                text = blabla.get('gui_choprofil'),
##                command=choix_profil,
##                borderwidth = 3)
##bouton.grid(row = 6,
##            column = 0,
##            columnspan = 2,
##            padx = 2,
##            pady = 2,
##            sticky = N+S+W+E)
##
##Button(fen_choix, text = blabla.get('gui_quit'),
##                  relief = RIDGE,
##                  borderwidth = 1,
##                  command = annuler).grid(row=6,
##                                          column=2,
##                                          padx = 2,
##                                          pady = 2,
##                                          sticky = N+S+W+E)
### Infobulles
##bull_choix = InfoBulle(parent = bouton,
##                       texte = u"Choisir le profil indiqué et lancer le\ntraitement avec les options choisies.")
##bull_actu = InfoBulle(parent = bout_actu,
##                      texte = u"Met à jour la liste des profils créés auparavant.\nÀ utiliser après avoir créé un nouveau profil.")
##bull_doc = InfoBulle(parent = caz_doc,
##                     texte = u"Fiche HTML exportée en Word composée d'une fiche récapitulative suivie de la\nliste des attributs sur lesquels est exécutée une série de statistiques de base.",
##                     image = thumb_doc)
##bull_xls = InfoBulle(parent = caz_xls,
##                     texte = u"Tableur Excel composé d'une feuille récapitulative et d'une seconde feuille dédiée\naux attributs et leurs statistiques.",
##                     image = thumb_xls)
##bull_xml = InfoBulle(parent = caz_xml,
##                     texte = u"Document XML au standart ISO permettant l'import dans des outils de catalogage\n(GeoNetwork, GéoSource...).",
##                     image = thumb_xml)


###################################
### Main program initialization ###
###################################

if __name__ == '__main__':
    app = Metadator_GUI()
    app.mainloop()