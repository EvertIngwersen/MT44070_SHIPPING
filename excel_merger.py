# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:53:33 2025

@author: evert
"""

import pandas as pd
import glob
import os
import sys

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Correct folder path
folder_path = os.path.join(script_dir, "Vessels_DATA", "MERGE_DATA")

# Check if folder exists
if not os.path.exists(folder_path):
    print(f"❌ ERROR: Folder '{folder_path}' does not exist. Check the folder name and location.")
    sys.exit()

# Get all Excel files in the folder
file_list = glob.glob(os.path.join(folder_path, "*.xlsx"))

# Debugging: Print found files
print(f"📂 Found {len(file_list)} Excel files: {file_list}")

# Check if any files were found
if not file_list:
    print("❌ ERROR: No Excel files found in MERGE_DATA.")
    sys.exit()

# Dictionary to store dataframes for each sheet
merged_sheets = {}

# Read each Excel file
for file in file_list:
    xls = pd.ExcelFile(file)  # Load Excel file
    file_name = os.path.basename(file).replace('.xlsx', '')  # Get file name without extension
    
    for sheet_name in xls.sheet_names:  # Loop through all sheets
        # Create a new sheet name by appending file name to the sheet name
        new_sheet_name = f"{sheet_name}_{file_name}"
        
        # Read the sheet into a DataFrame
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # If the sheet already exists in merged_sheets, merge horizontally
        if new_sheet_name in merged_sheets:
            merged_sheets[new_sheet_name] = pd.concat([merged_sheets[new_sheet_name], df], axis=1)
        else:
            # Otherwise, simply add the sheet to the dictionary
            merged_sheets[new_sheet_name] = df

# Save merged output
output_path = os.path.join(script_dir, "Vessels_DATA", "merged_output.xlsx")

# Write each sheet back to a new Excel file
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    for sheet_name, df in merged_sheets.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"✅ Merged file saved at: {output_path}")





