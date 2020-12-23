# -*- coding: UTF-8 -*-
#!/usr/bin/env python

from xml.etree import ElementTree as ET

# build a tree structure
root = ET.Element('HTML lang="fr"')

head = ET.SubElement(root, "head")

title = ET.SubElement(head, "title")
title.text = "Page Title"

body = ET.SubElement(root, "body")
body.set("bgcolor", "#ffffff")

body.text = "Hello, World!"

# wrap it in an ElementTree instance, and save as XML
tree = ET.ElementTree(root)
tree.write("page_html.html")
tree.write("page_xml.xml",
           encoding = 'utf-8',
           xml_declaration = 'version="1.0"',
           method = 'xml')


##print "Avec ET"
##
##xml_entree = ET.XML(open(r"test_xslt.xml", 'r').read())
##xslt_entree = ET.XML(open(r"test_xslt.xsl", 'r').read())
##transform = ET.XSLT(xslt_entree)
##sortie = output_file = open("sortie.html", 'w')
##resultat = etree.tostring(transform(xml_entree))
##sortie.write(resultat)
##sortie.close()

print "Avec lxml"

from lxml import etree

xml_entree = etree.XML(open(r"test_xslt.xml", 'r').read())
xslt_entree = etree.XML(open(r"test_xslt.xsl", 'r').read())
transform = etree.XSLT(xslt_entree)
sortie = output_file = open("sortie.html", 'w')
resultat = etree.tostring(transform(xml_entree))
sortie.write(resultat)
sortie.close()