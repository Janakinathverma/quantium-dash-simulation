import pandas as pd
import glob
import os

# 1. Define paths
DATA_DIR = "./data"
OUTPUT_FILE = "formatted_data.csv"

# 2. Load and Combine
# Using a list comprehension is a bit more 'Pythonic' and efficient
csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))

if not csv_files:
    print(f"Error: No CSV files found in {DATA_DIR}")
else:
    # Read all files and combine immediately
    combined_df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

    # 3. Filter for 'Pink Morsel'
    # Using .str.contains with case=False is often safer for variations
    combined_df = combined_df[combined_df['product'].str.contains('pink morsel', case=False, na=False)].copy()

    # 4. Clean Price and Calculate Sales
    # Use r'[\$,]' to avoid SyntaxWarnings and .replace to fix formatting
    if combined_df['price'].dtype == 'object':
        combined_df['price'] = combined_df['price'].replace(r'[\$,]', '', regex=True).astype(float)

    combined_df['sales'] = combined_df['price'] * combined_df['quantity']

    # 5. Select and Export
    final_df = combined_df[['sales', 'date', 'region']]
    final_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Success! Processed {len(final_df)} rows. Saved to {OUTPUT_FILE}")