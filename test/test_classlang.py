# -*- coding: UTF-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Utilisateur
#
# Created:     15/01/2013
# Copyright:   (c) Utilisateur 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from os import listdir, path, getcwd

home = getcwd()

# Gestion internationalisation
langues = {}              # dictionnaire des langues disponibles
blabla = {}               # dictionnaire des textes selon la langue choisie

dirlang = path.join(home, r'../locale/')
xmlang = path.join(home, r'../locale/FR/lang_FR.xml')

from langang import Langou

yahou = Langou(dirlang)

print yahou.locale