# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import Tkinter
import ttk

root = Tkinter.Tk()

icon_del_tag = r"..\data\img\icon_DelTag_np8756.gif"

drink = Tkinter.PhotoImage(file=icon_del_tag)
b1 = ttk.Button(root, image=drink, text="Hello", compound="right")
b1.grid()


root.mainloop()