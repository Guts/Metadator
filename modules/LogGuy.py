#-*-coding: utf-8-*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         LogGuy
# Purpose:
#
# Author:       Julien Moura (https://github.com/Guts/)
#
# Created:      27/05/2013
# Updated:
# Licence:      GPL 3
#-------------------------------------------------------------------------------

################################################################################
######## Libraries import #########
###################################
# Standard library
import logging
from logging.handlers import RotatingFileHandler

################################################################################
############# Classes #############
###################################

class LogGuy:
    """ Main class """
    def __init__(self):
        """ initial constructor """


    def config(self):
        """ create and configure the log file
        see: http://sametmax.com/ecrire-des-logs-en-python/ """
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)  # all errors will be get
        log_form = logging.Formatter('%(asctime)s || %(levelname)s || %(message)s')
        logfile = RotatingFileHandler('DicoGIS.log', 'a', 5000000, 1)
        logfile.setLevel(logging.DEBUG)
        logfile.setFormatter(log_form)
        self.logger.addHandler(logfile)
        self.logger.info('\t ====== DicoGIS ======')  # first write

    def title(self, titre):
        """ add a title to the log file """


    def append(self, message):
        """ add a new element """
        self.logger.info(message)

    def close(self):
        """ close the logfile """


################################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    LogGuy()
