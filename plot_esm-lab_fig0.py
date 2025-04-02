# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilvae@gmail.com"
__date__        = "March 31, 2025"
__description__ = "ESM LAB session plots"

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# Define grid dimensions
num_time = 5    # Number of time steps
num_lat = 6     # Number of latitude points
num_lon = 6     # Number of longitude points

# Generate grid coordinates
time_steps = np.arange(num_time)
latitudes = np.linspace(-90, 90, num_lat)
longitudes = np.linspace(-180, 180, num_lon)

# Create figure and 3D axis with adjusted viewing parameters
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Create colormap for time dimension
cmap = plt.cm.plasma
norm = Normalize(vmin=0, vmax=num_time-1)
mappable = ScalarMappable(norm=norm, cmap=cmap)

# Function to draw properly scaled voxels
def draw_voxel(lon_idx, lat_idx, t_idx, color):
    # Calculate actual coordinate ranges for each voxel
    lon_width = 360/num_lon
    lat_width = 180/num_lat
    time_height = 1
    
    # Base coordinates
    lon_start = longitudes[lon_idx]
    lat_start = latitudes[lat_idx]
    time_start = time_steps[t_idx]
    
    # Define all 8 vertices of the voxel
    vertices = [
        [lon_start, lat_start, time_start],
        [lon_start + lon_width, lat_start, time_start],
        [lon_start + lon_width, lat_start + lat_width, time_start],
        [lon_start, lat_start + lat_width, time_start],
        [lon_start, lat_start, time_start + time_height],
        [lon_start + lon_width, lat_start, time_start + time_height],
        [lon_start + lon_width, lat_start + lat_width, time_start + time_height],
        [lon_start, lat_start + lat_width, time_start + time_height]
    ]
    
    # Define the 6 faces of the voxel
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Bottom
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Top
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # Front
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # Back
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # Right
        [vertices[3], vertices[0], vertices[4], vertices[7]]   # Left
    ]
    
    ax.add_collection3d(Poly3DCollection(faces, 
                                      facecolors=color,
                                      edgecolor='k',
                                      linewidths=0.3,
                                      alpha=0.7))

# Plot all voxels
for t_idx in range(num_time):
    for lat_idx in range(num_lat):
        for lon_idx in range(num_lon):
            draw_voxel(lon_idx, lat_idx, t_idx, mappable.to_rgba(t_idx))

# Set labels with larger font and padding
ax.set_xlabel("Longitude (°)", fontsize=12, labelpad=20)
ax.set_ylabel("Latitude (°)", fontsize=12, labelpad=20)
ax.set_zlabel("Time Step", fontsize=12, labelpad=20)

# Set title
ax.set_title("3D NetCDF Structure Visualization\n(Longitude × Latitude × Time)", 
             fontsize=14, pad=25)

# Set axis limits with padding
ax.set_xlim([-180, 180])
ax.set_ylim([-90, 90])
ax.set_zlim([0, num_time])

# Add colorbar
cbar = fig.colorbar(mappable, ax=ax, shrink=0.6, aspect=20, pad=0.1)
cbar.set_label('Time Progression', rotation=270, labelpad=20)

# Adjust viewing angle to ensure all axes are visible
ax.view_init(elev=30, azim=-120)  # Changed viewing angle

# Force all axes to be visible by disabling axis panes
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

# Add grid lines
ax.grid(True, linestyle=':', alpha=0.5)

# Ensure tight layout
plt.tight_layout()
plt.show()



