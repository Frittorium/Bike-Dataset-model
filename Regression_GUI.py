from predict import predict
import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Bike Rental Prediction Model")
root.geometry("370x500")

temp_var = tk.StringVar()
atemp_var = tk.StringVar()
humidity_var = tk.StringVar()
windspeed_var = tk.StringVar()

weather_var = tk.StringVar(value="clear")
season_var = tk.StringVar(value="spring")

holiday_var = tk.BooleanVar(value=False)
workday_var = tk.BooleanVar(value=False)

year_var = tk.StringVar(value="2011")
month_var = tk.StringVar(value="1")
day_var = tk.StringVar(value="1")

hour_var = tk.StringVar(value="0")
minute_var = tk.StringVar(value="0")

def validate_float(value):
    if value == "":
        return True

    try:
        return float(value) >= 0
    except ValueError:
        return False


validate_command = (
    root.register(validate_float),
    "%P"
)

float_fields = [
    ("Temperature", temp_var),
    ("Temperature Feels-Like", atemp_var),
    ("Humidity Percentage", humidity_var),
    ("Wind Speed", windspeed_var)
]

for row, (label, variable) in enumerate(float_fields):
    ttk.Label(root, text=label).grid(
        row=row,
        column=0,
        padx=10,
        pady=8,
        sticky="w"
    )

    ttk.Entry(
        root,
        textvariable=variable,
        width=20,
        validate="key",
        validatecommand=validate_command
    ).grid(
        row=row,
        column=1,
        padx=10,
        pady=8,
        sticky="w"
    )

ttk.Label(root, text="Weather").grid(
    row=4,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Combobox(
    root,
    textvariable=weather_var,
    values=["clear", "cloudy", "light", "heavy"],
    state="readonly",
    width=17
).grid(
    row=4,
    column=1,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Label(root, text="Season").grid(
    row=5,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Combobox(
    root,
    textvariable=season_var,
    values=["spring", "summer", "fall", "winter"],
    state="readonly",
    width=17
).grid(
    row=5,
    column=1,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Checkbutton(
    root,
    text="Holiday",
    variable=holiday_var
).grid(
    row=6,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Checkbutton(
    root,
    text="Workday",
    variable=workday_var
).grid(
    row=6,
    column=1,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Label(root, text="Year").grid(
    row=7,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Combobox(
    root,
    textvariable=year_var,
    values=["2011", "2012"],
    state="readonly",
    width=17
).grid(
    row=7,
    column=1,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Label(root, text="Month").grid(
    row=8,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Combobox(
    root,
    textvariable=month_var,
    values=[str(i) for i in range(1, 13)],
    state="readonly",
    width=17
).grid(
    row=8,
    column=1,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Label(root, text="Day").grid(
    row=9,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Combobox(
    root,
    textvariable=day_var,
    values=[str(i) for i in range(1, 32)],
    state="readonly",
    width=17
).grid(
    row=9,
    column=1,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Label(root, text="Time").grid(
    row=10,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

time_frame = ttk.Frame(root)
time_frame.grid(
    row=10,
    column=1,
    padx=10,
    pady=8,
    sticky="w"
)

ttk.Label(time_frame, text="Hour").pack(side="left")

tk.Spinbox(
    time_frame,
    from_=0,
    to=23,
    textvariable=hour_var,
    width=5,
    wrap=True
).pack(side="left", padx=5)

ttk.Label(time_frame, text="Minute").pack(side="left")

tk.Spinbox(
    time_frame,
    from_=0,
    to=59,
    textvariable=minute_var,
    width=5,
    wrap=True
).pack(side="left", padx=5)

def submit():

    # Make sure the four float fields are filled in
    if not all([
        temp_var.get(),
        atemp_var.get(),
        humidity_var.get(),
        windspeed_var.get()
    ]):
        messagebox.showerror(
            "Invalid Input",
            "Please fill in all four weather measurements."
        )
        return

    # Convert the float fields to numbers
    temp = float(temp_var.get())
    atemp = float(atemp_var.get())
    humidity = float(humidity_var.get())
    windspeed = float(windspeed_var.get())

    # Extra safety check against negative numbers
    if any(value < 0 for value in [
        temp,
        atemp,
        humidity,
        windspeed
    ]):
        messagebox.showerror(
            "Invalid Input",
            "Measurements cannot be negative."
        )
        return

    weather = weather_var.get()

    weather_1 = weather == "clear"
    weather_2 = weather == "cloudy"
    weather_3 = weather == "light"
    weather_4 = weather == "heavy"

    season = season_var.get()

    season_1 = season == "spring"
    season_2 = season == "summer"
    season_3 = season == "fall"
    season_4 = season == "winter"

    holiday_0 = not holiday_var.get()
    holiday_1 = holiday_var.get()

    workingday_0 = not workday_var.get()
    workingday_1 = workday_var.get()

    year = int(year_var.get())
    month = int(month_var.get())
    day = int(day_var.get())

    hour = int(hour_var.get())
    minute = int(minute_var.get())

    data = {
        "temp": temp,
        "atemp": atemp,
        "humidity": humidity,
        "windspeed": windspeed,

        "weather_1": weather_1,
        "weather_2": weather_2,
        "weather_3": weather_3,
        "weather_4": weather_4,

        "season_1": season_1,
        "season_2": season_2,
        "season_3": season_3,
        "season_4": season_4,

        "holiday_0": holiday_0,
        "holiday_1": holiday_1,

        "workingday_0": workingday_0,
        "workingday_1": workingday_1,

        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute
    }

    result = predict(data)


    # Temporary output so you can see the result.
    print(data)
    print("Prediction:", result)

    messagebox.showinfo(
        "Prediction",
        f"Prediction: {result} bikes rented"
    )

ttk.Button(
    root,
    text="Submit",
    command=submit
).grid(
    row=11,
    column=0,
    columnspan=2,
    pady=20
)

root.mainloop()