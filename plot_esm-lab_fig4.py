# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilvae@gmail.com"
__date__        = "March 31, 2025"
__description__ = "ESM LAB session plots"

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set up the figure
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Define pressure levels from surface to upper atmosphere
pressure_levels = np.array([1000, 850, 700, 500, 300, 200, 100, 50, 10])  # in hPa

# Create altitude scaling (higher pressure = lower altitude)
altitude_approx = np.array([0, 1.5, 3, 5.5, 9, 12, 16, 20, 30])  # Approximate altitudes in km
scaled_levels = altitude_approx  # Positive values (will invert axis)

# Create grid for latitude and longitude
lat = np.linspace(-90, 90, 37)  # 5-degree steps
lon = np.linspace(-180, 180, 73)  # 5-degree steps
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Create colormap - NOT inverted (higher pressure = warmer colors)
colors = plt.cm.plasma(np.linspace(0, 1, len(pressure_levels)))  # Standard orientation (0→1)

# Plot each pressure level
for i, (p, level) in enumerate(zip(pressure_levels[::-1], scaled_levels[::-1])):  # Reverse iteration order
    z = np.full_like(lon_grid, level)
    
    ax.plot_surface(lon_grid, lat_grid, z, 
                   color=colors[i],
                   alpha=0.6, 
                   edgecolor='k', 
                   linewidth=0.3)

# Set axis labels and title
ax.set_xlabel('Longitude (°)', fontsize=12, labelpad=15)
ax.set_ylabel('Latitude (°)', fontsize=12, labelpad=15)
ax.set_zlabel('Altitude (km)', fontsize=12, labelpad=15)

# Invert ONLY the altitude axis (z-axis)
ax.set_zticks(altitude_approx)
ax.set_zticklabels(altitude_approx)
ax.invert_zaxis()  # Higher altitude (lower pressure) at top

# Set viewing angle
ax.view_init(elev=25, azim=-45)

# Customize grid
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.grid(True, linestyle='--', alpha=0.4)

# Set axis limits
ax.set_xlim(-180, 180)
ax.set_ylim(-90, 90)
ax.set_zlim(altitude_approx[0]+1, altitude_approx[-1]-1)

# Add STANDARD (non-inverted) colorbar
sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, 
                          norm=plt.Normalize(vmin=pressure_levels.min(), vmax=pressure_levels.max()))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, shrink=0.5, aspect=20, pad=0.1)
cbar.set_label('Pressure level (hPa)', rotation=270, labelpad=20)

plt.tight_layout()
plt.savefig('3d_atmospheric_levels.png', dpi=300, bbox_inches='tight')
plt.show()
exit()

