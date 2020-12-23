# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals

from os import path, walk, listdir

# global variables
li_shp = []
li_tab = []

li_shp2 = []
li_tab2 = []
foldertarget = r"samples"

# Looping in folders structure
for root, dirs, files in walk(foldertarget):
    for f in files:
        try:
    	   print f, type(f)
        except:
            print type(f)
        try:
        	unicode(path.join(root, f))
        	full_path = path.join(root, f)
        except UnicodeDecodeError, e:
        	full_path = path.join(root, f.decode('latin1'))
        	print unicode(full_path)
        # Looping on files contained
        if path.splitext(full_path.lower())[1] == '.shp' and \
        path.isfile('%s.dbf' % full_path[:-4]) and \
        path.isfile('%s.shx' % full_path[:-4]) and \
        path.isfile('%s.prj' % full_path[:-4]):
        	# add complete path of shapefile
        	li_shp.append(full_path)
        elif path.splitext(full_path.lower())[1] == '.tab' and \
        path.isfile(full_path[:-4] + '.dat') and \
        path.isfile(full_path[:-4] + '.map') and \
        path.isfile(full_path[:-4] + '.id'):
        	# add complete path of MapInfo file
        	li_tab.append(full_path)


for root, dirs, files in walk(unicode(foldertarget)):
    for f in files:
        try:
            unicode(path.join(root, f))
            full_path = path.join(root, f)
        except UnicodeDecodeError, e:
            full_path = path.join(root, f.decode('latin1'))
            print unicode(full_path)
        # Looping on files contained
        if path.splitext(full_path.lower())[1].lower() == '.shp' and \
        (path.isfile('%s.dbf' % full_path[:-4]) or path.isfile('%s.DBF' % full_path[:-4])) and \
        (path.isfile('%s.shx' % full_path[:-4]) or path.isfile('%s.SHX' % full_path[:-4])) and \
        (path.isfile('%s.prj' % full_path[:-4]) or path.isfile('%s.PRJ' % full_path[:-4])):
            # add complete path of shapefile
            li_shp2.append(full_path)
        elif path.splitext(full_path.lower())[1] == '.tab' and \
        (path.isfile(full_path[:-4] + '.dat') or path.isfile(full_path[:-4] + '.DAT')) and \
        (path.isfile(full_path[:-4] + '.map') or path.isfile(full_path[:-4] + '.MAP')) and \
        (path.isfile(full_path[:-4] + '.id') or path.isfile(full_path[:-4] + '.ID')):
            # add complete path of MapInfo file
            li_tab2.append(full_path)


print len(li_shp), li_shp
print len(li_shp2), li_shp2
print len(li_tab), li_tab
print len(li_tab2), li_tab2


   

# import re
# pat = re.compile(r'[.](shp|dbf|shx|prj)$', re.IGNORECASE)
# filenames = [filename for filename in listdir(r'samples/shp')
#              if re.search(pat, filename)]
# print(filenames)



file_case = r'samples/shp/10m_land.SHP' 
file_enc = r'samples/tab/Métaux_Bryophytes.TAB'

print file_case
print file_case.lower()
print path.lexists(file_case), path.exists(file_enc)
print path.lexists(file_case.lower()), path.exists(file_enc.lower())
print path.normpath(file_case)
print path.abspath(file_case)
print path.normcase(file_case)


