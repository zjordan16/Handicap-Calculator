import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class LoginPage:
    def create(self, login_action) -> toga.Box:
        main_box = toga.Box(style=Pack(direction=COLUMN))

        self.username_input = self.create_username_input()
        self.password_input = self.create_password_input()
        main_box.add(self.username_input)
        main_box.add(self.password_input)

        self.login_button = self.create_login_button(calculator_page)
        main_box.add(self.login_button)

        return main_box

    def create_username_input(self) -> toga.Box:
        username_label = toga.Label(
            "Username: ",
            style=Pack(padding=(0, 5)),
        )
        username_text_input = toga.TextInput(style=Pack(flex=1))
        username_input_box = toga.Box(style=Pack(direction=ROW, padding=5, flex=1))
        username_input_box.add(username_label)
        username_input_box.add(username_text_input)

        return username_input_box

    def create_password_input(self) -> toga.Box:
        password_label = toga.Label(
            "Password: ",
            style=Pack(padding=(0, 5)),
        )
        password_input = toga.PasswordInput(style=Pack(flex=1))
        password_input_box = toga.Box(style=Pack(direction=ROW, padding=5, flex=1))
        password_input_box.add(password_label)
        password_input_box.add(password_input)

        return password_input_box

    def validate_login(self) -> bool:
        return True
