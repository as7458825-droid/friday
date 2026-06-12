import os

import requests

API_KEY = os.getenv("WEATHERAPI_KEY", "")


def get_weather(city: str = "") -> str:
    if not API_KEY:
        return "Weather API key not set."
    try:
        location = city.strip() or "auto:ip"
        resp = requests.get(
            "https://api.weatherapi.com/v1/current.json",
            params={"key": API_KEY, "q": location, "aqi": "no"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        loc = data["location"]["name"] + ", " + data["location"]["country"]
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind = data["current"]["wind_kph"]
        return f"Weather in {loc}: {temp}°C, {condition}, humidity {humidity}%, wind {wind} km/h."
    except requests.RequestException as e:
        return f"Weather fetch error: {e}"
    except (KeyError, IndexError) as e:
        return f"Weather parse error: {e}"


def get_forecast(city: str = "", days: int = 3) -> str:
    if not API_KEY:
        return "Weather API key not set."
    try:
        location = city.strip() or "auto:ip"
        resp = requests.get(
            "https://api.weatherapi.com/v1/forecast.json",
            params={"key": API_KEY, "q": location, "days": days, "aqi": "no"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        loc = data["location"]["name"]
        lines = [f"Forecast for {loc}:"]
        for day in data["forecast"]["forecastday"]:
            date = day["date"]
            maxt = day["day"]["maxtemp_c"]
            mint = day["day"]["mintemp_c"]
            cond = day["day"]["condition"]["text"]
            lines.append(f"{date}: {cond}, {mint}-{maxt}°C")
        return " | ".join(lines)
    except Exception as e:
        return f"Forecast error: {e}"
