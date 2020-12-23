#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julien
#
# Created:     10/07/2012
# Copyright:   (c) Julien 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

class BarreProg():
      """ Petite fenêtre de progression """
      def __init__(self, num_shp, tot_shp):
          self.root = Tk()
          self.root.title('Traitement de Metadator en cours')
          self.lb_nomshp = Label(self.root, \
                              text = 'Shape en cours de traitement : ')
          self.lb_numshp = Label(self.root, \
                              text =  str(num_shp) + \
                                      ' sur ' + \
                                      str(tot_shp))

##          self.lb_numchp = Label(self.root, \
##                                 text = 'Champ n°' + \
##                                 str(nb_chp) + \
##                                 ' sur ' +\
##                                 str(tot_chp))

          self.lb_nomshp.pack()
          self.lb_numshp.pack()
##          self.lb_numchp.pack()
          self.root.mainloop()

      def maj_shp(self, num):
            self.root.update()

      def fin(self):
          self.root.destroy()



# Programme principal :
if __name__ == '__main__':
   from Tkinter import *
   f = BarreProg(num_shp= 15,  tot_shp = 25) # instanciation de l'objet application