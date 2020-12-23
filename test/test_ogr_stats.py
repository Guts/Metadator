#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Utilisateur
#
# Created:     12/09/2012
# Copyright:   (c) Utilisateur 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from osgeo import ogr               # pour la géométrie
from os import path, listdir, mkdir, chdir, rmdir, walk  # fichiers/dossiers
from xml.etree import ElementTree as ET    # pour les xml
from time import localtime                          # pour le log
from operator import itemgetter    # fonctions avancées d'itération

from datetime import date
from datetime import datetime

def load_textes(lang='FR'):
    u""" Charge les textes du xml selon la langue choisie. """
    # ouverture du XML (curseur)
    xml = ET.parse(r'locale\\' + lang
                   + r'\lang_' + lang + '.xml')
    # extraction et remplissage dictionnaire
    for elem in xml.getroot().getiterator():
        blabla[elem.tag] = elem.text
    # Fin de fonction
    return blabla, xml

def stats(champ, couche, tipo):
    u"""Réalise certaines opérations statistiques basiques sur le champ texte
    donné du dbf donné."""
    global mod, freq, vid, dico_champs, dico_freq
    # RAZ
    dico_freq.clear()
    liste_valeurs = []      # liste réceptionnaire des valeurs du champ
    for obj in range(couche.GetFeatureCount()):
        u"""Remplissage de la liste avec les valeurs du champ et calcul de la
        fréquence des modalités"""
        valeur = couche.GetFeature(obj).GetFieldAsString(champ)
        print '\t', valeur, type(valeur)
        valeur2 = couche.GetFeature(obj).GetFieldAsString(champ)
        print '\t\t', valeur2, type(valeur2)
        liste_valeurs.append(valeur)
        if dico_freq.has_key(valeur):
            dico_freq[valeur] = dico_freq.get(valeur)+1
        else:
            dico_freq[valeur] = 1

    # Check de la fréquence
    if len(dico_freq.keys()) == len(liste_valeurs):
        u""" si chaque valeur est unique """
        mod = blabla.get('valuniq')
    elif len(dico_freq.keys()) == 1:
        u""" si une seule valeur est commune à tous les objets """
        mod = blabla.get('valcom') + unicode(dico_freq.keys()[0])
    elif 1 < len(dico_freq.keys()) <= 20:
        u""" si le nombre de modalités différentes n'excède pas 20 """
        mod = unicode(len(dico_freq.keys())) \
              + blabla.get('txt_valdif')
        freq = dico_freq.items()    # transformation en liste de tuples
        freq.sort(key=itemgetter(1))
        freq = freq[0:20]
    else:
        mod = unicode(len(dico_freq.keys())) \
              + blabla.get('txt_valdif20')
        freq = dico_freq.items()
        freq.sort(key=itemgetter(1), reverse=True)
        freq = freq[0:20]
    vid = liste_valeurs.count('')             # nombre de valeurs vides

    # Fin de fonction
    return mod, freq, vid, dico_freq

def stats_date(champ, source):
    u"""Réalise certaines opérations statistiques basiques sur le champ date
    donné du dbf donné."""
    global diffdays, uppest, bottom, mod, freq, vid
    liste_valeurs = []    # où seront stockées les valeurs du champ
    dico_freq = {}    # pour calculer les modalités et leurs fréquence
    # Ouverture des données du shape
    couche = source.GetLayer()
    # Parcours des modalités
    for obj in range(couche.GetFeatureCount()):
        u"""Remplissage de la liste avec les valeurs du champ et calcul de la
        fréquence des modalités"""
        valeur = couche.GetFeature(obj).GetFieldAsString(champ)
        print valeur, type(valeur)
        if type(valeur) == date:
            liste_valeurs.append(valeur)
            # calcul de la fréquence des occurences
            if dico_freq.has_key(datetime.strftime(valeur, '%d-%m-%Y')):
                dico_freq[datetime.strftime(valeur, '%d-%m-%Y')] = \
                        dico_freq.get(datetime.strftime(valeur, '%d-%m-%Y'))+1
            else:
                dico_freq[datetime.strftime(valeur, '%d-%m-%Y')] = 1

def infos_ogr(source):
    u"""Utilise les fonctions de la librairie OGR pour extraire les
    caractéristiques de la table donnée en paramètre et les stocker dans le
    dictionnaire correspondant."""
    global dico_infos_couche, dico_champs, liste_chps, alert, def_couche
