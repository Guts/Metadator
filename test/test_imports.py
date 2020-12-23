#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Utilisateur
#
# Created:     05/09/2012
# Copyright:   (c) Utilisateur 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from Tkinter import *

def formu():
    import Form

root = Tk()
Button(root, text='Formulaire', command=formu).pack()

root.mainloop()