import pandas as pd

df1 = pd.read_csv('https://raw.githubusercontent.com/Cavidan-oss/IDS_706_Final_Project/refs/heads/main/data/csv/raw/city_facts.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/Cavidan-oss/IDS_706_Final_Project/refs/heads/main/data/csv/processed/uscities_processed.csv')

merged_df = pd.merge(df1, df2, on=['city', 'state_name'])
merged_df.to_csv('merged_dataset.csv', index=False)

print(merged_df.head())
