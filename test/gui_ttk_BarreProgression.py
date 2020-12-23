# -*- coding: UTF-8 -*-
#!/usr/bin/env python

from Tkinter import Tk, Button
from ttk import Progressbar as barprog

class Progrou(Tk):
    def __init__(self):
        Tk.__init__(self)               # constructor of parent graphic class
        self.title('Graphic progressbar test')
        self.prog = barprog(self,
                            orient=HORIZONTAL,
                            max = 50,
                            length=200,
                            mode='determinate')
        bouton = Button(self,
                        text="avancer",
                        command=self.avance)
        self.prog.pack()
        bouton.pack()

    def avance(self):
        self.prog.step(1)

###################################
### Main program initialization ###
###################################

if __name__ == '__main__':
    app = Progrou()
    app.mainloop()
