# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         InfoBulles
# Purpose:      A class to display a ballon tooltip above a Tkinter widget.
#               Can display an image too.
#
# Author:       Julien Moura (https://github.com/Guts)
#
# Source:       http://www.developpez.net/forums/d241112/autres-langages/python-zope/gui/tkinter/info-bulle-tkinter/#post1542643

# Created:      23/06/2013
# Updated:      23/06/2013
#-------------------------------------------------------------------------------

################################################################################
######## Libraries import #########
###################################

# Standard library
from Tkinter import Toplevel, Label, PhotoImage

################################################################################
############# Classes #############
###################################

class InfoBulle(Toplevel):
    u""" Affiche le texte au survol du widget parent. """
    def __init__(self, parent = None, message = '', image = '', time = 1000):
        """ create the top level window from the parent widget """
        Toplevel.__init__(self, parent, bd=1, bg='black')
        # class variables
        self.time = time
        self.parent = parent
        self.withdraw()             # window can't be resized
        self.overrideredirect(1)    # window without borders
        self.transient()
        # label creation
        l = Label(self, text = message, bg="grey", justify='left')
        # update & place
        l.update_idletasks()
        l.pack()
        l.update_idletasks()
        # check if an image has been given
        if image == '':
            pass
        else:
            self.photo=PhotoImage(file=image)
            thumb = Label(self, image=self.photo)
            thumb.pack()
        # get the default width & height
        self.tipwidth = l.winfo_width()
        self.tipheight = l.winfo_height()
        # events handling
        self.parent.bind('<Enter>', self.delay)
        self.parent.bind('<Button-1>', self.undisplay)
        self.parent.bind('<Leave>', self.undisplay)

    def delay(self, event):
        """ On attend self.tps avant d'afficher l'infobulle"""
        self.action = self.parent.after(self.time, self.display)
        # End of function
        return event, self.action

    def display(self):
        """ display the ballon tooltip """
        self.update_idletasks()
        posX = self.parent.winfo_rootx() + self.parent.winfo_width()/2
        posY = self.parent.winfo_rooty() + self.parent.winfo_height()
        if posX + self.tipwidth > self.winfo_screenwidth():
            posX = posX-self.winfo_width() - self.tipwidth
        if posY + self.tipheight > self.winfo_screenheight():
            posY = posY-self.winfo_height() - self.tipheight
        self.geometry('+%d+%d'%(posX,posY))
        self.deiconify()

    def undisplay(self, event):
        """ undisplay the ballon tooltip """
        self.withdraw()
        self.parent.after_cancel(self.action)


################################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    """ test parameters for a stand-alone run """
    from Tkinter import Tk, Button
    root = Tk()
    bouton = Button(root, text = 'test infobulles')
    bouton.pack()
    InfoBulle(bouton, message = 'Test infobulles réussi')
    root.mainloop()
