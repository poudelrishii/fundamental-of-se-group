from components.label_component import LabelComponent
from components.progress_bar_component import ProgressBarComponent
from views.base_page import BasePage

class SplashScreenPage(BasePage):
    def __init__(self, master, on_finish_callback):
        super().__init__(master)
        self._on_finish = on_finish_callback

        self.set_background_color("#ffffff")
        self.create_component()
        self.render()

        self.after(2500, self.finish_splash)

    def create_component(self):
        self.label = LabelComponent(self, "Loading...")
        self.progress = ProgressBarComponent(self)

    def render(self):
        self.label.render()
        self.progress.render()

    def finish_splash(self):
        self.pack_forget()
        self._on_finish()
