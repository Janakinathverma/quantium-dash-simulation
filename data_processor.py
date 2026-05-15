import pandas as pd
import glob
import os

# 1. Define paths
DATA_DIR = "./data"  # Make sure this matches your folder structure
OUTPUT_FILE = "formatted_data.csv"

# 2. Load all CSV files from the data folder
csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
data_frames = []

for file in csv_files:
    df = pd.read_csv(file)
    data_frames.append(df)

# 3. Combine all three files into one big dataframe
combined_df = pd.concat(data_frames, ignore_index=True)

# 4. Filter for 'Pink Morsel' only
# We use .str.lower() just in case there are casing inconsistencies
combined_df = combined_df[combined_df['product'].str.lower() == 'pink morsel']

# 5. Calculate 'sales' (price * quantity)
# First, clean the price column if it has '$' symbols
if combined_df['price'].dtype == 'object':
    combined_df['price'] = combined_df['price'].replace('[\$,]', '', regex=True).astype(float)

combined_df['sales'] = combined_df['price'] * combined_df['quantity']

# 6. Select only the required columns
final_df = combined_df[['sales', 'date', 'region']]

# 7. Export to CSV
final_df.to_csv(OUTPUT_FILE, index=False)

print(f"Success! Processed data saved to {OUTPUT_FILE}")