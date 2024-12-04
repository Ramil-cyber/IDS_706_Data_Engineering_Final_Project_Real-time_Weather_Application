import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
import altair as alt
from src import WeatherDatabaseApi


WeatherDb = WeatherDatabaseApi(
     'data/db/application', deploy_database = False
)
################## This part will change in next week
def get_live_data():
    current_Temp = random.randint(-10, 50)  # Simulated current temperature
    feels_like_temp = current_Temp + random.randint(-3, 3)  # Simulated feels-like temperature
    return {
        "current_Temp": current_Temp,
        "feels_like_temp": feels_like_temp,
        "humidity": random.randint(20, 90),  # Random humidity percentage
        "wind_speed": round(random.uniform(0, 20), 1),  # Simulated wind speed
        "description": random.choice(["clear sky", "scattered clouds", "rain", "snow"]),  # Random weather description
    }
description_icon_map = {
    "clear sky": "☀️",
    "scattered clouds": "🌥️",
    "rain": "🌧️",
    "snow": "❄️",
    "few clouds": "🌤️",
    "broken clouds": "☁️",
    "thunderstorm": "🌩️",
    "mist": "🌫️"
}
other_information="""The climate of Durham is humid subtropical 
(Cfa according to the Köppen classification system)
, with hot and humid summers, cool winters, and warm to mild spring and autumn."""

# Sample city data
cities = [
    {'name': 'New York', 'lat': 40.6943, 'lng': -73.9249}, 
    {'name': 'Los Angeles', 'lat': 34.1139, 'lng': -118.4068}, 
    {'name': 'Chicago', 'lat': 41.8373, 'lng': -87.6862}, 
    {'name': 'Houston', 'lat': 29.7863, 'lng': -95.3889}, 
    {'name': 'Philadelphia', 'lat': 40.0077, 'lng': -75.1339}, 
    {'name': 'Phoenix', 'lat': 33.5722, 'lng': -112.0891}, 
    {'name': 'San Antonio', 'lat': 29.4658, 'lng': -98.5253}, 
    {'name': 'San Diego', 'lat': 32.8312, 'lng': -117.1225}, 
    {'name': 'Dallas', 'lat': 32.7936, 'lng': -96.7662}, 
    {'name': 'San Jose', 'lat': 37.3019, 'lng': -121.8486}, 
    {'name': 'Austin', 'lat': 30.3004, 'lng': -97.7522}, 
    {'name': 'Jacksonville', 'lat': 30.3322, 'lng': -81.6749}, 
    {'name': 'San Francisco', 'lat': 37.7562, 'lng': -122.443}, 
    {'name': 'Indianapolis', 'lat': 39.7771, 'lng': -86.1458}, 
    {'name': 'Columbus', 'lat': 39.9862, 'lng': -82.985},
    {'name': 'Fort Worth', 'lat': 32.7811, 'lng': -97.3473}, 
    {'name': 'Charlotte', 'lat': 35.208, 'lng': -80.8304}, 
    {'name': 'Seattle', 'lat': 47.6211, 'lng': -122.3244}, 
    {'name': 'Denver', 'lat': 39.7621, 'lng': -104.8759}, 
    {'name': 'El Paso', 'lat': 31.8479, 'lng': -106.4309}, 
    {'name': 'Detroit', 'lat': 42.3834, 'lng': -83.1024}, 
    {'name': 'Washington', 'lat': 38.9047, 'lng': -77.0163}, 
    {'name': 'Boston', 'lat': 42.3188, 'lng': -71.0846}, 
    {'name': 'Memphis', 'lat': 35.1046, 'lng': -89.9773}, 
    {'name': 'Nashville', 'lat': 36.1715, 'lng': -86.7843}, 
    {'name': 'Portland', 'lat': 45.5372, 'lng': -122.65}, 
    {'name': 'Oklahoma City', 'lat': 35.4676, 'lng': -97.5136}, 
    {'name': 'Las Vegas', 'lat': 36.2333, 'lng': -115.2654}, 
    {'name': 'Baltimore', 'lat': 39.3051, 'lng': -76.6144}, 
    {'name': 'Louisville', 'lat': 38.1663, 'lng': -85.6485}, 
    {'name': 'Milwaukee', 'lat': 43.0642, 'lng': -87.9673}, 
    {'name': 'Kansas City', 'lat': 39.1239, 'lng': -94.5541}, 
    {'name': 'Cleveland', 'lat': 41.4767, 'lng': -81.6804}, 
    {'name': 'Tampa', 'lat': 27.9942, 'lng': -82.4451}, 
    {'name': 'Raleigh', 'lat': 35.8325, 'lng': -78.6435}, 
    {'name': 'Minneapolis', 'lat': 44.9635, 'lng': -93.2678}, 
    {'name': 'St. Louis', 'lat': 38.6358, 'lng': -90.2451}, 
    {'name': 'Miami', 'lat': 25.7839, 'lng': -80.2102}, 
    {'name': 'Salt Lake City', 'lat': 40.7777, 'lng': -111.9306}, 
    {'name': 'Tucson', 'lat': 32.1545, 'lng': -110.8782}, 
    {'name': 'Anchorage', 'lat': 61.1508, 'lng': -149.1091}, 
    {'name': 'Fresno', 'lat': 36.7831, 'lng': -119.7941}, 
    {'name': 'Birmingham', 'lat': 33.5277, 'lng': -86.7987}, 
    {'name': 'New Orleans', 'lat': 30.0687, 'lng': -89.9288}, 
    {'name': 'St. Petersburg', 'lat': 27.7931, 'lng': -82.6652}, 
    {'name': 'Macon', 'lat': 32.8065, 'lng': -83.6974}, 
    {'name': 'Lubbock', 'lat': 33.5659, 'lng': -101.8878}, 
    {'name': 'Shreveport', 'lat': 32.4656, 'lng': -93.7956}, 
    {'name': 'Peoria', 'lat': 40.752, 'lng': -89.6153}, 
    {'name': 'Grand Rapids', 'lat': 42.962, 'lng': -85.6562}
]
# Sample data from weather_API
def get_forecast():
    return [
        {"date": "2024-11-27", "avg_temp": 18.7, "max_temp": 22.0, "min_temp": 15.0, "description": "clear sky", "avg_wind": 3.2},
        {"date": "2024-11-28", "avg_temp": 19.3, "max_temp": 20.5, "min_temp": 18.5, "description": "broken clouds", "avg_wind": 3.0},
        {"date": "2024-11-29", "avg_temp": 17.5, "max_temp": 21.0, "min_temp": 14.0, "description": "rain", "avg_wind": 4.2},
        {"date": "2024-11-30", "avg_temp": 16.8, "max_temp": 19.5, "min_temp": 13.5, "description": "scattered clouds", "avg_wind": 3.5},
        {"date": "2024-12-01", "avg_temp": 20.1, "max_temp": 23.0, "min_temp": 18.0, "description": "clear sky", "avg_wind": 2.8},
    ]
