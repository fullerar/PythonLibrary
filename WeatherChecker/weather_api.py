import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHERSTACK_API_KEY")
BASE_URL = "http://api.weatherstack.com/current"
DEV_MODE = os.getenv("DEV_MODE") == "True"

def get_weather(city):
    if DEV_MODE:
        try:
            with open("sample_response_ny.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Dev mode is enabled, but sample_response_ny.json not found.")
            return None
    else:
        params = {
            "access_key": API_KEY,
            "query": city
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            return None
        data = response.json()

        with open("sample_response_ny.json", "w") as f:
            json.dump(data, f, indent=4)

    if "current" in data:
        return {
            "location": {
                "name": data["location"]["name"],
                "region": data["location"]["region"],
                "country": data["location"]["country"],
                "timezone": data["location"]["timezone_id"],
                "localtime": data["location"]["localtime"],
                "lat": data["location"]["lat"],
                "lon": data["location"]["lon"],
            },
            "current": {
                "observation_time": data["current"]["observation_time"],
                "temperature": data["current"]["temperature"],
                "feelslike": data["current"]["feelslike"],
                "description": data["current"]["weather_descriptions"][0],
                "icon_url": data["current"]["weather_icons"][0],
                "wind_speed": data["current"]["wind_speed"],
                "wind_degree": data["current"]["wind_degree"],
                "wind_dir": data["current"]["wind_dir"],
                "pressure": data["current"]["pressure"],
                "precip": data["current"]["precip"],
                "humidity": data["current"]["humidity"],
                "cloudcover": data["current"]["cloudcover"],
                "uv_index": data["current"]["uv_index"],
                "visibility": data["current"]["visibility"],
                "is_day": data["current"]["is_day"]
            },
            "astro": data["current"].get("astro", {}),
            "air_quality": data["current"].get("air_quality", {})
        }

    return None


