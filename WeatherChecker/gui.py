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

    def fetch_weather(self):
        city = self.city_entry.get()
        data = get_weather(city)

        if data:
            # Location and time
            location = data["location"]
            self.location_label.config(text=f"{location['name']}, {location['region']} ({location['country']})")
            self.time_label.config(text=f"Local time: {location['localtime']}")

            # Weather description
            current = data["current"]
            self.description_label.config(text=current["description"])

            # Load and show weather icon
            icon_data = requests.get(current["icon_url"]).content
            image = Image.open(io.BytesIO(icon_data)).resize((64, 64))
            photo = ImageTk.PhotoImage(image)
            self.icon_label.config(image=photo)
            self.icon_label.image = photo  # prevent garbage collection
        else:
            self.location_label.config(text="Could not fetch data.")
            self.time_label.config(text="")
            self.description_label.config(text="")
            self.icon_label.config(image='')