# Fetch forecast data
forecast_data = get_forecast()
df = pd.DataFrame(forecast_data)
df['date'] = pd.to_datetime(df['date'])
#next_day_forecast = df.iloc[0:1].set_index("date")
# Create an Altair area chart for temperature spread
spread_chart = alt.Chart(df).mark_area(opacity=0.4, color="lightblue").encode(
    x=alt.X('date:T', title='Date', axis=alt.Axis(format='%b %d')),  # Format date as "Month Day"
    y=alt.Y('min_temp:Q', title='Temperature (°C)', scale=alt.Scale(zero=False)),
    y2='max_temp:Q'
)

# Add a line for average temperature
avg_temp_line = alt.Chart(df).mark_line(color='blue', strokeWidth=2).encode(
    x='date:T',
    y='avg_temp:Q',
    tooltip=['date:T', 'avg_temp:Q', 'min_temp:Q', 'max_temp:Q']
)

# Combine the spread and line chart
chart = spread_chart + avg_temp_line



#################### Initial page design

st.set_page_config(
    page_title="Travel Exploration",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """
    <div style="
        background-color: #4c98af; /* Light blue background */
        padding: 5px; /* Smaller padding */
        border-radius: 5px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #FFFFFF; /* text to white */
        margin-bottom: 10px; /* Reduce space below the title */
        margin-top: -20px; /* Move closer to the top of the page */
        ">
         Write the point where you want to know Weather Information
    </div>
    """,
    unsafe_allow_html=True,
)



# temp_unit = st.sidebar.radio("Temperature Unit", ["Celsius", "Fahrenheit"], index=0)
# wind_speed_unit = st.sidebar.radio("Wind Speed Unit", ["km/h", "mph"], index=0)

# st.title("Weather Application!")
# Showcase Predefined Metrics



# if "clicked" not in st.session_state:
#     st.session_state.clicked = False  # Initialize state

# # Display the initial sidebar content
# if not st.session_state.clicked:
#st.sidebar.write("Select a city from the map to see more details.")


######################### Map Part


world_map = folium.Map(
        location=[37.0902, -95.7129],
        tiles="Cartodb Positron",
        zoom_start=4,
    )


city_data = WeatherDb.get_active_states()

for city_location, city_details in city_data.items():
    folium.Marker(
        [city_location[0], city_location[1]],
        popup=city_details["city"],  # Show city name on click
        tooltip=city_details["city"],  # Tooltip shows on hover
    ).add_to(world_map)




# sidebar:
st.sidebar.markdown(
    """
    <style>
        [data-testid="stSidebar"]::before {
            content: "Weather Information";
            display: flex;
            justify-content: center; /* Center horizontally */
            align-items: center;    /* Center vertically */
            height: 50px;           /* Define height for vertical centering */
            font-size: 20px;
            font-weight: bold;
            color: #2a3d42;         /* Text color */
            background-color: #cce7f0; /* Background color */
            padding: 0px 10px;      /* Adjust padding */
            border: 1px solid #4c98af; /* Border color */
            border-radius: 3px;     /* Rounded corners */
            margin-bottom: 10px;    /* Adds spacing below the label */
        }
    </style>
    """,
    unsafe_allow_html=True,
)



    
st_data = st_folium(world_map, use_container_width = True, height=800)  # Adjust dimensions for a wider layout

