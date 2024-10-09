import os
from datetime import datetime

import polars as pl
import toga
from dateutil.parser import parse
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .login import LoginPage


class CalculatorPage:
    def __init__(self) -> None:
        self.backend = self.Backend(self)
        self.backend.parent = self
        self.frontend = self.Frontend(self)
        self.frontend.parent = self

    # Frontend Inner Class
    class Frontend:
        def __init__(self, parent) -> None:
            self.parent: CalculatorPage = parent
            self.backend: CalculatorPage.Backend = parent.backend
            self.login_page: LoginPage = LoginPage()

            self.score_history_table: toga.Table | None = None
            self.content: toga.Box = toga.Box()
            self.handicap_display: toga.Box = toga.Box()
            self.invalid_inputs_message: toga.Label = toga.Label("")
            self.course_rating_input: toga.Box = toga.Box()
            self.course_slope_input: toga.Box = toga.Box()
            self.score_input: toga.Box = toga.Box()
            self.date_input: toga.Box = toga.Box()
            self.course_name_input: toga.Box = toga.Box()
            self.scorecap_display: toga.Box = toga.Box()
            return

        def create(self) -> toga.Box:
            self.content = toga.Box(style=Pack(direction=COLUMN))

            # Create Inputs
            self.course_name_input = self.create_course_name_input()
            self.date_input = self.create_date_input()
            self.score_input = self.create_score_input()
            self.course_slope_input = self.create_slope_input()
            self.course_rating_input = self.create_course_rating_input()
            self.invalid_inputs_message = self.create_invalid_inputs_message()

            # Create button to save inputs
            save_round_button: toga.Button = toga.Button("Save Round Information",
                                                         on_press=self.save_score,  # type: ignore
                                                         style=Pack(padding=5),
                                                         )

            # Add inputs to main box
            self.content.add(self.course_name_input)
            self.content.add(self.date_input)
            self.content.add(self.score_input)
            self.content.add(self.course_rating_input)
            self.content.add(self.course_slope_input)
            self.content.add(self.invalid_inputs_message)
            self.content.add(save_round_button)

            # Create table to show saved rounds
            self.score_history_table = self.create_score_history_table()
            self.content.add(self.score_history_table)
            self.display_table()

            # Create display for handicap
            self.handicap_display = self.create_handicap_display()
            self.content.add(self.handicap_display)

            # Create display for soft and hard cap
            self.scorecap_display = self.create_scorecap_display()
            self.content.add(self.scorecap_display)

            return self.content

        @staticmethod
        def create_course_name_input() -> toga.Box:
            course_name_label: toga.Label = toga.Label("Course Name: ",
                                                       style=Pack(padding=(0, 5), flex=1),
                                                       )
            course_name_text_input: toga.TextInput = toga.TextInput(style=Pack(flex=2))
            course_name_box: toga.Box = toga.Box(style=Pack(direction=ROW, padding=5, flex=1))
            course_name_box.add(course_name_label)
            course_name_box.add(course_name_text_input)

            return course_name_box

        @staticmethod
        def create_score_input() -> toga.Box:
            score_name_label: toga.Label = toga.Label("Adjusted Gross Score: ",
                                                      style=Pack(padding=(0, 5), flex=1),
                                                      )
            score_input: toga.NumberInput = toga.NumberInput(min=1, step=1, style=Pack(flex=2))  # type: ignore
            score_box: toga.Box = toga.Box(style=Pack(direction=ROW, padding=5, flex=1))
            score_box.add(score_name_label)
            score_box.add(score_input)

            return score_box

        @staticmethod
        def create_slope_input() -> toga.Box:
            slope_label: toga.Label = toga.Label("Course Slope Rating: ",
                                                 style=Pack(padding=(0, 5), flex=1),
                                                 )
            slope_input: toga.NumberInput = toga.NumberInput(min=55,  # type: ignore
                                                             max=155,  # type: ignore
                                                             step=1,
                                                             style=Pack(flex=2)
                                                             )

            slope_box: toga.Box = toga.Box(style=Pack(direction=ROW, padding=5, flex=1))
            slope_box.add(slope_label)
            slope_box.add(slope_input)

            return slope_box

        @staticmethod
        def create_course_rating_input() -> toga.Box:
            course_rating_label: toga.Label = toga.Label("Course Rating: ",
                                                         style=Pack(padding=(0, 5), flex=1),
                                                         )
            course_rating_input: toga.NumberInput = toga.NumberInput(min=55,  # type: ignore
                                                                     max=85,  # type: ignore
                                                                     step=0.1,
                                                                     style=Pack(flex=2)
                                                                     )
            course_rating_box: toga.Box = toga.Box(style=Pack(direction=ROW, padding=5, flex=1))
            course_rating_box.add(course_rating_label)
            course_rating_box.add(course_rating_input)

            return course_rating_box

        @staticmethod
        def create_date_input() -> toga.Box:
            date_label: toga.Label = toga.Label("Date (mm/dd): ",
                                                style=Pack(padding=(0, 5), flex=1),
                                                )
            date_input: toga.TextInput = toga.TextInput(style=Pack(flex=2))
            date_box: toga.Box = toga.Box(style=Pack(direction=ROW, padding=5, flex=1))
            date_box.add(date_label)
            date_box.add(date_input)

            return date_box

        @staticmethod
        def create_score_history_table() -> toga.Table:
            return toga.Table(headings=["Course Name", "Date", "Adjusted Gross Score", "Course Rating",
                                        "Course Slope Rating", "Round Differential"],
                              style=Pack(flex=5)
                              )

        @staticmethod
        def create_invalid_inputs_message() -> toga.Label:
            return toga.Label("Please provide a value for all inputs!",
                              style=Pack(padding=(0, 5), color="red", visibility="hidden", flex=1),
                              )

        def create_handicap_display(self) -> toga.Box:
            self.backend.calculate_handicap_index()
            handicap_label: toga.Label = toga.Label(f"Handicap Index: {self.backend.handicap_index}",
                                                    style=Pack(flex=1, color="blue", text_align="center"),
                                                    )
            handicap_box: toga.Box = toga.Box(style=Pack(flex=2, alignment="center"))
            handicap_box.add(handicap_label)
            return handicap_box

        def create_scorecap_display(self) -> toga.Box:
            scorecap_label: toga.Label = toga.Label(f"{self.backend.scorecap}",
                                                    style=Pack(flex=1, color="blue", text_align="center"),
                                                    )
            scorecap_box: toga.Box = toga.Box(style=Pack(flex=2, alignment="center"))
            scorecap_box.add(scorecap_label)
            return scorecap_box

        def display_table(self) -> None:
            self.score_history_table.data.clear()
            csv_file: str = self.backend.declare_csv_directory()
            if os.path.exists(csv_file):
                # read newest 20 rows from csv
                lf: pl.lazyframe = pl.scan_csv(csv_file).tail(20).collect()
                # loop displays newest 20 games to table from newest to oldest
                for row in reversed(list(lf.iter_rows(named=True))):
                    self.score_history_table.data.append(
                        [
                            str(row[lf.columns[0]]),
                            str(row[lf.columns[1]]),
                            str(row[lf.columns[2]]),
                            str(row[lf.columns[3]]),
                            str(row[lf.columns[4]]),
                            str(row[lf.columns[5]])
                        ]
                    )
            else:
                # display blank table
                self.score_history_table.data.clear()
            return

        def refresh_handicap_index(self) -> None:
            self.backend.calculate_handicap_index()
            self.handicap_display.children[0].text = f"Handicap Index: {self.backend.handicap_index}"
            self.scorecap_display.children[0].text = f"{self.backend.scorecap}"
            return

        def save_score(self, widget: toga.Button) -> None:
            inputs_are_valid = (self.course_name_input.children[1].value and
                                self.score_input.children[1].value and
                                self.course_slope_input.children[1].value and
                                self.course_rating_input.children[1].value and
                                self.date_input.children[1].value
                                )
            if inputs_are_valid:
                # Get Inputs
                course_name: str = self.course_name_input.children[1].value
                date: str = parse(self.date_input.children[1].value).strftime("%Y-%m-%d")
                adjusted_gross_score: int = self.score_input.children[1].value
                rating: float = self.course_rating_input.children[1].value
                slope: int = self.course_slope_input.children[1].value
                differential: float = self.backend.calculate_round_differential(adjusted_gross_score,
                                                                                rating,
                                                                                slope
                                                                                )
                # Write inputs to CSV
                self.backend.write_to_csv(course_name, date, adjusted_gross_score,
                                          rating, slope, differential
                                          )
                # Refresh handicap and table
                self.refresh_handicap_index()
                self.display_table()
                # Clear inputs
                self.invalid_inputs_message.style.visibility = "hidden"
                self.course_name_input.children[1].value = None
                self.date_input.children[1].value = None
                self.score_input.children[1].value = None
                self.course_slope_input.children[1].value = None
                self.course_rating_input.children[1].value = None
            else:
                self.invalid_inputs_message.style.visibility = "visible"

            return

    # Backend Inner Class
    class Backend:
        def __init__(self, parent) -> None:
            self.parent: CalculatorPage = parent

            self.handicap_index: str | float = ""
            self.scorecap: str = ""
            return

        @staticmethod
        def calculate_round_differential(adjusted_gross_score: int, rating: float, slope: int) -> float:
            return round(((113 / slope) * (adjusted_gross_score - rating)), 1)

        @staticmethod
        def declare_csv_directory() -> str:
            file_directory: str = os.path.dirname(__file__)
            os.makedirs(file_directory, exist_ok=True)

            return os.path.join(file_directory, "score_history_table.csv")

        def write_to_csv(self, course_name: str, date: str, adjusted_gross_score: int, rating: float, slope: int,
                         differential: float) -> None:
            # declare new_data as dictionary for polars, typecast to match datatypes with polars dataframe
            new_data: dict = {"course_name": course_name, "date": date,
                              "adjusted_gross_score": int(adjusted_gross_score),
                              "rating": float(rating),
                              "slope": int(slope),
                              "differential": float(differential)
                              }
            # Declare file directory for csv
            csv_file: str = self.declare_csv_directory()

            # Check if CSV exists, append if exists, create new if it doesn't
            if os.path.exists(csv_file):
                # Scan reads dataframes in lazy mode, pl.LazyFrame() creates new dataframe in lazy mode,
                # concat() combines frames
                existing_lf: pl.lazyframe = pl.scan_csv(csv_file)
                new_lf: pl.lazyframe = pl.LazyFrame(new_data,
                                                    schema={"course_name": pl.Utf8,
                                                            "date": pl.Utf8,
                                                            "adjusted_gross_score": pl.Int64,
                                                            "rating": pl.Float64,
                                                            "slope": pl.Int64,
                                                            "differential": pl.Float64}
                                                    )
                lf: pl.lazyframe.frame = pl.concat([existing_lf, new_lf])
            else:
                lf: pl.lazyframe = pl.LazyFrame(new_data, schema={"course_name": pl.Utf8,
                                                                  "date": pl.Utf8,
                                                                  "adjusted_gross_score": pl.Int64,
                                                                  "rating": pl.Float64,
                                                                  "slope": pl.Int64,
                                                                  "differential": pl.Float64
                                                                  }
                                                )

            # Write new data to list in csv
            # Collect() converts lazy frame to dataframe to read data; lazy() converts dataframe back to lazy frame
            df: pl.lazyframe = lf.collect().sort(by="date", descending=False).lazy()
            df.sink_csv(csv_file)

            return

        def calculate_handicap_index(self) -> None:
            # -100 used as flag for invalid cases of handicap index
            current_handicap_index: float = -100.0
            used_differentials: int

            current_handicap_index, used_differentials = self.calculate_current_handicap()
            print("Current HI: ", current_handicap_index)
            low_handicap_index: float = self.calculate_low_handicap_index(current_handicap_index, used_differentials)
            print("Low HI: ", low_handicap_index)

            soft_cap: bool
            hard_cap: bool

            current_handicap_index, soft_cap, hard_cap = self.limit_on_upward_movement(current_handicap_index,
                                                                                       low_handicap_index)

            # Display handicap index to GUI
            if current_handicap_index == -100:
                self.handicap_index = "N/A"
            else:
                self.handicap_index = current_handicap_index
                if soft_cap:
                    self.scorecap = "Soft-Cap Triggered"
                elif hard_cap:
                    self.scorecap = "Hard-Cap Triggered"
                else:
                    self.scorecap = ""

            return

        def calculate_current_handicap(self) -> tuple[float, int]:
            used_rounds, adjustment = self.calculate_rounds_to_use()

            if used_rounds > 0:
                csv_file = self.declare_csv_directory()
                df = pl.scan_csv(csv_file).collect()

                # If more than 20 total rounds, just use recent 20 for calculations
                if df.height > 20:
                    df = df.tail(20)

                df = df.sort("differential", descending=True).tail(used_rounds) \
                    .select(["differential"])
                # USGA rounds handicaps to one decimal
                handicap = round(df.mean().item(), 1)
                used_differentials = len(df)
            else:
                handicap = -100
                used_differentials = 0

            # Account for handicap adjustment
            handicap += adjustment

            # Set maximum allowable handicap index per USGA 5.3 Maximum Handicap Index
            if handicap > 54.0:
                handicap = 54
            else:
                pass

            return handicap, used_differentials

        def calculate_rounds_to_use(self) -> tuple[int, float]:
            total_rounds = 0
            csv_file = self.declare_csv_directory()

            # Calculates total rounds using lazy execution in polars
            if os.path.exists(csv_file):
                lf = pl.scan_csv(csv_file)
                total_rounds = lf.select(pl.len()).collect().item()
            else:
                total_rounds = 0

            # Logic for used rounds according to table 5.2a of USGA "Calculation of a Handicap Index"
            if total_rounds <= 0:
                used_rounds = 0
                adjustment = 0.0
            elif total_rounds <= 3:
                used_rounds = 1
                adjustment = -2.0
            elif total_rounds <= 4:
                used_rounds = 1
                adjustment = -1.0
            elif total_rounds <= 5:
                used_rounds = 1
                adjustment = 0.0
            elif total_rounds <= 6:
                used_rounds = 2
                adjustment = -1.0
            elif total_rounds <= 8:
                used_rounds = 2
                adjustment = 0.0
            elif total_rounds <= 11:
                used_rounds = 3
                adjustment = 0.0
            elif total_rounds <= 14:
                used_rounds = 4
                adjustment = 0.0
            elif total_rounds <= 16:
                used_rounds = 5
                adjustment = 0.0
            elif total_rounds <= 18:
                used_rounds = 6
                adjustment = 0.0
            elif total_rounds <= 19:
                used_rounds = 7
                adjustment = 0.0
            else:
                used_rounds = 8
                adjustment = 0.0

            return int(used_rounds), float(adjustment)

        def calculate_low_handicap_index(self, current_handicap: float, used_differentials: int) -> float:
            GROUP_SIZE: int = 20
            low_handicap_index = float('inf')
            csv_file = self.declare_csv_directory()
            date = self.get_date_one_year_ago()

            # Run query
            # Only need to iterate through data if list > 20 rows (i.e. 8 or more differentials get used)
            if used_differentials >= 8:
                if os.path.exists(csv_file):
                    df = pl.scan_csv(csv_file).filter(pl.col('date') >= date)
                    df = df.sort('date', descending=True).collect()
                    for i in range(len(df) - GROUP_SIZE + 1):
                        group = df.slice(i, GROUP_SIZE)
                        if len(group) == GROUP_SIZE:
                            low_8 = group.sort('differential').head(8)
                            mean_low_8 = low_8.select(pl.col('differential').mean())[0, 0]
                            if mean_low_8 < low_handicap_index:
                                low_handicap_index = mean_low_8
                else:
                    low_handicap_index = -100
            else:
                low_handicap_index = current_handicap

            # Set maximum allowable handicap index per USGA 5.3 Maximum Handicap Index
            if low_handicap_index > 54.0:
                low_handicap_index = 54.0
            else:
                pass

            return round(low_handicap_index, 1) if low_handicap_index != float('inf') else -100

        def get_date_one_year_ago(self) -> str:
            csv_file = self.declare_csv_directory()

            if os.path.exists(csv_file):
                df = pl.scan_csv(csv_file).select(pl.col("date")).tail(1).collect()
                current_date = df[0, "date"]

                # get previous date
                date_obj = datetime.strptime(current_date, "%Y-%m-%d")
                prev_date: datetime | str = date_obj.replace(year=date_obj.year - 1)
                prev_date = prev_date.strftime("%Y-%m-%d")
            else:
                current_date = "N/A"
                prev_date = "Error Fetching Date"

            return prev_date

        @staticmethod
        def limit_on_upward_movement(current_handicap: float, low_handicap: float) -> tuple[float, bool, bool]:
            soft_cap: bool = False
            hard_cap: bool = False

            if current_handicap > low_handicap:
                handicap_delta = current_handicap - low_handicap
                if handicap_delta >= 3:
                    # Hard cap ceiling (USGA 5.8 Limit on Upward Movement of a Handicap Index)
                    if handicap_delta >= 5:
                        print("hard cap")
                        current_handicap = low_handicap + 5
                        hard_cap = True
                    # Soft cap trigger (USGA 5.8 Limit on Upward Movement of a Handicap Index)
                    else:
                        print("soft cap")
                        current_handicap = low_handicap + 3 + ((handicap_delta - 3) * 0.5)
                        soft_cap = True
                else:
                    pass
            else:
                pass

            return round(current_handicap, 1), soft_cap, hard_cap
