import requests
from datetime import datetime
from statistics import mean
import logging


logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbose logging
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)


class WeatherAPI:
    def __init__(self, api_key):
        """
        Initialize WeatherAPI with your API key
        Sign up at: https://openweathermap.org/api to get an API key
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        logging.info("WeatherAPI initialized.")

    def get_current_weather(self, city):
        """Get current weather for a city"""
        endpoint = f"{self.base_url}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",  # Use metric units (Celsius, meters/sec)
        }

        try:
            logging.info(f"Fetching current weather for city: {city}")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if "main" not in data or "weather" not in data:
                logging.error(f"Unexpected API response format: {data}")
                raise ValueError(f"Unexpected API response format: {data}")

            weather_info = {
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "main_description": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "city": data["name"],
                "country": data["sys"]["country"],
                "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime(
                    "%H:%M"
                ),
                "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime(
                    "%H:%M"
                ),
            }

            logging.info(f"Current weather data fetched successfully for {city}.")
            return weather_info

        except requests.exceptions.RequestException as e:
            logging.error(f"API Request Error: {str(e)}")
            return None
        except ValueError as e:
            logging.error(f"Data Processing Error: {str(e)}")
            return None
        except Exception as e:
            logging.critical(f"Unexpected Error: {str(e)}")
            return None

    def get_forecast(self, city, days=5):
        """Get weather forecast for specified number of days"""
        endpoint = f"{self.base_url}/forecast"
        params = {"q": city, "appid": self.api_key, "units": "metric"}

        try:
            logging.info(f"Fetching weather forecast for city: {city} for {days} days.")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if "list" not in data:
                logging.error(f"Unexpected API response format: {data}")
                raise ValueError(f"Unexpected API response format: {data}")

            # Process forecast data by day
            daily_forecasts = {}

            for item in data["list"]:
                date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")

                if date not in daily_forecasts:
                    daily_forecasts[date] = {
                        "temperatures": [],
                        "descriptions": [],
                        "wind_speeds": [],
                    }

                daily_forecasts[date]["temperatures"].append(item["main"]["temp"])
                daily_forecasts[date]["descriptions"].append(
                    item["weather"][0]["description"]
                )
                daily_forecasts[date]["wind_speeds"].append(item["wind"]["speed"])

            # Create summary for each day
            forecast = []
            for date, data in list(daily_forecasts.items())[:days]:
                # Get most common weather description for the day
                most_common_description = max(
                    set(data["descriptions"]), key=data["descriptions"].count
                )

                forecast.append(
                    {
                        "date": date,
                        "avg_temp": round(mean(data["temperatures"]), 1),
                        "max_temp": round(max(data["temperatures"]), 1),
                        "min_temp": round(min(data["temperatures"]), 1),
                        "description": most_common_description,
                        "avg_wind": round(mean(data["wind_speeds"]), 1),
                    }
                )

            logging.info(f"Weather forecast data fetched successfully for {city}.")
            return forecast

        except requests.exceptions.RequestException as e:
            logging.error(f"API Request Error: {str(e)}")
            return None
        except ValueError as e:
            logging.error(f"Data Processing Error: {str(e)}")
            return None
        except Exception as e:
            logging.critical(f"Unexpected Error: {str(e)}")
            return None


# Example usage
if __name__ == "__main__":
    # Configuration
    api_key = "b38066974d9946f466ce5632a763aed3"  # Replace with your actual API key
    city_name = "New York"  # Replace with your desired city
    forecast_days = 5  # Number of days for forecast

    # Initialize weather API
    weather = WeatherAPI(api_key)

    # Get and display current weather
    current = weather.get_current_weather(city_name)
    if current:
        logging.info(f"Current weather: {current}")

    # Get and display forecast
    forecast = weather.get_forecast(city_name, forecast_days)
    if forecast:
        logging.info(f"Weather forecast: {forecast}")
