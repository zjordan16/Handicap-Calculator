# 3rd-party libraries
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, BOLD, RIGHT, BOTTOM, LEFT
# Built-in libraries
from typing import Callable
import os
# User-defined libraries


class LoginPage:
    def __init__(self):
        """
        Type annotation: Callable[param1, param2]

        Description: Used to type annotate callable methods, takes input as list of types of method parameters
        & type of return values

        Example callable method: method_name(paramType1, paramType2) -> return_type

        param1: List of method parameter Types, [paramType1, paramType2]
        param2: Type of the return value, return_Type
        """
        self.login_callback: Callable[[], None] | None= None
        self.login_failed_message: toga.Label | None = None
        self.login_button: toga.Button | None = None
        self.password_input: toga.PasswordInput | None = None
        self.username_input: toga.TextInput | None = None
        self.content: toga.Box | None = None
        self.logged_in: bool = False
        return

    def create(self, login_action_callback) -> toga.Box:
        # TODO: Add USGA logo to login page above login boxes
        self.login_callback = login_action_callback
        self.content = toga.Box(style=Pack(direction=COLUMN))

        self.username_input = self.create_username_input()
        self.password_input = self.create_password_input()
        self.login_failed_message = self.create_login_failed_message()
        # Ignore this attempt it is trash and I will fix it later (I have no idea how their ImageView() call works)
        try:
            image_dir = os.path.dirname(__file__)
            image_path = os.path.join(image_dir, 'WHS.png')
            self.image_usga = toga.ImageView(id='images', image=image_path)
            self.content.add(self.image_usga)
            # view = toga.ImageView(self.image_usga)
        except FileNotFoundError:
            print("File not found")
            pass
        self.content.add(self.username_input)
        self.content.add(self.password_input)
        self.content.add(self.login_failed_message)

        self.login_button = self.create_login_button()
        self.content.add(self.login_button)

        return self.content

    @staticmethod
    def create_username_input() -> toga.Box:
        username_label = toga.Label(
            "Username: ",
            style=Pack(padding=(300, 0, 5, 175), flex=1, width=100, font_weight=BOLD, font_size=10),
        )
        username_text_input = toga.TextInput(style=Pack(flex=2, font_size=10))
        username_input_box = toga.Box(style=Pack(direction=ROW, padding=5, flex=0, width=467, alignment=BOTTOM))
        username_input_box.add(username_label)
        username_input_box.add(username_text_input)

        return username_input_box

    @staticmethod
    def create_password_input() -> toga.Box:
        password_label = toga.Label(
            "Password: ",
            style=Pack(padding=(0, 0, 5, 175), flex=1, width=100, font_weight=BOLD, font_size=10),
        )
        password_input = toga.PasswordInput(style=Pack(flex=2, font_size=10))
        password_input_box = toga.Box(style=Pack(direction=ROW, padding=5, flex=0, width=467, alignment=CENTER))
        password_input_box.add(password_label)
        password_input_box.add(password_input)

        return password_input_box

    @staticmethod
    def create_login_failed_message() -> toga.Label:
        return toga.Label(
            "Login Failed",
            style=Pack(padding=(0, 5), color="red", visibility="hidden", flex=1),
        )

    def create_login_button(self) -> toga.Button:
        return toga.Button(
            "Login",
            on_press=self.validate_login,
            style=Pack(direction=ROW, padding=(5,20,20,175), flex=2, width=300, alignment=CENTER, font_size=10, font_weight=BOLD),
        )

    def validate_login(self, _widget) -> None:
        username = self.username_input.children[1].value
        password = self.password_input.children[1].value
        if self.check_login_credentials(username, password):
            self.login_failed_message.style.visibility = "hidden"
            self.logged_in = True
            self.login_callback()
        else:
            self.login_failed_message.style.visibility = "visible"
            self.logged_in = False

    @staticmethod
    def check_login_credentials(username, password) -> bool:
        return True if username == "user" and password == "password" else False
