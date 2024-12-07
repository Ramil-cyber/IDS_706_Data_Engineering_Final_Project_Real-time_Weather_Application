import requests
from datetime import datetime
from statistics import mean


class WeatherAPI:
    def __init__(self, api_key):
        """
        Initialize WeatherAPI with your API key
        Sign up at: https://openweathermap.org/api to get an API key
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self, city):
        """Get current weather for a city"""
        endpoint = f"{self.base_url}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",  # Use metric units (Celsius, meters/sec)
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if "main" not in data or "weather" not in data:
                raise ValueError(f"Unexpected API response format: {data}")
            print(data)
            weather_info = {
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "main_description" : data["weather"][0]["main"],
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

            return weather_info

        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {str(e)}")
            return None
        except ValueError as e:
            print(f"Data Processing Error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            return None

    def get_forecast(self, city, days=5):
        """Get weather forecast for specified number of days"""
        endpoint = f"{self.base_url}/forecast"
        params = {"q": city, "appid": self.api_key, "units": "metric"}

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if "list" not in data:
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

            return forecast

        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {str(e)}")
            return None
        except ValueError as e:
            print(f"Data Processing Error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
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
    # if current is not None:
    #     print("\nCurrent Weather:")
    #     print(f"City: {current['city']}, {current['country']}")
    #     print(f"Temperature: {current['temperature']}°C")
    #     print(f"Feels like: {current['feels_like']}°C")
    #     print(f"Description: {current['description']}")
    #     print(f"Humidity: {current['humidity']}%")
    #     print(f"Wind Speed: {current['wind_speed']} m/s")
    #     print(f"Sunrise: {current['sunrise']}")
    #     print(f"Sunset: {current['sunset']}")
    # else:
    #     print(
    #         "Failed to get weather data. Please check your API key and internet connection."
    #     )

    # # Get and display forecast
    # print(f"\n{forecast_days}-Day Weather Forecast for {city_name}:")
    # forecast = weather.get_forecast(city_name)
    # print(forecast)
    # if forecast is not None:
    #     for day in forecast:
    #         print(f"\n{day['date']}:")
    #         print(type(day['date']))
    #         print(
    #             f"  Temperature: {day['min_temp']}°C to {day['max_temp']}°C (avg: {day['avg_temp']}°C)"
    #         )
    #         print(f"  Description: {day['description']}")
    #         print(f"  Wind Speed: {day['avg_wind']} m/s")
    # else:
    #     print(
    #         "Failed to get forecast data. Please check your API key and internet connection."
    #     )