if st_data and "last_object_clicked" in st_data and st_data["last_object_clicked"]:
    clicked_city = st_data["last_object_clicked"]
    print(f"Clicked City : {clicked_city}")
    # print(f"City Data : {city_data}")
    if city_data.get((clicked_city['lat'], clicked_city['lng'])):

        city_details = city_data.get((clicked_city['lat'], clicked_city['lng']))
        city_name = city_details.get('city')
        city_state = city_details.get('state')

        # Generate live data
        live_data = get_live_data()
        current_temp=live_data["current_Temp"]
        feels_like_temp=live_data["feels_like_temp"]
        humidity=live_data["humidity"]
        wind_speed=live_data["wind_speed"]
        feel_vs_true = feels_like_temp - current_temp
        description = live_data["description"]

        # Get the icon for the current description
        description_icon = description_icon_map.get(description, "🌡️")

        st.sidebar.title(city_name)

        # Create a layout for temperature metric and description icon
        col11, col12 = st.sidebar.columns([3, 1])  # Adjust column ratios for spacing

        # Display temperature metric in the first column
        with col11:
            st.metric(
                label="Temperature", 
                value=f"{current_temp}°C", 
                delta=f"Feels {feel_vs_true:+}°C"
            )

        # Display enlarged icon in the second column
        with col12:
                st.markdown(
                f"""
                <div style="font-size: 50px; text-align: left; margin-left: -60px; margin-top: 20px;">{description_icon}</div>
                """,
            unsafe_allow_html=True,
            )

        # Humidity and Wind Speed on the Same Line
        col21, col22 = st.sidebar.columns(2)

        with col21:
            st.metric(label="💧 Humidity", value=f"{humidity}%", delta=None)

        with col22:
            st.metric(label="💨 Wind Speed", value=f"{wind_speed} m/s", delta=None)
            
        # forcast table
        st.sidebar.subheader("Temperture Forecast")
        #st.sidebar.dataframe(next_day_forecast[["avg_temp", "description"]])
        with st.sidebar:
            st.altair_chart(chart, use_container_width=True)





        # Update the sidebar with the city data
        # st.sidebar.subheader(f"City: {city_name}")
        # st.sidebar.write(f"Live Data: {live_data}")
        # st.sidebar.write("Additional Information:")
        # st.sidebar.write(f"Coordinates: {clicked_city}")
        # st.sidebar.title("Weather Settings")

        # Sidebar Fields
        # 1. Location Input
        # location = st.sidebar.text_input("Enter Location", placeholder="e.g., New York, USA")

        # 2. Date Range Picker
        # st.sidebar.subheader("Select Date Range")
        # date_range = st.sidebar.date_input(
        #     "Choose dates", 
        #     value=[None, None],  # Default value is empty
        #     help="Select a specific date or a range to get historical or forecast data"
        # )

        # 3. Weather Metrics
        st.sidebar.subheader("Other Information")

        # Display the entered note
        st.sidebar.write("Climate detail:")
        st.sidebar.write(other_information)

    
    
else: 
    st.sidebar.write("Select a city from the map to see more details.")
    # metrics = st.sidebar.multiselect(
    #     "Select Metrics to Display", 
    #     options=["Temperature", "Humidity", "Wind Speed", "Precipitation", "UV Index"],
    #     default=["Temperature", "Humidity"],
    #     help="Choose which weather metrics to show in the main dashboard"
    # )

    # # 4. Units Selector
    # st.sidebar.subheader("Units")
    # temp_unit = st.sidebar.radio("Temperature Unit", ["Celsius", "Fahrenheit"], index=0)
    # wind_speed_unit = st.sidebar.radio("Wind Speed Unit", ["km/h", "mph"], index=0)

    # # 5. Forecast Type
    # st.sidebar.subheader("Forecast Type")
    # forecast_type = st.sidebar.radio(
    #     "Choose Forecast Type",
    #     ["Current Weather", "Hourly Forecast", "Daily Forecast"],
    #     index=0
    # )

    # # 6. Refresh Button
    # st.sidebar.subheader("Actions")
    # if st.sidebar.button("Fetch Weather Data"):
    #     st.sidebar.success("Fetching data...")

    # # Main Page Content
    # st.title("Weather Application 🌤️")
    # st.write("Use the sidebar to configure your weather preferences.")

    # # Display selected options
    # st.write("### Selected Options")
    # st.write(f"Location: `{location}`")
    # # st.write(f"Date Range: `{date_range}`")
    # st.write(f"Metrics: `{metrics}`")
    # st.write(f"Temperature Unit: `{temp_unit}`")
    # st.write(f"Wind Speed Unit: `{wind_speed_unit}`")
    # st.write(f"Forecast Type: `{forecast_type}`")






### Configuring the page

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




