from .component import Component
from parameters.parameters import TEXT_INPUT
import tkinter as tk

class TextInputComponent(Component):
    def __init__(self, master):
        super().__init__(master)
        self._text_box = None
        self.create_text()

    def create_text(self):
        self._text_box = tk.Text(
            self.get_root(),
            height=1,
            width=40,
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#000000",
            bd=1,
            relief="solid"
        )

    def render(self):
        if self._text_box:
            self._text_box.pack(pady=5, padx=20)

    def get_text(self) -> str:
        if self._text_box:
            return self._text_box.get("1.0", tk.END).strip()
        return ""
