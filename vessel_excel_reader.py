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
    df = pd.read_excel(sheet_path, sheet_name=sheet_name)

    for label in labels:
        cell_location = df.isin([label])  
        found_value = False

        for row in range(len(df)):
            for col in range(len(df.columns) - 1):
                if cell_location.iloc[row, col]:  
                    next_cell = df.iloc[row, col + 1]  

                    if isinstance(next_cell, (int, float)) and not np.isnan(next_cell):
                        result_dict[label] = float(next_cell)  
                        found_value = True
                        break  
            if found_value:
                break  

        if not found_value:
            print(f"No value found for: {label}\n")
            result_dict[label] = None

    return result_dict

# Get the current working directory dynamically
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the new path to the "VESSELS" folder inside "Vessel_DATA"
vessel_data_folder = os.path.join(current_directory, 'Vessels_DATA', 'VESSELS')

# Ensure the folder exists
if not os.path.exists(vessel_data_folder):
    raise FileNotFoundError(f"Error: The folder '{vessel_data_folder}' does not exist!")

# List of cost labels
labels_total_ship_costs = ["Running cost ship", "Voyage cost ship", "Port handling cost ship", "Fixed cost ship"]
labels_running_costs = ["Manning cost ship", "Store cost", "Insurance cost", "Repair and Maintainance cost", "Management cost"]
label_voyage_costs = ["Fuel cost ship ports", "Fuel cost ship ECA", "Fuel cost ship NON ECA", "Lub oil cost ship", "External cost", "ETS cost ship", "Cannel cost ship"]

# Dictionary to store all data
all_models_data = {}

# Loop through all Excel files in the VESSELS folder
for file_name in os.listdir(vessel_data_folder):
    if file_name.endswith(".xlsx"):  
        model_number = file_name.split(".")[0]  

        file_path = os.path.join(vessel_data_folder, file_name)

        # Initialize dictionaries for storing results
        Total_ship_costs = {}
        Running_costs = {}
        Voyage_costs = {}

        # Extract cost data
        Total_ship_costs = find_and_store_costs(labels_total_ship_costs, Total_ship_costs, file_path, "CostShip")
        Running_costs = find_and_store_costs(labels_running_costs, Running_costs, file_path, "CostShip")
        Voyage_costs = find_and_store_costs(label_voyage_costs, Voyage_costs, file_path, "CostShip")

        # Store the results
        all_models_data[model_number] = {
            "Total_ship_costs": Total_ship_costs,
            "Running_costs": Running_costs,
            "Voyage_costs": Voyage_costs
        }

# Print result
print(all_models_data)

# Save JSON file in "Vessel_DATA" (not in "VESSELS")
output_file_path = os.path.join(current_directory, 'Vessels_DATA', 'all_models_data.json')

with open(output_file_path, 'w') as json_file:
    json.dump(all_models_data, json_file, indent=4)

print(f"\nData saved to {output_file_path}")

# Function to extract cost data
def extract_cost_data(json_data, cost_category):
    cost_data = {}

    for model, data in json_data.items():
        teu = int(model.split("_")[-1])  

        for label, cost in data[cost_category].items():
            if label not in cost_data:
                cost_data[label] = []
            if cost is not None:  
                cost_data[label].append((teu, cost))

    for label in cost_data:
        cost_data[label] = sorted(cost_data[label], key=lambda x: x[0])

    return cost_data

# Load JSON data
with open(output_file_path, 'r') as json_file:
    all_models_data = json.load(json_file)

# Extract cost data
total_cost_data = extract_cost_data(all_models_data, "Total_ship_costs")
running_cost_data = extract_cost_data(all_models_data, "Running_costs")
voyage_cost_data = extract_cost_data(all_models_data, "Voyage_costs")

# Create a "Plots" folder inside "Vessel_DATA"
plots_folder = os.path.join(current_directory, 'Vessels_DATA', 'Plots')
os.makedirs(plots_folder, exist_ok=True)  

