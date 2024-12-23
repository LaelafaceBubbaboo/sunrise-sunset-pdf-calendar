Sunrise/Sunset PDF Calendar Generator

	Overview

	The Sunrise/Sunset PDF Calendar Generator is a Python application that generates a monthly calendar displaying sunrise and sunset times, solar noon, and the lengths of day and night for each day. The application uses a GUI (Graphical User Interface) to allow users to select a month and year, and outputs the data as a PDF file.

	Features

	Dynamic Calendar Creation: Generates a calendar for any selected month and year.
	Sunrise and Sunset Calculation: Provides daily sunrise, sunset, and solar noon times.
	Day/Night Length: Displays the duration of daylight and nighttime for each day.
	PDF Export: Generates a formatted PDF with all relevant information.

	Requirements
	Python 3.x

	Required Python Libraries:
	tkinter
	suntime
	dateutil
	fpdf

	You can install the required dependencies by running:

	pip install suntime python-dateutil fpdf

	Installation
	Clone or download this repository.
	Ensure you have Python 3.x and the required libraries installed.
	Place the script in your desired directory.

	Usage
	Run the script by executing:
	python Sunrise_Sunset_pdf_output_month_year.py

	A GUI window will appear with options to select the month and year.
	Choose the desired month and year from the dropdowns.
	Click the "Generate PDF" button to create the calendar.

	The generated PDF will be saved in the same directory as the script, named in the format Month_Year.pdf (e.g., March_2024.pdf).

	Configuration

	The default location for sunrise and sunset calculations is set to Oklahoma City (Latitude: 35.514873, Longitude: -97.538425).

	To change the location, modify the following lines in the script:
	latitude = [your_latitude]
	longitude = [your_longitude]

	File Details
File Name: Sunrise_Sunset_pdf_output_month_year.py

Version: 1.0
Created On: 12/22/2024
Author: Matt McCarter

Notes
The program accounts for leap years and varying lengths of months.
Times are displayed in Central Standard Time (CST) by default.
Error handling is implemented to manage cases where sunrise/sunset times cannot be calculated.