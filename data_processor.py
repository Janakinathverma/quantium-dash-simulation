import pandas as pd
import glob
import os

# 1. Define paths
DATA_DIR = "./data"
OUTPUT_FILE = "formatted_data.csv"

# 2. Load and Combine
csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))

if not csv_files:
    print(f"Error: No CSV files found in {DATA_DIR}")
else:
    combined_df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

    # 3. Filter for 'Pink Morsel'
    combined_df = combined_df[
        combined_df['product'].str.contains('pink morsel', case=False, na=False)
    ].copy()

    # 4. Clean Price BEFORE multiplication
    # BUG FIX: Always strip $ and commas regardless of dtype.
    # The old dtype=='object' guard was skipping the clean on some pandas versions,
    # causing the raw string to be used directly in the multiplication, which Python
    # interpreted as string repetition (* quantity) instead of numeric multiplication.
    combined_df['price'] = (
        combined_df['price']
        .astype(str)                          # ensure string for .str accessor
        .str.replace(r'[\$,]', '', regex=True) # strip $ and commas
        .astype(float)                         # convert to number
    )

    # 5. Quantity must also be numeric
    combined_df['quantity'] = pd.to_numeric(combined_df['quantity'], errors='coerce')

    # 6. Calculate Sales (now safely numeric * numeric)
    combined_df['sales'] = combined_df['price'] * combined_df['quantity']

    # 7. Select and Export
    final_df = combined_df[['sales', 'date', 'region']]
    final_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Success! Processed {len(final_df)} rows. Saved to {OUTPUT_FILE}")
    print(f"Sales range: ${final_df['sales'].min():.2f} – ${final_df['sales'].max():.2f}")