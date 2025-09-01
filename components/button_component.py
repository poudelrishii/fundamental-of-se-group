from .component import Component

class ButtonComponent(Component):
    def __init__(self, master, name, action):
        super().__init__(master)
        self._name = name
        self._action = action
        self.create_button()

    def create_button(self):
        self._btn = self.get_ttk().Button(
            self.get_root(),
            text=self._name,
            command=self._action
        )


    def render(self):
        self._btn.pack(pady=20, ipadx=10, ipady=5)
