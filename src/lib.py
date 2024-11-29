import pandas as pd


def process_raw_cities_csv(
    file_path, target_file_path, city_list=["New York", "Los Angeles", "Chicago"]
):
    df = pd.read_csv(file_path)

    df["active_cities"] = df["city"].apply(lambda x: 1 if x in city_list else 0)

    df.to_csv(target_file_path)

    return True

if __name__ == "__main__":
    process_raw_cities_csv(
        file_path="data/csv/raw/uscities.csv",
        target_file_path="data/csv/processed/uscities_processed.csv",
    )
