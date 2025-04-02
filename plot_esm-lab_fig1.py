# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilvae@gmail.com"
__date__        = "March 31, 2025"
__description__ = "ESM LAB session "

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.interpolate import griddata

# Set up figure
fig = plt.figure(figsize=(18, 6))
plt.suptitle("CDO remapbil: CMIP6 → ERA5 regridding over Europe", fontsize=16, y=1.05)

# Europe domain boundaries
lon_bounds = [-15, 25]
lat_bounds = [35, 60]

# Panel 1
ax1 = fig.add_subplot(131, projection=ccrs.PlateCarree())
ax1.set_title("CMIP6 original grid (1.5° resolution)", pad=12)

# Create CMIP6 grid (1.5° resolution)
lons_cmip = np.arange(-180, 180, 1.5)
lats_cmip = np.arange(-90, 91, 1.5)
lon_c, lat_c = np.meshgrid(lons_cmip, lats_cmip)
data_cmip = np.sin(np.radians(lon_c)) * np.cos(np.radians(lat_c))

# Plot only European points
europe_mask = (lon_c >= lon_bounds[0]) & (lon_c <= lon_bounds[1]) & \
              (lat_c >= lat_bounds[0]) & (lat_c <= lat_bounds[1])
ax1.scatter(lon_c[europe_mask], lat_c[europe_mask], color='red', s=15, transform=ccrs.PlateCarree(), label=f'CMIP6 points: {np.sum(europe_mask)}')

# Add map features
ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.8)
ax1.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
ax1.set_extent([lon_bounds[0]-5, lon_bounds[1]+5, lat_bounds[0]-5, lat_bounds[1]+5])
ax1.legend(loc='lower left')

# Panel 2
ax2 = fig.add_subplot(132, projection=ccrs.PlateCarree())
ax2.set_title("ERA5 target grid (0.25° resolution)", pad=12)

# Create ERA5 grid (0.25° resolution)
lons_era = np.arange(-180, 180, 0.25)
lats_era = np.arange(-90, 90.25, 0.25)
lon_e, lat_e = np.meshgrid(lons_era, lats_era)
data_era = np.sin(np.radians(lon_e*0.9)) * np.cos(np.radians(lat_e*0.9))

# Plot only European points
europe_mask = (lon_e >= lon_bounds[0]) & (lon_e <= lon_bounds[1]) & \
              (lat_e >= lat_bounds[0]) & (lat_e <= lat_bounds[1])
ax2.scatter(lon_e[europe_mask], lat_e[europe_mask], color='red', s=3, transform=ccrs.PlateCarree(), label=f'ERA5 points: {np.sum(europe_mask)}')

# Map features
ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.8)
ax2.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
ax2.set_extent([lon_bounds[0]-5, lon_bounds[1]+5, lat_bounds[0]-5, lat_bounds[1]+5])
ax2.legend(loc='lower left')

# Panel 3
ax3 = fig.add_subplot(133, projection=ccrs.PlateCarree())
ax3.set_title("Regridded CMIP6 (to ERA5 grid)", pad=12)

# Simulate regridding using bilinear interpolation
points = np.column_stack((lon_c.flatten(), lat_c.flatten()))
values = data_cmip.flatten()
grid = np.column_stack((lon_e.flatten(), lat_e.flatten()))
data_regrid = griddata(points, values, grid, method='linear').reshape(lon_e.shape)

# Plot only European points (same as ERA5)
ax3.scatter(lon_e[europe_mask], lat_e[europe_mask], color='red', s=3, transform=ccrs.PlateCarree(), label=f'Regridded points: {np.sum(europe_mask)}')

# Show original CMIP6 grid locations
ax3.scatter(lon_c, lat_c, color='black', s=2, transform=ccrs.PlateCarree(), alpha=0.3, label='Original CMIP6 grid')

# Map features
ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.8)
ax3.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
ax3.set_extent([lon_bounds[0]-5, lon_bounds[1]+5, lat_bounds[0]-5, lat_bounds[1]+5])
ax3.legend(loc='lower left')

# Add process arrows
fig.text(0.31, 0.25, "CDO remapbil", ha='center', va='center', fontsize=12, bbox=dict(boxstyle='rarrow,pad=0.5', fc='lightblue'))

# Add explanatory text
fig.text(0.5, 0.05, "Note: Red dots show actual grid points. After regridding, CMIP6 data exists at all ERA5 grid points.", ha='center', fontsize=10)

plt.tight_layout()
plt.savefig("cdo_remapbil_gridpoints_europe.png", dpi=300, bbox_inches='tight')
plt.show()
exit()
