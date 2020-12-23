#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Utilisateur
#
# Created:     05/09/2012
# Copyright:   (c) Utilisateur 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from xml.etree import ElementTree as ET    # pour les xml
blabla = {}

class loadlang:
    def __init__(lang='FR'):
        u""" Charge les textes du xml selon la langue choisie. """
        # ouverture du XML (curseur)
        xml = ET.parse(chemin_script + r'\locale\\' + langues.get(lang)[1] +
                       r'\lang_' + lang + '.xml')
        # extraction et remplissage dictionnaire
        for elem in xml.getroot().getiterator():
            blabla[elem.tag] = elem.text
        # Fin de fonction
        return blabla, xml

def main():
    pass

if __name__ == '__main__':
    main()
