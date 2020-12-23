import ttk
import Tkinter

root = Tkinter.Tk()

##style1 = ttk.Style()
##style1.layout("TMenubutton", [
##   ("Menubutton.background", None),
##   ("Menubutton.button", {"children":
##       [("Menubutton.focus", {"children":
##           [("Menubutton.padding", {"children":
##               [("Menubutton.label", {"side": "left", "expand": 1})]
##           })]
##       })]
##   }),
##])
##
##mbtn = ttk.Menubutton(text='Text')
##mbtn.pack()


style2 = ttk.Style()
style2.map("C.TButton",
    foreground=[('pressed', 'red'), ('active', 'blue')],
    background=[('pressed', '!disabled', 'green'), ('active', 'purple'), ('background', 'black')]
    )

colored_btn = ttk.Button(text="Test", style="C.TButton").pack()

b = ttk.Button(root, text='Hello', style='Fun.TButton')


b.pack()

style2.theme_use('clam')

##style3 = ttk.Style()
##style3.theme_settings("default", {
##   "TCombobox": {
##       "configure": {"padding": 5},
##       "map": {
##           "background": [("active", "green2"),
##                          ("!disabled", "green4")],
##           "fieldbackground": [("!disabled", "green3")],
##           "foreground": [("focus", "OliveDrab1"),
##                          ("!disabled", "OliveDrab2")]
##       }
##   }
##})
##
##combo = ttk.Combobox().pack())

print style2.element_options('Button.label')
print style2.element_options('TCombobox.label')

root.mainloop()