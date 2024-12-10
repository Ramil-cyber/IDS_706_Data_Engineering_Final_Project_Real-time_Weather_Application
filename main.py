import logging
import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
import altair as alt
from src import WeatherDatabaseApi, WeatherAPI
from dotenv import load_dotenv
import os

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbose logging
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)

load_dotenv()

#@st.cache_data
def initialize_weather_db():
    """Initialize WeatherDatabaseApi."""
    logging.info("Initializing WeatherDatabaseApi.")
    try:
        db = WeatherDatabaseApi("data/db/application", deploy_database=False)
        logging.debug("WeatherDatabaseApi initialized successfully.")
        return db
    except Exception as e:
        logging.error(f"Failed to initialize WeatherDatabaseApi: {e}")
        raise


def initialize_api():
    logging.info("Initializing WeatherAPI.")
    try:
        api_access_key = os.environ.get("WEATHER_API_ACCESS_TOKEN")
        if not api_access_key:
            logging.error("WEATHER_API_ACCESS_TOKEN is not set.")
            raise ValueError("API access key is missing!")
        logging.debug("WeatherAPI initialized successfully.")
        return WeatherAPI(api_access_key)
    except Exception as e:
        logging.error(f"Failed to initialize WeatherAPI: {e}")
        raise


def get_live_data(city_name):
    """Simulate fetching live weather data."""
    logging.info(f"Fetching live weather data for {city_name}.")
    try:
        weather_api = initialize_api()
        current = weather_api.get_current_weather(city_name)
        logging.debug(f"Current weather for {city_name}: {current}")
        return {
            "current_Temp": round(current["temperature"], 1),
            "feels_like_temp": round(current["feels_like"], 1),
            "humidity": round(current["humidity"], 1),
            "wind_speed": round(current["wind_speed"], 1),
            "description": current["description"],
            "main_description": current["main_description"],
        }
    except Exception as e:
        logging.error(f"Error fetching live data for {city_name}: {e}")
        raise


def get_forecast(city_name):
    """Simulate fetching weather forecast data."""
    logging.info(f"Fetching forecast data for {city_name}.")
    try:
        weather_api = initialize_api()
        forecast_data = weather_api.get_forecast(city_name)
        logging.debug(f"Forecast data for {city_name}: {forecast_data}")
        return forecast_data
    except Exception as e:
        logging.error(f"Error fetching forecast data for {city_name}: {e}")
        raise


def create_forecast_chart(forecast_data):
    """Create Altair chart for temperature forecast."""
    logging.info("Creating forecast chart.")
    try:
        df = pd.DataFrame(forecast_data)
        logging.debug(f"Forecast DataFrame: {df.head()}")

        df["date"] = pd.to_datetime(df["date"])
        logging.debug("Converted 'date' column to datetime.")

        spread_chart = (
            alt.Chart(df)
            .mark_area(opacity=0.4, color="lightblue")
            .encode(
                x=alt.X("date:T", title="Date", axis=alt.Axis(format="%b %d")),
                y=alt.Y(
                    "min_temp:Q", title="Temperature (°C)", scale=alt.Scale(zero=False)
                ),
                y2="max_temp:Q",
            )
        )
        avg_temp_line = (
            alt.Chart(df)
            .mark_line(color="blue", strokeWidth=2)
            .encode(
                x="date:T",
                y="avg_temp:Q",
                tooltip=["date:T", "avg_temp:Q", "min_temp:Q", "max_temp:Q"],
            )
        )
        logging.debug("Altair chart created successfully.")
        return spread_chart + avg_temp_line
    except Exception as e:
        logging.error(f"Error while creating forecast chart: {e}")
        raise

@st.cache_data
def create_map(_weather_db):
    """Create a folium map with weather data."""
    logging.info("Initializing map creation.")
    try:
        world_map = folium.Map(
            location=[37.0902, -95.7129],
            tiles="Cartodb Positron",
            zoom_start=4,
        )
        logging.debug("Base map initialized.")

        city_data = _weather_db.get_active_states()
        logging.debug(f"Retrieved city data: {len(city_data)} locations found.")

        for city_location, city_details in city_data.items():
            folium.Marker(
                [city_location[0], city_location[1]],
                popup=city_details["city"],
                tooltip=city_details["city"],
                icon=folium.Icon(color="blue", icon="flag")
            ).add_to(world_map)
        logging.info("Added all city markers to the map.")

        st.markdown(
            """
            <style>
            body {
                overflow: hidden;
            }
            .st-emotion-cache-1jicfl2 {
                width: 100%;
                # height:100%;
                padding: 4rem 1rem 1rem;
                margin:0;
                min-width: auto;
                max-width: initial;    
        }
                    """,
            unsafe_allow_html=True,
        )
        logging.debug("Custom map styling applied.")

        st.markdown(
            """
            <style>
                # .reportview-container {
                #     margin-top: -2em;
                # }
                #MainMenu {visibility: hidden;}
                .stAppDeployButton {display:none;}
                footer {visibility: hidden;}
                #stDecoration {display:none;}
            </style>
        """,
            unsafe_allow_html=True,
        )
        st.html("<style> .main {overflow: hidden} </style>")
        logging.debug("Additional HTML styling applied.")

        return world_map, city_data

    except Exception as e:
        logging.error(f"Error occurred while creating the map: {e}")
        raise

