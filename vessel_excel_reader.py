# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 12:42:53 2025

@author: evert
"""

import pandas as pd
import numpy as np

path = r"C:\Users\evert\Documents\TU-Delft\TIL Master\MT44070 Shipping Management\MT44070_REPO\MT44070_SHIPPING\Vessels_DATA\MODEL_23964.xlsx"
df = pd.read_excel(path, sheet_name="CostShip") 


# Dictionary to store results
result = {}

# Find all occurrences of "Running Cost Ship"
cell_location = df.isin(["Running Cost Ship"])  # Boolean mask

# Flag to check if a valid value is found
found_value = False

# Iterate over matching locations
for row in range(len(df)):
    for col in range(len(df.columns) - 1):  # Avoid out-of-bounds error
        if cell_location.iloc[row, col]:  # If "Running Cost Ship" found
            next_cell = df.iloc[row, col + 1]  # Value next to it
            
            # Check if the next cell is a number (integer or float)
            if isinstance(next_cell, (int, float)) and not np.isnan(next_cell):
                result["Running_cost_value"] = next_cell  # Store in dictionary
                found_value = True
                break  # Stop after finding the first valid one
    else:
        continue
    break  # Exit outer loop if a valid match is found

# If no valid value is found
if not found_value:
    result["Running_cost_value"] = None  # No valid value found

# Print result
print(result)
    
    

    