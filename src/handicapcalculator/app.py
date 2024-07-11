"""
This is a mobile/desktop application that can calculate an unofficial USGA handicap.
"""

import toga
from .pages import CalculatorPage, LoginPage


class HandicapCalculator(toga.App):
    def startup(self):
        self.calculator_page = CalculatorPage().Frontend().create()
        self.login_page = LoginPage()
        self.login_page_content = self.login_page.create(self.check_login)
        self.main_window = toga.MainWindow(title="Handicap Calculator")
        self.main_window.content = self.login_page_content
        self.main_window.show()

    def check_login(self) -> None:
        print("checking if logged in")
        if self.login_page.logged_in:
            self.main_window.content = self.calculator_page
            self.main_window.show()

def main():
    return HandicapCalculator()
