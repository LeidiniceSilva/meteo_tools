# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilvae@gmail.com"
__date__        = "March 31, 2025"
__description__ = "ESM LAB session plots"

import matplotlib.pyplot as plt
import pandas as pd

# Define the data
data = {
    "Metric Name": [
        "Mean Bias Error (MBE)",
        "Mean Absolute Error (MAE)",
        "Root Mean Square Error (RMSE)",
        "Normalized RMSE (NRMSE)",
        "Mean Squared Error Skill Score (MSESS)",
        "Correlation Coefficient (R)",
        "Coefficient of Determination (R²)",
        "Taylor Skill Score (TSS)",
        "Index of Agreement (d)",
        "Brier Score"
    ],
    
    "Equation": [
        r"$MBE = \frac{1}{N} \sum_{i=1}^{N} (M_i - O_i)$",
        r"$MAE = \frac{1}{N} \sum_{i=1}^{N} |M_i - O_i|$",
        r"$RMSE = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (M_i - O_i)^2}$",
        r"$NRMSE = \frac{RMSE}{O_{max} - O_{min}}$",
        r"$MSESS = 1 - \frac{MSE}{MSE_{ref}}$",
        r"$R = \frac{\sum (O_i - \bar{O}) (M_i - \bar{M})}{\sqrt{\sum (O_i - \bar{O})^2 \sum (M_i - \bar{M})^2}}$",
        r"$R^2 = \left(\frac{Cov(O, M)}{\sigma_O \sigma_M}\right)^2$",
        r"$TSS = 1 - \frac{(1 + R)^4}{4(\sigma_M/\sigma_O + 1/\sigma_M/\sigma_O)^2}$",
        r"$d = 1 - \frac{\sum (M_i - O_i)^2}{\sum (|M_i - \bar{O}| + |O_i - \bar{O}|)^2}$",
        r"$BS = \frac{1}{N} \sum_{i=1}^{N} (p_i - o_i)^2$"
    ],
    
    "Reference Values": [
        "Ideal: 0 (no bias)",
        "Always positive",
        "Lower values indicate better accuracy",
        "Typically reported as a percentage",
        "Range: -∞ to 1",
        "Range: -1 to 1",
        "Range: 0 to 1",
        "1 is perfect agreement",
        "Range: 0 to 1 (1 = perfect match)",
        "Lower values indicate better probabilistic prediction"
    ],
    
    "Applicability": [
        "Measures systematic error (over/underestimation)",
        "Evaluates overall model accuracy",
        "Penalizes large errors more than MAE",
        "Allows comparison across different datasets",
        "Compares model error relative to a reference (e.g., climatology)",
        "Measures strength and direction of the relationship",
        "Indicates the proportion of variance explained",
        "Summarizes correlation, variance, and RMSE",
        "Measures how well model predictions match observations",
        "Used in climate risk and ensemble forecasting"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Create the figure
fig, ax = plt.subplots(figsize=(14, 10))  # Increased height for better spacing
ax.axis("tight")
ax.axis("off")

# Create the table
table = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    cellLoc="center",
    loc="center",
    colColours=["#E0E0E0"] * 4  # Light gray column headers
)

# Improve table appearance
table.auto_set_font_size(False)
table.set_fontsize(14)
table.auto_set_column_width([0, 1, 2, 3])

# Adjust row height for more spacing
row_height = 0.08  # Increased row height for better spacing
for i in range(len(df) + 1):  # Including header row
    for j in range(len(df.columns)):
        cell = table[i, j]
        cell.set_edgecolor("black")
        cell.set_linewidth(0.5)
        cell.set_height(row_height)  # Increase row height

        # Improve header row styling
        if i == 0:
            cell.set_fontsize(14)
            cell.set_linewidth(1)

# Save and show the figure 
plt.savefig("climatology_metrics.png", dpi=400, bbox_inches="tight")
plt.show()
exit()
