#!/bin/bash

echo "Cleaning up old data..."
# Purani formatted file delete karo (agar exist karti hai)
rm -f formatted_data.csv

echo "Running data processor to generate fresh data..."
# Aapki data processing script (Check kar lena file ka naam yahi hai na)
python data_processor.py 

echo "Starting the Dashboard..."
# Final Dashboard run karna
python app.py