from .component import Component

class ProgressBarComponent(Component):
    def __init__(self, master, value=0, interval=30, step=2):
        super().__init__(master)
        self._value = value
        self._interval = interval
        self._step = step

        self.progress = self.get_ttk().Progressbar(
            self.get_root(),
            orient="horizontal",
            length=200,
            mode="determinate"
        )

    def render(self):
        self.progress.pack(pady=10)
        self.start_loading()

    def start_loading(self):
        self._update()

    def _update(self):
        if self._value < 100:
            self._value += self._step
            self.progress['value'] = self._value
            self.get_root().after(self._interval, self._update)

    def reset(self):
        self._value = 0
        self.progress['value'] = 0

    def set_value(self, value):
        self._value = value
        self.progress['value'] = value
