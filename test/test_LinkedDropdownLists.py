#-------------------------------------------------------------------------------
# Name:         test_LinkedDropdownLists
# Purpose:      testing how a dropdown's values can depend on the values
#               from another dropdown list
#
# Author:       Julien Moura (https://github.com/Guts/)
#
# Created:      16/02/2014
# Licence:      GPL 3
#-------------------------------------------------------------------------------

# imports
from Tkinter import Tk, HORIZONTAL
from ttk import Combobox, Separator

from xml.etree import ElementTree as ET     # pour les xml

# Python 3 backported
from collections import OrderedDict as OD


# global variables
dico_diff_open = OD()
dico_diff_cloz = OD()

# functions
path_diff = '../locale/%s/inspire/diffusion_%s.xml' % ("FR", "FR")
# reading and parsing the xml
with open(path_diff, 'r') as source:
    xml = ET.parse(source)                  # xml cursor
    opened = xml.find('opened')
    for diffusion in opened.findall('licence'):
        name = diffusion.find('name').text
        norm = diffusion.find('norm').text
        cat = diffusion.find('type').text
        doc = diffusion.find('doc').text
        # fillfulling the INSPIRE dictionary
        dico_diff_open[name] = cat, norm, doc




def switch_sub_ddl(event):
    """ set the sub dropdownlist values according to the selected value in the main dropdownlist """
    if event.widget.get() == 'Open':
        ddl_sub["values"] = li_sub_open
    elif event.widget.get() == 'Limited':
        ddl_sub["values"] = li_sub_cloz

# main program
root = Tk()

li_main = ['Open', 'Limited']   # main list
li_sub_open = ["Open Database Licence", "Licence Ouverte / Open Licence"]   # 1st sublist
li_sub_cloz = ["Security", "Legal", ""] # 2nd sublist

# main dropdownlist
ddl_main = Combobox(root, values = li_main)
ddl_main.pack()
ddl_main.bind("<<ComboboxSelected>>", switch_sub_ddl)

# a separator to see better ^^
Separator(orient=HORIZONTAL).pack()

# sub dropdownlist
ddl_sub = Combobox(root, values = li_sub_open)
ddl_sub.pack()

root.mainloop()