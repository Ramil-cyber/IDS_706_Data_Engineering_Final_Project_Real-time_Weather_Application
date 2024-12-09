try:
    from src.db import WeatherDatabaseApi as WeatherDatabaseApi, SQL as SQL

except ImportError:
    from db import WeatherDatabaseApi as WeatherDatabaseApi, SQL as SQL


try:
    from src.weather_api import WeatherAPI as WeatherAPI
except ImportError:
    from weather_api import WeatherAPI as WeatherAPI
