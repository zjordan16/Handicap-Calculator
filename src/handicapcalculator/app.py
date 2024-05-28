"""
This is a mobile/desktop application that can calculate an unofficial USGA handicap.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import Tuple
from icecream import ic
import os
import polars as pl


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
		main_box.add(self.course_rating_input)
		main_box.add(self.course_slope_input)
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

		# Display table on startup
		self.display_table()


	def save_score(self, widget):
		inputs_are_valid = (
				self.course_name_input.children[1].value and self.score_input.children[1].value and
				self.course_slope_input.children[1].value and self.course_rating_input.children[1].value
		)
		if inputs_are_valid:
			# Get Inputs
			course_name = self.course_name_input.children[1].value
			adjusted_gross_score = self.score_input.children[1].value
			slope = self.course_slope_input.children[1].value
			rating = self.course_rating_input.children[1].value
			differential = self.calculate_round_differential(adjusted_gross_score, slope, rating)

   			# Write inputs to CSV
			self.write_to_csv(course_name, adjusted_gross_score, slope, rating, differential)
			
			# Refresh handicap and table
			self.refresh_handicap_index()
			self.display_table()

			# Clear inputs
			self.invalid_inputs_message.style.visibility = "hidden"
			self.course_name_input.children[1].value = None
			self.score_input.children[1].value = None
			self.course_slope_input.children[1].value = None
			self.course_rating_input.children[1].value = None
		else:
			self.invalid_inputs_message.style.visibility = "visible"


	def write_to_csv(self, course_name: str, adjusted_gross_score: int, slope: int, rating: float, differential: float):
		# declare new_data as dictionary for polars, typecast to match datatypes with polars dataframe
		new_data = {"course_name": course_name, "adjusted_gross_score": int(adjusted_gross_score),"slope": int(slope),
		"rating": float(rating), "differential": float(differential)}

		# Declare file directory for csv
		csv_file = self.declare_csv_directory()

		# Check if CSV exists, append if exists, create new if it doesn't
		if os.path.exists(csv_file):
			# Scan reads dataframes in lazy mode, pl.LazyFrame() creates new dataframe in lazy mode, concat() combines frames
			existing_df = pl.scan_csv(csv_file)
			new_df = pl.LazyFrame(new_data, schema={"course_name": pl.Utf8, "adjusted_gross_score": pl.Int64, "slope": pl.Int64, "rating": pl.Float64, "differential": pl.Float64})
			df = pl.concat([existing_df, new_df])
		else:
			df = pl.LazyFrame(new_data, schema={"course_name": pl.Utf8, "adjusted_gross_score": pl.Int64, "slope": pl.Int64, "rating": pl.Float64, "differential": pl.Float64})

		# Write new data to list in csv
		df = df.collect().lazy()
		df.sink_csv(csv_file)

		
	def declare_csv_directory(self):
		file_directory = os.path.dirname(__file__)
		os.makedirs(file_directory, exist_ok=True)
		return os.path.join(file_directory, "score_history_table.csv")


	def display_table(self):
		self.score_history_table.data.clear()

		# Declare file directory for csv
		csv_file = self.declare_csv_directory()

		if os.path.exists(csv_file):
			# read newest 20 rows from csv
			df = pl.scan_csv(csv_file).tail(20).collect()

			# loop displays newest 20 games to table from newest to oldest
			for row in reversed(list(df.iter_rows(named=True))):
				self.score_history_table.data.append([str(row[df.columns[0]]),
													  str(row[df.columns[1]]),
													  str(row[df.columns[2]]),
													  str(row[df.columns[3]]),
													  str(row[df.columns[4]]),
													  ])
		else:
			# display blank table
			self.score_history_table.data.clear()


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
			headings=["Course Name", "Adjusted Gross Score", "Course Rating", "Course Slope Rating",
					  "Round Differential"],
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
		return round(((113 / slope) * (adjusted_gross_score - rating)), 1)

	
	def calculate_rounds_to_use(self) -> Tuple[int, float]:
		# Calculates total rounds using lazy execution in polars
		csv_file = self.declare_csv_directory()
		df = pl.scan_csv(csv_file)
		total_rounds = df.select(pl.len()).collect().item()

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
		elif total_rounds <=5:
			used_rounds = 1
			adjustment = 0.0
		elif total_rounds <= 6:
			used_rounds = 2
			adjustment = -1.0
		elif total_rounds <= 8:
			used_rounds = 2
			adjustment = 0
		elif total_rounds <= 11:
			used_rounds = 3
			adjustment = 0
		elif total_rounds <= 14:
			used_rounds = 4
			adjustment = 0
		elif total_rounds <= 16:
			used_rounds = 5
			adjustment = 0
		elif total_rounds <= 18:
			used_rounds = 6
			adjustment = 0
		elif total_rounds <= 19:
			used_rounds = 7
			adjustment = 0
		else:
			used_rounds = 8
			adjustment = 0
		return int(used_rounds), float(adjustment)

	
	def read_used_rounds(self) -> Tuple[float, list]:
		used_rounds, adjustment = self.calculate_rounds_to_use()
		csv_file = self.declare_csv_directory()
		df = pl.scan_csv(csv_file).collect()

		# If more than 20 total rounds, just use recent 20 for calculations
		if df.height > 20:
			df = df.tail(20)

		df = df.sort("differential", descending=True).tail(used_rounds)\
			.select(["differential"])
		# USGA rounds handicaps to one decimal
		handicap = round(df.mean().item(), 1)
		used_differentials = list(df)
		return handicap, used_differentials

	
	
	def calculate_handicap_index(self) -> float:
		# TODO: implement overall handicap index calculation logic
		# In Progress
		calc_handicap_index = -100  # -100 = flag
		# fetch handicap index & used differentials
		calc_handicap_index, used_differentials = self.read_used_rounds()

		# display handicap index to GUI
		if calc_handicap_index == -100:
			self.handicap_index = "N/A"
		else:
			self.handicap_index = calc_handicap_index


	def refresh_handicap_index(self) -> None:
		self.calculate_handicap_index()
		self.handicap_display.children[0].text = f"Handicap Index: {self.handicap_index}"


def main():
	return HandicapCalculator()
