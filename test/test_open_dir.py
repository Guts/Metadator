# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals




import subprocess
import sys
import os
 
def run_file(path):
    """ 
    http://sametmax.com/ouvrir-un-fichier-avec-le-bon-programme-en-python"""
    # Pas de EAFP cette fois puisqu'on est dans un process externe,
    # on ne peut pas gérer l'exception aussi facilement, donc on fait
    # des checks essentiels avant.
 
    # Vérifier que le fichier existe
    if not os.path.exists(path):
        raise IOError('No such file: %s' % path)
 
    # On a accès en lecture ?
    if hasattr(os, 'access') and not os.access(path, os.R_OK):
        raise IOError('Cannot access file: %s' % path)
 
    # Lancer le bon programme pour le bon OS :
 
    if hasattr(os, 'startfile'): # Windows
        # Startfile est très limité sous Windows, on ne pourra pas savoir
        # si il y a eu une erreu
        proc = os.startfile(path)
 
    elif sys.platform.startswith('linux'): # Linux:
        proc = subprocess.Popen(['xdg-open', path], 
                                 # on capture stdin et out pour rendre le 
                                 # tout non bloquant
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 
    elif sys.platform == 'darwin': # Mac:
        proc = subprocess.Popen(['open', '--', path], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 
    else:
        raise NotImplementedError(
            "Your `%s` isn't a supported operatin system`." % sys.platform)
 
    # Proc sera toujours None sous Windows. Sous les autres OS, il permet de
    # récupérer le status code du programme, and lire / ecrire sur stdin et out
    return proc




test_dir = r'/home/guts/code/GitHub/Metadator/test/samples/shp'
test_file = r'/home/guts/code/GitHub/Metadator/test/samples/metadator_template_odt_en.odt'


run_file(test_dir)
run_file(test_file)