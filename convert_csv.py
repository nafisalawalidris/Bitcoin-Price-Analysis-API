import pandas as pd

# Load the CSV file
df = pd.read_csv('C:/Users/USER/Downloads/Bitcoin-Price-Analysis-API/data/BTC-USD Yahoo Finance - Max Yrs.csv')

# Convert scientific notation to integers
df['Volume'] = df['Volume'].apply(lambda x: int(float(x)))

# Save the updated CSV
df.to_csv('C:/Users/USER/Downloads/Bitcoin-Price-Analysis-API/data/BTC-USD Yahoo Finance - Max Yrs_updated.csv', index=False)

