from .component import Component

class LabelComponent(Component):
    def __init__(self, master, text):
        super().__init__(master)
        self._text = text
        self.create_text()

    def create_text(self):
        self._label = self.get_ttk().Label(
            self.get_root(),
            text=self._text,
            font=("Segoe UI", 12),
            background=self.get_background_color(),
            foreground="#333333"
        )

    def render(self):
        self._label.pack(pady=10, anchor="w", padx=20)
