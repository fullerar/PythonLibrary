import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import io
from weather_api import get_weather

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.city_entry = ttk.Entry(root, font=("Helvetica", 12))
        self.city_entry.pack(pady=10)

        self.search_button = ttk.Button(root, text="Get Weather", command=self.fetch_weather)
        self.search_button.pack()

        # Header section
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(pady=20)

        self.location_label = tk.Label(self.header_frame, text="", font=("Helvetica", 16, "bold"))
        self.location_label.pack()

        self.time_label = tk.Label(self.header_frame, text="", font=("Helvetica", 12), fg="gray")
        self.time_label.pack()

        self.icon_label = tk.Label(self.header_frame)
        self.icon_label.pack(pady=10)

        self.description_label = tk.Label(self.header_frame, text="", font=("Helvetica", 14))
        self.description_label.pack()

        # Details section (grid layout)
        self.details_frame = tk.Frame(root)
        self.details_frame.pack(pady=20, anchor="w", padx=20)

        self.temp_label = tk.Label(self.details_frame, text="", font=("Helvetica", 12), fg="gray")
        self.temp_label.grid(row=0, column=0, sticky="w", pady=2)

        self.feels_like_label = tk.Label(self.details_frame, text="", font=("Helvetica", 12), fg="gray")
        self.feels_like_label.grid(row=1, column=0, sticky="w", pady=2)

        self.wind_speed_label = tk.Label(self.details_frame, text="", font=("Helvetica", 12), fg="gray")
        self.wind_speed_label.grid(row=2, column=0, sticky="w", pady=2)

        self.wind_dir_label = tk.Label(self.details_frame, text="", font=("Helvetica", 12), fg="gray")
        self.wind_dir_label.grid(row=3, column=0, sticky="w", pady=2)

        self.pressure_label = tk.Label(self.details_frame, text="", font=("Helvetica", 12), fg="gray")
        self.pressure_label.grid(row=4, column=0, sticky="w", pady=2)

        # Optional status label
        self.status_label = tk.Label(root, text="", font=("Helvetica", 10), fg="gray")
        self.status_label.pack(pady=5)

    def fetch_weather(self):
        city = self.city_entry.get()
        data = get_weather(city)

        if data:
            location = data["location"]
            current = data["current"]

            self.location_label.config(text=f"{location['name']}, {location['region']} ({location['country']})")
            self.time_label.config(text=f"Local time: {location['localtime']}")
            self.description_label.config(text=current["description"])

            # Load and show weather icon
            icon_data = requests.get(current["icon_url"]).content
            image = Image.open(io.BytesIO(icon_data)).resize((64, 64))
            photo = ImageTk.PhotoImage(image)
            self.icon_label.config(image=photo)
            self.icon_label.image = photo

            # Weather details with units
            self.temp_label.config(text=f"Temperature: {current['temperature']}°C")
            self.feels_like_label.config(text=f"Feels like: {current['feelslike']}°C")
            self.wind_speed_label.config(text=f"Wind Speed: {current['wind_speed']} km/h")
            self.wind_dir_label.config(text=f"Wind Direction: {current['wind_dir']} ({current['wind_degree']}°)")
            self.pressure_label.config(text=f"Pressure: {current['pressure']} mb")

            self.status_label.config(text=f"Showing weather for {location['name']}.")
        else:
            self.clear_display()

    def clear_display(self):
        self.location_label.config(text="Could not fetch data.")
        self.time_label.config(text="")
        self.description_label.config(text="")
        self.icon_label.config(image='')
        self.temp_label.config(text="")
        self.feels_like_label.config(text="")
        self.wind_speed_label.config(text="")
        self.wind_dir_label.config(text="")
        self.pressure_label.config(text="")
        self.status_label.config(text="Error fetching weather.")
