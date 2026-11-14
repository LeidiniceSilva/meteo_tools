# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "November 13, 2026"
__description__ = "This script plot map of study area"

import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter


def get_border_mask(topo, number=9):
	"""Return a mask with 1 on the outer 'number' grid points of the domain and NaN elsewhere."""
	ny, nx = topo.shape
	border_mask = np.full((ny, nx), np.nan)
	border_mask[:number, :] = 1
	border_mask[-number:, :] = 1
	border_mask[:, :number] = 1
	border_mask[:, -number:] = 1
	return border_mask


# Open the CORDEX topography file
file = "/leonardo_work/ICT26_ESP/CORDEX-CMIP6/DD/SAM-12/ICTP/ERA5/evaluation/r1i1p1f1/RegCM5-0/v1-r1/fx/orog/orog_SAM-12_ERA5_evaluation_r1i1p1f1_ICTP_RegCM5-0_v1-r1_fx.nc"
ds = xr.open_dataset(file)
alt = ds["orog"]
lons = ds["lon"]
lats = ds["lat"]

# Domain border mask (same approach as the previous code)
number = 9
border_mask = get_border_mask(alt.values, number=number)

# Load the IPCC WGI reference regions shapefile
shapefile_path = ("/leonardo/home/userexternal/mdasilva/leonardo_work/Mask/IPCC-WGI-land-reference-regions-v5.shp")
regions_gdf = gpd.read_file(shapefile_path)
print(regions_gdf)

# Filter only South America continent regions
sam_gdf = regions_gdf[regions_gdf["CONTINENT"] == "SOUTH-AMERICA"]

# Create figure
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={"projection": ccrs.PlateCarree()})
lon1, lon2, lat1, lat2 = -110, -15, -60, 20

# Plot topography contour
contour = ax.contourf(lons, lats, alt, levels=50, cmap="terrain", extend="max", transform=ccrs.PlateCarree(),)

# Plot domain border (gray band along the edge of the CORDEX domain)
ax.contourf(lons, lats, border_mask, cmap="gray", levels=[0, 1], transform=ccrs.PlateCarree(), zorder=1.5)

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

ax.add_geometries(sam_gdf["geometry"], crs=ccrs.PlateCarree(), facecolor="none", edgecolor="black", linewidth=1., zorder=2,)

for _, row in sam_gdf.iterrows():
    centroid = row['geometry'].centroid
    print(row)
    ax.text(centroid.x, centroid.y, row['ACRONYM'], color='red', fontsize=8, fontweight='bold', ha='center', va='center', transform=ccrs.PlateCarree(), bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='none'))

# North arrow indicator
ax.text(-105, -58, u"\u25B2 \nN", color="black", fontweight="bold")

# Path out to save figure
path_out = "/leonardo/home/userexternal/mdasilva/leonardo_work/ENSO/figs"
name_out = "pyplt_maps_study_area_cordex_sa-12_ipcc_regions.png"
plt.savefig(os.path.join(path_out, name_out), dpi=400, bbox_inches="tight")
plt.show()
exit()
