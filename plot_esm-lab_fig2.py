# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilvae@gmail.com"
__date__        = "March 31, 2025"
__description__ = "ESM LAB session plots"

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.interpolate import griddata

# Set up figure
fig = plt.figure(figsize=(20, 10))
plt.suptitle("CDO grid remapping: CMIP6 → ERA5 method comparison", fontsize=18, y=1.0)

# Europe domain
lon_bounds = [-15, 25]
lat_bounds = [35, 60]

# Panel 1
ax1 = fig.add_subplot(231, projection=ccrs.PlateCarree())
ax1.set_title("CMIP6 original grid (1.5°)", pad=10)

# Create CMIP6 grid
lons_cmip = np.arange(-180, 180, 1.5)
lats_cmip = np.arange(-90, 91, 1.5)
lon_c, lat_c = np.meshgrid(lons_cmip, lats_cmip)
data_cmip = np.sin(np.radians(lon_c)) * np.cos(np.radians(lat_c))

# Plot Europe points
europe_mask = (lon_c >= lon_bounds[0]) & (lon_c <= lon_bounds[1]) & \
              (lat_c >= lat_bounds[0]) & (lat_c <= lat_bounds[1])
ax1.scatter(lon_c[europe_mask], lat_c[europe_mask], color='red', s=20, transform=ccrs.PlateCarree(), label=f'{np.sum(europe_mask)} points')

# Map features
ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.8)
ax1.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
ax1.set_extent([lon_bounds[0]-5, lon_bounds[1]+5, lat_bounds[0]-5, lat_bounds[1]+5])
ax1.legend(loc='lower left')

# Panel 2
ax2 = fig.add_subplot(232, projection=ccrs.PlateCarree())
ax2.set_title("ERA5 target grid (0.25°)", pad=10)

# Create ERA5 grid
lons_era = np.arange(-180, 180, 0.25)
lats_era = np.arange(-90, 90.25, 0.25)
lon_e, lat_e = np.meshgrid(lons_era, lats_era)

# Plot Europe points
europe_mask = (lon_e >= lon_bounds[0]) & (lon_e <= lon_bounds[1]) & \
              (lat_e >= lat_bounds[0]) & (lat_e <= lat_bounds[1])
ax2.scatter(lon_e[europe_mask], lat_e[europe_mask], color='red', s=2, transform=ccrs.PlateCarree(), label=f'{np.sum(europe_mask)} points')

# Map features
ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.8)
ax2.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
ax2.set_extent([lon_bounds[0]-5, lon_bounds[1]+5, lat_bounds[0]-5, lat_bounds[1]+5])
ax2.legend(loc='lower left')

# Panel 3
ax3 = fig.add_subplot(233, projection=ccrs.PlateCarree())
ax3.set_title("Bilinear (remapbil)", pad=10)

# Simulate bilinear regridding
data_bilin = griddata(np.column_stack((lon_c.flatten(), lat_c.flatten())), data_cmip.flatten(), np.column_stack((lon_e.flatten(), lat_e.flatten())), method='linear').reshape(lon_e.shape)
ax3.scatter(lon_e[europe_mask], lat_e[europe_mask], color='red', s=2, transform=ccrs.PlateCarree())

# Panel 4
ax4 = fig.add_subplot(234, projection=ccrs.PlateCarree())
ax4.set_title("Nearest neighbor (remapnn)", pad=10)

data_nn = griddata(np.column_stack((lon_c.flatten(), lat_c.flatten())), data_cmip.flatten(), np.column_stack((lon_e.flatten(), lat_e.flatten())), method='nearest').reshape(lon_e.shape)
ax4.scatter(lon_e[europe_mask], lat_e[europe_mask], color='red', s=2, transform=ccrs.PlateCarree())

# Panel 5
ax5 = fig.add_subplot(235, projection=ccrs.PlateCarree())
ax5.set_title("Conservative (remapcon)", pad=10)

# Simplified conservative remapping visualization
data_con = griddata(np.column_stack((lon_c.flatten(), lat_c.flatten())), data_cmip.flatten(), np.column_stack((lon_e.flatten(), lat_e.flatten())), method='linear').reshape(lon_e.shape)
data_con = np.where(data_con < -0.5, -0.5, data_con)  
ax5.scatter(lon_e[europe_mask], lat_e[europe_mask], color='red', s=2, transform=ccrs.PlateCarree())

# Panel 6
ax6 = fig.add_subplot(236)
methods = ['Bilinear', 'Nearest', 'Conservative']
rmse_values = [0.12, 0.25, 0.18]  # Example values
bars = ax6.bar(methods, rmse_values, color=['blue', 'orange', 'green'])
ax6.set_title("Method comparison (RMSE vs ERA5)")
ax6.set_ylabel("RMSE")
ax6.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax6.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig("cdo_regrid_comparison.png", dpi=300, bbox_inches='tight')
plt.show()
exit()

