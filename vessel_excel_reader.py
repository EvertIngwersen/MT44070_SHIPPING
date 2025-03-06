# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 12:42:53 2025

@author: evert
"""


import pandas as pd
import numpy as np
import json
import os
import matplotlib.pyplot as plt

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

# Get the current working directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the "Vessels_DATA" folder
vessel_data_folder = os.path.join(current_directory, 'Vessels_DATA')

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
for file_name in os.listdir(vessel_data_folder):
    if file_name.endswith(".xlsx"):  # Ensure it's an Excel file
        # Extract model number (TEU capacity) from the file name
        model_number = file_name.split(".")[0]  # Assumes the name is something like MODEL_23964
        
        # Full path to the current Excel file
        file_path = os.path.join(vessel_data_folder, file_name)

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

# Define the output file path dynamically within the "Vessels_DATA" folder
output_file_path = os.path.join(vessel_data_folder, 'all_models_data.json')

# Save the dictionary to a JSON file
with open(output_file_path, 'w') as json_file:
    json.dump(all_models_data, json_file, indent=4)

print("")
print(f"Data saved to {output_file_path}")

#final commit message
    
def extract_cost_data(json_data, cost_category):
    """
    Extracts cost data for a given category from the JSON data.

    Args:
        json_data (dict): Dictionary containing cost data for different ship models.
        cost_category (str): The cost category to extract (Total_ship_costs, Running_costs, or Voyage_costs).

    Returns:
        dict: Dictionary where keys are cost labels and values are lists of (TEU, cost) tuples.
    """
    cost_data = {}

    for model, data in json_data.items():
        teu = int(model.split("_")[-1])  # Extract TEU from model name

        for label, cost in data[cost_category].items():
            if label not in cost_data:
                cost_data[label] = []
            if cost is not None:  # Ignore None values
                cost_data[label].append((teu, cost))

    # Sort each label's data by TEU (ensures x-axis is ordered correctly)
    for label in cost_data:
        cost_data[label] = sorted(cost_data[label], key=lambda x: x[0])

    return cost_data

# Load JSON data
current_directory = os.path.dirname(os.path.abspath(__file__))
vessel_data_folder = os.path.join(current_directory, 'Vessels_DATA')
json_file_path = os.path.join(vessel_data_folder, 'all_models_data.json')

with open(json_file_path, 'r') as json_file:
    all_models_data = json.load(json_file)

# Extract data for each category
total_cost_data = extract_cost_data(all_models_data, "Total_ship_costs")
running_cost_data = extract_cost_data(all_models_data, "Running_costs")
voyage_cost_data = extract_cost_data(all_models_data, "Voyage_costs")

# Function to plot costs
def plot_costs(cost_data, category_name):
    """
    Plots cost data for each label.

    Args:
        cost_data (dict): Dictionary where keys are cost labels and values are lists of (TEU, cost) tuples.
        category_name (str): The name of the cost category (used for titles and file names).
    """
    for label, values in cost_data.items():
        if not values:
            continue  # Skip empty labels

        # Extract TEU values and costs
        teus, costs = zip(*values)

        # Create plot
        plt.figure(figsize=(8, 5))
        plt.plot(teus, costs, marker='o', linestyle='-', color='b')
        plt.xlabel("Ship Model (TEU)")
        plt.ylabel("Cost")
        plt.title(f"{label} ({category_name})")
        plt.grid(True)

        # Save plot
        plot_filename = f"{label.replace(' ', '_')}_{category_name}.png"
        plot_path = os.path.join(vessel_data_folder, plot_filename)
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()

        print(f"Saved plot: {plot_path}")

# Generate plots
plot_costs(total_cost_data, "Total_ship_costs")
plot_costs(running_cost_data, "Running_costs")
plot_costs(voyage_cost_data, "Voyage_costs")

print("\nAll plots have been generated and saved in the Vessels_DATA folder.")
















    