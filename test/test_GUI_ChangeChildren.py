#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julien
#
# Created:     15/07/2013
# Copyright:   (c) Julien 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Tkinter import *
from ttk import *

wid = ''

def change_children():
    global wid
##    print fr1.children
    print fr1.winfo_children()
    for wid in fr1.winfo_children():
        print wid.winfo_class()
        if wid.winfo_class() == 'TEntry':
            wid.configure(state = ACTIVE)



root = Tk()

Label(root, text = 'main').pack()


fr1 = Labelframe(root, text = 'sub frame')
ent1 = Entry(fr1, state = DISABLED)
ent1.pack()

Button(fr1, text = 'change', command = change_children).pack()

fr1.pack()


root.mainloop()