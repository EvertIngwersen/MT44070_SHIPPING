# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:53:33 2025

@author: evert
"""

import pandas as pd
import glob
import os

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the subfolder
folder_path = os.path.join(script_dir, "MERGE_DATA")

# Get all Excel files in the subfolder
file_list = glob.glob(os.path.join(folder_path, "*.xlsx"))  # Change to "*.xls" if needed

# Read and merge all files
df_list = [pd.read_excel(file) for file in file_list]
merged_df = pd.concat(df_list, ignore_index=True)

# Save the merged file in the same directory as the script
output_path = os.path.join(script_dir, "merged_output.xlsx")
merged_df.to_excel(output_path, index=False)

print(f"Merged file saved at: {output_path}")
