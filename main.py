from tkinter import *
from tkinter import ttk

from strings import en as STRINGS

class Main:
    def __init__(self):
        self.root = Tk() 

    def main_view(self):
        frm = ttk.Frame(self.root, padding=100)
        frm.grid()
        ttk.Label(frm, text= STRINGS.APP_TITLE).grid(column=0, row=0)
        self.root.mainloop()

main = Main()
main.main_view()
