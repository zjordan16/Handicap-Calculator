# 3rd-party libraries
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, BOLD, BOTTOM, RIGHT
# Built-in libraries
from typing import Callable, LiteralString
import os


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
        self.usga_image_file_path: LiteralString | str | bytes | None = None
        self.usga_image: toga.ImageView | None = None

        return

    def create(self, login_action_callback) -> toga.Box:
        self.login_callback = login_action_callback
        # vertical spacing adjusted here (horizontal spacing adjusted in each child box creation method)
        self.content = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, flex=2, padding=(10, 0, 10, 0), height=600))

        # create child boxes
        self.usga_image_file_path = self.get_file_path("WHS.png")
        self.usga_image = self.create_login_image(self.usga_image_file_path)
        self.username_input = self.create_username_input()
        self.password_input = self.create_password_input()
        self.login_failed_message = self.create_login_failed_message()
        self.login_button = self.create_login_button()

        # add children boxes to parent box
        if self.usga_image is not None:
            self.content.add(self.usga_image)
        self.content.add(self.username_input)
        self.content.add(self.password_input)
        self.content.add(self.login_failed_message)
        self.content.add(self.login_button)

        return self.content

    @staticmethod
    def create_username_input() -> toga.Box:
        username_label = toga.Label(
            "Username: ",
            style=Pack(padding=1, flex=1, font_weight=BOLD, font_size=10),
        )
        username_text_input = toga.TextInput(style=Pack(flex=5, font_size=10, width=200))
        username_input_box = toga.Box(style=Pack(direction=ROW, padding=(0, 200, 5, 200), flex=5, width=300))
        username_input_box.add(username_label)
        username_input_box.add(username_text_input)

        return username_input_box

    @staticmethod
    def create_password_input() -> toga.Box:
        password_label = toga.Label(
            "Password: ",
            style=Pack(padding=1, flex=1, font_weight=BOLD, font_size=10),
        )
        password_input = toga.PasswordInput(style=Pack(flex=5, font_size=10, width=200))
        password_input_box = toga.Box(style=Pack(direction=ROW, padding=(0, 200, 0, 200), flex=5, width=300))
        password_input_box.add(password_label)
        password_input_box.add(password_input)

        return password_input_box

    @staticmethod
    def create_login_failed_message() -> toga.Label:
        return toga.Label(
            "Login Failed",
            style=Pack(padding=5, color="red", visibility="hidden", flex=4),
        )

    def create_login_button(self) -> toga.Button:
        return toga.Button(
            "Login",
            on_press=self.validate_login,
            style=Pack(direction=ROW, padding=(1, 1, 20, 1), flex=1, font_size=10, font_weight=BOLD, width=300),
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

    @staticmethod
    def get_file_path(filename: str) -> LiteralString | str | bytes | None:
        filepath: LiteralString | str | bytes | None = None
        try:
            filepath = os.path.join(os.path.dirname(__file__), filename)
        except OSError:
            print(f"Error: {filename} not found.")
        return filepath

    def create_login_image(self, filepath: LiteralString | str | bytes | None) -> toga.ImageView | None:
        try:
            self.usga_image = toga.ImageView(id='images', image=self.usga_image_file_path,
                                             style=Pack(padding=0, flex=50, width=600)
                                             )
        except FileNotFoundError:
            print(f"Error: Failed to load image")
            return None
        return self.usga_image
