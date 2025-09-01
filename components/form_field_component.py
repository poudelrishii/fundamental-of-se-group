from .component import Component
from .label_component import LabelComponent
from .text_input_component import TextInputComponent

class FormField(Component):
    def __init__(self, master, label_text):
        super().__init__(master)
        self.label = LabelComponent(master, label_text)
        self.text_input = TextInputComponent(master)

    def create_component(self):
        self.label.create_text()
        self.text_input.create_text()

    def render(self):
        self.label.render()
        self.text_input.render()

    def get_value(self):
        return self.text_input.get_text()
