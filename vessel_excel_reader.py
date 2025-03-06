# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 12:42:53 2025

@author: evert
"""

import pandas as pd
import numpy as np
import json
import os

def find_and_store_costs(labels, result_dict, sheet_path, sheet_name):
    """
    Searches for the given labels in an Excel sheet and stores their values in the result dictionary.

    Args:
        labels (list): List of labels to search for in the Excel sheet.
        result_dict (dict): An empty dictionary to store the results.
        sheet_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to search in.

    Returns:
        dict: Updated dictionary with the labels and their corresponding values.
    """
    # Load the Excel file
    df = pd.read_excel(sheet_path, sheet_name=sheet_name)
    
    # Iterate through each label and search for its value
    for label in labels:
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
                        result_dict[label] = float(next_cell)  # Store value as float in the result
                        found_value = True
                        break  # Stop after finding the first valid one
            if found_value:
                break  # Exit outer loop if a valid match is found
        
        # If no valid value is found, store None for that label
        if not found_value:
            print(f"No value found for: {label}\n")
            result_dict[label] = None
    
    return result_dict

# Path to the folder containing the Excel files
folder_path = r"C:\Users\evert\Documents\TU-Delft\TIL Master\MT44070 Shipping Management\MT44070_REPO\MT44070_SHIPPING\Vessels_DATA"

# List of labels to search for
labels_total_ship_costs = [
    "Running cost ship", 
    "Voyage cost ship", 
    "Port handling cost ship", 
    "Fixed cost ship"
]

labels_running_costs = [
    "Manning cost ship",
    "Store cost",
    "Insurance cost",
    "Repair and Maintainance cost",
    "Management cost"]

label_voyage_costs = [
    "Fuel cost ship ports",
    "Fuel cost ship ECA",
    "Fuel cost ship NON ECA",
    "Lub oil cost ship",
    "External cost",
    "ETS cost ship",
    "Cannel cost ship"]

# Dictionary to store all data for each model
all_models_data = {}

# Loop through all the Excel files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".xlsx"):  # Ensure it's an Excel file
        # Extract model number (TEU capacity) from the file name
        model_number = file_name.split(".")[0]  # Assumes the name is something like MODEL_23964
        
        # Full path to the current Excel file
        file_path = os.path.join(folder_path, file_name)

        # Initialize dictionaries for storing results for the current model
        Total_ship_costs = {}
        Running_costs = {}
        Voyage_costs = {}

        # Call the function for each category
        Total_ship_costs = find_and_store_costs(labels_total_ship_costs, Total_ship_costs, file_path, "CostShip")
        Running_costs = find_and_store_costs(labels_running_costs, Running_costs, file_path, "CostShip")
        Voyage_costs = find_and_store_costs(label_voyage_costs, Voyage_costs, file_path, "CostShip")

        # Store the results in the dictionary for the current model
        all_models_data[model_number] = {
            "Total_ship_costs": Total_ship_costs,
            "Running_costs": Running_costs,
            "Voyage_costs": Voyage_costs
        }

# Print the final dictionary containing data for all models
print(all_models_data)

output_file_path = r"C:\Users\evert\Documents\TU-Delft\TIL Master\MT44070 Shipping Management\MT44070_REPO\MT44070_SHIPPING\Vessels_DATA\all_models_data.json"

with open(output_file_path, 'w') as json_file:
    json.dump(all_models_data, json_file, indent=4)

print("")
print(f"Data saved to {output_file_path}")
    

















    