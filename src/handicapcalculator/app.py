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
        self.invalid_inputs_message = self.create_invalid_inputs_message()

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
        main_box.add(self.invalid_inputs_message)
        main_box.add(save_round_button)

        # Create table to show saved rounds
        self.score_history_table = self.create_score_history_table()
        main_box.add(self.score_history_table)

        # Create display for handicap
        self.handicap_display = self.create_handicap_display()
        main_box.add(self.handicap_display)

        self.main_window = toga.MainWindow(title="Handicap Calculator")
        self.main_window.content = main_box
        self.main_window.show()

    def save_score(self, widget):
        inputs_are_valid = (
            self.course_name_input.children[1].value and self.score_input.children[1].value and self.course_slope_input.children[1].value and self.course_rating_input.children[1].value
        )
        if inputs_are_valid:
            # Get Inputs
            course_name = self.course_name_input.children[1].value
            adjusted_gross_score = self.score_input.children[1].value
            slope = self.course_slope_input.children[1].value
            rating = self.course_rating_input.children[1].value
            differential = self.calculate_round_differential(adjusted_gross_score, slope, rating)

            self.score_history_table.data.append((course_name, adjusted_gross_score, slope, rating, differential))

            # Refresh handicap
            self.refresh_handicap_index()

            # Clear inputs
            self.invalid_inputs_message.style.visibility = "hidden"
            self.course_name_input.children[1].value = None
            self.score_input.children[1].value = None
            self.course_slope_input.children[1].value = None
            self.course_rating_input.children[1].value = None
        else:
            self.invalid_inputs_message.style.visibility = "visible"

    def create_course_name_input(self) -> toga.Box:
        course_name_label = toga.Label(
            "Course Name: ",
            style=Pack(padding=(0, 5)),
        )
        course_name_text_input = toga.TextInput(style=Pack(flex=1))
        course_name_box = toga.Box(style=Pack(direction=ROW, padding=5, flex=1))
        course_name_box.add(course_name_label)
        course_name_box.add(course_name_text_input)

        return course_name_box

    def create_score_input(self) -> toga.Box:
        score_name_label = toga.Label(
            "Adjusted Gross Score: ",
            style=Pack(padding=(0, 5)),
        )
        score_input = toga.NumberInput(min=1, step=1)
        score_box = toga.Box(style=Pack(direction=ROW, padding=5, flex=1))
        score_box.add(score_name_label)
        score_box.add(score_input)

        return score_box

    def create_slope_input(self) -> toga.Box:
        slope_label = toga.Label(
            "Course Slope Rating: ",
            style=Pack(padding=(0, 5)),
        )
        slope_input = toga.NumberInput(min=55, max=155, step=1)
        slope_box = toga.Box(style=Pack(direction=ROW, padding=5, flex=1))
        slope_box.add(slope_label)
        slope_box.add(slope_input)

        return slope_box

    def create_course_rating_input(self) -> toga.Box:
        course_rating_label = toga.Label(
            "Course Rating: ",
            style=Pack(padding=(0, 5)),
        )
        course_rating_input = toga.NumberInput(min=55, max=85, step=0.1)
        course_rating_box = toga.Box(style=Pack(direction=ROW, padding=5, flex=1))
        course_rating_box.add(course_rating_label)
        course_rating_box.add(course_rating_input)

        return course_rating_box

    def create_score_history_table(self) -> toga.Table:
        return toga.Table(
            headings=["Course Name", "Adjusted Gross Score", "Course Rating", "Course Slope Rating", "Round Differential"],
            style=Pack(flex=5)
        )

    def create_invalid_inputs_message(self) -> toga.Label:
        return toga.Label(
            "Please provide a value for all four inputs!",
            style=Pack(padding=(0, 5), color="red", visibility="hidden", flex=1),
        )

    def create_handicap_display(self) -> toga.Box:
        self.calculate_handicap_index()
        handicap_label = toga.Label(
            f"Handicap Index: {self.handicap_index}",
            style=Pack(flex=1, color="blue", text_align="center"),
        )
        handicap_box = toga.Box(style=Pack(flex=2, alignment="center"))
        handicap_box.add(handicap_label)

        return handicap_box

    def calculate_round_differential(self, adjusted_gross_score: int, slope: int, rating: float) -> float:
        return round((adjusted_gross_score - rating) * 113 / slope, 1)

    def calculate_handicap_index(self) -> float:
        # TODO: implement overall handicap index calculation logic
        self.handicap_index = "N/A"

    def refresh_handicap_index(self) -> None:
        self.calculate_handicap_index()
        self.handicap_display.children[0].text = f"Handicap Index: {self.handicap_index}"

def main():
    return HandicapCalculator()
