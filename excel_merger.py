# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:53:33 2025

@author: evert
"""

import pandas as pd
import glob
import os

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(script_dir, "MERGE_DATA")

# Check if the folder exists
if not os.path.exists(folder_path):
    print(f"❌ ERROR: Folder {folder_path} does not exist.")
    exit()

# Get all Excel files in the folder
file_list = glob.glob(os.path.join(folder_path, "*.xlsx"))

# Debugging: Print found files
print(f"📂 Found {len(file_list)} Excel files: {file_list}")

# Check if any files were found
if not file_list:
    print("❌ ERROR: No Excel files found in MERGE_DATA.")
    exit()

# Read and merge files
df_list = [pd.read_excel(file) for file in file_list]
merged_df = pd.concat(df_list, ignore_index=True)

# Save merged file
output_path = os.path.join(script_dir, "merged_output.xlsx")
merged_df.to_excel(output_path, index=False)

print(f"✅ Merged file saved at: {output_path}")

