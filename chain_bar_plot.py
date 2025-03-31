# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:39:59 2025

@author: evert
"""

import numpy as np
import matplotlib.pyplot as plt

# Data
categories = ["From Hinterland cost", "From Port cost", "Maritime cost", 
              "To Port cost", "To Hinterland cost", "Total Generalised cost"]

LNG = [1085.7482038294, 99.6525134105646, 1180.09232180842, 381.868486416876, 390.616842097209, 3137.97836756248]
Scrubbers = [1085.7482038294, 99.6525134105646, 632.241878165697, 381.829869501831, 390.616842097209, 2590.08930700471]
MDO = [1085.7482038294, 99.6525134105646, 637.590815501861, 381.829869501831, 390.616842097209, 2595.43824434087]

# Number of categories
x = np.arange(len(categories))  # X-axis positions
bar_width = 0.3  # Width of each bar

# Create the grouped bar plot
plt.figure(figsize=(10, 6))
plt.bar(x - bar_width, MDO, width=bar_width, label="MDO", color='blue')
plt.bar(x, Scrubbers, width=bar_width, label="SCRUBBER", color='orange')
plt.bar(x + bar_width, LNG, width=bar_width, label="LNG", color='green')

# Labels and title
plt.title("Cost Breakdown for Different Propulsion in Chain")
plt.xlabel("Cost Categories")
plt.grid()
plt.ylabel("Cost (€)")
plt.title("Fuel Cost Breakdown by Ship Type")
plt.xticks(x, categories, rotation=30, ha="right")  # Rotate labels for readability
plt.legend()

# Show the plot
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
