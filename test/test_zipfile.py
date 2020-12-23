#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Risor
#
# Created:     04/02/2014
# Copyright:   (c) Risor 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import zipfile

template_odt = "samples/metadator_template_odt_en.odt"
print zipfile.is_zipfile(template_odt)

oupen_temp = zipfile.ZipFile(template_odt)