def display_sidebar(city_details, live_data, chart, other_information):
    """Update the sidebar with city weather details."""
    logging.info("Updating sidebar with city weather details.")

    try:
        city_name = city_details.get("city")
        logging.debug(f"City name retrieved: {city_name}")

        st.markdown(
            """
        <style>
        [data-testid="stSidebar"] h1 {
            margin-top: 0px; /* Adjust this value */
            font-size: 50px; /* Adjust font size if needed */
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        logging.debug("Sidebar styling applied.")

        # Sidebar title
        st.sidebar.markdown(f"<h1>{city_name}</h1>", unsafe_allow_html=True)

        current_temp = live_data["current_Temp"]
        feels_like_temp = live_data["feels_like_temp"]
        feel_vs_true = round(feels_like_temp - current_temp, 1)
        description = live_data["main_description"]
        logging.debug(
            f"Live data retrieved: Current Temp={current_temp}, Feels Like={feels_like_temp}, Description={description}"
        )

        description_icon_map = {
            "clear sky": "☀️",
            "scattered clouds": "🌥️",
            "rain": "🌧️",
            "snow": "❄️",
            "overcast clouds": "☁️",
            "few clouds": "🌤️",
            "thunderstorm": "🌩️",
            "clouds": "☁️",  # General representation of clouds
            "clear": "☀️",  # Clear weather
            "tornado": "🌪️",  # Tornado icon
            "squall": "🌬️",  # Strong wind/squall
            "ash": "🌋",  # Volcanic ash
            "dust": "🌪️",  # Dust storm (same as tornado for simplicity)
            "sand": "🏜️",  # Sandstorm
            "fog": "🌁",  # Foggy weather, represented with a bridge in the mist
            "haze": "🌅",  # Hazy conditions, often associated with a sun obscured by haze
            "mist": "🌫️",  # Misty weather, depicted with low visibility
            "smoke": "💨",  # Smoke
            "drizzle": "🌦️",  # Light rain/drizzle
        }

        description_icon = description_icon_map.get(description.lower(), "🌍")
        logging.debug(f"Weather icon selected: {description_icon}")

        col11, col12 = st.sidebar.columns([3, 1])

        with col11:
            st.metric(
                label="Temperature",
                value=f"{current_temp}°C",
                delta=f"Feels {feel_vs_true:+}°C",
            )
        with col12:
            st.markdown(
                f"""
                <div style="font-size: 50px; text-align: left; margin-left: -60px; margin-top: 20px;">{description_icon}</div>
                """,
                unsafe_allow_html=True,
            )
        logging.debug("Temperature and weather icon added to sidebar.")

        col21, col22 = st.sidebar.columns(2)

        with col21:
            st.metric(
                label="💧 Humidity", value=f"{live_data['humidity']}%", delta=None
            )
        with col22:
            st.metric(
                label="💨 Wind Speed",
                value=f"{live_data['wind_speed']} m/s",
                delta=None,
            )
        logging.debug("Humidity and wind speed metrics added to sidebar.")

        st.sidebar.subheader("Temperature Forecast [Min~Max]")
        with st.sidebar:
            st.altair_chart(chart, use_container_width=True)
        logging.debug("Forecast chart added to sidebar.")

        st.sidebar.subheader("Other Information")
        st.sidebar.write(other_information)
        logging.info("Sidebar successfully updated.")

    except KeyError as e:
        logging.error(f"Missing data key in sidebar update: {e}")
    except Exception as e:
        logging.error(f"Error while updating the sidebar: {e}")
        raise


def main():
    """Main function to run the Streamlit app."""
    logging.info("Starting the Streamlit application.")

    try:
        st.set_page_config(
            page_title="Travel Exploration",
            page_icon="🌍",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        logging.debug("Page configuration set successfully.")

        # Initialize the weather database
        WeatherDb = initialize_weather_db()
        logging.debug("Weather database initialized.")

        # Create the map and display it
        world_map, city_data = create_map(WeatherDb)
        st_data = st_folium(world_map, use_container_width=True, height=800)
        logging.debug("Map displayed with folium and Streamlit integration.")

        # Handle city selection from the map
        if (
            st_data
            and "last_object_clicked" in st_data
            and st_data["last_object_clicked"]
        ):
            clicked_city = st_data["last_object_clicked"]
            logging.debug(f"City clicked on the map: {clicked_city}")

            if city_data.get((clicked_city["lat"], clicked_city["lng"])):
                city_details = city_data.get((clicked_city["lat"], clicked_city["lng"]))
                logging.debug(f"City details retrieved: {city_details}")

                live_data = get_live_data(city_details.get("city"))
                logging.info(
                    f"Live weather data retrieved for {city_details.get('city')}: {live_data}"
                )

                forecast_data = get_forecast(city_details.get("city"))
                logging.info(
                    f"Forecast data retrieved for {city_details.get('city')}: {forecast_data}"
                )

                chart = create_forecast_chart(forecast_data)
                logging.debug("Forecast chart created.")

                other_information = WeatherDb.get_interesting_fact_for_location(
                    clicked_city["lat"], clicked_city["lng"]
                )
                logging.debug(f"Interesting fact retrieved: {other_information}")

                display_sidebar(city_details, live_data, chart, other_information)
                logging.info("Sidebar updated with city details.")
            else:
                logging.warning("City clicked does not have data in the database.")
        else:
            st.sidebar.write("Select a city from the map to see more details.")
            logging.info("No city selected from the map.")

    except KeyError as e:
        logging.error(f"KeyError encountered: {e}")
    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}")
        raise


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    main()
