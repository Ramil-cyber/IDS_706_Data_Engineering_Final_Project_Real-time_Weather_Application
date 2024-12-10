import pandas as pd

def process_raw_cities_csv(
    file_path, target_file_path, city_list=[['New York', 'New York'], ['Los Angeles', 'California'], ['Chicago', 'Illinois']]
):
    df = pd.read_csv(file_path)

    # Create a set of (city, state) tuples from city_list for fast lookup
    city_state_set = set(tuple(city_state) for city_state in city_list)

    # Update the lambda function to check both city and state
    df["active_cities"] = df.apply(lambda row: 1 if (row['city'], row['state_name']) in city_state_set else 0, axis=1)

    df.to_csv(target_file_path)

    return True


if __name__ == "__main__":
    city_list = [['Austin', 'Texas'],
                 ['Boston', 'Massachusetts'],
                 ['Chicago', 'Illinois'],
                 ['Columbus', 'Ohio'],
                 ['Dallas', 'Texas'],
                 ['Denver', 'Colorado'],
                 ['Houston', 'Texas'],
                 ['Indianapolis', 'Indiana'],
                 ['Los Angeles', 'California'],
                 ['Miami', 'Florida'],
                 ['Minneapolis', 'Minnesota'],
                 ['New York', 'New York'],
                 ['Oklahoma City', 'Oklahoma'],
                 ['Philadelphia', 'Pennsylvania'],
                 ['Raleigh', 'North Carolina'],
                 ['San Diego', 'California'],
                 ['San Francisco', 'California'],
                 ['Seattle', 'Washington'],
                 ['Shreveport', 'Louisiana'],
                 ['Washington', 'District of Columbia']]
    
    process_raw_cities_csv(
        file_path="data/csv/raw/uscities.csv",
        target_file_path="data/csv/processed/uscities_processed.csv",
        city_list=city_list
    )