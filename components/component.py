from tkinter import *
from tkinter import ttk

class Component:
    def __init__(self, master):
        self._master = master
        self._ttk = ttk
        self._bg_color = self._resolve_background()

    def get_root(self):
        return self._master

    def get_ttk(self):
        return self._ttk

    def get_background_color(self):
        return self._bg_color

    def _resolve_background(self):
        try:
            return self._master["bg"]
        except (KeyError, TclError):
            return "#f0f0f0"
