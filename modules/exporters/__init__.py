# -*- coding: UTF-8 -*-
#!/usr/bin/env python

from sys import platform

from md2html import ExportToHTML
from md2odt import ExportToODT
from md2xls import ExportToXLS
from md2xml import ExportToXML

# Imports depending on operating system
if platform == 'win32':
    u""" windows """
    from md2docx import ExportToDocX
    from DocxMerger import DocxMerger
else:
    pass
