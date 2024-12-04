# Let's try again to generate the city data from the uploaded file

import pandas as pd

# Load the CSV file
df = pd.read_csv("https://raw.githubusercontent.com/Cavidan-oss/IDS_706_Final_Project/refs/heads/main/data/csv/processed/merged_dataset.csv")

# Extracting the relevant data from the DataFrame
cities_data = [
    {"name": row['city'], "lat": row['lat'], "lng": row['lng']}
    for index, row in df.iterrows()
]

# Displaying the first few cities
print(cities_data)
