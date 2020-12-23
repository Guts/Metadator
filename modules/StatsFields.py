#-*-coding: utf-8-*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         Stats Fields
# Purpose:
#
# Author:       Julien Moura (https://github.com/Guts)
#
# Created:      13/06/2013
# Updated:      18/06/2013
# Licence:      GPL 3
#-------------------------------------------------------------------------------

################################################################################
######## Libraries import #########
###################################
# Standard library
from operator import itemgetter     # avanced iteration functions
from os import path

import logging

import warnings

# Python 3 backported
from collections import OrderedDict as OD

# 3rd party libraries
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta    # times delta calculation

from numpy import median, average   # median and mean calculation
from numpy import std as ectyp      # standart deviation (French abbreviation beacause std is a Python keywords)
from osgeo import ogr               # for geography objects

# Custom modules


################################################################################
############# Classes #############
###################################

class StatsFields():
    """ Main class """
    def __init__(self, feature, dico_fields, dico_rekurs, blabla):
        u"""
        Parsing fields and command statistical methods.

        dico_fields: dictionary of fields definition
        dico_rekurs: dictionary of recurring fields (specific use for Metadator)
        """
        # getting the layer
        source = ogr.Open(feature, 0)
        layer = source.GetLayer()
        # variables depending on type of feature
        if path.splitext(feature)[1].lower() == '.shp':
            start = 0
            end = layer.GetFeatureCount()
        elif path.splitext(feature)[1].lower() == '.tab':
            start = 1
            end = layer.GetFeatureCount() +1
        # parsing fields
        for field in dico_fields:
            # check recurring field and adding information found in
            do_stats = 1
            if field in dico_rekurs.keys():
                descript = dico_rekurs.get(field)[0]
                if dico_rekurs.get(field)[2] == '0':
                    """ check if basics statistics are disabled for this field """
                    do_stats = 0
                    dico_fields[field] = dico_fields.get(field),\
                                         descript, do_stats
                    pass
                else:
                    pass
            else:
                descript = blabla.get('acompleter')

            # statistical method depending on field type
            if dico_fields[field][0] == 'Integer' and do_stats == 1:
                """ integer (short and long ones) """
                # compiling information
                dico_fields[field] = dico_fields.get(field),\
                                     descript,\
                                     self.stats_ent(layer, field, blabla, start, end)
            elif dico_fields[field][0] == 'Real' and do_stats == 1:
                """ float / doubles / real """
                # compiling information
                dico_fields[field] = dico_fields.get(field),\
                                     descript,\
                                     self.stats_flo(layer, field, blabla, start, end)
            elif dico_fields[field][0] == 'String' and do_stats == 1:
                """ text / string """
                # compiling information
                dico_fields[field] = dico_fields.get(field),\
                                     descript,\
                                     self.stats_text(layer, field, blabla, start, end)
            elif dico_fields[field][0] == 'Date' and do_stats == 1:
                """ date """
                # compiling information
                dico_fields[field] = dico_fields.get(field),\
                                     descript,\
                                     self.stats_date(layer, field, blabla, start, end)
            else:
                pass


    def stats_flo(self, layer, field, txt, start, end = 0):
        u"""
        Basic statistics about float fields.
        """
        # local variables
        li_values = []
        dico_freq = {}
        # frequency
        for obj in range(start, end):
            u"""
            Calculates frequency: values and the number of occurrences of
            each unique field value
            """
            value = layer.GetFeature(obj).GetFieldAsDouble(field)
            li_values.append(value)
            if dico_freq.has_key(value):
                dico_freq[value] = dico_freq.get(value)+1
            else:
                dico_freq[value] = 1
        # basic statistics
        som = round(sum(li_values), 2)          # sum
        med = round(median(li_values), 2)       # median
        moy = round(average(li_values), 2)      # mean
        ect = round(ectyp(li_values), 2)        # standart deviation
        uppest = max(li_values)                 # maximum
        bottom = min(li_values)                 # minimum
        vid = li_values.count(0)                # counter for null values
        # null and frequency checks
        if vid != 0:
            dico_freq.pop(0)
        if len(dico_freq.keys()) == len(li_values):
            mod = txt.get('valuniq')
            freq = ''
        elif len(dico_freq.keys()) == 1:
            mod = txt.get('valcom') + unicode(dico_freq.keys()[0])
            freq = ''
        elif 1 < len(dico_freq.keys()) <= 20:
            mod = unicode(len(dico_freq.keys())) \
                  + txt.get('num_valdif')
            freq = dico_freq.items()    # tuplization
            freq.sort(key=itemgetter(1))
            freq = freq[0:20]
        else:
            mod = unicode(len(dico_freq.keys())) \
                  + txt.get('num_valdif20')
            freq = dico_freq.items()
            freq.sort(key=itemgetter(1), reverse=True)
            freq = freq[0:20]

        # End of function
        return (som, med, moy, uppest, bottom, freq, mod, ect, vid)

    def stats_ent(self, layer, field, txt, start, end = 0):
        u"""
        Basic statistics about integer fields.
        """
        # local variables
        li_values = []
        dico_freq = {}
        # frequency
        for obj in range(start, end):
            u"""
            Calculates frequency: values and the number of occurrences of
            each unique field value
            """
            value = layer.GetFeature(obj).GetFieldAsInteger(field)
            li_values.append(value)
            if dico_freq.has_key(value):
                dico_freq[value] = dico_freq.get(value)+1
            else:
                dico_freq[value] = 1
        # basic statistics
        som = sum(li_values)                 # sum
        med = median(li_values)              # median
        moy = round(average(li_values), 2)   # mean
        ect = round(ectyp(li_values), 2)     # standart deviation
        uppest = max(li_values)              # maximum
        bottom = min(li_values)              # minimum
        vid = li_values.count(0)             # counter for null values
        # null and frequency checks
        if vid != 0:
            dico_freq.pop(0)
        if len(dico_freq.keys()) == len(li_values):
            mod = txt.get('valuniq')
            freq = ''
        elif len(dico_freq.keys()) == 1:
            mod = txt.get('valcom') + unicode(dico_freq.keys()[0])
            freq = ''
        elif 1 < len(dico_freq.keys()) <= 20:
            mod = unicode(len(dico_freq.keys())) \
                  + txt.get('num_valdif')
            freq = dico_freq.items()    # tuplization
            freq.sort(key=itemgetter(1))
            freq = freq[0:20]
        else:
            mod = unicode(len(dico_freq.keys())) \
                  + txt.get('num_valdif')
            freq = dico_freq.items()
            freq.sort(key=itemgetter(1), reverse=True)
            freq = freq[0:20]

        # End of function
        return (som, med, moy, uppest, bottom, freq, mod, ect, vid)

    def stats_text(self, layer, field, txt, start, end = 0):
        u"""
        Basic statistics about string fields.
        """
        # local variables
        li_values = []
        dico_freq = {}
        # frequency
        for obj in range(start, end):
            u"""
            Calculates frequency: values and the number of occurrences of
            each unique field value
            """
            value = layer.GetFeature(obj).GetFieldAsString(field)
            li_values.append(value)
            if dico_freq.has_key(value):
                dico_freq[value] = dico_freq.get(value)+1
            else:
                dico_freq[value] = 1
        # null and frequency checks
        if len(dico_freq.keys()) == len(li_values):
            mod = txt.get('valuniq')
            freq = ''
        elif len(dico_freq.keys()) == 1:
            try:
                mod = txt.get(u'valcom') + unicode(dico_freq.keys()[0])
            except UnicodeDecodeError:
                mod = txt.get(u'valcom') + unicode(dico_freq.keys()[0].decode('utf8'))
            freq = ''
        elif 1 < len(dico_freq.keys()) <= 20:
            mod = unicode(len(dico_freq.keys())) \
                  + txt.get('txt_valdif')
            freq = dico_freq.items()    # tuplization
            freq.sort(key=itemgetter(1))
            freq = freq[0:20]
        else:
            mod = unicode(len(dico_freq.keys())) \
                  + txt.get('txt_valdif20')
            freq = dico_freq.items()
            freq.sort(key=itemgetter(1), reverse=True)
            freq = freq[0:20]

        warnings.filterwarnings('ignore')   # due to issue #10 https://github.com/Guts/Metadator/issues/10
        vid = li_values.count(u'')             # counter for null values

        # Fin de fonction
        return (mod, freq, vid)

    def stats_date(self, layer, field, txt, start, end = 0):
        u"""
        Basic statistics about date fields.
        """
        # local variables
        li_values = []
        dico_freq = {}
        diffdays = ''
        vid = 0
        # frequency
        for obj in range(start, end):
            u"""
            Calculates frequency: values and the number of occurrences of
            each unique field value
            """
            value = layer.GetFeature(obj).GetFieldAsString(field)
            try:
                valdat = datetime.strptime(value, '%Y/%m/%d')
                if type(valdat) == datetime:
                    li_values.append(valdat)
                    # calcul de la fréquence des occurences
                    if dico_freq.has_key(value):
                        dico_freq[value] = \
                                dico_freq.get(value)+1
                    else:
                        dico_freq[value] = 1
            except ValueError, e:
                vid = vid +1    # counter of null values
        # null check
        if len(li_values) == 0: # if the fields is empty: not perform the stats
            uppest = '0000/00/00'
            bottom = '0000/00/00'
            mod = txt.get('champvid')
            freq = ''
            logging.warning('This date field has empty values: %s' % field)
            # End of function
            return (uppest, bottom, diffdays, freq, mod, vid)
        else:
            # frequency checks
            if len(dico_freq.keys()) == len(li_values):
                mod = txt.get('valuniq')
                freq = ''
            elif len(dico_freq.keys()) == 1:
                mod = txt.get('valcom') + unicode(dico_freq.keys()[0])
                freq = ''
            elif 1 < len(dico_freq.keys()) <= 20:
                mod = unicode(len(dico_freq.keys())) \
                      + txt.get('txt_valdif')
                freq = dico_freq.items()    # tuplization
                freq.sort(key=itemgetter(1))
                freq = freq[0:20]
            else:
                mod = unicode(len(dico_freq.keys())) \
                      + txt.get('txt_valdif20')
                freq = dico_freq.items()
                freq.sort(key=itemgetter(1), reverse=True)
                freq = freq[0:20]

            # delta tima calculation
            uppest = max(li_values)    # maximum
            bottom = min(li_values)    # minimum
            dico_days = relativedelta(uppest, bottom).__dict__  # delta in days
            if dico_days.has_key('years'):
               diffdays = diffdays + unicode(dico_days.get('years')) + txt.get('date_ans')
            if dico_days.has_key('months'):
               diffdays = diffdays + unicode(dico_days.get('months')) \
                                   + txt.get('date_mois')
            if dico_days.has_key('days'):
               diffdays = diffdays + unicode(dico_days.get('days')) \
                                   + txt.get('date_jour')

            # End of function
            return (uppest, bottom, diffdays, freq, mod, vid)


################################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    """ Test parameters for a stand-alone run """
    print('Only for a use with Metadator')
