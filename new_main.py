import streamlit as st
import folium
from streamlit_folium import st_folium
import random


################## This part will change in next week
def get_live_data():
    return f"{random.randint(-10, 50)}"

# Sample city data
cities = [
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"name": "Chicago", "lat": 41.8781, "lon": -87.6298},
]
#################### Initial page design



st.set_page_config(
    page_title="Travel Exploration",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# temp_unit = st.sidebar.radio("Temperature Unit", ["Celsius", "Fahrenheit"], index=0)
# wind_speed_unit = st.sidebar.radio("Wind Speed Unit", ["km/h", "mph"], index=0)

# st.title("Weather Application!")
# Showcase Predefined Metrics



# if "clicked" not in st.session_state:
#     st.session_state.clicked = False  # Initialize state

# # Display the initial sidebar content
# if not st.session_state.clicked:
st.sidebar.write("Select a city from the map to see more details.")


######################### Map Part


world_map = folium.Map(
        location=[37.0902, -95.7129],
        tiles="Cartodb Positron",
        zoom_start=4,
    )

for city in cities:
    folium.Marker(
        [city["lat"], city["lon"]],
        popup=city["name"],  # Show city name on click
        tooltip=city["name"],  # Tooltip shows on hover
    ).add_to(world_map)



st_data = st_folium(world_map, use_container_width = True, height=800)  # Adjust dimensions for a wider layout


print(st_data["last_object_clicked"])


if st_data and "last_object_clicked" in st_data and st_data["last_object_clicked"]:
    clicked_city = st_data["last_object_clicked"]
    city_name = 'Los Angeles'

    # Generate live data
    live_data = get_live_data()

    st.sidebar.subheader("📋 Predefined Metrics (Example)")
    st.sidebar.write("Here's an example of weather data:")
    st.sidebar.metric(label="Temperature", value=f'{live_data}°C')
    st.sidebar.metric(label="Humidity", value="60%", delta="5%")

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
    st.sidebar.subheader("Weather Metrics")
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

# st.components.v1.html(folium.Figure().add_child(world_map).render(), height=800)



