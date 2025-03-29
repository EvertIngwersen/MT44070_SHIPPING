import matplotlib.pyplot as plt
import matplotlib as mpl

# Check available styles
print("Available styles:", plt.style.available)

# Use a seaborn style that is available
plt.style.use('seaborn-v0_8-colorblind')

# Customize rcParams to mimic Excel-like formatting
mpl.rcParams.update({
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'grid.color': 'lightgray',
    'grid.linestyle': '--',
    'grid.linewidth': 0.5,
    'font.family': 'Calibri',  # if Calibri is installed, otherwise choose another font
    'axes.titleweight': 'bold',
    'axes.titlesize': 14,
    'axes.labelsize': 12
})
# Provided data
# data = {
#     "MODEL_23964_BASE": {
#         "Total_ship_costs": {
#             "Running cost ship": 480936.0,
#             "Voyage cost ship": 8929520.0,
#             "Port handling cost ship": 7403358.0,
#             "Fixed cost ship": 3977509.0
#         },
#         "Running_costs": {
#             "Manning cost ship": 207612.0,
#             "Store cost": 8307.0,
#             "Insurance cost": 217422.0,
#             "Repair and Maintainance cost": 18891.0,
#             "Management cost": 28705.0
#         },
#         "Voyage_costs": {
#             "Fuel cost ship ports": 202937.0,
#             "Fuel cost ship ECA": 473413.0,
#             "Fuel cost ship NON ECA": 4454960.0,
#             "Lub oil cost ship": 27718.0,
#             "External cost": 0.0,
#             "ETS cost ship": 413617.0,
#             "Cannel cost ship": 2053900.0
#         }
#     },
#     "MODEL_23964_LNG": {
#         "Total_ship_costs": {
#             "Running cost ship": 480936.0,
#             "Voyage cost ship": 30133473.0,
#             "Port handling cost ship": 7403358.0,
#             "Fixed cost ship": 3977509.0
#         },
#         "Running_costs": {
#             "Manning cost ship": 207612.0,
#             "Store cost": 8307.0,
#             "Insurance cost": 217422.0,
#             "Repair and Maintainance cost": 18891.0,
#             "Management cost": 28705.0
#         },
#         "Voyage_costs": {
#             "Fuel cost ship ports": 217162.0,
#             "Fuel cost ship ECA": 1728733.0,
#             "Fuel cost ship NON ECA": 24389368.0,
#             "Lub oil cost ship": 27718.0,
#             "External cost": 0.0,
#             "ETS cost ship": 413617.0,
#             "Cannel cost ship": 2053900.0
#         }
#     }
# }


import matplotlib.pyplot as plt
import matplotlib as mpl

# Use a seaborn style
plt.style.use('seaborn-v0_8-colorblind')

# Customize rcParams for an Excel-like look
mpl.rcParams.update({
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'grid.color': 'lightgray',
    'grid.linestyle': '--',
    'grid.linewidth': 0.5,
    'font.family': 'Calibri',
    'axes.titleweight': 'bold',
    'axes.titlesize': 14,
    'axes.labelsize': 12
})

# Provided data
data = {
    "MODEL_23964_BASE": {
        "Total_ship_costs": {
            "Running cost ship": 480936.0,
            "Voyage cost ship": 8929520.0,
            "Port handling cost ship": 7403358.0,
            "Fixed cost ship": 3977509.0
        }
    },
    "MODEL_23964_LNG": {
        "Total_ship_costs": {
            "Running cost ship": 480936.0,
            "Voyage cost ship": 30133473.0,
            "Port handling cost ship": 7403358.0,
            "Fixed cost ship": 3977509.0
        }
    }
}

# Function to compute percentage breakdown
def compute_percentages(model_data):
    total_cost = sum(model_data["Total_ship_costs"].values())
    return {k: (v / total_cost) * 100 for k, v in model_data["Total_ship_costs"].items()}

# Compute percentages
base_percentages = compute_percentages(data["MODEL_23964_BASE"])
lng_percentages = compute_percentages(data["MODEL_23964_LNG"])

# Define models, categories, and colors
models = ["23964 TEU", "23964 TEU (LNG or Scrubber)"]
categories = ["Running cost ship", "Voyage cost ship", "Port handling cost ship", "Fixed cost ship"]
colors = {
    "Running cost ship": "blue",
    "Voyage cost ship": "orange",
    "Port handling cost ship": "green",
    "Fixed cost ship": "red"
}
bar_width = 0.5

# Create the figure with a smaller size
fig, ax = plt.subplots(figsize=(8, 6))

# Initialize bottom values for stacking
bottom_base = [0, 0]  # For 23964 TEU and 23964 TEU (LNG)
bars = []  # To store bar elements for the legend

# Plot stacked bars
for category in categories:
    bars.append(ax.bar(models, [base_percentages[category], lng_percentages[category]], 
                        width=bar_width, label=category, color=colors[category], bottom=bottom_base))
    
    # Update bottom values for stacking
    bottom_base = [bottom_base[i] + val for i, val in enumerate([base_percentages[category], lng_percentages[category]])]

# Customize the chart
ax.set_ylabel("Percentage (%)", fontsize=12)
ax.set_xlabel("Ship Type", fontsize=12)
ax.set_title("Cost Breakdown by Propulsion Type", fontsize=14)
ax.tick_params(axis='x', rotation=30, labelsize=10)
ax.tick_params(axis='y', labelsize=10)

# Add a proper legend with all cost categories
ax.legend(title="Cost Components", loc="upper right", fontsize=10)

# Save the figure
save_path = r"C:\Users\evert\Documents\TU-Delft\TIL Master\MT44070 Shipping Management\MT44070_REPO\MT44070_SHIPPING\Vessels_DATA\Plots\cost_breakdown.png"
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.show()

