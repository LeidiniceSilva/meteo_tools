# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "Dec 04, 2024"
__description__ = "Script to plot textbook figures"

import matplotlib.pyplot as plt
import numpy as np

# Altitude (km)
altitude = np.array([0, 10, 21, 32, 49, 52, 60, 80, 87, 88])
temperature = np.array([15, -56.5, -56.5, -44, -5, -5, -20, -90, -90, -85])

# Atmospheric layers and colors
boundaries = {
    "TROPOSFERA": (0, 10),
    "ESTRATOSFERA": (10, 48),
    "MESOSFERA": (50, 80),
    "TERMOSFERA": (80, 90),
}
colors = ['#cce5ff', '#d9f2d9', '#f2e6d9', '#ffd9ec']

# Layer and pause labels
labels = {
    "TROPOSFERA": 6,
    "TROPOPAUSA": 11,
    "ESTRATOSFERA": 25,
    "ESTRATOPAUSA": 49,
    "MESOSFERA": 69,
    "MESOPAUSA": 81,
    "TERMOSFERA": 85
}

# Plot setup
fig, ax1 = plt.subplots(figsize=(8, 8))
ax2 = ax1.twiny()

# Fill atmospheric layers
for (i, (layer, (bottom, top))) in enumerate(boundaries.items()):
    ax1.fill_betweenx([bottom, top], -100, 50, color=colors[i], alpha=0.5)

# Plot temperature profile
ax1.plot(temperature, altitude, color='black', linewidth=2)

# Add layer names
for label, alt in labels.items():
    ax1.text(0, alt, label, fontsize=9, ha='left', va='center', color='darkgray', weight='bold')

# Add thick horizontal bands for pauses
for pause in [10, 48, 80]:
    ax1.fill_betweenx([pause - 0, pause + 2], -100, 50, color='white')

# Draw dotted vertical temperature lines
for t in np.arange(-80, 41, 20):
    ax1.axvline(t, color='black', linestyle='--', linewidth=0.5)

# Altitude axis
ax1.set_ylim(0, 90)
ax1.set_xlim(-100, 50)
ax1.set_ylabel("ALTITUDE (km)", fontsize=10)
ax1.set_xlabel("TEMPERATURA (°C)", fontsize=10)

# Pressure axis (right)
pressure_ticks = [1000, 100, 10, 1, 0.1, 0.01]
alt_for_pressure = -7 * np.log(np.array(pressure_ticks) / 1000)
ax3 = ax1.secondary_yaxis('right')
ax3.set_yticks(alt_for_pressure)
ax3.set_yticklabels([f"{p:.2f}" if p < 1 else f"{int(p)}" for p in pressure_ticks])
ax3.set_ylabel("PRESSÃO (mb)", fontsize=10)

# Grid and layout
ax1.grid(True, which='both', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('atmospheric_profile.png', dpi=300)
plt.show()
exit()


