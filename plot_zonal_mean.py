# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "May 19, 2025"
__description__ = "This script plot zonal mean"

from netCDF4 import Dataset, num2date
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap, BoundaryNorm

# Read dataset and extract variables
ds = Dataset('tisr_ERA5_day_1991_unit_ymonmean_zonalmean.nc')
tisr = np.squeeze(ds.variables['tisr'][:])       
lat = ds.variables['lat'][:]
time = ds.variables['valid_time'][:]
time_units = ds.variables['valid_time'].units
time_calendar = ds.variables['valid_time'].calendar
dates = num2date(time, units=time_units, calendar=time_calendar)

# Transpose for (lat, time)
tisr_plot = tisr.T

# Set up color levels
vmin, vmax = np.nanmin(tisr_plot), np.nanmax(tisr_plot)
levels = np.linspace(vmin, vmax, 30)

# Create a custom colormap where 0 values are white
cmap = plt.get_cmap('jet', len(levels) - 1)
newcolors = cmap(np.linspace(0, 1, len(levels) - 1))

# Identify which bin contains 0
zero_index = np.digitize([0], levels)[0] - 1  # adjust to 0-based index

# Replace color at zero bin with white
if 0 <= zero_index < len(newcolors):
    newcolors[zero_index] = [1, 1, 1, 1]  # RGBA for white

custom_cmap = ListedColormap(newcolors)
norm = BoundaryNorm(levels, custom_cmap.N)

# Create meshgrid for plotting
X, Y = np.meshgrid(np.arange(len(dates)), lat)

# Plot
plt.figure(figsize=(12, 6))
contour = plt.contourf(X, Y, tisr_plot, levels=levels, cmap=custom_cmap, norm=norm, extend='neither')
plt.colorbar(contour, label='TISR (W/m²)')

# Format time axis
plt.xticks(
    ticks=np.arange(len(dates)),
    labels=[d.strftime('%b') for d in dates],
    rotation=45
)

plt.title("Top-of-Atmosphere Insolation (TISR)")
plt.xlabel("Time (Months of 1991)")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()
exit()

