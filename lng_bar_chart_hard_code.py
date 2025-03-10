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
data = {
    "MODEL_23964_BASE": {
        "Total_ship_costs": {
            "Running cost ship": 480936.0,
            "Voyage cost ship": 8929520.0,
            "Port handling cost ship": 7403358.0,
            "Fixed cost ship": 3977509.0
        },
        "Running_costs": {
            "Manning cost ship": 207612.0,
            "Store cost": 8307.0,
            "Insurance cost": 217422.0,
            "Repair and Maintainance cost": 18891.0,
            "Management cost": 28705.0
        },
        "Voyage_costs": {
            "Fuel cost ship ports": 202937.0,
            "Fuel cost ship ECA": 473413.0,
            "Fuel cost ship NON ECA": 4454960.0,
            "Lub oil cost ship": 27718.0,
            "External cost": 0.0,
            "ETS cost ship": 413617.0,
            "Cannel cost ship": 2053900.0
        }
    },
    "MODEL_23964_LNG": {
        "Total_ship_costs": {
            "Running cost ship": 480936.0,
            "Voyage cost ship": 30133473.0,
            "Port handling cost ship": 7403358.0,
            "Fixed cost ship": 3977509.0
        },
        "Running_costs": {
            "Manning cost ship": 207612.0,
            "Store cost": 8307.0,
            "Insurance cost": 217422.0,
            "Repair and Maintainance cost": 18891.0,
            "Management cost": 28705.0
        },
        "Voyage_costs": {
            "Fuel cost ship ports": 217162.0,
            "Fuel cost ship ECA": 1728733.0,
            "Fuel cost ship NON ECA": 24389368.0,
            "Lub oil cost ship": 27718.0,
            "External cost": 0.0,
            "ETS cost ship": 413617.0,
            "Cannel cost ship": 2053900.0
        }
    }
}

# Function to calculate total costs per category
def compute_totals(model_data):
    total_ship = sum(model_data["Total_ship_costs"].values())
    running = sum(model_data["Running_costs"].values())
    voyage = sum(model_data["Voyage_costs"].values())
    total = total_ship + running + voyage
    return total_ship, running, voyage, total

# Compute totals for each model
base_totals = compute_totals(data["MODEL_23964_BASE"])
lng_totals = compute_totals(data["MODEL_23964_LNG"])

# Calculate percentages for each cost category
base_percentages = [base_totals[0] / base_totals[3] * 100,
                    base_totals[1] / base_totals[3] * 100,
                    base_totals[2] / base_totals[3] * 100]

lng_percentages = [lng_totals[0] / lng_totals[3] * 100,
                   lng_totals[1] / lng_totals[3] * 100,
                   lng_totals[2] / lng_totals[3] * 100]

# Define models, categories, and fixed colors for each category
models = ["23964 TEU", "23964 TEU (LNG and Scrubber)"]
categories = ["Total_ship_costs", "Running_costs", "Voyage_costs"]
colors = {
    "Total_ship_costs": "blue",
    "Running_costs": "orange",
    "Voyage_costs": "green"
}
bar_width = 0.5

fig, ax = plt.subplots()

# Plot stacked bars for MODEL_23964_BASE with labels
ax.bar(models[0], base_percentages[0], width=bar_width, label="Total_ship_costs", color=colors["Total_ship_costs"])
ax.bar(models[0], base_percentages[1], width=bar_width, label="Running_costs", 
       bottom=base_percentages[0], color=colors["Running_costs"])
ax.bar(models[0], base_percentages[2], width=bar_width, label="Voyage_costs", 
       bottom=base_percentages[0] + base_percentages[1], color=colors["Voyage_costs"])

# Plot stacked bars for MODEL_23964_LNG without duplicating labels
ax.bar(models[1], lng_percentages[0], width=bar_width, color=colors["Total_ship_costs"])
ax.bar(models[1], lng_percentages[1], width=bar_width, 
       bottom=lng_percentages[0], color=colors["Running_costs"])
ax.bar(models[1], lng_percentages[2], width=bar_width, 
       bottom=lng_percentages[0] + lng_percentages[1], color=colors["Voyage_costs"])

# Customize the chart
ax.set_ylabel("Percentage (%)")
ax.set_title("Cost Breakdown by of Propulsion Type")
ax.legend()

# Save the figure to the specified directory
save_path = r"C:\Users\evert\Documents\TU-Delft\TIL Master\MT44070 Shipping Management\MT44070_REPO\MT44070_SHIPPING\Vessels_DATA\Plots\cost_breakdown.png"
plt.savefig(save_path)
plt.show()
