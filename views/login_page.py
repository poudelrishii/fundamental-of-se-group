from components.form_field_component import FormField
from components.button_component import ButtonComponent
from views.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller

        self.set_title("Login")
        self.set_background_color("#ffffff")

        self.username_field = FormField(self, "Username")
        self.password_field = FormField(self, "Password")
        self.login_button = ButtonComponent(self, "Submit", self.handle_login)

        self.create_components()
        self.render()

    def create_components(self):
        self.username_field.create_component()
        self.password_field.create_component()

    def render(self):
        self.username_field.render()
        self.password_field.render()
        self.login_button.render()

    def handle_login(self):
        username = self.username_field.get_value()
        password = self.password_field.get_value()
        print(f"Username: {username}, Password: {password}")
