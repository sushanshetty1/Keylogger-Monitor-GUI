import json
import os
from datetime import datetime
from tkinter import *

# Initialize the main window
window = Tk()
window.title("Keylogger Monitor")
window.config(pady=30, padx=50, bg="#f0f0f0")
window.resizable(False, False)

# Title Label
title = Label(window, text="KeyLogger Data", font=("Helvetica", 30, "bold"), bg="#f0f0f0")
title.grid(column=0, row=0, columnspan=7, pady=20)

# Labels
time_label = Label(window, text="Required Time:", font=("Courier New", 15), bg="#f0f0f0")
time_label.grid(column=0, row=1, sticky=E, padx=(0, 10))

# Get current date and time
now = datetime.now()

# Year, Month, Day, Hour, and Minute Variables with default current values
year_var = StringVar(value=now.strftime("%Y"))
month_var = StringVar(value=now.strftime("%m"))
day_var = StringVar(value=now.strftime("%d"))
hour_var = StringVar(value=now.strftime("%H"))
minute_var = StringVar(value=(now.minute // 5) * 5)  # Round down to the nearest multiple of 5


def create_time_selector(parent, row, col):
    years = [f"{i}" for i in range(2020, 2031)]
    months = [f"{i:02}" for i in range(1, 13)]
    days = [f"{i:02}" for i in range(1, 32)]
    hours = [f"{i:02}" for i in range(24)]
    minutes = [f"{i:02}" for i in range(0, 60, 5)]

    year_menu = OptionMenu(parent, year_var, *years)
    year_menu.config(width=5, font=("Arial", 12))
    year_menu.grid(row=row, column=col, sticky=W, padx=(0, 5))

    month_menu = OptionMenu(parent, month_var, *months)
    month_menu.config(width=5, font=("Arial", 12))
    month_menu.grid(row=row, column=col + 1, sticky=W, padx=(0, 5))

    day_menu = OptionMenu(parent, day_var, *days)
    day_menu.config(width=5, font=("Arial", 12))
    day_menu.grid(row=row, column=col + 2, sticky=W, padx=(0, 5))

    hour_menu = OptionMenu(parent, hour_var, *hours)
    hour_menu.config(width=5, font=("Arial", 12))
    hour_menu.grid(row=row, column=col + 3, sticky=W, padx=(0, 5))

    minute_menu = OptionMenu(parent, minute_var, *minutes)
    minute_menu.config(width=5, font=("Arial", 12))
    minute_menu.grid(row=row, column=col + 4, sticky=W, padx=(0, 5))


create_time_selector(window, 1, 1)


def search_button_clicked():
    try:
        year = int(year_var.get())
        month = int(month_var.get())
        day = int(day_var.get())
        hour = int(hour_var.get())
        minute = int(minute_var.get())
    except ValueError:
        display_text = "Invalid time format."
        data_canvas.delete("all")
        data_canvas.create_text(200, 150, text=display_text, fill="red", font=("Arial", 12))
        return

    timestamp = get_5min_interval_timestamp(datetime(year, month, day, hour, minute, 0))
    display_text = f"Timestamp: {timestamp}\nEvents:\n"

    try:
        with open("keylogger.json", "r") as file:
            data = json.load(file)
            if timestamp in data:
                display_text += "\n".join(data[timestamp])
            else:
                display_text += "No events for this timestamp."
    except FileNotFoundError:
        display_text += "Log file not found."

    data_canvas.delete("all")
    data_canvas.create_text(10, 10, text=display_text, fill="black", font=("Arial", 12), anchor=NW)

    data_canvas.config(scrollregion=data_canvas.bbox("all"))


def delete_button_clicked():
    try:
        year = int(year_var.get())
        month = int(month_var.get())
        day = int(day_var.get())
        hour = int(hour_var.get())
        minute = int(minute_var.get())
    except ValueError:
        display_text = "Invalid time format."
        data_canvas.delete("all")
        data_canvas.create_text(200, 150, text=display_text, fill="red", font=("Arial", 12))
        return

    timestamp = get_5min_interval_timestamp(datetime(year, month, day, hour, minute, 0))
    if os.path.exists("keylogger.json"):
        try:
            with open("keylogger.json", "r+") as file:
                data = json.load(file)
                if timestamp in data:
                    del data[timestamp]  # Remove the data for the selected timestamp
                    file.seek(0)  # Move to the start of the file
                    json.dump(data, file, indent=4)  # Write the updated data
                    file.truncate()  # Remove any remaining data if the new data is shorter
                    display_text = f"Data for timestamp {timestamp} deleted."
                else:
                    display_text = "No data found for this timestamp."
        except json.JSONDecodeError:
            display_text = "Error reading the log file."
    else:
        display_text = "Log file not found."

    data_canvas.delete("all")
    data_canvas.create_text(10, 10, text=display_text, fill="black", font=("Arial", 12), anchor=NW)

    data_canvas.config(scrollregion=data_canvas.bbox("all"))


search = Button(window, text="Search", width=15, font=("Arial", 12, "bold"), command=search_button_clicked)
search.grid(column=0, row=2, columnspan=3, pady=10)

delete = Button(window, text="Delete", width=15, font=("Arial", 12, "bold"), command=delete_button_clicked)
delete.grid(column=3, row=2, columnspan=3, pady=10)

canvas_frame = Frame(window)
canvas_frame.grid(column=0, row=3, columnspan=7, pady=20)

data_canvas = Canvas(canvas_frame, width=500, height=300, bg="white", highlightthickness=2, highlightbackground="black")
data_canvas.grid(row=0, column=0)

scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=data_canvas.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
data_canvas.config(yscrollcommand=scrollbar.set)


def get_5min_interval_timestamp(dt):
    rounded_minute = (dt.minute // 5) * 5
    return dt.replace(minute=rounded_minute, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")


def on_mouse_wheel(event):
    data_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


data_canvas.bind_all("<MouseWheel>", on_mouse_wheel)

window.mainloop()
