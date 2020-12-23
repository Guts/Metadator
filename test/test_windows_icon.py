import Tkinter
from Tkinter import Tk

root = Tk()
imgif = Tkinter.Image("photo", file="../data/img/icon_AddContact_np10888.gif")
imicon = "../Metadator.ico"
root.iconbitmap(imicon)
root.tk.call('wm','iconphoto',root._w,imgif)

root.mainloop()