##    driver = ogr.GetDriverByName('ESRI Shapefile')    # driver OGR
##    source = driver.Open(chemin_couche, 0)
    couche = source.GetLayer()
    if couche.GetFeatureCount() == 0:
        u""" Si le shape n'a aucun objet, le processus est interrompu """
        dico_infos_couche[u'nom'] = path.basename(chemin_couche)
        def_couche = couche.GetLayerDefn()
        dico_infos_couche[u'nbr_attributs'] = def_couche.GetFieldCount()
        alert = 1
        return
    objet = couche.GetFeature(0)
    if not objet:
        objet = couche.GetFeature(1)
    geom = objet.GetGeometryRef()
    def_couche = couche.GetLayerDefn()
    srs = couche.GetSpatialRef()
    srs.AutoIdentifyEPSG()
    # remplissage du dictionnaire
    dico_infos_couche[u'nom'] = path.basename(chemin_couche)
    dico_infos_couche[u'titre'] = dico_infos_couche[u'nom'][:-4].replace('_', ' ').capitalize()
    dico_infos_couche[u'nbr_objets'] = couche.GetFeatureCount()
    dico_infos_couche[u'nbr_attributs'] = def_couche.GetFieldCount()
    dico_infos_couche[u'EPSG'] = unicode(srs.GetAttrValue("AUTHORITY", 1))
    dico_infos_couche[u'srs'] = unicode(srs.GetAttrValue("PROJCS")).replace('_', ' ')

    # type géométrie
    if geom.GetGeometryName() == u'POINT':
        dico_infos_couche[u'type_geom'] = blabla.get('geom_point')
    elif u'LINESTRING' in geom.GetGeometryName():
        dico_infos_couche[u'type_geom'] = blabla.get('geom_ligne')
    elif u'POLYGON' in geom.GetGeometryName():
        dico_infos_couche[u'type_geom'] = blabla.get('geom_polyg')
    else:
        dico_infos_couche[u'type_geom'] = geom.GetGeometryName()

    # extension
    dico_infos_couche[u'Xmin'] = round(couche.GetExtent()[0],2)
    dico_infos_couche[u'Xmax'] = round(couche.GetExtent()[1],2)
    dico_infos_couche[u'Ymin'] = round(couche.GetExtent()[2],2)
    dico_infos_couche[u'Ymax'] = round(couche.GetExtent()[3],2)

    # champs (merci à Gene http://www.forumsig.org/member.php?u=2923)
    for i in range(def_couche.GetFieldCount()):
        champomy = def_couche.GetFieldDefn(i)
        dico_champs[champomy.GetName()] = champomy.GetTypeName(),\
                                          champomy.GetWidth(),\
                                          champomy.GetPrecision()

    # données
    for chp in sorted(dico_champs.keys()):
        print chp
        # RAZ
        dico_freq.clear()
        mod = ''
        vid = 0
        freq = ''
        if dico_champs.get(chp)[0] == 'String':
            print '- TEXTE -'
            stats(chp, couche, 'String')
        elif dico_champs.get(chp)[0] == 'Integer':
            print '- ENTIER -'
            stats(chp, couche, 'Integer')
        elif dico_champs.get(chp)[0] == 'Real':
            print '- REEL -'
            stats(chp, couche, 'Real')
        elif dico_champs.get(chp)[0] == 'Date':
            print '- DATE -'
            stats_date(chp, source)

    # dates clésde la couche d'information
    dico_infos_couche[u'date_actu'] = localtime(path.getmtime(chemin_couche))[0:3]
    dico_infos_couche[u'date_creation'] = localtime(path.getctime(chemin_couche))[0:3]

    # Fin de fonction
    return dico_infos_couche, dico_champs, liste_chps, alert, mod, vid, freq

dico_infos_couche = {}
dico_freq = {}
dico_champs = {}
liste_chps = []
alert = ''

def_couche = ''

blabla = {}
load_textes()

chemin_couche = r'data\test\airports.shp'
driver = ogr.GetDriverByName('ESRI Shapefile')    # driver OGR
source = driver.Open(chemin_couche, 0)
##infos_ogr(source)

liste_valeurs = []    # où seront stockées les valeurs du champ
dico_freq = {}    # pour calculer les modalités et leurs fréquence
# Ouverture des données du shape
couche = source.GetLayer()
# Parcours des modalités
for obj in range(couche.GetFeatureCount()):
    u"""Remplissage de la liste avec les valeurs du champ et calcul de la
    fréquence des modalités"""
    valeur = couche.GetFeature(obj).GetFieldAsString('CREATION')
    print valeur, type(valeur)
    if type(datetime.strptime(valeur, '%Y/%m/%d')) == datetime:
        liste_valeurs.append(datetime.strptime(valeur, '%Y/%m/%d'))
        # calcul de la fréquence des occurences
        if dico_freq.has_key(datetime.strptime(valeur, '%Y/%m/%d')):
            dico_freq[datetime.strptime(valeur, '%Y/%m/%d')] = \
                    dico_freq.get(datetime.strptime(valeur, '%Y/%m/%d'))+1
        else:
            dico_freq[datetime.strptime(valeur, '%Y/%m/%d')] = 1


# champs (merci à Gene http://www.forumsig.org/member.php?u=2923)
def_couche = couche.GetLayerDefn()
for i in range(def_couche.GetFieldCount()):
    champomy = def_couche.GetFieldDefn(i)
    dico_champs[champomy.GetName()] = champomy.GetTypeName(),\
                                      champomy.GetWidth(),\
                                      champomy.GetPrecision()


