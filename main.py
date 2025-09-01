from tkinter import Tk
from views.login_page import LoginPage
from views.splash_page import SplashScreenPage

class MainPage:
    def __init__(self):
        self.root = Tk()
        self.root.title("Aplikasi")
        self.root.geometry("400x300")
        self.current_page = None

        self.show_splash()

    def show_splash(self):
        self.current_page = SplashScreenPage(self.root, self.show_login_page)

    def show_login_page(self):
        self.current_page.pack_forget()
        self.current_page = LoginPage(self.root, self)
        self.current_page.render()

    # def show_home_page(self):
    #     self.current_page.pack_forget()
    #     self.current_page = HomePage(self.root, self)

    # def show_other_page(self):
    #     self.current_page.pack_forget()
    #     self.current_page = OtherPage(self.root, self)

    def run(self):
        self.root.mainloop()

main = MainPage()
main.run()
