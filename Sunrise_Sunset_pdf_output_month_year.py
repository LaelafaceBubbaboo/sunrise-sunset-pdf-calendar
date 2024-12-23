# created 12/22/2024
# ver 1.0
# created by Matt_McCarter
# file name is Sunrise_Sunset_pdf_output_month_year.py


import tkinter as tk
from tkinter import ttk, messagebox
from suntime import Sun, SunTimeException
from datetime import datetime, timedelta
from dateutil import tz
from fpdf import FPDF

# Replace with your desired location (Example: Oklahoma City)
latitude = 35.514873
longitude = -97.538425

sun = Sun(latitude, longitude)

# Timezone conversion to CST (UTC-6)
cst = tz.gettz('America/Chicago')  # CST timezone

# Function to generate the PDF
def generate_pdf(month, year):
    # Set the start and end date for the selected month and year
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, 28)  # Default end date to 28, will adjust for leap years

    # Adjust for the correct end date based on the selected month
    if month == 2:  # February
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):  # Leap year check
            end_date = datetime(year, month, 29)
        else:
            end_date = datetime(year, month, 28)
    elif month in [4, 6, 9, 11]:  # Months with 30 days
        end_date = datetime(year, month, 30)
    else:  # Months with 31 days
        end_date = datetime(year, month, 31)

    title = f"My House - {start_date.strftime('%B')} {start_date.year}"

    # Create PDF instance
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add title with dynamic month and year
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt=title, ln=True, align='C')

    # Set font for content
    pdf.set_font("Arial", size=6)

    # Define calendar grid parameters
    days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    start_day = (start_date.weekday() + 1) % 7  # Day of the week for 1st of the selected month, adjusted for Sunday start
    days_in_month = (end_date - start_date).days + 1  # Number of days in the month
    days_per_row = 7  # 7 days in a week
    cell_width = 25  # Width of each cell (day box)
    cell_height = 30  # Height of each cell
    line_height = 4  # Space for line breaks

    # Add day headers
    pdf.set_font("Arial", 'B', 8)
    pdf.set_xy(10, 20)
    for col, day in enumerate(days_of_week):
        pdf.cell(cell_width, line_height, day, border=1, align='C', ln=0 if col < days_per_row - 1 else 1)

    # Create a calendar grid
    pdf.set_font("Arial", size=6)
    pdf.set_xy(10, 24)  # Adjust starting position for the calendar grid, right below the day headers
    total_rows = (start_day + days_in_month + days_per_row - 1) // days_per_row
    for row in range(total_rows):
        for col in range(days_per_row):
            # Calculate the current day of the month
            day_num = row * days_per_row + col - start_day + 1

            if 1 <= day_num <= days_in_month:
                current_date = start_date + timedelta(days=day_num - 1)
                try:
                    # Get sunrise, sunset, and lengths for the day
                    sunrise_utc = sun.get_sunrise_time(current_date)
                    sunset_utc = sun.get_sunset_time(current_date)
                    solar_noon_utc = sunrise_utc + (sunset_utc - sunrise_utc) / 2  # Midpoint between sunrise and sunset

                    # Convert to CST
                    sunrise_cst = sunrise_utc.astimezone(cst)
                    sunset_cst = sunset_utc.astimezone(cst)
                    solar_noon_cst = solar_noon_utc.astimezone(cst)

                    # Correct AM/PM formatting for solar noon
                    solar_noon_cst_str = solar_noon_cst.strftime("%I:%M %p")
                    if solar_noon_cst.hour == 0:
                        solar_noon_cst_str = solar_noon_cst_str.replace("AM", "PM")

                    # Calculate day and night lengths
                    day_length = sunset_cst - sunrise_cst
                    night_length = timedelta(days=1) - day_length

                    # Convert day length to hours, minutes, seconds
                    day_hours = day_length.seconds // 3600
                    day_minutes = (day_length.seconds % 3600) // 60
                    day_seconds = day_length.seconds % 60

                    # Convert night length to hours, minutes, seconds
                    night_hours = night_length.seconds // 3600
                    night_minutes = (night_length.seconds % 3600) // 60
                    night_seconds = night_length.seconds % 60

                    # Set day text
                    day_text = f"{current_date.day}\n"
                    day_text += f"Sunrise: {sunrise_cst.strftime('%I:%M %p')}\n"
                    day_text += f"Sunset: {sunset_cst.strftime('%I:%M %p')}\n"
                    day_text += f"Solar Noon: {solar_noon_cst_str}\n"
                    day_text += f"Day: {day_hours:02}:{day_minutes:02}:{day_seconds:02}\n"
                    day_text += f"Night: {night_hours:02}:{night_minutes:02}:{night_seconds:02}"

                except SunTimeException as e:
                    day_text = f"{current_date.day}\nError: {e}"

            else:
                day_text = ""  # Empty box for days outside the current month

            # Draw the cell with the data
            pdf.set_xy(col * cell_width + 10, row * cell_height + 24)
            pdf.rect(col * cell_width + 10, row * cell_height + 24, cell_width, cell_height)
            pdf.multi_cell(cell_width, line_height, day_text, border=0, align='L')

    # Output the PDF (use selected month and year for file name)
    pdf.output(f"{start_date.strftime('%B')}_{start_date.year}.pdf")
    messagebox.showinfo("Success", f"PDF generated successfully: {start_date.strftime('%B')}_{start_date.year}.pdf")

# GUI Setup
def create_gui():
    root = tk.Tk()
    root.title("Sunrise/Sunset Calendar Generator")
    root.geometry("400x250")

    # Month Dropdown
    month_label = tk.Label(root, text="Select Month:")
    month_label.pack(pady=10)
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    month_dropdown = ttk.Combobox(root, values=month_names, state="readonly")
    month_dropdown.set(datetime.now().strftime("%B"))  # Default to current month
    month_dropdown.pack(pady=5)

    # Year Dropdown
    year_label = tk.Label(root, text="Select Year:")
    year_label.pack(pady=10)
    years = [i for i in range(1900, 2031)]  # Years from 1900 to 2030
    year_dropdown = ttk.Combobox(root, values=years, state="readonly")
    year_dropdown.set(datetime.now().year)  # Default to current year
    year_dropdown.pack(pady=5)

    # Generate PDF Button
    generate_btn = tk.Button(root, text="Generate PDF", command=lambda: generate_pdf(month_names.index(month_dropdown.get()) + 1, int(year_dropdown.get())))
    generate_btn.pack(pady=20)

    root.mainloop()

# Start the GUI
create_gui()