# Function to plot costs
def plot_costs(cost_data, category_name):
    for label, values in cost_data.items():
        if not values:
            continue  

        teus, costs = zip(*values)

        plt.figure(figsize=(8, 5))
        plt.plot(teus, costs, marker='o', linestyle='-', color='b')
        plt.xlabel("Ship Model (TEU)")
        plt.ylabel("Cost")
        plt.title(f"{label} ({category_name})")
        plt.grid(True)

        plot_filename = f"{label.replace(' ', '_')}_{category_name}.png"
        plot_path = os.path.join(plots_folder, plot_filename)
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()

        print(f"Saved plot: {plot_path}")

# Generate plots
plot_costs(total_cost_data, "Total_ship_costs")
plot_costs(running_cost_data, "Running_costs")
plot_costs(voyage_cost_data, "Voyage_costs")

print("\nAll plots have been saved in 'Vessels_DATA/Plots'.")


def read_cost_chain_data(file_path, sheet_name="CostChain_TwoNuts"):
    """
    Reads a specific range (D6:N21) from the given Excel sheet and stores the data in a dictionary.

    Args:
        file_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet containing cost chain data.

    Returns:
        pd.DataFrame: DataFrame containing the cost chain data.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols="D:N", skiprows=5, nrows=16)

        # Drop rows and columns with all NaN values
        df = df.dropna(how="all").dropna(axis=1, how="all")

        return df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# Get the current directory dynamically
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path to "Vessels_DATA\CHAIN"
chain_folder = os.path.join(current_directory, 'Vessels_DATA', 'CHAIN')

# Ensure the folder exists
if not os.path.exists(chain_folder):
    raise FileNotFoundError(f"Error: The folder '{chain_folder}' does not exist!")

# Dictionary to store all models
all_chain_data = {}
lowest_cost_chains = {}

# Loop through all Excel files in the CHAIN folder
for file_name in os.listdir(chain_folder):
    if file_name.startswith("MODEL_CHAIN_") and file_name.endswith(".xlsx"):
        try:
            # Extract TEU number from file name (MODEL_CHAIN_6865.xlsx → 6865)
            teu_number = int(file_name.split("_")[-1].split(".")[0])

            # Construct full file path
            file_path = os.path.join(chain_folder, file_name)

            # Read the cost chain data
            df = read_cost_chain_data(file_path)

            if df is not None:
                # Convert to dictionary and store full data
                all_chain_data[teu_number] = df.to_dict(orient="list")

                # Find the row with the minimum total cost
                min_cost_index = df["Total generalised chain cost"].idxmin()
                lowest_cost_chain = df.iloc[min_cost_index].to_dict()
                
                # Store the lowest cost chain for this TEU model
                lowest_cost_chains[teu_number] = lowest_cost_chain
        except ValueError:
            print(f"Skipping file {file_name} (TEU number extraction failed).")

# Sort both dictionaries by TEU number (ascending order)
sorted_chain_data = dict(sorted(all_chain_data.items()))
sorted_lowest_cost_chains = dict(sorted(lowest_cost_chains.items()))

# Define output file paths
output_all_data_path = os.path.join(current_directory, 'Vessels_DATA', 'all_chain_data.json')
output_lowest_cost_path = os.path.join(current_directory, 'Vessels_DATA', 'lowest_cost_chains.json')

# Save all chain data
with open(output_all_data_path, 'w') as json_file:
    json.dump(sorted_chain_data, json_file, indent=4)

# Save lowest-cost chain data
with open(output_lowest_cost_path, 'w') as json_file:
    json.dump(sorted_lowest_cost_chains, json_file, indent=4)

print(f"\nData saved to {output_all_data_path} (sorted by TEU number).")
print(f"Lowest cost chains saved to {output_lowest_cost_path} (sorted by TEU number).")






























