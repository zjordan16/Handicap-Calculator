"""
This is a mobile/desktop application that can calculate an unofficial USGA handicap.
"""
# 3rd-party libraries
import toga
# Built-in libraries
from typing import Optional
# User-defined libraries
from .pages import *


class HandicapCalculator(toga.App):
    def __init__(self):
        super().__init__()
        self.calculator_page: Optional[CalculatorPage] = None
        self.login_page: Optional[LoginPage] = None
        self.login_page_content: Optional[toga.Box] = None
        self.main_window: toga.MainWindow
        self.main_window_content: toga.Box
        return

    def startup(self):
        self.calculator_page = CalculatorPage().Frontend().create()
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
