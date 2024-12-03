import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
import altair as alt
from src import WeatherDatabaseApi, WeatherAPI
from dotenv import load_dotenv
import os

load_dotenv()

def initialize_weather_db():
    """Initialize WeatherDatabaseApi."""
    return WeatherDatabaseApi('data/db/application', deploy_database=False)

def initialize_api():
    api_access_key = os.environ.get("WEATHER_API_ACCESS_TOKEN")
    return WeatherAPI(api_access_key)


def get_live_data(city_name):
    """Simulate fetching live weather data."""
    weather_api = initialize_api()

    current = weather_api.get_current_weather(city_name)
    print(current['description'])
    return {
        "current_Temp": round(current['temperature'], 1),
        "feels_like_temp": round(current['feels_like'], 1),
        "humidity": round(current['humidity'], 1),
        "wind_speed": round(current['wind_speed'],1),
        "description": current['description'],
    }

def get_forecast(city_name):
    """Simulate fetching weather forecast data."""
    weather_api = initialize_api()
    
    forecast_data = weather_api.get_forecast(city_name)

    return forecast_data

def create_forecast_chart(forecast_data):
    """Create Altair chart for temperature forecast."""
    df = pd.DataFrame(forecast_data)
    df['date'] = pd.to_datetime(df['date'])

    spread_chart = alt.Chart(df).mark_area(opacity=0.4, color="lightblue").encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(format='%b %d')),
        y=alt.Y('min_temp:Q', title='Temperature (°C)', scale=alt.Scale(zero=False)),
        y2='max_temp:Q'
    )

    avg_temp_line = alt.Chart(df).mark_line(color='blue', strokeWidth=2).encode(
        x='date:T',
        y='avg_temp:Q',
        tooltip=['date:T', 'avg_temp:Q', 'min_temp:Q', 'max_temp:Q']
    )

    return spread_chart + avg_temp_line

def create_map(weather_db):
    """Create a folium map with weather data."""
    world_map = folium.Map(
        location=[37.0902, -95.7129],
        tiles="Cartodb Positron",
        zoom_start=4,
    )

    city_data = weather_db.get_active_states()
    for city_location, city_details in city_data.items():
        folium.Marker(
            [city_location[0], city_location[1]],
            popup=city_details["city"],
            tooltip=city_details["city"],
        ).add_to(world_map)

        
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

    st.markdown("""
        <style>
            # .reportview-container {
            #     margin-top: -2em;
            # }
            #MainMenu {visibility: hidden;}
            .stAppDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
        </style>
    """, unsafe_allow_html=True)

    st.html("<style> .main {overflow: hidden} </style>")


    return world_map, city_data

def display_sidebar(city_details, live_data, chart, other_information):
    """Update the sidebar with city weather details."""
    city_name = city_details.get('city')

    st.sidebar.title(city_name)

    current_temp = live_data["current_Temp"]
    feels_like_temp = live_data["feels_like_temp"]
    feel_vs_true = round(feels_like_temp - current_temp, 1)
    description = live_data["description"]
    description_icon_map = {
        "clear sky": "☀️",
        "scattered clouds": "🌥️",
        "rain": "🌧️",
        "snow": "❄️",
        "overcast clouds": "☁️",  # Added icon for overcast clouds
    }

    description_icon = description_icon_map.get(description)

    col11, col12 = st.sidebar.columns([3, 1])

    with col11:
        st.metric(label="Temperature", value=f"{current_temp}°C", delta=f"Feels {feel_vs_true:+}°C")

    with col12:
        st.markdown(
            f"""
            <div style="font-size: 50px; text-align: left; margin-left: -60px; margin-top: 20px;">{description_icon}</div>
            """,
            unsafe_allow_html=True,
        )

    col21, col22 = st.sidebar.columns(2)

    with col21:
        st.metric(label="💧 Humidity", value=f"{live_data['humidity']}%", delta=None)

    with col22:
        st.metric(label="💨 Wind Speed", value=f"{live_data['wind_speed']} m/s", delta=None)

    st.sidebar.subheader("Temperature Forecast")
    with st.sidebar:
        st.altair_chart(chart, use_container_width=True)

    st.sidebar.subheader("Other Information")
    st.sidebar.write(other_information)

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="Travel Exploration",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    WeatherDb = initialize_weather_db()
    

    other_information = """The climate of Durham is humid subtropical
    (Cfa according to the Köppen classification system)
    , with hot and humid summers, cool winters, and warm to mild spring and autumn."""


    world_map, city_data = create_map(WeatherDb)
    st_data = st_folium(world_map, use_container_width=True, height=800)

    if st_data and "last_object_clicked" in st_data and st_data["last_object_clicked"]:
        clicked_city = st_data["last_object_clicked"]
        if city_data.get((clicked_city['lat'], clicked_city['lng'])):
            city_details = city_data.get((clicked_city['lat'], clicked_city['lng']))
            live_data = get_live_data(city_details.get('city'))

            forecast_data = get_forecast(city_details.get('city'))
            print(f"Forecast - {forecast_data}")
            chart = create_forecast_chart(forecast_data)

            display_sidebar(city_details, live_data, chart, other_information)

    else:
        st.sidebar.write("Select a city from the map to see more details.")

if __name__ == "__main__":
    main()