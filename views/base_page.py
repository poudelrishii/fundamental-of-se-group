from tkinter import *

class BasePage(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.pack(fill=BOTH, expand=True)
        self.title_label = None

    def clear_page(self):
        for widget in self.winfo_children():
            if widget != self.title_label:
                widget.destroy()

    def set_background_color(self, color="#f0f0f0"):
        self.configure(bg=color)

    def set_title(self, text, font=("Arial", 16), pady=20):
        if self.title_label:
            self.title_label.config(text=text)
        else:
            self.title_label = Label(self, text=text, font=font, bg=self["bg"])
            self.title_label.pack(pady=pady)
