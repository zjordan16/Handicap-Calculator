"""
This is a mobile/desktop application that can calculate an unofficial USGA handicap.
"""
import toga

from .pages import *


class HandicapCalculator(toga.App):
    def __init__(self):
        # Initialize toga.App
        super().__init__()

        # Initialize app pages
        self.calculator_page: CalculatorPage | None = None
        self.login_page: LoginPage | None = None

        # Initialize app window and content
        self.login_page_content: toga.Box | None = None
        self.main_window: toga.MainWindow
        self.main_window_content: toga.Box
        return

    def startup(self):
        self.calculator_page = CalculatorPage().frontend.create()
        self.login_page = LoginPage()
        self.login_page_content = self.login_page.create(self.check_login)
        self.main_window = toga.MainWindow(title="Handicap Calculator")
        self.main_window.content = self.login_page_content
        self.main_window.show()
        return

    def check_login(self) -> None:
        print("checking if logged in")
        if self.login_page.logged_in:
            self.main_window.content = self.calculator_page
            self.main_window.show()
        return


def main():
    return HandicapCalculator()
