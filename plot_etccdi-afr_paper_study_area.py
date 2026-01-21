# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "September 10, 2025"
__description__ = "This script plot map of genesis"

import os
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import matplotlib.patches as mpatches

from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# Open the file
file = '/home/mda_silv/clima-archive2-b/ETCCDI_paper/CORDEX/AFR-22/RegCM4/ECMWF-ERAINT/orog_AFR-22_ECMWF-ERAINT_evaluation_r1i1p1_ICTP-RegCM4-7_v0_fx.nc'
ds = xr.open_dataset(file)
alt = ds['orog']
lons = ds['lon']
lats = ds['lat']

# Create figure
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
lon1, lon2, lat1, lat2 = -20, 60, -40, 40

contour = ax.contourf(
    lons, lats, alt,
    levels=50,              
    cmap='terrain',
    extend='max',
    transform=ccrs.PlateCarree()
)

ax.set_extent([lon1, lon2, lat1, lat2], crs=ccrs.PlateCarree())
ax.set_xticks(np.arange(lon1,lon2,10), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(lat1,lat2,10), crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.grid(c='k', ls='--', alpha=0.5)       
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.coastlines(resolution='10m')
ax.add_feature(cfeature.OCEAN, facecolor='white', zorder=1)

cbar = plt.colorbar(contour, ax=ax, orientation='vertical', shrink=0.7, pad=0.05)
cbar.set_label('Topography (m)', fontweight='bold')

# Add red rectangle
lon_min, lon_max = -18, 15   
lat_min, lat_max = 4, 18   

rect = mpatches.Rectangle(
    (lon_min, lat_min),           
    lon_max - lon_min,          
    lat_max - lat_min,           
    linewidth=2,
    edgecolor='red',
    facecolor='none',
    transform=ccrs.PlateCarree()
)
ax.add_patch(rect)

# Middle coordinates
lon_mid = (lon_min + lon_max) / 2
lat_mid = (lat_min + lat_max) / 2

# Horizontal dashed line in the middle
ax.plot([lon_min, lon_max], [lat_mid, lat_mid],
        color='red', linestyle='--', linewidth=1.5,
        transform=ccrs.PlateCarree())

# Add labels for zones
ax.text((lon_min + lon_max)/2, (lat_mid + lat_max)/2, 'Sahel Zone',
        color='black', fontweight='bold',
        ha='center', va='center', transform=ccrs.PlateCarree())

ax.text((lon_min + lon_max)/2, (lat_min + lat_mid)/2, 'Coastal Zone',
        color='black', fontweight='bold',
        ha='center', va='center', transform=ccrs.PlateCarree())

ax.text(-16, -36, u'\u25B2 \nN', color='black', fontweight='bold')

# Path out to save figure
path_out = '/home/mda_silv/clima-archive2-b/ETCCDI_paper/figs'
name_out = 'pyplt_maps_study_area_cordex_afr-22.png'
plt.savefig(os.path.join(path_out, name_out), dpi=400, bbox_inches='tight')
plt.show()
exit()

