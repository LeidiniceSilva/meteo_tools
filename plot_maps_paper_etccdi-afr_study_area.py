# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "September 10, 2025"
__description__ = "This script plot map of study area"

import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

# Open the CORDEX topography file
file = "/home/mda_silv/clima-archive2-b/ETCCDI/CORDEX/AFR-22/RegCM4/ECMWF-ERAINT/orog_AFR-22_ECMWF-ERAINT_evaluation_r1i1p1_ICTP-RegCM4-7_v0_fx.nc"
ds = xr.open_dataset(file)
alt = ds["orog"]
lons = ds["lon"]
lats = ds["lat"]

# Load the IPCC WGI reference regions shapefile
shapefile_path = ("/home/clima-archive4-b/nzazulie/trendsCORDEX/IPCC-WGI-land-reference-regions-v5.shp")
regions_gdf = gpd.read_file(shapefile_path)

# Filter only Africa continent regions
africa_gdf = regions_gdf[regions_gdf["CONTINENT"] == "AFRICA"]

# Create figure
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={"projection": ccrs.PlateCarree()})
lon1, lon2, lat1, lat2 = -25, 60, -40, 40

# Plot topography contour
contour = ax.contourf(lons, lats, alt, levels=50, cmap="terrain", extend="max", transform=ccrs.PlateCarree(),)

ax.set_extent([lon1, lon2, lat1, lat2], crs=ccrs.PlateCarree())
ax.set_xticks(np.arange(lon1, lon2, 10), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(lat1, lat2, 10), crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.grid(c="gray", ls="--", alpha=0.75)
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.coastlines(resolution="10m")
ax.add_feature(cfeature.OCEAN, facecolor="white", zorder=1)

cbar = plt.colorbar(contour, ax=ax, orientation="vertical", shrink=0.7, pad=0.05)
cbar.set_label("Topography (m)", fontweight="bold")

ax.add_geometries(africa_gdf["geometry"], crs=ccrs.PlateCarree(), facecolor="none", edgecolor="black", linewidth=1., zorder=2,)

for _, row in africa_gdf.iterrows():
    centroid = row['geometry'].centroid
    print(row)
    ax.text(centroid.x, centroid.y, row['ACRONYM'], color='red', fontsize=8, fontweight='bold', ha='center', va='center', transform=ccrs.PlateCarree(), bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='none'))

# North arrow indicator
ax.text(-16, -36, u"\u25B2 \nN", color="black", fontweight="bold")

# Path out to save figure
path_out = "/home/mda_silv/clima-archive2-b/ETCCDI/figs"
name_out = "pyplt_maps_study_area_cordex_afr-22_ipcc_regions.png"
plt.savefig(os.path.join(path_out, name_out), dpi=400, bbox_inches="tight")
plt.show()
exit()
