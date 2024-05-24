"""
This is a mobile/desktop application that can calculate an unofficial USGA handicap.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class HandicapCalculator(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        # Create Inputs
        self.course_name_input = self.create_course_name_input()
        self.score_input = self.create_score_input()
        self.course_slope_input = self.create_slope_input()
        self.course_rating_input = self.create_course_rating_input()

        # Create button to save inputs
        save_round_button = toga.Button(
            "Save Round Information",
            on_press=self.save_score,
            style=Pack(padding=5),
        )

        # Add inputs to main box
        main_box.add(self.course_name_input)
        main_box.add(self.score_input)
        main_box.add(self.course_slope_input)
        main_box.add(self.course_rating_input)
        main_box.add(save_round_button)

        # Create table to show saved rounds
        self.score_history_table = self.create_score_history_table()

        # Add table to main box
        main_box.add(self.score_history_table)

        self.main_window = toga.MainWindow(title="Handicap Calculator")
        self.main_window.content = main_box
        self.main_window.show()

    def save_score(self, widget):
        # TODO: Validate that all the inputs have a value. Show an error to user and mark them as required if not.
        # Add inputs to table
        self.score_history_table.data.append(
            (
                self.course_name_input.children[1].value,
                self.score_input.children[1].value,
                self.course_slope_input.children[1].value,
                self.course_rating_input.children[1].value,
            )
        )

        # Clear inputs
        self.course_name_input.children[1].value = None
        self.score_input.children[1].value = None
        self.course_slope_input.children[1].value = None
        self.course_rating_input.children[1].value = None

    def create_course_name_input(self) -> toga.Box:
        course_name_label = toga.Label(
            "Course Name: ",
            style=Pack(padding=(0, 5)),
        )
        course_name_text_input = toga.TextInput(style=Pack(flex=1))
        course_name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        course_name_box.add(course_name_label)
        course_name_box.add(course_name_text_input)

        return course_name_box

    def create_score_input(self) -> toga.Box:
        score_name_label = toga.Label(
            "Net Score: ",
            style=Pack(padding=(0, 5)),
        )
        score_input = toga.NumberInput(min_value=1, step=1)
        score_box = toga.Box(style=Pack(direction=ROW, padding=5))
        score_box.add(score_name_label)
        score_box.add(score_input)

        return score_box

    def create_slope_input(self) -> toga.Box:
        slope_label = toga.Label(
            "Course Slope Rating: ",
            style=Pack(padding=(0, 5)),
        )
        slope_input = toga.NumberInput(min_value=55, max_value=155, step=1)
        slope_box = toga.Box(style=Pack(direction=ROW, padding=5))
        slope_box.add(slope_label)
        slope_box.add(slope_input)

        return slope_box

    def create_course_rating_input(self) -> toga.Box:
        course_rating_label = toga.Label(
            "Course Rating: ",
            style=Pack(padding=(0, 5)),
        )
        course_rating_input = toga.NumberInput(min_value=55, max_value=85, step=0.1)
        course_rating_box = toga.Box(style=Pack(direction=ROW, padding=5))
        course_rating_box.add(course_rating_label)
        course_rating_box.add(course_rating_input)

        return course_rating_box

    def create_score_history_table(self) -> toga.Table:
        return toga.Table(headings=["Course Name", "Net Score", "Course Rating", "Course Slope Rating"])

def main():
    return HandicapCalculator()
