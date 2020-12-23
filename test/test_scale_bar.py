# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         Metadata profile form
# Purpose:      Allow to create a metadata profile which could be used after in
#                   metadator. Profiles are saved as xml files.
# Author:       Julien Moura (https://github.com/Guts/)
# Python :      2.7.x
# Encoding:     utf-8
# Created:      17/11/2011
# Updated:      16/12/2013
#-------------------------------------------------------------------------------

# inspired by: http://www.pyinmyeye.com/2012/08/tkinter-ttkscale-demo.html

from Tkinter import Tk, HORIZONTAL, VERTICAL, StringVar, IntVar, PhotoImage
from ttk import Scale, Label, LabeledScale


def _scale_update(evt):
    idx = int(float(evt))
    icon = PhotoImage(name = 'icon', file = dico_scales.get(idx)[2])
    lb_display.configure(text='1: {}\n({})'.format(dico_scales.get(idx)[1], dico_scales.get(idx)[0] ),
                         image = icon,
                         compound ='right')
    lb_display.update()

root = Tk()


dico_scales = {
                1 : ("Globe", "150 000 000", r"../data/img/icon_scale_world_np11042.gif"),
                2 : ("Continent", "50 000 000", r"../data/img/icon_scale_continent_np19032.gif"),
                3 : ("Pays", "20 000 000", r"../data/img/icon_scale_country_np27171.gif"),
                4 : ("Région", "5 000 000", r"../data/img/icon_scale_world_np11042.gif"),
                5 : ("Département", "150 000", r"../data/img/icon_scale_world_np11042.gif"),
                6 : ("Ville", "50 000", r"../data/img/icon_scale_world_np11042.gif"),
                7 : ("Bâtiment", "5 000", r"../data/img/icon_scale_world_np11042.gif"),
                }

sc_var = StringVar()
lbsc_var = IntVar()

icon = PhotoImage(name = 'icon', file = dico_scales.get(1)[2])

lb_display = Label(root, compound="right", image = icon)

sc_test = Scale(root,
                orient = HORIZONTAL,
                variable = sc_var,
                from_ = 1,
                to = 7,
                command = _scale_update)



#### former codelines from ProfileForm.py (line 389 +)
##self.lb_icon_minscale = Label(self.FrDivers, image = self.icon_inspire)
##self.sc_geoscale = Scale(self.FrDivers, orient=HORIZONTAL, label = "échelle",
##                         from_= 5000, to = 150000, tickinterval = 10000, troughcolor="cyan",
##                         resolution = 50000, sliderlength=50)
##self.lb_icon_maxscale = Label(self.FrDivers, image = self.icon_new_profile)
##
##self.lb_icon_minscale.grid(row = 4, column = 0, pady = 3, sticky = "w")
##self.lb_icon_maxscale.grid(row = 4, column = 3, pady = 3, sticky = "e")
##self.sc_geoscale.grid(row = 4, column = 0, columnspan = 4, padx = 55, pady = 3, sticky = "we")


sc_test.pack()
lb_display.pack()


lbsc_test = LabeledScale(root, variable = lbsc_var)
lbsc_test.pack()

root.mainloop(0)
