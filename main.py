from tkinter import Tk
from views.login_page import LoginPage
from views.register_page import RegisterPage
from views.splash_page import SplashScreenPage
from views.enrolment_page import EnrolmentPage
from theme.style_config import setup_styles
from resources.parameters.app_parameters import APP_CONFIG
from db.database import Database
from views.subject_page import SubjectPage

class MainPage:
    def __init__(self):
        self.root = Tk()
        self._initialize_window()
        setup_styles()
        
        # Initialize the database
        self.db = Database()

        # Available pages
        self.pages = {
            "splash": SplashScreenPage,
            "login": LoginPage,
            "register": RegisterPage,
            "enrolment": EnrolmentPage,
            "subjects": SubjectPage, # student landing
            #"admin": AdminPage,           # admin landing
        }


        self.current_page = LoginPage(self.root, controller=self, db=self.db)
        self.navigate("splash")


    def _initialize_window(self):
        self.root.title(APP_CONFIG["title"])
        self.root.configure(bg=APP_CONFIG["background_color"])
        self.root.resizable(False, False) 

    def navigate(self, page_name: str):
        self._clear_current_page()

        page_class = self.pages.get(page_name)
        if not page_class:
            raise ValueError(f"Page '{page_name}' not found.")

        if page_name == "splash":
            self.current_page = page_class(self.root, lambda: self.navigate("login"))
        else:
            self.current_page = page_class(self.root, controller=self, db=self.db)

        self.current_page.pack(fill="both", expand=True)

        if hasattr(self.current_page, "render"):
            self.current_page.render()

        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        min_width = max(width, 700)
        min_height = max(height, 400)
        self.root.geometry(f"{min_width}x{min_height}+100+100")


    def _clear_current_page(self):
        if self.current_page:
            self.current_page.pack_forget()
            self.current_page.destroy()
            self.current_page = None

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainPage()
    app.run()
