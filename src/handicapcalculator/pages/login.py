import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class LoginPage:
    def __init__(self):
        self.login_callback = None
        self.login_failed_message = None
        self.login_button = None
        self.password_input = None
        self.username_input = None
        self.content = None
        self.logged_in = False

    def create(self, login_action_callback) -> toga.Box:
        # TODO: Fix the formatting to make this page look nicer.
        self.login_callback = login_action_callback
        self.content = toga.Box(style=Pack(direction=COLUMN))

        self.username_input = self.create_username_input()
        self.password_input = self.create_password_input()
        self.login_failed_message = self.create_login_failed_message()
        self.content.add(self.username_input)
        self.content.add(self.password_input)
        self.content.add(self.login_failed_message)

        self.login_button = self.create_login_button()
        self.content.add(self.login_button)

        return self.content

    def create_username_input(self) -> toga.Box:
        username_label = toga.Label(
            "Username: ",
            style=Pack(padding=(0, 5), flex=1),
        )
        username_text_input = toga.TextInput(style=Pack(flex=2))
        username_input_box = toga.Box(style=Pack(direction=ROW, padding=5, flex=2))
        username_input_box.add(username_label)
        username_input_box.add(username_text_input)

        return username_input_box

    def create_password_input(self) -> toga.Box:
        password_label = toga.Label(
            "Password: ",
            style=Pack(padding=(0, 5), flex=1),
        )
        password_input = toga.PasswordInput(style=Pack(flex=2))
        password_input_box = toga.Box(style=Pack(direction=ROW, padding=5, flex=2))
        password_input_box.add(password_label)
        password_input_box.add(password_input)

        return password_input_box

    def create_login_failed_message(self) -> toga.Box:
        return toga.Label(
            "Login Failed",
            style=Pack(padding=(0, 5), color="red", visibility="hidden", flex=1),
        )

    def create_login_button(self) -> toga.Button:
        return toga.Button(
            "Login",
            on_press=self.validate_login,
            style=Pack(padding=5, flex=1),
        )

    # We have to keep the second argument 'o'. I'm not exactly sure why, but it causes errors when this function
    # is called if we don't have the second argument present.
    # TODO: Figure out why that happens and fix it.
    def validate_login(self, o) -> None:
        username = self.username_input.children[1].value
        password = self.password_input.children[1].value
        if self.check_login_credentials(username, password):
            self.login_failed_message.style.visibility = "hidden"
            self.logged_in = True
            self.login_callback()
        else:
            self.login_failed_message.style.visibility = "visible"
            self.logged_in = False

    def check_login_credentials(self, username, password) -> bool:
        return True if username == "user" and password == "password" else False
