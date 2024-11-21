import streamlit as st
import folium
from streamlit_folium import st_folium
import random

# Function to simulate live data (replace with your API call)
def get_live_data():
    return f"Live Data: {random.randint(100, 1000)}"

# Sample city data
cities = [
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"name": "Chicago", "lat": 41.8781, "lon": -87.6298},
]

# Create a Streamlit app
st.title("Interactive Dashboard with Map")

# Create a sidebar for the dashboard-like interface
st.sidebar.header("City Dashboard")
st.sidebar.write("Select a city from the map to see more details.")

# Create the layout with two columns: One for the sidebar and one for the map
col1, col2 = st.columns([1, 4])  # First column for sidebar (width 1), second for map (width 4)

# Sidebar for dashboard
with col1:
    st.sidebar.header("City Dashboard")
    st.sidebar.write("Select a city from the map to see more details.")

# Create a map
with col2:
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4,width=1000,tiles="Cartodb Positron",
                        height= 1000)

    # Add markers for each city
    for city in cities:
        folium.Marker(
            [city["lat"], city["lon"]],
            popup=city["name"],  # Show city name on click
            tooltip=city["name"],  # Tooltip shows on hover
        ).add_to(m)

    # Display map   
    st_data = st_folium(m, width=500, height=500)

# Sidebar Dashboard - Show data based on user interaction
if st_data and "last_object_clicked" in st_data and st_data["last_object_clicked"]:
    clicked_city = st_data["last_object_clicked"]
    city_name = 'Los Angeles'

    # Generate live data
    live_data = get_live_data()

    # Update the sidebar with the city data
    st.sidebar.subheader(f"City: {city_name}")
    st.sidebar.write(f"Live Data: {live_data}")
    
    # You can add more dashboard elements here (like charts, graphs, etc.)
    st.sidebar.write("Additional Information:")
    st.sidebar.write(f"Coordinates: {clicked_city}")
    
    # Example of a button to simulate actions
    if st.sidebar.button("Show more data"):
        st.sidebar.write("Here you could display more detailed data or trigger an action.")

# Add more elements to the main page if needed (e.g., summary of the dashboard, etc.)
st.write("Use the sidebar to view detailed information about the cities.")