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
Total_ship_costs = {}

# List of target labels to search for
labels_total_ship_costs = ["Running cost ship", 
          "Voyage cost ship", 
          "Port handling cost ship", 
          "Fixed cost ship"
          ]

# Iterate through each label and search for its value
for label in labels_total_ship_costs:
    # Find all occurrences of the label
    cell_location = df.isin([label])  # Boolean mask
    found_value = False
    
    # Iterate over matching locations
    for row in range(len(df)):
        for col in range(len(df.columns) - 1):  # Avoid out-of-bounds error
            if cell_location.iloc[row, col]:  # If label found
                next_cell = df.iloc[row, col + 1]  # Value next to it
                
                # Check if the next cell is a number (integer or float)
                if isinstance(next_cell, (int, float)) and not np.isnan(next_cell):
                    Total_ship_costs[label] = float(next_cell)  # Store value as float in the result
                    found_value = True
                    break  # Stop after finding the first valid one
        if found_value:
            break  # Exit outer loop if a valid match is found
    
    # If no valid value is found, store None for that label
    if not found_value:
        print("No value found for:", label)
        print("")
        Total_ship_costs[label] = None

# Print result
print(Total_ship_costs)
    

















    